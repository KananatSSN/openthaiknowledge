"""Seeded variants of the reviewed TPhO 4 (2548) national physics olympiad."""

from fractions import Fraction
from math import ceil, floor, isqrt, log, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2548_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2548_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19

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


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


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


def figures(value):
    """A nonzero float to three significant figures, as plain text."""
    digits = 2 - floor(log10(abs(value)))
    return f"{round(value, digits):.{digits}f}" if digits > 0 else str(int(round(value, digits)))


def measure(value):
    """A nonzero float to three significant figures: plain in ordinary
    ranges, otherwise as mantissa × 10^n."""
    if 1e-3 <= abs(value) < 1e5:
        return figures(value)
    power = floor(log10(abs(value)))
    mantissa = round(value / 10**power, 2)
    if abs(mantissa) >= 10:
        mantissa, power = mantissa / 10, power + 1
    return rf"{mantissa:.2f}\times10^{{{power}}}"


SLIPS = {
    1: ("phys.elastic_masses_swapped", "phys.elastic_as_inelastic", "phys.elastic_velocities_exchanged"),
    2: ("phys.elastic_masses_swapped", "phys.elastic_as_inelastic", "phys.elastic_velocities_exchanged"),
    3: ("phys.energy_fraction_kept_given", "phys.energy_fraction_speed_ratio", "phys.energy_fraction_mass_share"),
    4: ("phys.middle_mass_arithmetic_mean", "phys.middle_mass_equal_first", "phys.middle_mass_harmonic_mean"),
    5: ("phys.middle_mass_ignored", "phys.middle_mass_one_collision", "phys.middle_mass_full_transfer"),
    6: ("phys.collision_count_linearised", "phys.collision_count_speed_halved", "phys.collision_count_round_trips"),
    7: ("phys.assembly_diagonals_dropped", "phys.assembly_pairs_halved", "phys.assembly_pairs_double_counted"),
    8: ("phys.square_centre_side_distance", "phys.square_centre_full_diagonal", "phys.square_centre_one_charge"),
    9: ("phys.positron_far_pair_dropped", "phys.positron_pairs_single", "phys.positron_mean_distance"),
    10: ("phys.positron_barrier_at_centre", "phys.positron_kinetic_half_dropped", "phys.positron_start_inside_field"),
    11: ("phys.positron_spring_sqrt2_dropped", "phys.positron_spring_doubled", "phys.positron_omega_not_rooted"),
    12: ("phys.radial_flow_half_dropped", "phys.radial_flow_disc_area", "phys.radial_flow_radius_not_squared"),
    13: ("phys.bernoulli_gauge_sign", "phys.bernoulli_rim_speed_ignored", "phys.bernoulli_half_dropped"),
    14: ("phys.disc_lift_log_only", "phys.disc_lift_ring_doubled", "phys.disc_lift_uniform_deficit"),
    15: ("phys.jet_force_kinetic", "phys.jet_force_mass_rate", "phys.jet_force_rebound"),
    16: ("phys.lift_jet_force_ignored", "phys.lift_jet_force_sign", "phys.lift_force_as_mass"),
    17: ("phys.rc_angular_frequency_as_f", "phys.capacitor_area_not_divided", "phys.capacitor_area_unit"),
    18: ("phys.dielectric_thickness_unit", "phys.dielectric_thickness_divided", "phys.dielectric_ratio_inverted"),
    19: ("phys.laser_ruler_sine_used", "phys.laser_ruler_tangent_used", "phys.laser_ruler_height_ratio_as_sine"),
}


class _Clash(Exception):
    """Two choices came out equal: the draw is made again."""


def draw(number_, answer, prompt, hint, slips):
    if len({answer, *slips}) != 4:
        raise _Clash
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number_], slips)],
    )


SHEET = "ฟิสิกส์โอลิมปิก สอวน. ครั้งที่ 4 (2548)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2548_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2548_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


