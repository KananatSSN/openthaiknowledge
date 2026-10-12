"""ความเข้มเสียง ระดับเสียง และผลของความถี่กับระดับเสียงต่อการได้ยิน

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/6

Sets moved here from: science_wave_e14.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e14 import SUBJECT, UPPER_FIVE, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_LOUDNESS = "ความเข้มเสียง ระดับเสียง และผลของความถี่กับระดับเสียงต่อการได้ยิน"


HEARING_EFFECTS = (
    (0, "เป็นเสียงค่อยที่สุดที่หูคนทั่วไปเริ่มได้ยิน"),
    (30, "เป็นระดับเสียงกระซิบเบา ๆ ฟังสบาย ไม่เป็นอันตราย"),
    (60, "เป็นระดับเสียงสนทนาทั่วไป ไม่เป็นอันตราย"),
    (90, "ถ้าฟังติดต่อกันนานหลายชั่วโมงทุกวัน อาจทำให้หูเสื่อมได้"),
    (120, "ทำให้รู้สึกเจ็บปวดในหู และอาจทำให้หูเสียหายได้ทันที"),
)


HEARING_TRUE = (
    "หูมนุษย์ได้ยินเสียงที่มีความถี่ประมาณ 20 ถึง 20,000 เฮิรตซ์",
    "เสียงที่ความถี่สูงกว่า 20,000 เฮิรตซ์เป็นคลื่นเหนือเสียง หูมนุษย์ไม่ได้ยินแม้จะมีระดับเสียงสูง",
    "หูไวต่อเสียงความถี่ประมาณ 1,000 ถึง 4,000 เฮิรตซ์มากกว่าเสียงความถี่ต่ำมาก ๆ ที่ระดับเสียงเท่ากัน",
    "การฟังเสียงระดับสูงกว่า 85 เดซิเบลเป็นเวลานานทำให้หูเสื่อมได้",
    "ผู้สูงอายุมักได้ยินเสียงความถี่สูงได้ลดลง",
)


HEARING_FALSE = (
    "หูมนุษย์ได้ยินเสียงทุกความถี่ถ้าเสียงดังพอ",
    "เสียงความถี่ 10 เฮิรตซ์ได้ยินชัดที่สุดเพราะเป็นเสียงทุ้ม",
    "ระดับเสียง 120 เดซิเบลปลอดภัยต่อการฟังเป็นเวลานาน",
    "หูไวต่อเสียงทุกความถี่เท่ากันที่ระดับเสียงเท่ากัน",
    "คลื่นเหนือเสียงคือเสียงที่ดังมากจนหูรับไม่ไหว",
)


def classify_frequency(f: int) -> str:
    if f < 20:
        return "คลื่นใต้เสียง หูมนุษย์ไม่ได้ยิน"
    if f > 20_000:
        return "คลื่นเหนือเสียง หูมนุษย์ไม่ได้ยิน"
    return "เสียงที่หูมนุษย์ได้ยิน"


FREQUENCY_CLASSES = ("คลื่นใต้เสียง หูมนุษย์ไม่ได้ยิน", "เสียงที่หูมนุษย์ได้ยิน",
                     "คลื่นเหนือเสียง หูมนุษย์ไม่ได้ยิน", "เสียงที่ได้ยินเฉพาะเมื่อดังกว่า 120 เดซิเบล")


_SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _sup(n: int) -> str:
    return str(n).translate(_SUPERSCRIPT)


@question_type(
    "phys.sound_intensity_foundation",
    display_name={"th": "ความเข้มเสียง ระดับเสียง และช่วงความถี่ที่หูได้ยิน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LOUDNESS,
)
class SoundIntensityFoundation(QuestionType):
    """The quantities and their units, and which frequencies an ear can hear at all."""

    DEFINITIONS = (
        ("ความเข้มเสียงหมายถึงข้อใด",
         "พลังงานเสียงที่ตกตั้งฉากบนพื้นที่หนึ่งตารางเมตรในหนึ่งวินาที (W/m²)",
         ("จำนวนครั้งที่แหล่งกำเนิดเสียงสั่นในหนึ่งวินาที", "ความสูงต่ำของเสียง",
          "อัตราเร็วของเสียงในอากาศ")),
        ("ระดับเสียงมีหน่วยเป็นข้อใด", "เดซิเบล (dB)",
         ("เฮิรตซ์ (Hz)", "วัตต์ต่อตารางเมตร (W/m²)", "เมตรต่อวินาที (m/s)")),
        ("ถ้าอยู่ห่างจากแหล่งกำเนิดเสียงมากขึ้น ความเข้มเสียงที่ได้รับจะเป็นอย่างไร",
         "ลดลง เพราะพลังงานเสียงแผ่กระจายไปบนพื้นที่ที่กว้างขึ้น",
         ("เพิ่มขึ้น เพราะเสียงสะสมพลังงานระหว่างทาง", "เท่าเดิมทุกระยะ",
          "ลดลงเพราะความถี่ของเสียงลดลง")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(self.DEFINITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_LOUDNESS,
                             hint="ความเข้มเสียงวัดเป็น W/m² ระดับเสียงวัดเป็นเดซิเบล ส่วนความถี่วัดเป็นเฮิรตซ์")
        band = rng.randrange(3)
        f = (rng.randint(1, 19) if band == 0 else
             rng.choice((rng.randint(2, 99) * 10, rng.randint(1, 19) * 1_000)) if band == 1 else
             rng.randint(21, 100) * 1_000)
        correct = classify_frequency(f)
        return _labelled(
            stem=f"เสียงความถี่ {f:,} เฮิรตซ์ จัดเป็นเสียงประเภทใด",
            correct=correct, wrongs=tuple(c for c in FREQUENCY_CLASSES if c != correct),
            topic=TOPIC_LOUDNESS,
            hint="หูมนุษย์ได้ยินความถี่ประมาณ 20 ถึง 20,000 เฮิรตซ์ ต่ำกว่านั้นเป็นคลื่นใต้เสียง สูงกว่าเป็นคลื่นเหนือเสียง")


@question_type(
    "phys.sound_intensity_fluency",
    display_name={"th": "อธิบายความสัมพันธ์ระหว่างความเข้มเสียงกับระดับเสียง และผลต่อการได้ยิน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LOUDNESS,
)
class SoundIntensityFluency(QuestionType):
    """Both objects of the indicator: intensity against level, and what level and
    frequency do to hearing."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            n = rng.randint(1, 4)
            factor = 10 ** n
            return _labelled(
                stem=f"ถ้าความเข้มเสียงเพิ่มขึ้นเป็น {factor:,} เท่า ระดับเสียงจะเพิ่มขึ้นกี่เดซิเบล",
                correct=f"{10 * n} เดซิเบล",
                wrongs=tuple(f"{x:,} เดซิเบล" for x in dict.fromkeys((factor, n, 20 * n, 10 * n + 10, factor * 10))
                             if x != 10 * n)[:3],
                topic=TOPIC_LOUDNESS,
                hint="ความเข้มเสียงเพิ่มขึ้น 10 เท่า ระดับเสียงเพิ่มขึ้น 10 เดซิเบล (เพิ่มแบบลอการิทึม)")
        if shape == 1:
            n = rng.randint(1, 4)
            return _labelled(
                stem=f"ระดับเสียงเพิ่มขึ้น {10 * n} เดซิเบล แสดงว่าความเข้มเสียงเพิ่มขึ้นกี่เท่า",
                correct=f"{10 ** n:,} เท่า",
                wrongs=tuple(f"{x:,} เท่า" for x in dict.fromkeys((10 * n, n, 10 ** (n + 1), 2 * 10 ** n))
                             if x != 10 ** n)[:3],
                topic=TOPIC_LOUDNESS,
                hint="ทุก ๆ 10 เดซิเบลที่เพิ่มขึ้น ความเข้มเสียงเพิ่มขึ้น 10 เท่า")
        if shape == 2:
            level, effect = rng.choice(HEARING_EFFECTS)
            return _labelled(
                stem=f"เสียงที่มีระดับเสียงประมาณ {level} เดซิเบล มีผลต่อการได้ยินอย่างไร",
                correct=effect, wrongs=tuple([e for lv, e in HEARING_EFFECTS if lv != level]),
                topic=TOPIC_LOUDNESS,
                hint="0 เดซิเบลเริ่มได้ยิน 60 เดซิเบลคือเสียงพูดคุย เกิน 85 เดซิเบลนาน ๆ เป็นอันตราย 120 เดซิเบลทำให้เจ็บหู")
        return _labelled(
            stem="ข้อใดกล่าวถึงผลของความถี่และระดับเสียงต่อการได้ยินได้ถูกต้อง",
            correct=rng.choice(HEARING_TRUE), wrongs=tuple(HEARING_FALSE),
            topic=TOPIC_LOUDNESS,
            hint="การได้ยินขึ้นกับทั้งความถี่ (ต้องอยู่ในช่วงที่หูรับได้) และระดับเสียง (ต้องดังพอแต่ไม่ดังจนเป็นอันตราย)")


