"""Seeded variants of the reviewed POSN physics 2568 camp selection paper."""

from fractions import Fraction
from math import isqrt, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2568_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2568_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2568_physics import q21, q22, q23, q24, q25

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def radical(value):
    """Exact reduced radical of a nonnegative rational."""
    value = Fraction(value)
    square, remainder = 1, value.numerator * value.denominator
    divisor = 2
    while divisor <= isqrt(remainder):
        while remainder % (divisor * divisor) == 0:
            square *= divisor
            remainder //= divisor * divisor
        divisor += 1
    coefficient = Fraction(square, value.denominator)
    if remainder == 1:
        return tex(coefficient)
    numerator = (
        str(coefficient.numerator) if coefficient.numerator != 1 else ""
    ) + rf"\sqrt{{{remainder}}}"
    return (
        numerator
        if coefficient.denominator == 1
        else rf"\frac{{{numerator}}}{{{coefficient.denominator}}}"
    )


def _decimal(value):
    """Plain decimal TeX for a value with at most six decimal places."""
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


def sci(value, force=False):
    """A rational as a plain decimal when it is short and of moderate size,
    otherwise as mantissa × 10^n; a mantissa that does not terminate stays a
    fraction, so nothing is rounded."""
    value = Fraction(value)
    if value == 0:
        return "0"
    if not force and (value * 1000).denominator == 1 and abs(value) < 10**6:
        return _decimal(value) if value.denominator != 1 else str(value)
    if not force and Fraction(1, 1000) <= abs(value) < 10**6 and (value * 10**6).denominator != 1:
        return tex(value)
    power = 0
    while abs(value) >= 10:
        value, power = value / 10, power + 1
    while abs(value) < 1:
        value, power = value * 10, power - 1
    if value == 1:
        return rf"10^{{{power}}}"
    mantissa = _decimal(value) if (value * 10**6).denominator == 1 else tex(value)
    return rf"{mantissa}\times10^{{{power}}}"


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


def pi_sci(value):
    """value * pi as (sign) mantissa pi x 10^n, the mantissa exact."""
    value = Fraction(value)
    sign = "-" if value < 0 else ""
    value = abs(value)
    power = 0
    while value >= 10:
        value, power = value / 10, power + 1
    while value < 1:
        value, power = value * 10, power - 1
    mantissa = _decimal(value) if (value * 10**6).denominator == 1 else tex(value)
    mantissa = "" if mantissa == "1" else mantissa
    return rf"{sign}{mantissa}\pi\times10^{{{power}}}"


def over_pi(value):
    """value / pi as exact TeX."""
    value = Fraction(value)
    bottom = rf"{value.denominator}\pi" if value.denominator != 1 else r"\pi"
    return rf"\frac{{{value.numerator}}}{{{bottom}}}"


def times_pi(value, power=""):
    """value * pi (or pi^2 with power="^2") as exact TeX."""
    value = Fraction(value)
    if value == 0:
        return "0"
    top = "" if abs(value.numerator) == 1 else str(abs(value.numerator))
    sign = "-" if value < 0 else ""
    if value.denominator == 1:
        return rf"{sign}{top}\pi{power}"
    return rf"{sign}\frac{{{top}\pi{power}}}{{{value.denominator}}}"


def pi_radical(square):
    """pi * sqrt(square) as exact TeX."""
    root = radical(square)
    return r"\pi" if root == "1" else rf"{root}\pi"


def three_figures(value):
    """A positive float to three significant figures, as plain text."""
    digits = 3 - len(str(int(value))) if value >= 1 else 3
    return f"{round(value, max(digits, 0)):.{max(digits, 0)}f}"