def _collision(rng):
    mass_a, mass_b = rng.sample(range(1, 11), 2)
    speed_a = rng.randint(1, 10)
    speed_b = rng.randint(-5, speed_a - 1)
    return mass_a, mass_b, speed_a, speed_b


COLLIDE = "มวล {a} kg เคลื่อนที่ด้วยความเร็ว {ua} m/s ไปทางขวา เข้าชนมวล {b} kg ที่มีความเร็ว {ub} m/s (ทางขวาเป็นบวก) บนพื้นลื่น การชนเป็นแบบยืดหยุ่นในแนวเส้นตรง"


@_type(1, "ความเร็วของมวลที่ถูกชนหลังการชนยืดหยุ่น", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class StruckSpeed(PhysicsSheet):
    def _variant(self, rng):
        a, b, ua, ub = _collision(rng)
        exact = Fraction(2 * a * ua + (b - a) * ub, a + b)
        agree(q01.solve(mass_a=a, mass_b=b, speed_a=ua, speed_b=ub), exact)
        return draw(
            1,
            tex(exact),
            COLLIDE.format(a=a, ua=ua, b=b, ub=ub) + f" หลังการชนมวล {b} kg มีความเร็วกี่ m/s",
            r"M_Au_A+M_Bu_B=M_Av_A+M_Bv_B,\quad u_A-u_B=v_B-v_A",
            [tex(Fraction(2 * b * ua + (a - b) * ub, a + b)), tex(Fraction(a * ua + b * ub, a + b)), str(ua)],
        )


@_type(2, "ความเร็วของมวลที่เข้าชนหลังการชนยืดหยุ่น", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class StrikerSpeed(PhysicsSheet):
    def _variant(self, rng):
        a, b, ua, ub = _collision(rng)
        exact = Fraction(2 * b * ub + (a - b) * ua, a + b)
        agree(q02.solve(mass_a=a, mass_b=b, speed_a=ua, speed_b=ub), exact)
        return draw(
            2,
            tex(exact),
            COLLIDE.format(a=a, ua=ua, b=b, ub=ub) + f" หลังการชนมวล {a} kg มีความเร็วกี่ m/s",
            r"M_Au_A+M_Bu_B=M_Av_A+M_Bv_B,\quad u_A-u_B=v_B-v_A",
            [tex(Fraction(2 * a * ub + (b - a) * ua, a + b)), tex(Fraction(a * ua + b * ub, a + b)), str(ub)],
        )


@_type(3, "สัดส่วนพลังงานที่ส่งให้มวลที่หยุดนิ่ง", "สัดส่วนพลังงานในการชนยืดหยุ่นหนึ่งมิติ")
class EnergyShare(PhysicsSheet):
    def _variant(self, rng):
        a, b = rng.sample(range(1, 13), 2)
        exact = Fraction(4 * a * b, (a + b) ** 2)
        agree(q03.solve(mass_a=a, mass_b=b), exact)
        return draw(
            3,
            tex(exact),
            f"มวล {a} kg เคลื่อนที่เข้าชนมวล {b} kg ที่หยุดนิ่งแบบยืดหยุ่นในแนวเส้นตรงบนพื้นลื่น มวล {b} kg ได้รับพลังงานจลน์เป็นสัดส่วนเท่าใดของพลังงานจลน์เริ่มต้นของมวล {a} kg",
            r"v_B=\frac{2M_Au_A}{M_A+M_B}",
            [tex(Fraction((b - a) ** 2, (a + b) ** 2)), tex(Fraction(2 * a, a + b)), tex(Fraction(b, a + b))],
        )


@_type(4, "มวลตัวกลางที่ส่งพลังงานได้มากที่สุด", "สัดส่วนพลังงานในการชนยืดหยุ่นหนึ่งมิติ")
class BestMiddleMass(PhysicsSheet):
    def _variant(self, rng):
        a, b = rng.sample(range(1, 21), 2)
        agree(q04.solve(mass_a=a, mass_b=b) ** 2, a * b)
        return draw(
            4,
            radical(a * b),
            f"มวล {a} kg เคลื่อนที่เข้าชนมวล m ที่หยุดนิ่ง แล้ว m เคลื่อนที่ไปชนมวล {b} kg ที่หยุดนิ่งในแนวเส้นตรงเดียวกัน การชนทั้งหมดเป็นแบบยืดหยุ่นบนพื้นลื่น m ต้องเป็นกี่ kg มวล {b} kg จึงได้รับพลังงานมากที่สุด",
            r"R=\frac{4M_Am}{(M_A+m)^2}\cdot\frac{4mM_B}{(m+M_B)^2},\quad\frac{dR}{dm}=0",
            [tex(Fraction(a + b, 2)), str(a), tex(Fraction(2 * a * b, a + b))],
        )


@_type(5, "สัดส่วนพลังงานสูงสุดผ่านมวลตัวกลาง", "สัดส่วนพลังงานในการชนยืดหยุ่นหนึ่งมิติ")
class BestMiddleShare(PhysicsSheet):
    def _variant(self, rng):
        p, q = rng.sample(range(1, 8), 2)
        a, b = p * p, q * q
        exact = Fraction(16 * a * b, (p + q) ** 4)
        agree(q05.solve(mass_a=a, mass_b=b), exact)
        return draw(
            5,
            tex(exact),
            f"มวล {a} kg เคลื่อนที่เข้าชนมวล m ที่หยุดนิ่ง แล้ว m ไปชนมวล {b} kg ที่หยุดนิ่ง (ชนแบบยืดหยุ่นในแนวเส้นตรงบนพื้นลื่น) โดยเลือก m ให้มวล {b} kg ได้พลังงานมากที่สุด มวล {b} kg ได้รับพลังงานเป็นสัดส่วนเท่าใดของพลังงานเริ่มต้นของมวล {a} kg",
            r"m=\sqrt{M_AM_B},\quad R=\frac{4M_Am}{(M_A+m)^2}\cdot\frac{4mM_B}{(m+M_B)^2}",
            [tex(Fraction(4 * a * b, (a + b) ** 2)), tex(Fraction(4 * p * q, (p + q) ** 2)), "1"],
        )


@_type(6, "จำนวนครั้งการชนจนพลังงานเหลือครึ่งหนึ่ง", "สัดส่วนพลังงานในการชนยืดหยุ่นหนึ่งมิติ")
class HalvingCollisions(PhysicsSheet):
    def _variant(self, rng):
        ratio = rng.choice((20, 40, 50, 80, 100, 200, 400, 500, 800, 1000))
        count = q06.solve(ratio=ratio)
        exact = log(0.5) / (2 * log((ratio - 1) / (ratio + 1)))
        assert count == ceil(exact - 1e-12)
        return draw(
            6,
            str(count),
            f"มวล M สองก้อนวางนิ่งบนพื้นลื่นห่างกันพอสมควร มีมวล m = M/{ratio} อยู่ระหว่างกัน ทำให้ m เคลื่อนที่ชนมวล M แบบยืดหยุ่นกลับไปกลับมา (ถือว่ามวล M แทบไม่ขยับ) ต้องชนอย่างน้อยกี่ครั้ง พลังงานจลน์ของ m จึงเหลือไม่เกินครึ่งหนึ่งของพลังงานเริ่มต้น",
            r"\frac{K_n}{K_0}=\left(\frac{M-m}{M+m}\right)^{2n}",
            [str(round(ratio / 8)), str(ceil(2 * exact - 1e-12)), str(ceil(exact / 2 - 1e-12))],
        )


RECTANGLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25))
SIZES = (Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(2))


