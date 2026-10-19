"""A random group of k boys and n − k girls holds Σcⱼ garlands on average."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันที่สอง ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def average_garlands(couples: list[int], n: int, k: int) -> Fraction:
    """Boys and girls each hold C = Σcⱼ garlands in all (one per dancer per
    song). A random boy holds C/n on average, a random girl too, so a random
    group of k boys and n − k girls holds k·C/n + (n − k)·C/n = C ≥ m: some
    group reaches the average."""
    total = sum(couples)
    return Fraction(k * total, n) + Fraction((n - k) * total, n)


@question_type(
    "math.garland_average_olympiad",
    display_name={"th": "ค่าเฉลี่ยจำนวนพวงมาลัยของกลุ่มนักเรียน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class GarlandAverage(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 12)
        k = rng.randint(1, n - 1)
        songs = rng.randint(3, 7)
        couples = [rng.randint(1, n) for _ in range(songs)]
        answer = average_garlands(couples, n, k)
        total = sum(couples)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(2 * total), Fraction(k * total, n), Fraction(songs), Fraction((n - k) * total, n), Fraction(total, 2)]) if v != answer]
        listing = ", ".join(map(str, couples))
        return MathDraw(
            rf"n={n},\quad k={k}",
            frac_tex(answer),
            prompt=f"มีนักเรียนหญิง n คนและชาย n คน มีการเต้นรำ {songs} เพลง จำนวนคู่ที่ขึ้นเต้นในแต่ละเพลงเป็น {listing} คู่ ทุกคนที่ขึ้นเต้นได้พวงมาลัยคนละหนึ่งพวงต่อเพลง ถ้าสุ่มกลุ่มนักเรียนชาย k คนและหญิง n − k คน จงหาค่าคาดหมายของจำนวนพวงมาลัยรวมของกลุ่ม",
            hint="ฝ่ายชายรวมกันได้พวงมาลัยเท่ากับจำนวนคู่ทั้งหมด ฝ่ายหญิงก็เช่นกัน นักเรียนชายแต่ละคนได้เฉลี่ย C/n พวง",
            distractors=wrong,
        )
