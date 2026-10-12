"""Area model, balance, fraction number line, double bars, dot plot and
histogram: answers re-derived from the spec each picture was drawn from."""

from __future__ import annotations

from otk.tests._origins import keys_from

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_pictures_hi as mh

SEEDS = range(300)
KEYS = keys_from("math_pictures_hi")
SPECS = {s.asset_id: s for s in (*mh.AREA_MODELS, *mh.BALANCES, *mh.FRAC_LINES,
                                 *mh.DOUBLE_BARS, *mh.DOT_PLOTS, *mh.HISTOGRAMS)}


def _text(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _choice(c) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", "") for b in c.content)


def _answer(q) -> str:
    return _choice(q.choices[q.answer])


def _spec(q):
    [img] = [b for b in q.stem if b.kind == "image"]
    return SPECS[img.asset_id], img


def test_six_sets_and_every_picture_ships():
    assert len(KEYS) == 6
    assert len(SPECS) == len(mh.ALL_PICTURE_IDS)
    assert [i for i in SPECS if not is_diagram(i)] == []


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices_and_alt_text_hides_the_answer(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        _, img = _spec(q)
        # The number line's alt text names its fixed ends, never the point.
        assert not re.search(r"\d", img.alt.replace("-2 ถึง 2", "")), (key, img.alt)
        choices = [_choice(c) for c in q.choices]
        assert len(choices) >= 3 and len(set(choices)) == len(choices), (key, seed, choices)


def test_area_model():
    for seed in SEEDS:
        q = generate("math.area_model_p3", Random(seed))
        m, _ = _spec(q)
        s = _text(q)
        if "ใหญ่กว่า" in s:
            assert int(_answer(q)) == m.a // 10 * 10 * m.b
        elif "เล็กกว่า" in s:
            assert int(_answer(q)) == m.a % 10 * m.b
        else:
            assert int(_answer(q)) == m.a * m.b


def _side_value(expr: str, x: int) -> int:
    total = 0
    for term in expr.split(" + "):
        if term.endswith("x"):
            total += int(term[:-1] or 1) * x
        else:
            total += int(term)
    return total


def test_balance():
    for b in mh.BALANCES:
        assert b.a * b.x + b.b == b.c * b.x + b.d and b.x > 0
    for seed in SEEDS:
        q = generate("math.balance_equation_m1", Random(seed))
        b, _ = _spec(q)
        if "สมการใด" in _text(q):
            left, right = _answer(q).split(" = ")
            assert (_side_value(left, 0), _side_value(left, 1) - _side_value(left, 0)) == (b.b, b.a)
            assert (_side_value(right, 0), _side_value(right, 1) - _side_value(right, 0)) == (b.d, b.c)
        else:
            assert int(_answer(q)) == b.x


def _frac(tex: str) -> Fraction:
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", tex)
    if not m:
        return Fraction(int(tex))
    return (-1 if m.group(1) else 1) * Fraction(int(m.group(2)), int(m.group(3)))


def test_fraction_number_line():
    for seed in SEEDS:
        q = generate("math.fraction_number_line_m1", Random(seed))
        f, _ = _spec(q)
        assert _frac(_answer(q)) == Fraction(f.k, f.d) and -2 < f.k / f.d < 2
        assert [c for i, c in enumerate(q.choices)
                if i != q.answer and _frac(_choice(c)) == _frac(_answer(q))] == []


def test_double_bars():
    for seed in SEEDS:
        q = generate("math.double_bar_chart_m1", Random(seed))
        c, _ = _spec(q)
        s = _text(q)
        key = dict(re.findall(r"([A-E]) = ([^\s)]+)", s))
        names = [key[L] for L in "ABCDE"[:len(c.first)]]
        blue, orange = re.search(r"แท่งสีฟ้า = (.+?) แท่งสีส้ม = (.+?);", s).groups()
        if "ต่างกัน" in s:
            i = next(j for j, n in enumerate(names) if f"ใน{n} " in s)
            assert int(_answer(q)) == abs(c.first[i] - c.second[i])
        elif "มากที่สุด" in s:
            totals = [a + b for a, b in zip(c.first, c.second)]
            assert totals[names.index(_answer(q))] == max(totals)
        elif "รวมทุกกลุ่ม" in s:
            assert int(_answer(q)) == sum(c.first)
        else:
            ask = q.stem[1].text                     # "<series>ของ<category>มีกี่<unit>"
            series, name = re.fullmatch(r"(.+)ของ(\S+?)มีกี่\S+", ask).groups()
            values = c.first if series == blue else c.second
            assert series in (blue, orange)
            assert int(_answer(q)) == values[names.index(name)], (seed, ask)


def test_dot_plot():
    for seed in SEEDS:
        q = generate("math.dot_plot_picture_m2", Random(seed))
        p, _ = _spec(q)
        data, s = p.data, _text(q)
        if "ฐานนิยม" in s:
            counts = {v: data.count(v) for v in set(data)}
            assert counts[int(_answer(q))] == max(counts.values())
            assert list(counts.values()).count(max(counts.values())) == 1
        elif "กี่นัด" in s and "ตั้งแต่" in s:
            k = int(re.search(r"ตั้งแต่ (\d+)", s).group(1))
            assert int(_answer(q)) == sum(1 for v in data if v >= k)
        else:
            assert int(_answer(q)) == len(data)


def test_histogram():
    for seed in SEEDS:
        q = generate("math.histogram_picture_m2", Random(seed))
        h, _ = _spec(q)
        s = _text(q)
        if "ทั้งหมด" in s:
            assert int(_answer(q)) == sum(h.freq)
        elif "มากที่สุด" in s:
            best = max(range(len(h.freq)), key=lambda i: h.freq[i])
            assert _answer(q) == h.label(best) and h.freq.count(max(h.freq)) == 1
        else:
            lo = int(re.search(r"ชั้น (\d+)", s).group(1))
            assert int(_answer(q)) == h.freq[(lo - h.low) // h.width]