@_type(7, "งานในการนำประจุสี่ตัวมาวางที่มุมสี่เหลี่ยม", "พลังงานศักย์ไฟฟ้าของระบบประจุ")
class FourChargeAssembly(PhysicsSheet):
    def _variant(self, rng):
        size = rng.choice(SIZES)
        w, h, c = (x * size for x in rng.choice(RECTANGLES))
        exact = 2 / w + 2 / h + 2 / c
        agree(q07.solve(width=float(w), height=float(h)), exact)
        return draw(
            7,
            tex(exact),
            f"ประจุบวก q เท่ากันสี่ตัวถูกนำจากระยะอนันต์มาวางที่มุมทั้งสี่ของสี่เหลี่ยมผืนผ้ากว้าง {number(w)} m ยาว {number(h)} m งานที่ต้องทำทั้งหมดเป็นกี่เท่าของ kq² (k = 1/(4πε₀), ระยะเป็นเมตร)",
            r"W=\sum_{\text{pairs}}\frac{kq^2}{r_{ij}}",
            [tex(2 / w + 2 / h), tex(1 / w + 1 / h + 1 / c), tex(2 * exact)],
        )


@_type(8, "ศักย์ไฟฟ้าที่จุดกลางสี่เหลี่ยมโปรตอน", "พลังงานศักย์ไฟฟ้าของระบบประจุ")
class SquareCentrePotential(PhysicsSheet):
    def _variant(self, rng):
        side = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)))
        unit = Fraction(144, 100) / side  # ke/a in volts with a in nm
        agree(q08.solve(side=float(side)), float(4 * unit) * 2**0.5)
        root = lambda k: rf"{tex(k)}\sqrt{{2}}"  # noqa: E731
        return draw(
            8,
            root(4 * unit),
            f"โปรตอนสี่ตัวถูกยึดไว้ที่มุมของสี่เหลี่ยมจัตุรัสด้านยาว {number(side)} nm ศักย์ไฟฟ้าต่ำสุดภายในสี่เหลี่ยม (ที่จุดกลาง) เป็นกี่โวลต์ (ke = 1.44×10⁻⁹ V·m, ศักย์ที่อนันต์เป็นศูนย์)",
            r"V=4\cdot\frac{ke}{a/\sqrt2}",
            [tex(4 * unit), root(2 * unit), root(unit)],
        )


