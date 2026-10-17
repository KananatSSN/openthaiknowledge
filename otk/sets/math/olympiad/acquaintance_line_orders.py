"""Every prefix must be a block of morning neighbours: 2^(n − 1) orders after a line, n·2^(n − 2) after a circle."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 5",))


def order_tex(n: int, circle: bool) -> str:
    """The people placed so far always form a block of neighbours, and each
    new person extends the block at one end: 2 choices per step after the
    first, except the last on a circle. Line: 2^(n − 1) (source: n = 50);
    circle: n·2^(n − 2)."""
    return rf"{n}\cdot 2^{{{n - 2}}}" if circle else rf"2^{{{n - 1}}}"


@question_type(
    "math.acquaintance_line_orders_olympiad",
    display_name={"th": "จำนวนวิธีจัดแถวให้ทุกคนมีคนรู้จักอยู่ข้างหน้า"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class AcquaintanceLineOrders(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(6, 60)
        circle = rng.random() < 0.4
        answer = order_tex(n, circle)
        wrong = [rf"2^{{{n}}}", rf"2^{{{n - 2}}}", rf"{n}\cdot 2^{{{n - 1}}}", rf"{n - 1}\cdot 2^{{{n - 2}}}", rf"2^{{{n - 1}}}"]
        where = "ยืนเป็นวงกลม" if circle else "ยืนเรียงแถวหน้ากระดาน"
        return MathDraw(
            rf"n={n}",
            answer,
            prompt=f"นักเรียน n คนที่ไม่รู้จักกันเลย ตอนเช้า{where} และรู้จักเฉพาะเพื่อนที่ยืนติดกัน ตอนบ่ายยืนแถวตอนเรียงหนึ่ง โดยทุกคน (ยกเว้นคนแรก) ต้องมีเพื่อนที่รู้จักตั้งแต่ตอนเช้ายืนอยู่ข้างหน้าอย่างน้อยหนึ่งคน จัดแถวได้ทั้งหมดกี่วิธี",
            hint="คนที่ยืนไปแล้วต้องเป็นกลุ่มที่ติดกันในตอนเช้าเสมอ คนถัดไปจึงต้องต่อที่ปลายข้างใดข้างหนึ่งของกลุ่ม",
            distractors=[t for t in dict.fromkeys(wrong) if t != answer],
        )
