"""Reviewed waves of POSN camp-selection chemistry 2561."""

from fractions import Fraction

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2561_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24,
    q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36,
    q37, q38, q39, q40, q41, q42, q43, q44, q45,
)


LEVEL = {"th": "โอลิมปิก (สอวน.)"}
SHEET_ID = "posn2561_chemistry"
SHEET = "สอวน. ค่าย 1 เคมี (2561)"


@question_type(
    "chem.posn2561_q01", display_name={"th": "ไอออนที่มีอิเล็กตรอนเท่ากัน"},
    level=LEVEL, subject="เคมี", topic="ไอออนและจำนวนอิเล็กตรอน",
)
class IsoelectronicIons(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q01.PARAMS, *q01.VARIANTS))
        answer = q01.solve(**values)
        groups = ("A⁺, A⁻, D⁺", "E⁻, E⁺, G", "E⁻, A⁻, D⁺", "E⁻, G, A⁺")
        mistakes = (
            "chem.posn2561_confused_isotopes_with_electron_count",
            "chem.posn2561_ignored_opposite_ion_charges",
            "chem.posn2561_counted_nuclear_particles_as_electrons",
            "chem.posn2561_ignored_positive_ion_charge",
        )
        return GeneratedQuestion(
            stem=[text("ธาตุสมมติ A, D, E และ G มีเลขอะตอม "
                       f"{values['a']}, {values['d']}, {values['e']} และ {values['g']} "
                       "ตามลำดับ กลุ่มใดมีจำนวนอิเล็กตรอนเท่ากันทั้งสามอนุภาค")],
            correct=[text(groups[answer])],
            distractors=fixed(*( [text(named(mistakes[i], group))]
                                for i, group in enumerate(groups) if i != answer)),
            topic="ไอออนและจำนวนอิเล็กตรอน",
            hint=[text("จำนวนอิเล็กตรอน = เลขอะตอม − ประจุ โดยประจุลบเพิ่มอิเล็กตรอน")],
        )


@question_type(
    "chem.posn2561_q02", display_name={"th": "เลขอะตอมและเลขมวลของไอออน"},
    level=LEVEL, subject="เคมี", topic="ไอโซโทปและไอออน",
)
class IonAtomicAndMassNumbers(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q02.PARAMS, *q02.VARIANTS))
        atomic, mass = q02.solve(**values)
        electrons, neutrons, charge = (values[k] for k in
                                       ("ion_electrons", "neutrons", "charge"))
        fmt = lambda z, a: f"{z} และ {a}"
        return GeneratedQuestion(
            stem=[text(f"ไอออน X ประจุ +{charge} มี {electrons} อิเล็กตรอน "
                       f"และนิวเคลียสมี {neutrons} นิวตรอน "
                       "เลขอะตอมและเลขมวลของ X เป็นเท่าใดตามลำดับ")],
            correct=[text(fmt(atomic, mass))],
            distractors=fixed(
                [text(named("chem.posn2561_used_ion_electrons_as_protons",
                            fmt(electrons, electrons + neutrons)))],
                [text(named("chem.posn2561_used_neutrons_as_mass_number",
                            fmt(atomic, neutrons)))],
                [text(named("chem.posn2561_swapped_atomic_and_mass_numbers",
                            fmt(mass, atomic)))],
            ),
            topic="ไอโซโทปและไอออน",
            hint=[text("โปรตอน = อิเล็กตรอนในไอออนบวก + ประจุ; เลขมวล = โปรตอน + นิวตรอน")],
        )


@question_type(
    "chem.posn2561_q03", display_name={"th": "เปรียบเทียบพลังงานเส้นสเปกตรัม"},
    level=LEVEL, subject="เคมี", topic="พลังงานและความยาวคลื่นของโฟตอน",
)
class SpectralLineEnergyOrder(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q03.PARAMS, *q03.VARIANTS))
        assert q03.solve(**values) == 1
        return GeneratedQuestion(
            stem=[text("เส้นสเปกตรัมสี่เส้นมีความยาวคลื่น "
                       f"A={values['a_nm']} nm, B={values['b_nm']} nm, "
                       f"C={values['c_nm']} nm และ D={values['d_nm']} nm "
                       "ข้อความใดถูกต้อง")],
            correct=[text("พลังงานของ C มากกว่า B")],
            distractors=fixed(
                [text(named("chem.posn2561_treated_frequency_as_wavelength",
                            "ความถี่ของ A มากกว่า B"))],
                [text(named("chem.posn2561_treated_energy_as_wavelength",
                            "พลังงานของ A มากกว่า C"))],
                [text(named("chem.posn2561_shortest_wavelength_least_energy",
                            "พลังงานของ D น้อยที่สุด"))],
            ),
            topic="พลังงานและความยาวคลื่นของโฟตอน",
            hint=[text("E=hc/λ: ความยาวคลื่นสั้นกว่าให้โฟตอนพลังงานมากกว่า")],
        )


@question_type(
    "chem.posn2561_q04", display_name={"th": "ข้อสรุปจากธาตุต่างกันหกโปรตอน"},
    level=LEVEL, subject="เคมี", topic="ชั้นอิเล็กตรอนและคาบของธาตุ",
)
class PeriodTwoElementOffset(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q04.PARAMS, *q04.VARIANTS))
        answer = q04.solve(**values)
        assert answer == 1
        claims = (
            "ธาตุ X และ Z อยู่ในคาบเดียวกันเสมอ",
            "ธาตุ Z มีอิเล็กตรอนในชั้นที่สองมากกว่า 6 เสมอ",
            f"เลขมวลของ Z มากกว่า X เท่ากับ {values['offset']} เสมอ",
            f"เวเลนซ์อิเล็กตรอนของ Z มากกว่า X เท่ากับ {values['offset']} เสมอ",
        )
        mistakes = (
            "chem.posn2561_assumed_same_period_after_proton_offset",
            "",
            "chem.posn2561_confused_proton_and_nucleon_difference",
            "chem.posn2561_assumed_valence_tracks_atomic_offset",
        )
        return GeneratedQuestion(
            stem=[text(f"ธาตุ X มีเลขอะตอมตั้งแต่ {values['x_min']} ถึง "
                       f"{values['x_max']} (อยู่ในคาบที่ 2) และธาตุ Z มีโปรตอน"
                       f"มากกว่า X {values['offset']} ตัว ข้อความใดถูกต้องเสมอ")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[i], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="ชั้นอิเล็กตรอนและคาบของธาตุ",
            hint=[text("ตรวจ X ทุกธาตุในช่วง และแยกจำนวนโปรตอนออกจากจำนวนนิวตรอน")],
        )


_ELECTRON_CONFIGS = {
    6: "1s² 2s² 2p²", 8: "1s² 2s² 2p⁴", 9: "1s² 2s² 2p⁵",
    11: "1s² 2s² 2p⁶ 3s¹", 12: "1s² 2s² 2p⁶ 3s²",
    17: "1s² 2s² 2p⁶ 3s² 3p⁵",
    20: "1s² 2s² 2p⁶ 3s² 3p⁶ 4s²",
    35: "1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s² 4p⁵",
}


@question_type(
    "chem.posn2561_q05", display_name={"th": "อโลหะที่ไวต่อปฏิกิริยาที่สุด"},
    level=LEVEL, subject="เคมี", topic="การจัดอิเล็กตรอนและความไวต่อปฏิกิริยา",
)
class ReactiveNonmetalConfiguration(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q05.PARAMS, *q05.VARIANTS))
        answer = q05.solve(**values)
        wrongs = []
        for z in values["options"]:
            if z == answer:
                continue
            if z in (17, 35):
                mistake = "chem.posn2561_chose_lower_halogen_reactivity"
            elif z in (11, 12, 20):
                mistake = "chem.posn2561_chose_reactive_metal_as_nonmetal"
            else:
                mistake = "chem.posn2561_chose_nonhalogen_over_halogen"
            wrongs.append([text(named(mistake, _ELECTRON_CONFIGS[z]))])
        return GeneratedQuestion(
            stem=[text("การจัดอิเล็กตรอนข้อใดเป็นธาตุอโลหะที่ไวต่อปฏิกิริยา"
                       "มากที่สุดในกลุ่มที่กำหนด")],
            correct=[text(_ELECTRON_CONFIGS[answer])],
            distractors=fixed(*wrongs),
            topic="การจัดอิเล็กตรอนและความไวต่อปฏิกิริยา",
            hint=[text("ระบุธาตุจากการจัดอิเล็กตรอน แล้วเปรียบเทียบแฮโลเจนตามหมู่")],
        )