POSITIONS = (Fraction(-2), Fraction(-3, 2), Fraction(-1), Fraction(-1, 2), Fraction(-1, 4), Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1))


@_type(9, "พลังงานศักย์ของโพสิตรอนบนแกนผ่านกลางสี่เหลี่ยม", "พลังงานศักย์ไฟฟ้าของระบบประจุ")
class PositronAxisEnergy(PhysicsSheet):
    def _variant(self, rng):
        x = rng.choice(POSITIONS)
        near, far = (Fraction(1, 2) + x) ** 2 + Fraction(1, 4), (Fraction(1, 2) - x) ** 2 + Fraction(1, 4)
        pair = lambda s, t: radical(16 / s) if s == t else f"{radical(4 / s)}+{radical(4 / t)}"  # noqa: E731
        agree(q09.solve(position=float(x)), 2 / float(near) ** 0.5 + 2 / float(far) ** 0.5)
        single = radical(4 / near) if x >= 0 else radical(4 / far)
        halves = radical(4 / near) if near == far else f"{radical(1 / near)}+{radical(1 / far)}"
        return draw(
            9,
            pair(near, far),
            f"โปรตอนสี่ตัวอยู่ที่มุมของสี่เหลี่ยมจัตุรัสด้านยาว a ที่พิกัด (±a/2, ±a/2) โพสิตรอนอยู่บนแกน x ที่ x = {number(x)}a พลังงานศักย์ของโพสิตรอนเป็นกี่เท่าของ ke²/a",
            r"E_p=\frac{2ke^2}{\sqrt{(a/2+x)^2+(a/2)^2}}+\frac{2ke^2}{\sqrt{(a/2-x)^2+(a/2)^2}}",
            [single, halves, radical(16 / (x * x + Fraction(1, 2)))],
        )


