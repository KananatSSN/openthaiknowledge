"""Independent decimal checks for added ม.5 interest and money-value sets."""

import re
from decimal import ROUND_HALF_UP, Decimal, localcontext
from random import Random

import pytest

from otk.api import REGISTRY, catalog

KEYS = (
    "math.compound_quarterly_m5",
    "math.regular_deposit_future_value_m5",
    "math.regular_payment_present_value_m5",
)


def _nearest(value):
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _solve_from_stem(key, stem):
    with localcontext() as ctx:
        ctx.prec = 50
        if key == KEYS[0]:
            principal, rate, years = re.search(
                r"ฝากเงิน ([\d,]+) บาท อัตราดอกเบี้ยร้อยละ (\d+) ต่อปี.*เมื่อครบ (\d+) ปี", stem).groups()
            principal = Decimal(principal.replace(",", ""))
            factor = 1 + Decimal(rate) / 400
            return _nearest(principal * factor ** (4 * int(years)))
        if key == KEYS[1]:
            deposit, years, rate = re.search(
                r"ฝากเงิน ([\d,]+) บาท ทุกสิ้นปี เป็นเวลา (\d+) ปี.*ร้อยละ (\d+) ต่อปี", stem).groups()
            deposit = Decimal(deposit.replace(",", ""))
            factor = 1 + Decimal(rate) / 100
            # The last deposit earns no interest, the first earns n-1 periods.
            return _nearest(sum((deposit * factor ** j for j in range(int(years))), Decimal(0)))
        payment, years, rate = re.search(
            r"จะได้รับเงิน ([\d,]+) บาท ทุกสิ้นปี เป็นเวลา (\d+) ปี.*ร้อยละ (\d+) ต่อปี", stem).groups()
        payment = Decimal(payment.replace(",", ""))
        factor = 1 + Decimal(rate) / 100
        return _nearest(sum((payment / factor ** j for j in range(1, int(years) + 1)), Decimal(0)))


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(120))
def test_exactly_rounded_amount_and_named_choices(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = _solve_from_stem(key, q.stem[0].text)
    assert q.choices[q.answer].content[0].tex == str(expected)
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)
    assert all(choice.content[0].tex != str(expected)
               for i, choice in enumerate(q.choices) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_catalog_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.5", "ดอกเบี้ยและมูลค่าของเงิน", 3,
    )
    stems = {REGISTRY[key].generate(Random(seed)).stem[0].text for seed in range(200)}
    assert len(stems) >= 100