@question_type(
    "chem.posn2561_q06", display_name={"th": "เปรียบเทียบพลังงานไอออไนเซชันลำดับที่สอง"},
    level=LEVEL, subject="เคมี", topic="พลังงานไอออไนเซชันลำดับที่สอง",
)
class SecondIonizationComparisons(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q06.PARAMS, *q06.VARIANTS))
        answer = q06.solve(**values)
        labels = ("L", "M", "Q", "R", "T")
        claims = tuple(f"IE₂({left}) < IE₂({right})"
                       for left, right in zip(labels, labels[1:]))
        mistakes = (
            "chem.posn2561_reversed_l_m_second_ie_comparison",
            "chem.posn2561_reversed_m_q_second_ie_comparison",
            "chem.posn2561_reversed_q_r_second_ie_comparison",
            "chem.posn2561_reversed_r_t_second_ie_comparison",
        )
        assignments = ", ".join(f"{label}={z}" for label, z in
                                zip(labels, values["elements"]))
        data = ", ".join(f"{label}: {q06.IE2_EV[z]:.3f}"
                         for label, z in zip(labels, values["elements"]))
        return GeneratedQuestion(
            stem=[text(f"ธาตุสมมติมีเลขอะตอม {assignments} ตามลำดับ "
                       f"ข้อมูล IE₂ (eV) คือ {data} "
                       "การเปรียบเทียบข้อใดไม่ถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[i], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="พลังงานไอออไนเซชันลำดับที่สอง",
            hint=[text("IE₂ คือพลังงานดึงอิเล็กตรอนจากไอออนประจุ +1; เปรียบเทียบค่าทีละคู่")],
        )


@question_type(
    "chem.posn2561_q07", display_name={"th": "เปรียบเทียบรัศมีอะตอมและไอออน"},
    level=LEVEL, subject="เคมี", topic="รัศมีอะตอมและไอออน",
)
class AtomicAndIonicRadii(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q07.PARAMS, *q07.VARIANTS))
        answer = q07.solve(**values)
        claims = ("Na > Na⁺ > Cl", "Ca > Cl > Na⁺",
                  "Br⁻ > Br > Ca", "Br > Cl > Na")
        mistakes = (
            "", "chem.posn2561_overestimated_chlorine_vs_sodium_ion",
            "chem.posn2561_overestimated_bromine_vs_calcium",
            "chem.posn2561_reversed_sodium_period_trend",
        )
        data = ", ".join(f"{species}={radius}" for species, radius in
                         zip(q07.SPECIES, values["radii"]))
        return GeneratedQuestion(
            stem=[text(f"ใช้ข้อมูลรัศมีที่กำหนด (pm): {data} "
                       "การเปรียบเทียบข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[i], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="รัศมีอะตอมและไอออน",
            hint=[text("เปรียบเทียบรัศมีทั้งสามตัวในแต่ละข้อความจากข้อมูลชุดเดียวกัน")],
        )


@question_type(
    "chem.posn2561_q08", display_name={"th": "ตรวจลำดับสมบัติของ P Ca และ As"},
    level=LEVEL, subject="เคมี", topic="สมบัติตามคาบและหมู่",
)
class PeriodicPropertyRanks(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q08.PARAMS, *q08.VARIANTS))
        answer = q08.solve(**values)
        labels = dict(zip(q08.ELEMENTS, values["labels"]))
        claims = tuple(f"{name}: {' > '.join(order)}" for name, order in
                       zip(("IE₁", "EN", "รัศมี", "จุดหลอมเหลว"),
                           (order for _, order in q08.claims(values["labels"]))))
        mistakes = (
            "", "chem.posn2561_confused_p_as_electronegativity",
            "chem.posn2561_reversed_periodic_size_trend",
            "chem.posn2561_misranked_arsenic_melting_point",
        )
        assignments = ", ".join(f"{element}={labels[element]}" for element in q08.ELEMENTS)
        data = "; ".join(
            f"{name} ({unit}): " + ", ".join(
                f"{labels[element]}={q08.PROPERTIES[property_name][element]:g}"
                for element in q08.ELEMENTS
            )
            for property_name, name, unit in (
                ("ie", "IE₁", "kJ/mol"), ("en", "EN", "Pauling"),
                ("radius", "รัศมี", "pm"), ("melting", "จุดหลอมเหลว", "°C"),
            )
        )
        return GeneratedQuestion(
            stem=[text(f"ธาตุ P, Ca และ As แทนด้วยสัญลักษณ์ {assignments} "
                       "ตามลำดับ สำหรับ As ใช้จุดหลอมเหลวของรูปสีเทาภายใต้ความดัน "
                       f"ข้อมูลสมบัติมีดังนี้: {data} "
                       "ข้อความเรียงค่าจากมากไปน้อยข้อใดผิด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[i], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สมบัติตามคาบและหมู่",
            hint=[text("ตรวจ IE₁ และ EN แยกจากขนาดอะตอม; As สีเทาระเหิดที่ความดันปกติ")],
        )


@question_type(
    "chem.posn2561_q09", display_name={"th": "ออกไซด์กรดและเบสในน้ำ"},
    level=LEVEL, subject="เคมี", topic="สมบัติกรดเบสของออกไซด์",
)
class OxidePairsInWater(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q09.PARAMS, *q09.VARIANTS))
        answer = q09.solve(**values)
        options = values["options"]
        claims = tuple(f"X={q09.PAIRS[i][0]}, Y={q09.PAIRS[i][1]}" for i in options)
        mistakes = (
            "chem.posn2561_treated_beo_as_acidic_oxide",
            "chem.posn2561_treated_sio2_as_water_soluble",
            "chem.posn2561_treated_al2o3_as_basic_in_water",
            "",
        )
        return GeneratedQuestion(
            stem=[text("ออกไซด์ X เมื่อละลายน้ำให้สารละลายกรด "
                       "และออกไซด์ Y เมื่อละลายน้ำให้สารละลายเบส "
                       "คู่ใดสอดคล้องกับข้อมูล")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สมบัติกรดเบสของออกไซด์",
            hint=[text("ออกไซด์อโลหะบางชนิดให้กรดกับน้ำ; ตรวจว่าออกไซด์อีกตัวทำปฏิกิริยากับน้ำให้เบสจริง")],
        )


@question_type(
    "chem.posn2561_q10", display_name={"th": "อนุมานแมกนีเซียมไอโอไดด์จากการทดลอง"},
    level=LEVEL, subject="เคมี", topic="การระบุโลหะและแฮโลเจนจากปฏิกิริยา",
)
class IdentifyMagnesiumIodide(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q10.PARAMS, *q10.VARIANTS))
        answer = q10.solve(**values)
        options = values["options"]
        claims = tuple(q10.CLAIMS[i] for i in options)
        mistakes = (
            "", "chem.posn2561_assumed_iodide_solution_colored",
            "chem.posn2561_misranked_third_ionization",
            "chem.posn2561_assumed_magnesium_sulfate_precipitates",
        )
        return GeneratedQuestion(
            stem=[text("โลหะ M ทำปฏิกิริยากับธาตุ X ซึ่งเป็นของแข็งระเหิดง่าย "
                       "ได้เกลือ Y ที่ละลายน้ำดี เติมน้ำคลอรีนแล้วสกัดด้วย CCl₄ "
                       "ได้ชั้นสีม่วง M แทบไม่ทำปฏิกิริยากับน้ำเย็น "
                       "แต่ในน้ำร้อนให้ H₂ สารละลายเบสและตะกอนขาว "
                       "ข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="การระบุโลหะและแฮโลเจนจากปฏิกิริยา",
            hint=[text("สีม่วงใน CCl₄ บ่งชี้ I₂; น้ำร้อนกับโลหะให้ไฮดรอกไซด์ขาว")],
        )


@question_type(
    "chem.posn2561_q11", display_name={"th": "เลขออกซิเดชันและสารประกอบของฟอสฟอรัส"},
    level=LEVEL, subject="เคมี", topic="เลขออกซิเดชันและออกไซด์ของฟอสฟอรัส",
)
class PhosphorusOxidationStates(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q11.PARAMS, *q11.VARIANTS))
        answer = q11.solve(**values)
        options = values["options"]
        claims = tuple(q11.claims(values["label"])[i] for i in options)
        mistakes = (
            "chem.posn2561_confused_phosphorus_diatomic_form",
            "chem.posn2561_confused_phosphorus_room_state",
            "", "chem.posn2561_assumed_all_phosphorus_chlorides_polar",
        )
        return GeneratedQuestion(
            stem=[text(f"ธาตุ {values['label']} อยู่คาบ 3 และมีเลขออกซิเดชันตั้งแต่ "
                       "−3 ถึง +5 ข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="เลขออกซิเดชันและออกไซด์ของฟอสฟอรัส",
            hint=[text("ระบุธาตุจากคาบและช่วงเลขออกซิเดชัน แล้วตรวจ P₄, ออกไซด์ และ PCl₅")],
        )


@question_type(
    "chem.posn2561_q12", display_name={"th": "สารละลายที่มีสีทั้งคู่"},
    level=LEVEL, subject="เคมี", topic="สีของสารละลายไอออน",
)
class ColoredSolutionPairs(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q12.PARAMS, *q12.VARIANTS))
        answer = q12.solve(**values)
        options = values["options"]
        claims = tuple(f"{q12.PAIRS[i][0]} และ {q12.PAIRS[i][1]}" for i in options)
        mistakes = (
            "chem.posn2561_assumed_sulfate_solution_colored",
            "chem.posn2561_assumed_sodium_chloride_solution_colored",
            "", "chem.posn2561_assumed_rubidium_chloride_solution_colored",
        )
        return GeneratedQuestion(
            stem=[text("ละลายสารแต่ละชนิดในน้ำให้สารละลายเจือจาง "
                       "คู่ใดให้สารละลายมีสีทั้งสองชนิด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สีของสารละลายไอออน",
            hint=[text("ไอออน Cr₂O₇²⁻ และ Fe³⁺ มีสี; ตรวจอีกสารในแต่ละคู่ด้วย")],
        )


@question_type(
    "chem.posn2561_q13", display_name={"th": "จำแนกไอออนจากตะกอนคาร์บอเนตและซัลเฟต"},
    level=LEVEL, subject="เคมี", topic="การตกตะกอนและกฎการละลาย",
)
class PrecipitationIdentification(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q13.PARAMS, *q13.VARIANTS))
        answer = q13.solve(**values)
        options = values["options"]
        claims = tuple("A={}, B={}, C={}".format(*q13.OPTIONS[i]) for i in options)
        mistakes = (
            "chem.posn2561_misassigned_magnesium_to_no_precipitate",
            "chem.posn2561_misassigned_barium_to_no_precipitate",
            "chem.posn2561_swapped_barium_magnesium_precipitates",
            "",
        )
        return GeneratedQuestion(
            stem=[text("ทดสอบสารละลาย A, B, C แยกกันด้วย NaCl, Na₂CO₃, Na₂SO₄: "
                       "A ให้ตะกอนขาวเฉพาะกับ Na₂CO₃; B ไม่ให้ตะกอน; "
                       "C ให้ตะกอนขาวกับ Na₂CO₃ และ Na₂SO₄ "
                       "ข้อใดอาจเป็นสูตรของ A, B, C ตามลำดับ")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="การตกตะกอนและกฎการละลาย",
            hint=[text("คาร์บอเนตของ Mg และ Ba ตกตะกอน แต่ซัลเฟตของ Ba เท่านั้นที่ตกตะกอน")],
        )


@question_type(
    "chem.posn2561_q14", display_name={"th": "เลขออกซิเดชันสูงสุดในสารเชิงซ้อน"},
    level=LEVEL, subject="เคมี", topic="สารประกอบเชิงซ้อนและเลขออกซิเดชัน",
)
class HighestComplexOxidation(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q14.PARAMS, *q14.VARIANTS))
        answer = q14.solve(**values)
        options = values["options"]
        claims = tuple(q14.COMPOUNDS[i] for i in options)
        mistakes = (
            "chem.posn2561_ignored_complex_requirement_for_manganese",
            "chem.posn2561_treated_nickel_sulfate_as_complex",
            "chem.posn2561_misranked_iron_chromium_oxidation",
            "",
        )
        return GeneratedQuestion(
            stem=[text("ข้อใดเป็นสารประกอบเชิงซ้อนที่โลหะแทรนซิชันกลาง "
                       "มีเลขออกซิเดชันสูงที่สุดในบรรดาสารเชิงซ้อนที่ให้")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สารประกอบเชิงซ้อนและเลขออกซิเดชัน",
            hint=[text("คัดสารที่มีไอออนเชิงซ้อนในวงเล็บก่อน แล้วใช้ประจุลิแกนด์คำนวณเลขออกซิเดชัน")],
        )


@question_type(
    "chem.posn2561_q15", display_name={"th": "รังสีที่ทำให้เลขอะตอมเพิ่มหนึ่ง"},
    level=LEVEL, subject="เคมี", topic="การสลายตัวแบบบีตาลบ",
)
class AtomicNumberIncreaseRadiation(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q15.PARAMS, *q15.VARIANTS))
        answer = q15.solve(**values)
        mistakes = (
            "chem.posn2561_confused_alpha_atomic_number_change",
            "", "chem.posn2561_assumed_gamma_changes_element",
            "chem.posn2561_confused_positron_with_beta_minus",
        )
        return GeneratedQuestion(
            stem=[text(f"นิวเคลียสเริ่มต้นมีเลขอะตอม {values['z']} และเลขมวล "
                       f"{values['a']} หลังสลายตัวได้ธาตุใหม่เลขอะตอม "
                       f"{values['z'] + 1} โดยเลขมวลคงเดิม "
                       "แผ่รังสีชนิดใด")],
            correct=[text(q15.RADIATIONS[answer])],
            distractors=fixed(*( [text(named(mistakes[i], radiation))]
                                for i, radiation in enumerate(q15.RADIATIONS)
                                if i != answer)),
            topic="การสลายตัวแบบบีตาลบ",
            hint=[text("β⁻ เปลี่ยนนิวตรอนเป็นโปรตอน ส่วน β⁺ เปลี่ยนโปรตอนเป็นนิวตรอน")],
        )


@question_type(
    "chem.posn2561_q16", display_name={"th": "กราฟมวลสารกัมมันตรังสีตามครึ่งชีวิต"},
    level=LEVEL, subject="เคมี", topic="กฎการสลายตัวและครึ่งชีวิต",
)
class ParentMassDecayGraph(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q16.PARAMS, *q16.VARIANTS))
        answer = q16.solve(**values)
        initial, half_life = values["initial"], values["half_life"]
        times = (0, half_life, 2 * half_life)
        claims = tuple(
            ", ".join(f"m({time})={mass}" for time, mass in zip(times, masses))
            for masses in q16.graph_values(initial, half_life)
        )
        mistakes = (
            "", "chem.posn2561_graphed_daughter_instead_of_parent",
            "chem.posn2561_halved_at_half_the_stated_half_life",
            "chem.posn2561_graphed_fast_daughter_growth",
        )
        return GeneratedQuestion(
            stem=[text(f"ธาตุกัมมันตรังสี X เริ่มต้นมวล {initial} หน่วย "
                       f"และมีครึ่งชีวิต {half_life} วินาที "
                       "ข้อใดให้ค่ามวล X ตามเวลาอย่างถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[i], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="กฎการสลายตัวและครึ่งชีวิต",
            hint=[text("มวลของ X ต้องเริ่มที่มวลตั้งต้นและเหลือครึ่งหนึ่งทุกหนึ่งครึ่งชีวิต")],
        )


@question_type(
    "chem.posn2561_q17", display_name={"th": "จำแนกปฏิกิริยานิวเคลียร์ฟิวชัน"},
    level=LEVEL, subject="เคมี", topic="ฟิวชันและปฏิกิริยานิวเคลียร์",
)
class IdentifyNuclearFusion(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q17.PARAMS, *q17.VARIANTS))
        answer = q17.solve(**values)
        options = values["options"]
        claims = tuple(q17.REACTIONS[i] for i in options)
        mistakes = (
            "chem.posn2561_confused_beta_decay_with_fusion",
            "chem.posn2561_confused_neutron_exchange_with_fusion",
            "", "chem.posn2561_confused_fission_with_fusion",
        )
        return GeneratedQuestion(
            stem=[text("สมการนิวเคลียร์ข้อใดแสดงปฏิกิริยาฟิวชัน")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="ฟิวชันและปฏิกิริยานิวเคลียร์",
            hint=[text("ฟิวชันเริ่มจากนิวเคลียสเบาสองตัวรวมกันให้ผลิตภัณฑ์ที่หนักกว่า")],
        )


@question_type(
    "chem.posn2561_q18", display_name={"th": "ออกไซด์ที่ให้สารละลายเบส"},
    level=LEVEL, subject="เคมี", topic="ออกไซด์โลหะและสารละลายเบส",
)
class BasicOxideElements(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q18.PARAMS, *q18.VARIANTS))
        answer = q18.solve(**values)
        options = values["options"]
        labels = ("A", "D", "L", "M")
        claims = tuple(f"ธาตุ {labels[q18.PAIRS[i][0]]} และ "
                       f"{labels[q18.PAIRS[i][1]]}" for i in options)
        mistakes = (
            "chem.posn2561_treated_both_nonmetal_oxides_as_basic",
            "chem.posn2561_treated_nitrogen_oxide_as_basic",
            "chem.posn2561_treated_sulfur_oxide_as_basic",
            "",
        )
        assignments = ", ".join(f"{label}={z}" for label, z in
                                zip(labels, q18.ATOMIC_NUMBERS))
        return GeneratedQuestion(
            stem=[text(f"ธาตุสมมติมีเลขอะตอม {assignments} ตามลำดับ "
                       "ออกไซด์ของธาตุคู่ใดทำปฏิกิริยากับน้ำให้สารละลาย "
                       "ที่เปลี่ยนฟีนอลฟ์ทาลีนจากไม่มีสีเป็นสีชมพู")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="ออกไซด์โลหะและสารละลายเบส",
            hint=[text("จับเลขอะตอมเป็น N, S, Ca, Rb แล้วพิจารณาไฮดรอกไซด์จากออกไซด์โลหะ")],
        )


@question_type(
    "chem.posn2561_q19", display_name={"th": "อนุมานหมู่ของแกลเลียมจากปฏิกิริยา"},
    level=LEVEL, subject="เคมี", topic="การระบุธาตุจากปฏิกิริยาและเลขออกซิเดชัน",
)
class GalliumIdentityInference(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q19.PARAMS, *q19.VARIANTS))
        answer = q19.solve(**values)
        options = values["options"]
        claims = tuple(q19.CLAIMS[i] for i in options)
        mistakes = (
            "", "chem.posn2561_ignored_period_four_clue",
            "chem.posn2561_misidentified_acid_gas",
            "chem.posn2561_missed_gallium_aluminium_group",
        )
        return GeneratedQuestion(
            stem=[text("ธาตุ X เป็นของแข็งที่ 20°C เลขอะตอม 19–36 ไม่ทำปฏิกิริยา"
                       "กับน้ำ แต่กับกรดให้แก๊ส Y และสารละลายไม่มีสี "
                       "X 2 mol รวมกับ Cl₂ 3 mol ได้คลอไรด์ ข้อสรุปใดผิด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="การระบุธาตุจากปฏิกิริยาและเลขออกซิเดชัน",
            hint=[text("อัตราส่วน X:Cl₂ = 2:3 ให้ XCl₃; ใช้ช่วงเลขอะตอมและสีสารละลายระบุธาตุ")],
        )


@question_type(
    "chem.posn2561_q20", display_name={"th": "สมการปฏิกิริยาของรูบิเดียม"},
    level=LEVEL, subject="เคมี", topic="ปฏิกิริยาโลหะหมู่ 1 และกฎการละลาย",
)
class RubidiumReactionEquation(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q20.PARAMS, *q20.VARIANTS))
        answer = q20.solve(**values)
        options = values["options"]
        claims = tuple(q20.CLAIMS[i] for i in options)
        mistakes = (
            "", "chem.posn2561_assumed_rubidium_dichloride",
            "chem.posn2561_assumed_iodine_displaces_bromine",
            "chem.posn2561_ignored_barium_sulfate_precipitate",
        )
        return GeneratedQuestion(
            stem=[text("M มีเลขอะตอม 37 สมการใดถูกต้องทั้งผลิตภัณฑ์ "
                       "และการดุลสมการ")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="ปฏิกิริยาโลหะหมู่ 1 และกฎการละลาย",
            hint=[text("M คือ Rb ประจุ +1; ตรวจสมดุลอะตอม การแทนที่แฮโลเจน และ BaSO₄")],
        )


@question_type(
    "chem.posn2561_q21", display_name={"th": "พันธะและคู่โดดเดี่ยวของไซยาโนเจน"},
    level=LEVEL, subject="เคมี", topic="สูตรลิวอิสและกฎออกเตต",
)
class CyanogenLewisCounts(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q21.PARAMS, *q21.VARIANTS))
        answer = q21.solve(**values)
        options = values["options"]
        claims = tuple("พันธะเดี่ยว {}, พันธะคู่ {}, พันธะสาม {}, คู่โดดเดี่ยว {}".format(
            *q21.OPTIONS[i]) for i in options)
        mistakes = (
            "chem.posn2561_counted_one_cyanogen_triple_bond",
            "", "chem.posn2561_used_double_bonds_for_cyanogen",
            "chem.posn2561_overcounted_cyanogen_bonds",
        )
        return GeneratedQuestion(
            stem=[text("C₂N₂ เป็นโมเลกุลเป็นกลางที่ทุกอะตอมครบออกเตต "
                       "สูตรลิวอิสมีพันธะเดี่ยว พันธะคู่ พันธะสาม "
                       "และอิเล็กตรอนคู่โดดเดี่ยวกี่คู่ตามลำดับ")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สูตรลิวอิสและกฎออกเตต",
            hint=[text("วางโครง N–C–C–N แล้วเติมพันธะให้ C มีสี่และ N มีสามพันธะ")],
        )


@question_type(
    "chem.posn2561_q22", display_name={"th": "เปรียบเทียบ CS₂ กับ SiO₂"},
    level=LEVEL, subject="เคมี", topic="แรงยึดเหนี่ยวและโครงผลึกร่างตาข่าย",
)
class CarbonDisulfideSilicaProperties(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q22.PARAMS, *q22.VARIANTS))
        answer = q22.solve(**values)
        options = values["options"]
        claims = tuple(q22.CLAIMS[i] for i in options)
        mistakes = (
            "chem.posn2561_assumed_cs2_has_dipole_forces",
            "chem.posn2561_ranked_molecular_above_network_melting",
            "",
            "chem.posn2561_assumed_silica_dissolves_in_hexane",
        )
        return GeneratedQuestion(
            stem=[text("A เกิดจากธาตุเลขอะตอม 6 และ 16 ส่วน B เกิดจากธาตุ "
                       "เลขอะตอม 14 และ 8 ข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="แรงยึดเหนี่ยวและโครงผลึกร่างตาข่าย",
            hint=[text("ระบุ CS₂ กับ SiO₂ แล้วแยกโมเลกุลสมมาตรออกจากผลึกร่างตาข่าย")],
        )


@question_type(
    "chem.posn2561_q23", display_name={"th": "รูปทรงและขั้วของโมเลกุล"},
    level=LEVEL, subject="เคมี", topic="ทฤษฎี VSEPR และสภาพขั้ว",
)
class MolecularShapesAndPolarity(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q23.PARAMS, *q23.VARIANTS))
        answer = q23.solve(**values)
        options = values["options"]
        claims = tuple(q23.CLAIMS[i] for i in options)
        mistakes = (
            "", "chem.posn2561_assumed_sih4_polar_ignored_tef6",
            "chem.posn2561_assumed_sih4_polar_ignored_sbcl5",
            "chem.posn2561_assumed_sih4_polar",
        )
        distractors = fixed(*( [text(named(mistakes[options[i]], claim))]
                               for i, claim in enumerate(claims) if i != answer))
        # The four authored combinations are exhaustive. A generic prose
        # double-slip could invent an invalid repeated number such as "2 และ 2".
        distractors.balanced = True
        return GeneratedQuestion(
            stem=[text("พิจารณาข้อความ: " + " ; ".join(
                f"{i}. {statement}" for i, statement in enumerate(q23.STATEMENTS, 1)
            ) + " ข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=distractors,
            topic="ทฤษฎี VSEPR และสภาพขั้ว",
            hint=[text("นับคู่พันธะและคู่โดดเดี่ยว แล้วตรวจว่าคู่ขั้วพันธะหักล้างกันหรือไม่")],
        )


@question_type(
    "chem.posn2561_q24", display_name={"th": "กลุ่มสารโคเวเลนต์ที่ละลายน้ำ"},
    level=LEVEL, subject="เคมี", topic="สภาพขั้วและการละลายน้ำของสารโคเวเลนต์",
)
class CovalentWaterSolubilityGroup(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q24.PARAMS, *q24.VARIANTS))
        answer = q24.solve(**values)
        options = values["options"]
        claims = tuple(" / ".join(q24.GROUPS[i]) for i in options)
        mistakes = (
            "chem.posn2561_assumed_benzene_water_soluble", "",
            "chem.posn2561_assumed_ccl4_silica_water_soluble",
            "chem.posn2561_assumed_cs2_water_soluble",
        )
        return GeneratedQuestion(
            stem=[text("กลุ่มใดประกอบด้วยสารโคเวเลนต์ที่ละลายน้ำได้ดีทุกชนิด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สภาพขั้วและการละลายน้ำของสารโคเวเลนต์",
            hint=[text("ตรวจทุกสารในแต่ละกลุ่ม รวมทั้งแยกสารไอออนิกออกจากโคเวเลนต์")],
        )


@question_type(
    "chem.posn2561_q25", display_name={"th": "อนุมานสภาพขั้วจากการสกัด"},
    level=LEVEL, subject="เคมี", topic="ความมีขั้วและการสกัดด้วยตัวทำละลาย",
)
class SolventExtractionPolarityTrend(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q25.PARAMS, *q25.VARIANTS))
        answer = q25.solve(**values)
        options = values["options"]
        claims = tuple(q25.CLAIMS[i] for i in options)
        mistakes = (
            "chem.posn2561_assumed_extraction_proves_binary_polarity",
            "chem.posn2561_rejected_possible_d_hydrogen_bonding",
            "",
            "chem.posn2561_assumed_chloroform_extract_nonpolar",
        )
        distractors = fixed(*( [text(named(mistakes[options[i]], claim))]
                               for i, claim in enumerate(claims) if i != answer))
        # These statement combinations are the complete reviewed choice set.
        distractors.balanced = True
        rows = "; ".join(
            f"{solvent}: " + ", ".join(f"{name} {percent}%" for name, percent in composition)
            for solvent, composition in q25.EXTRACTS
        )
        return GeneratedQuestion(
            stem=[text("สารสกัดจากสมุนไพรถูกแยกด้วยตัวทำละลายเรียงจากขั้วน้อยไปมาก "
                       f"(ร้อยละโดยมวลในแต่ละสารสกัด): {rows} "
                       + "พิจารณาข้อสรุปเชิงแนวโน้ม: " + " ; ".join(
                           f"{i}. {statement}" for i, statement in enumerate(q25.STATEMENTS, 1)
                       ) + " ข้อใดเหมาะสม")],
            correct=[text(claims[answer])],
            distractors=distractors,
            topic="ความมีขั้วและการสกัดด้วยตัวทำละลาย",
            hint=[text("เฮกเซน < คลอโรฟอร์ม < เอทานอลด้านความมีขั้ว; "
                       "การสกัดบอกแนวโน้ม ไม่ยืนยันหมู่ฟังก์ชันของสาร")],
        )


@question_type(
    "chem.posn2561_q26", display_name={"th": "ลำดับการกลั่นของบิวเทน อีเทอร์ และเอทานอล"},
    level=LEVEL, subject="เคมี", topic="จุดเดือด แรงยึดเหนี่ยว และการกลั่นลำดับส่วน",
)
class FractionalDistillationOrder(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q26.PARAMS, *q26.VARIANTS))
        answer = q26.solve(**values)
        options = values["options"]
        claims = tuple(" → ".join(q26.ORDERS[i]) for i in options)
        mistakes = (
            "chem.posn2561_reversed_distillation_by_boiling_point",
            "chem.posn2561_ranked_ether_below_butane_boiling",
            "",
            "chem.posn2561_ignored_ethanol_hydrogen_bonding",
        )
        return GeneratedQuestion(
            stem=[text("ของผสมบิวเทน ไดเอทิลอีเทอร์ และเอทานอลถูกทำให้เย็นจนเป็นของเหลว "
                       "แล้วกลั่นลำดับส่วนที่ความดัน 1 atm สารออกมาก่อนจนถึงสุดท้ายเรียงอย่างไร")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="จุดเดือด แรงยึดเหนี่ยว และการกลั่นลำดับส่วน",
            hint=[text("เปรียบเทียบจุดเดือด: บิวเทนต่ำสุด อีเทอร์ถัดมา เอทานอลสูงสุด")],
        )


@question_type(
    "chem.posn2561_q27", display_name={"th": "กฎออกเตตที่อะตอมกลาง"},
    level=LEVEL, subject="เคมี", topic="กฎออกเตตและโครงสร้างลิวอิส",
)
class CentralAtomOctetPairs(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q27.PARAMS, *q27.VARIANTS))
        answer = q27.solve(**values)
        options = values["options"]
        claims = tuple(" และ ".join(q27.PAIRS[i]) for i in options)
        mistakes = (
            "chem.posn2561_treated_no2_radical_as_octet",
            "chem.posn2561_treated_no2_radical_as_octet_with_carbonate",
            "chem.posn2561_treated_xef4_expanded_octet_as_eight",
            "",
        )
        return GeneratedQuestion(
            stem=[text("ใน NO₂, BF₄⁻, XeF₄ และ CO₃²⁻ คู่ใดมีอะตอมกลางที่นับ "
                       "อิเล็กตรอนในโครงสร้างลิวอิสได้แปดตัวทั้งคู่")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="กฎออกเตตและโครงสร้างลิวอิส",
            hint=[text("NO₂ เป็นอนุมูลอิสระอิเล็กตรอนคี่; XeF₄ มีคู่โดดเดี่ยวบน Xe สองคู่")],
        )


@question_type(
    "chem.posn2561_q28", display_name={"th": "พันธะในแอมโมเนียมไอออน"},
    level=LEVEL, subject="เคมี", topic="พันธะโคเวเลนต์และโครงสร้างแอมโมเนียม",
)
class AmmoniumEquivalentBonds(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q28.PARAMS, *q28.VARIANTS))
        answer = q28.solve(**values)
        options = values["options"]
        claims = tuple(q28.CLAIMS[i] for i in options)
        mistakes = (
            "chem.posn2561_misidentified_ammonium_shape",
            "chem.posn2561_misidentified_nh_bond_polarity",
            "chem.posn2561_assumed_ammonium_lone_pair",
            "",
        )
        return GeneratedQuestion(
            stem=[text("ข้อใดกล่าวผิดเกี่ยวกับ NH₄⁺ ที่เกิดจาก NH₃ รับ H⁺")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="พันธะโคเวเลนต์และโครงสร้างแอมโมเนียม",
            hint=[text("หลังเกิดไอออนแล้ว H ทั้งสี่อยู่ในสภาพสมมูลกันในทรงสี่หน้า")],
        )


@question_type(
    "chem.posn2561_q29", display_name={"th": "โมเลกุลที่รูปร่างแตกต่าง"},
    level=LEVEL, subject="เคมี", topic="ทฤษฎี VSEPR และรูปร่างโมเลกุล",
)
class BentVersusLinearMolecule(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q29.PARAMS, *q29.VARIANTS))
        answer = q29.solve(**values)
        options = values["options"]
        claims = tuple(q29.MOLECULES[i] for i in options)
        mistakes = (
            "", "chem.posn2561_assumed_co2_bent",
            "chem.posn2561_assumed_xef2_bent",
            "chem.posn2561_assumed_becl2_bent",
        )
        return GeneratedQuestion(
            stem=[text("เมื่อพิจารณาโมเลกุลเดี่ยวในสถานะแก๊ส "
                       "สารใดมีรูปร่างโมเลกุลแตกต่างจากอีกสามชนิด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="ทฤษฎี VSEPR และรูปร่างโมเลกุล",
            hint=[text("SO₂ มีคู่โดดเดี่ยวบน S หนึ่งคู่; "
                       "XeF₂ มีคู่โดดเดี่ยวสามคู่เรียงในระนาบเส้นศูนย์สูตร")],
        )


@question_type(
    "chem.posn2561_q30", display_name={"th": "มุมพันธะที่เล็กที่สุด"},
    level=LEVEL, subject="เคมี", topic="รูปทรงโมเลกุลและมุมพันธะ",
)
class SmallestMolecularBondAngle(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q30.PARAMS, *q30.VARIANTS))
        answer = q30.solve(**values)
        options = values["options"]
        claims = tuple(q30.MOLECULES[i] for i in options)
        mistakes = (
            "chem.posn2561_assumed_ncl3_angle_under_90",
            "", "chem.posn2561_assumed_socl2_angle_under_90",
            "chem.posn2561_assumed_ch2cl2_angle_under_90",
        )
        return GeneratedQuestion(
            stem=[text("สำหรับโมเลกุลเดี่ยวในสถานะแก๊ส ถ้าพิจารณามุมระหว่าง "
                       "พันธะที่เล็กที่สุดของแต่ละโมเลกุล สารใดมีค่าน้อยที่สุด")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="รูปทรงโมเลกุลและมุมพันธะ",
            hint=[text("PCl₅ แบบพีระมิดคู่ฐานสามเหลี่ยมมีมุมระหว่างพันธะแนวแกนกับแนวระนาบ 90°")],
        )


@question_type(
    "chem.posn2561_q31", display_name={"th": "คู่โมเลกุลที่มีแรงระหว่างขั้ว"},
    level=LEVEL, subject="เคมี", topic="สภาพขั้วโมเลกุลและแรงระหว่างขั้ว",
)
class PolarMoleculePair(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q31.PARAMS, *q31.VARIANTS))
        answer = q31.solve(**values)
        options = values["options"]
        claims = tuple(" และ ".join(q31.PAIRS[i]) for i in options)
        mistakes = (
            "chem.posn2561_assumed_co2_polar_imf",
            "chem.posn2561_assumed_o2_polar_imf",
            "chem.posn2561_assumed_methane_silane_polar_imf",
            "",
        )
        return GeneratedQuestion(
            stem=[text("คู่ใดมีแรงดึงดูดระหว่างโมเลกุลแบบขั้ว–ขั้วทั้งสองสาร "
                       "(ไม่นับแรงลอนดอนซึ่งมีในทุกสาร)")],
            correct=[text(claims[answer])],
            distractors=fixed(*( [text(named(mistakes[options[i]], claim))]
                                for i, claim in enumerate(claims) if i != answer)),
            topic="สภาพขั้วโมเลกุลและแรงระหว่างขั้ว",
            hint=[text("ตรวจรูปร่างและการหักล้างของขั้ว; PH₃ และ H₂S มีขั้วอ่อน")],
        )


@question_type(
    "chem.posn2561_q32", display_name={"th": "พันธะและขั้วของสารโคเวเลนต์"},
    level=LEVEL, subject="เคมี", topic="อันดับพันธะ สภาพขั้ว และจุดเดือด",
)
class BondPolarityBoilingClaims(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q32.PARAMS, *q32.VARIANTS))
        answer = q32.solve(**values)
        options = values["options"]
        claims = tuple(q32.CLAIMS[i] for i in options)
        mistakes = (
            "chem.posn2561_ignored_cf4_chf3_boiling_order", "",
            "chem.posn2561_assumed_bf3_polar_ignored_carbonate_bond",
            "chem.posn2561_assumed_bf3_polar",
        )
        distractors = fixed(*( [text(named(mistakes[options[i]], claim))]
                               for i, claim in enumerate(claims) if i != answer))
        distractors.balanced = True  # Fixed statement combinations only.
        return GeneratedQuestion(
            stem=[text("พิจารณาข้อความ: " + " ; ".join(
                f"{i}. {statement}" for i, statement in enumerate(q32.STATEMENTS, 1)
            ) + " ข้อใดถูกต้อง")],
            correct=[text(claims[answer])],
            distractors=distractors,
            topic="อันดับพันธะ สภาพขั้ว และจุดเดือด",
            hint=[text("CO₃²⁻ มีอันดับพันธะเฉลี่ย 4/3; BF₃ สมมาตร; CF₄ เดือดต่ำกว่า CHF₃")],
        )


@question_type(
    "chem.posn2561_q33", display_name={"th": "ส่วนผสมแก๊สก่อนเกิด HCl"},
    level=LEVEL, subject="เคมี", topic="สัดส่วนแก๊สและปริมาณสารสัมพันธ์",
)
class InitialHydrogenGasFraction(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q33.PARAMS, *q33.VARIANTS))
        answer = q33.solve(**values)
        initial_chlorine = 100 - answer
        return GeneratedQuestion(
            stem=[text("ในขวดปิดที่อุณหภูมิและความดันคงที่ ฉาย UV ให้ H₂ และ Cl₂ "
                       f"ทำปฏิกิริยา พบว่า Cl₂ ลดลง {values['chlorine_consumed_percent']}% "
                       "จากปริมาณเริ่มต้น และแก๊สสุดท้ายมี "
                       f"Cl₂ {values['final_chlorine']}%, H₂ {values['final_hydrogen']}%, "
                       f"HCl {values['final_hcl']}% โดยปริมาตร "
                       "ตอนเริ่มต้น H₂ คิดเป็นร้อยละเท่าใดโดยปริมาตร")],
            correct=[text(str(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_used_final_hydrogen_as_initial",
                            str(values["final_hydrogen"])))],
                [text(named("chem.posn2561_reported_initial_chlorine_instead",
                            str(initial_chlorine)))],
                [text(named("chem.posn2561_counted_all_hcl_as_consumed_hydrogen",
                            str(values["final_hydrogen"] + values["final_hcl"])))],
            ),
            topic="สัดส่วนแก๊สและปริมาณสารสัมพันธ์",
            hint=[text("H₂ + Cl₂ → 2HCl; H₂ ที่ใช้เท่ากับครึ่งหนึ่งของ HCl ที่เกิด")],
        )


@question_type(
    "chem.posn2561_q34", display_name={"th": "ระบุโลหะจากตะกอนแบเรียมซัลเฟต"},
    level=LEVEL, subject="เคมี", topic="มวลโมลและปฏิกิริยาตกตะกอน",
)
class MetalFromSulfatePrecipitate(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q34.PARAMS, *q34.VARIANTS))
        answer = q34.solve(**values)
        names = tuple(name for name, _ in q34.METALS)
        mistakes = (
            "chem.posn2561_chose_titanium_sulfate_mass",
            "chem.posn2561_chose_copper_sulfate_mass",
            "chem.posn2561_chose_zinc_sulfate_mass",
            "chem.posn2561_chose_zirconium_sulfate_mass",
        )
        return GeneratedQuestion(
            stem=[text(f"เกลือ ASO₄ {values['salt_centigrams'] / 100:.2f} g "
                       "ทำปฏิกิริยากับ BaCl₂ มากเกินพอ ได้ตะกอน BaSO₄ "
                       f"{values['precip_centigrams'] / 100:.2f} g "
                       "กำหนดมวลโมล BaSO₄ = 233 และ SO₄ = 96 g/mol "
                       "A เป็นธาตุใด")],
            correct=[text(names[answer])],
            distractors=fixed(*( [text(named(mistakes[i], name))]
                                for i, name in enumerate(names) if i != answer)),
            topic="มวลโมลและปฏิกิริยาตกตะกอน",
            hint=[text("ASO₄ หนึ่งโมลให้ BaSO₄ หนึ่งโมล; หามวลโมล ASO₄ แล้วลบ 96")],
        )


@question_type(
    "chem.posn2561_q35", display_name={"th": "ปริมาตรอากาศสำหรับเผาไหม้แก๊สผสม"},
    level=LEVEL, subject="เคมี", topic="การเผาไหม้และสัดส่วนปริมาตรแก๊ส",
)
class AirForGasMixtureCombustion(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q35.PARAMS, *q35.VARIANTS))
        answer = q35.solve(**values)
        oxygen_volume = answer * values["air_oxygen_percent"] // 100
        air_if_quarter_oxygen = oxygen_volume * 4
        mixture = ", ".join(f"{name} {amount / 10:g}%" for name, amount in
                            zip(q35.GAS_NAMES, q35.GAS_TENTHS))
        return GeneratedQuestion(
            stem=[text(f"แก๊สผสม {mixture} โดยปริมาตร ปริมาตรรวม "
                       f"{values['gas_volume_m3']} m³ เผาไหม้สมบูรณ์ที่อุณหภูมิ"
                       "และความดันเดียวกัน ต้องใช้อากาศอย่างน้อยกี่ m³ "
                       f"ถ้าอากาศมี O₂ {values['air_oxygen_percent']}% โดยปริมาตร")],
            correct=[text(str(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_reported_oxygen_not_air_volume",
                            str(oxygen_volume)))],
                [text(named("chem.posn2561_assumed_air_quarter_oxygen",
                            str(air_if_quarter_oxygen)))],
                [text(named("chem.posn2561_halved_air_oxygen_fraction",
                            str(answer * 2)))],
            ),
            topic="การเผาไหม้และสัดส่วนปริมาตรแก๊ส",
            hint=[text("CO, H₂ ใช้ O₂ อย่างละ 1/2; CH₄ ใช้ 2; C₂H₄ ใช้ 3; "
                       "CO₂ และ Ar ไม่ใช้")],
        )


@question_type(
    "chem.posn2561_q36", display_name={"th": "แมกนีเซียมสำหรับผลิตแอมโมเนีย"},
    level=LEVEL, subject="เคมี", topic="ปริมาณสารสัมพันธ์และร้อยละผลได้",
)
class MagnesiumForAmmoniaYield(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q36.PARAMS, *q36.VARIANTS))
        answer = q36.solve(**values)
        ammonia_liters = values["target_ammonia_centiliters"] / 100
        no_yield = answer * values["nitride_yield_percent"] / 100
        one_to_one = answer * 2 / 3
        fmt = lambda value: f"{float(value):g}"
        return GeneratedQuestion(
            stem=[text("เผา Mg กับ N₂ ให้ Mg₃N₂ ได้ผลได้ "
                       f"{values['nitride_yield_percent']}% แล้วไฮโดรไลซ์จนได้ "
                       f"NH₃ {ammonia_liters:g} L ที่ 0°C, 1 atm "
                       "(22.4 L/mol) ต้องใช้ Mg อย่างน้อยกี่กรัม "
                       "กำหนดมวลอะตอม Mg = 24")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_ignored_nitride_yield",
                            fmt(no_yield)))],
                [text(named("chem.posn2561_used_one_to_one_mg_nh3",
                            fmt(one_to_one)))],
                [text(named("chem.posn2561_halved_nitride_yield",
                            fmt(answer * 2)))],
            ),
            topic="ปริมาณสารสัมพันธ์และร้อยละผลได้",
            hint=[text("3Mg → Mg₃N₂ → 2NH₃; ปรับปริมาณ Mg ตามผลได้ของ Mg₃N₂")],
        )


