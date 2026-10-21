"""Generators for reviewed POSN camp-selection chemistry questions (2562)."""

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2562_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24,
    q25, q26, q27, q28, q29, q30,
)

LEVEL = {"th": "โอลิมปิก (สอวน.)"}
SHEET_ID = "posn2562_chemistry"
SHEET = "สอวน. ค่าย 1 เคมี (2562)"


def _question(number, stem, choices, answer, topic, hint, mistakes):
    assert len(choices) == 4 and len(set(choices)) == 4
    assert len(mistakes) == 4
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(choices[answer])],
        distractors=fixed(*(
            [text(named(f"chem.posn2562_q{number:02d}_{mistakes[i]}", choice))]
            for i, choice in enumerate(choices) if i != answer
        )),
        topic=topic, hint=[text(hint)],
    )


class _Base(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET


@question_type("chem.posn2562_q01", display_name={"th": "เปรียบเทียบอนุภาคในไอออน"},
               level=LEVEL, subject="เคมี", topic="ไอโซโทปและไอออน")
class ParticleCounts(_Base):
    def build(self, rng, **params):
        v = rng.choice((q01.PARAMS, *q01.VARIANTS))
        choices = ("จำนวนนิวตรอนต่างกัน 4", "ไอออนแรกมีโปรตอนมากกว่า",
                   "อะตอมที่สองมีอิเล็กตรอนมากกว่าไอออนแรก 8",
                   "โปรตอน นิวตรอน และอิเล็กตรอนเท่ากันทั้งหมด")
        return _question(1, f"ไอออน X ประจุ +{v['charge']} มีเลขมวล {v['a']} "
                         f"เลขอะตอม {v['z']}; อะตอม Y มีเลขมวล {v['b']} "
                         f"เลขอะตอม {v['other_z']} ข้อความใดถูกต้อง",
                         choices, q01.solve(**v), "ไอโซโทปและไอออน",
                         "โปรตอน = Z, นิวตรอน = A−Z, อิเล็กตรอน = Z−ประจุ",
                         ("miscounted_neutrons", "reversed_protons", "correct",
                          "ignored_charge"))


@question_type("chem.posn2562_q02", display_name={"th": "เปรียบเทียบพลังงานโฟตอน"},
               level=LEVEL, subject="เคมี", topic="พลังงานและความยาวคลื่นของโฟตอน")
class PhotonEnergy(_Base):
    def build(self, rng, **params):
        v = rng.choice((q02.PARAMS, *q02.VARIANTS))
        choices = (f"ความถี่ {v['frequency']:.1e} Hz",
                   f"พลังงาน {v['energy']:.1e} J",
                   f"ความยาวคลื่น {v['long_nm']} nm",
                   f"ความยาวคลื่น {v['short_nm']} nm")
        return _question(2, "โฟตอนข้อใดมีพลังงานมากที่สุด", choices,
                         q02.solve(**v), "พลังงานและความยาวคลื่นของโฟตอน",
                         "แปลงทุกตัวเลือกเป็นพลังงานด้วย E = hν = hc/λ",
                         ("equated_frequency_with_energy", "ignored_units",
                          "chose_longer_wavelength", "correct"))


@question_type("chem.posn2562_q03", display_name={"th": "ความยาวคลื่นของการเปลี่ยนระดับ"},
               level=LEVEL, subject="เคมี", topic="ระดับพลังงานอิเล็กตรอน")
class AdjacentTransition(_Base):
    def build(self, rng, **params):
        v = rng.choice((q03.PARAMS, *q03.VARIANTS))
        n, wave = v['lower'], v['wavelength_nm']
        choices = (f"สั้นกว่า {wave} nm", f"ยาวกว่า {wave} nm",
                   f"เท่ากับ {wave} nm", f"เท่ากับ {wave} nm แต่เพิ่มจำนวนโฟตอน")
        return _question(3, f"อะตอมแบบไฮโดรเจนใช้แสง {wave} nm "
                         f"กระตุ้นจาก n={n} ไป n={n+1} หากกระตุ้นจาก "
                         f"n={n-1} ไป n={n} ต้องใช้ความยาวคลื่นแบบใด",
                         choices, q03.solve(**v), "ระดับพลังงานอิเล็กตรอน",
                         "ช่วงพลังงานของระดับต่ำกว่ากว้างกว่า; E = hc/λ",
                         ("correct", "reversed_level_gap", "equal_gap",
                          "confused_photon_count_with_energy"))


@question_type("chem.posn2562_q04", display_name={"th": "ลำดับพลังงานออร์บิทัล"},
               level=LEVEL, subject="เคมี", topic="ออร์บิทัลและการจัดอิเล็กตรอน")
class OrbitalEnergy(_Base):
    def build(self, rng, **params):
        v = rng.choice((q04.PARAMS, *q04.VARIANTS))
        choices = ("H: 2p มีพลังงานสูงกว่า 2s",
                   f"Z={v['multielectron_z']}: 3p มีพลังงานสูงกว่า 3s",
                   f"Z={v['metal_z']}: 3d มีพลังงานสูงกว่า 4p",
                   f"Z={v['halogen_z']}: 3d มีพลังงานสูงกว่า 4p")
        return _question(4, "ข้อความใดถูกต้องเกี่ยวกับพลังงานออร์บิทัล",
                         choices, q04.solve(**v), "ออร์บิทัลและการจัดอิเล็กตรอน",
                         "H มีออร์บิทัล n เดียวกันเสมอพลังงาน; หลายอิเล็กตรอน 3s < 3p",
                         ("ignored_hydrogen_degeneracy", "correct",
                          "reversed_3d_4p_metal", "reversed_3d_4p_halogen"))


@question_type("chem.posn2562_q05", display_name={"th": "การจัดอิเล็กตรอนของโลหะแทรนซิชัน"},
               level=LEVEL, subject="เคมี", topic="ออร์บิทัลและการจัดอิเล็กตรอน")
class TransitionConfiguration(_Base):
    def build(self, rng, **params):
        v = rng.choice((q05.PARAMS, *q05.VARIANTS))
        z = v['z']
        choices = (f"Z={z} อยู่หมู่เดียวกับ Z={v['comparison_z']}",
                   f"อะตอม Z={z} มีอิเล็กตรอน 3d จำนวน {z-20} ตัว",
                   f"อะตอม Z={z} มีอิเล็กตรอนเฉพาะระดับ n≤3",
                   "เมื่อเป็นไอออน 2+ จำนวนอิเล็กตรอน 3d ลดลง")
        return _question(5, f"ธาตุเลขอะตอม {z} มีข้อใดถูกต้อง", choices,
                         q05.solve(**v), "ออร์บิทัลและการจัดอิเล็กตรอน",
                         "เขียน [Ar] 3dⁿ4s² แล้วดึง 4s ออกก่อนเมื่อเกิดไอออน",
                         ("confused_transition_groups", "correct",
                          "omitted_4s", "removed_3d_before_4s"))


@question_type("chem.posn2562_q06", display_name={"th": "ออร์บิทัลครึ่งเต็ม"},
               level=LEVEL, subject="เคมี", topic="ออร์บิทัลและการจัดอิเล็กตรอน")
class HalfFilledSubshells(_Base):
    def build(self, rng, **params):
        v = rng.choice((q06.PARAMS, *q06.VARIANTS))
        a, p, m, f = (v[k] for k in ('alkali', 'pnictogen', 'manganese', 'iron'))
        choices = (f"Z={a} และ Z={p}", f"Z={a} และ Z={f}",
                   f"Z={p} และ Z={m}", f"Z={m} และ Z={f}")
        return _question(6, "คู่ใดมีอิเล็กตรอนใน p หรือ d ระดับสูงสุด "
                         "เพียงครึ่งหนึ่งของความจุทั้งสองธาตุ", choices,
                         q06.solve(**v), "ออร์บิทัลและการจัดอิเล็กตรอน",
                         "p ครึ่งเต็มคือ p³; d ครึ่งเต็มคือ d⁵",
                         ("mistook_s1_for_half_p", "mistook_d6_for_half_d",
                          "correct", "mistook_d6_for_half_d"))


@question_type("chem.posn2562_q07", display_name={"th": "แนวโน้มการรับอิเล็กตรอน"},
               level=LEVEL, subject="เคมี", topic="สัมพรรคภาพอิเล็กตรอน")
class ElectronAffinity(_Base):
    def build(self, rng, **params):
        v = rng.choice((q07.PARAMS, *q07.VARIANTS))
        configs = {12: "[Ne] 3s²", 13: "[Ne] 3s²3p¹",
                   14: "[Ne] 3s²3p²", 15: "[Ne] 3s²3p³"}
        choices = tuple(configs[z] for z in v['options'])
        mistakes = tuple("correct" if z == 14 else
                         "assumed_half_filled_p3_best" if z == 15 else
                         "assumed_group13_best" if z == 13 else
                         "assumed_filled_3s_best" for z in v['options'])
        return _question(7, "อะตอมใดรับอิเล็กตรอนได้ดีที่สุดในกลุ่มนี้",
                         choices, q07.solve(**v), "สัมพรรคภาพอิเล็กตรอน",
                         "เปรียบเทียบสัมพรรคภาพอิเล็กตรอน; p³ ครึ่งเต็มต้านการเพิ่ม",
                         mistakes)


@question_type("chem.posn2562_q08", display_name={"th": "อนุมานสูตรออกไซด์จาก IE"},
               level=LEVEL, subject="เคมี", topic="พลังงานไอออไนเซชัน")
class IonizationJump(_Base):
    def build(self, rng, **params):
        v = rng.choice((q08.PARAMS, *q08.VARIANTS))
        ies = ', '.join(str(n) for n in v['ies'])
        choices = ("ธาตุ X ไม่นำไฟฟ้า", "คลอไรด์ของ X เป็นแก๊สที่อุณหภูมิห้อง",
                   "ออกไซด์ของ X มีสัดส่วน X:O เท่ากับ 1:1",
                   "X มีเลขออกซิเดชันลบในสารธรรมชาติ")
        return _question(8, f"IE₁–IE₆ ของ X (kJ/mol) คือ {ies} ข้อใดถูกต้อง",
                         choices, q08.solve(**v), "พลังงานไอออไนเซชัน",
                         "ดูจุดที่ IE กระโดดมาก เพื่อหาเวเลนซ์อิเล็กตรอน",
                         ("mistook_metal_for_nonmetal", "assumed_ionic_halide_gas",
                          "correct", "assigned_negative_metal_oxidation"))


@question_type("chem.posn2562_q09", display_name={"th": "สมบัติออกไซด์ของอโลหะ"},
               level=LEVEL, subject="เคมี", topic="ออกไซด์กรดและออกไซด์เบส")
class AcidicTrioxide(_Base):
    def build(self, rng, **params):
        v = rng.choice((q09.PARAMS, *q09.VARIANTS))
        x, m = v['nonmetal'], v['metal']
        choices = (f"ธาตุ {x} อยู่ในหมู่ 13 ของตารางธาตุ",
                   f"เกลือโซเดียมจาก {x}O₃ มีสูตร Na{x}O₄",
                   f"คลอไรด์จาก {m}O กับ HCl มีสูตร {m}Cl",
                   f"สารละลาย {x}O₃ ในน้ำมีสมบัติเป็นกรด")
        return _question(9, f"ออกไซด์ {x}O₃ ทำปฏิกิริยากับเบส และ {m}O "
                         "เป็นสารไอออนิก ข้อใดถูกต้อง", choices,
                         q09.solve(**v), "ออกไซด์กรดและออกไซด์เบส",
                         "อโลหะออกไซด์ที่ให้กรดทำให้น้ำเป็นกรด; ดุลประจุของเกลือ",
                         ("confused_group16_with13", "missed_second_sodium",
                          "missed_second_chloride", "correct"))


@question_type("chem.posn2562_q10", display_name={"th": "คลอไรด์ของธาตุหมู่ 13"},
               level=LEVEL, subject="เคมี", topic="พันธะโคเวเลนต์และไฮโดรลิซิส")
class Group13Chloride(_Base):
    def build(self, rng, **params):
        v = rng.choice((q10.PARAMS, *q10.VARIANTS))
        symbol = {5: "B", 13: "Al", 31: "Ga"}[v['z']]
        base = (f"สูตรคือ {symbol}Cl₂", "มีพันธะโคเวเลนต์",
                "เป็นของเหลวไม่ละลายน้ำที่อุณหภูมิห้อง",
                "เติมน้ำแล้วสารละลายเป็นกลาง")
        choices = tuple(base[i] for i in v['order'])
        errors = tuple(("assumed_dichloride", "correct", "assumed_inert_liquid",
                        "ignored_hydrolysis")[i] for i in v['order'])
        return _question(10, f"ธาตุ X มีเลขอะตอม {v['z']} คลอไรด์ของ X "
                         "มีสมบัติใดถูกต้อง", choices, q10.solve(**v),
                         "พันธะโคเวเลนต์และไฮโดรลิซิส",
                         "หมู่ 13 ให้ XCl₃ และไฮโดรลิซิสในน้ำ", errors)


@question_type("chem.posn2562_q11", display_name={"th": "โลหะที่ให้น้ำเกิดไฮโดรเจน"},
               level=LEVEL, subject="เคมี", topic="ปฏิกิริยาของโลหะกับน้ำ")
class AlkaliMetalWater(_Base):
    def build(self, rng, **params):
        v = rng.choice((q11.PARAMS, *q11.VARIANTS))
        choices = tuple(v[k] for k in ('alkali', 'second', 'third', 'fourth'))
        errors = tuple("correct" if symbol == v['alkali'] else
                       "assumed_beryllium_reacts_cold" if symbol == "Be" else
                       "assumed_zinc_reacts_cold" if symbol == "Zn" else
                       "assumed_ammonia_makes_hydrogen" for symbol in choices)
        return _question(11, "สารใดทำปฏิกิริยากับน้ำที่อุณหภูมิห้อง "
                         "และความดันบรรยากาศให้แก๊ส H₂", choices,
                         q11.solve(**v), "ปฏิกิริยาของโลหะกับน้ำ",
                         "โลหะหมู่ 1 ทำปฏิกิริยากับน้ำเย็น; Zn ต้องใช้ไอน้ำ",
                         errors)


@question_type("chem.posn2562_q12", display_name={"th": "ลำดับความว่องไวของแฮโลเจน"},
               level=LEVEL, subject="เคมี", topic="ปฏิกิริยาแทนที่ของแฮโลเจน")
class HalogenDisplacement(_Base):
    def build(self, rng, **params):
        v = rng.choice((q12.PARAMS, *q12.VARIANTS))
        choices = ("I และ II", "II และ III", "I และ III", "I เท่านั้น")
        return _question(12, f"พิจารณา I: Br₂ + {v['alkali']} → bromide; "
                         f"II: I₂ + {v['bromide']} → iodide + Br₂; "
                         f"III: Br₂ + {v['chloride']} → bromide + Cl₂ "
                         "ปฏิกิริยาใดเกิดได้เอง", choices, q12.solve(**v),
                         "ปฏิกิริยาแทนที่ของแฮโลเจน",
                         "กำลังออกซิไดซ์ Cl₂ > Br₂ > I₂",
                         ("assumed_iodine_displaces_bromine",
                          "reversed_halogen_strength", "assumed_bromine_displaces_chlorine",
                          "correct"))


@question_type("chem.posn2562_q13", display_name={"th": 'ไฮโดรเจนกับสมบัติคล้ายแฮโลเจน'},
               level=LEVEL, subject="เคมี", topic='สมบัติของไฮโดรเจน')
class ReviewedQuestion13(_Base):
    def build(self, rng, **params):
        v = rng.choice((q13.PARAMS, *q13.VARIANTS))
        choices = ('I, III และ IV', 'II, III และ IV', 'I และ III เท่านั้น', 'II และ IV เท่านั้น')
        mistakes = ('includes_positive_hydrogen', 'overstates_electron_affinity', 'correct', 'misses_diatomic_hydrogen')
        order = v["order"]
        return _question(13, 'ข้อใดแสดงสมบัติของไฮโดรเจนคล้ายแฮโลเจน: I เป็น H₂ พันธะเดี่ยว; II รับอิเล็กตรอนแล้วคายพลังงานมาก; III ใน NaH มีเลขออกซิเดชัน −1; IV ใน HCl มีเลขออกซิเดชัน +1'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q13.solve(**v),
                         'สมบัติของไฮโดรเจน', 'เปรียบเทียบ H₂ กับ X₂ และ H⁻ ในไฮไดรด์กับ X⁻',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q14", display_name={"th": 'อิเล็กตรอนเดี่ยวของทองแดง'},
               level=LEVEL, subject="เคมี", topic='การจัดอิเล็กตรอนของทองแดง')
class ReviewedQuestion14(_Base):
    def build(self, rng, **params):
        v = rng.choice((q14.PARAMS, *q14.VARIANTS))
        choices = ('1, 0', '1, 1', '0, 0', '1, 3')
        mistakes = ('assumes_cu2_d10', 'correct', 'misses_cu_4s', 'overcounts_cu2_unpaired')
        order = v["order"]
        return _question(14, 'โลหะ X ให้ X₂O และ XO; XO ละลายใน HCl ให้สารละลายสีฟ้า จำนวนอิเล็กตรอนเดี่ยวของ X และ X²⁺ ตามลำดับคือข้อใด'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q14.solve(**v),
                         'การจัดอิเล็กตรอนของทองแดง', 'X คือ Cu; เขียน [Ar]3d¹⁰4s¹ แล้วดึง 4s ก่อน 3d',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q15", display_name={"th": 'พันธะในสารเชิงซ้อนโคบอลต์'},
               level=LEVEL, subject="เคมี", topic='สารเชิงซ้อนและพันธะโคออร์ดิเนต')
class ReviewedQuestion15(_Base):
    def build(self, rng, **params):
        v = rng.choice((q15.PARAMS, *q15.VARIANTS))
        choices = ('ไอออนเชิงซ้อนทำให้สารประกอบมีสี', 'Co มีเลขออกซิเดชัน +3', 'ไอออนเชิงซ้อนมีประจุ +2', 'Co เกิดพันธะไอออนิกกับ N และ Br')
        mistakes = ('assumes_colorless_complex', 'misassigns_cobalt_oxidation', 'misassigns_complex_charge', 'correct')
        order = v["order"]
        return _question(15, 'สำหรับ [Co(NH₃)₅Br]SO₄ ข้อใดผิด'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q15.solve(**v),
                         'สารเชิงซ้อนและพันธะโคออร์ดิเนต', 'SO₄²⁻ กำหนดประจุไอออนเชิงซ้อน; NH₃ เป็นกลางและ Br⁻ เป็นลิแกนด์',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q16", display_name={"th": 'ระบุปฏิกิริยาฟิวชัน'},
               level=LEVEL, subject="เคมี", topic='ปฏิกิริยานิวเคลียร์ฟิวชัน')
class ReviewedQuestion16(_Base):
    def build(self, rng, **params):
        v = rng.choice((q16.PARAMS, *q16.VARIANTS))
        choices = ('²₁H + ²₁H → ³₂He + ¹₀n', '²⁷₁₃Al + ⁴₂He → ³⁰₁₄Si + ¹₁H', '²¹⁴₈₃Bi → ²¹⁴₈₄Po + ⁰₋₁e', '²³⁵₉₂U + ¹₀n → ¹⁴⁴₅₆Ba + ⁸⁹₃₆Kr + 3¹₀n')
        mistakes = ('correct', 'confuses_transmutation_with_fusion', 'confuses_beta_decay_with_fusion', 'confuses_fission_with_fusion')
        order = v["order"]
        return _question(16, 'สมการใดเป็นฟิวชัน'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q16.solve(**v),
                         'ปฏิกิริยานิวเคลียร์ฟิวชัน', 'ฟิวชันรวมสองนิวเคลียสเบาเป็นนิวเคลียสที่หนักขึ้น',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q17", display_name={"th": 'อนุภาคในสมการนิวเคลียร์'},
               level=LEVEL, subject="เคมี", topic='อนุรักษ์เลขมวลและเลขอะตอม')
class ReviewedQuestion17(_Base):
    def build(self, rng, **params):
        v = rng.choice((q17.PARAMS, *q17.VARIANTS))
        choices = ('อนุภาคมวล 2 ประจุ +1; โปรตอน; นิวตรอน', 'p; n; β⁻', 'อนุภาคมวล 2 ประจุ 0; นิวตรอน; โปรตอน', 'นิวตรอน; γ; β⁻')
        mistakes = ('uses_charged_capture', 'confuses_capture_with_proton', 'violates_mass_conservation', 'correct')
        order = v["order"]
        return _question(17, '⁽ᴬ⁾₄₅Rh + a → ⁽ᴬ⁺¹⁾₄₅Rh + b; ⁽ᴬ⁺¹⁾₄₅Rh → ⁽ᴬ⁺¹⁾₄₆Pd + c. a, b, c คือชุดใด'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q17.solve(**v),
                         'อนุรักษ์เลขมวลและเลขอะตอม', 'ดุล A และ Z ในสมการทั้งสองแยกกัน',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q18", display_name={"th": 'การสลายแอลฟาของโบห์เรียม'},
               level=LEVEL, subject="เคมี", topic='การสลายแอลฟาและหมู่ธาตุ')
class ReviewedQuestion18(_Base):
    def build(self, rng, **params):
        v = rng.choice((q18.PARAMS, *q18.VARIANTS))
        choices = ('I และ II', 'II และ III', 'I และ III', 'II เท่านั้น')
        mistakes = ('forgets_alpha_neutrons', 'correct', 'misplaces_bh_group', 'dismisses_possible_oxide')
        order = v["order"]
        return _question(18, '⁽ᴬ⁾₁₀₇Bh สลายแอลฟา: I ลูกมี 105 โปรตอนและ A−107 นิวตรอน; II Bh อยู่หมู่ 7; III BhO₂ เป็นออกไซด์ +4 ที่เป็นไปได้ตามแนวโน้มหมู่ ข้อใดถูก'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q18.solve(**v),
                         'การสลายแอลฟาและหมู่ธาตุ', 'แอลฟาทำให้ A ลด 4 และ Z ลด 2; ตรวจเลขออกซิเดชันใน BhO₂',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q19", display_name={"th": 'สมบัติของแอนติโมนี'},
               level=LEVEL, subject="เคมี", topic='สมบัติธาตุหมู่ 15')
class ReviewedQuestion19(_Base):
    def build(self, rng, **params):
        v = rng.choice((q19.PARAMS, *q19.VARIANTS))
        choices = ('จัดเป็นโลหะที่นำไฟฟ้าได้ไม่ดีนัก', 'ไม่ทำปฏิกิริยากับน้ำเย็นแบบโลหะหมู่ 1', 'มีค่าอิเล็กโทรเนกาติวิตีต่ำกว่าฟอสฟอรัส', 'เกิดเลขออกซิเดชันสูงสุด +5 ได้')
        mistakes = ('correct', 'assumes_alkali_water_reactivity', 'reverses_p_sb_electronegativity', 'misses_sb_plus_five')
        order = v["order"]
        return _question(19, 'ธาตุเลขอะตอม 51 มีข้อความใดผิด'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q19.solve(**v),
                         'สมบัติธาตุหมู่ 15', 'ธาตุ 51 คือ Sb อยู่ตามแนวกึ่งโลหะในหมู่ 15',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q20", display_name={"th": 'ข้อเท็จจริงเกี่ยวกับออกซิเจน'},
               level=LEVEL, subject="เคมี", topic='ออกซิเจนและเปอร์ออกไซด์')
class ReviewedQuestion20(_Base):
    def build(self, rng, **params):
        v = rng.choice((q20.PARAMS, *q20.VARIANTS))
        choices = ('I และ II', 'III และ IV', 'I และ III', 'II และ IV')
        mistakes = ('correct', 'rejects_peroxide_disinfection', 'accepts_ground_ozone', 'assumes_heavy_superoxide')
        order = v["order"]
        return _question(20, 'ข้อใดผิด: I โอโซนระดับพื้นดินมากขึ้นดีต่อสุขภาพ; II ซุปเปอร์ออกไซด์มักเกิดกับโลหะหนักและแทรนซิชัน; III H₂O₂ ใช้ฆ่าเชื้อ; IV ในออกโซแอนไอออนทั่วไปที่ไม่มีพันธะ O–F หรือ O–O, O มีเลขออกซิเดชัน −2'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q20.solve(**v),
                         'ออกซิเจนและเปอร์ออกไซด์', 'โอโซนระดับพื้นดินระคายทางเดินหายใจ; ซุปเปอร์ออกไซด์เสถียรในโลหะหมู่ 1 ขนาดใหญ่',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q21", display_name={"th": 'เรโซแนนซ์และพันธะสาม'},
               level=LEVEL, subject="เคมี", topic='เรโซแนนซ์และชนิดพันธะ')
class ReviewedQuestion21(_Base):
    def build(self, rng, **params):
        v = rng.choice((q21.PARAMS, *q21.VARIANTS))
        choices = ('I และ II', 'I และ III', 'II และ III', 'I, II และ III')
        mistakes = ('misses_ionic_salt_bond', 'correct', 'misses_nitrate_resonance', 'calls_salt_all_covalent')
        order = v["order"]
        return _question(21, 'พิจารณา I NO₃⁻ มีเรโซแนนซ์; II NH₄Br มีแต่พันธะโคเวเลนต์; III C₂H₂ และ HCN ต่างมีพันธะสามใช้อิเล็กตรอนร่วมกัน 6 ตัว ข้อใดถูก'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q21.solve(**v),
                         'เรโซแนนซ์และชนิดพันธะ', 'พิจารณาพันธะภายในไอออนและแรงยึดระหว่าง NH₄⁺ กับ Br⁻ แยกกัน',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q22", display_name={"th": 'รูปร่างไอออนตาม VSEPR'},
               level=LEVEL, subject="เคมี", topic='รูปร่างโมเลกุลตาม VSEPR')
class ReviewedQuestion22(_Base):
    def build(self, rng, **params):
        v = rng.choice((q22.PARAMS, *q22.VARIANTS))
        choices = ('I เท่านั้น', 'II เท่านั้น', 'III เท่านั้น', 'II และ III')
        mistakes = ('assigns_carbon_lone_pair', 'equates_planar_pyramidal', 'correct', 'accepts_shape_equality')
        order = v["order"]
        return _question(22, 'สำหรับ CO₃²⁻, NO₂⁻, SO₃²⁻, ClO₃⁻: I ทุกอะตอมกลางมีคู่โดดเดี่ยว; II CO₃²⁻, SO₃²⁻, ClO₃⁻ รูปร่างเหมือนกัน; III NO₂⁻ และ NH₂⁻ ต่างมุมงอ แต่มุม NO₂⁻ มากกว่า ข้อใดถูก'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q22.solve(**v),
                         'รูปร่างโมเลกุลตาม VSEPR', 'นับบริเวณอิเล็กตรอนของอะตอมกลาง; CO₃²⁻ เป็น AX₃',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q23", display_name={"th": 'การยกเว้นกฎออกเตต'},
               level=LEVEL, subject="เคมี", topic='กฎออกเตตและโครงสร้างลิวอิส')
class ReviewedQuestion23(_Base):
    def build(self, rng, **params):
        v = rng.choice((q23.PARAMS, *q23.VARIANTS))
        choices = ('BF₃, SF₆, XeF₂', 'CO, NO, N₂O', 'NO₂⁻, O₃, I₃⁻', 'N₂O₃, N₂O₄, N₂H₄')
        mistakes = ('correct', 'treats_co_as_non_octet', 'treats_nitrite_as_non_octet', 'treats_hydrazine_as_non_octet')
        order = v["order"]
        return _question(23, 'ชุดใดมีทุกโมเลกุลหรือไอออนที่ไม่เป็นไปตามกฎออกเตต'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q23.solve(**v),
                         'กฎออกเตตและโครงสร้างลิวอิส', 'นับอิเล็กตรอนรอบ B, S และ Xe แล้วหาตัวอย่างออกเตตในชุดอื่น',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q24", display_name={"th": 'ชื่อสารและรูปร่าง VSEPR'},
               level=LEVEL, subject="เคมี", topic='การเรียกชื่อสารและรูปร่างโมเลกุล')
class ReviewedQuestion24(_Base):
    def build(self, rng, **params):
        v = rng.choice((q24.PARAMS, *q24.VARIANTS))
        choices = ('I เท่านั้น', 'II เท่านั้น', 'III เท่านั้น', 'I และ II')
        mistakes = ('correct', 'ignores_oxygen_lone_pairs', 'confuses_si_with_s', 'accepts_linear_of2')
        order = v["order"]
        return _question(24, 'ข้อใดระบุทั้งชื่อและรูปร่างถูก: I Cl₂O ไดคลอรีนมอนอกไซด์ มุมงอ; II OF₂ ออกซิเจนไดฟลูออไรด์ เส้นตรง; III SiF₄ ซัลเฟอร์เตตระฟลูออไรด์ ทรงสี่หน้าบิดเบี้ยว'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q24.solve(**v),
                         'การเรียกชื่อสารและรูปร่างโมเลกุล', 'Cl₂O และ OF₂ มี O เป็น AX₂E₂; SiF₄ มี Si เป็น AX₄',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q25", display_name={"th": 'เรโซแนนซ์ของไซยาเนต'},
               level=LEVEL, subject="เคมี", topic='เรโซแนนซ์และกฎออกเตต')
class ReviewedQuestion25(_Base):
    def build(self, rng, **params):
        v = rng.choice((q25.PARAMS, *q25.VARIANTS))
        choices = ('N≡C=O', 'N≡C–O', 'N=C=O', 'N–C≡O')
        mistakes = ('correct', 'accepts_valid_nitrile_form', 'rejects_valid_double_form', 'rejects_valid_oxide_form')
        order = v["order"]
        return _question(25, 'โครงสร้างพันธะของ NCO⁻ แบบใดไม่เป็นเรโซแนนซ์ที่เป็นไปได้ (พิจารณาออกเตตของ C)'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q25.solve(**v),
                         'เรโซแนนซ์และกฎออกเตต', 'C คาบ 2 รับอิเล็กตรอนรอบตัวได้ไม่เกิน 8',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q26", display_name={"th": 'รูปร่างเหมือนแต่ขั้วต่าง'},
               level=LEVEL, subject="เคมี", topic='รูปร่างและสภาพขั้วโมเลกุล')
class ReviewedQuestion26(_Base):
    def build(self, rng, **params):
        v = rng.choice((q26.PARAMS, *q26.VARIANTS))
        choices = ('POCl₃ และ XeO₄', 'ClF₃ และ PCl₃', 'ClO₂ และ SO₂', 'SF₄ และ GeCl₄')
        mistakes = ('correct', 'equates_t_shape_pyramid', 'mistakes_both_polar_for_opposite', 'equates_seesaw_tetrahedral')
        order = v["order"]
        return _question(26, 'คู่ใดมีรูปร่างโมเลกุลเหมือนกัน แต่สภาพขั้วต่างกัน'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q26.solve(**v),
                         'รูปร่างและสภาพขั้วโมเลกุล', 'เทียบ VSEPR ก่อน แล้วพิจารณาการหักล้างเวกเตอร์ขั้ว',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q27", display_name={"th": 'ผลของคู่โดดเดี่ยวต่อ XeF4'},
               level=LEVEL, subject="เคมี", topic='รูปร่างโมเลกุลตาม VSEPR')
class ReviewedQuestion27(_Base):
    def build(self, rng, **params):
        v = rng.choice((q27.PARAMS, *q27.VARIANTS))
        choices = ('ทรงสี่หน้า → seesaw', 'สี่เหลี่ยมแบนราบ → seesaw', 'สี่เหลี่ยมแบนราบ → พีระมิดฐานสี่เหลี่ยม', 'seesaw → สี่เหลี่ยมแบนราบ')
        mistakes = ('mistakes_initial_xe_shape', 'correct', 'uses_six_domain_after_removal', 'reverses_shape_change')
        order = v["order"]
        return _question(27, 'ถ้าดึงคู่อิเล็กตรอนโดดเดี่ยวหนึ่งคู่ออกจาก Xe ของ XeF₄ แต่ยังมีพันธะ Xe–F สี่พันธะ รูปร่างเดิมและใหม่คือข้อใด'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q27.solve(**v),
                         'รูปร่างโมเลกุลตาม VSEPR', 'AX₄E₂ มี 6 โดเมน; หลังลดคู่โดดเดี่ยวเป็น AX₄E มี 5 โดเมน',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q28", display_name={"th": 'มุมพันธะและรูปร่าง BrF3'},
               level=LEVEL, subject="เคมี", topic='รูปร่างโมเลกุลตาม VSEPR')
class ReviewedQuestion28(_Base):
    def build(self, rng, **params):
        v = rng.choice((q28.PARAMS, *q28.VARIANTS))
        choices = ('I และ II', 'I และ III', 'II และ III', 'I, II และ III')
        mistakes = ('assumes_brf3_trigonal', 'misses_shape_difference', 'correct', 'assumes_all_angles_120')
        order = v["order"]
        return _question(28, 'สำหรับ SO₃, COCl₂, BrF₃: I ทั้งสามมีทุกมุม 120°; II COCl₂ กับ BrF₃ มีรูปร่างต่างกัน; III รอบ Br ใน BrF₃ มี 10 อิเล็กตรอน ข้อใดถูก'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q28.solve(**v),
                         'รูปร่างโมเลกุลตาม VSEPR', 'BrF₃ เป็น AX₃E₂ มีรูปร่าง T และ 5 โดเมน',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q29", display_name={"th": 'แรงยึดเหนี่ยวระหว่างโมเลกุล'},
               level=LEVEL, subject="เคมี", topic='พันธะไฮโดรเจนและแรงระหว่างโมเลกุล')
class ReviewedQuestion29(_Base):
    def build(self, rng, **params):
        v = rng.choice((q29.PARAMS, *q29.VARIANTS))
        choices = ('H₂S, H₂O และ CO₂ ในสถานะก๊าซ', 'PH₃, AsH₃, NH₃', 'CS₂, SO₂, COCl₂', 'CH₃OH, HNO₂, CH₃COOH')
        mistakes = ('treats_h2s_like_water', 'treats_ph3_like_ammonia', 'ignores_cs2_nonpolarity', 'correct')
        order = v["order"]
        return _question(29, 'ชุดใดมีแรงยึดเหนี่ยวระหว่างโมเลกุลชนิดเด่นเหมือนกันทุกสาร'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q29.solve(**v),
                         'พันธะไฮโดรเจนและแรงระหว่างโมเลกุล', 'การให้พันธะไฮโดรเจนต้องมี H ผูกกับ N, O หรือ F',
                         tuple(mistakes[i] for i in order))


@question_type("chem.posn2562_q30", display_name={"th": 'ความดันไอ จุดเดือด และการละลาย'},
               level=LEVEL, subject="เคมี", topic='แรงระหว่างโมเลกุลและสมบัติสาร')
class ReviewedQuestion30(_Base):
    def build(self, rng, **params):
        v = rng.choice((q30.PARAMS, *q30.VARIANTS))
        choices = ('I เท่านั้น', 'II เท่านั้น', 'III เท่านั้น', 'I และ II')
        mistakes = ('reverses_ccl4_water_vapor_pressure', 'correct', 'assumes_so2_insoluble', 'accepts_false_vapor_claim')
        order = v["order"]
        return _question(30, 'ข้อใดถูก: I ที่ 20 °C CCl₄ มีความดันไอต่ำกว่าน้ำ; II SF₄ มีจุดเดือดสูงกว่า SF₆; III SO₂ ไม่ละลายน้ำ'.replace("⁽ᴬ⁾", str(v["mass"]) if "mass" in v else "⁽ᴬ⁾").replace("⁽ᴬ⁺¹⁾", str(v["mass"] + 1) if "mass" in v else "⁽ᴬ⁺¹⁾"),
                         tuple(choices[i] for i in order), q30.solve(**v),
                         'แรงระหว่างโมเลกุลและสมบัติสาร', 'เทียบความดันไอที่อุณหภูมิเดียวกันและความมีขั้วของ SF₄ กับ SF₆',
                         tuple(mistakes[i] for i in order))