SLIPS = {
    1: ("phys.direction_height_max_height", "phys.direction_height_doubled", "phys.direction_height_halved"),
    2: ("phys.offset_impact_target_speed", "phys.offset_impact_head_on", "phys.offset_impact_stops"),
    3: ("phys.spring_closest_initial_speed", "phys.spring_closest_mass_dropped", "phys.spring_closest_elastic_final"),
    4: ("phys.ring_axis_direction_reversed", "phys.ring_force_point_distance", "phys.ring_force_centre_charge"),
    5: ("phys.ring_current_pi_dropped", "phys.ring_current_half_period", "phys.ring_current_charge_times_rate"),
    6: ("phys.ring_field_current_no_period", "phys.ring_field_radius_squared", "phys.ring_field_doubled"),
    7: ("phys.split_parallel_half", "phys.split_parallel_whole", "phys.split_parallel_uneven"),
    8: ("phys.self_equal_series_sum", "phys.self_equal_parallel", "phys.self_equal_negative_root"),
    9: ("phys.thermal_resistance_inverted", "phys.thermal_resistance_conductivity_on_top", "phys.thermal_resistance_area_units"),
    10: ("phys.junction_simple_average", "phys.junction_area_ignored", "phys.junction_weights_swapped"),
    11: ("phys.accel_tank_accel_ignored", "phys.accel_tank_sign", "phys.accel_tank_gauge"),
    12: ("phys.jet_head_from_bottom", "phys.jet_range_halved", "phys.jet_range_g_halved"),
    13: ("phys.beam_intensity_not_squared", "phys.beam_intensity_inverted", "phys.beam_intensity_inverted_linear"),
    14: ("phys.longitudinal_used_lateral_far", "phys.longitudinal_used_lateral_near", "phys.longitudinal_squared"),
    15: ("phys.stretch_radius_ignored", "phys.stretch_radius_sign", "phys.stretch_radius_not_squared"),
    16: ("phys.charging_emf_heat_only", "phys.charging_emf_capacitor_only", "phys.charging_emf_subtracted"),
    17: ("phys.series_sum_not_inverted", "phys.series_first_only", "phys.series_pi_not_squared"),
    18: ("phys.echo_away_tau_ignored", "phys.echo_away_sign", "phys.echo_away_one_way"),
    19: ("phys.plate_force_full_field", "phys.plate_force_energy_as_force", "phys.plate_force_charge_not_squared"),
    20: ("phys.equator_gravity_added", "phys.equator_gravity_pi_not_squared", "phys.equator_rotation_ignored"),
    21: ("phys.equator_rotation_ignored", "phys.equator_gravity_added", "phys.equator_term_halved"),
    22: ("phys.kepler_mass_inverted", "phys.kepler_mass_ignored", "phys.kepler_wrong_power"),
    23: ("phys.triangle_single_pair", "phys.triangle_binary_formula", "phys.triangle_period_halved"),
    24: ("phys.viscous_torricelli", "phys.poiseuille_factor_two", "phys.poiseuille_radius_not_squared"),
    25: ("phys.hairpin_one_wire", "phys.hairpin_wires_ignored", "phys.hairpin_full_infinite_wires"),
}


def draw(number_, answer, prompt, hint, slips):
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number_], slips)],
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2568_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2568)"


def _type(n, title, topic):
    return question_type(
        f"phys.posn2568_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


# (launch angle from vertical, sin^2 of elevation) and (A angle from vertical, tan^2 of elevation)
LAUNCHES = ((45, Fraction(1, 2)), (30, Fraction(3, 4)))
AT_A = ((90, Fraction(0)), (60, Fraction(1, 3)), (45, Fraction(1)))


@_type(1, "ความสูงที่ทิศความเร็วโพรเจกไทล์เปลี่ยนไป", "การเคลื่อนที่แบบโพรเจกไทล์")
class DirectionHeight(PhysicsSheet):
    def expr(self, rng):
        while True:
            (launch, sin2), (at_a, tan2) = rng.choice(LAUNCHES), rng.choice(AT_A)
            if tan2 < sin2 / (1 - sin2):
                break
        speed = 2 * rng.randint(2, 15)
        exact = speed * speed * (sin2 - (1 - sin2) * tan2) / 20
        answer = agree(q01.solve(speed=speed, sin2=float(sin2), tan2=float(tan2)), exact)
        where = "อยู่ในแนวระดับ (จุดสูงสุด)" if at_a == 90 else f"ทำมุม {at_a}° กับแนวดิ่ง (ยังเคลื่อนขึ้น)"
        return draw(
            1,
            tex(answer),
            f"โพรเจกไทล์ออกจากจุด O บนพื้นระดับด้วยอัตราเร็ว {speed} m/s ทำมุม {launch}° กับแนวดิ่ง ที่จุด A ความเร็ว{where} จุด A สูงจากพื้นกี่ m ให้ g=10 m/s²",
            r"v_x=u_x,\quad v_y=v_x\tan\beta,\quad h=\frac{u_y^2-v_y^2}{2g}",
            [tex(speed * speed * sin2 / 20), tex(2 * exact), tex(exact / 2)],
        )


@_type(2, "อัตราเร็วของลูกที่ชนหลังชนเยื้องแบบยืดหยุ่น", "แรงดลตามแนวศูนย์กลางของผิวเกลี้ยง")
class GlancingStriker(PhysicsSheet):
    def expr(self, rng):
        sine = rng.choice((Fraction(1, 2), Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13)))
        speed = sine.denominator * rng.randint(1, 4)
        answer = agree(q02.solve(speed=speed, sine=float(sine)), speed * sine)
        angle = "30°" if sine == Fraction(1, 2) else f"θ (sin θ = {number(sine)})"
        return draw(
            2,
            tex(answer),
            f"ทรงกลมเกลี้ยง A และ B มวลเท่ากัน A เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s ชน B ที่อยู่นิ่งแบบยืดหยุ่น ขณะชนแนวเส้นต่อศูนย์กลางทำมุม {angle} กับทิศเดิมของ A หลังชน A มีอัตราเร็วกี่ m/s",
            r"v_B=u\cos\theta,\quad v_A=u\sin\theta",
            [radical(speed * speed * (1 - sine * sine)), str(speed), "0"],
        )