@question_type(
    "chem.posn2561_q37", display_name={"th": "คาร์บอเนตเหลือหลังตกตะกอน"},
    level=LEVEL, subject="เคมี", topic="สารกำหนดปริมาณและความเข้มข้นหลังผสม",
)
class CarbonateAfterSilverPrecipitation(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q37.PARAMS, *q37.VARIANTS))
        answer = q37.solve(**values)
        c, cv, s, sv = (values[key] for key in
                        ("carbonate_mm", "carbonate_ml", "silver_mm", "silver_ml"))
        volume = cv + sv
        carbonate = Fraction(c * cv, 1000)
        silver = Fraction(s * sv, 1000)
        leftover = carbonate - silver / 2
        fmt = lambda value: f"{float(value):.4f}"
        return GeneratedQuestion(
            stem=[text(f"ผสม Na₂CO₃ {c / 1000:.3f} mol/L ปริมาตร {cv} mL "
                       f"กับ AgNO₃ {s / 1000:.3f} mol/L ปริมาตร {sv} mL "
                       "เกิดตะกอน Ag₂CO₃ จนปฏิกิริยาสมบูรณ์ "
                       "สมมติปริมาตรรวมเท่ากับผลบวกของปริมาตรสารละลาย "
                       "สารตั้งต้นที่เหลือมีความเข้มข้นกี่ mol/L")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_ignored_silver_precipitation",
                            fmt(carbonate / volume)))],
                [text(named("chem.posn2561_ignored_mixed_solution_volume",
                            fmt(leftover / cv)))],
                [text(named("chem.posn2561_used_initial_carbonate_concentration",
                            fmt(Fraction(c, 1000))))],
            ),
            topic="สารกำหนดปริมาณและความเข้มข้นหลังผสม",
            hint=[text("Ag₂CO₃ ใช้ Ag⁺ สองโมลต่อ CO₃²⁻ หนึ่งโมล; หักโมลที่ตกตะกอนแล้วหารด้วยปริมาตรรวม")],
        )


