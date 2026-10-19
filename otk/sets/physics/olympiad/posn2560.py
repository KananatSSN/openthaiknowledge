"""POSN camp 1 physics, 2560: computed variants with audited solvers.

Source diagrams are described in each question; parameter-labelled source
crops are not reused after their constants change.
"""

from fractions import Fraction

from otk.core.registry import question_type
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.kit.answer_choices import show
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.posn2560_physics import q01, q02, q05, q08
from otk.sheets.posn2560_physics import q03, q04, q06, q07, q09, q10
from otk.sheets.posn2560_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20
from otk.sheets.posn2560_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29, q30

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


# Authored diagnostic slips, in the same order as each draw distractor list.
DISTRACTOR_TAGS = {
    1: ("phys.area_dimension_ignored", "phys.time_dimension_wrong", "phys.dimensions_multiplied"),
    2: ("phys.used_full_gravity", "phys.halved_speed", "part.complement"),
    3: ("phys.ignored_lift_acceleration", "phys.lift_acceleration_subtracted", "phys.halved_time"),
    4: ("phys.ignored_weight", "phys.added_weight_to_buoyancy", "phys.ignored_buoyancy"),
    5: ("phys.ignored_contact_weight", "phys.subtracted_rebound_speed", "phys.ignored_rebound"),
    6: (
        "phys.used_sticking_collision",
        "phys.conserved_collision_energy",
        "phys.kinetic_half_missing",
    ),
    7: ("phys.used_final_force_for_work", "phys.halved_speed", "units.wrong_conversion"),
    9: ("phys.kept_release_angle", "phys.extra_factor_two", "phys.used_half_release_cosine"),
    10: ("phys.used_vertical_tension", "phys.weight_at_beam_end", "phys.ignored_beam_weight"),
    11: ("direction.opposite", "phys.used_charge_ratio_not_root", "phys.charge_zero_between"),
    12: ("fraction.inverted", "phys.ignored_charge_weights", "phys.reversed_charge_sign"),
    13: (
        "phys.subtracted_parallel_resistances",
        "phys.added_parallel_resistances",
        "fraction.inverted",
    ),
    14: ("phys.equal_capacitor_voltage", "phys.ignored_divider", "phys.added_series_capacitance"),
    15: (
        "phys.kept_wire_area",
        "proportion.direct_instead_of_inverse",
        "phys.power_tracks_resistance",
    ),
    16: ("part.complement", "fraction.inverted", "phys.used_emerged_second_volume"),
    17: ("phys.pressure_height_added", "phys.ignored_column_height", "phys.pressure_height_only"),
    18: ("phys.ignored_oil_heat", "phys.final_temperature_only", "phys.equal_heat_capacities"),
    19: ("phys.celsius_for_gas", "units.not_converted", "units.wrong_conversion"),
    20: ("phys.upright_self_image", "phys.mirror_focus_not_centre", "phys.lens_sign_reversed"),
    21: ("phys.velocity_angle_unchanged", "phys.height_factor_inverted", "fraction.inverted"),
    22: (
        "phys.ignored_small_mass",
        "phys.ignored_big_mass",
        "phys.multiplied_friction_coefficient",
    ),
    23: ("phys.used_one_rod_balance", "phys.wrong_pivot_distance", "phys.added_lever_lengths"),
    24: (
        "phys.radial_force_only",
        "phys.added_perpendicular_forces",
        "phys.kinetic_factor_two_missing",
    ),
    25: ("area.added_signed_regions", "phys.rectangle_for_force_graph", "phys.ignored_ramp_work"),
    26: ("phys.total_charge_one_sphere", "phys.ignored_other_final_charge", "fraction.inverted"),
    27: ("phys.added_branch_currents", "phys.ignored_node_voltage", "direction.opposite"),
    28: ("units.not_converted", "phys.radius_not_area", "phys.multiplied_tank_area"),
    29: ("fraction.inverted", "phys.radius_not_diameter", "proportion.area_scaled_once"),
    30: (
        "phys.image_distances_as_conjugates",
        "phys.image_distance_as_focal",
        "phys.doubled_focal",
    ),
}


def _named_draw(number, draw):
    draw.distractors = [
        named(tag, value) for tag, value in zip(DISTRACTOR_TAGS[number], draw.distractors)
    ]
    return draw


def _tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def _written_provenance(number):
    return Provenance(
        "adapted",
        sources=(
            f"ข้อสอบคัดเลือกค่าย 1 สอวน. ฟิสิกส์ ปี 2560 ตอนที่ 2 ข้อ {number} "
            "(สอวน_physics/posn1-60-physics.pdf)",
        ),
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2560_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2560)"