@_type(3, "ความเร็วขณะสปริงหดมากที่สุด", "การชนผ่านสปริงและโมเมนตัม")
class SpringClosest(PhysicsSheet):
    def expr(self, rng):
        small, big = rng.sample(range(1, 10), 2)
        speed = rng.randint(2, 15)
        exact = Fraction(small * speed, small + big)
        answer = agree(q03.solve(small=small, big=big, speed=speed), exact)
        return draw(
            3,
            tex(answer),
            f"มวล {small} kg เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s บนพื้นลื่น เข้าชนอัดสปริงเบาที่ติดอยู่กับมวล {big} kg ซึ่งอยู่นิ่ง ขณะที่สองมวลเข้าใกล้กันมากที่สุด มวล {small} kg มีอัตราเร็วกี่ m/s",
            r"mu=(m+M)v",
            [str(speed), tex(Fraction(small * speed, big)), tex(Fraction((small - big) * speed, small + big))],
        )


TRIPLES = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10))


@_type(4, "สนามไฟฟ้าบนแกนวงแหวนด้านตรงข้าม", "การอินทิเกรตสนามและสมมาตร")
class RingAxisField(PhysicsSheet):
    def expr(self, rng):
        radius, distance, hyp = rng.choice(TRIPLES)
        charge = rng.randint(1, 9)
        exact = -Fraction(9 * charge * distance, hyp**3)
        answer = agree(q04.solve(charge=charge, radius=radius, distance=distance), exact)
        return draw(
            4,
            tex(answer),
            f"วงแหวนรัศมี {radius} m อยู่ในระนาบ XOY ศูนย์กลางที่ O มีประจุ +{charge} nC กระจายสม่ำเสมอ องค์ประกอบ E_z ของสนามไฟฟ้าที่จุด (0, 0, −{distance} m) เป็นกี่ V/m (บวกถ้าชี้ไปทาง +Z) ให้ k=9×10⁹ N m²/C²",
            r"E=\frac{kQL}{(R^2+L^2)^{3/2}}",
            [tex(-exact), tex(-Fraction(9 * charge, hyp * hyp)), tex(-Fraction(9 * charge, distance * distance))],
        )


@_type(5, "กระแสจากวงแหวนมีประจุที่หมุน", "กระแสไฟฟ้าจากประจุที่เคลื่อนที่")
class SpinningRingCurrent(PhysicsSheet):
    def expr(self, rng):
        charge = rng.randint(1, 12)
        omega = rng.randint(2, 30)
        agree(q05.solve(charge=charge, omega=omega), charge * omega / (2 * pi))
        return draw(
            5,
            over_pi(Fraction(charge * omega, 2)),
            f"วงแหวนมีประจุ {charge} μC กระจายสม่ำเสมอ หมุนรอบแกนที่ผ่านศูนย์กลางและตั้งฉากกับระนาบวงด้วยอัตราเร็วเชิงมุม {omega} rad/s กระแสไฟฟ้าตามแนววงแหวนมีขนาดกี่ μA",
            r"I=\frac{Q}{T},\quad T=\frac{2\pi}{\omega}",
            [tex(Fraction(charge * omega, 2)), over_pi(charge * omega), str(charge * omega)],
        )


@_type(6, "สนามแม่เหล็กจากวงแหวนมีประจุที่หมุน", "สนามแม่เหล็กจากกระแสวงกลม")
class SpinningRingField(PhysicsSheet):
    def expr(self, rng):
        charge = rng.randint(1, 20)
        omega = 10 * rng.randint(1, 10)
        radius = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(2), Fraction(5)))
        exact = Fraction(charge * omega, 10**13) / radius
        answer = agree(q06.solve(charge=charge, omega=omega, radius=float(radius)), exact)
        return draw(
            6,
            sci(answer, force=True),
            f"วงแหวนรัศมี {number(radius)} m มีประจุ {charge} μC กระจายสม่ำเสมอ หมุนรอบแกนของมันด้วยอัตราเร็วเชิงมุม {omega} rad/s สนามแม่เหล็กที่ศูนย์กลางวงแหวนมีขนาดกี่เทสลา ให้ μ₀=4π×10⁻⁷ T m/A",
            r"I=\frac{Q\omega}{2\pi},\quad B=\frac{\mu_0I}{2R}",
            [pi_sci(2 * exact), sci(exact / radius, force=True), sci(2 * exact, force=True)],
        )