@question_type(
    "chem.posn2561_q38", display_name={"th": "อะลูมิเนียมในโลหะผสมจากแก๊สไฮโดรเจน"},
    level=LEVEL, subject="เคมี", topic="ปริมาณสารสัมพันธ์และองค์ประกอบโลหะผสม",
)
class AluminiumFractionInAlloy(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q38.PARAMS, *q38.VARIANTS))
        answer = q38.solve(**values)
        total, residue = values["alloy_mg"], values["residue_mg"]
        hydrogen = Fraction(values["hydrogen_cm3"]) / Fraction("22.4")
        fmt = lambda value: f"{float(value):.1f}"
        return GeneratedQuestion(
            stem=[text(f"โลหะผสม Al, Zn, Si และ Cu มวล {total} mg "
                       "ทำปฏิกิริยากับ HCl มากเกินพอ ได้ H₂ "
                       f"{values['hydrogen_cm3']} cm³ ที่ 0°C, 1 atm "
                       f"(22.4 L/mol) และเหลือ Si กับ Cu {residue} mg "
                       "Al เป็นร้อยละโดยมวลเท่าใด กำหนดมวลอะตอม Al=27, Zn=65")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_assumed_all_hydrogen_from_aluminium",
                            fmt(100 * hydrogen * 18 / total)))],
                [text(named("chem.posn2561_treated_all_reactive_mass_as_aluminium",
                            fmt(100 * (total - residue) / total)))],
                [text(named("chem.posn2561_used_one_to_one_aluminium_hydrogen",
                            fmt(100 * hydrogen * 27 / total)))],
            ),
            topic="ปริมาณสารสัมพันธ์และองค์ประกอบโลหะผสม",
            hint=[text("ตั้งมวล Al+Zn เท่ากับมวลที่ละลาย และโมล H₂ = 3/2 โมล Al + โมล Zn")],
        )


