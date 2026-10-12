"""อนุกรม

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem

PROVENANCE = Provenance("original")


@question_type("math.p_series",
               display_name={"th": "การลู่เข้าของอนุกรมพี (p-series)"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรม")
class PSeries(ChoiceType):
    def compose(self, rng: Random):
        p = rng.choice(["1/2", "1", "2", "3"])
        if p in ("2", "3"):
            return f"อนุกรม Σ 1/n^{p} ลู่เข้าหรือลู่ออก?", "ลู่เข้า (p > 1)", \
                ["ลู่ออก (p ≤ 1)"]
        return f"อนุกรม Σ 1/n^{p} ลู่เข้าหรือลู่ออก?", "ลู่ออก (p ≤ 1)", \
            ["ลู่เข้า (p > 1)"]


@question_type("math.series_convergence_tests",
               display_name={"th": "การทดสอบการลู่เข้าของอนุกรม"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรม")
class SeriesConvergenceTests(ConceptBankType):
    ITEMS = [
        Concept("Σ 1/n² ทดสอบด้วย Integral Test (∫₁^∞ 1/x² dx = 1) สรุปได้ว่าอย่างไร?",
                "ลู่เข้า", ("ลู่ออก", "ลู่เข้าสู่ 1", "สรุปไม่ได้")),
        Concept("เพื่อทดสอบ Σ 1/(n²+1) ด้วยการเปรียบเทียบ ควรเทียบกับอนุกรมใด?",
                "Σ 1/n² (ลู่เข้า)", ("Σ 1/n (ลู่ออก)", "Σ 1/n³ (ลู่เข้า)", "Σ 1/√n (ลู่ออก)")),
        Concept("อนุกรมสลับ Σ(−1)ⁿ·bₙ ลู่เข้าตามเงื่อนไขใด?",
                "bₙ ลดลงและ lim bₙ = 0",
                ("bₙ ลดลงและ lim bₙ ≠ 0", "bₙ เพิ่มขึ้นและ lim bₙ = ∞", "lim bₙ = 0 อย่างเดียวก็พอ")),
        Concept("Σ (−1)ⁿ/n เป็นการลู่เข้าแบบใด?", "ลู่เข้าแบบมีเงื่อนไข",
                ("ลู่เข้าสัมบูรณ์", "ลู่ออก", "ไม่ลู่เข้า")),
        Concept("ใช้ Ratio Test กับ Σ 1/n! ได้ค่า L เท่าใดและสรุปอย่างไร?",
                "L = 0 < 1 จึงลู่เข้า",
                ("L = 1 สรุปไม่ได้", "L = ∞ จึงลู่ออก", "L = 0 จึงลู่ออก")),
    ]


@question_type("math.power_series_radius",
               display_name={"th": "รัศมีการลู่เข้าของอนุกรมกำลัง"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรม")
class PowerSeriesRadius(WordProblem):
    def expr(self, rng: Random):
        r = rng.randint(2, 6)
        return MathDraw("", str(r),
                        prompt=f"รัศมีการลู่เข้าของ Σ x^n/{r}^n เท่ากับเท่าใด?",
                        distractors=["1", str(r * r), "0"])


@question_type("math.power_series_representation",
               display_name={"th": "การแทนฟังก์ชันด้วยอนุกรมกำลัง"},
               level={"th": "แคลคูลัส 2"}, topic="อนุกรม")
class PowerSeriesRepresentation(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"\frac{1}{1 - x}\ (|x| < 1)", r"\sum_{n=0}^{\infty} x^{n}",
            prompt="การกระจายเป็นอนุกรมกำลังคือข้อใด",
            distractors=[r"\sum_{n=0}^{\infty} (-1)^{n} x^{n}",
                         r"\sum_{n=0}^{\infty} \frac{x^{n}}{n!}",
                         r"\sum_{n=0}^{\infty} n x^{n}"])
