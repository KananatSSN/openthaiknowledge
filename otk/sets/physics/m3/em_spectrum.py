"""คลื่นแม่เหล็กไฟฟ้าและสเปกตรัม

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/11, ว 2.3 ม.3/12

Sets moved here from: physics, science_wave_a7.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a7 import WAVES

PROVENANCE = Provenance("original")


LOWER = {"th": "ม.3"}


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...],
              hint: str) -> GeneratedQuestion:
    """A question whose choices are all Thai labels drawn from one pool."""
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=WAVES,
        hint=[text(hint)],
    )


# The seven bands in order of increasing frequency, which is decreasing
# wavelength. Order is carried by position in this tuple and nowhere else, so an
# ordering question and a wavelength question can never disagree.
# (ชื่อคลื่น, การใช้ประโยชน์ที่พบบ่อย, อันตรายหรือข้อควรระวัง)
EM_BANDS = (
    ("คลื่นวิทยุ", "ใช้ส่งสัญญาณวิทยุกระจายเสียงและโทรทัศน์",
     "รบกวนการทำงานของเครื่องมือสื่อสารอื่นเมื่อใช้กำลังส่งสูงในย่านเดียวกัน"),
    ("ไมโครเวฟ", "ใช้ในเตาไมโครเวฟและการสื่อสารผ่านดาวเทียม",
     "ทำให้เนื้อเยื่อที่มีน้ำร้อนขึ้นจนเป็นอันตรายเมื่อได้รับปริมาณมาก"),
    ("รังสีอินฟราเรด", "ใช้ในรีโมตคอนโทรลและกล้องถ่ายภาพความร้อน",
     "ทำให้ผิวหนังร้อนจัดจนไหม้ได้เมื่ออยู่ใกล้แหล่งความร้อนแรงเป็นเวลานาน"),
    ("แสงที่มองเห็นได้", "ทำให้มนุษย์มองเห็นและพืชสังเคราะห์ด้วยแสงได้",
     "แสงจ้าเกินไปทำให้จอตาเสียหายเมื่อจ้องโดยตรง"),
    ("รังสีอัลตราไวโอเลต", "ใช้ฆ่าเชื้อโรคในเครื่องมือแพทย์และในน้ำ",
     "ทำให้ผิวหนังไหม้แดดและเพิ่มความเสี่ยงของมะเร็งผิวหนัง"),
    ("รังสีเอกซ์", "ใช้ถ่ายภาพกระดูกและฟันทางการแพทย์",
     "ทำลายเซลล์และสารพันธุกรรมเมื่อได้รับสะสมเป็นปริมาณมาก"),
    ("รังสีแกมมา", "ใช้ฉายรังสีรักษามะเร็งและถนอมอาหาร",
     "ทะลุทะลวงสูงมากและทำลายเซลล์ได้รุนแรง ต้องกำบังด้วยตะกั่วหรือคอนกรีตหนา"),
)


EM_NAMES = tuple(name for name, _, _ in EM_BANDS)


# (งาน, ช่วงคลื่นที่เหมาะสม) — jobs other than each band's headline use
EM_JOBS = (
    ("ตรวจหาผู้รอดชีวิตในที่มืดด้วยกล้องที่จับความร้อนจากร่างกาย", "รังสีอินฟราเรด"),
    ("อุ่นอาหารให้ร้อนจากภายในอย่างรวดเร็ว", "ไมโครเวฟ"),
    ("ตรวจกระเป๋าเดินทางที่สนามบินโดยไม่ต้องเปิด", "รังสีเอกซ์"),
    ("ฆ่าเชื้อในน้ำดื่มโดยไม่ใช้สารเคมี", "รังสีอัลตราไวโอเลต"),
    ("ฆ่าเชื้อในเครื่องมือแพทย์ที่ห่อพลาสติกปิดสนิทแล้ว", "รังสีแกมมา"),
    ("ส่งสัญญาณสถานีวิทยุ FM", "คลื่นวิทยุ"),
    ("เรดาร์ตรวจจับความเร็วของรถบนถนน", "ไมโครเวฟ"),
    ("ตรวจธนบัตรปลอมด้วยหมึกที่เรืองแสง", "รังสีอัลตราไวโอเลต"),
    ("ถ่ายภาพฟันเพื่อหาฟันผุ", "รังสีเอกซ์"),
    ("ส่งสัญญาณ Wi-Fi ภายในบ้าน", "ไมโครเวฟ"),
    ("ให้พืชในโรงเรือนสังเคราะห์ด้วยแสง", "แสงที่มองเห็นได้"),
    ("ตรวจรอยร้าวภายในชิ้นโลหะหนาในโรงงาน", "รังสีแกมมา"),
    ("เปิดปิดโทรทัศน์ด้วยรีโมตคอนโทรล", "รังสีอินฟราเรด"),
    ("สื่อสารกับเรือกลางทะเลในระยะไกล", "คลื่นวิทยุ"),
)


EM_HAZARDS = tuple(hazard for _, _, hazard in EM_BANDS)


# (สถานการณ์, คำตอบที่ถูกต้อง, ตัวลวงสามข้อ). Each wrong choice names a real band
# with a real property of it — the mistake is the match to the job, never an
# invented fact.
EM_SCENARIOS = (
    ("โรงพยาบาลต้องการตรวจดูว่ากระดูกแขนของผู้ป่วยหักหรือไม่ โดยไม่ต้องผ่าตัด "
     "ควรใช้คลื่นแม่เหล็กไฟฟ้าช่วงใด และต้องระวังเรื่องใด",
     "รังสีเอกซ์ เพราะทะลุผ่านเนื้อเยื่อแต่ถูกกระดูกดูดกลืน จึงต้องจำกัดปริมาณและกำบังส่วนอื่นของร่างกาย",
     ("แสงที่มองเห็นได้ เพราะให้ภาพที่ชัดที่สุด จึงต้องระวังไม่ให้แสงจ้าเกินไป",
      "คลื่นวิทยุ เพราะทะลุผ่านร่างกายได้โดยไม่เป็นอันตรายเลย จึงไม่ต้องระวังสิ่งใด",
      "รังสีแกมมา เพราะทะลุทะลวงสูงที่สุด จึงให้ภาพกระดูกที่คมชัดที่สุด")),
    ("ต้องการฆ่าเชื้อโรคบนผิวของเครื่องมือผ่าตัดโดยไม่ใช้ความร้อน "
     "ควรใช้คลื่นแม่เหล็กไฟฟ้าช่วงใด และต้องระวังเรื่องใด",
     "รังสีอัลตราไวโอเลต เพราะทำลายสารพันธุกรรมของจุลินทรีย์ได้ จึงต้องไม่ให้ผิวหนังและดวงตาสัมผัสโดยตรง",
     ("รังสีอินฟราเรด เพราะให้ความร้อนสูง จึงต้องระวังไม่ให้เครื่องมือละลาย",
      "ไมโครเวฟ เพราะทำให้น้ำในเซลล์ของเชื้อโรคเดือด จึงต้องระวังไม่ให้เครื่องมือเปียก",
      "คลื่นวิทยุ เพราะมีความยาวคลื่นยาวจึงกระจายได้ทั่วถึง จึงต้องระวังสัญญาณรบกวน")),
    ("นักเรียนต้องการวัดว่าผนังห้องส่วนใดรั่วความร้อนออกไปมากที่สุด "
     "ควรใช้เครื่องมือที่ตรวจจับคลื่นช่วงใด",
     "รังสีอินฟราเรด เพราะวัตถุที่อุ่นกว่าแผ่รังสีอินฟราเรดออกมามากกว่า",
     ("รังสีอัลตราไวโอเลต เพราะวัตถุที่ร้อนกว่าแผ่รังสีอัลตราไวโอเลตออกมามากกว่า",
      "คลื่นวิทยุ เพราะทะลุผ่านผนังได้ จึงบอกตำแหน่งรอยรั่วได้",
      "รังสีเอกซ์ เพราะทะลุผ่านผนังและแสดงโครงสร้างภายในได้")),
    ("จะสื่อสารกับเรือที่อยู่กลางทะเลซึ่งอยู่ไกลจากฝั่งมาก "
     "ควรใช้คลื่นแม่เหล็กไฟฟ้าช่วงใด",
     "คลื่นวิทยุ เพราะเดินทางได้ไกลและเลี้ยวเบนผ่านสิ่งกีดขวางได้ดี",
     ("แสงที่มองเห็นได้ เพราะเดินทางเป็นเส้นตรงจึงส่งได้ตรงเป้าหมายที่สุด",
      "รังสีเอกซ์ เพราะมีพลังงานสูงจึงส่งได้ไกลที่สุด",
      "รังสีอัลตราไวโอเลต เพราะไม่ถูกน้ำทะเลดูดกลืน")),
    ("ผู้ที่ทำงานกลางแจ้งตลอดวันควรป้องกันตนเองจากคลื่นแม่เหล็กไฟฟ้าช่วงใดเป็นพิเศษ "
     "และป้องกันอย่างไร",
     "รังสีอัลตราไวโอเลตจากดวงอาทิตย์ โดยทาครีมกันแดดและสวมเสื้อแขนยาวกับหมวก",
     ("รังสีแกมมาจากดวงอาทิตย์ โดยสวมเสื้อผ้าที่บุด้วยตะกั่ว",
      "คลื่นวิทยุจากเสาส่งสัญญาณ โดยหลีกเลี่ยงการใช้โทรศัพท์กลางแจ้ง",
      "แสงที่มองเห็นได้ โดยหลับตาเป็นระยะขณะทำงาน")),
    ("เตาไมโครเวฟทำให้อาหารร้อนได้อย่างไร และเหตุใดจึงต้องมีตะแกรงโลหะที่ประตูเตา",
     "คลื่นทำให้โมเลกุลของน้ำในอาหารสั่นจนเกิดความร้อน และตะแกรงกันไม่ให้ไมโครเวฟออกมาสู่ผู้ใช้",
     ("คลื่นทำให้อากาศในเตาร้อนแล้วถ่ายเทความร้อนสู่อาหาร และตะแกรงช่วยเก็บความร้อนไว้",
      "คลื่นเปลี่ยนอาหารให้เป็นสารกัมมันตรังสีชั่วคราว และตะแกรงกันรังสีที่เกิดขึ้น",
      "คลื่นทำให้โมเลกุลของน้ำแตกตัวเป็นไอออน และตะแกรงกันไอออนไม่ให้รั่วออกมา")),
)


@question_type("phys.em_spectrum",
               display_name={"th": "สเปกตรัมคลื่นแม่เหล็กไฟฟ้าและการใช้ประโยชน์"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class EMSpectrum(ClassifyType):
    """จับคู่ช่วงคลื่นแม่เหล็กไฟฟ้ากับลักษณะเด่นและการประยุกต์ใช้."""

    CLASSIFY_STEM = "การใช้ประโยชน์ต่อไปนี้เป็นของคลื่นกลุ่มใด: “{member}”"
    PICK_STEM = "ข้อใดคือลักษณะเด่นหรือการใช้ประโยชน์ของ{category}"

    CATEGORIES = [
        Category("คลื่นวิทยุและไมโครเวฟ (Radio & Microwave)",
                 ("ใช้ในระบบสื่อสารโทรคมนาคมและวิทยุกระจายเสียง",
                  "ใช้ในระบบเรดาร์ตรวจจับตำแหน่ง",
                  "ทำให้อนุภาคของน้ำในอาหารสั่นจนเกิดความร้อน")),
        Category("รังสีอินฟราเรดและแสงที่มองเห็นได้ (Infrared & Visible Light)",
                 ("ใช้ในการทำงานของรีโมตคอนโทรล",
                  "ใช้ในกล้องถ่ายภาพความร้อน (Thermal camera)",
                  "ช่วยให้กระบวนการมองเห็นของมนุษย์ทำงานได้",
                  "พืชใช้เป็นพลังงานในการสังเคราะห์ด้วยแสง")),
        Category("คลื่นพลังงานสูง (UV, X-ray, Gamma ray)",
                 ("ใช้ตรวจวินิจฉัยกระดูกและฟันทางการแพทย์",
                  "ใช้ฉายรังสีเพื่อรักษามะเร็ง",
                  "ใช้ฆ่าเชื้อโรคในเครื่องมือแพทย์",
                  "อาจก่อให้เกิดมะเร็งผิวหนังหรือทำลายเนื้อเยื่อได้")),
    ]


@question_type(
    "phys.em_spectrum_fluency",
    display_name={"th": "ลำดับของสเปกตรัมคลื่นแม่เหล็กไฟฟ้าและอันตรายของแต่ละช่วง"},
    level=LOWER, subject=SUBJECT, topic=WAVES,
)
class EMSpectrumFluency(QuestionType):
    """Place a band in the spectrum, and say what each band's danger is.

    `phys.em_spectrum` sorts uses into three broad groups. Neither the order of
    the spectrum — which is what ``ม.3/11`` names — nor the danger belonging to
    each band, which is half of ``ม.3/12``, is reachable from those groups.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            return self._extreme(rng)
        if which == 1:
            return self._higher(rng)
        return self._hazard(rng)

    def _extreme(self, rng: Random) -> GeneratedQuestion:
        picked = rng.sample(range(len(EM_BANDS)), 4)
        longest = rng.random() < 0.5
        target = min(picked) if longest else max(picked)
        wanted = "ความยาวคลื่นมากที่สุด" if longest else "ความถี่สูงที่สุด"
        return _labelled(
            stem=f"ในคลื่นแม่เหล็กไฟฟ้าต่อไปนี้ คลื่นใดมี{wanted}",
            correct=EM_NAMES[target],
            wrongs=tuple(EM_NAMES[index] for index in picked if index != target),
            hint="เรียงสเปกตรัมจากคลื่นวิทยุไปหารังสีแกมมา ความถี่เพิ่มขึ้นและ"
                 "ความยาวคลื่นลดลงไปตามลำดับ",
        )

    def _higher(self, rng: Random) -> GeneratedQuestion:
        # A reference band with at least one band above and three below, so
        # exactly one of the four choices is the higher-frequency one.
        reference = rng.randrange(3, len(EM_BANDS) - 1)
        above = rng.randrange(reference + 1, len(EM_BANDS))
        below = rng.sample(range(reference), 3)
        return _labelled(
            stem=(f"คลื่นใดต่อไปนี้มีความถี่สูงกว่า{EM_NAMES[reference]}"),
            correct=EM_NAMES[above],
            wrongs=tuple(EM_NAMES[index] for index in below),
            hint="คลื่นที่อยู่ทางด้านรังสีแกมมาของสเปกตรัมมีความถี่สูงกว่าเสมอ",
        )

    def _hazard(self, rng: Random) -> GeneratedQuestion:
        index = rng.randrange(len(EM_BANDS))
        name, _, hazard = EM_BANDS[index]
        others = [other for other in EM_NAMES if other != name]
        rng.shuffle(others)
        return _labelled(
            stem=f"อันตรายต่อไปนี้เกิดจากคลื่นแม่เหล็กไฟฟ้าช่วงใด: “{hazard}”",
            correct=name,
            wrongs=tuple(others[:3]),
            hint="ดูว่าอันตรายนั้นเป็นความร้อน การไหม้ของผิวหนัง หรือการทำลายเซลล์ "
                 "ซึ่งบอกได้ว่าคลื่นมีพลังงานระดับใด",
        )