@question_type(
    "phys.posn2560_q03",
    display_name={"th": "หลอดไฟตกในลิฟต์เร่งขึ้น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความเร่งสัมพัทธ์",
)
class FallingBulb(PhysicsSheet):
    def expr(self, rng):
        a = rng.choice((2, 4, 6))
        t = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2))
        h = Fraction(10 + a, 2) * t * t
        answer = q03.solve(h=float(h), a=a, g=10)
        # Named mistakes: ignore elevator acceleration, use g-a, halve the time.
        return _named_draw(
            3,
            MathDraw(
                "",
                _tex(answer),
                prompt=(
                    f"ลิฟต์เร่งขึ้นคงตัว {a} m/s² หลอดไฟสูงจากพื้นลิฟต์ {show(h)} m หลุดจากเพดาน "
                    "ขณะหลุดหลอดไฟมีความเร็วเท่าลิฟต์ ลิฟต์ยังเร่งเท่าเดิม หลอดไฟตกถึงพื้นลิฟต์ในกี่วินาที "
                    "(g = 10 m/s²)"
                ),
                hint=r"h=\frac12(g+a)t^2",
                distractors=[
                    rf"\sqrt{{{_tex(h / 5)}}}",
                    rf"\sqrt{{{_tex(2 * h / (10 - a))}}}",
                    _tex(t / 2),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q04",
    display_name={"th": "อัตราเร็วปลายของวัตถุลอยขึ้นในน้ำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงลอยตัวและแรงต้าน",
)
class UpwardTerminalSpeed(PhysicsSheet):
    def expr(self, rng):
        displaced, mass, drag = rng.randint(3, 8), rng.randint(1, 2), rng.choice((2, 4, 5))
        v = q04.solve(rho=1000, volume=displaced / 1000, mass=mass, drag=drag, g=10)
        return _named_draw(
            4,
            MathDraw(
                "",
                _tex(v),
                prompt=(
                    f"วัตถุมวล {mass} kg ปริมาตร {displaced} L จมอยู่ใต้น้ำทั้งหมดและลอยขึ้น "
                    f"น้ำมีความหนาแน่น 1000 kg/m³ แรงต้านมีขนาด {drag}v N เมื่อ v มีหน่วย m/s "
                    "อัตราเร็วปลายมีค่าเท่าใดในหน่วย m/s (g = 10 m/s²)"
                ),
                hint=r"\rho Vg-mg-Cv=0",
                distractors=[
                    _tex(displaced * 10 / drag),
                    _tex((displaced + mass) * 10 / drag),
                    _tex(mass * 10 / drag),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q06",
    display_name={"th": "ชนลูกตุ้มแล้ววัตถุตกในแนวดิ่ง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="โมเมนตัมและพลังงานของลูกตุ้ม",
)
class BallisticPendulum(PhysicsSheet):
    def expr(self, rng):
        mass, target, speed = rng.choice((1, 2)), rng.choice((3, 4, 5)), rng.choice((4, 6, 8, 10))
        h = q06.solve(mass=mass, target=target, speed=speed, g=10)
        return _named_draw(
            6,
            MathDraw(
                "",
                _tex(h),
                prompt=(
                    f"วัตถุมวล {mass} kg เคลื่อนที่แนวระดับ {speed} m/s ชนทรงกลมมวล {target} kg "
                    "ซึ่งห้อยนิ่งด้วยเชือกเบา หลังชนวัตถุแรกตกตรงลงโดยไม่มีความเร็วแนวระดับ "
                    "ทรงกลมขึ้นสูงจากตำแหน่งชนได้เท่าใดในหน่วย m (g = 10 m/s² ไม่คิดการสูญเสียระหว่างแกว่ง)"
                ),
                hint=r"mv=MV,\quad Mgh=\frac12MV^2",
                distractors=[
                    _tex((mass * speed / (mass + target)) ** 2 / 20),
                    _tex(mass * speed**2 / (target * 20)),
                    _tex(2 * h),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q07",
    display_name={"th": "แรงดึงธนูและพลังงานลูกธนู"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานยืดหยุ่น",
)
class BowEnergy(PhysicsSheet):
    def expr(self, rng):
        mass = rng.choice((Fraction(1, 50), Fraction(1, 25), Fraction(1, 10)))
        x = rng.choice((Fraction(2, 5), Fraction(1, 2), Fraction(3, 5)))
        speed = rng.choice((20, 30, 40, 60))
        force = mass * speed**2 / x
        v = q07.solve(force=float(force), extension=float(x), mass=float(mass))
        return _named_draw(
            7,
            MathDraw(
                "",
                _tex(v),
                prompt=(
                    f"ธนูเป็นไปตามกฎของฮุก แรงดึงเพิ่มจากศูนย์จนเป็น {show(force)} N "
                    f"เมื่อดึงไป {show(x)} m ลูกธนูมวล {show(mass * 1000)} g "
                    "รับพลังงานยืดหยุ่นทั้งหมด จะพุ่งด้วยอัตราเร็วเท่าใดในหน่วย m/s"
                ),
                hint=r"\frac12Fx=\frac12mv^2",
                distractors=[rf"{speed}\sqrt{{2}}", _tex(speed / 2), _tex(speed / 10)],
            ),
        )


@question_type(
    "phys.posn2560_q09",
    display_name={"th": "จุดหลุดจากผิวทรงกลมลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่บนผิวทรงกลม",
)
class LeavingSphere(PhysicsSheet):
    def expr(self, rng):
        c = rng.choice((Fraction(3, 5), Fraction(4, 5), Fraction(1, 2), Fraction(9, 10)))
        result = q09.solve(cos_start=float(c))
        return _named_draw(
            9,
            MathDraw(
                rf"\cos\theta_0={_tex(c)}",
                rf"\arccos\left({_tex(result)}\right)",
                prompt=(
                    "ปล่อยมวลจุดจากหยุดนิ่งให้ไถลบนผิวด้านนอกของครึ่งทรงกลมลื่น "
                    "ตำแหน่งเริ่มทำมุม θ₀ กับแนวดิ่งผ่านยอด เมื่อใดวัตถุจะเริ่มหลุดจากผิว "
                    "ตอบเป็นมุมวัดจากแนวดิ่งผ่านยอด"
                ),
                hint=r"mg\cos\theta=mv^2/R,\quad v^2=2gR(\cos\theta_0-\cos\theta)",
                distractors=[
                    rf"\arccos\left({_tex(c)}\right)",
                    rf"\arccos\left({_tex(c / 3)}\right)",
                    rf"\arccos\left({_tex(c / 2)}\right)",
                ],
            ),
        )


@question_type(
    "phys.posn2560_q10",
    display_name={"th": "แรงตึงสายเคเบิลค้ำคาน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลโมเมนต์ของคาน",
)
class SupportedBeam(PhysicsSheet):
    def expr(self, rng):
        length, height, diagonal = rng.choice(((3, 4, 5), (4, 3, 5), (5, 12, 13)))
        weight, load = 20 * rng.randint(2, 15), 20 * rng.randint(2, 20)
        tension = q10.solve(length=length, height=height, weight=weight, load=load)
        return _named_draw(
            10,
            MathDraw(
                "",
                _tex(tension),
                prompt=(
                    f"คานสม่ำเสมอ AB ยาว {length} m หนัก {weight} N วางแนวระดับ บานพับ A ติดกำแพงลื่น "
                    f"จุด C อยู่บนกำแพงสูงกว่า A {height} m สายเคเบิล BC ค้ำปลาย B ซึ่งแขวนของหนัก {load} N "
                    "แรงตึงสาย BC เป็นเท่าใดในหน่วย N"
                ),
                hint=r"T\sin\theta\,L=W L/2+PL",
                distractors=[
                    _tex(weight / 2 + load),
                    _tex((weight + load) * diagonal / height),
                    _tex(load * diagonal / height),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q11",
    display_name={"th": "ประจุสามตัวอยู่ในสมดุล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลของประจุบนเส้นตรง",
)
class ChargeEquilibrium(PhysicsSheet):
    def expr(self, rng):
        root_a, root_b = rng.choice(((2, 3), (2, 5), (3, 4), (3, 5)))
        a, b, d = root_a**2, root_b**2, rng.choice((6, 10, 12, 18))
        x = q11.solve(a=a, b=b, d=d)
        return _named_draw(
            11,
            MathDraw(
                "",
                _tex(x),
                prompt=(
                    f"ประจุ −{a} µC อยู่ที่ x = 0 และ +{b} µC อยู่ที่ x = {d} cm "
                    "นำประจุไม่เป็นศูนย์ตัวที่สามมาวางบนแกน x แล้วประจุทั้งสามอยู่ในสมดุล "
                    "ประจุตัวที่สามอยู่ที่พิกัด x เท่าใดในหน่วย cm"
                ),
                hint=r"\frac{a}{x^2}=\frac{b}{(d-x)^2},\quad x<0",
                distractors=[
                    _tex(-x),
                    _tex(-d * a / (b - a)),
                    _tex(d * root_a / (root_a + root_b)),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q12",
    display_name={"th": "ทิศสนามไฟฟ้าจากสองประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การรวมเวกเตอร์สนามไฟฟ้า",
)
class ElectricFieldDirection(PhysicsSheet):
    def expr(self, rng):
        p, n = rng.choice(((2, 1), (3, 1), (4, 1), (3, 2)))
        a, h = rng.choice(((3, 4), (4, 3), (5, 12)))
        ratio = q12.solve(p=p, n=n, a=a, h=h)
        return _named_draw(
            12,
            MathDraw(
                "",
                rf"\arctan\left({_tex(ratio)}\right)",
                prompt=(
                    f"ตรึงประจุ +{p}Q ที่ (0,0) และ −{n}Q ที่ ({2 * a},0) "
                    f"สนามไฟฟ้าที่ ({a},{h}) ทำมุมเท่าใดกับแกน +x (Q > 0 พิกัดใช้หน่วยเดียวกัน)"
                ),
                hint=r"\tan\theta=E_y/E_x",
                distractors=[
                    rf"\arctan\left({_tex(1 / ratio)}\right)",
                    rf"\arctan\left({_tex(Fraction(h, a))}\right)",
                    rf"\arctan\left({_tex(Fraction((p + n) * h, (p - n) * a))}\right)",
                ],
            ),
        )


@question_type(
    "phys.posn2560_q13",
    display_name={"th": "หาตัวต้านทานที่ซ่อนอยู่ในวงจรขนาน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความต้านทานรวมของวงจรขนาน",
)
class UnknownParallelResistance(PhysicsSheet):
    def expr(self, rng):
        scale = rng.choice((1, 2, 3, 4))
        rs = (15 * scale, 6 * scale, 10 * scale)
        total = rng.choice((scale, 2 * scale))
        x = q13.solve(total=total, resistors=rs)
        known = 1 / sum(1 / Fraction(r) for r in rs)
        return _named_draw(
            13,
            MathDraw(
                "",
                _tex(x),
                prompt=(
                    f"ตัวต้านทาน {rs[0]}, {rs[1]}, {rs[2]} Ω และ X ต่อขนานทั้งหมดระหว่างจุด a กับ b "
                    f"วัดความต้านทานรวมได้ {total} Ω จงหา X ในหน่วย Ω"
                ),
                hint=r"1/R_{ab}=1/R_1+1/R_2+1/R_3+1/X",
                distractors=[_tex(known - total), _tex(known + total), _tex(1 / x)],
            ),
        )


@question_type(
    "phys.posn2560_q14",
    display_name={"th": "ประจุในวงจรตัวเก็บประจุเมื่อกระแสคงตัว"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="วงจรตัวต้านทานและตัวเก็บประจุ",
)
class SteadyCapacitorCharge(PhysicsSheet):
    def expr(self, rng):
        voltage, c1, c2, cp = (
            rng.choice((6, 12, 18, 24)),
            rng.choice((1, 2, 3)),
            rng.choice((4, 5, 6)),
            rng.choice((2, 8)),
        )
        charge = q14.solve(voltage=voltage, c1=c1, c2=c2, cp=cp)
        across = Fraction(2 * voltage, 3)
        return _named_draw(
            14,
            MathDraw(
                "",
                _tex(charge),
                prompt=(
                    f"แหล่งจ่าย {voltage} V ต่ออนุกรมกับชุดตัวต้านทาน (3 Ω ขนาน 6 Ω) แล้วต่อกับชุดแขนงขนานสามแขนง "
                    f"ได้แก่ (2.5 Ω อนุกรม 1.5 Ω), ({c1} µF อนุกรม {c2} µF), และ {cp} µF "
                    f"หลังเข้าสู่สภาวะคงตัว ประจุบนตัวเก็บประจุ {c2} µF เท่าใดในหน่วย µC "
                    "จุดต่อกลางระหว่างตัวเก็บประจุอนุกรมมีประจุสุทธิเป็นศูนย์"
                ),
                hint=r"V_C=V\frac{4}{2+4},\quad Q=\frac{C_1C_2}{C_1+C_2}V_C",
                distractors=[
                    _tex(c2 * across),
                    _tex(Fraction(c1 * c2, c1 + c2) * voltage),
                    _tex((c1 + c2) * across),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q15",
    display_name={"th": "กำลังไฟฟ้าหลังยืดลวด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สภาพต้านทานและกำลังไฟฟ้า",
)
class StretchedWire(PhysicsSheet):
    def expr(self, rng):
        x = rng.randint(2, 8)
        return _named_draw(
            15,
            MathDraw(
                "",
                _tex(q15.solve(x=x)),
                prompt=(
                    f"ลวดมีความยาวเพิ่มเป็น {x} เท่า ปริมาตรและสภาพต้านทานยังคงเดิม "
                    "นำไปต่อกับความต่างศักย์เดิม กำลังไฟฟ้าใหม่เป็นกี่เท่าของเดิม"
                ),
                hint=r"AL=\text{constant},\quad R=\rho L/A,\quad P=V^2/R",
                distractors=[_tex(Fraction(1, x)), str(x), str(x * x)],
            ),
        )


@question_type(
    "phys.posn2560_q16",
    display_name={"th": "เทียบความหนาแน่นจากปริมาตรที่ลอยพ้นน้ำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การลอยตัวและความหนาแน่น",
)
class FloatingDensityRatio(PhysicsSheet):
    def expr(self, rng):
        above = rng.choice((Fraction(1, 4), Fraction(1, 5), Fraction(1, 3)))
        submerged = rng.choice((Fraction(1, 2), Fraction(2, 3), Fraction(3, 5)))
        ratio = q16.solve(
            above_num=above.numerator,
            above_den=above.denominator,
            sub_num=submerged.numerator,
            sub_den=submerged.denominator,
        )
        return _named_draw(
            16,
            MathDraw(
                rf"V_{{1,\mathrm{{air}}}}/V_1={_tex(above)},\quad V_{{2,\mathrm{{water}}}}/V_2={_tex(submerged)}",
                _tex(ratio),
                prompt=(
                    "วัตถุตันสองชิ้นลอยนิ่งในน้ำ มีเศษส่วนปริมาตรพ้นน้ำของชิ้นแรกและจมน้ำของชิ้นที่สองดังนี้ "
                    "จงหาอัตราส่วนความหนาแน่นของชิ้นแรกต่อชิ้นที่สอง"
                ),
                hint=r"\rho_{\mathrm{body}}/\rho_{\mathrm{water}}=V_{\mathrm{sub}}/V",
                distractors=[
                    _tex(above / submerged),
                    _tex(submerged / (1 - above)),
                    _tex((1 - above) / (1 - submerged)),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q17",
    display_name={"th": "ความดันแก๊สเหนือคอลัมน์ปรอท"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลความดันของของไหล",
)
class TrappedGasPressure(PhysicsSheet):
    def expr(self, rng):
        atmosphere, height = rng.choice((740, 750, 760)), rng.choice((10, 20, 30, 40))
        pressure = q17.solve(atmosphere=atmosphere, height=height)
        return _named_draw(
            17,
            MathDraw(
                "",
                str(pressure),
                prompt=(
                    f"หลอดแก้วคว่ำในอ่างปรอทเปิด ผิวปรอทในหลอดสูงกว่าผิวในอ่าง {height} mm "
                    f"ความดันบรรยากาศ {atmosphere} mmHg ความดันแก๊สเหนือปรอทในหลอดเป็นเท่าใดในหน่วย mmHg"
                ),
                hint=r"P_{\mathrm{gas}}+h=P_{\mathrm{atm}}",
                distractors=[str(atmosphere + height), str(atmosphere), str(height)],
            ),
        )


@question_type(
    "phys.posn2560_q18",
    display_name={"th": "อุณหภูมิน้ำมันก่อนผสมน้ำร้อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลความร้อนในระบบปิด",
)
class OilWaterTemperature(PhysicsSheet):
    def expr(self, rng):
        oil_mass = rng.choice((0.075, 0.15, 0.225))
        factor, initial = rng.choice((2, 3, 4)), rng.choice((10, 15, 20))
        hot = initial * (factor + (factor - 1) * oil_mass * 1400 / 1050)
        answer = q18.solve(oil_mass=oil_mass, water_temp=hot, factor=factor)
        return _named_draw(
            18,
            MathDraw(
                "",
                _tex(answer),
                prompt=(
                    f"ภาชนะฉนวนบรรจุน้ำมัน {show(oil_mass * 1000)} g ผสมน้ำ 250 g ที่ {show(hot)} °C "
                    f"อุณหภูมิสมดุลในหน่วย °C เป็น {factor} เท่าของอุณหภูมิน้ำมันเดิม "
                    "อุณหภูมิน้ำมันเดิมกี่ °C (c น้ำมัน = 1400, c น้ำ = 4200 J/(kg K) "
                    "ไม่คิดความจุความร้อนภาชนะและการเปลี่ยนสถานะ)"
                ),
                hint=r"m_wc_w(T_w-kT)=m_oc_o(kT-T)",
                distractors=[
                    _tex(hot / factor),
                    _tex(initial * factor),
                    _tex(hot / (2 * factor - 1)),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q19",
    display_name={"th": "จำนวนโมเลกุลจากกฎแก๊สอุดมคติ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="จำนวนอนุภาคของแก๊สอุดมคติ",
)
class GasMoleculeCount(PhysicsSheet):
    def expr(self, rng):
        volume, pressure, temp = (
            rng.choice((0.05, 0.075, 0.1, 0.15)),
            rng.choice((0.05, 0.1, 0.2)),
            rng.choice((27, 77, 127)),
        )
        count = q19.solve(volume=volume, pressure_atm=pressure, celsius=temp)
        fmt = lambda n: rf"{n / 1e23:.2f}\times10^{{23}}"
        return _named_draw(
            19,
            MathDraw(
                "",
                fmt(count),
                prompt=(
                    f"แก๊สอุดมคติปริมาตร {show(volume * 1000)} L ความดัน {show(pressure)} atm อุณหภูมิ {temp} °C "
                    "มีจำนวนโมเลกุลเท่าใด ตอบในรูป A×10²³ โดยปัด A สองตำแหน่งทศนิยม "
                    "(1 atm = 101300 Pa, R = 8.31 J/(mol K), Nₐ = 6.02×10²³ mol⁻¹, T = t + 273)"
                ),
                hint=r"N=\frac{PVN_A}{RT}",
                distractors=[
                    fmt(count * (temp + 273) / temp),
                    fmt(count / 1000),
                    fmt(count * 1000),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q20",
    display_name={"th": "เลนส์กับกระจกนูนให้ภาพกลับหัวตรงระนาบวัตถุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเกิดภาพซ้ำของเลนส์และกระจก",
)
class LensMirrorInvertedImage(PhysicsSheet):
    def expr(self, rng):
        u, d, radius = rng.choice((24, 30, 40)), rng.choice((4, 5, 8)), rng.choice((12, 15, 20))
        focal = q20.solve(u=u, d=d, radius=radius)
        return _named_draw(
            20,
            MathDraw(
                "",
                _tex(focal),
                prompt=(
                    f"วัตถุอยู่หน้าเลนส์บางนูน {u} cm กระจกนูนอยู่หลังเลนส์ {d} cm รัศมีความโค้ง {radius} cm "
                    "หลังแสงผ่านเลนส์ สะท้อนกระจก แล้วกลับผ่านเลนส์อีกครั้ง เกิดภาพกลับหัวในระนาบเดียวกับวัตถุ "
                    "จงหาความยาวโฟกัสเลนส์ในหน่วย cm (ใช้แสงใกล้แกน)"
                ),
                hint=r"v=d+R,\quad 1/f=1/u+1/v",
                distractors=[
                    _tex(Fraction(u * d, u + d)),
                    _tex(Fraction(u * (2 * d + radius), 2 * u + 2 * d + radius)),
                    _tex(Fraction(u * (d + radius), d + radius - u)) if d + radius != u else str(u),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q01",
    display_name={"th": "มิติของสัมประสิทธิ์แรงต้าน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การวิเคราะห์มิติ",
)
class DragDimensions(PhysicsSheet):
    def expr(self, rng):
        power = rng.randint(1, 5)
        m, length, time = q01.solve(power=power)
        fmt = lambda mm, ll, tt: rf"M^{{{mm}}}L^{{{ll}}}T^{{{tt}}}"
        return _named_draw(
            1,
            MathDraw(
                rf"F=kv^{{{power}}}A",
                fmt(m, length, time),
                prompt=(
                    "แรงต้าน F ขึ้นกับอัตราเร็ว v และพื้นที่หน้าตัด A ตามสมการ "
                    "มิติของ k เป็นเท่าใด (M แทนมวล L แทนความยาว T แทนเวลา)"
                ),
                hint=r"[F]=MLT^{-2},\quad [v]=LT^{-1},\quad [A]=L^2",
                distractors=[
                    fmt(m, length + 2, time),
                    fmt(m, length, -time - 1),
                    fmt(m, -length, -time),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q02",
    display_name={"th": "ความเร็วและความเร่งตามแนวสัมผัสของรางลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความเร่งตามแนวสัมผัส",
)
class SlideTangentialAcceleration(PhysicsSheet):
    def expr(self, rng):
        speed = rng.choice((4, 6, 8, 10, 12))
        drop = Fraction(speed**2, 20)
        sine = rng.choice((Fraction(3, 5), Fraction(4, 5), Fraction(1, 2)))
        v, a = q02.solve(drop=float(drop), sine=float(sine), g=10)
        pair = lambda x, y: rf"\left({_tex(x)},\ {_tex(y)}\right)"
        return _named_draw(
            2,
            MathDraw(
                rf"\sin\theta={_tex(sine)}",
                pair(v, a),
                prompt=(
                    f"เด็กเริ่มไถลจากหยุดนิ่งบนรางลื่น เมื่อระดับลดลง {show(drop)} m "
                    "รางทำมุม θ กับแนวระดับ จงหาคู่อันดับ (อัตราเร็ว m/s, ขนาดความเร่งตามแนวสัมผัส m/s²) "
                    "ณ จุดนั้น (g = 10 m/s² ไม่คิดแรงต้าน)"
                ),
                hint=r"v^2=2g\Delta h,\quad a_t=g\sin\theta",
                distractors=[pair(v, 10), pair(v / 2, a), pair(v, 10 * (1 - sine))],
            ),
        )


@question_type(
    "phys.posn2560_q05",
    display_name={"th": "แรงปกติเฉลี่ยระหว่างลูกบอลกระดอน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การดลของแรงเฉลี่ย",
)
class AverageBounceForce(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 4)
        before, after = rng.choice((4, 6, 8, 10)), rng.choice((2, 4, 6))
        drop, rebound = Fraction(before**2, 20), Fraction(after**2, 20)
        contact = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)))
        force = q05.solve(
            mass=mass, drop=float(drop), rebound=float(rebound), contact=float(contact), g=10
        )
        return _named_draw(
            5,
            MathDraw(
                "",
                _tex(force),
                prompt=(
                    f"ปล่อยลูกบอลมวล {mass} kg จากความสูง {show(drop)} m กระทบพื้นแล้วกระดอนสูง {show(rebound)} m "
                    f"ช่วงสัมผัสพื้นนาน {show(contact)} s แรงปกติเฉลี่ยที่พื้นกระทำต่อลูกบอลมีค่าเท่าใดในหน่วย N "
                    "(g = 10 m/s² ไม่คิดแรงต้าน และไม่คิดการเปลี่ยนความสูงระหว่างสัมผัสพื้น)"
                ),
                hint=r"(\overline{N}-mg)\Delta t=m(v_{\mathrm{up}}+v_{\mathrm{down}})",
                distractors=[
                    _tex(mass * (before + after) / contact),
                    _tex(mass * abs(before - after) / contact + mass * 10),
                    _tex(mass * before / contact + mass * 10),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q08",
    display_name={"th": "ผลของแรงต้านต่อวิถีโพรเจกไทล์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="โพรเจกไทล์เมื่อมีแรงต้านอากาศ",
)
class ProjectileDrag(ChoiceType):
    sheet_id = "posn2560_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2560)"

    def compose(self, rng):
        vx, vy, k = (
            rng.choice((8, 10, 15, 20)),
            rng.choice((8, 10, 15)),
            rng.choice((0.1, 0.2, 0.5)),
        )
        height_ratio, range_ratio = q08.solve(vx=vx, vy=vy, decay=k)
        assert 0 < height_ratio < 1 and 0 < range_ratio < 1
        return (
            f"ยิงวัตถุจากพื้นด้วยความเร็วแนวระดับ {vx} m/s และแนวดิ่งขึ้น {vy} m/s "
            f"เมื่ออากาศนิ่งมีแรงต้านตรงข้ามความเร็ว ขนาด mkv โดย k = {k} s⁻¹ "
            "ให้ H และ R เป็นความสูงสูงสุดและพิสัยที่กลับถึงพื้นเดิม "
            "ส่วน H₀ และ R₀ เป็นค่าของการยิงด้วยความเร็วต้นเดียวกันในสุญญากาศ ข้อใดถูกต้อง",
            "H < H₀ และ R < R₀",
            (
                named("phys.drag_range_unchanged", "H < H₀ และ R = R₀"),
                named("phys.drag_height_unchanged", "H = H₀ และ R < R₀"),
                named("phys.drag_increases_motion", "H > H₀ และ R > R₀"),
            ),
        )


@question_type(
    "phys.posn2560_q21",
    display_name={"th": "มุมยิงจากทิศความเร็วระหว่างทาง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความเร็วของโพรเจกไทล์ระหว่างทาง",
)
class ProjectileLaunchAngle(PhysicsSheet):
    PROVENANCE = _written_provenance(1)

    def expr(self, rng):
        beta = rng.choice((30, 45, 60))
        fraction = rng.choice((Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)))
        squared = q21.solve(fraction=float(fraction), beta=beta)
        angle = rf"\arctan\sqrt{{{_tex(squared)}}}"
        return _named_draw(
            21,
            MathDraw(
                rf"h/H_{{\max}}={_tex(fraction)}",
                angle,
                prompt=(
                    f"ยิงวัตถุจากพื้น เมื่อกำลังขึ้นถึงเศษส่วนความสูงสูงสุดตามสมการ ทิศความเร็วทำมุม {beta}° กับแนวระดับ "
                    "มุมยิงเริ่มต้นเป็นเท่าใด (ไม่คิดแรงต้าน)"
                ),
                hint=r"v_x=u_x,\quad v_y^2=u_y^2(1-h/H_{\max})",
                distractors=[
                    rf"{beta}^\circ",
                    rf"\arctan\sqrt{{{_tex(squared * (1 - fraction) ** 2)}}}",
                    rf"\arctan\sqrt{{{_tex(1 / squared)}}}",
                ],
            ),
        )


@question_type(
    "phys.posn2560_q22",
    display_name={"th": "แรงผลักขั้นต่ำให้ก้อนเล็กเกาะผนัง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเสียดทานบนผนังที่เร่ง",
)
class AcceleratingWall(PhysicsSheet):
    PROVENANCE = _written_provenance(2)

    def expr(self, rng):
        big, small, mu = rng.randint(3, 10), rng.randint(1, 2), rng.choice((0.2, 0.25, 0.4, 0.5))
        force = q22.solve(big=big, small=small, mu=mu, g=10)
        return _named_draw(
            22,
            MathDraw(
                "",
                _tex(force),
                prompt=(
                    f"กล่อง M = {big} kg อยู่บนพื้นระดับลื่น ก้อน m = {small} kg แตะผนังแนวดิ่งด้านขวาของกล่อง "
                    f"สัมประสิทธิ์เสียดทานสถิตระหว่างก้อนกับผนัง {mu} "
                    "ต้องผลัก M ไปทางขวาด้วยแรงอย่างน้อยกี่ N เพื่อให้ m ไม่ไถลลง (g = 10 m/s²)"
                ),
                hint=r"\mu ma\ge mg,\quad F=(M+m)a",
                distractors=[
                    _tex(big * 10 / mu),
                    _tex(small * 10 / mu),
                    _tex((big + small) * 10 * mu),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q23",
    display_name={"th": "น้ำหนักคานไม่สม่ำเสมอจากสองสมดุล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลคานเมื่อเปลี่ยนจุดรองรับ",
)
class NonuniformRod(PhysicsSheet):
    PROVENANCE = _written_provenance(3)

    def expr(self, rng):
        length, pivot = rng.choice(((3, 1), (4, 1), (4, 2), (5, 2), (6, 1), (6, 4)))
        ratio = q23.solve(length=length, pivot=pivot)
        return _named_draw(
            23,
            MathDraw(
                "",
                _tex(ratio),
                prompt=(
                    f"คานไม่สม่ำเสมอ AB ยาว {length}L สมดุลแนวระดับด้วยเชือกแนวดิ่งที่ A และ B แรงตึงที่ A เท่ากับ T "
                    f"ถอดเชือก A แล้วรองคานที่ระยะ {pivot}L จาก A คานยังสมดุลและแรงตึงเชือก B เท่ากับ T "
                    "น้ำหนักคานเป็นกี่เท่าของ T"
                ),
                hint=r"Wx=(W-T)\ell,\quad Wx=(W-T)a+T\ell",
                distractors=[
                    _tex(Fraction(length, length - pivot)),
                    _tex(Fraction(length, pivot)),
                    _tex(Fraction(length + pivot, length - pivot)),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q24",
    display_name={"th": "แรงลัพธ์ที่ขอบวงกลมของรางลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงลัพธ์ในการเคลื่อนที่ตามรางวงกลม",
)
class CircularTrackForce(PhysicsSheet):
    PROVENANCE = _written_provenance(4)

    def expr(self, rng):
        drop = rng.choice((1, 2, 3, 4))
        coefficient = q24.solve(drop_ratio=drop)
        squared = round(coefficient**2)
        return _named_draw(
            24,
            MathDraw(
                "",
                rf"\sqrt{{{squared}}}",
                prompt=(
                    "มวลจุด m เริ่มจากหยุดนิ่งบนรางลื่น รางมีช่วงวงกลมรัศมี R ในระนาบดิ่ง "
                    f"ตำแหน่งปล่อยสูงกว่าจุด B ซึ่งเป็นจุดขวาสุดของวงกลม {drop}R "
                    "เมื่อถึง B วัตถุเคลื่อนที่ในแนวดิ่ง ขนาดแรงลัพธ์เป็นกี่เท่าของ mg (ไม่มีแรงต้าน)"
                ),
                hint=r"v^2=2g\Delta h,\quad F=\sqrt{(mv^2/R)^2+(mg)^2}",
                distractors=[str(2 * drop), str(2 * drop + 1), rf"\sqrt{{{1 + drop**2}}}"],
            ),
        )


@question_type(
    "phys.posn2560_q25",
    display_name={"th": "งานจากกราฟแรงที่มีส่วนลบ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พื้นที่แบบมีเครื่องหมายใต้กราฟแรง",
)
class SignedForceWork(PhysicsSheet):
    PROVENANCE = _written_provenance(5)

    def expr(self, rng):
        ramp, plateau, tail = rng.choice((1, 2)), rng.choice((2, 3, 4)), rng.choice((1, 2))
        pos, neg = rng.choice((2, 4, 6)), rng.choice((2, 4))
        work = q25.solve(ramp=ramp, plateau=plateau, tail=tail, positive=pos, negative=neg)
        end1, end2 = ramp + plateau, ramp + plateau + tail
        points = rf"(0,0),({ramp},{pos}),({end1},{pos}),({end1},-{neg}),({end2},0)"
        return _named_draw(
            25,
            MathDraw(
                points,
                _tex(work),
                prompt=(
                    "กราฟแรง F (N) กับตำแหน่ง x (m) เชื่อมจุด (x,F) ที่ให้ตามลำดับด้วยเส้นตรง "
                    f"ที่ x = {end1} มีการกระโดดของแรง วัตถุเคลื่อนที่ไปทาง +x จาก x = 0 ถึง {end2} m "
                    "งานของแรงนี้เท่าใดในหน่วย J"
                ),
                hint=r"W=\int F\,dx",
                distractors=[
                    _tex(pos * ramp / 2 + pos * plateau + neg * tail / 2),
                    _tex(pos * end2),
                    _tex(work - pos * ramp / 2),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q26",
    display_name={"th": "แบ่งประจุระหว่างทรงกลมตัวนำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ศักย์ไฟฟ้าของทรงกลมตัวนำที่เชื่อมกัน",
)
class ConnectedSpheres(PhysicsSheet):
    PROVENANCE = _written_provenance(6)

    def expr(self, rng):
        denominator = rng.randint(2, 9)
        fraction = Fraction(1, denominator)
        ratio = q26.solve(num=1, den=denominator)
        return _named_draw(
            26,
            MathDraw(
                rf"q_a={_tex(fraction)}Q",
                _tex(ratio),
                prompt=(
                    "ทรงกลมตัวนำรัศมี a และ b แต่ละลูกมีประจุ +Q อยู่ห่างกันมาก "
                    "เมื่อต่อด้วยลวดจนสมดุล ทรงกลมรัศมี a มีประจุดังสมการ จงหา b/a "
                    "ละเลยประจุบนลวดและอิทธิพลเหนี่ยวนำระหว่างทรงกลม"
                ),
                hint=r"q_a+q_b=2Q,\quad q_a/a=q_b/b",
                distractors=[str(denominator - 1), str(denominator), _tex(1 / ratio)],
            ),
        )


@question_type(
    "phys.posn2560_q27",
    display_name={"th": "กระแสในวงจรสามแขนงที่มีแบตเตอรี่"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎของเคอร์ชอฟฟ์และขั้วแบตเตอรี่",
)
class ThreeBranchCircuit(PhysicsSheet):
    PROVENANCE = _written_provenance(7)

    def expr(self, rng):
        i1, i3 = rng.choice((1, 2)), rng.choice((1, 2, 3, 4))
        e1, r1, r2 = rng.choice((3, 4, 5)), 1, 2
        potential = e1 - i1 * r1
        e2 = r2 * (i1 + i3) - potential
        if e2 <= 0:
            e2 += 6
        answer = q27.solve(e1=e1, r1=r1, e2=e2, r2=r2, i1=i1)
        return _named_draw(
            27,
            MathDraw(
                "",
                _tex(answer),
                prompt=(
                    "วงจรมีสามแขนงขนานระหว่างจุดซ้าย L กับขวา R "
                    f"แขนงบนมีแบตเตอรี่ {e1} V ขั้วบวกอยู่ขวา ต่ออนุกรมตัวต้านทาน 1 Ω กระแส I₁ = {i1} A ไปขวา "
                    f"แขนงกลางมีแบตเตอรี่ {e2} V ขั้วบวกอยู่ซ้าย ต่ออนุกรมตัวต้านทาน 2 Ω "
                    "แขนงล่างมีแบตเตอรี่ไม่ทราบค่า ขั้วบวกอยู่ขวา ต่ออนุกรมตัวต้านทาน 4 Ω "
                    "กระแส I₃ ที่ไหลไปขวาในแขนงล่างเท่าใดในหน่วย A"
                ),
                hint=r"V_R-V_L=E_1-I_1R_1=I_2R_2-E_2,\quad I_3=I_2-I_1",
                distractors=[_tex(answer + 2 * i1), _tex(Fraction(e2, r2) - i1), _tex(-answer)],
            ),
        )


@question_type(
    "phys.posn2560_q28",
    display_name={"th": "อัตราการลดระดับน้ำจากอัตราการไหล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความต่อเนื่องของการไหล",
)
class TankSurfaceSpeed(PhysicsSheet):
    PROVENANCE = _written_provenance(8)

    def expr(self, rng):
        numerator, radius = rng.choice((2, 4, 6, 8, 12)), rng.choice((1, 2, 3))
        speed = q28.solve(q_num=numerator, q_den=100, radius=radius)
        return _named_draw(
            28,
            MathDraw(
                rf"Q=\frac{{{numerator}\pi}}{{100}}\ \mathrm{{m^3/s}}",
                _tex(speed),
                prompt=(
                    f"ถังทรงกระบอกตั้งตรงรัศมี {radius} m มีน้ำไหลออกทางรูด้านล่างด้วยอัตราปริมาตร Q ดังสมการ "
                    "อัตราเร็วที่ระดับผิวน้ำลดลงเป็นเท่าใดในหน่วย cm/s"
                ),
                hint=r"Q=\pi R^2\left|dh/dt\right|",
                distractors=[
                    _tex(speed / 100),
                    _tex(Fraction(numerator, radius)),
                    _tex(numerator * radius**2),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q29",
    display_name={"th": "อัตราส่วนการขยายตัวของทรงกระบอกและทรงกลม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การขยายตัวเชิงความร้อนและเรขาคณิต",
)
class CylinderSphereExpansion(PhysicsSheet):
    PROVENANCE = _written_provenance(9)

    def expr(self, rng):
        radius_ratio = rng.choice(
            (Fraction(1), Fraction(2), Fraction(1, 2), Fraction(3, 2), Fraction(3))
        )
        result = q29.solve(radius_num=radius_ratio.numerator, radius_den=radius_ratio.denominator)
        return _named_draw(
            29,
            MathDraw(
                rf"r_{{\mathrm{{cyl}}}}/r_{{\mathrm{{sphere}}}}={_tex(radius_ratio)}",
                _tex(result),
                prompt=(
                    "ทรงกระบอกตันและทรงกลมตันทำจากวัสดุเดียวกัน มีปริมาตรเริ่มต้นเท่ากันและอัตราส่วนรัศมีดังสมการ "
                    "ให้ความร้อนจนทั้งสองมีอุณหภูมิเพิ่มเท่ากันและขยายตัวเหมือนกันทุกทิศ "
                    "ความสูงทรงกระบอกที่เพิ่มขึ้นเป็นกี่เท่าของเส้นผ่านศูนย์กลางทรงกลมที่เพิ่มขึ้น"
                ),
                hint=r"\pi r_c^2 h=\frac43\pi r_s^3,\quad \Delta h/\Delta d=h/(2r_s)",
                distractors=[
                    _tex(1 / result),
                    _tex(2 * result),
                    _tex(Fraction(2, 3) / radius_ratio),
                ],
            ),
        )


@question_type(
    "phys.posn2560_q30",
    display_name={"th": "หาโฟกัสจากการเลื่อนเลนส์และฉาก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมการเลนส์เมื่อเลื่อนเลนส์และฉาก",
)
class MovingLensScreen(PhysicsSheet):
    PROVENANCE = _written_provenance(10)

    def expr(self, rng):
        scale = rng.randint(1, 12)
        v, a, b = 15 * scale, 2 * scale, scale
        focal = q30.solve(image=v, lens_move=a, screen_move=b)
        return _named_draw(
            30,
            MathDraw(
                "",
                _tex(focal),
                prompt=(
                    f"วัตถุคงที่หน้าเลนส์นูนบาง เกิดภาพคมชัดบนฉากห่างเลนส์ {v} cm "
                    f"เลื่อนเลนส์ออกห่างวัตถุ {a} cm และเลื่อนฉากเข้าหาวัตถุ {b} cm โดยวัดการเลื่อนทั้งสองเทียบกับห้อง "
                    "พบภาพคมชัดอีกครั้ง ความยาวโฟกัสเลนส์เท่าใดในหน่วย cm"
                ),
                hint=r"u_2=u_1+a,\quad v_2=v_1-a-b,\quad 1/u_1+1/v_1=1/u_2+1/v_2",
                distractors=[
                    _tex(Fraction(v * (v - a - b), 2 * v - a - b)),
                    _tex(v - a - b),
                    _tex(focal * 2),
                ],
            ),
        )