@question_type(
    "chem.posn2561_q39", display_name={"th": "เหล็กสามหลังออกซิเดชันด้วยเปอร์แมงกาเนต"},
    level=LEVEL, subject="เคมี", topic="รีดอกซ์และความเข้มข้นไอออนหลังผสม",
)
class FerricConcentrationAfterPermanganate(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q39.PARAMS, *q39.VARIANTS))
        answer = q39.solve(**values)
        v, pv = values["mixture_ml"], values["permanganate_ml"]
        ferric = Fraction(values["iron_iii_sulfate_m"]) * v
        oxidized = 5 * Fraction(values["permanganate_m"]) * pv
        fmt = lambda value: f"{float(value):.4f}"
        return GeneratedQuestion(
            stem=[text(f"สารละลายผสม {v} mL มี Fe(NH₄)₂(SO₄)₂ "
                       f"{values['iron_ii_m']} mol/L, Fe₂(SO₄)₃ "
                       f"{values['iron_iii_sulfate_m']} mol/L และ H₂SO₄ มากเกินพอ "
                       f"เติม KMnO₄ {values['permanganate_m']} mol/L {pv} mL "
                       "สมมติปริมาตรรวมเป็นผลบวกของปริมาตรสารละลาย "
                       "ความเข้มข้น Fe³⁺ สุดท้ายเป็นกี่ mol/L? "
                       "5Fe²⁺ + MnO₄⁻ + 8H⁺ → 5Fe³⁺ + Mn²⁺ + 4H₂O")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_omitted_initial_ferric_ions",
                            fmt(oxidized / (v + pv))))],
                [text(named("chem.posn2561_counted_one_ferric_per_ferric_sulfate",
                            fmt((ferric + oxidized) / (v + pv))))],
                [text(named("chem.posn2561_ignored_permanganate_solution_volume",
                            fmt((2 * ferric + oxidized) / v)))],
            ),
            topic="รีดอกซ์และความเข้มข้นไอออนหลังผสม",
            hint=[text("Fe₂(SO₄)₃ เริ่มต้นให้ Fe³⁺ สองโมลต่อโมล; MnO₄⁻ หนึ่งโมลออกซิไดซ์ Fe²⁺ ห้าโมล")],
        )


