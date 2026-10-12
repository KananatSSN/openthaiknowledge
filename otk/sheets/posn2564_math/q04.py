"""ข้อ 4 — อัตราส่วนโรบัสต้าต่ออาราบิก้าที่ทำให้ได้กำไร 20%

ร้านค้าแห่งหนึ่งขายเมล็ดกาแฟอาราบิก้าผสมโรบัสต้า ถ้าลงทุนซื้อกาแฟโรบัสต้า
กิโลกรัมละ 100 บาท และกาแฟอาราบิก้ากิโลกรัมละ 400 บาท แล้วเจ้าของร้านจะต้อง
ผสมกาแฟด้วยอัตราส่วนของโรบัสต้าต่ออาราบิก้าเป็นเท่าใด จึงทำให้ได้กำไร 20%
เมื่อขายกาแฟที่ผสมได้ทั้งหมดในราคากิโลกรัมละ 200 บาท

The profit is on **cost**, so a selling price of 200 at 20% profit means the
blend costs 200/1.2 = 500/3 per kilogram. That single number turns the question
into the alligation rule: the two ingredients must appear in the ratio of their
*distances from the blend cost*, on opposite sides,

    cheap : dear = (dear − cost) : (cost − cheap) = (400 − 500/3) : (500/3 − 100)

which is (700/3) : (200/3) = **7 : 2**.

``solve`` computes that in exact fractions. ``check`` mixes an actual batch: it
searches whole-kilogram recipes, prices each one, and keeps the ones whose
profit really is the printed percentage — so the alligation rule is confirmed by
a sale rather than assumed.
"""

from __future__ import annotations

from fractions import Fraction

#: prices per kilogram, and the profit percentage on cost.
PARAMS = {"cheap": 100, "dear": 400, "sell": 200, "profit": 20}
ANSWER = Fraction(7, 2)
VARIANTS = [
    {"cheap": 100, "dear": 400, "sell": 250, "profit": 25},
    {"cheap": 50, "dear": 200, "sell": 120, "profit": 20},
    {"cheap": 80, "dear": 380, "sell": 240, "profit": 20},
    {"cheap": 120, "dear": 300, "sell": 240, "profit": 20},
    {"cheap": 100, "dear": 400, "sell": 600, "profit": 20},   # cost above dear
    {"cheap": 90, "dear": 210, "sell": 180, "profit": 50},
]


def solve(cheap=100, dear=400, sell=200, profit=20):
    """(dear − cost) : (cost − cheap), with cost = sell/(1 + profit/100)."""
    if cheap <= 0 or dear <= cheap or sell <= 0 or profit <= -100:
        return None
    cost = Fraction(sell) / (1 + Fraction(profit, 100))
    if not cheap < cost < dear:
        return None              # the blend cost has to lie between the two
    return (dear - cost) / (cost - cheap)


def check(cheap=100, dear=400, sell=200, profit=20):
    """Independent: mix real batches and keep the ones that hit the profit.

    For every whole-kilogram recipe up to a modest size, the outlay and the
    takings are computed directly and the profit compared with the printed one.
    Every recipe that qualifies is kept, and they must all be the same ratio —
    which is the alligation claim, tested rather than used.
    """
    if cheap <= 0 or dear <= cheap or sell <= 0 or profit <= -100:
        return None
    wanted = 1 + Fraction(profit, 100)
    ratios = set()
    for r in range(1, 60):
        for a in range(1, 60):
            outlay = cheap * r + dear * a
            takings = sell * (r + a)
            if Fraction(takings, outlay) == wanted:
                ratios.add(Fraction(r, a))
    if len(ratios) != 1:
        return None
    return ratios.pop()