KE2, ELECTRON = 2.307e-28, 9.109e-31
NANO = (0.05, 0.1, 0.2, 0.5, 1.0, 2.0)


def _barrier():
    # Highest point of E_p (units ke^2/a) along the axis, by golden section.
    def energy(x):
        return 2 / sqrt((0.5 + x) ** 2 + 0.25) + 2 / sqrt((0.5 - x) ** 2 + 0.25)

    lo, hi, phi = 0.0, 1.0, (sqrt(5) - 1) / 2
    for _ in range(200):
        x1, x2 = hi - phi * (hi - lo), lo + phi * (hi - lo)
        lo, hi = (lo, x2) if energy(x1) > energy(x2) else (x1, hi)
    return energy((lo + hi) / 2)


@_type(10, "อัตราเร็วต่ำสุดของโพสิตรอนที่ผ่านสี่เหลี่ยมโปรตอน", "พลังงานศักย์ไฟฟ้าของระบบประจุ")
class PositronLaunchSpeed(PhysicsSheet):
    def _variant(self, rng):
        side = rng.choice(NANO)
        speed = q10.solve(side=side)
        unit = KE2 / (ELECTRON * side * 1e-9)
        agree(speed, sqrt(2 * _barrier() * unit))
        return draw(
            10,
            measure(speed),
            f"โปรตอนสี่ตัวยึดไว้ที่มุมของสี่เหลี่ยมจัตุรัสด้านยาว {number(side)} nm โพสิตรอนวิ่งจากระยะไกลมากตามแกน x ที่ผ่านจุดกลางสี่เหลี่ยม (ขนานกับด้าน) ต้องมีอัตราเร็วเริ่มต้นอย่างน้อยกี่ m/s จึงผ่านไปได้ตลอด (ke² = 2.307×10⁻²⁸ J·m, mₑ = 9.109×10⁻³¹ kg, พลังงานศักย์สูงสุดบนแกนประมาณ 5.866 ke²/a)",
            r"\tfrac12m_ev_0^2=E_{p,\max}",
            [measure(sqrt(2 * 4 * sqrt(2) * unit)), measure(sqrt(_barrier() * unit)), measure(sqrt(2 * (_barrier() - 2.049) * unit))],
        )


@_type(11, "ความถี่เชิงมุมของโพสิตรอนที่สั่นรอบจุดกลาง", "การสั่นรอบสมดุลในสนามไฟฟ้า")
class PositronOscillation(PhysicsSheet):
    def _variant(self, rng):
        side = rng.choice(NANO)
        a = side * 1e-9
        omega = q11.solve(side=side)
        agree(omega, sqrt(4 * sqrt(2) * KE2 / (a**3 * ELECTRON)))
        return draw(
            11,
            measure(omega),
            f"โปรตอนสี่ตัวยึดไว้ที่มุมของสี่เหลี่ยมจัตุรัสด้านยาว {number(side)} nm โพสิตรอนที่อยู่นิ่ง ณ จุดกลางสี่เหลี่ยมถูกผลักออกเล็กน้อยแล้วปล่อยให้สั่นในระนาบ ความถี่เชิงมุมของการสั่นเป็นกี่ rad/s (ke² = 2.307×10⁻²⁸ J·m, mₑ = 9.109×10⁻³¹ kg)",
            r"F\approx-\frac{4\sqrt2ke^2}{a^3}x,\quad\omega=\sqrt{K/m_e}",
            [measure(sqrt(4 * KE2 / (a**3 * ELECTRON))), measure(sqrt(8 * sqrt(2) * KE2 / (a**3 * ELECTRON))), measure(omega**2)],
        )


