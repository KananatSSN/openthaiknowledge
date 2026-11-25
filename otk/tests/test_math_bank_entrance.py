"""Sets added for the maths entrance papers: each answer re-derived by another route."""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

import sympy as sp

from otk.api import REGISTRY

SEEDS = range(40)


def _draw(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    texts = [c.content[0].text for c in q.choices]
    assert len(set(texts)) == len(texts) == REGISTRY[key].max_choices
    return q.stem[0].text, texts[q.answer]


def _ints(s):
    return [int(n) for n in re.findall(r"\d+", s)]


def test_train_passing_by_equations():
    x, t = sp.symbols("x t", positive=True)
    for seed in SEEDS:
        stem, right = _draw("math.train_passing_m3", seed)
        value = sp.Rational(right.split()[0])
        if stem.startswith("รถไฟขบวนที่หนึ่ง"):
            lengths = re.findall(r"ยาว (\d*)x เมตร", stem)
            p, q = (int(n) if n else 1 for n in lengths)
            v1, v2 = (sp.Rational(n) * 1000 / 3600 for n in re.findall(r"(\d+) กิโลเมตรต่อชั่วโมง", stem))
            head_on = int(re.search(r"(\d+) วินาที", stem).group(1))
            (length,) = sp.solve(sp.Eq((p + q) * x, (v1 + v2) * head_on), x)
            (time,) = sp.solve(sp.Eq((p + q) * length, abs(v2 - v1) * t), t)
            assert time == value, (seed, stem)
        else:
            v1, v2 = (sp.Rational(n) * 1000 / 3600
                      for n in re.search(r"ความเร็ว (\d+) และ (\d+)", stem).groups())
            overtake = int(re.search(r"ใช้เวลา (\d+) วินาที", stem).group(1))
            k = int(re.search(r"เป็น (\d+) เท่า", stem).group(1))
            # the short train is x, the long one kx; overtaking covers both at the speed difference
            (short,) = sp.solve(sp.Eq(x + k * x, abs(v2 - v1) * overtake), x)
            assert short == value, (seed, stem)


def test_transfer_probability_by_enumeration():
    for seed in SEEDS:
        stem, right = _draw("math.probability_transfer_m5", seed)
        r1, k1, r2, k2 = _ints(stem)[:4]
        want = "แดง" if stem.endswith("สีแดงเท่ากับเท่าใด") else "ดำ"
        box1 = ["แดง"] * r1 + ["ดำ"] * k1
        box2 = ["แดง"] * r2 + ["ดำ"] * k2
        hits = total = 0
        for moved in range(len(box1)):          # every labelled ball equally likely
            after = box2 + [box1[moved]]
            for drawn in range(len(after)):
                weight = Fraction(1, len(box1)) * Fraction(1, len(after))
                total += weight
                hits += weight if after[drawn] == want else 0
        assert total == 1 and hits == Fraction(right), (seed, stem)


def test_tangential_trapezoid_by_coordinates():
    for seed in SEEDS:
        stem, right = _draw("math.tangential_trapezoid_m5", seed)
        area = int(re.search(r"พื้นที่ (\d+) ตารางหน่วย", stem).group(1))
        cos_a = Fraction(re.search(r"cos\(∠DAB\) = (\d+/\d+)", stem).group(1))
        asked = re.search(r"ด้าน (\w+) ยาวกี่หน่วย", stem).group(1)
        cos_q = sp.Rational(cos_a.numerator, cos_a.denominator)
        leg = sp.symbols("leg", positive=True)
        # A at the origin, AB on the x-axis; D and C one leg up at angle A on either side.
        dx, dy = leg * cos_q, leg * sp.sqrt(1 - cos_q ** 2)
        dc = leg - dx                                  # AB + DC = 2·leg with AB = DC + 2·dx
        ab = dc + 2 * dx
        shape = sp.Polygon((0, 0), (ab, 0), (ab - dx, dy), (dx, dy))
        (solved,) = sp.solve(sp.Eq(abs(shape.area), area), leg)
        sides = {"AB": ab, "CD": dc, "AD": leg}
        assert sp.simplify(sides[asked].subs(leg, solved) - int(right)) == 0, (seed, stem)


def test_conjugate_root_cubic_by_solving_for_coefficients():
    a, b, c = sp.symbols("a b c")
    x = sp.symbols("x")
    for seed in SEEDS:
        stem, right = _draw("math.conjugate_root_cubic_m4", seed)
        factor = re.search(r"ถ้า (x(?: [−+] \d+)?) เป็นตัวประกอบ", stem).group(1)
        r = 0 if factor == "x" else (int(factor.split()[-1]) * (1 if "−" in factor else -1))
        root_text = re.search(r"และ P\((.+?)\) = 0", stem).group(1).replace("−", "-").replace(" ", "")
        root = sp.sympify(root_text.replace("√", "sqrt(") + ")" * root_text.count("√"))
        poly = x ** 3 + a * x ** 2 + b * x + c
        at_root = sp.expand(poly.subs(x, root))
        rational, irrational = at_root.as_independent(sp.sqrt(sp.Integer(_ints(root_text)[-1])))
        solution = sp.solve([poly.subs(x, r), rational, irrational], [a, b, c], dict=True)
        assert len(solution) == 1
        total = sum(solution[0][v] for v in (a, b, c))
        assert all(solution[0][v].is_integer for v in (a, b, c))
        assert total == int(right.replace("−", "-")), (seed, stem)
