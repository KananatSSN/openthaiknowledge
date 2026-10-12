"""การประยุกต์ใช้สมบัติและกฎของแก๊ส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/6

Sets moved here from: science_wave_f25.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, celsius, exact
from otk.sets._support.science_wave_f25 import STP_VOLUME, SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_USE = "การประยุกต์ใช้สมบัติและกฎของแก๊ส"


GAS_SCENARIOS = (
    ("นักดำน้ำต้องค่อย ๆ ขึ้นสู่ผิวน้ำและหายใจออกตลอด เพราะอากาศในปอดขยายตัวเมื่อความดันลดลง", "กฎของบอยล์"),
    ("บอลลูนลมร้อนลอยได้ เพราะอากาศที่ร้อนขึ้นขยายตัวจนมีความหนาแน่นน้อยกว่าอากาศภายนอก", "กฎของชาร์ล"),
    ("ไม่ควรทิ้งกระป๋องสเปรย์ในที่ร้อน เพราะความดันในกระป๋องปิดสนิทเพิ่มขึ้นตามอุณหภูมิ", "กฎของเกย์-ลูสแซก"),
    ("ถุงลมนิรภัยพองได้เต็มถุงเมื่อปฏิกิริยาเคมีให้แก๊สไนโตรเจนจำนวนโมลมากพอ", "กฎของอาโวกาโดร"),
    ("ถังอากาศสำหรับดำน้ำลึกต้องปรับสัดส่วนออกซิเจน เพราะความดันย่อยของออกซิเจนสูงขึ้นตามความดันรวม", "กฎความดันย่อยของดอลตัน"),
    ("ได้กลิ่นน้ำหอมทั่วห้องหลังเปิดขวดไม่นาน และแก๊สเบาได้กลิ่นเร็วกว่าแก๊สหนัก", "กฎการแพร่ผ่านของเกรแฮม"),
    ("แยกไอโซโทปยูเรเนียมโดยให้ UF₆ แพร่ผ่านเยื่อกรองหลายชั้น", "กฎการแพร่ผ่านของเกรแฮม"),
    ("เครื่องวัดความดันลมยางแสดงค่าสูงขึ้นหลังรถวิ่งนาน ๆ", "กฎของเกย์-ลูสแซก"),
    ("ปั๊มลมจักรยานอัดอากาศให้ปริมาตรเล็กลงเพื่อเพิ่มความดัน", "กฎของบอยล์"),
    ("ลูกโป่งที่เป่าไว้ในห้องปรับอากาศแฟบลงเล็กน้อยเมื่อเทียบกับตอนอยู่กลางแดด", "กฎของชาร์ล"),
)


USE_LAWS = ("กฎของบอยล์", "กฎของชาร์ล", "กฎของเกย์-ลูสแซก", "กฎของอาโวกาโดร", "กฎความดันย่อยของดอลตัน",
            "กฎการแพร่ผ่านของเกรแฮม")


@question_type(
    "chem.gas_application_foundation",
    display_name={"th": "กฎของแก๊สที่อธิบายปรากฏการณ์ในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class GasApplicationFoundation(QuestionType):
    """Name the law behind a use or an everyday effect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case, law = rng.choice(GAS_SCENARIOS)
        return _labelled(stem=f"\"{case}\" สอดคล้องกับกฎใดมากที่สุด", correct=law,
                         wrongs=tuple([x for x in USE_LAWS if x != law]), topic=TOPIC_USE,
                         hint="ดูว่าปริมาณใดเปลี่ยนและปริมาณใดคงที่ หรือเป็นเรื่องความดันย่อยหรือการแพร่")