@_type(7, "ความต้านทานขนานสูงสุดจากการตัดลวด", "ตัวต้านทานขนานและค่าสูงสุด")
class SplitWire(PhysicsSheet):
    def expr(self, rng):
        resistance = 4 * rng.randint(1, 30)
        answer = agree(q07.solve(resistance=resistance), Fraction(resistance, 4))
        return draw(
            7,
            tex(answer),
            f"ตัดลวดความต้านทาน {resistance} Ω ออกเป็นสองท่อนยาวเท่าใดก็ได้ แล้วนำสองท่อนมาต่อขนานกัน ความต้านทานรวมมีค่ามากที่สุดได้กี่ Ω",
            r"R_\parallel=\frac{R_1(R-R_1)}R",
            [tex(Fraction(resistance, 2)), str(resistance), tex(Fraction(3 * resistance, 16))],
        )


def _self_equal_pool():
    pool = []
    for first in range(1, 11):
        for second in range(1, 21):
            root = isqrt(first * first + 4 * first * second)
            if root * root == first * first + 4 * first * second and (first + root) % 2 == 0:
                pool.append((first, second, (first + root) // 2))
    return tuple(pool)


SELF_EQUAL = _self_equal_pool()


@_type(8, "ตัวต้านทานที่ทำให้ความต้านทานรวมเท่าตัวเอง", "วงจรตัวต้านทานและสมการกำลังสอง")
class SelfEqualResistance(PhysicsSheet):
    def expr(self, rng):
        first, second, value = rng.choice(SELF_EQUAL)
        answer = agree(q08.solve(first=first, second=second), value)
        other = value - first  # magnitude of the negative root
        return draw(
            8,
            str(answer),
            f"ตัวต้านทาน R₁ = {first} Ω ต่ออนุกรมกับกลุ่มขนานของ R₂ = {second} Ω กับตัวต้านทาน R ความต้านทานรวมระหว่างปลาย A กับ B เท่ากับ R พอดี R มีค่ากี่ Ω",
            r"R_1+\frac{R_2R}{R_2+R}=R",
            [str(first + second), tex(Fraction(first * second, first + second)), str(other)],
        )


@_type(9, "ความต้านทานความร้อนของแท่งตัวนำ", "การนำความร้อนคงตัวหนึ่งมิติ")
class ThermalResistance(PhysicsSheet):
    def expr(self, rng):
        length = Fraction(rng.randint(1, 20), 10)
        area = rng.choice((1, 2, 4, 5, 10))
        conductivity = rng.choice((50, 80, 100, 200, 400))
        a = Fraction(area, 10**4)
        exact = length / (conductivity * a)
        answer = agree(q09.solve(length=float(length), area=area, conductivity=conductivity), exact)
        return draw(
            9,
            tex(answer),
            f"แท่งตัวนำความร้อนยาว {number(length)} m พื้นที่หน้าตัด {area} cm² สภาพนำความร้อน {conductivity} W/(m K) ถ้าเขียนอัตราการไหลของความร้อน Q = (T₁ − T₂)/ℛ ค่า ℛ เป็นกี่ K/W",
            r"Q=\frac{KA(T_1-T_2)}L",
            [tex(conductivity * a / length), tex(conductivity * length / a), tex(length / (conductivity * area))],
        )


@_type(10, "อุณหภูมิรอยต่อของแท่งสองท่อน", "การนำความร้อนคงตัวหนึ่งมิติ")
class ThermalJunction(PhysicsSheet):
    def expr(self, rng):
        while True:
            l1, l2 = rng.randint(1, 4), rng.randint(1, 4)
            a1, a2 = rng.randint(1, 4), rng.randint(1, 4)
            if l1 * a2 != l2 * a1:
                break
        hot = 10 * rng.randint(5, 15)
        cold = 10 * rng.randint(0, 4)
        r1, r2 = Fraction(l1, a1), Fraction(l2, a2)
        exact = hot - (hot - cold) * r1 / (r1 + r2)
        answer = agree(q10.solve(hot=hot, cold=cold, l1=l1, a1=a1, l2=l2, a2=a2), exact)
        return draw(
            10,
            tex(answer),
            f"แท่งตัวนำความร้อนสองท่อนทำจากวัสดุเดียวกันต่อกัน ท่อนแรกยาว {l1}L หน้าตัด {a1}A ท่อนที่สองยาว {l2}L หน้าตัด {a2}A ผิวข้างหุ้มฉนวน ปลายท่อนแรกคงที่ {hot} °C ปลายท่อนที่สองคงที่ {cold} °C ในสภาวะคงตัว รอยต่อมีอุณหภูมิกี่ °C",
            r"\mathcal R=\frac{L}{KA},\quad\frac{T_1-T_j}{\mathcal R_1}=\frac{T_j-T_2}{\mathcal R_2}",
            [
                tex(Fraction(hot + cold, 2)),
                tex(hot - (hot - cold) * Fraction(l1, l1 + l2)),
                tex(hot - (hot - cold) * r2 / (r1 + r2)),
            ],
        )


@_type(11, "ความดันก้นถังที่ถูกเร่งขึ้น", "ความดันในของไหลที่มีความเร่ง")
class AcceleratingTank(PhysicsSheet):
    def expr(self, rng):
        accel = rng.randint(1, 8)
        depth = Fraction(rng.randint(1, 20), 10)
        exact = 10**5 + 1000 * (10 + accel) * depth
        answer = agree(q11.solve(depth=float(depth), accel=accel), exact)
        return draw(
            11,
            tex(answer),
            f"ถังเปิดบรรจุน้ำลึก {number(depth)} m (ความหนาแน่น 1000 kg/m³) ถูกดึงขึ้นในแนวดิ่งด้วยความเร่ง {accel} m/s² ความดันบรรยากาศ 1×10⁵ Pa ความดันที่ก้นถังเป็นกี่ Pa ให้ g=10 m/s²",
            r"(P-P_a)A-mg=ma",
            [tex(10**5 + 10000 * depth), tex(10**5 + 1000 * (10 - accel) * depth), tex(1000 * (10 + accel) * depth)],
        )


@_type(12, "ระยะตกของน้ำที่พุ่งจากรูข้างถัง", "แบร์นูลลีและการเคลื่อนที่แบบโพรเจกไทล์")
class TorricelliRange(PhysicsSheet):
    def expr(self, rng):
        depth = Fraction(rng.randint(5, 30), 10)
        hole = Fraction(rng.randint(1, int(depth * 10) - 1), 10)
        squared = 4 * hole * (depth - hole)
        agree(q12.solve(depth=float(depth), hole=float(hole)) ** 2, squared)
        return draw(
            12,
            radical(squared),
            f"ถังเปิดตั้งบนพื้น น้ำในถังลึก {number(depth)} m จากพื้น มีรูเล็กที่ผนังสูงจากพื้น {number(hole)} m น้ำพุ่งออกในแนวระดับ ไม่คิดความหนืด น้ำตกถึงพื้นห่างจากผนังกี่ m",
            r"v=\sqrt{2g(h-y)},\quad t=\sqrt{2y/g}",
            [radical(4 * hole * depth), radical(squared / 4), radical(squared / 2)],
        )


@_type(13, "ความเข้มแสงหลังระบบเลนส์ลดขนาดลำแสง", "ระบบเลนส์เว้าร่วมเลนส์นูนแบบไร้โฟกัส")
class BeamReducer(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.choice((Fraction(2), Fraction(3), Fraction(4), Fraction(3, 2), Fraction(5, 2)))
        diverging = ratio.denominator * rng.randint(2, 6)
        converging = ratio * diverging
        answer = agree(q13.solve(ratio=float(ratio)), ratio**2)
        return draw(
            13,
            tex(answer),
            f"ลำแสงขนานความเข้ม I₁ ผ่านเลนส์นูนโฟกัส {converging} cm แล้วผ่านเลนส์เว้าโฟกัส −{diverging} cm ที่วางห่างพอดีจนลำแสงออกมาขนานกันอีกครั้งด้วยความเข้ม I₂ ไม่มีการสูญเสียพลังงาน I₂/I₁ เป็นกี่เท่า",
            r"\frac{w_2}{w_1}=\frac{|f_2|}{f_1},\quad I\propto\frac1{w^2}",
            [tex(ratio), tex(1 / ratio**2), tex(1 / ratio)],
        )


ENDS = (Fraction(5, 4), Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(3), Fraction(4), Fraction(5))


@_type(14, "ความยาวภาพของวัตถุที่วางตามแกน", "สมการเลนส์และกำลังขยายตามแนวแกน")
class LongitudinalImage(PhysicsSheet):
    def expr(self, rng):
        near, far = sorted(rng.sample(ENDS, 2))
        exact = 1 / ((far - 1) * (near - 1))
        answer = agree(q14.solve(far=float(far), near=float(near)), exact)
        return draw(
            14,
            tex(answer),
            f"วัตถุ AB วางตามแนวแกนมุขสำคัญของเลนส์นูนความยาวโฟกัส f โดยปลาย A ห่างเลนส์ {number(far)}f และปลาย B ห่างเลนส์ {number(near)}f ภาพจริง A′B′ ยาวเป็นกี่เท่าของ AB",
            r"v=\frac{uf}{u-f}",
            [tex(1 / (far - 1)), tex(1 / (near - 1)), tex(exact**2)],
        )


@_type(15, "การเปลี่ยนปริมาตรของเส้นยางที่ถูกยืด", "การยืดและปริมาตร")
class StretchedCord(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.choice((Fraction(1, 2), Fraction(1, 4), Fraction(1, 3), Fraction(1, 5), Fraction(0)))
        radius = rng.randint(1, 5)
        change = Fraction(rng.randint(1, 10), 10)
        exact = radius * radius * (1 - 2 * ratio) * change
        answer = agree(q15.solve(radius=radius, change=float(change), ratio=float(ratio)), exact)
        return draw(
            15,
            times_pi(answer),
            f"เส้นยางยาว 100 mm รัศมี {radius} mm ถูกดึงให้ยาวขึ้น {number(change)} mm ทำให้รัศมีลดลงโดย δr/r = {number(ratio)}·(δl/l) ถ้าทิ้งพจน์อันดับสอง ปริมาตรเพิ่มขึ้นกี่ mm³ (ตอบเป็นพหุคูณของ π)",
            r"\frac{\delta V}{V}=\frac{\delta l}l-2\frac{\delta r}r",
            [
                times_pi(radius * radius * change),
                times_pi(radius * radius * (1 + 2 * ratio) * change),
                times_pi(radius * radius * (1 - ratio) * change),
            ],
        )


@_type(16, "แรงเคลื่อนจากสมดุลพลังงานขณะอัดประจุ", "พลังงานในวงจร RC")
class ChargingEmf(PhysicsSheet):
    def expr(self, rng):
        resistance = rng.randint(1, 20)
        cap = rng.randint(1, 10)
        charge = cap * rng.randint(1, 10)
        current = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2), Fraction(1, 4)))
        heat, store = current * resistance, Fraction(charge, cap)
        answer = agree(q16.solve(resistance=resistance, capacitance=cap, charge=charge, current=float(current)), heat + store)
        return draw(
            16,
            tex(answer),
            f"แหล่งกำเนิดอัดประจุตัวเก็บประจุ {cap} μF ผ่านตัวต้านทาน {resistance} Ω ขณะหนึ่งตัวเก็บประจุมีประจุ {charge} μC และกระแส {number(current)} A จากสมดุลกำลัง εi = i²R + (q/C)i แรงเคลื่อนไฟฟ้า ε เป็นกี่ V",
            r"\varepsilon i=i^2R+\frac qCi",
            [tex(heat), tex(store), tex(heat - store)],
        )


@_type(17, "ประจุในตัวเก็บประจุอนุกรมอนันต์", "ตัวเก็บประจุต่ออนุกรมและอนุกรมอนันต์")
class SeriesSquares(PhysicsSheet):
    def expr(self, rng):
        first = rng.randint(1, 10)
        emf = rng.choice((3, 5, 6, 10, 12, 20))
        agree(q17.solve(first=first, emf=emf), 6 * first * emf / pi**2)
        top = 6 * first * emf
        return draw(
            17,
            rf"\frac{{{top}}}{{\pi^2}}",
            f"ตัวเก็บประจุ C₁, C₂, ..., C_n ต่ออนุกรมกันกับแหล่งกำเนิด {emf} V โดย C_i = i²C₁ และ C₁ = {first} μF เมื่อ n มีค่ามาก (ใช้ 1 + 1/2² + 1/3² + ... ≈ π²/6) หลังสับสวิตช์ ประจุในตัวเก็บประจุ C_i แต่ละตัวมีขนาดกี่ μC",
            r"\frac1{C_{eq}}=\sum\frac1{i^2C_1}=\frac{\pi^2}{6C_1}",
            [times_pi(Fraction(first * emf, 6), "^2"), str(first * emf), over_pi(top)],
        )


@_type(18, "ความเร็วเรือที่แล่นหนีหน้าผาจากเสียงสะท้อน", "เสียงสะท้อนจากผู้สังเกตที่เคลื่อนที่")
class EchoAway(PhysicsSheet):
    def expr(self, rng):
        start = rng.randint(2, 20)
        delay = rng.randint(1, 6)
        sound = 340
        exact = Fraction(sound * delay, 2 * start + delay)
        answer = agree(q18.solve(start=start, delay=delay, sound=sound), exact)
        return draw(
            18,
            tex(answer),
            f"เรือออกจากหน้าผาเมื่อ t = 0 แล่นหนีด้วยความเร็วคงที่ ที่เวลา t = {start} s เรือเปิดหวูดสั้นๆ และได้ยินเสียงสะท้อนจากหน้าผาหลังเปิดหวูด {delay} s อัตราเร็วเสียง {sound} m/s เรือแล่นเร็วกี่ m/s",
            r"c\tau=vt_1+v(t_1+\tau)",
            [
                tex(Fraction(sound * delay, 2 * start)),
                tex(Fraction(sound * delay, 2 * start - delay)) if 2 * start != delay else "0",
                tex(Fraction(sound * delay, start + delay)),
            ],
        )


@_type(19, "แรงดึงดูดระหว่างแผ่นตัวเก็บประจุจากความต่างศักย์", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateForceVoltage(PhysicsSheet):
    def expr(self, rng):
        area = rng.choice((10, 20, 50, 100, 200))
        voltage = 100 * rng.randint(1, 10)
        gap = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2)))
        a, d = Fraction(area, 10**4), gap / 1000
        exact = a * voltage**2 / (2 * d * d)
        answer = agree(q19.solve(area=area, voltage=voltage, gap=float(gap)), exact)
        return draw(
            19,
            sci(answer, force=True),
            f"ตัวเก็บประจุแผ่นขนาน แผ่นละ {area} cm² ห่างกัน {number(gap)} mm ต่อกับแหล่งกำเนิด {voltage} V ประจุกระจายสม่ำเสมอบนผิวด้านใน แรงที่แผ่นหนึ่งดึงดูดอีกแผ่นเป็นกี่เท่าของ ε₀ (หน่วย SI)",
            r"F=\frac{Q^2}{2\varepsilon_0A},\quad Q=\frac{\varepsilon_0AV}{d}",
            [sci(2 * exact, force=True), sci(exact * d, force=True), sci(exact / voltage, force=True)],
        )