@question_type(
    "chem.posn2561_q40", display_name={"th": "โซเดียมโบโรไฮไดรด์สำหรับไดบอเรน"},
    level=LEVEL, subject="เคมี", topic="ดุลสมการและร้อยละผลได้",
)
class BorohydrideForDiboraneYield(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q40.PARAMS, *q40.VARIANTS))
        target = Fraction(values["target_diborane_mol"])
        yield_fraction = Fraction(values["yield_percent"], 100)
        answer = q40.solve(**values)
        fmt = lambda value: f"{float(value):.3f}"
        return GeneratedQuestion(
            stem=[text("NaBH₄ ทำปฏิกิริยากับ BF₃ มากเกินพอให้ NaBF₄ และ B₂H₆ "
                       f"ถ้าต้องการ B₂H₆ {float(target):.3f} mol ที่ผลได้ "
                       f"{values['yield_percent']}% ต้องใช้ NaBH₄ กี่ mol")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_ignored_diborane_yield",
                            fmt(target * Fraction(3, 2))))],
                [text(named("chem.posn2561_assumed_one_to_one_borohydride_diborane",
                            fmt(target / yield_fraction)))],
                [text(named("chem.posn2561_reversed_borohydride_diborane_ratio",
                            fmt(target * Fraction(2, 3) / yield_fraction)))],
            ),
            topic="ดุลสมการและร้อยละผลได้",
            hint=[text("ดุลได้ 3NaBH₄ + 4BF₃ → 3NaBF₄ + 2B₂H₆ แล้วปรับด้วยร้อยละผลได้")],
        )