@question_type(
    "chem.gas_application_fluency",
    display_name={"th": "ความดันใต้น้ำและความดันย่อยของอากาศที่นักดำน้ำหายใจ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class GasApplicationFluency(QuestionType):
    """Every 10 m of water adds about 1 atm; air is 21% O₂ and 79% N₂ by moles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        depth = rng.choice((10, 20, 30, 40, 50))
        pressure = 1 + Fraction(depth, 10)
        hint = "ความดันรวมใต้น้ำ = 1 atm + 1 atm ทุก ๆ 10 m ความดันย่อย = เศษส่วนโมล × ความดันรวม"
        kind = rng.randrange(3)
        if kind == 0:
            share, name = rng.choice(((Fraction(21, 100), "O₂"), (Fraction(79, 100), "N₂")))
            return numeric(stem=f"นักดำน้ำหายใจอากาศอัด (O₂ 21% N₂ 79% โดยโมล) ที่ความลึก {depth} m "
                                f"(ความดันเพิ่ม 1 atm ทุก 10 m จากผิวน้ำ 1 atm) ความดันย่อยของ {name} ในอากาศที่หายใจเท่าใด",
                           answer=share * pressure, wrongs=[share * Fraction(depth, 10), share, pressure],
                           unit="atm", topic=TOPIC_USE, hint=hint)
        volume = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, Fraction(5, 2), 3))
        if kind == 1:
            return numeric(stem=f"นักดำน้ำกลั้นหายใจที่ความลึก {depth} m โดยอากาศในปอดมีปริมาตร {show(volume)} L "
                                "ถ้าขึ้นถึงผิวน้ำ (1 atm) โดยไม่หายใจออกและอุณหภูมิคงที่ อากาศนี้จะมีปริมาตรกี่ลิตร "
                                "(ความดันเพิ่ม 1 atm ทุก 10 m)",
                           answer=volume * pressure, wrongs=[volume * Fraction(depth, 10), volume / pressure if exact(volume / pressure) else volume * 2, volume],
                           unit="L", topic=TOPIC_USE, hint="กฎของบอยล์: P₁V₁ = P₂V₂")
        return numeric(stem=f"ลูกโป่งมีอากาศ {show(volume * pressure)} L ที่ผิวน้ำ (1 atm) ถ้านำลงไปที่ความลึก {depth} m "
                            "ที่อุณหภูมิเท่าเดิม ลูกโป่งจะมีปริมาตรกี่ลิตร (ความดันเพิ่ม 1 atm ทุก 10 m)",
                       answer=volume, wrongs=[volume * pressure * pressure, volume * pressure, volume * pressure / Fraction(depth, 10) if exact(volume * pressure / Fraction(depth, 10)) else volume + 1],
                       unit="L", topic=TOPIC_USE, hint="กฎของบอยล์: P₁V₁ = P₂V₂")


@question_type(
    "chem.gas_application_application",
    display_name={"th": "ถุงลมนิรภัยและบอลลูนลมร้อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class GasApplicationApplication(QuestionType):
    """Air bag N₂ from NaN₃ at STP, and the density of heated air."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            def draw():
                grams = rng.randrange(13, 261, 13)
                n2 = Fraction(grams, 65) * Fraction(3, 2)
                return (grams, n2) if exact(n2 * STP_VOLUME) else None

            grams, n2 = _find(rng, draw)
            if rng.random() < 0.5:
                return numeric(stem=f"ถุงลมนิรภัยต้องการแก๊สไนโตรเจน {show(n2 * STP_VOLUME)} ลิตรที่ STP จากปฏิกิริยา "
                                    "2NaN₃ → 2Na + 3N₂ ต้องใช้ NaN₃ กี่กรัม (มวลสูตร 65)",
                               answer=grams, wrongs=[n2 * 65, grams * Fraction(3, 2), grams * 2], unit="กรัม",
                               topic=TOPIC_USE,
                               hint="โมล N₂ = ปริมาตร ÷ 22.4 แล้ว NaN₃ = 2/3 เท่าของ N₂ แล้วคูณมวลสูตร 65")
            return numeric(stem=f"ถุงลมนิรภัยใช้ปฏิกิริยา 2NaN₃ → 2Na + 3N₂ ถ้าใช้ NaN₃ {grams} กรัม (มวลสูตร 65) "
                                "จะได้แก๊สไนโตรเจนกี่ลิตรที่ STP",
                           answer=n2 * STP_VOLUME, wrongs=[Fraction(grams, 65) * STP_VOLUME, n2 * 3 * STP_VOLUME / 2,
                                                            Fraction(grams, 65) * 3 * STP_VOLUME],
                           unit="L", topic=TOPIC_USE,
                           hint="โมล NaN₃ = มวล ÷ 65 แล้ว N₂ = 3/2 เท่าของ NaN₃ และ 1 โมลที่ STP = 22.4 L")

        def draw():
            # Outside air 2-27 °C; a hot air balloon runs at about 50-130 °C.
            cold = rng.randrange(275, 301, 5)
            hot = rng.randrange(325, 401, 5)
            ratio = Fraction(cold, hot)
            return (cold, hot, ratio) if exact(ratio) else None

        cold, hot, ratio = _find(rng, draw)
        if rng.random() < 0.5:
            return numeric(stem=f"อากาศภายนอกบอลลูนมีอุณหภูมิ {celsius(cold)} ต้องทำให้อากาศในบอลลูนร้อนกี่ °C "
                                f"ความหนาแน่นจึงเหลือ {show(ratio)} เท่าของอากาศภายนอก (ความดันเท่ากัน)",
                           answer=hot - 273, wrongs=[hot, Fraction(cold - 273, ratio) if cold != 273 else hot + 273,
                                                     hot - 273 + 50], unit="°C", topic=TOPIC_USE,
                           hint="ความหนาแน่นแปรผกผันกับ T (เคลวิน): T_ร้อน = T_ภายนอก ÷ อัตราส่วนความหนาแน่น")
        return numeric(stem=f"อากาศภายนอกบอลลูนมีอุณหภูมิ {celsius(cold)} ถ้าอากาศในบอลลูนร้อน {celsius(hot)} "
                            "ที่ความดันเท่ากัน ความหนาแน่นของอากาศในบอลลูนเป็นกี่เท่าของอากาศภายนอก",
                       answer=ratio, wrongs=[Fraction(hot, cold), 1 - ratio if 1 - ratio > 0 else ratio / 2,
                                             Fraction(cold - 273 or 1, hot - 273) if exact(Fraction(cold - 273 or 1, hot - 273)) else ratio + 1],
                       unit="เท่า", topic=TOPIC_USE,
                       hint="ที่ P คงที่ V ∝ T ความหนาแน่น = มวล ÷ ปริมาตร จึงแปรผกผันกับ T (เคลวิน)")