@_type(20, "ความเร่งโน้มถ่วงที่เส้นศูนย์สูตรของดาวที่หมุน", "การเคลื่อนที่แบบวงกลมกับน้ำหนักปรากฏ")
class EquatorGravityExact(PhysicsSheet):
    def expr(self, rng):
        period = 1000 * rng.choice((2, 4, 5, 10))
        k = Fraction(rng.randint(1, 20), 1000)  # 4R/T^2
        radius = k * period * period / 4
        polar = rng.choice((4, 6, 8, 10, 12))
        agree(q20.solve(polar=polar, period=period, radius=float(radius)), polar - float(k) * pi**2)
        fmt = lambda c, power="^2": rf"{polar}-{tex(c)}\pi{power}"
        return draw(
            20,
            fmt(k),
            f"ดาวเคราะห์ทรงกลมสม่ำเสมอรัศมี {number(radius / 1000)} km หมุนรอบตัวเองเทียบกับดาวไกลโพ้นด้วยคาบ {period} s ความเร่งโน้มถ่วงที่ขั้วดาวเป็น {polar} m/s² ความเร่งโน้มถ่วงปรากฏที่เส้นศูนย์สูตรเป็นกี่ m/s²",
            r"g=g_0-\omega^2R,\quad\omega=\frac{2\pi}T",
            [rf"{polar}+{tex(k)}\pi^2", fmt(k / 2, ""), str(polar)],
        )