def _discs(rng):
    tube = Fraction(rng.randint(5, 20), 1000)
    speed = rng.randint(5, 30)
    gap = Fraction(rng.randint(1, 5), 1000)
    rim = Fraction(rng.randint(5, 20), 100)
    return tube, speed, gap, rim


DISCS = "อากาศความหนาแน่น {rho} kg/m³ ถูกเป่าด้วยความเร็ว {speed} m/s ลงในท่อรัศมี {tube} m ที่ปลายท่อมีแผ่นกลมรัศมี {rim} m ติดอยู่ และมีแผ่นกลมอีกแผ่นอยู่ด้านล่างห่างออกไป {gap} m อากาศแผ่ออกระหว่างแผ่นตามแนวรัศมี (ไม่คิดความหนืด)"


def _discs_stem(density, tube, speed, gap, rim):
    return DISCS.format(rho=number(density), speed=speed, tube=number(tube), rim=number(rim), gap=number(gap))


@_type(12, "อัตราเร็วลมที่แผ่ออกระหว่างแผ่นกลม", "แบร์นูลลีและสมการความต่อเนื่อง")
class RadialFlowSpeed(PhysicsSheet):
    def _variant(self, rng):
        tube, speed, gap, rim = _discs(rng)
        radius = Fraction(rng.randint(int(tube * 100) + 1, int(rim * 100)), 100)
        exact = tube**2 * speed / (2 * gap * radius)
        agree(q12.solve(tube=float(tube), speed=speed, gap=float(gap), radius=float(radius)), exact)
        return draw(
            12,
            tex(exact),
            _discs_stem(Fraction(6, 5), tube, speed, gap, rim) + f" อัตราเร็วลมที่ระยะ {number(radius)} m จากแกนท่อเป็นกี่ m/s",
            r"\pi a^2v_0=2\pi rtv",
            [tex(2 * exact), tex(tube**2 * speed / radius**2), tex(tube * speed / (2 * gap))],
        )


@_type(13, "ความดันเกจระหว่างแผ่นกลม", "แบร์นูลลีและสมการความต่อเนื่อง")
class RadialFlowPressure(PhysicsSheet):
    def _variant(self, rng):
        tube, speed, gap, rim = _discs(rng)
        radius = Fraction(rng.randint(int(tube * 100) + 1, int(rim * 100) - 1), 100)
        density = Fraction(6, 5)
        k = tube**2 * speed / (2 * gap)
        exact = density * k * k / 2 * (1 / rim**2 - 1 / radius**2)
        agree(q13.solve(density=1.2, tube=float(tube), speed=speed, gap=float(gap), rim=float(rim), radius=float(radius)), exact)
        return draw(
            13,
            measure(float(exact)),
            _discs_stem(density, tube, speed, gap, rim) + f" ความดันอากาศที่ระยะ {number(radius)} m จากแกนท่อต่างจากความดันบรรยากาศ (P − P₀) กี่ปาสกาล (ที่ขอบแผ่นความดันเท่ากับ P₀, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P+\tfrac12\rho v^2=P_0+\tfrac12\rho V_R^2,\quad v=\frac Kr",
            [measure(float(-exact)), measure(float(-density * k * k / (2 * radius**2))), measure(float(2 * exact))],
        )


def _lift(density, tube, speed, gap, rim):
    k = float(tube**2 * speed / (2 * gap))
    a, r = float(tube), float(rim)
    return pi * density * k * k * (log(r / a) - 0.5 + a * a / (2 * r * r)), k


