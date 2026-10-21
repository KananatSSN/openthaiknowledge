"""Reviewed waves of POSN camp-selection chemistry 2561."""

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2561_chemistry import q01, q02, q03, q04, q05, q06


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