PLANETS = (
    (Fraction(983, 100), 23, 56, 6370),
    (Fraction(373, 100), 24, 37, 3390),
    (Fraction(983, 100), 5, 0, 6370),
    (Fraction(12), 4, 0, 8000),
    (Fraction(373, 100), 3, 0, 3390),
    (Fraction(887, 100), 10, 0, 6050),
)


@_type(21, "ค่าตัวเลขความเร่งโน้มถ่วงที่เส้นศูนย์สูตร", "การเคลื่อนที่แบบวงกลมกับน้ำหนักปรากฏ")
class EquatorGravityNumber(PhysicsSheet):
    def expr(self, rng):
        polar, hours, minutes, radius_km = rng.choice(PLANETS)
        value = q21.solve(polar=float(polar), hours=hours, minutes=minutes, radius_km=radius_km)
        term = float(polar) - value
        spin = f"{hours} ชั่วโมง {minutes} นาที" if minutes else f"{hours} ชั่วโมง"
        return draw(
            21,
            three_figures(value),
            f"ดาวเคราะห์ทรงกลมรัศมี {radius_km} km หมุนรอบตัวเองเทียบกับดาวไกลโพ้นด้วยคาบ {spin} ความเร่งโน้มถ่วงที่ขั้ว {number(polar)} m/s² ความเร่งโน้มถ่วงปรากฏที่เส้นศูนย์สูตรเป็นกี่ m/s² (เลขนัยสำคัญ 3 ตัว)",
            r"g=g_0-\left(\frac{2\pi}T\right)^2R",
            [three_figures(float(polar)), three_figures(float(polar) + term), three_figures(float(polar) - term / 2)],
        )