@_type(14, "แรงยกจากผลต่างความดันบนแผ่นกลม", "แรงจากความดันของการไหล")
class DiscPressureLift(PhysicsSheet):
    def _variant(self, rng):
        tube, speed, gap, rim = _discs(rng)
        force = q14.solve(density=1.2, tube=float(tube), speed=speed, gap=float(gap), rim=float(rim))
        exact, k = _lift(1.2, tube, speed, gap, rim)
        agree(force, exact)
        a, r = float(tube), float(rim)
        return draw(
            14,
            measure(force),
            _discs_stem(Fraction(6, 5), tube, speed, gap, rim) + " แรงที่ผลต่างความดันจากรัศมีท่อถึงขอบแผ่นกระทำต่อแผ่นล่างมีขนาดกี่นิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=\int_a^R(P_0-P)\,2\pi r\,dr",
            [
                measure(pi * 1.2 * k * k * log(r / a)),
                measure(2 * force),
                measure(1.2 * k * k / 2 * (1 / a**2 - 1 / r**2) * pi * (r * r - a * a)),
            ],
        )


@_type(15, "แรงจากการเปลี่ยนโมเมนตัมของลมที่ปลายท่อ", "การดลจากการไหลของของไหล")
class JetMomentumForce(PhysicsSheet):
    def _variant(self, rng):
        tube, speed, _, _ = _discs(rng)
        density = Fraction(6, 5)
        exact = density * tube**2 * speed**2
        agree(q15.solve(density=1.2, tube=float(tube), speed=speed), float(exact) * pi)
        return draw(
            15,
            times_pi(exact),
            f"อากาศความหนาแน่น {number(density)} kg/m³ พุ่งลงจากปลายท่อรัศมี {number(tube)} m ด้วยความเร็ว {speed} m/s กระทบแผ่นกลมแล้วแผ่ออกในแนวระดับ แรงที่อากาศกระทำต่อแผ่นในแนวดิ่งเนื่องจากการเปลี่ยนโมเมนตัมมีขนาดกี่นิวตัน",
            r"F=\frac{dp}{dt}=(\rho\pi a^2v_0)v_0",
            [times_pi(exact / 2), times_pi(density * tube**2 * speed), times_pi(2 * exact)],
        )


@_type(16, "มวลมากที่สุดของแผ่นที่ถูกยกขึ้นได้", "แรงจากความดันของการไหล")
class DiscMaxMass(PhysicsSheet):
    def _variant(self, rng):
        tube, speed, gap, rim = _discs(rng)
        lift, _ = _lift(1.2, tube, speed, gap, rim)
        jet = 1.2 * pi * float(tube) ** 2 * speed**2
        if lift < 1.5 * jet:
            raise _Clash
        mass = q16.solve(density=1.2, tube=float(tube), speed=speed, gap=float(gap), rim=float(rim))
        agree(mass, (lift - jet) / 9.8)
        return draw(
            16,
            measure(mass),
            _discs_stem(Fraction(6, 5), tube, speed, gap, rim) + " แผ่นล่างที่มีมวลมากที่สุดกี่กิโลกรัมจึงถูกยกขึ้นได้ (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mg\le\pi\rho K^2\left[\ln\frac Ra-\frac12+\frac{a^2}{2R^2}\right]-\rho\pi a^2v_0^2",
            [measure(lift / 9.8), measure((lift + jet) / 9.8), measure(lift - jet)],
        )


@_type(17, "ค่า κε₀/d จากกระแสผ่านตัวเก็บประจุ", "ความจุของตัวเก็บประจุแผ่นขนาน")
class FoilCapacitor(PhysicsSheet):
    def _variant(self, rng):
        voltage = rng.randint(5, 24)
        current = rng.randint(5, 120)  # microamperes
        area = 50 * rng.randint(2, 12)  # cm^2
        value = q17.solve(voltage=voltage, current=current * 1e-6, area=area * 1e-4)
        agree(value, current * 1e-6 / (2 * pi * 50 * voltage * area * 1e-4))
        return draw(
            17,
            measure(value),
            f"ตัวเก็บประจุแผ่นคู่ขนานทำจากอะลูมิเนียมฟอยล์คั่นด้วยกระดาษ มีพื้นที่ซ้อนทับ {area} cm² ต่อกับแหล่งจ่ายไฟฟ้ากระแสสลับ {voltage} V (rms) ความถี่ 50 Hz วัดกระแสได้ {current} μA (rms) ถ้า X_C ≫ R ค่า κε₀/d ของกระดาษเป็นกี่ F/m²",
            r"I=V\omega C,\quad C=\frac{\kappa\varepsilon_0}{d}A",
            [measure(value * 2 * pi), measure(value * area * 1e-4), measure(value * 1e-4)],
        )