@question_type(
    "chem.posn2561_q41", display_name={"th": "โซเดียมเอไซด์สำหรับแก๊สไนโตรเจน"},
    level=LEVEL, subject="เคมี", topic="ปริมาณสารสัมพันธ์ของแก๊สและปฏิกิริยาต่อเนื่อง",
)
class AzideForNitrogenGas(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q41.PARAMS, *q41.VARIANTS))
        answer = q41.solve(**values)
        nitrogen = (Fraction(values["pressure_mmhg"], 760)
                    * Fraction(values["nitrogen_l"])
                    / (q41.R * (values["temperature_c"] + 273)))
        fmt = lambda value: f"{float(value):.1f}"
        return GeneratedQuestion(
            stem=[text("NaN₃ สลายตัวให้ N₂ และ Na จากนั้น Na ทำปฏิกิริยากับ "
                       "KNO₃ ให้ N₂ เพิ่มอีกตามสมการ "
                       "2NaN₃ → 2Na + 3N₂; "
                       "10Na + 2KNO₃ → K₂O + 5Na₂O + N₂ "
                       f"ถ้าต้องการ N₂ {values['nitrogen_l']} L ที่ "
                       f"{values['temperature_c']}°C และ {values['pressure_mmhg']} mmHg "
                       "ต้องใช้ NaN₃ ประมาณกี่กรัม ตอบทศนิยมหนึ่งตำแหน่ง "
                       "กำหนด R=0.082 L·atm/(mol·K), มวลโมล NaN₃=65 g/mol")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_ignored_nitrate_nitrogen",
                            fmt(nitrogen * Fraction(2, 3) * 65)))],
                [text(named("chem.posn2561_used_stp_volume_for_warm_nitrogen",
                            fmt(Fraction(values["nitrogen_l"]) / Fraction("22.4")
                                * Fraction(values["pressure_mmhg"], 760)
                                * Fraction(5, 8) * 65)))],
                [text(named("chem.posn2561_assumed_one_to_one_azide_nitrogen",
                            fmt(nitrogen * 65)))],
            ),
            topic="ปริมาณสารสัมพันธ์ของแก๊สและปฏิกิริยาต่อเนื่อง",
            hint=[text("NaN₃ หนึ่งโมลให้ N₂ รวม 3/2 + 1/10 = 8/5 mol; ใช้ PV=nRT")],
        )


