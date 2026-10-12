"""การจัดเรียงอิเล็กตรอนในอะตอม

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/3

Sets moved here from: science_wave_f19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f19 import REPRESENTATIVE, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_CONFIG = "การจัดเรียงอิเล็กตรอนในอะตอม"


SUBSHELLS = (("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6), ("4s", 2), ("3d", 10), ("4p", 6), ("5s", 2))


SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def subshell_config(z: int) -> list[tuple[str, int]]:
    """Aufbau filling with the chromium and copper exceptions."""
    left, config = z, []
    for name, cap in SUBSHELLS:
        if left <= 0:
            break
        take = min(cap, left)
        config.append((name, take))
        left -= take
    if z in (24, 29):
        config = [(n, c) for n, c in config if n not in ("4s", "3d")]
        config += [("4s", 1), ("3d", 5 if z == 24 else 10)]
    return config


def config_text(config) -> str:
    ordered = sorted(config, key=lambda p: (int(p[0][0]), "spdf".index(p[0][1])))
    return " ".join(f"{n}{str(c).translate(SUPERSCRIPT)}" for n, c in ordered)


def main_levels(z: int) -> list[int]:
    levels: dict[int, int] = {}
    for name, count in subshell_config(z):
        levels[int(name[0])] = levels.get(int(name[0]), 0) + count
    return [levels[k] for k in sorted(levels)]


@question_type(
    "chem.electron_config_foundation",
    display_name={"th": "การจัดเรียงอิเล็กตรอนในระดับพลังงานหลัก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONFIG,
)
class ElectronConfigFoundation(QuestionType):
    """2, 8, 8, … by main level for the first twenty elements."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        z = rng.randint(3, 36)
        levels = lambda n: ", ".join(str(x) for x in main_levels(n))
        right = levels(z)
        # Neighbouring elements, and filling the third level to 18 before the fourth.
        pool = {levels(w) for w in (z - 1, z + 1, z + 2)}
        if 18 < z <= 20:
            pool.add(f"2, 8, {z - 10}")
        pool.discard(right)
        return _labelled(stem=f"ธาตุที่มีเลขอะตอม {z} จัดเรียงอิเล็กตรอนในระดับพลังงานหลักอย่างไร",
                         correct=right, wrongs=tuple(sorted(pool)), topic=TOPIC_CONFIG,
                         hint="เติมอิเล็กตรอนตามลำดับระดับพลังงานย่อย 1s 2s 2p 3s 3p 4s 3d 4p แล้วรวมตามระดับพลังงานหลัก (20 ธาตุแรกเป็น 2, 8, 8, 2)")


@question_type(
    "chem.electron_config_fluency",
    display_name={"th": "การจัดเรียงอิเล็กตรอนในระดับพลังงานย่อย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONFIG,
)
class ElectronConfigFluency(QuestionType):
    """1s² 2s² 2p⁶ … by the aufbau order, including 4s before 3d."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        z = rng.randint(3, 36)
        right = config_text(subshell_config(z))
        wrong_pool = {config_text(subshell_config(w)) for w in (z - 2, z - 1, z + 1, z + 2) if 1 <= w <= 38}
        if z > 20:
            # Filling 3d before 4s, a common slip.
            naive, left = [], z
            for name, cap in (("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6), ("3d", 10), ("4s", 2), ("4p", 6)):
                if left <= 0:
                    break
                naive.append((name, min(cap, left)))
                left -= min(cap, left)
            wrong_pool.add(config_text(naive))
        wrong_pool.discard(right)
        return _labelled(stem=f"ธาตุที่มีเลขอะตอม {z} จัดเรียงอิเล็กตรอนในระดับพลังงานย่อยอย่างไร",
                         correct=right, wrongs=tuple(sorted(wrong_pool)), topic=TOPIC_CONFIG,
                         hint="เติมอิเล็กตรอนตามลำดับ 1s 2s 2p 3s 3p 4s 3d 4p (Cr และ Cu เป็นข้อยกเว้น)")


@question_type(
    "chem.electron_config_application",
    display_name={"th": "เวเลนซ์อิเล็กตรอน หมู่ และคาบจากการจัดเรียงอิเล็กตรอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONFIG,
)
class ElectronConfigApplication(QuestionType):
    """Valence electrons, and the period and group a configuration places an element in."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element = rng.choice([e for e in REPRESENTATIVE if e[0] <= 36])
        z, _, _, period, group = element
        valence = group if group <= 2 else group - 10
        shape = rng.randrange(3)
        given = config_text(subshell_config(z))
        if shape == 0:
            return numeric(stem=f"ธาตุที่จัดเรียงอิเล็กตรอนเป็น {given} มีเวเลนซ์อิเล็กตรอนกี่ตัว",
                           answer=valence, wrongs=[period, z % 8 or 8, valence + 2], unit="ตัว", topic=TOPIC_CONFIG,
                           hint="เวเลนซ์อิเล็กตรอนคืออิเล็กตรอนในระดับพลังงานหลักชั้นนอกสุด (s และ p ชั้นสุดท้าย)")
        if shape == 1:
            return numeric(stem=f"ธาตุที่จัดเรียงอิเล็กตรอนเป็น {given} อยู่คาบที่เท่าใด", answer=period,
                           wrongs=[valence, period + 1, len(subshell_config(z))], unit="", topic=TOPIC_CONFIG,
                           hint="คาบเท่ากับเลขระดับพลังงานหลักชั้นนอกสุดที่มีอิเล็กตรอน")
        return numeric(stem=f"ธาตุที่จัดเรียงอิเล็กตรอนเป็น {given} อยู่หมู่ที่เท่าใด (ระบบ 1-18)", answer=group,
                       wrongs=[valence if valence != group else group + 1, group + 2, period], unit="",
                       topic=TOPIC_CONFIG, hint="หมู่ 1-2 เท่ากับจำนวนเวเลนซ์อิเล็กตรอน หมู่ 13-18 เท่ากับเวเลนซ์อิเล็กตรอน + 10")