@_type(18, "ค่าคงตัวไดอิเล็กตริกของแผ่นใส", "ความจุของตัวเก็บประจุแผ่นขนาน")
class SheetDielectric(PhysicsSheet):
    def _variant(self, rng):
        hundredths = rng.randint(10, 60)
        per_area = hundredths / 100 * 1e-6  # F/m^2
        thickness = 10 * rng.randint(5, 20)  # micrometres
        kappa = q18.solve(per_area=per_area, thickness=thickness)
        agree(kappa, per_area * thickness * 1e-6 / 8.854e-12)
        return draw(
            18,
            measure(kappa),
            f"ตัวเก็บประจุแผ่นคู่ขนานที่ใช้แผ่นใสหนา {thickness} μm เป็นไดอิเล็กตริก วัดได้ κε₀/d = {number(Fraction(hundredths, 10))}×10⁻⁷ F/m² ค่าคงตัวไดอิเล็กตริก κ ของแผ่นใสเป็นเท่าใด (ε₀ = 8.854×10⁻¹² F/m)",
            r"\kappa=\frac{\kappa\varepsilon_0}{d}\cdot\frac{d}{\varepsilon_0}",
            [measure(kappa * 1e6), measure(per_area / (thickness * 1e-6 * 8.854e-12)), measure(1 / kappa)],
        )


@_type(19, "ความยาวคลื่นเลเซอร์จากการสะท้อนบนสเกลฟุตเหล็ก", "การแทรกสอดจากเกรตติงสะท้อน")
class RulerLaser(PhysicsSheet):
    def _variant(self, rng):
        pitch = rng.choice((1.0, 0.5))  # mm
        distance = rng.choice((1.5, 2.0, 2.5, 3.0))
        tangent = rng.randint(50, 150) / 1000
        wavelength = rng.randint(600, 700) * 1e-9
        order = rng.randint(1, 3)
        c0 = 1 / sqrt(1 + tangent**2)
        cn = c0 - order * wavelength / (pitch * 1e-3)
        mirror = round(distance * tangent, 4)
        spot = round(distance * sqrt(1 / cn**2 - 1), 4)
        answer = q19.solve(pitch=pitch * 1e-3, distance=distance, mirror=mirror, spot=spot, order=order)
        h0, hn = mirror / distance, spot / distance
        s0, sn = h0 / sqrt(1 + h0 * h0), hn / sqrt(1 + hn * hn)
        scale = pitch * 1e-3 / order * 1e9
        return draw(
            19,
            measure(answer),
            f"ส่องแสงเลเซอร์ทำมุมเฉียดกับผิวฟุตเหล็กที่มีขีดสเกลห่างกัน {pitch} mm ฉากตั้งฉากกับฟุตอยู่ห่างจุดที่แสงตกกระทบ {distance} m จุดสว่างจากการสะท้อนปกติอยู่สูงจากระนาบฟุต {mirror:.4f} m และจุดสว่างลำดับที่ {order} อยู่สูง {spot:.4f} m ความยาวคลื่นของแสงเป็นกี่นาโนเมตร (d cos θ − d cos φ = nλ)",
            r"\cos\theta=\frac{L}{\sqrt{L^2+h^2}}",
            [
                measure(scale * (sn - s0)),
                measure(scale * (hn - h0)),
                measure(scale * (sqrt(1 - h0 * h0) - sqrt(1 - hn * hn))),
            ],
        )
