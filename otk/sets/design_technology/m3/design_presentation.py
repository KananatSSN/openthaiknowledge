"""เทคนิคการนำเสนอแนวทางการแก้ปัญหา

การออกแบบและเทคโนโลยี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.3/3

Sets moved here from: technology_t2s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s3 import M3, _pair_either_way

PROVENANCE = Provenance("original")


PRESENT_TOPIC = "เทคนิคการนำเสนอแนวทางการแก้ปัญหา"


TECHNIQUES = (
    ("แสดงรูปทรงสามมิติของชิ้นงานในภาพเดียว โดยแกนทั้งสามทำมุมเท่ากัน", "ภาพไอโซเมตริก"),
    ("แสดงด้านหน้า ด้านข้าง และด้านบนของชิ้นงานพร้อมขนาดจริง", "ภาพฉาย"),
    ("แสดงชิ้นส่วนที่แยกออกจากกันเพื่อบอกวิธีประกอบ", "ภาพแยกชิ้นส่วน"),
    ("ให้ผู้ใช้จับต้องและทดลองรูปทรงจริงในขนาดย่อส่วน", "แบบจำลอง"),
    ("แสดงลำดับการทำงานและเงื่อนไขของระบบ", "ผังงาน"),
    ("บันทึกความคิดเบื้องต้นอย่างรวดเร็วด้วยมือ", "ภาพร่างอย่างง่าย"),
)


VIEWS = {"ด้านหน้า": ("width", "height"), "ด้านบน": ("width", "depth"), "ด้านข้าง": ("depth", "height")}


def _size(a: int, b: int) -> str:
    return f"{a} × {b} เซนติเมตร"


def _clock(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d} น."


@question_type(
    "tech.design_presentation_foundation",
    display_name={"th": "เลือกเทคนิคการนำเสนอแนวทางการแก้ปัญหา"},
    level=M3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DesignPresentationFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, TECHNIQUES,
                                forward="ต้องการ{} ควรใช้เทคนิคการนำเสนอใด",
                                backward="{}เหมาะสำหรับใช้ทำสิ่งใด",
                                hint="ภาพไอโซเมตริกให้เห็นสามมิติ ภาพฉายบอกขนาดแต่ละด้าน ภาพแยกชิ้นส่วนบอกการประกอบ "
                                     "แบบจำลองให้จับต้องได้ ผังงานบอกลำดับการทำงาน",
                                topic=PRESENT_TOPIC)


@question_type(
    "tech.design_presentation_fluency",
    display_name={"th": "อ่านขนาดจากภาพฉายด้านหน้า ด้านบน และด้านข้าง"},
    level=M3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DesignPresentationFluency(QuestionType):
    def build(self, rng: Random, **params):
        dims = dict(zip(("width", "depth", "height"), rng.sample(range(8, 61, 2), 3)))
        view = rng.choice(list(VIEWS))
        first, second = VIEWS[view]
        correct = _size(dims[first], dims[second])
        wrongs = [_size(dims[a], dims[b]) for v, (a, b) in VIEWS.items() if v != view]
        wrongs.append(_size(dims["width"] + dims["depth"], dims["height"]))
        return _labelled(
            stem=(f"กล่องทรงสี่เหลี่ยมมุมฉากกว้าง {dims['width']} เซนติเมตร ลึก {dims['depth']} เซนติเมตร "
                  f"และสูง {dims['height']} เซนติเมตร ในภาพฉาย{view} จะเห็นเป็นรูปสี่เหลี่ยมขนาดเท่าใด"),
            correct=correct, wrongs=tuple(wrongs),
            hint="ภาพด้านหน้าเห็นความกว้างกับความสูง ภาพด้านบนเห็นความกว้างกับความลึก ภาพด้านข้างเห็นความลึกกับความสูง",
            topic=PRESENT_TOPIC,
        )


@question_type(
    "tech.design_presentation_application",
    display_name={"th": "วางแผนขั้นตอนการทำงานที่ทำพร้อมกันได้"},
    level=M3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DesignPresentationApplication(QuestionType):
    """Two jobs side by side, then a third that needs both."""

    def build(self, rng: Random, **params):
        cut, wire, build = (rng.randrange(20, 95, 5) for _ in range(3))
        while cut == wire:
            wire = rng.randrange(20, 95, 5)
        start = rng.randrange(8 * 60, 13 * 60 + 1, 30)
        total = max(cut, wire) + build
        answer = start + total
        wrongs = _near(answer, (start + cut + wire + build, start + min(cut, wire) + build,
                                start + max(cut, wire), answer + 30))
        return _labelled(
            stem=(f"กลุ่มหนึ่งมีสองคน คนแรกตัดชิ้นส่วนใช้เวลา {cut} นาที คนที่สองเตรียมวงจรไฟฟ้าใช้เวลา {wire} นาที "
                  f"ทั้งสองงานทำพร้อมกันได้ เมื่อทั้งสองงานเสร็จแล้วจึงประกอบชิ้นงานร่วมกันอีก {build} นาที "
                  f"ถ้าเริ่มเวลา {_clock(start)} งานจะเสร็จเร็วที่สุดเวลาใด"),
            correct=_clock(answer), wrongs=tuple(_clock(w) for w in rng.sample(wrongs, 3)),
            hint="งานที่ทำพร้อมกันเสร็จเมื่องานที่นานกว่าเสร็จ จากนั้นจึงบวกเวลาประกอบ",
            topic=PRESENT_TOPIC,
        )
