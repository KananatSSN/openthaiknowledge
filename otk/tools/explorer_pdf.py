"""One-page worksheets for the explorer: a page of problems and a page of answers.

Each request draws a fresh sheet from one problem set, with as many questions
as fill the first page, so the PDF is always the problem page and its answer
key (laid out by ``otk.tools.explorer_sheet``). The explorer's "download PDF"
button calls the small server below; nginx forwards ``/api/sheet`` to it.

    python -m otk.tools.explorer_pdf KEY out.pdf      # one sheet to a file
    python -m otk.tools.explorer_pdf --serve           # the server, port 8000

The server takes no input but a set key, which must be a registered key, and
allows each client one sheet every ``COOLDOWN_SECONDS``. Matplotlib is not
thread-safe, so one sheet is drawn at a time.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import tempfile
import threading
import time
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from random import Random
from urllib.parse import parse_qs, quote, urlsplit

from otk.core.registry import REGISTRY
from otk.core.render.assets import shipped_asset
from otk.tools.explorer_sheet import SheetInfo, plan_page, render_sheet, unique_draws

#: Seconds a client waits between two sheets.
COOLDOWN_SECONDS = 30

#: Requests allowed to wait for the drawing lock before the server says busy.
MAX_WAITING = 4


#: Thai fonts preferred for the sheet, in order. The layout measures what it
#: draws, so any of them fits; Loma is the one the image installs.
COMPACT_THAI_FONTS = ("Tahoma", "Leelawadee UI", "Noto Sans Thai", "Loma")


@lru_cache(maxsize=1)
def thai_font() -> str:
    from matplotlib import font_manager

    installed = {font.name for font in font_manager.fontManager.ttflist}
    return next((name for name in COMPACT_THAI_FONTS if name in installed), "")


@lru_cache(maxsize=1)
def logo_path() -> Path:
    """The openthaiknowledge mark (explorer/static/favicon.svg), drawn once as a PNG.

    A purple-to-teal rounded square with an open book and a dot above it.
    """
    from PIL import Image, ImageDraw

    size = 256
    scale = size / 32
    top, bottom = (0x7C, 0x5B, 0xD6), (0x2F, 0x8F, 0x87)
    gradient = Image.new("RGB", (size, size))
    pixels = gradient.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            pixels[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=9 * scale, fill=255)
    mark = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    mark.paste(gradient, (0, 0), mask)

    def pt(x: float, y: float) -> tuple[float, float]:
        return (x * scale, y * scale)

    # The book: two pages meeting at the spine (x = 16), drawn as polygons.
    left = [pt(16, 11.2), pt(13.4, 9.8), pt(10.4, 9.4), pt(7, 10), pt(7, 22),
            pt(10.4, 21.4), pt(13.4, 21.8), pt(16, 23.2)]
    right = [(size - x, y) for x, y in left]
    overlay = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    for page in (left, right):
        draw.polygon(page, fill=(255, 255, 255, 56))
        draw.line(page + [page[0]], fill=(255, 255, 255, 255), width=round(1.7 * scale), joint="curve")
    draw.line([pt(16, 11.2), pt(16, 23.2)], fill=(255, 255, 255, 255), width=round(1.7 * scale))
    r = 1.6 * scale
    draw.ellipse((16 * scale - r, 6 * scale - r, 16 * scale + r, 6 * scale + r), fill=(255, 255, 255, 255))
    mark = Image.alpha_composite(mark, overlay)
    # Written under a temporary name, then renamed into place, so another process
    # drawing a sheet never reads a half-written PNG. The mark is always the same,
    # so a file already there is the one this would write: on Windows it cannot
    # be replaced while that other process has it open, and need not be.
    path = Path(tempfile.gettempdir()) / "otk-explorer-logo.png"
    if path.exists():
        return path
    tmp = path.with_name(f".{path.stem}.{os.getpid()}.tmp")
    mark.save(tmp, format="PNG")
    try:
        os.replace(tmp, path)
    except PermissionError:
        tmp.unlink(missing_ok=True)
        if not path.exists():
            raise
    return path


def sheet_info(key: str) -> SheetInfo:
    spec = REGISTRY[key]
    return SheetInfo(
        title=spec.display_name.get("th", key),
        meta=f"{spec.subject} · {spec.topic}",
        level=spec.level.get("th", ""),
        key=key,
        instructions="เลือกคำตอบที่ถูกต้องที่สุด",
        logo=logo_path(),
        font=thai_font(),
    )


def plan_sheet(key: str, seed: int):
    """Which questions of ``key`` fill the page, drawn from ``seed``, and where they go."""
    if key not in REGISTRY:
        raise KeyError(key)
    draw = unique_draws(REGISTRY[key].generate, Random(seed))
    return plan_page(sheet_info(key), draw, shipped_asset)


def one_page_sheet(key: str, seed: int) -> bytes:
    """A PDF of exactly two pages: the problems that fill one page, then their answers."""
    plan = plan_sheet(key, seed)
    return render_sheet(sheet_info(key), plan, shipped_asset)


class Cooldown:
    """Remembers when each client last got a sheet; forgets clients idle past the window."""

    def __init__(self, seconds: float, clock=time.monotonic) -> None:
        self.seconds = seconds
        self.clock = clock
        self.last: dict[str, float] = {}
        self.lock = threading.Lock()

    def take(self, client: str) -> float:
        """Claim a sheet for ``client``: 0 if allowed now, else the seconds left to wait."""
        with self.lock:
            now = self.clock()
            for other, at in list(self.last.items()):
                if now - at >= self.seconds:
                    del self.last[other]
            if client in self.last:
                return self.seconds - (now - self.last[client])
            self.last[client] = now
            return 0.0

    def release(self, client: str) -> None:
        """Give the claim back, when the sheet could not be drawn."""
        with self.lock:
            self.last.pop(client, None)


COOLDOWN = Cooldown(COOLDOWN_SECONDS)
DRAWING = threading.Lock()
WAITING = threading.BoundedSemaphore(MAX_WAITING)


class SheetHandler(BaseHTTPRequestHandler):
    server_version = "otk-sheets"

    def _json(self, status: int, body: dict, headers: dict | None = None) -> None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802 (the stdlib's name)
        url = urlsplit(self.path)
        if url.path == "/api/health":
            self._json(200, {"ok": True})
            return
        if url.path != "/api/sheet":
            self._json(404, {"error": "not_found"})
            return
        key = parse_qs(url.query).get("key", [""])[0]
        if key not in REGISTRY:
            self._json(404, {"error": "unknown_set"})
            return
        # nginx passes the visitor's address (Cloudflare's CF-Connecting-IP) here;
        # this port is reachable only from nginx, so the header can be trusted.
        client = self.headers.get("X-Client-IP") or self.client_address[0]
        wait = COOLDOWN.take(client)
        if wait > 0:
            seconds = max(1, round(wait))
            self._json(429, {"error": "too_soon", "retry_after": seconds},
                       {"Retry-After": str(seconds)})
            return
        if not WAITING.acquire(blocking=False):
            COOLDOWN.release(client)
            self._json(503, {"error": "busy"}, {"Retry-After": "5"})
            return
        try:
            with DRAWING:
                pdf = one_page_sheet(key, secrets.randbelow(2**31))
        except Exception:
            COOLDOWN.release(client)
            self._json(500, {"error": "render_failed"})
            raise
        finally:
            WAITING.release()
        name = f"otk-{key}.pdf"
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Length", str(len(pdf)))
        self.send_header("Content-Disposition",
                         f"attachment; filename=\"{name}\"; filename*=UTF-8''{quote(name)}")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(pdf)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        # One line per request, without the client's address.
        print(f"{self.command} {urlsplit(self.path).path} {args[1] if len(args) > 1 else ''}", flush=True)


def serve(port: int) -> None:
    logo_path()
    server = ThreadingHTTPServer(("0.0.0.0", port), SheetHandler)
    print(f"otk sheets listening on :{port}", flush=True)
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?")
    parser.add_argument("out", nargs="?", type=Path)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.serve:
        serve(args.port)
        return
    if not args.key or not args.out:
        parser.error("give a set KEY and an OUT file, or --serve")
    seed = args.seed if args.seed is not None else secrets.randbelow(2**31)
    args.out.write_bytes(one_page_sheet(args.key, seed))
    print(args.out)


if __name__ == "__main__":
    main()
