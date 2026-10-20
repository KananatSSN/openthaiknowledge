"""Reviewed waves of POSN camp-selection chemistry 2560."""

import re

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.posn2560_chemistry import (
    q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12,
    q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24,
    q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36,
)

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


class ChemistrySheet(WordProblem):
    sheet_id = "posn2560_chemistry"
    sheet = "สอวน. ค่าย 1 เคมี (2560)"


@question_type(
    "chem.posn2560_q01", display_name={"th": "มวลรังสีบวกและรังสีแคโทด"},
    level=LEVEL, subject="เคมี", topic="รังสีแคโทดและรังสีบวก",
)
class CanalRayMass(ChemistrySheet):
    def expr(self, rng):
        isotope, nucleons = rng.choice((("H-1", 1), ("H-2", 2), ("He-4", 4), ("Ne-20", 20)))
        answer = q01.solve(nucleons=nucleons)
        return MathDraw(
            "", str(answer),
            prompt=(
                f"ในหลอดรังสีแคโทด อนุภาคบวก X เป็นไอออนของ {isotope} "
                "และอนุภาค Y เป็นอิเล็กตรอน สมมติให้มวลของไอออนเท่ากับจำนวน "
                "นิวคลีออนคูณมวลนิวคลีออน และมวลนิวคลีออนเป็น 1836 เท่าของมวลอิเล็กตรอน "
                "มวลของ X เป็นกี่เท่าของมวล Y"
            ),
            hint=r"m_X/m_Y=A(m_{\rm nucleon}/m_e)",
            distractors=[
                named("chem.used_nucleon_count_only", str(nucleons)),
                named("chem.added_mass_factors", str(nucleons + 1836)),
                named("chem.included_extra_nucleon", str((nucleons + 1) * 1836)),
            ],
        )


@question_type(
    "chem.posn2560_q02", display_name={"th": "ข้อสันนิษฐานเลขออกซิเดชันของแฮโลเจน"},
    level=LEVEL, subject="เคมี", topic="หมู่ธาตุและเลขออกซิเดชัน",
)
class HalogenOxidationClaims(ChemistrySheet):
    def expr(self, rng):
        symbol, states = rng.choice((
            ("Ts", (-1, 1, 3, 5)),
            ("Cl", (-1, 1, 3, 5, 7)),
            ("Br", (-1, 1, 3, 5, 7)),
            ("I", (-1, 1, 3, 5, 7)),
        ))
        answer = q02.solve(states=states)
        assert answer == "only_minus_one"
        return MathDraw(
            "", r"S=\{-1\}",
            prompt=(
                f"แบบจำลองของธาตุ {symbol} หมู่ 17 ให้ชุดเลขออกซิเดชันที่เป็นไปได้ "
                f"S = {{{', '.join(f'{s:+d}' if s > 0 else str(s) for s in states)}}} "
                "และอิเล็กตรอนชั้นนอกเป็น p⁵ ข้อความใดขัดกับแบบจำลองนี้"
            ),
            hint="ตรวจสมาชิกของ S ก่อนสรุปว่ามีเลขออกซิเดชันเพียงค่าเดียว",
            distractors=[
                named("chem.confused_member_with_only_state", r"-1\in S"),
                named("chem.ignored_positive_oxidation", r"+1\in S"),
                named("chem.miscounted_unpaired_p", r"n_{\rm unpaired}=1"),
            ],
        )


