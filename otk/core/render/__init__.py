"""Rendering back-ends. matplotlib (PDF/print) lives here and *only* here — the
interactive quiz renders in the browser with KaTeX."""

from .pdf import render_edit_preview, render_page_png, render_pdf
from .fonts import default_thai_font

__all__ = ["render_pdf", "render_page_png", "render_edit_preview", "default_thai_font"]
