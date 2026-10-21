"""Generators for reviewed POSN camp-selection chemistry questions (2562)."""

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2562_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
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
