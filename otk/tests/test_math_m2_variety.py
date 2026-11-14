"""The ม.2 sets added for variety across the units: each answer is worked out again here from the stem alone.

Geometry is checked by building the figure in coordinates where that is the natural check (the ladder, the
box, the isosceles height, the angle bisector, the parallel-line angles); everything else by solving what the
stem states, with exact fractions.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from random import Random
from statistics import median, mode

from otk.core import generate

SEEDS = range(300)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"-?\d+", s.replace(",", "").replace("−", "-"))]


def _lin(s: str) -> tuple[int, int]:
    """'2x + 3', '5x − 9', 'x' → (m, c)."""
    m = re.fullmatch(r"(\d*)x(?: ([+−]) (\d+))?", s.strip())
    assert m, s
    return int(m.group(1) or 1), int(m.group(3) or 0) * (-1 if m.group(2) == "−" else 1)


def _angle(at, p, q) -> float:
    a1 = math.atan2(p[1] - at[1], p[0] - at[0])
    a2 = math.atan2(q[1] - at[1], q[0] - at[0])
    d = abs(math.degrees(a1 - a2)) % 360
    return min(d, 360 - d)


# ── ความเท่ากันทุกประการ ──

def test_correspondence_reads_letters_by_position():
    for seed in SEEDS:
        stem, right, _ = _q("congruence_correspondence_m2", seed)
        first, second = re.search(r"△(\w{3}) ≅ △(\w{3})", stem).groups()
        pair = dict(zip(first, second))
        if "ด้าน" in stem:
            side = re.search(r"ด้าน (\w\w) สมนัย", stem).group(1)
            assert set(right.removeprefix("ด้าน ")) == {pair[side[0]], pair[side[1]]}, stem
        else:
            assert right == "∠" + pair[re.search(r"∠(\w) สมนัย", stem).group(1)], stem


_CASES = {"ด.ม.ด.": ("s", "a", "s"), "ม.ด.ม.": ("a", "s", "a"), "ด.ด.ด.": ("s", "s", "s")}


def _parts(conditions: str) -> list[tuple[str, frozenset]]:
    out = []
    for c in re.split(r", | และ ", conditions):
        left = c.split(" = ")[0]
        out.append(("a", frozenset(left[1])) if left.startswith("∠") else ("s", frozenset(left)))
    return out


def _proves(parts: list[tuple[str, frozenset]]) -> str | None:
    """Which case three parts of ABC make, or None when they prove nothing."""
    sides = [p for k, p in parts if k == "s"]
    angles = [next(iter(p)) for k, p in parts if k == "a"]
    if len(parts) != 3:
        return None
    if len(sides) == 3:
        return "ด.ด.ด."
    if len(sides) == 2:
        between = next(iter(sides[0] & sides[1]))
        return "ด.ม.ด." if angles[0] == between else None
    if len(sides) == 1:
        return "ม.ด.ม." if set(angles) == set(sides[0]) else "ม.ม.ด."
    return None


def test_missing_condition_completes_the_named_case():
    for seed in SEEDS:
        stem, right, texts = _q("congruence_missing_condition_m2", seed)
        given = re.search(r"มี (.+) ถ้าต้องการ", stem).group(1)
        case = re.search(r"กรณี (\S+) ต้อง", stem).group(1)
        for t in texts:
            made = _proves(_parts(given) + _parts(t))
            assert (made == case) == (t == right), (stem, t, made)


def test_not_enough_finds_the_odd_one():
    for seed in SEEDS:
        stem, right, texts = _q("congruence_not_enough_m2", seed)
        want_enough = "ไม่เพียงพอ" not in stem
        for t in texts:
            enough = _proves(_parts(t)) is not None
            assert (enough == want_enough) == (t == right), (stem, t)


def test_sides_and_angles_in_x():
    for seed in SEEDS:
        stem, right, _ = _q("congruence_sides_algebra_m2", seed)
        first, second = re.search(r"△(\w{3}) ≅ △(\w{3})", stem).groups()
        a, ea, b, eb = re.search(r"ถ้า (\w\w) = (.+?) เซนติเมตร และ (\w\w) = (.+?) เซนติเมตร", stem).groups()
        pair = dict(zip(first, second))
        assert {pair[a[0]], pair[a[1]]} == set(b), stem
        (m1, c1), (m2, c2) = _lin(ea), _lin(eb)
        x = Fraction(c2 - c1, m1 - m2)
        assert x.denominator == 1 and m1 * x + c1 > 0
        assert int(right) == (x if "x มีค่า" in stem else m1 * x + c1), stem
    for seed in SEEDS:
        stem, right, _ = _q("congruence_angles_algebra_m2", seed)
        first, second = re.search(r"△(\w{3}) ≅ △(\w{3})", stem).groups()
        pair = dict(zip(first, second))
        a, ea, b, eb = re.search(r"∠(\w) = \((.+?)\)°(?:,| และ) ∠(\w) = \((.+?)\)°", stem).groups()
        assert pair[a] == b
        (m1, c1), (m2, c2) = _lin(ea), _lin(eb)
        x = Fraction(c2 - c1, m1 - m2)
        angle = m1 * x + c1
        if "x มีค่า" in stem:
            assert int(right) == x
            continue
        c, other, asked = re.search(r"และ ∠(\w) = (\d+)° แล้ว ∠(\w)", stem).groups()
        # The angles of ABC: a is `angle`, c is `other`, the third fills 180°.
        known = {a: angle, c: int(other)}
        third = next(v for v in first if v not in known)
        known[third] = 180 - sum(known.values())
        back = {v: k for k, v in pair.items()}
        assert int(right) == known[back[asked]] and all(0 < v < 180 for v in known.values()), stem


def test_proof_reasons_are_distinct():
    for seed in SEEDS:
        _q("congruence_proof_reason_m2", seed)


# ── การให้เหตุผลทางเรขาคณิต and เส้นขนาน ──

def _deg_exprs(stem: str) -> list[tuple[str, int, int]]:
    out = []
    for name, body in re.findall(r"∠(\w+) = \(?([^()°]+?)\)?°", stem):
        if "x" in body:
            out.append((name, *_lin(body)))
    return out


def test_triangle_angles_add_to_180():
    for seed in SEEDS:
        stem, right, _ = _q("triangle_angle_algebra_m2", seed)
        if "อัตราส่วน" in stem:
            p, q, r = (int(n) for n in re.search(r"(\d+) : (\d+) : (\d+)", stem).groups())
            assert Fraction(180 * r, p + q + r) == int(right)
            continue
        exprs = _deg_exprs(stem)
        m, c = sum(e[1] for e in exprs), sum(e[2] for e in exprs)
        x = Fraction(180 - c, m)
        assert x.denominator == 1
        if "ค่า x" in stem:
            assert int(right) == x
        else:
            asked = re.search(r"ขนาดของ ∠(\w)", stem).group(1)
            e = next(e for e in exprs if e[0] == asked)
            assert int(right) == e[1] * x + e[2]


def test_polygon_exterior():
    for seed in SEEDS:
        stem, right, _ = _q("polygon_exterior_m2", seed)
        if stem.startswith("รูป ") and "แต่ละมุมขนาดกี่" in stem:
            n = _ints(stem)[0]
            assert Fraction(360, n) == int(right)
        else:
            angle = _ints(stem)[0]
            exterior = angle if "มุมภายนอก" in stem else 180 - angle
            assert Fraction(360, exterior) == int(right)


def test_triangle_inequality_by_trying_every_length():
    for seed in SEEDS:
        stem, right, _ = _q("triangle_inequality_m2", seed)
        a, b = _ints(stem)[:2]
        possible = [c for c in range(1, a + b + 5) if a + b > c and a + c > b and b + c > a]
        expected = max(possible) if "มากที่สุด" in stem else min(possible) if "น้อยที่สุด" in stem else len(possible)
        assert int(right) == expected, stem


def test_vertical_and_straight_angles():
    for seed in SEEDS:
        stem, right, _ = _q("vertical_angles_algebra_m2", seed)
        (n1, m1, c1), (n2, m2, c2) = _deg_exprs(stem)
        # On lines AB and CD through O, ∠AOC and ∠BOD are opposite; ∠AOC and ∠COB share the ray OC.
        x = Fraction(c2 - c1, m1 - m2) if n2 == "BOD" else Fraction(180 - c1 - c2, m1 + m2)
        assert x.denominator == 1 and 0 < m1 * x + c1 < 180 and 0 < m2 * x + c2 < 180
        assert int(right) == (x if "ค่า x" in stem else m1 * x + c1), stem


def test_angle_bisector_in_coordinates():
    for seed in SEEDS:
        stem, right, _ = _q("angle_bisector_triangle_m2", seed)
        b, c = _ints(stem)[:2]
        B, C = (0.0, 0.0), (10.0, 0.0)
        # A from the base angles: the rays from B and C meet.
        tb, tc = math.tan(math.radians(b)), math.tan(math.radians(c))
        ax = 10 * tc / (tb + tc)
        A = (ax, ax * tb)
        half = _angle(A, B, C) / 2
        # D on BC where the ray from A at half the angle from AB meets y = 0.
        lo, hi = 0.0, 10.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if _angle(A, B, (mid, 0.0)) < half:
                lo = mid
            else:
                hi = mid
        D = (lo, 0.0)
        asked = re.search(r"ขนาดของ ∠(\w+)", stem).group(1)
        got = {"BAD": _angle(A, B, D), "ADC": _angle(D, A, C), "ADB": _angle(D, A, B)}[asked]
        assert round(got) == int(right), stem


def test_isosceles_converse():
    for seed in SEEDS:
        stem, right, _ = _q("isosceles_sides_m2", seed)
        e1, e2 = re.search(r"AB = (.+?) เซนติเมตร(?:,| และ) AC = (.+?) เซนติเมตร", stem).groups()
        (m1, c1), (m2, c2) = _lin(e1), _lin(e2)
        x = Fraction(c2 - c1, m1 - m2)
        side = m1 * x + c1
        if "ค่า x" in stem:
            assert int(right) == x
        else:
            base = int(re.search(r"BC = (\d+)", stem).group(1))
            assert base < 2 * side and int(right) == 2 * side + base


def test_named_angles_measured_on_a_drawing():
    for seed in SEEDS:
        stem, right, _ = _q("parallel_named_angle_m2", seed)
        given, v, asked = re.search(r"ถ้า ∠(\w+) = (\d+)° จงหาขนาดของ ∠(\w+)", stem).groups()
        v = int(v)
        for u in (v, 180 - v):
            # AB on y = 1, CD on y = 0, EF through G = (0, 1) and H at angle u to GB, E up and F down.
            d = (math.cos(math.radians(u)), math.sin(math.radians(u)))
            G = (0.0, 1.0)
            H = (G[0] - d[0] / d[1], 0.0)
            pts = {"A": (-5, 1), "B": (5, 1), "C": (-5, 0), "D": (5, 0), "G": G, "H": H,
                   "E": (G[0] + d[0], G[1] + d[1]), "F": (H[0] - d[0], H[1] - d[1])}

            def ang(name):
                return round(_angle(pts[name[1]], pts[name[0]], pts[name[2]]))

            if ang(given) == v:
                assert ang(asked) == int(right), stem
                break
        else:
            raise AssertionError(stem)


# ── พื้นที่ผิวและปริมาตร ──

PI = Fraction(22, 7)


def test_volumes():
    for seed in SEEDS:
        stem, right, _ = _q("prism_volume_base_m2", seed)
        n = _ints(stem)
        if "สี่เหลี่ยมจัตุรัส" in stem:
            assert int(right) == n[0] ** 2 * n[1]
        elif re.search(r"มีปริมาตร \d", stem):
            assert int(right) * n[1] == n[0]
        else:
            assert int(right) == n[0] * n[1]
        stem, right, _ = _q("cylinder_dimension_m2", seed)
        n = _ints(stem.replace("22/7", ""))
        if stem.startswith("ทรงกระบอกรัศมี"):
            r, vol = n[:2]
            assert PI * r * r * int(right) == vol
        else:
            h, vol = n[:2]
            assert PI * int(right) ** 2 * h == vol
        stem, right, _ = _q("volume_litres_m2", seed)
        n = _ints(stem.replace("1,000", ""))
        if stem.startswith("ตู้ปลา"):
            assert Fraction(n[0] * n[1] * n[2], 1000) == int(right)
        else:
            assert n[0] * n[1] * int(right) == n[2] * 1000
        stem, right, _ = _q("hollow_cylinder_m2", seed)
        h, big, small = _ints(stem.replace("22/7", ""))[:3]
        assert PI * (big * big - small * small) * h == int(right)
        stem, right, _ = _q("box_with_hole_m2", seed)
        w, d, h, r = _ints(stem.replace("22/7", ""))[:4]
        assert w * d * h - PI * r * r * h == int(right)


def test_scaling_by_measuring_two_solids():
    for seed in SEEDS:
        stem, right, _ = _q("scale_volume_m2", seed)
        k = _ints(stem)[0]
        if "กล่อง" in stem:
            w, d, h = 3, 4, 5
            before = w * d * h if "ปริมาตร" in stem else 2 * (w * d + d * h + w * h)
            after = k ** 3 * before if "ปริมาตร" in stem else 2 * k * k * (w * d + d * h + w * h)
        else:
            r, h = 7, 10
            before = PI * r * r * h
            after = PI * (k * r) ** 2 * h if "รัศมีเป็น" in stem else PI * r * r * k * h
        assert Fraction(after) / before == int(right), stem


# ── ทฤษฎีบทพีทาโกรัส ──

def test_pythagoras_figures():
    for seed in SEEDS:
        stem, right, _ = _q("pythagoras_isosceles_m2", seed)
        side, base = _ints(stem)[:2]
        height = math.isqrt(side * side - (base // 2) ** 2)
        assert height * height + (base // 2) ** 2 == side * side and base % 2 == 0
        assert int(right) == (height if "ส่วนสูง" in stem else base * height // 2)
        stem, right, _ = _q("pythagoras_rectangle_m2", seed)
        c, a = _ints(stem)[:2]
        b = math.isqrt(c * c - a * a)
        assert a * a + b * b == c * c
        expected = b if "อีกด้าน" in stem else a * b if "พื้นที่" in stem else 2 * (a + b)
        assert int(right) == expected
        stem, right, _ = _q("pythagoras_ladder_m2", seed)
        n = _ints(stem)
        length, foot = n[0], n[1]
        top = math.isqrt(length * length - foot * foot)
        assert top * top + foot * foot == length * length
        if "เลื่อนลง" in stem:
            foot2 = foot + n[2]
            top2 = math.isqrt(length * length - foot2 * foot2)
            assert top2 * top2 + foot2 * foot2 == length * length
            assert int(right) == top - top2
        else:
            assert int(right) == top
        stem, right, _ = _q("pythagoras_box_diagonal_m2", seed)
        w, d, h = _ints(stem)[:3]
        assert int(right) ** 2 == w * w + d * d + h * h


# ── จำนวนจริง, สถิติ ──

def test_sqrt_estimates():
    for seed in SEEDS:
        stem, right, _ = _q("sqrt_estimate_m2", seed)
        n = int(re.search(r"\\sqrt\{(\d+)\}", stem).group(1))
        if "จำนวนเต็ม" in stem:
            assert int(right) == round(math.sqrt(n))
        else:
            assert right == f"{math.sqrt(n):.1f}", (n, right)


def test_averages():
    for seed in SEEDS:
        stem, right, _ = _q("mean_median_mode_m2", seed)
        data = [int(v) for v in re.search(r"ได้แก่ ([\d, ]+) จงหา", stem).group(1).split(", ")]
        assert len(data) == _ints(stem)[0]
        word = re.search(r"จงหา(\S+?)ของข้อมูล", stem).group(1)
        expected = {"ค่าเฉลี่ยเลขคณิต": Fraction(sum(data), len(data)), "มัธยฐาน": median(data),
                    "ฐานนิยม": mode(data)}[word]
        assert int(right) == expected
        stem, right, _ = _q("mean_from_frequency_m2", seed)
        scores, counts = (re.search(p, stem).group(1) for p in (r"คะแนน (.+?) จำนวน", r"จำนวน (.+?) คน"))
        xs, fs = _ints(scores), _ints(counts)
        assert Fraction(sum(f * x for f, x in zip(fs, xs)), sum(fs)) == int(right)


# ── การแปลงทางเรขาคณิต ──

def _pt(s: str) -> tuple[int, int]:
    a, b = _ints(s)
    return a, b


def test_reflections_keep_distance_to_the_line():
    for seed in SEEDS:
        stem, right, _ = _q("reflect_line_m2", seed)
        p = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        q = _pt(right)
        line = re.search(r"เส้นตรง (.+?) ภาพ", stem).group(1)
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        if line.startswith("x = "):
            k = int(line[4:])
            assert mid[0] == k and p[1] == q[1]
        elif line.startswith("y = ") and line[4:].lstrip("-").isdigit():
            k = int(line[4:])
            assert mid[1] == k and p[0] == q[0]
        elif line == "y = x":
            assert mid[0] == mid[1] and (q[0] - p[0]) == -(q[1] - p[1])
        else:
            assert mid[0] == -mid[1] and (q[0] - p[0]) == (q[1] - p[1])


def test_translation_from_a_point_and_its_image():
    for seed in SEEDS:
        stem, right, _ = _q("translation_vector_m2", seed)
        a = _pt(re.search(r"A = (\(.+?\))", stem).group(1))
        image = _pt(re.search(r"A′ = (\(.+?\))", stem).group(1))
        move = (image[0] - a[0], image[1] - a[1])
        if "จุด B" in stem:
            b = _pt(re.search(r"B = (\(.+?\))", stem).group(1))
            assert _pt(right) == (b[0] + move[0], b[1] + move[1])
        else:
            assert _pt(right) == move


def test_transformation_properties_are_distinct():
    for seed in SEEDS:
        _q("transformation_property_m2", seed)
