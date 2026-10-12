"""กัมมันตภาพรังสีและรังสีแอลฟา บีตา แกมมา

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/13

Sets moved here from: science_wave_f17.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f17 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_RAYS = "กัมมันตภาพรังสีและรังสีแอลฟา บีตา แกมมา"


RAY_PROPERTIES = (
    ("รังสีแอลฟา", "คือนิวเคลียสของฮีเลียม มีประจุ +2 ถูกกั้นได้ด้วยกระดาษแผ่นเดียว"),
    ("รังสีบีตา", "คืออิเล็กตรอนพลังงานสูง มีประจุ −1 ถูกกั้นได้ด้วยแผ่นอะลูมิเนียมบาง ๆ"),
    ("รังสีแกมมา", "คือคลื่นแม่เหล็กไฟฟ้าพลังงานสูง ไม่มีประจุ ต้องใช้ตะกั่วหนาหรือคอนกรีตกั้น"),
)


RAY_FACTS = (
    ("รังสีชนิดใดทำให้อากาศแตกตัวเป็นไอออนได้มากที่สุด", "รังสีแอลฟา", ("รังสีบีตา", "รังสีแกมมา", "ทั้งสามชนิดเท่ากัน")),
    ("รังสีชนิดใดทะลุผ่านวัตถุได้มากที่สุด", "รังสีแกมมา", ("รังสีแอลฟา", "รังสีบีตา", "ทั้งสามชนิดเท่ากัน")),
    ("รังสีชนิดใดไม่เบี่ยงเบนในสนามแม่เหล็ก", "รังสีแกมมา", ("รังสีแอลฟา", "รังสีบีตา", "ทั้งแอลฟาและบีตา")),
    ("ในสนามไฟฟ้า รังสีบีตาเบนไปทางใด", "ไปทางขั้วบวก เพราะมีประจุลบ", ("ไปทางขั้วลบ", "ไม่เบน", "เบนตั้งฉากกับแผ่นขั้วออกนอกหน้ากระดาษ")),
    ("กัมมันตภาพรังสีคืออะไร", "ปรากฏการณ์ที่นิวเคลียสที่ไม่เสถียรสลายตัวและปล่อยรังสีออกมาเอง",
     ("การที่อะตอมรับอิเล็กตรอนเพิ่ม", "การเผาไหม้ของสารเคมี", "การสะท้อนของรังสีจากผิวโลหะ")),
)


def _decay(a: int, z: int, kind: str) -> tuple[int, int]:
    return {"แอลฟา": (a - 4, z - 2), "บีตา": (a, z + 1), "แกมมา": (a, z)}[kind]


@question_type(
    "phys.alpha_beta_gamma_foundation",
    display_name={"th": "สมบัติของรังสีแอลฟา บีตา และแกมมา"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RAYS,
)
class AlphaBetaGammaFoundation(QuestionType):
    """Charge, penetration and ionising power of each ray."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "แอลฟา: หนัก ประจุ +2 ทะลุน้อย แตกตัวไอออนมาก บีตา: อิเล็กตรอน ประจุ −1 แกมมา: คลื่นแม่เหล็กไฟฟ้า ไม่มีประจุ ทะลุมาก"
        if rng.random() < 0.4:
            # A source gives some of the three rays; a shield stops everything below its strength.
            emitted = [r for r in ("แอลฟา", "บีตา", "แกมมา") if rng.random() < 0.6] or ["แอลฟา", "แกมมา"]
            shield, stops = rng.choice((("กระดาษแผ่นหนึ่ง", 1), ("แผ่นอะลูมิเนียมหนา 5 mm", 2), ("แผ่นตะกั่วหนา 10 cm", 3)))
            order = {"แอลฟา": 1, "บีตา": 2, "แกมมา": 3}
            passed = [r for r in emitted if order[r] > stops]
            label = lambda rays: "ไม่มีรังสีผ่าน" if not rays else "รังสี" + " และ".join(rays)
            pool = {label(x) for x in (["แอลฟา"], ["บีตา"], ["แกมมา"], ["บีตา", "แกมมา"], ["แอลฟา", "บีตา", "แกมมา"], [])}
            pool.discard(label(passed))
            return _labelled(
                stem=f"ต้นกำเนิดรังสีปล่อยรังสี{' '.join(emitted)} นำ{shield} มากั้น รังสีใดผ่านไปได้ (ความเข้มลดลงมากถือว่าไม่ผ่าน)",
                correct=label(passed), wrongs=tuple(sorted(pool)), topic=TOPIC_RAYS, hint=hint)
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(RAY_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_RAYS, hint=hint)
        ray, what = rng.choice(RAY_PROPERTIES)
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดอธิบาย{ray}ได้ถูกต้อง", correct=what,
                             wrongs=tuple(w for r, w in RAY_PROPERTIES if r != ray) + ("คือโปรตอนอิสระ มีประจุ +1 ทะลุได้มากที่สุด",),
                             topic=TOPIC_RAYS, hint=hint)
        return _labelled(stem=f"รังสีใด{what}", correct=ray,
                         wrongs=tuple(r for r, _ in RAY_PROPERTIES if r != ray) + ("รังสีเอกซ์",), topic=TOPIC_RAYS, hint=hint)