@question_type(
    "chem.posn2560_q03", display_name={"th": "จำนวนเส้นสเปกตรัมไฮโดรเจน"},
    level=LEVEL, subject="เคมี", topic="สเปกตรัมของอะตอม",
)
class HydrogenLines(ChemistrySheet):
    def expr(self, rng):
        upper = rng.randint(3, 8)
        answer = q03.solve(upper=upper)
        return MathDraw(
            "", str(answer),
            prompt=(
                f"กระตุ้นอะตอมไฮโดรเจนจำนวนมากให้อิเล็กตรอนอยู่ที่ระดับ n = {upper} "
                "แล้วปล่อยให้คายพลังงานผ่านระดับใดก็ได้จนกลับสู่สถานะพื้น "
                "จะพบเส้นสเปกตรัมเปล่งออกที่มีความยาวคลื่นต่างกันได้มากที่สุดกี่เส้น"
            ),
            hint=r"N=\binom{n}{2}=\frac{n(n-1)}{2}",
            distractors=[
                named("chem.only_ground_transitions", str(upper - 1)),
                named("chem.counted_upward_transitions", str(2 * answer)),
                named("chem.included_extra_level", str(upper * (upper + 1) // 2)),
            ],
        )


def _nucleus(atomic, mass):
    return rf"{{}}^{{{mass}}}_{{{atomic}}}\mathrm{{X}}"


@question_type(
    "chem.posn2560_q04", display_name={"th": "สัญลักษณ์นิวเคลียร์จากข้อมูลไอโซโทป"},
    level=LEVEL, subject="เคมี", topic="ไอโซโทปและไอออน",
)
class IsotopeNotation(ChemistrySheet):
    def expr(self, rng):
        electrons = rng.choice((10, 18))
        charge = rng.choice((1, 2, 3))
        neutrons = electrons + rng.randint(4, 10)
        fewer = rng.randint(2, 5)
        atomic, mass = q04.solve(electrons=electrons, charge=charge,
                                 neutrons=neutrons, fewer=fewer)
        return MathDraw(
            "", _nucleus(atomic, mass),
            prompt=(
                f"ไอโซโทป X และ Y เป็นธาตุเดียวกัน โดย X มีนิวตรอนน้อยกว่า Y {fewer} อนุภาค "
                f"ไอออนของ Y ที่มีประจุ +{charge} มีอิเล็กตรอน {electrons} อนุภาค "
                f"และนิวตรอน {neutrons} อนุภาค สัญลักษณ์นิวเคลียร์ของอะตอม X ข้อใดถูกต้อง"
            ),
            hint=r"Z=e+q,\quad A_X=Z+N_Y-\Delta N",
            distractors=[
                named("chem.ignored_ion_charge", _nucleus(electrons, electrons + neutrons - fewer)),
                named("chem.reversed_ion_charge", _nucleus(electrons - charge, mass - 2 * charge)),
                named("chem.kept_other_isotope_neutrons", _nucleus(atomic, mass + fewer)),
            ],
        )


@question_type(
    "chem.posn2560_q05", display_name={"th": "ขนาดไอออนจากจำนวนชั้นอิเล็กตรอน"},
    level=LEVEL, subject="เคมี", topic="แนวโน้มขนาดไอออน",
)
class IonicShellRadius(ChemistrySheet):
    def expr(self, rng):
        first, second = rng.choice((
            (("Mg", 12, 2), ("P", 15, -3)),
            (("P", 15, -3), ("Mg", 12, 2)),
            (("Na", 11, 1), ("Cl", 17, -1)),
            (("Ca", 20, 2), ("As", 33, -3)),
        ))
        answer = q05.solve(first_atomic=first[1], first_charge=first[2],
                           second_atomic=second[1], second_charge=second[2])
        smaller = "A" if answer == "first" else "B"
        larger = "B" if answer == "first" else "A"
        return MathDraw(
            "", rf"r_{{{smaller}}}<r_{{{larger}}}",
            prompt=(
                f"ให้ A = {first[0]} ({first[1]}) ที่มีประจุ {first[2]:+d} และ "
                f"B = {second[0]} ({second[1]}) ที่มีประจุ {second[2]:+d} "
                "เลขในวงเล็บคือเลขอะตอม เมื่อไอออนทั้งสองมีจำนวนชั้นอิเล็กตรอน "
                "ที่ครองอยู่ต่างกัน ความสัมพันธ์ของรัศมีไอออนข้อใดถูกต้อง"
            ),
            hint="หาจำนวนอิเล็กตรอนของไอออนก่อน แล้วดูชั้นนอกสุดที่ครองอยู่",
            distractors=[
                named("chem.reversed_ionic_shell_order", rf"r_{{{smaller}}}>r_{{{larger}}}"),
                named("chem.assumed_equal_ionic_radii", r"r_A=r_B"),
                named("chem.assumed_ionic_radius_unknown", r"\text{insufficient data}"),
            ],
        )


@question_type(
    "chem.posn2560_q06", display_name={"th": "อิเล็กตรอน 3d ของไอออนในออกไซด์"},
    level=LEVEL, subject="เคมี", topic="การจัดเรียงอิเล็กตรอนของไอออน",
)
class OxideDElectrons(ChemistrySheet):
    def expr(self, rng):
        symbol, atomic = rng.choice((("Mn", 25), ("Fe", 26), ("Co", 27), ("Ni", 28)))
        charge = rng.choice((2, 3))
        metal_count, oxygen_count = (1, 1) if charge == 2 else (2, 3)
        formula = f"{symbol}O" if charge == 2 else f"{symbol}₂O₃"
        answer = q06.solve(atomic=atomic, metal_count=metal_count, oxygen_count=oxygen_count)
        return MathDraw(
            "", str(answer),
            prompt=(
                f"ธาตุ {symbol} มีเลขอะตอม {atomic} และอะตอมเป็นกลางมีการจัดเรียงอิเล็กตรอน "
                f"[Ar]3d^{atomic - 20}4s² ในสารประกอบ {formula} กำหนดให้ออกซิเจนมีเลขออกซิเดชัน −2 "
                f"ไอออนของ {symbol} มีการจัดเรียงเป็น [Ar]3d^k โดย k มีค่าเท่าใด"
            ),
            hint=r"q_M=\frac{2b}{a}\;(M_aO_b),\quad 4s\text{ removed before }3d",
            distractors=[
                named("chem.removed_3d_before_4s", str(answer - 2)),
                named("chem.added_electrons_for_cation", str(atomic - 18 + charge)),
                named("chem.assumed_monovalent_metal", str(atomic - 19)),
            ],
        )


def _species_tex(symbol, charge):
    suffix = "" if charge == 0 else ("+" if charge == 1 else f"{charge}+")
    return rf"\mathrm{{{symbol}}}^{{{suffix}}}" if suffix else rf"\mathrm{{{symbol}}}"


def _pair_tex(pair):
    return rf"({_species_tex(*pair[0])},\,{_species_tex(*pair[1])})"


@question_type(
    "chem.posn2560_q07", display_name={"th": "จำนวนอิเล็กตรอนเดี่ยวของอะตอมและไอออน"},
    level=LEVEL, subject="เคมี", topic="อิเล็กตรอนเดี่ยวและกฎของฮุนด์",
)
class UnpairedIonPair(ChemistrySheet):
    def expr(self, rng):
        correct = rng.choice((
            (("Cr", 1), ("Mn", 2)),
            (("Mn", 2), ("Fe", 3)),
            (("As", 0), ("Cr", 3)),
            (("Cu", 2), ("Cu", 0)),
        ))
        wrong = (
            ((("As", 0), ("Mn", 2)), "chem.confused_p3_with_d5"),
            ((("Cu", 2), ("Cr", 3)), "chem.assumed_d_ions_same_spin"),
            ((("As", 3), ("Cu", 0)), "chem.ignored_p_electron_loss"),
        )
        assert q07.solve(first_symbol=correct[0][0], first_charge=correct[0][1],
                         second_symbol=correct[1][0], second_charge=correct[1][1])
        return MathDraw(
            "", _pair_tex(correct),
            prompt="อะตอมหรือไอออนคู่ใดมีจำนวนอิเล็กตรอนเดี่ยวในสถานะพื้นเท่ากัน (พิจารณาอนุภาคอิสระ)",
            hint="ไอออนโลหะทรานซิชันนำอิเล็กตรอน 4s ออกก่อน 3d; ใช้กฎของฮุนด์นับอิเล็กตรอนเดี่ยว",
            distractors=[named(mistake, _pair_tex(pair)) for pair, mistake in wrong],
        )


@question_type(
    "chem.posn2560_q08", display_name={"th": "ไอออนของโลหะหมู่ 2 กับแก๊สมีตระกูล"},
    level=LEVEL, subject="เคมี", topic="สารประกอบไอออนิกและแก๊สมีตระกูล",
)
class DichlorideNobleGas(ChemistrySheet):
    def expr(self, rng):
        symbol, atomic = rng.choice((("Mg", 12), ("Ca", 20), ("Sr", 38), ("Ba", 56)))
        answer = q08.solve(atomic=atomic)
        gases = ("Ne", "Ar", "Kr", "Xe")
        index = gases.index(answer)
        wrong = [gas for gas in gases if gas != answer]
        return MathDraw(
            "", rf"\mathrm{{{answer}}}",
            prompt=(
                f"สารประกอบ {symbol}Cl₂ เป็นของแข็งไอออนิก; ธาตุ {symbol} มีเลขอะตอม {atomic} "
                "เมื่อละลายน้ำได้ไอออนประจุ +2 ไอออนนี้มีจำนวนอิเล็กตรอนเท่ากับแก๊สมีตระกูลใด"
            ),
            hint="นับอิเล็กตรอนของไอออน +2 โดยนำออกสองตัวจากอะตอมเป็นกลาง",
            distractors=[
                named("chem.ignored_cation_electron_loss" if gases.index(gas) > index
                      else "chem.removed_extra_shell", rf"\mathrm{{{gas}}}")
                for gas in wrong
            ],
        )


def _oxidation_triplet(values):
    return "(" + ",".join(f"+{value}" if value > 0 else str(value) for value in values) + ")"


@question_type(
    "chem.posn2560_q09", display_name={"th": "เลขออกซิเดชันในออกซีแอนไอออนและไซยาโนคอมเพล็กซ์"},
    level=LEVEL, subject="เคมี", topic="การหาเลขออกซิเดชัน",
)
class ThreeOxidationStates(ChemistrySheet):
    def expr(self, rng):
        first_formula, first_element, oxygen, oxo_charge = rng.choice((
            ("[Co(NH₃)₄SO₄]Cl", "S", 4, -2),
            ("NaNO₃", "N", 3, -1),
            ("Na₃PO₄", "P", 4, -3),
        ))
        acid_formula, acid_element, acid_oxygen = rng.choice((
            ("HClO₄", "Cl", 4), ("HClO₃", "Cl", 3), ("HBrO₃", "Br", 3),
        ))
        complex_formula, metal, cyanides, complex_charge = rng.choice((
            ("Na[Au(CN)₂]", "Au", 2, -1),
            ("K₃[Co(CN)₆]", "Co", 6, -3),
            ("K₂[Pt(CN)₄]", "Pt", 4, -2),
        ))
        answer = q09.solve(oxo_oxygen=oxygen, oxo_charge=oxo_charge,
                           acid_oxygen=acid_oxygen, cyanide_count=cyanides,
                           complex_charge=complex_charge)
        return MathDraw(
            "", _oxidation_triplet(answer),
            prompt=(
                f"จงหาเลขออกซิเดชันของ {first_element} ใน {first_formula}, "
                f"{acid_element} ใน {acid_formula} และ {metal} ใน {complex_formula} "
                "ตามลำดับ (NH₃ เป็นลิแกนด์เป็นกลาง, CN⁻ มีประจุ −1)"
            ),
            hint="ผลรวมเลขออกซิเดชันในแต่ละไอออนเท่ากับประจุของไอออน; O = −2 และ H = +1",
            distractors=[
                named("chem.used_oxoanion_charge_as_central_state",
                      _oxidation_triplet((oxo_charge, answer[1], answer[2]))),
                named("chem.ignored_acid_hydrogen",
                      _oxidation_triplet((answer[0], answer[1] + 1, answer[2]))),
                named("chem.ignored_complex_charge",
                      _oxidation_triplet((answer[0], answer[1], cyanides))),
            ],
        )


def _orbital_box(electrons):
    return r"\boxed{" + r"\uparrow" * min(electrons, 1) + r"\downarrow" * (electrons == 2) + "}"


def _orbital_diagram(pattern):
    s, p = pattern
    return (r"1s:" + _orbital_box(2) + r",\;2s:" + _orbital_box(s)
            + r",\;2p:" + "".join(_orbital_box(count) for count in p))


@question_type(
    "chem.posn2560_q10", display_name={"th": "แผนภาพออร์บิทัลกับกฎของฮุนด์"},
    level=LEVEL, subject="เคมี", topic="การบรรจุอิเล็กตรอนในออร์บิทัล",
)
class HundOrbitalDiagram(ChemistrySheet):
    def expr(self, rng):
        invalid = rng.choice(((2, (2, 1, 0)), (2, (2, 0, 0)), (2, (2, 2, 0))))
        valid = ((2, (1, 1, 1)), (1, (2, 1, 1)), (2, (2, 1, 1)))
        patterns = [*valid, invalid]
        rng.shuffle(patterns)
        answer = q10.solve(patterns=tuple(patterns))
        mistake = {
            valid[0]: "chem.thought_parallel_p_singles_invalid",
            valid[1]: "chem.confused_excitation_with_hund",
            valid[2]: "chem.thought_p4_pairing_invalid",
        }
        return MathDraw(
            "", _orbital_diagram(patterns[answer]),
            prompt="แผนภาพใดไม่เป็นไปตามกฎของฮุนด์ในการบรรจุอิเล็กตรอน 2p (พิจารณาแต่ละอะตอมแยกกัน)",
            hint="ออร์บิทัล 2p ทั้งสามต้องครองเดี่ยวก่อนจึงจับคู่",
            distractors=[named(mistake[pattern], _orbital_diagram(pattern))
                         for i, pattern in enumerate(patterns) if i != answer],
        )


def _rank_tex(rankings):
    radius, ionization = rankings
    return (r"r:" + ">".join(radius) + r",\quad I_1:"
            + ">".join(ionization))


@question_type(
    "chem.posn2560_q11", display_name={"th": "ลำดับขนาดอะตอมและพลังงานไอออไนเซชัน"},
    level=LEVEL, subject="เคมี", topic="แนวโน้มรัศมีอะตอมและพลังงานไอออไนเซชัน",
)
class RadiusAndIonizationOrder(ChemistrySheet):
    def expr(self, rng):
        elements = list(("O", "P", "Ga", "As"))
        rng.shuffle(elements)
        radius, ionization = q11.solve(elements=tuple(elements))
        choices = (
            ((radius[1], radius[0], *radius[2:]), ionization),
            (radius, (ionization[2], ionization[1], ionization[0], ionization[3])),
            (radius, tuple(reversed(ionization))),
        )
        labels = "ADEG"
        assignment = ", ".join(f"{label}={symbol}" for label, symbol in zip(labels, elements))
        return MathDraw(
            "", _rank_tex((radius, ionization)),
            prompt=(
                f"กำหนด {assignment} โดยอะตอมทั้งหมดอยู่ในสถานะพื้น "
                "ข้อใดเรียงรัศมีอะตอมเชิงประจักษ์ r และพลังงานไอออไนเซชันลำดับที่ 1 "
                "I₁ จากมากไปน้อยได้ถูกต้องทั้งสองลำดับ"
            ),
            hint="ตรวจลำดับในคาบและหมู่แยกสำหรับรัศมีและพลังงานไอออไนเซชัน",
            distractors=[
                named("chem.reversed_ga_as_radius", _rank_tex(choices[0])),
                named("chem.put_as_above_o_ionization", _rank_tex(choices[1])),
                named("chem.reversed_ionization_order", _rank_tex(choices[2])),
            ],
        )


def _position_tuple(values):
    return "(" + ",".join(map(str, values)) + ")"


@question_type(
    "chem.posn2560_q12", display_name={"th": "หมู่และคาบของไอออนที่ไอโซอิเล็กทรอนิก"},
    level=LEVEL, subject="เคมี", topic="ไอออนไอโซอิเล็กทรอนิกและตารางธาตุ",
)
class IsoelectronicIonPositions(ChemistrySheet):
    def expr(self, rng):
        gas, electrons = rng.choice((("Ne", 10), ("Ar", 18), ("Kr", 36), ("Xe", 54)))
        group_x, period_x, group_y, period_y = q12.solve(noble_electrons=electrons)
        return MathDraw(
            "", _position_tuple((group_x, period_x, group_y, period_y)),
            prompt=(
                f"ไอออน X²⁺ และ Y⁻ มีอิเล็กตรอนเท่ากับแก๊สมีตระกูล {gas} "
                "จงระบุ (หมู่ X, คาบ X, หมู่ Y, คาบ Y) โดยใช้เลขหมู่หลักแบบเดิม 1–8"
            ),
            hint="หาเลขอะตอมของ X และ Y จากจำนวนอิเล็กตรอนของไอออนก่อน",
            distractors=[
                named("chem.swapped_group_and_period", _position_tuple(
                    (period_x, group_x, group_y, period_y))),
                named("chem.put_halogen_in_next_period", _position_tuple(
                    (group_x, period_x, group_y, period_x))),
                named("chem.treated_anion_as_group_two", _position_tuple(
                    (group_x, period_x, group_x, period_y))),
            ],
        )


def _oxide_pair(pair):
    return r"\mathrm{" + r"},\;\mathrm{".join(pair) + "}"


@question_type(
    "chem.posn2560_q13", display_name={"th": "ออกไซด์ที่ทำให้น้ำเป็นกรด"},
    level=LEVEL, subject="เคมี", topic="สมบัติกรดเบสของออกไซด์",
)
class AcidicOxides(ChemistrySheet):
    def expr(self, rng):
        oxides = rng.choice((q13.PARAMS, *q13.VARIANTS))["oxides"]
        acids = q13.solve(oxides=oxides)
        others = [oxide for oxide in oxides if oxide not in acids]
        amphoteric = next(oxide for oxide in others if oxide in ("Cr2O3", "Al2O3"))
        basic = next(oxide for oxide in others if oxide in ("Na2O", "K2O"))
        wrong = (
            (tuple(sorted((acids[0], amphoteric))), "chem.confused_amphoteric_oxide_with_acid"),
            (tuple(sorted((acids[1], basic))), "chem.confused_basic_oxide_with_acid"),
            (tuple(sorted(others)), "chem.ignored_nonmetal_acid_anhydrides"),
        )
        return MathDraw(
            "", _oxide_pair(acids),
            prompt=("ออกไซด์คู่ใดเมื่อลงน้ำแล้วให้สารละลายที่เปลี่ยนกระดาษลิตมัส"
                    "จากน้ำเงินเป็นแดง: " + ", ".join(oxides)),
            hint="พิจารณาว่าออกไซด์ใดเป็นแอนไฮไดรด์ของกรด และตัวใดเป็นเบสหรือแอมโฟเทอริก",
            distractors=[named(mistake, _oxide_pair(pair)) for pair, mistake in wrong],
        )


def _salt_list(formulas):
    return r",\;".join(r"\mathrm{" + formula + "}" for formula in sorted(formulas))


@question_type(
    "chem.posn2560_q14", display_name={"th": "ตะกอนจากส่วนผสมของไอออน"},
    level=LEVEL, subject="เคมี", topic="การละลายและการเกิดตะกอน",
)
class MixedIonPrecipitates(ChemistrySheet):
    def expr(self, rng):
        params = rng.choice((q14.PARAMS, *q14.VARIANTS))
        cations, anions = params["cations"], params["anions"]
        answer = q14.solve(**params)
        alkali = next(c for c in cations if c in ("Na", "K"))
        spectator = next(a for a in anions if a in ("Cl", "NO3"))
        spectator_salts = (("BaCl2", "MgCl2") if spectator == "Cl"
                           else ("Ba(NO3)2", "Mg(NO3)2"))
        sulfate = f"{alkali}2SO4"
        wrong = (
            (("BaSO4", "MgSO4", "MgHPO4"), "chem.assumed_magnesium_sulfate_precipitates"),
            (("BaSO4", f"{alkali}2HPO4", "MgHPO4"),
             "chem.assumed_alkali_hydrogen_phosphate_precipitates"),
            ((*spectator_salts, sulfate),
             "chem.selected_soluble_spectator_salts"),
        )
        return MathDraw(
            "", _salt_list(answer),
            prompt=("ผสมสารละลายที่มีไอออน " + ", ".join(
                f"{cation}{'⁺' if cation in ('Na', 'K') else '²⁺'}" for cation in cations)
                + " และ " + ", ".join(
                    f"{anion}{'⁻' if anion in ('Cl', 'NO3') else '²⁻'}" for anion in anions)
                + " เข้าด้วยกัน ภายใต้สมมติฐานกฎการละลายทั่วไป ข้อใดระบุสารที่ตกตะกอนทั้งหมด"),
            hint="เกลือหมู่ 1 และไนเตรตละลายได้; เทียบซัลเฟตกับไฮโดรเจนฟอสเฟตของ Ba และ Mg",
            distractors=[named(mistake, _salt_list(salts)) for salts, mistake in wrong],
        )


def _label_order(labels):
    return ">".join(labels)


@question_type(
    "chem.posn2560_q15", display_name={"th": "สีของแฮโลเจนและลำดับอิเล็กโทรเนกาติวิตี"},
    level=LEVEL, subject="เคมี", topic="ปฏิกิริยาแทนที่ของแฮโลเจน",
)
class HalogenDisplacementOrder(ChemistrySheet):
    def expr(self, rng):
        assignment = rng.choice((q15.PARAMS, *q15.VARIANTS))["assignment"]
        labels = {symbol: "XYZ"[i] for i, symbol in enumerate(assignment)}
        answer = q15.solve(assignment=assignment)
        wrong = (
            ((labels["Br"], labels["Cl"], labels["I"]), "chem.put_bromine_above_chlorine"),
            ((labels["I"], labels["Br"], labels["Cl"]), "chem.reversed_halogen_group_trend"),
            ((labels["Cl"], labels["I"], labels["Br"]), "chem.put_iodine_above_bromine"),
        )
        return MathDraw(
            "", _label_order(answer),
            prompt=(
                "X, Y, Z เป็นธาตุแฮโลเจนสามชนิดที่ต่างกันในชุด Cl, Br, I "
                f"สารละลาย {labels['Br']}₂ ใน CCl₄ มีสีส้ม; เมื่อนำไปเขย่ากับสารละลาย "
                f"K{labels['I']} ชั้น CCl₄ เปลี่ยนเป็นสีม่วง จงเรียงค่าอิเล็กโทรเนกาติวิตี"
                "ของ X, Y, Z จากมากไปน้อย"
            ),
            hint="สีส้มระบุ Br₂; สีม่วงหลังแทนที่ระบุ I₂ แล้วใช้แนวโน้มในหมู่ 17",
            distractors=[named(mistake, _label_order(order)) for order, mistake in wrong],
        )


def _nuclear_triplet(first, second, product):
    mass, atomic = product
    return (rf"(\mathrm{{{first}}},\;\mathrm{{{second}}},\;"
            rf"{{}}^{{{mass}}}_{{{atomic}}}\mathrm{{Ra}})")


@question_type(
    "chem.posn2560_q16", display_name={"th": "อนุรักษ์เลขมวลในสมการนิวเคลียร์"},
    level=LEVEL, subject="เคมี", topic="สมการปฏิกิริยานิวเคลียร์",
)
class NuclearReactionBalance(ChemistrySheet):
    def expr(self, rng):
        params = rng.choice((q16.PARAMS, *q16.VARIANTS))
        first, second, product = q16.solve(**params)
        return MathDraw(
            "", _nuclear_triplet(first, second, product),
            prompt=(
                "กำหนดเลขอะตอม Co=27, Mn=25, Te=52, I=53 และ Rn=86 "
                f"สมการ Co-{params['co_mass']} + A → Mn-{params['mn_mass']} + α; "
                f"Te-{params['te_mass']} + B → I-{params['iodine_mass']} + 2n; "
                f"Rn-{params['rn_mass']} + α → C + γ "
                "โดย n คือนิวตรอน, p คือโปรตอน, d คือดิวทีรอน, α คืออนุภาคแอลฟา "
                "จงระบุ A, B และ C ตามลำดับ"
            ),
            hint="เลขมวล A และเลขอะตอม Z ต้องอนุรักษ์แยกกัน; γ ไม่มีทั้ง A และ Z",
            distractors=[
                named("chem.confused_neutron_with_proton",
                      _nuclear_triplet("p", second, product)),
                named("chem.confused_deuteron_with_proton",
                      _nuclear_triplet(first, "p", product)),
                named("chem.failed_alpha_mass_balance",
                      _nuclear_triplet(first, second, (product[0] - 2, product[1]))),
            ],
        )


def _valence_pair(halogen, counts):
    return (rf"n_v(\mathrm{{H}})={counts[0]},\;"
            rf"n_v(\mathrm{{{halogen}}})={counts[1]}")


@question_type(
    "chem.posn2560_q17", display_name={"th": "เวเลนซ์อิเล็กตรอนของไฮโดรเจนและแฮโลเจน"},
    level=LEVEL, subject="เคมี", topic="เวเลนซ์อิเล็กตรอนและหมู่ธาตุ",
)
class HydrogenHalogenValence(ChemistrySheet):
    def expr(self, rng):
        halogen = rng.choice((q17.PARAMS, *q17.VARIANTS))["halogen"]
        answer = q17.solve(halogen=halogen)
        return MathDraw(
            "", _valence_pair(halogen, answer),
            prompt=(f"ไฮโดรเจน H และแฮโลเจน {halogen} มีจำนวนอิเล็กตรอนเวเลนซ์"
                    "ตามลำดับเท่าใด"),
            hint="นับอิเล็กตรอนในชั้นพลังงานนอกสุดของอะตอมเป็นกลาง",
            distractors=[
                named("chem.assumed_halogen_one_valence_electron",
                      _valence_pair(halogen, (1, 1))),
                named("chem.swapped_hydrogen_halogen_valence",
                      _valence_pair(halogen, (7, 1))),
                named("chem.confused_hydrogen_duet_with_valence",
                      _valence_pair(halogen, (2, 7))),
            ],
        )


def _halide_order(molecules):
    return "<".join(rf"\mathrm{{{molecule}}}" for molecule in molecules)


@question_type(
    "chem.posn2560_q18", display_name={"th": "ลำดับจุดเดือดของไฮโดรเจนเฮไลด์"},
    level=LEVEL, subject="เคมี", topic="แรงยึดเหนี่ยวระหว่างโมเลกุล",
)
class HydrogenHalideBoilingOrder(ChemistrySheet):
    def expr(self, rng):
        molecules = rng.choice((q18.PARAMS, *q18.VARIANTS))["molecules"]
        answer = q18.solve(molecules=molecules)
        if "HF" in molecules:
            first_wrong = tuple(m for m in ("HF", "HCl", "HBr", "HI") if m in molecules)
            first_mistake = "chem.ignored_hf_hydrogen_bonding"
        else:
            first_wrong = (answer[1], answer[0], *answer[2:])
            first_mistake = "chem.reversed_hcl_hbr_boiling_order"
        return MathDraw(
            "", _halide_order(answer),
            prompt=("เรียงจุดเดือดปกติของ " + ", ".join(molecules)
                    + " จากต่ำไปสูง ข้อใดถูกต้อง"),
            hint="HCl, HBr, HI สูงขึ้นตามแรงลอนดอน; HF มีพันธะไฮโดรเจนเด่น",
            distractors=[
                named(first_mistake, _halide_order(first_wrong)),
                named("chem.reversed_halide_boiling_order",
                      _halide_order(tuple(reversed(answer)))),
                named("chem.swapped_two_highest_halide_boiling_points",
                      _halide_order((*answer[:-2], answer[-1], answer[-2]))),
            ],
        )


_ION_TEX = {
    "Pb": r"\mathrm{Pb}", "Ba": r"\mathrm{Ba}",
    "Ag": r"\mathrm{Ag}", "Ca": r"\mathrm{Ca}",
    "SO4": r"\mathrm{SO_4}", "Cl": r"\mathrm{Cl}",
    "CO3": r"\mathrm{CO_3}", "K": r"\mathrm{K}",
    "Na": r"\mathrm{Na}", "NO3": r"\mathrm{NO_3}",
}
_PRECIPITATE_TEX = {
    "PbSO4": r"\mathrm{PbSO_4}", "BaSO4": r"\mathrm{BaSO_4}",
    "AgCl": r"\mathrm{AgCl}", "CaCO3": r"\mathrm{CaCO_3}",
    "KNO3": r"\mathrm{KNO_3}", "NaNO3": r"\mathrm{NaNO_3}",
    "NaCl": r"\mathrm{NaCl}",
}
_MIXTURES = {
    ("Pb", "SO4"): ("Pb(NO₃)₂", "K₂SO₄", "K", "NO3", "KNO3"),
    ("Ba", "SO4"): ("BaCl₂", "Na₂SO₄", "Na", "Cl", "NaCl"),
    ("Ag", "Cl"): ("AgNO₃", "NaCl", "Na", "NO3", "NaNO3"),
    ("Ca", "CO3"): ("CaCl₂", "Na₂CO₃", "Na", "Cl", "NaCl"),
}


def _ion_tex(symbol, charge, state="aq"):
    sign = "+" if charge > 0 else "-"
    magnitude = "" if abs(charge) == 1 else str(abs(charge))
    return rf"{_ION_TEX[symbol]}^{{{magnitude}{sign}}}_{{({state})}}"


def _net_ionic(metal, metal_charge, anion, anion_charge, product, state="s"):
    return (f"{_ion_tex(metal, metal_charge)}+{_ion_tex(anion, -anion_charge)}"
            rf"\rightarrow {_PRECIPITATE_TEX[product]}_{{({state})}}")


@question_type(
    "chem.posn2560_q19", display_name={"th": "สมการไอออนิกสุทธิของตะกอน"},
    level=LEVEL, subject="เคมี", topic="สมการไอออนิกสุทธิ",
)
class NetIonicPrecipitation(ChemistrySheet):
    def expr(self, rng):
        params = rng.choice((q19.PARAMS, *q19.VARIANTS))
        metal, anion = params["metal"], params["anion"]
        positive, negative, product = q19.solve(**params)
        first, second, spectator_positive, spectator_negative, spectator_salt = _MIXTURES[(metal, anion)]
        spectator_tex = (f"{_ion_tex(spectator_positive, 1)}+"
                         f"{_ion_tex(spectator_negative, -1)}"
                         rf"\rightarrow {_PRECIPITATE_TEX[spectator_salt]}_{{(s)}}")
        wrong_charge = 1 if positive == 2 else 2
        return MathDraw(
            "", _net_ionic(metal, positive, anion, negative, product),
            prompt=(f"ผสมสารละลาย {first} กับ {second} แล้วเกิดตะกอน "
                    "สมการไอออนิกสุทธิข้อใดถูกต้อง"),
            hint="แยกเกลือที่ละลายได้เป็นไอออน แล้วตัดไอออนผู้ชมทั้งสองข้าง",
            distractors=[
                named("chem.precipitated_spectator_salt", spectator_tex),
                named("chem.misassigned_metal_ion_charge",
                      _net_ionic(metal, wrong_charge, anion, negative, product)),
                named("chem.kept_precipitate_aqueous",
                      _net_ionic(metal, positive, anion, negative, product, "aq")),
            ],
        )


_CONDUCTIVITY_ROWS = (
    (1455, 2837, "นำ", "นำ", "ไม่ละลาย"),
    (-56, -28, "ไม่นำ", "ไม่นำ", "ไม่นำ"),
    (685, 1324, "ไม่นำ", "นำ", "นำ"),
    (-51, -35, "ไม่นำ", "ไม่นำ", "นำ"),
    (-89, 118, "ไม่นำ", "ไม่นำ", "ไม่นำ"),
)


def _type_triplet(labels):
    return "(" + ",".join(labels) + ")"


@question_type(
    "chem.posn2560_q20", display_name={"th": "จำแนกสารจากการนำไฟฟ้า"},
    level=LEVEL, subject="เคมี", topic="สมบัติของสารไอออนิก โคเวเลนต์ และโลหะ",
)
class ConductivitySubstanceTypes(ChemistrySheet):
    def expr(self, rng):
        labels = rng.choice((q20.PARAMS, *q20.VARIANTS))["labels"]
        ionic, ionizing, metal = q20.solve(labels=labels)
        rows = "; ".join(
            f"{label}=({mp},{bp};{solid}/{liquid}/{water})"
            for label, (mp, bp, solid, liquid, water) in zip(labels, _CONDUCTIVITY_ROWS)
        )
        return MathDraw(
            "", _type_triplet((ionic, ionizing, metal)),
            prompt=("ข้อมูลแต่ละสารเป็น (จุดหลอมเหลว°C, จุดเดือด°C; การนำไฟฟ้า"
                    "ของแข็ง/ของเหลว/สารละลายน้ำ): " + rows + " "
                    "จงระบุ (สารไอออนิก, สารโคเวเลนต์ที่สารละลายน้ำนำไฟฟ้า, โลหะ)"),
            hint="โลหะนำไฟฟ้าในของแข็ง; ไอออนิกนำเมื่อหลอม/ละลาย; โมเลกุลบางชนิดแตกตัวในน้ำ",
            distractors=[
                named("chem.swapped_ionic_and_metal_properties",
                      _type_triplet((metal, ionizing, ionic))),
                named("chem.ignored_aqueous_molecular_ionization",
                      _type_triplet((ionic, labels[1], metal))),
                named("chem.swapped_ionic_and_ionizing_molecular",
                      _type_triplet((ionizing, ionic, metal))),
            ],
        )


_NITROGEN_OXIDE_TEX = {
    "NO+": r"\mathrm{NO}^{+}", "NO": r"\mathrm{NO}",
    "NO2+": r"\mathrm{NO_2}^{+}", "NO2-": r"\mathrm{NO_2}^{-}",
    "NO3-": r"\mathrm{NO_3}^{-}",
}
_NITROGEN_OXIDE_TEXT = {
    "NO+": "NO⁺", "NO": "NO", "NO2+": "NO₂⁺",
    "NO2-": "NO₂⁻", "NO3-": "NO₃⁻",
}
_BOND_MISTAKES = {
    "NO": "chem.ignored_no_antibonding_electron",
    "NO2+": "chem.assumed_nitronium_shorter_than_nitrosonium",
    "NO2-": "chem.overstated_nitrite_bond_order",
    "NO3-": "chem.overstated_nitrate_bond_order",
}


@question_type(
    "chem.posn2560_q21", display_name={"th": "ไอออนที่มีพันธะไนโตรเจนออกซิเจนสั้นที่สุด"},
    level=LEVEL, subject="เคมี", topic="อันดับพันธะและความยาวพันธะ",
)
class NitrogenOxygenBondLength(ChemistrySheet):
    def expr(self, rng):
        species = rng.choice((q21.PARAMS, *q21.VARIANTS))["species"]
        answer = q21.solve(species=species)
        return MathDraw(
            "", _NITROGEN_OXIDE_TEX[answer],
            prompt=("ในบรรดาชนิดต่อไปนี้ " + ", ".join(
                _NITROGEN_OXIDE_TEXT[item] for item in species)
                + " ชนิดใดมีพันธะ N–O สั้นที่สุด"),
            hint="พันธะสั้นมักมีอันดับพันธะสูง; NO⁺ มีอันดับพันธะ 3",
            distractors=[named(_BOND_MISTAKES[item], _NITROGEN_OXIDE_TEX[item])
                         for item in species if item != answer],
        )


_VSEPR_TEX = {
    "BF4-": r"\mathrm{BF_4}^{-}", "POCl3": r"\mathrm{POCl_3}",
    "ICl4-": r"\mathrm{ICl_4}^{-}", "XeF4": r"\mathrm{XeF_4}",
    "TeCl4": r"\mathrm{TeCl_4}", "SF4": r"\mathrm{SF_4}",
    "NH3": r"\mathrm{NH_3}", "PCl3": r"\mathrm{PCl_3}",
}
_SHAPE_PAIR_MISTAKES = {
    ("BF4-", "ICl4-"): "chem.confused_tetrahedral_with_square_planar",
    ("TeCl4", "POCl3"): "chem.confused_seesaw_with_tetrahedral",
    ("ICl4-", "TeCl4"): "chem.confused_square_planar_with_seesaw",
}


def _shape_pair_tex(pair):
    return _VSEPR_TEX[pair[0]] + r",\;" + _VSEPR_TEX[pair[1]]


@question_type(
    "chem.posn2560_q22", display_name={"th": "คู่สารที่มีรูปร่างโมเลกุลเหมือนกัน"},
    level=LEVEL, subject="เคมี", topic="รูปร่างโมเลกุลตาม VSEPR",
)
class SameMolecularShape(ChemistrySheet):
    def expr(self, rng):
        pairs = rng.choice((q22.PARAMS, *q22.VARIANTS))["pairs"]
        answer = q22.solve(pairs=pairs)
        return MathDraw(
            "", _shape_pair_tex(answer),
            prompt="สารหรือไอออนคู่ใดมีรูปร่างการจัดเรียงอะตอมเหมือนกัน",
            hint="นับโดเมนพันธะและคู่โดดเดี่ยวบนอะตอมกลาง แล้วพิจารณารูปร่างของอะตอม",
            distractors=[named(_SHAPE_PAIR_MISTAKES[pair], _shape_pair_tex(pair))
                         for pair in pairs if pair != answer],
        )


_ANGLE_TEX = {
    "ClF3": r"\mathrm{ClF_3}", "ClF5": r"\mathrm{ClF_5}",
    "SiF4": r"\mathrm{SiF_4}", "NCl3": r"\mathrm{NCl_3}",
    "OCl2": r"\mathrm{OCl_2}", "BF3": r"\mathrm{BF_3}",
    "NH3": r"\mathrm{NH_3}", "H2O": r"\mathrm{H_2O}",
}
_ANGLE_TEXT = {
    "ClF3": "ClF₃", "ClF5": "ClF₅", "SiF4": "SiF₄",
    "NCl3": "NCl₃", "OCl2": "OCl₂", "BF3": "BF₃",
    "NH3": "NH₃", "H2O": "H₂O",
}
_ANGLE_MISTAKES = {
    "SiF4": "chem.assumed_tetrahedral_bond_angle_smallest",
    "NCl3": "chem.assumed_pyramidal_bond_angle_smallest",
    "OCl2": "chem.assumed_bent_bond_angle_smallest",
    "BF3": "chem.assumed_trigonal_bond_angle_smallest",
    "NH3": "chem.assumed_pyramidal_bond_angle_smallest",
    "H2O": "chem.assumed_bent_bond_angle_smallest",
}


@question_type(
    "chem.posn2560_q23", display_name={"th": "มุมพันธะที่เล็กที่สุด"},
    level=LEVEL, subject="เคมี", topic="มุมพันธะและรูปร่างโมเลกุล",
)
class SmallestBondAngle(ChemistrySheet):
    def expr(self, rng):
        molecules = rng.choice((q23.PARAMS, *q23.VARIANTS))["molecules"]
        answer = q23.solve(molecules=molecules)
        return MathDraw(
            "", _ANGLE_TEX[answer],
            prompt=("พิจารณามุมระหว่างพันธะที่เล็กที่สุดในแต่ละโมเลกุล: "
                    + ", ".join(_ANGLE_TEXT[molecule] for molecule in molecules)
                    + " โมเลกุลใดมีมุมดังกล่าวเล็กที่สุด"),
            hint="ClF₃ และ ClF₅ มีมุมติดกันต่ำกว่า 90° จากคู่โดดเดี่ยวของอะตอมกลาง",
            distractors=[named(_ANGLE_MISTAKES[molecule], _ANGLE_TEX[molecule])
                         for molecule in molecules if molecule != answer],
        )


_LONE_PAIR_TEX = {
    "NH3": r"\mathrm{NH_3}", "XeF2": r"\mathrm{XeF_2}",
    "NO2-": r"\mathrm{NO_2}^{-}", "SO3^2-": r"\mathrm{SO_3}^{2-}",
    "I3-": r"\mathrm{I_3}^{-}", "XeF4": r"\mathrm{XeF_4}",
    "ClF3": r"\mathrm{ClF_3}", "SF4": r"\mathrm{SF_4}",
}
_LONE_PAIR_TEXT = {
    "NH3": "NH₃", "XeF2": "XeF₂", "NO2-": "NO₂⁻",
    "SO3^2-": "SO₃²⁻", "I3-": "I₃⁻", "XeF4": "XeF₄",
    "ClF3": "ClF₃", "SF4": "SF₄",
}
_LONE_PAIR_MISTAKES = {
    "NH3": "chem.assumed_nh3_most_lone_pairs",
    "NO2-": "chem.assumed_nitrite_most_lone_pairs",
    "SO3^2-": "chem.assumed_sulfite_most_lone_pairs",
    "XeF4": "chem.confused_xef4_with_xef2_lone_pairs",
    "ClF3": "chem.confused_clf3_with_xef2_lone_pairs",
    "SF4": "chem.assumed_sf4_most_lone_pairs",
}


@question_type(
    "chem.posn2560_q24", display_name={"th": "คู่โดดเดี่ยวบนอะตอมกลางมากที่สุด"},
    level=LEVEL, subject="เคมี", topic="คู่โดดเดี่ยวและโครงสร้างลูอิส",
)
class CentralLonePairs(ChemistrySheet):
    def expr(self, rng):
        species = rng.choice((q24.PARAMS, *q24.VARIANTS))["species"]
        answer = q24.solve(species=species)
        return MathDraw(
            "", _LONE_PAIR_TEX[answer],
            prompt=("ในบรรดา " + ", ".join(_LONE_PAIR_TEXT[item] for item in species)
                    + " ชนิดใดมีอิเล็กตรอนคู่โดดเดี่ยวบนอะตอมกลางมากที่สุด"),
            hint="วาดโครงสร้างลูอิสและนับคู่โดดเดี่ยวบนอะตอมกลาง ไม่ใช่อะตอมปลาย",
            distractors=[named(_LONE_PAIR_MISTAKES[item], _LONE_PAIR_TEX[item])
                         for item in species if item != answer],
        )


_BONDING_TEX = {
    "SF4": r"\mathrm{SF_4}", "SCl2": r"\mathrm{SCl_2}",
    "PCl3": r"\mathrm{PCl_3}", "PF5": r"\mathrm{PF_5}",
    "H2O": r"\mathrm{H_2O}", "NH3": r"\mathrm{NH_3}",
    "CO2": r"\mathrm{CO_2}", "BF3": r"\mathrm{BF_3}",
    "CF4": r"\mathrm{CF_4}", "XeF4": r"\mathrm{XeF_4}",
    "ClF3": r"\mathrm{ClF_3}", "Na2O": r"\mathrm{Na_2O}",
    "COCl2": r"\mathrm{COCl_2}", "H2SO4": r"\mathrm{H_2SO_4}",
    "CaCO3": r"\mathrm{CaCO_3}", "NaNO3": r"\mathrm{NaNO_3}",
    "NH4Cl": r"\mathrm{NH_4Cl}", "K2SO4": r"\mathrm{K_2SO_4}",
    "NaCl": r"\mathrm{NaCl}", "O3": r"\mathrm{O_3}",
    "H2O2": r"\mathrm{H_2O_2}", "H2CO": r"\mathrm{H_2CO}",
    "CH2NH": r"\mathrm{CH_2NH}", "CH4": r"\mathrm{CH_4}",
    "HCl": r"\mathrm{HCl}",
}
_BONDING_TEXT = {
    key: value.replace(r"\mathrm{", "").replace("}", "").replace("_", "")
    for key, value in _BONDING_TEX.items()
}
_POLAR_MISTAKES = {
    "SF4": "chem.ignored_seesaw_dipole", "SCl2": "chem.ignored_bent_dipole",
    "PCl3": "chem.ignored_pyramidal_dipole", "H2O": "chem.ignored_bent_dipole",
    "NH3": "chem.ignored_pyramidal_dipole", "ClF3": "chem.ignored_t_shape_dipole",
}
_MIXED_BOND_MISTAKES = {
    "Na2O": "chem.assumed_simple_ionic_has_covalent_bond",
    "NaCl": "chem.assumed_simple_ionic_has_covalent_bond",
    "COCl2": "chem.assumed_molecular_compound_ionic",
    "H2SO4": "chem.confused_pure_acid_with_aqueous_ions",
    "H2O": "chem.assumed_molecular_compound_ionic",
    "CO2": "chem.assumed_molecular_compound_ionic",
}
_DATIVE_MISTAKES = {
    "H2O2": "chem.confused_peroxide_single_bond_with_dative",
    "H2CO": "chem.confused_carbonyl_double_bond_with_dative",
    "CH2NH": "chem.confused_imine_double_bond_with_dative",
    "H2O": "chem.confused_oxygen_lone_pairs_with_dative",
    "CO2": "chem.confused_carbonyl_double_bond_with_dative",
    "NH3": "chem.confused_oxygen_lone_pairs_with_dative",
    "CH4": "chem.confused_ordinary_single_bond_with_dative",
    "HCl": "chem.confused_ordinary_single_bond_with_dative",
}


@question_type(
    "chem.posn2560_q25", display_name={"th": "โมเลกุลไม่มีขั้วจากรูปร่าง"},
    level=LEVEL, subject="เคมี", topic="ขั้วโมเลกุลและรูปร่างโมเลกุล",
)
class NonpolarMolecule(ChemistrySheet):
    def expr(self, rng):
        species = rng.choice((q25.PARAMS, *q25.VARIANTS))["species"]
        answer = q25.solve(species=species)
        return MathDraw(
            "", _BONDING_TEX[answer],
            prompt=("ในบรรดา " + ", ".join(_BONDING_TEXT[item] for item in species)
                    + " โมเลกุลใดไม่มีขั้วโดยรวม"),
            hint="ใช้รูปร่าง VSEPR และดูว่าทิศทางไดโพลของพันธะหักล้างกันหรือไม่",
            distractors=[named(_POLAR_MISTAKES[item], _BONDING_TEX[item])
                         for item in species if item != answer],
        )


@question_type(
    "chem.posn2560_q26", display_name={"th": "สารประกอบที่มีพันธะไอออนิกและโคเวเลนต์"},
    level=LEVEL, subject="เคมี", topic="พันธะไอออนิกและโคเวเลนต์ในสารประกอบ",
)
class IonicAndCovalentBonds(ChemistrySheet):
    def expr(self, rng):
        compounds = rng.choice((q26.PARAMS, *q26.VARIANTS))["compounds"]
        answer = q26.solve(compounds=compounds)
        return MathDraw(
            "", _BONDING_TEX[answer],
            prompt=("พิจารณาสารบริสุทธิ์ "
                    + ", ".join(_BONDING_TEXT[item] for item in compounds)
                    + " สารใดมีทั้งแรงยึดเหนี่ยวแบบไอออนิกระหว่างไอออน "
                    "และพันธะโคเวเลนต์ภายในไอออนหลายอะตอม"),
            hint="หาเกลือที่มีไอออนหลายอะตอม เช่น CO₃²⁻ หรือ NO₃⁻",
            distractors=[named(_MIXED_BOND_MISTAKES[item], _BONDING_TEX[item])
                         for item in compounds if item != answer],
        )


@question_type(
    "chem.posn2560_q27", display_name={"th": "ภาพลูอิสแบบโคออร์ดิเนตของโอโซน"},
    level=LEVEL, subject="เคมี", topic="พันธะโคออร์ดิเนตและเรโซแนนซ์",
)
class CoordinateLewisDepiction(ChemistrySheet):
    def expr(self, rng):
        species = rng.choice((q27.PARAMS, *q27.VARIANTS))["species"]
        answer = q27.solve(species=species)
        return MathDraw(
            "", _BONDING_TEX[answer],
            prompt=("ในบรรดา " + ", ".join(_BONDING_TEXT[item] for item in species)
                    + " โมเลกุลใดแสดงภาพลูอิสแบบผู้ให้คู่อิเล็กตรอน→ผู้รับ "
                    "และมีภาพเรโซแนนซ์ที่สลับตำแหน่งพันธะได้ "
                    "(ลูกศรเป็นแบบจำลองการนับอิเล็กตรอน)"),
            hint="หาโมเลกุลที่มีภาพลูอิสเรโซแนนซ์สองแบบและมีการบริจาคคู่โดดเดี่ยวในภาพตำรา",
            distractors=[named(_DATIVE_MISTAKES[item], _BONDING_TEX[item])
                         for item in species if item != answer],
        )


_Q28_SHAPES = {
    "tetrahedral": "ทรงสี่หน้า", "square_planar": "สี่เหลี่ยมแบนราบ",
    "seesaw": "ทรงสี่หน้าบิดเบี้ยว", "trigonal_pyramidal": "พีระมิดฐานสามเหลี่ยม",
    "square_pyramidal": "พีระมิดฐานสี่เหลี่ยม",
}
_Q28_MISTAKES = {
    "tetrahedral": "chem.ignored_noble_gas_lone_pair",
    "square_planar": "chem.assigned_two_noble_gas_lone_pairs",
    "seesaw": "chem.assumed_four_ligands_one_lone_pair",
    "trigonal_pyramidal": "chem.counted_double_oxo_as_two_ligands",
    "square_pyramidal": "chem.confused_five_and_six_domains",
}
_Q28_DISTRACTORS = {
    "seesaw": ("tetrahedral", "square_planar", "trigonal_pyramidal"),
    "square_pyramidal": ("tetrahedral", "square_planar", "seesaw"),
    "trigonal_pyramidal": ("tetrahedral", "seesaw", "square_pyramidal"),
    "square_planar": ("tetrahedral", "seesaw", "square_pyramidal"),
}


@question_type(
    "chem.posn2560_q28", display_name={"th": "รูปร่างของออกไซด์แก๊สมีตระกูล"},
    level=LEVEL, subject="เคมี", topic="รูปร่างโมเลกุลตาม VSEPR",
)
class NobleGasOxoShape(QuestionType):
    sheet_id = ChemistrySheet.sheet_id
    sheet = ChemistrySheet.sheet

    def build(self, rng, **params):
        formula = rng.choice((q28.PARAMS, *q28.VARIANTS))["formula"]
        answer = q28.solve(formula=formula)
        return GeneratedQuestion(
            stem=[text("ตามแบบจำลองลูอิสที่ O ปลายสร้างพันธะคู่ และ H/F สร้างพันธะเดี่ยว "
                       f"รูปร่างการจัดเรียงอะตอมรอบอะตอมกลางของ {formula} เป็นอย่างไร")],
            correct=[text(_Q28_SHAPES[answer])],
            distractors=fixed(*[[text(named(_Q28_MISTAKES[shape], _Q28_SHAPES[shape]))]
                                for shape in _Q28_DISTRACTORS[answer]]),
            topic="รูปร่างโมเลกุลตาม VSEPR",
            hint=[text("นับหนึ่งโดเมนต่อพันธะคู่ แล้วนับคู่โดดเดี่ยวของ Kr/Xe แยกต่างหาก")],
        )


_Q29_NAMES = {
    "chromium_trioxide": "โครเมียมไตรออกไซด์",
    "chromium_dioxide": "โครเมียมไดออกไซด์",
    "sodium_thiosulfate": "โซเดียมไทโอซัลเฟต",
    "sodium_sulfite": "โซเดียมซัลไฟต์",
    "mercury_i_chloride": "เมอร์คิวรี(I)คลอไรด์",
    "mercury_ii_chloride": "เมอร์คิวรี(II)คลอไรด์",
    "barium_nitrite": "แบเรียมไนไตรต์",
    "barium_nitrate": "แบเรียมไนเตรต",
}


@question_type(
    "chem.posn2560_q29", display_name={"th": "ตรวจชื่อสารจากสูตรเคมี"},
    level=LEVEL, subject="เคมี", topic="การเรียกชื่อสารประกอบอนินทรีย์",
)
class CompoundNameAudit(ChemistrySheet):
    def expr(self, rng):
        names = rng.choice((q29.PARAMS, *q29.VARIANTS))["names"]
        answer = q29.solve(names=names)
        rows = "; ".join(f"{formula} = {_Q29_NAMES[name]}"
                         for formula, name in zip(q29.FORMULAS, names))
        return MathDraw(
            "", str(answer),
            prompt=f"พิจารณาคู่สูตร–ชื่อสารต่อไปนี้: {rows} มีคู่ที่เรียกชื่อผิดกี่คู่",
            hint="ตรวจไนไตรต์/ไนเตรต และประจุเมอร์คิวรี(I) ใน Hg₂Cl₂ ด้วย",
            distractors=[named("chem.overcounted_nomenclature_errors" if number > answer
                               else "chem.undercounted_nomenclature_errors", str(number))
                         for number in range(4) if number != answer],
        )


_Q30_WRONG = {
    "CH2=CHCH3": (("CH2=CCH3", "H"), ("CH2=CH", "CH3"),
                   ("CH2=CHCH2", "H")),
    "CH2=CHCH2CH3": (("CH2=CCH2CH3", "H"), ("CH2=CH", "CH2CH3"),
                      ("CH2=CHCH2CH2", "H")),
    "CH3CH=CHCH3": (("CH3C=CHCH3", "H"), ("CH3", "CH=CHCH3"),
                     ("CH2CH=CHCH3", "H")),
    "CH2=CHCH2CH2CH3": (("CH2=CCH2CH2CH3", "H"),
                         ("CH2=CH", "CH2CH2CH3"), ("CH2=CHCH2CH2CH2", "H")),
}
_Q30_MISTAKES = (
    "chem.broke_vinylic_carbon_hydrogen", "chem.broke_alkene_adjacent_single_bond",
    "chem.broke_alkyl_carbon_hydrogen",
)


def _hydrocarbon_tex(formula):
    pieces = formula.split("=")
    return "=".join(r"\mathrm{" + re.sub(r"([A-Z][a-z]?)(\d+)", r"\1_\2", part) + "}"
                    for part in pieces)


def _cleavage_tex(alkene, products):
    return (_hydrocarbon_tex(alkene) + r"_{(g)}\rightarrow "
            + "+".join(_hydrocarbon_tex(item) + r"_{(g)}" for item in products))


@question_type(
    "chem.posn2560_q30", display_name={"th": "การสลายพันธะคู่คาร์บอนคาร์บอน"},
    level=LEVEL, subject="เคมี", topic="พลังงานสลายพันธะและการแยกพันธะ",
)
class AlkeneDoubleBondDissociation(ChemistrySheet):
    def expr(self, rng):
        alkene = rng.choice((q30.PARAMS, *q30.VARIANTS))["alkene"]
        answer = q30.solve(alkene=alkene)
        return MathDraw(
            "", _cleavage_tex(alkene, answer),
            prompt=(f"จาก {alkene}(g) ปฏิกิริยาแตกตัวเป็นชิ้นส่วนข้อใด "
                    "ตัดพันธะ C=C เดิมทั้งพันธะโดยตรง"),
            hint="เมื่อตัดพันธะคู่ C=C ชิ้นส่วนต้องอยู่คนละด้านของเครื่องหมาย = เดิม",
            distractors=[named(key, _cleavage_tex(alkene, products))
                         for key, products in zip(_Q30_MISTAKES, _Q30_WRONG[alkene])],
        )


def _interhalogen_tex(item):
    element, count, charge = item
    formula = element + "F"
    subscript = "" if count == 1 else f"_{{{count}}}"
    superscript = "" if charge == 0 else "^{+}" if charge == 1 else f"^{{{charge}+}}"
    return rf"\mathrm{{{formula}}}{subscript}{superscript}"


def _interhalogen_text(item):
    element, count, charge = item
    return element + "F" + (str(count) if count > 1 else "") + (
        "" if charge == 0 else "+" if charge == 1 else f"^{charge}+")


_OCTET_MISTAKES = {
    1: "chem.assumed_diatomic_halide_breaks_octet",
    2: "chem.ignored_charge_in_difluoride_octet",
    3: "chem.assumed_trifluoride_exceeds_octet",
    4: "chem.assumed_four_bonds_always_exceed_octet",
}


@question_type(
    "chem.posn2560_q31", display_name={"th": "กฎออกเตตของไอออนอินเตอร์แฮโลเจน"},
    level=LEVEL, subject="เคมี", topic="กฎออกเตตและโครงสร้างลูอิส",
)
class InterhalogenOctet(ChemistrySheet):
    def expr(self, rng):
        species = rng.choice((q31.PARAMS, *q31.VARIANTS))["species"]
        answer = q31.solve(species=species)
        return MathDraw(
            "", _interhalogen_tex(answer),
            prompt=("สมมติโครงสร้างลูอิสที่มีพันธะเดี่ยวระหว่างอะตอมกลางกับ F ทุกอะตอม "
                    "ในบรรดา " + ", ".join(_interhalogen_text(item) for item in species)
                    + " ชนิดใดมีอิเล็กตรอนรอบอะตอมกลางไม่เท่ากับ 8"),
            hint="นับอิเล็กตรอนเวเลนซ์รวม หักประจุบวก และเติมออกเตตให้ F ปลายก่อน",
            distractors=[named(_OCTET_MISTAKES[item[1]], _interhalogen_tex(item))
                         for item in species if item != answer],
        )


_POLAR_PAIR_TEX = {
    "HCN": r"\mathrm{HCN}", "KrF4": r"\mathrm{KrF_4}",
    "AsI5": r"\mathrm{AsI_5}", "SBr2": r"\mathrm{SBr_2}",
    "ClH3": r"\mathrm{ClH_3}", "TeF4": r"\mathrm{TeF_4}",
    "SO3": r"\mathrm{SO_3}", "PBr3": r"\mathrm{PBr_3}",
    "NH3": r"\mathrm{NH_3}", "H2O": r"\mathrm{H_2O}",
    "CO2": r"\mathrm{CO_2}", "XeF4": r"\mathrm{XeF_4}",
    "BF3": r"\mathrm{BF_3}", "PCl3": r"\mathrm{PCl_3}",
    "SF4": r"\mathrm{SF_4}",
}
_NONPOLAR_MISTAKES = {
    "KrF4": "chem.assumed_square_planar_krf4_polar",
    "AsI5": "chem.assumed_symmetric_trigonal_bipyramid_polar",
    "SO3": "chem.assumed_trigonal_planar_oxide_polar",
    "CO2": "chem.assumed_linear_co2_polar",
    "XeF4": "chem.assumed_square_planar_xef4_polar",
    "BF3": "chem.assumed_trigonal_planar_bf3_polar",
}


def _polar_pair_tex(pair):
    return _POLAR_PAIR_TEX[pair[0]] + r",\;" + _POLAR_PAIR_TEX[pair[1]]


@question_type(
    "chem.posn2560_q32", display_name={"th": "คู่โมเลกุลที่มีขั้วทั้งสองชนิด"},
    level=LEVEL, subject="เคมี", topic="ขั้วโมเลกุลและรูปร่างโมเลกุล",
)
class BothMoleculesPolar(ChemistrySheet):
    def expr(self, rng):
        pairs = rng.choice((q32.PARAMS, *q32.VARIANTS))["pairs"]
        answer = q32.solve(pairs=pairs)
        model_note = (" สำหรับ ClH3 ให้ถือเป็นแบบจำลอง Cl–H สามพันธะ"
                      "และคู่โดดเดี่ยวสองคู่" if any("ClH3" in pair for pair in pairs) else "")
        return MathDraw(
            "", _polar_pair_tex(answer),
            prompt=("พิจารณารูปร่างตามแบบลูอิส/VSEPR" + model_note
                    + " คู่ใดมีขั้วสุทธิทั้งสองชนิด"),
            hint="โมเลกุลสมมาตรที่พันธะปลายเหมือนกันมีไดโพลหักล้างกัน",
            distractors=[named(_NONPOLAR_MISTAKES[next(item for item in pair
                                                     if item in _NONPOLAR_MISTAKES)],
                               _polar_pair_tex(pair))
                         for pair in pairs if pair != answer],
        )


_LIQUID_TREND_TEXT = {
    ("vapor_pressure", "decrease"): "ความดันไอลดลง",
    ("vapor_pressure", "increase"): "ความดันไอเพิ่มขึ้น",
    ("surface_tension", "decrease"): "ความตึงผิวลดลง",
    ("surface_tension", "increase"): "ความตึงผิวเพิ่มขึ้น",
    ("kinetic_energy", "decrease"): "พลังงานจลน์เฉลี่ยของโมเลกุลลดลง",
    ("kinetic_energy", "increase"): "พลังงานจลน์เฉลี่ยของโมเลกุลเพิ่มขึ้น",
    ("fixed_distance_attraction", "decrease"): "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมลดลง",
    ("fixed_distance_attraction", "increase"): "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมเพิ่มขึ้น",
    ("fixed_distance_attraction", "same"): "แรงดึงดูดระหว่างโมเลกุลที่ระยะห่างเท่าเดิมไม่เปลี่ยน",
}
_LIQUID_MISTAKES = {
    "vapor_pressure": "chem.misread_vapor_pressure_temperature_trend",
    "surface_tension": "chem.misread_surface_tension_temperature_trend",
    "kinetic_energy": "chem.misread_kinetic_energy_temperature_trend",
    "fixed_distance_attraction": "chem.confused_temperature_with_pair_force_law",
}


@question_type(
    "chem.posn2560_q33", display_name={"th": "ผลของอุณหภูมิต่อสมบัติของเหลว"},
    level=LEVEL, subject="เคมี", topic="สมบัติของเหลวและแรงยึดเหนี่ยวระหว่างโมเลกุล",
)
class LiquidCoolingClaims(QuestionType):
    sheet_id = ChemistrySheet.sheet_id
    sheet = ChemistrySheet.sheet

    def build(self, rng, **params):
        values = rng.choice((q33.PARAMS, *q33.VARIANTS))
        direction, claims = values["direction"], values["claims"]
        wrong = q33.solve(direction=direction, claims=claims)
        verb = "ลด" if direction == "cool" else "เพิ่ม"
        return GeneratedQuestion(
            stem=[text(f"เมื่อ{verb}อุณหภูมิของของเหลวชนิดเดิม (ยังอยู่ในสถานะของเหลว) "
                       "ข้อความใดไม่ถูกต้อง")],
            correct=[text(_LIQUID_TREND_TEXT[claims[wrong]])],
            distractors=fixed(*[[text(named(_LIQUID_MISTAKES[claim[0]],
                                            _LIQUID_TREND_TEXT[claim]))]
                                for i, claim in enumerate(claims) if i != wrong]),
            topic="สมบัติของเหลวและแรงยึดเหนี่ยวระหว่างโมเลกุล",
            hint=[text("ความดันไอและพลังงานจลน์เปลี่ยนตามอุณหภูมิ; "
                       "แรงระหว่างโมเลกุลชนิดเดิมที่ระยะห่างเท่าเดิมไม่เปลี่ยน")],
        )


_PHASE_CLAIMS = {
    "boil_pressure_up": "เมื่อความดันภายนอกลดลง จุดเดือดของของเหลวสูงขึ้น",
    "boil_pressure_down": "เมื่อความดันภายนอกลดลง จุดเดือดของของเหลวต่ำลง",
    "evap_surface": "การระเหยเกิดขึ้นที่ผิวหน้าของของเหลว",
    "evap_bulk_only": "การระเหยเกิดขึ้นเฉพาะในเนื้อของเหลว ไม่เกิดที่ผิวหน้า",
    "iodine_melts_below_room": "ไอโอดีนมีจุดหลอมเหลวต่ำกว่าอุณหภูมิห้อง 25 °C",
    "iodine_melts_above_room": "ไอโอดีนมีจุดหลอมเหลวสูงกว่าอุณหภูมิห้อง 25 °C",
    "salt_vapor_higher": "ที่ 25 °C NaCl แข็งมีความดันไอสูงกว่าไอโอดีนแข็ง",
    "salt_vapor_lower": "ที่ 25 °C NaCl แข็งมีความดันไอต่ำกว่าไอโอดีนแข็ง",
}
_PHASE_MISTAKES = {
    "boil_pressure_up": "chem.inverted_external_pressure_boiling_trend",
    "evap_bulk_only": "chem.confused_evaporation_with_bulk_boiling",
    "iodine_melts_below_room": "chem.assumed_iodine_sublimes_because_melting_below_room",
    "salt_vapor_higher": "chem.assumed_ionic_solid_has_higher_vapor_pressure",
}


@question_type(
    "chem.posn2560_q34", display_name={"th": "การระเหยและสมดุลไอของสาร"},
    level=LEVEL, subject="เคมี", topic="การเปลี่ยนสถานะและความดันไอ",
)
class PhaseChangeClaims(QuestionType):
    sheet_id = ChemistrySheet.sheet_id
    sheet = ChemistrySheet.sheet

    def build(self, rng, **params):
        claims = rng.choice((q34.PARAMS, *q34.VARIANTS))["claims"]
        correct_index = q34.solve(claims=claims)
        return GeneratedQuestion(
            stem=[text("ที่ความดันปกติและอุณหภูมิห้อง 25 °C ข้อความใดถูกต้อง")],
            correct=[text(_PHASE_CLAIMS[claims[correct_index]])],
            distractors=fixed(*[[text(named(_PHASE_MISTAKES[claim], _PHASE_CLAIMS[claim]))]
                                for i, claim in enumerate(claims) if i != correct_index]),
            topic="การเปลี่ยนสถานะและความดันไอ",
            hint=[text("จุดเดือดขึ้นกับความดันภายนอก; แยกการระเหยที่ผิวหน้าออกจากการเดือด")],
        )


_LATTICE_CLAIMS = {
    "coord_equal": "จำนวน Cl⁻ เพื่อนบ้านใกล้สุดรอบ Na⁺ เท่ากับจำนวน Na⁺ รอบ Cl⁻",
    "coord_unequal": "Na⁺ และ Cl⁻ ในโครงสร้าง NaCl มีจำนวนเพื่อนบ้านประจุตรงข้ามไม่เท่ากัน",
    "lattice_overcome": "เมื่อละลายน้ำ โครงข่ายไอออนิกของผลึก NaCl ถูกแยกออกเป็นไอออนที่ไฮเดรต",
    "lattice_unchanged": "เมื่อละลายน้ำ โครงข่ายผลึก NaCl ยังคงเดิมทั้งก้อน",
    "crop_is_formula": "ถ้าภาพตัดแสดง Na⁺ 14 ลูกกับ Cl⁻ 13 ลูก สูตรของเกลือคือ Na₁₄Cl₁₃",
    "formula_one_to_one": "ถึงภาพตัดจะมีจำนวนลูกไม่เท่ากัน สูตรหน่วยของเกลือนี้คือ NaCl",
}
_LATTICE_OPTIONS = ((0,), (1, 2), (0, 1), (0, 2))
_LATTICE_OPTION_TEXT = {
    (0,): "a เท่านั้น", (1, 2): "b และ c", (0, 1): "a และ b", (0, 2): "a และ c",
}


@question_type(
    "chem.posn2560_q35", display_name={"th": "โครงผลึกและสูตรหน่วยของ NaCl"},
    level=LEVEL, subject="เคมี", topic="โครงสร้างผลึกไอออนิกและสูตรหน่วย",
)
class SaltLatticeClaims(QuestionType):
    sheet_id = ChemistrySheet.sheet_id
    sheet = ChemistrySheet.sheet

    def build(self, rng, **params):
        claims = rng.choice((q35.PARAMS, *q35.VARIANTS))["claims"]
        correct = q35.solve(claims=claims)
        labels = "abc"
        lines = "; ".join(f"{labels[i]}. {_LATTICE_CLAIMS[claim]}"
                          for i, claim in enumerate(claims))
        wrong = {
            (0,): "chem.omitted_true_lattice_claim",
            (1, 2): "chem.misread_lattice_claim_combination",
            (0, 1): "chem.misread_lattice_claim_combination",
            (0, 2): "chem.misread_lattice_claim_combination",
        }
        return GeneratedQuestion(
            stem=[text("ผลึก NaCl แบบร็อกซอลต์มีเพื่อนบ้านประจุตรงข้าม 6 ตัวต่อไอออน "
                       f"พิจารณาข้อความต่อไปนี้: {lines} ข้อใดถูกต้อง")],
            correct=[text(_LATTICE_OPTION_TEXT[correct])],
            distractors=fixed(*[[text(named(wrong[option], _LATTICE_OPTION_TEXT[option]))]
                                for option in _LATTICE_OPTIONS if option != correct]),
            topic="โครงสร้างผลึกไอออนิกและสูตรหน่วย",
            hint=[text("ภาพตัดไม่ใช่หนึ่งสูตรหน่วย; สูตร NaCl ต้องเป็นกลางทางไฟฟ้า")],
        )


@question_type(
    "chem.posn2560_q36", display_name={"th": "กฎของชาร์ลส์จากองศาเซลเซียส"},
    level=LEVEL, subject="เคมี", topic="กฎแก๊สอุดมคติและอุณหภูมิสัมบูรณ์",
)
class CharlesLawVolume(ChemistrySheet):
    def expr(self, rng):
        values = rng.choice((q36.PARAMS, *q36.VARIANTS))
        volume = values["initial_volume"]
        initial = values["initial_celsius"]
        final = values["final_celsius"]
        answer = q36.solve(**values)
        mistaken_celsius = round(volume * final / initial, 1) if initial else 0.0
        distractors = [volume / 2, round(volume * (initial + 273.15) /
                                          (final + 273.15), 1), mistaken_celsius]
        return MathDraw(
            "", f"{answer:.1f}",
            prompt=(f"แก๊สมีปริมาตร {volume} cm³ ที่ {initial} °C และความดันคงที่ "
                    f"เมื่ออุณหภูมิเป็น {final} °C ปริมาตรเป็นกี่ cm³ "
                    "(ตอบทศนิยมหนึ่งตำแหน่ง)"),
            hint="ใช้ V₁/T₁ = V₂/T₂ โดย T เป็นเคลวิน",
            distractors=[named(key, f"{value:.1f}") for key, value in zip((
                "chem.halved_volume_for_temperature_change",
                "chem.inverted_charles_temperature_ratio",
                "chem.used_celsius_in_charles_law",
            ), distractors)],
        )
