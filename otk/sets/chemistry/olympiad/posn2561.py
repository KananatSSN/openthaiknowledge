"""Reviewed waves of POSN camp-selection chemistry 2561."""

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sheets.posn2561_chemistry import q01, q02, q03


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