@question_type(
    "phys.alpha_beta_gamma_fluency",
    display_name={"th": "เลขมวลและเลขอะตอมของนิวเคลียสหลังการสลาย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RAYS,
)
class AlphaBetaGammaFluency(QuestionType):
    """Alpha takes 4 and 2; beta adds a proton; gamma changes neither."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        z = rng.randint(20, 94)
        a = 2 * z + rng.randint(0, 50)
        kind = rng.choice(("แอลฟา", "บีตา", "แกมมา"))
        na, nz = _decay(a, z, kind)
        label = lambda aa, zz: f"เลขมวล {aa} เลขอะตอม {zz}"
        wrongs = {label(a - 4, z + 2), label(a, z - 1), label(a - 2, z - 4), label(a, z), label(a - 4, z - 2), label(a, z + 1)}
        wrongs.discard(label(na, nz))
        return _labelled(
            stem=f"นิวเคลียสที่มีเลขมวล {a} และเลขอะตอม {z} สลายให้รังสี{kind} นิวเคลียสใหม่มีเลขมวลและเลขอะตอมเท่าใด",
            correct=label(na, nz), wrongs=tuple(sorted(wrongs)), topic=TOPIC_RAYS,
            hint="แอลฟา: A − 4, Z − 2   บีตา: A เท่าเดิม, Z + 1   แกมมา: ไม่เปลี่ยน")


@question_type(
    "phys.alpha_beta_gamma_application",
    display_name={"th": "จำนวนการสลายแอลฟาและบีตาในอนุกรมการสลาย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RAYS,
)
class AlphaBetaGammaApplication(QuestionType):
    """From the change in A and Z, count the alphas first and then the betas."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        alphas = rng.randint(1, 8)
        betas = rng.randint(1, 6)
        z = rng.randint(82, 94)
        a = 2 * z + rng.randint(40, 60)
        fa, fz = a - 4 * alphas, z - 2 * alphas + betas
        ask_alpha = rng.random() < 0.5
        return numeric(
            stem=(f"นิวเคลียสเลขมวล {a} เลขอะตอม {z} สลายต่อเนื่องจนได้นิวเคลียสเลขมวล {fa} เลขอะตอม {fz} "
                  f"โดยปล่อยเฉพาะรังสีแอลฟาและบีตา ปล่อยรังสี{'แอลฟา' if ask_alpha else 'บีตา'}กี่ครั้ง"),
            answer=alphas if ask_alpha else betas, wrongs=[betas if ask_alpha else alphas, a - fa, abs(z - fz) + 1],
            unit="ครั้ง", topic=TOPIC_RAYS,
            hint="เลขมวลลดเฉพาะจากแอลฟา: จำนวนแอลฟา = ΔA/4 แล้วจำนวนบีตา = 2 × จำนวนแอลฟา − (Z เดิม − Z ใหม่)")
