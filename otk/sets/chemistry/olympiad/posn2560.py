"""Reviewed waves of POSN camp-selection chemistry 2560."""

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.posn2560_chemistry import q01, q02, q03, q04, q05, q06

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