@_type(22, "คาบการโคจรของระบบสองวัตถุ", "กฎความโน้มถ่วงสากลและวงโคจร")
class BinaryPeriodScaling(PhysicsSheet):
    def expr(self, rng):
        scale = rng.choice((Fraction(1, 2), Fraction(2), Fraction(3), Fraction(4)))
        mass = rng.choice((Fraction(1, 2), Fraction(2), Fraction(3), Fraction(4), Fraction(9)))
        squared = scale**3 / mass
        agree(q22.solve(scale=float(scale), mass_factor=float(mass)) ** 2, squared)
        return draw(
            22,
            radical(squared),
            f"ดาวสองดวงโคจรรอบกันเป็นวงกลมที่ระยะห่างคงที่ ถ้าระยะห่างเปลี่ยนเป็น {number(scale)} เท่าของเดิม และมวลรวมของระบบเปลี่ยนเป็น {number(mass)} เท่าของเดิม คาบการโคจรใหม่เป็นกี่เท่าของเดิม",
            r"T=2\pi\sqrt{\frac{D^3}{G(M+m)}}",
            [radical(scale**3 * mass), radical(scale**3), radical(scale**2 / mass)],
        )


@_type(23, "คาบการโคจรของดาวสามดวงสามเหลี่ยมด้านเท่า", "กฎความโน้มถ่วงสากลและวงโคจร")
class TriangleThreeBody(PhysicsSheet):
    def expr(self, rng):
        side = rng.randint(1, 6)
        half = rng.randint(1, 4)  # T = 2 * half * pi
        gm = Fraction(side**3, 3 * half * half)
        answer = agree(q23.solve(side=side, gm=float(gm)), 2 * half)
        return draw(
            23,
            times_pi(answer),
            f"ดาวสามดวงมวลเท่ากัน M อยู่ที่มุมของสามเหลี่ยมด้านเท่ายาวด้าน {side} หน่วย และโคจรรอบศูนย์กลางมวลด้วยรูปร่างคงที่ ถ้า GM = {number(gm)} (หน่วยเดียวกัน) คาบการโคจรเป็นเท่าใด",
            r"\sqrt3\frac{GM^2}{D^2}=M\omega^2\frac{D}{\sqrt3}",
            [pi_radical(4 * side**3 / gm), pi_radical(2 * side**3 / gm), times_pi(half)],
        )


