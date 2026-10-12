"""ชั้นบรรยากาศ

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/1

Sets moved here from: science_wave_c16.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import ATMOSPHERE_ALT, ATMOSPHERE_ASSET, diagram_question
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c15 import FIVE_LETTERS
from otk.sets._support.science_wave_c16 import LAYER_SCENARIOS

PROVENANCE = Provenance("original")


LAYER_TOPIC = "ชั้นบรรยากาศ"


class Layer(NamedTuple):
    """A layer of the atmosphere by temperature, and what it does for us."""
    name: str
    span: str
    trend: str
    benefit: str


# In order from the ground up; the IPST ม.1 division by temperature.
LAYERS = (
    Layer("โทรโพสเฟียร์", "ผิวโลกถึงประมาณ 10 กิโลเมตร", "อุณหภูมิลดลงเมื่อสูงขึ้น",
          "มีไอน้ำและเกิดเมฆ ฝน และลมฟ้าอากาศ ซึ่งสิ่งมีชีวิตใช้ดำรงชีวิต"),
    Layer("สตราโตสเฟียร์", "ประมาณ 10 ถึง 50 กิโลเมตร", "อุณหภูมิสูงขึ้นเมื่อสูงขึ้น",
          "มีแก๊สโอโซนดูดกลืนรังสีอัลตราไวโอเลตที่เป็นอันตรายต่อสิ่งมีชีวิต"),
    Layer("มีโซสเฟียร์", "ประมาณ 50 ถึง 80 กิโลเมตร", "อุณหภูมิลดลงเมื่อสูงขึ้นจนต่ำที่สุด",
          "ทำให้วัตถุจากอวกาศเสียดสีกับอากาศและลุกไหม้เป็นดาวตก ก่อนตกถึงพื้นโลก"),
    Layer("เทอร์โมสเฟียร์", "ประมาณ 80 ถึง 500 กิโลเมตร", "อุณหภูมิสูงขึ้นอย่างรวดเร็วเมื่อสูงขึ้น",
          "มีอนุภาคมีประจุสะท้อนคลื่นวิทยุ ทำให้สื่อสารระยะไกลได้"),
    Layer("เอกโซสเฟียร์", "สูงกว่าประมาณ 500 กิโลเมตรขึ้นไป", "อากาศเบาบางมากจนเกือบเป็นอวกาศ",
          "เป็นบริเวณที่ดาวเทียมหลายดวงโคจรอยู่"),
)


def _layer_statement(name: str, layer: Layer) -> str:
    return f"{name} อยู่ที่{layer.span} และ{layer.trend}"


def _match_benefits(letters: list[str]) -> str:
    return " / ".join(f"{layer.name} → {letter}" for layer, letter in zip(LAYERS, letters))


@question_type(
    "geo.atmosphere_layers_foundation",
    display_name={"th": "อธิบายการแบ่งชั้นบรรยากาศจากแบบจำลอง"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=LAYER_TOPIC,
)
class AtmosphereLayersFoundation(QuestionType):
    """Name a layer from its height and temperature trend, read off the model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        """The indicator says จากแบบจำลอง, so the model is shown, not listed.

        Only the four plotted layers can be asked about by number; all five stay
        available as distractors, because mistaking เทอร์โมสเฟียร์ for
        เอกโซสเฟียร์ is the confusion worth offering.
        """
        number = rng.randint(1, 4)
        layer = LAYERS[number - 1]
        others = [other for other in LAYERS if other.name != layer.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            stem = f"จากแบบจำลอง บรรยากาศชั้นที่กำกับด้วยหมายเลข {number} คือชั้นใด"
            correct = layer.name
            wrongs = tuple(other.name for other in others[:3])
        else:
            stem = f"จากแบบจำลอง ข้อใดอธิบายบรรยากาศชั้นที่กำกับด้วยหมายเลข {number} ได้ถูกต้อง"
            correct = _layer_statement(layer.name, layer)
            wrongs = tuple(_layer_statement(other.name, other) for other in others[:3])
        return diagram_question(
            ATMOSPHERE_ASSET, ATMOSPHERE_ALT,
            stem=stem, correct=correct, wrongs=wrongs,
            hint=("ไล่จากผิวโลกขึ้นไปทีละหมายเลข แล้วดูจากกราฟว่าอุณหภูมิลดลงหรือเพิ่มขึ้น"
                  "เมื่อความสูงเพิ่มขึ้นในช่วงนั้น"),
            topic=LAYER_TOPIC,
        )


@question_type(
    "geo.atmosphere_layers_fluency",
    display_name={"th": "เปรียบเทียบประโยชน์ของบรรยากาศแต่ละชั้น"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=LAYER_TOPIC,
)
class AtmosphereLayersFluency(QuestionType):
    """Place every layer against its benefit; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shuffled = list(LAYERS)
        rng.shuffle(shuffled)
        listing = " / ".join(f"{letter}. {layer.benefit}"
                             for letter, layer in zip(FIVE_LETTERS, shuffled))
        letter_of = {layer.name: FIVE_LETTERS[i] for i, layer in enumerate(shuffled)}
        right = [letter_of[layer.name] for layer in LAYERS]
        return _labelled(
            stem=f"ประโยชน์ของบรรยากาศ 5 ข้อ — {listing} "
                 "ข้อใดเปรียบเทียบประโยชน์ของบรรยากาศแต่ละชั้นได้ถูกต้องทั้งหมด",
            correct=_match_benefits(right),
            wrongs=tuple(_match_benefits(_swapped(right, i, j)) for i, j in _swaps(rng, 3, 5)),
            hint="เริ่มจากชั้นที่มีลมฟ้าอากาศและชั้นที่มีโอโซน แล้วไล่ขึ้นไปทีละชั้น",
            topic=LAYER_TOPIC,
        )


@question_type(
    "geo.atmosphere_layers_application",
    display_name={"th": "ใช้ความรู้เรื่องชั้นบรรยากาศอธิบายเหตุการณ์"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=LAYER_TOPIC,
)
class AtmosphereLayersApplication(QuestionType):
    """Why planes cruise where they do, what losing ozone means, and meteors."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LAYER_SCENARIOS,
            hint="นึกว่าเหตุการณ์นั้นเกิดในชั้นใด และชั้นนั้นมีลักษณะอย่างไร",
        ), LAYER_TOPIC)