@question_type(
    "chem.posn2561_q42", display_name={"th": "กรดสำหรับแร่โทรนา"},
    level=LEVEL, subject="เคมี", topic="สมมูลกรดของคาร์บอเนตและไบคาร์บอเนต",
)
class HydrochloricAcidForTrona(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q42.PARAMS, *q42.VARIANTS))
        answer = q42.solve(**values)
        fmt = lambda value: f"{float(value):.1f}"
        return GeneratedQuestion(
            stem=[text("แร่โทรนา Na₂CO₃·NaHCO₃·2H₂O "
                       f"มวล {values['trona_mg'] / 1000:.3f} g "
                       f"(มวลสูตร 226 g/mol) ต้องใช้ HCl {values['acid_m']} mol/L "
                       "กี่ mL จึงเปลี่ยนคาร์บอเนตและไบคาร์บอเนตทั้งหมด "
                       "เป็น CO₂ และ H₂O")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_neutralized_only_carbonate_in_trona",
                            fmt(Fraction(answer) * Fraction(2, 3))))],
                [text(named("chem.posn2561_neutralized_only_bicarbonate_in_trona",
                            fmt(answer / 3)))],
                [text(named("chem.posn2561_counted_both_trona_anions_as_carbonate",
                            fmt(Fraction(answer) * Fraction(4, 3))))],
            ),
            topic="สมมูลกรดของคาร์บอเนตและไบคาร์บอเนต",
            hint=[text("โทรนาหนึ่งสูตรมี CO₃²⁻ หนึ่งตัวใช้ H⁺ สองตัว และ HCO₃⁻ หนึ่งตัวใช้อีกหนึ่งตัว")],
        )


@question_type(
    "chem.posn2561_q43", display_name={"th": "ออกซิเจนจากโพแทสเซียมซูเปอร์ออกไซด์"},
    level=LEVEL, subject="เคมี", topic="สารกำหนดปริมาณและสัดส่วนแก๊ส",
)
class OxygenFromPotassiumSuperoxide(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q43.PARAMS, *q43.VARIANTS))
        ko2_mmol = Fraction(values["superoxide_mg"], 71)
        ko2_potential = Fraction(3, 4) * ko2_mmol * Fraction(224, 10)
        co2_potential = Fraction(3, 2) * values["carbon_dioxide_cm3"]
        answer = q43.solve(**values)
        other_limit = max(ko2_potential, co2_potential)
        return GeneratedQuestion(
            stem=[text("KO₂ ทำปฏิกิริยากับ CO₂ ให้ K₂CO₃ และ O₂ "
                       f"ถ้าใช้ KO₂ {values['superoxide_mg'] / 1000:.3f} g "
                       f"กับ CO₂ {values['carbon_dioxide_cm3']} cm³ "
                       "ปริมาตร O₂ สูงสุดที่ได้เป็นกี่ cm³ ที่ 0°C, 1 atm "
                       "(22.4 L/mol) กำหนดมวลโมล KO₂=71 g/mol")],
            correct=[text(str(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_chose_excess_reagent_for_oxygen",
                            str(int(other_limit))))],
                [text(named("chem.posn2561_used_one_to_one_superoxide_oxygen",
                            str(int(ko2_mmol * Fraction(224, 10)))))],
                [text(named("chem.posn2561_used_one_to_one_carbon_dioxide_oxygen",
                            str(values["carbon_dioxide_cm3"])))],
            ),
            topic="สารกำหนดปริมาณและสัดส่วนแก๊ส",
            hint=[text("ดุล 4KO₂ + 2CO₂ → 2K₂CO₃ + 3O₂ แล้วเทียบ O₂ สูงสุดจากสารตั้งต้นแต่ละตัว")],
        )


@question_type(
    "chem.posn2561_q44", display_name={"th": "ระบุกรดจากโมลาริตี ร้อยละมวล และความหนาแน่น"},
    level=LEVEL, subject="เคมี", topic="โมลาริตี ร้อยละมวล และความหนาแน่น",
)
class AcidFromSolutionConcentrations(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q44.PARAMS, *q44.VARIANTS))
        answer = q44.solve(**values)
        names = [name for name, _ in q44.ACIDS]
        mistakes = (
            "chem.posn2561_chose_hcl_from_concentration",
            "chem.posn2561_chose_hbr_from_concentration",
            "chem.posn2561_chose_acetic_acid_from_concentration",
            "chem.posn2561_chose_phosphoric_acid_from_concentration",
        )
        return GeneratedQuestion(
            stem=[text(f"สารละลายกรด A เข้มข้น {values['molarity']} mol/L "
                       f"มี A {values['mass_percent']}% โดยมวล "
                       f"และมีความหนาแน่น {values['density']} g/mL "
                       "A เป็นกรดชนิดใด")],
            correct=[text(names[answer])],
            distractors=fixed(*([text(named(mistakes[i], name))]
                                for i, name in enumerate(names) if i != answer)),
            topic="โมลาริตี ร้อยละมวล และความหนาแน่น",
            hint=[text("สารละลาย 1 L มีมวล 1000 เท่าของความหนาแน่น; หามวลกรดแล้วหารด้วยจำนวนโมล")],
        )


@question_type(
    "chem.posn2561_q45", display_name={"th": "โซเดียมไอออนหลังผสมเกลือสองชนิด"},
    level=LEVEL, subject="เคมี", topic="ความเข้มข้นไอออนหลังผสมสารละลาย",
)
class SodiumAfterMixingSulfateAndPhosphate(QuestionType):
    sheet_id = SHEET_ID
    sheet = SHEET

    def build(self, rng, **params):
        values = rng.choice((q45.PARAMS, *q45.VARIANTS))
        answer = q45.solve(**values)
        sv, pv = values["sulfate_ml"], values["phosphate_ml"]
        sulfate = Fraction(values["sulfate_m"]) * sv
        phosphate = Fraction(values["phosphate_m"]) * pv
        sodium = 2 * sulfate + 3 * phosphate
        fmt = lambda value: f"{float(value):.4f}"
        return GeneratedQuestion(
            stem=[text(f"ผสม Na₂SO₄ {values['sulfate_m']} mol/L {sv} mL "
                       f"กับ Na₃PO₄ {values['phosphate_m']} mol/L {pv} mL "
                       "สมมติปริมาตรรวมเป็นผลบวกของปริมาตรสารละลาย "
                       "ความเข้มข้น Na⁺ สุดท้ายเป็นกี่ mol/L")],
            correct=[text(fmt(answer))],
            distractors=fixed(
                [text(named("chem.posn2561_counted_one_sodium_per_phosphate",
                            fmt((2 * sulfate + phosphate) / (sv + pv))))],
                [text(named("chem.posn2561_omitted_sulfate_sodium",
                            fmt(3 * phosphate / (sv + pv))))],
                [text(named("chem.posn2561_reported_sodium_moles_as_molarity",
                            fmt(sodium / 1000)))],
            ),
            topic="ความเข้มข้นไอออนหลังผสมสารละลาย",
            hint=[text("Na₂SO₄ ให้ Na⁺ สองโมล และ Na₃PO₄ ให้ Na⁺ สามโมลต่อโมลเกลือ; หารด้วยปริมาตรรวม")],
        )