@_type(24, "ความเร็วน้ำไหลออกจากท่อหนืด", "ความหนืดและกฎของปัวเซย")
class PoiseuilleDrain(PhysicsSheet):
    def expr(self, rng):
        depth = Fraction(rng.randint(1, 10), 10)
        radius = Fraction(rng.randint(1, 5), 10)  # mm
        viscosity = rng.choice((1, 2))  # mPa s
        length = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2)))
        r = radius / 1000
        exact = 1000 * 10 * depth * r * r / (8 * Fraction(viscosity, 1000) * length)
        answer = agree(
            q24.solve(depth=float(depth), radius=float(radius), viscosity=viscosity, length=float(length)), exact
        )
        return draw(
            24,
            tex(answer),
            f"น้ำ (1000 kg/m³ ความหนืด {viscosity}×10⁻³ Pa s) ในถังใหญ่ลึก {number(depth)} m ไหลออกทางท่อแนวระดับยาว {number(length)} m รัศมี {number(radius)} mm ที่ก้นถังแบบไม่ปั่นป่วน ปลายท่อเปิดสู่บรรยากาศ ใช้ Q = ΔPπr⁴/(8ηl) และละพลังงานจลน์ที่ปลายท่อ น้ำพุ่งออกด้วยอัตราเร็วเฉลี่ยกี่ m/s ให้ g=10 m/s²",
            r"v=\frac{Q}{\pi r^2},\quad\Delta P=\rho gh",
            [radical(20 * depth), tex(2 * exact), tex(exact / r)],
        )


@_type(25, "สนามแม่เหล็กจากลวดรูปตัวยูกึ่งอนันต์", "กฎบีโอต์ซาวาร์ตสำหรับลวดโค้ง")
class HairpinField(PhysicsSheet):
    def expr(self, rng):
        current = rng.randint(1, 20)
        radius = rng.choice((1, 2, 4, 5, 10))  # cm
        c = Fraction(10 * current, radius)  # B in uT = c (pi + 2)
        value = q25.solve(radius=radius) * 4e-7 * pi * current * 1e6
        agree(value, float(c) * (pi + 2))
        fmt = lambda extra: rf"{tex(c)}\left(\pi+{extra}\right)" if extra else rf"{tex(c)}\pi"
        return draw(
            25,
            fmt(2),
            f"ลวดตรงยาวมากสองเส้นขนานกันห่างกัน {2 * radius} cm ปลายด้านหนึ่งของทั้งสองเส้นต่อกันด้วยลวดครึ่งวงกลมรัศมี {radius} cm ศูนย์กลาง O (ปลายลวดตรงอยู่บนแนวผ่าน O ที่ตั้งฉากกับลวด) มีกระแส {current} A ไหลต่อเนื่องตลอดเส้น สนามแม่เหล็กที่ O มีขนาดกี่ μT ให้ μ₀=4π×10⁻⁷ T m/A",
            r"B=\frac{\mu_0I}{4R}+2\cdot\frac{\mu_0I}{4\pi R}",
            [fmt(1), fmt(0), fmt(4)],
        )