@question_type(
    "phys.em_spectrum_application",
    display_name={"th": "เลือกใช้คลื่นแม่เหล็กไฟฟ้าให้เหมาะกับงานและป้องกันอันตราย"},
    level=LOWER, subject=SUBJECT, topic=WAVES,
)
class EMSpectrumApplication(QuestionType):
    """Choose the band a real job needs, and name what it costs to use it.

    ``ม.3/12`` is about weighing ประโยชน์ against อันตราย in everyday life, so
    every item here states both halves and every distractor is a real band whose
    real property simply does not fit the job.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            job, band = rng.choice(EM_JOBS)
            return _labelled(
                stem=f"งาน \"{job}\" ควรใช้คลื่นแม่เหล็กไฟฟ้าช่วงใด",
                correct=band,
                wrongs=tuple([n for n in EM_NAMES if n != band]),
                hint="ถามตัวเองก่อนว่างานนั้นต้องการให้คลื่นทะลุผ่าน สะท้อน ให้ความร้อน หรือทำลายเชื้อ",
            )
        if roll < 0.7:
            name, _, hazard = rng.choice(EM_BANDS)
            return _labelled(
                stem=f"ผู้ที่ทำงานกับ{name}เป็นประจำควรระวังอันตรายข้อใดมากที่สุด",
                correct=hazard,
                wrongs=tuple([h for h in EM_HAZARDS if h != hazard]),
                hint="คลื่นความถี่สูงทำลายเซลล์ได้ คลื่นความถี่ต่ำกว่ามักก่อความร้อนหรือรบกวนสัญญาณ",
            )
        stem, correct, wrongs = rng.choice(EM_SCENARIOS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="ถามตัวเองก่อนว่างานนั้นต้องการให้คลื่นทะลุผ่าน สะท้อน หรือให้พลังงาน "
                 "แล้วจึงดูว่าช่วงคลื่นนั้นมีอันตรายแบบใด",
        )
