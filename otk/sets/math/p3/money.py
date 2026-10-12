"""เงิน

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.3/*

Sets moved here from: math, math_number, math_p3, math_pictures_extra.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import _maths, _texts
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_p2 import MONEY

PROVENANCE = Provenance("original")


_GOODS = [("สมุด", 12), ("ดินสอ", 5), ("ยางลบ", 8), ("ไม้บรรทัด", 15),
          ("ปากกา", 10), ("กบเหลาดินสอ", 20), ("แฟ้ม", 25), ("กระเป๋าดินสอ", 45)]


_PAYMENTS = tuple(m for m in MONEY if m.total >= 20)


@question_type("math.money_total", display_name={"th": "รวมราคาสินค้า"},
               level={"th": "ป.3"}, topic="เงิน")
class MoneyTotal(WordProblem):
    def expr(self, rng: Random, count_lo: int = 2, count_hi: int = 6):
        (name_a, price_a), (name_b, price_b) = rng.sample(_GOODS, 2)
        qa, qb = rng.randint(count_lo, count_hi), rng.randint(count_lo, count_hi)
        total = qa * price_a + qb * price_b
        return MathDraw(
            "", str(total),
            prompt=(f"ซื้อ{name_a} {qa} ชิ้น ราคาชิ้นละ {price_a} บาท "
                    f"และ{name_b} {qb} ชิ้น ราคาชิ้นละ {price_b} บาท "
                    "รวมเป็นเงินกี่บาท"),
            distractors=[str(qa * price_b + qb * price_a),
                         str(price_a + price_b),
                         str((qa + qb) * (price_a + price_b))])


@question_type("math.baht_satang_p3",
               display_name={"th": "บาทและสตางค์"},
               level=LEVEL, topic="เงิน")
class BahtSatangP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        baht = rng.randint(1, 99)
        satang = rng.choice((25, 50, 75))
        kind = rng.randrange(4)
        if kind == 0:
            ans = 100 * baht + satang
            return _maths([text(f"{baht} บาท {satang} สตางค์ เท่ากับกี่สตางค์")], str(ans),
                          _story.keep(10 * baht + satang, baht + satang, 100 * baht,
                                      1000 * baht + satang, answer=ans), self.topic)
        if kind == 1:
            right = f"{baht}.{satang} บาท"
            return _texts([text(f"{baht} บาท {satang} สตางค์ เขียนเป็นจำนวนเงินแบบมีจุดได้อย่างไร")],
                          right, [f"{baht}.{satang // 10} บาท", f"{satang}.{baht:02d} บาท",
                                  f"{baht}{satang} บาท", f"{baht}.0{satang // 25} บาท"],
                          self.topic)
        if kind == 2:
            n = 2 * rng.randint(2, 20)
            return _maths([text(f"เหรียญห้าสิบสตางค์ {n} เหรียญ รวมเป็นเงินกี่บาท")], str(n // 2),
                          _story.keep(n * 50, n, n * 5, n // 2 + 1, answer=n // 2), self.topic)
        n = 4 * rng.randint(2, 12)
        return _maths([text(f"เหรียญยี่สิบห้าสตางค์ {n} เหรียญ รวมเป็นเงินกี่บาท")], str(n // 4),
                      _story.keep(n * 25, n // 2, n, n // 4 + 1, answer=n // 4), self.topic)


@question_type("math.income_expense_record_p3",
               display_name={"th": "บันทึกรายรับรายจ่าย"},
               level=LEVEL, topic="เงิน")
class IncomeExpenseRecordP3(WordProblem):
    _IN = ("แม่ให้เงิน", "คุณยายให้เงิน", "ขายขวดพลาสติกได้", "ช่วยงานบ้านได้ค่าขนม")
    _OUT = ("ซื้อสมุด", "ซื้อขนม", "ซื้อดินสอสี", "ค่ารถ", "ทำบุญ", "ซื้อหนังสือนิทาน")

    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        balance = 0
        lines, income, expense = [], 0, 0
        for day in range(1, rng.randint(4, 6) + 1):
            if day == 1 or balance < 15 or (rng.random() < 0.4 and balance < 150):
                amount = rng.choice(range(20, 210, 10))
                lines.append(f"วันที่ {day}  รายรับ  {rng.choice(self._IN)} {amount} บาท")
                balance += amount
                income += amount
            else:
                amount = rng.randint(5, max(6, balance - 1))
                lines.append(f"วันที่ {day}  รายจ่าย  {rng.choice(self._OUT)} {amount} บาท")
                balance -= amount
                expense += amount
        record = f"บันทึกรายรับรายจ่ายของ{p}\n" + "\n".join(lines)
        ask = rng.randrange(3)
        if ask == 0 or not expense:
            return MathDraw("", str(balance), prompt=f"{record}\n{p}มีเงินคงเหลือกี่บาท",
                            distractors=_story.keep(income + expense, income, balance + 10,
                                                    expense, answer=balance, lo=0))
        if ask == 1:
            return MathDraw("", str(expense), prompt=f"{record}\n{p}มีรายจ่ายรวมกี่บาท",
                            distractors=_story.keep(income, balance, expense + 10, expense - 5,
                                                    answer=expense, lo=1))
        return MathDraw("", str(income), prompt=f"{record}\n{p}มีรายรับรวมกี่บาท",
                        distractors=_story.keep(expense, balance, income + 10, income - 20,
                                                answer=income, lo=1))


@question_type("math.change_picture_p3", display_name={"th": "หาเงินทอนจากเงินในภาพ"},
               level={"th": "ป.3"}, topic="เงิน")
class ChangePictureP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice(_PAYMENTS)
        price = rng.randint(max(1, m.total // 3), m.total - 1)
        change = m.total - price
        img = image(m.asset_id, alt="ภาพเหรียญและธนบัตร")
        # Answering with the money shown; adding; a coin off.
        return _math_q([text(f"ภาพคือเงินที่จ่ายไปทั้งหมด ซื้อของราคา {price} บาท ได้เงินทอนกี่บาท"), img],
                       str(change), _near(change, m.total, m.total + price, change + 1, change + 5,
                                          lo=1), self.topic)


@question_type("math.make_change",
               display_name={"th": "การทอนเงิน"}, level={"th": "ป.3"},
               topic="เงิน")
class MakeChange(WordProblem):
    _ITEMS = ("ขนม", "นม", "สมุด", "ดินสอสี", "ไอศกรีม", "หนังสือการ์ตูน", "ของเล่น",
              "ข้าวผัด", "น้ำผลไม้")

    def expr(self, rng: Random):
        paid = rng.choice([20, 50, 100, 500, 1000])
        price = rng.randint(max(5, paid // 10), paid - 1)
        change = paid - price
        p = rng.choice(_story.NAMES)
        item = rng.choice(self._ITEMS)
        if paid >= 100 and rng.random() < 0.4:
            # Two things at once: add first, then take from the note.
            first = rng.randint(1, price - 1)
            other = rng.choice([x for x in self._ITEMS if x != item])
            prompt = (f"{p}ซื้อ{item}ราคา {first} บาท และ{other}ราคา {price - first} บาท "
                      f"จ่ายด้วยธนบัตรใบละ {paid} บาท จะได้เงินทอนกี่บาท")
            wrongs = [paid - first, price, change + 10, change - 1]
        else:
            prompt = rng.choice((
                f"ซื้อ{item}ราคา {price} บาท จ่ายด้วยธนบัตรใบละ {paid} บาท ได้เงินทอนเท่าใด?",
                f"{p}จ่ายเงิน {paid} บาท เพื่อซื้อ{item}ราคา {price} บาท "
                f"แม่ค้าต้องทอนเงินให้{p}กี่บาท",
            ))
            wrongs = [price, paid + price, change + 10, change - 1]
        return MathDraw("", str(change), prompt=prompt,
                        distractors=_story.keep(*wrongs, answer=change, lo=1))


@question_type("math.money_change_left", display_name={"th": "ซื้อของแล้วเหลือเงินเท่าไร"},
               level={"th": "ป.3"}, topic="เงิน")
class MoneyChangeLeft(WordProblem):
    def expr(self, rng: Random, note_lo: int = 100, note_hi: int = 500):
        note = rng.choice([n for n in (100, 200, 500, 1000)
                           if note_lo <= n <= note_hi] or [100])
        name, price = rng.choice(_GOODS)
        qty = rng.randint(2, max(2, min(12, note // (price * 2))))
        spent = price * qty
        return MathDraw(
            "", str(note - spent),
            prompt=(f"มีเงิน {note} บาท ซื้อ{name} {qty} ชิ้น ชิ้นละ {price} บาท "
                    "จะเหลือเงินกี่บาท"),
            distractors=[str(spent), str(note + spent), str(note - price)])
