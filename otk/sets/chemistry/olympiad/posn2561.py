"""Reviewed waves of POSN camp-selection chemistry 2561."""

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2561_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18,
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