@question_type(
    "phys.sound_intensity_application",
    display_name={"th": "คำนวณระดับเสียงจากความเข้มเสียงและจำนวนแหล่งกำเนิดเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LOUDNESS,
)
class SoundIntensityApplication(QuestionType):
    """β = 10 log(I/I₀) with I₀ = 10⁻¹² W/m², and ten sources instead of one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            k = rng.randint(1, 11)
            level = 10 * (12 - k)
            return _numeric(
                stem=(f"เสียงมีความเข้ม 10⁻{_sup(k)} วัตต์ต่อตารางเมตร ถ้าความเข้มเสียงต่ำสุดที่หูได้ยินคือ "
                      "10⁻¹² วัตต์ต่อตารางเมตร เสียงนี้มีระดับเสียงกี่เดซิเบล (β = 10 log(I/I₀))"),
                answer=level, wrongs=[12 - k, 10 * k, 10 * (12 + k)],
                unit="เดซิเบล", topic=TOPIC_LOUDNESS,
                hint="I/I₀ = 10^(12−k) ดังนั้น β = 10 × (12 − k)")
        if shape == 1:
            base = rng.choice((40, 50, 60, 70, 80))
            n = rng.choice((10, 100, 1000))
            added = 10 * len(str(n)[1:])
            what = rng.choice(("เครื่องจักร", "ลำโพง", "พัดลมอุตสาหกรรม"))
            return _numeric(
                stem=(f"{what}หนึ่งเครื่องทำให้ผู้ฟังได้ยินระดับเสียง {base} เดซิเบล ถ้าเปิด{what}ที่เหมือนกัน "
                      f"{n:,} เครื่องพร้อมกัน ณ ตำแหน่งเดิม ระดับเสียงเป็นกี่เดซิเบล"),
                answer=base + added, wrongs=[base * n, base + n, base * 2],
                unit="เดซิเบล", topic=TOPIC_LOUDNESS,
                hint="ความเข้มเสียงรวมเพิ่มเป็น n เท่า ทุก ๆ 10 เท่าของความเข้มเพิ่มระดับเสียง 10 เดซิเบล")
        level = rng.choice((70, 80, 90, 100, 110, 120))
        risky = level > 85
        return _labelled(
            stem=f"พนักงานทำงานในโรงงานที่มีระดับเสียง {level} เดซิเบลวันละ 8 ชั่วโมง ข้อใดเหมาะสมที่สุด",
            correct=("ควรสวมอุปกรณ์ป้องกันเสียง เพราะระดับเสียงเกิน 85 เดซิเบลเป็นเวลานานทำให้หูเสื่อม"
                     if risky else "ไม่จำเป็นต้องสวมอุปกรณ์ป้องกันเสียง เพราะระดับเสียงไม่เกิน 85 เดซิเบล"),
            wrongs=(("ไม่จำเป็นต้องสวมอุปกรณ์ป้องกันเสียง เพราะระดับเสียงไม่เกิน 85 เดซิเบล"
                     if risky else "ควรสวมอุปกรณ์ป้องกันเสียง เพราะระดับเสียงเกิน 85 เดซิเบลเป็นเวลานานทำให้หูเสื่อม"),
                    "ควรเปลี่ยนไปทำงานกะกลางคืน เพราะเสียงกลางคืนมีความถี่ต่ำกว่า",
                    "ไม่ต้องทำอะไร เพราะหูจะปรับตัวจนชินกับเสียงดังได้เอง"),
            topic=TOPIC_LOUDNESS,
            hint="มาตรฐานความปลอดภัยทั่วไปกำหนดให้ไม่ฟังเสียงเกิน 85 เดซิเบลต่อเนื่องวันละ 8 ชั่วโมง")
