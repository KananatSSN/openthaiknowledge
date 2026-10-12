"""ข้อ 25 — ค่าของ a + b + c

กำหนดให้ a, b, c เป็นเลขโดด และจำนวน 20ab13c เป็นจำนวนเต็มเจ็ดหลักที่หารด้วย 792
ลงตัว จงหาค่าของ a + b + c

792 = 8 · 9 · 11, three coprime factors, so three independent digit rules apply
to ``2 0 a b 1 3 c``:

* **8** looks only at the last three digits, ``13c``: 130 + c ≡ 0 (mod 8) and
  130 ≡ 2, so c = **6**.
* **9** looks at the digit sum: 2 + a + b + 1 + 3 + 6 = 12 + a + b ≡ 0 (mod 9),
  so a + b = 6 or 15.
* **11** looks at the alternating sum: 2 − 0 + a − b + 1 − 3 + 6 = 6 + a − b ≡ 0
  (mod 11), so a − b = 5 or a − b = −6.

Of the four combinations only ``a + b = 6`` with ``a − b = −6`` has an integer
solution — a = 0, b = 6 — so the number is **2006136** (= 792 · 2533) and

    a + b + c = 0 + 6 + 6 = **12**

The leading 2 and the fixed 1, 3 are not decoration: they are what makes the
three rules land on a single triple.

``solve`` sweeps the three digits and tests divisibility once. ``check`` never
looks at digits: it walks the multiples of the divisor in the seven-digit range
and matches each against the printed template.
"""

from __future__ import annotations

#: the printed template, with letters for the unknown digits.
PARAMS = {"template": "20ab13c", "divisor": 792}
ANSWER = 12
VARIANTS = [
    {"template": "20ab13c", "divisor": 396},
    {"template": "5a7b2c", "divisor": 132},
    {"template": "1ab2c", "divisor": 198},
    {"template": "9ab7c", "divisor": 891},
    {"template": "20ab13c", "divisor": 7919},     # prime: nothing fits
    {"template": "20ab13c", "divisor": 8},        # far too loose
]
LETTERS = "abc"


def _fill(template: str, digits: dict[str, int]) -> int | None:
    """The number the template becomes, or None if a letter is missing."""
    out = 0
    for ch in template:
        if ch.isdigit():
            out = out * 10 + int(ch)
        elif ch in digits:
            out = out * 10 + digits[ch]
        else:
            return None
    return out


def solve(template="20ab13c", divisor=792):
    """a + b + c for the one digit triple that makes the number divisible."""
    letters = [ch for ch in LETTERS if ch in template]
    if not letters or divisor <= 0:
        return None
    hits = set()
    for value in range(10 ** len(letters)):
        digits, rest = {}, value
        for ch in letters:
            digits[ch], rest = rest % 10, rest // 10
        number = _fill(template, digits)
        if number is None or number % divisor:
            continue
        if len(str(number)) != len(template):      # a leading zero would shrink it
            continue
        hits.add(sum(digits.values()))
    if len(hits) != 1:
        return None
    return next(iter(hits))


def check(template="20ab13c", divisor=792):
    """Independent: walk the multiples of the divisor and match the template.

    Every multiple with the right number of digits is written out and compared
    position by position against the printed pattern — fixed digits must agree,
    and a repeated letter would have to take the same value. No divisibility
    rule for 8, 9 or 11 is used anywhere.
    """
    letters = [ch for ch in LETTERS if ch in template]
    if not letters or divisor <= 0:
        return None
    width = len(template)
    low, high = 10 ** (width - 1), 10 ** width - 1
    if (high - low) // divisor > 5 * 10 ** 6:
        return None

    sums = set()
    start = ((low + divisor - 1) // divisor) * divisor
    for number in range(start, high + 1, divisor):
        text = str(number)
        digits: dict[str, int] = {}
        ok = True
        for want, got in zip(template, text):
            if want.isdigit():
                if want != got:
                    ok = False
                    break
            elif want in digits:
                if digits[want] != int(got):
                    ok = False
                    break
            else:
                digits[want] = int(got)
        if ok and len(digits) == len(letters):
            sums.add(sum(digits.values()))
    if len(sums) != 1:
        return None
    return next(iter(sums))
