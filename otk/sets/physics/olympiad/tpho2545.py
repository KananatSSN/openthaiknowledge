"""Seeded variants of the reviewed TPhO 1 (2545) national physics olympiad."""

from fractions import Fraction
from math import acos, asin, degrees, isqrt, log

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2545_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2545_physics import q11, q12, q13, q14, q15, q16, q17

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
    1: ("phys.spring_masses_equal_share", "phys.spring_masses_swapped", "phys.spring_masses_all_on_one"),
    2: ("phys.tilted_rod_emf_cosine", "phys.tilted_rod_emf_over_cosine", "phys.tilted_rod_emf_sine"),
    3: ("phys.magnetic_drag_reciprocal", "phys.magnetic_drag_exponent_halved", "phys.magnetic_drag_exponent_doubled"),
    4: ("phys.equal_images_geometric_mean", "phys.equal_images_difference", "phys.equal_images_lens_formula"),
    5: ("phys.rolling_bowl_rotation_ignored", "phys.rolling_bowl_orbit_rate", "phys.rolling_bowl_radius_unreduced"),
    6: ("phys.ionosphere_used_sine", "phys.ionosphere_height_ignored", "phys.ionosphere_not_rooted"),
    7: ("phys.hoop_pe_contact_offset_ignored", "phys.hoop_pe_radius_unreduced", "phys.hoop_pe_sign"),
    8: ("phys.hoop_ke_rotation_ignored", "phys.hoop_ke_radius_unreduced", "phys.hoop_ke_spin_full"),
    9: ("phys.hoop_accel_rotation_ignored", "phys.hoop_accel_radius_unreduced", "phys.hoop_accel_cosine"),
    10: ("phys.hoop_period_rotation_ignored", "phys.hoop_period_radius_unreduced", "phys.hoop_period_inverted"),
    11: ("phys.rim_pendulum_point_mass", "phys.rim_pendulum_centre_inertia", "phys.rim_pendulum_halved"),
    13: ("phys.mhd_level_doubled", "phys.mhd_level_halved", "phys.mhd_level_used_plate_length"),
    14: ("phys.mhd_heat_conductivity_as_resistivity", "phys.mhd_heat_halved", "phys.mhd_heat_current_not_squared"),
    15: ("phys.cooling_room_ignored", "phys.cooling_reciprocal_decay", "phys.cooling_exponent_doubled"),
    16: ("phys.cooling_beta_log_multiplied", "phys.cooling_beta_ratio_minus_one", "phys.cooling_beta_ratio"),
    17: ("phys.airy_factor_omitted", "phys.airy_factor_inverted", "phys.airy_offset_doubled"),
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
    sheet_id = "tpho2545_physics"
    sheet = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 1 (2545)"


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2545_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


COSINES = (Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13), Fraction(1, 2))


def _sine(cos):
    """sin for a cosine from COSINES, as (exact or None, square)."""
    square = 1 - cos * cos
    root = Fraction(isqrt(square.numerator), isqrt(square.denominator))
    return (root if root * root == square else None), square


@_type(1, "ตำแหน่งมวลบนสปริงที่ปล่อยจากหยุดนิ่ง", "ศูนย์กลางมวลของระบบ")
class SpringCentre(PhysicsSheet):
    def expr(self, rng):
        near, far = rng.sample((1, 2, 3, 4, 5), 2)
        gap = Fraction(rng.randint(5, 20), 10)
        length = Fraction(rng.randint(12, 25), 10)
        later = length - Fraction(rng.randint(1, 6), 10)
        shrink = length - later
        exact = gap + far * shrink / (near + far)
        answer = agree(q01.solve(near=near, far=far, gap=float(gap), length=float(length), later=float(later)), exact)
        return draw(
            1,
            tex(answer),
            f"มวล A {near} kg และ B {far} kg ติดปลายสปริงเบาที่ถูกยืดยาว {number(length)} m บนพื้นลื่น A อยู่ห่างกำแพง {number(gap)} m และ B อยู่ไกลออกไป ปล่อยทั้งสองจากหยุดนิ่งพร้อมกัน เมื่อสปริงหดเหลือยาว {number(later)} m มวล A อยู่ห่างกำแพงกี่ m",
            r"x_{cm}=\frac{m_Ax_A+m_Bx_B}{m_A+m_B}=\text{const}",
            [tex(gap + shrink / 2), tex(gap + near * shrink / (near + far)), tex(gap + shrink)],
        )


@_type(2, "แรงเคลื่อนเหนี่ยวนำของแท่งที่เลื่อนบนราง", "แรงเคลื่อนไฟฟ้าเหนี่ยวนำ")
class TiltedRodEmf(PhysicsSheet):
    def expr(self, rng):
        cos = rng.choice(COSINES[:4])
        sine, _ = _sine(cos)
        speed = rng.randint(2, 12)
        separation = Fraction(rng.randint(2, 10), 10)
        field = Fraction(rng.randint(1, 10), 10)
        exact = speed * separation * field
        answer = agree(q02.solve(speed=speed, separation=float(separation), field=float(field)), exact)
        return draw(
            2,
            tex(answer),
            f"รางตัวนำเกลี้ยงขนานสองเส้นห่างกัน {number(separation)} m ต่อปลายด้วยตัวต้านทาน อยู่ในสนามแม่เหล็ก {number(field)} T ตั้งฉากกับระนาบราง แท่งตัวนำวางพาดรางโดยเอียงทำมุม θ กับแนวตั้งฉากกับราง (cos θ = {number(cos)}) และเลื่อนไปตามรางด้วยความเร็ว {speed} m/s แรงเคลื่อนไฟฟ้าเหนี่ยวนำเป็นกี่โวลต์",
            r"\mathcal E=\frac{d\Phi}{dt}=B\frac{dA}{dt}=BLv",
            [tex(exact * cos), tex(exact / cos), tex(exact * sine)],
        )


@_type(3, "ความเร็วของแท่งที่ถูกหน่วงด้วยแรงแม่เหล็ก", "แรงเคลื่อนไฟฟ้าเหนี่ยวนำ")
class MagneticDrag(PhysicsSheet):
    def expr(self, rng):
        speed = rng.randint(2, 20)
        n = rng.randint(1, 4)
        separation, field = Fraction(1, 2), rng.choice((1, 2))
        mass = Fraction(rng.randint(1, 4), 2)
        resistance = rng.choice((1, 2))
        rate = (separation * field) ** 2 / (mass * resistance)
        time = n / rate
        agree(
            q03.solve(speed=speed, separation=float(separation), field=field, mass=float(mass), resistance=resistance, time=float(time)),
            speed * 2.718281828459045 ** (-n),
        )
        fmt = lambda k: rf"{speed}e^{{-{k}}}" if k != 1 else rf"{speed}e^{{-1}}"
        return draw(
            3,
            fmt(n),
            f"แท่งตัวนำมวล {number(mass)} kg เลื่อนบนรางลื่นห่างกัน {number(separation)} m ที่ต่อปลายด้วยตัวต้านทาน {resistance} Ω ในสนามแม่เหล็ก {field} T ตั้งฉากกับระนาบราง ความเร็วต้น {speed} m/s ไม่มีแรงอื่น ที่เวลา t = {number(time)} s แท่งมีความเร็วกี่ m/s",
            r"M\frac{dv}{dt}=-\frac{L^2B^2}{R}v",
            [tex(Fraction(speed, 1 + n)), rf"{speed}e^{{-{tex(Fraction(n, 2))}}}", rf"{speed}e^{{-{2 * n}}}"],
        )


@_type(4, "ความยาวโฟกัสจากภาพจริงและภาพเสมือนขนาดเท่ากัน", "สมการเลนส์และกำลังขยายภาพเสมือน")
class EqualImages(PhysicsSheet):
    def expr(self, rng):
        near = rng.randint(2, 12)
        far = near + 2 * rng.randint(1, 10)
        answer = agree(q04.solve(near=near, far=far), Fraction(near + far, 2))
        return draw(
            4,
            tex(answer),
            f"วางวัตถุห่างเลนส์นูนบาง {near} cm ได้ภาพเสมือน และเมื่อวางวัตถุห่าง {far} cm ได้ภาพจริงที่มีขนาดเท่ากับภาพเสมือนนั้น ความยาวโฟกัสของเลนส์เป็นกี่ cm",
            r"\frac{f}{f-a}=\frac{f}{b-f}",
            [radical(near * far), tex(Fraction(far - near, 2)), tex(Fraction(near * far, near + far))],
        )


@_type(5, "อัตราเร็วเชิงมุมสูงสุดของทรงกลมกลิ้งในชาม", "พลังงานการเลื่อนที่ร่วมการหมุน")
class RollingBowl(PhysicsSheet):
    def expr(self, rng):
        bowl = Fraction(rng.randint(5, 30), 10)
        ball = Fraction(rng.randint(1, 4), 10)
        cos = rng.choice(COSINES)
        squared = Fraction(100, 7) * (bowl - ball) * (1 - cos) / ball**2
        agree(q05.solve(bowl=float(bowl), ball=float(ball), cosine=float(cos)) ** 2, squared)
        return draw(
            5,
            radical(squared),
            f"ทรงกลมตันรัศมี {number(ball)} m กลิ้งโดยไม่ไถลจากหยุดนิ่งในชามทรงกลมรัศมีภายใน {number(bowl)} m เริ่มที่ตำแหน่งซึ่งแนวจากศูนย์กลางชามทำมุม θ₀ กับแนวดิ่ง (cos θ₀ = {number(cos)}) อัตราเร็วเชิงมุมสูงสุดของทรงกลมรอบแกนผ่านศูนย์กลางมวลเป็นกี่ rad/s (I = (2/5)Mr², g = 10 m/s²)",
            r"\tfrac7{10}Mv^2=Mg(R-r)(1-\cos\theta_0),\quad\omega=\frac vr",
            [
                radical(20 * (bowl - ball) * (1 - cos) / ball**2),
                radical(Fraction(100, 7) * (1 - cos) / (bowl - ball)),
                radical(Fraction(100, 7) * bowl * (1 - cos) / ball**2),
            ],
        )


@_type(6, "ความยาวคลื่นจำกัดที่ไอโอโนสเฟียร์สะท้อนกลับหมด", "การสะท้อนกลับหมด")
class IonosphereLimit(PhysicsSheet):
    def expr(self, rng):
        root_a = rng.randint(1, 10)
        sine = rng.choice((Fraction(3, 5), Fraction(4, 5), Fraction(1, 2), Fraction(12, 13)))
        height = rng.choice((Fraction(1, 4), Fraction(1, 5), Fraction(1, 10), Fraction(1, 2)))
        s1 = sine / (1 + height)
        squared = root_a**2 * (1 - s1 * s1)
        agree(q06.solve(constant=root_a**2, sine=float(sine), height=float(height)) ** 2, squared)
        return draw(
            6,
            radical(squared),
            f"ดรรชนีหักเหของไอโอโนสเฟียร์สำหรับคลื่นวิทยุคือ √(1 − λ²/A) โดย A = {root_a**2} m² ขอบล่างของไอโอโนสเฟียร์อยู่สูง h = {number(height)}R เหนือผิวโลกรัศมี R คลื่นออกจากผิวโลกทำมุม α กับแนวดิ่ง (sin α = {number(sine)}) ความยาวคลื่นสั้นที่สุดที่ยังสะท้อนกลับหมดได้เป็นกี่ m",
            r"(R+h)\sin\theta_1=R\sin\alpha,\quad\sin\theta_1\ge n",
            [tex(root_a * s1), radical(root_a**2 * (1 - sine * sine)), tex(squared)],
        )


@_type(7, "พลังงานศักย์ของห่วงที่กลิ้งบนแกน", "พลังงานศักย์ของวัตถุแข็งเกร็ง")
class HoopPotential(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 6)
        hoop = Fraction(rng.randint(3, 10), 10)
        rod = Fraction(rng.randint(1, 2), 10)
        cos = rng.choice(COSINES)
        exact = -10 * mass * (rod + (hoop - rod) * cos)
        answer = q07.solve(mass=mass, hoop=float(hoop), rod=float(rod), angle=degrees(acos(float(cos))))
        agree(answer, exact)
        return draw(
            7,
            tex(exact),
            f"แกนทรงกระบอกรัศมี {number(rod)} m ยึดตั้งฉากกับผนัง ห่วงบางมวล {mass} kg รัศมี {number(hoop)} m แกว่งรอบแกนในระนาบดิ่งโดยกลิ้งไม่ไถล ให้จุดสัมผัสบนสุดของแกน (A) เป็นระดับอ้างอิงพลังงานศักย์ศูนย์ ขณะเส้นจากศูนย์กลางแกนไปศูนย์กลางห่วงทำมุม θ กับแนวดิ่ง (cos θ = {number(cos)}) พลังงานศักย์ของห่วงเป็นกี่ J (g = 10 m/s²)",
            r"y_{cm}=-r-(R-r)\cos\theta",
            [tex(-10 * mass * (hoop - rod) * cos), tex(-10 * mass * hoop * cos), tex(-exact)],
        )


@_type(8, "พลังงานจลน์ของห่วงที่กลิ้งบนแกน", "พลังงานการเลื่อนที่ร่วมการหมุน")
class HoopKinetic(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 6)
        hoop = Fraction(rng.randint(3, 10), 10)
        rod = Fraction(rng.randint(1, 2), 10)
        rate = rng.randint(1, 5)
        exact = mass * (hoop - rod) ** 2 * rate**2
        answer = agree(q08.solve(mass=mass, hoop=float(hoop), rod=float(rod), rate=rate), exact)
        return draw(
            8,
            tex(answer),
            f"ห่วงบางมวล {mass} kg รัศมี {number(hoop)} m กลิ้งไม่ไถลรอบแกนรัศมี {number(rod)} m ที่ยึดกับผนัง ขณะเส้นจากศูนย์กลางแกนไปศูนย์กลางห่วงหมุนด้วยอัตรา dθ/dt = {rate} rad/s พลังงานจลน์ของห่วงเป็นกี่ J",
            r"v_{cm}=(R-r)\dot\theta,\quad\omega=\left(1-\frac rR\right)\dot\theta",
            [tex(exact / 2), tex(mass * hoop**2 * rate**2), tex(exact / 2 + mass * hoop**2 * rate**2 / 2)],
        )


@_type(9, "ความเร่งเชิงมุมของห่วงที่กลิ้งบนแกน", "การแกว่งของวัตถุแข็งเกร็ง")
class HoopAcceleration(PhysicsSheet):
    def expr(self, rng):
        hoop = Fraction(rng.randint(3, 10), 10)
        rod = Fraction(rng.randint(1, 2), 10)
        cos = rng.choice(COSINES[:4])
        sine, _ = _sine(cos)
        exact = -10 * sine / (2 * (hoop - rod))
        answer = agree(q09.solve(hoop=float(hoop), rod=float(rod), angle=degrees(asin(float(sine)))), exact)
        return draw(
            9,
            tex(answer),
            f"ห่วงบางรัศมี {number(hoop)} m กลิ้งไม่ไถลรอบแกนรัศมี {number(rod)} m ขณะเส้นจากศูนย์กลางแกนไปศูนย์กลางห่วงทำมุม θ กับแนวดิ่ง (sin θ = {number(sine)} และ cos θ = {number(cos)}) d²θ/dt² เป็นกี่ rad/s² (g = 10 m/s²)",
            r"M(R-r)^2\dot\theta^2-Mg(R-r)\cos\theta=\text{const}",
            [tex(2 * exact), tex(-10 * sine / (2 * hoop)), tex(-10 * cos / (2 * (hoop - rod)))],
        )


@_type(10, "คาบการแกว่งน้อยๆ ของห่วงบนแกน", "การแกว่งของวัตถุแข็งเกร็ง")
class HoopPeriod(PhysicsSheet):
    def expr(self, rng):
        hoop = Fraction(rng.randint(3, 15), 10)
        rod = Fraction(rng.randint(1, 2), 10)
        squared = 4 * 2 * (hoop - rod) / 10
        agree(q10.solve(hoop=float(hoop), rod=float(rod)) ** 2, squared)
        return draw(
            10,
            pi_radical(squared),
            f"ห่วงบางรัศมี {number(hoop)} m กลิ้งไม่ไถลรอบแกนรัศมี {number(rod)} m ที่ยึดในแนวระดับ แกว่งด้วยแอมพลิจูดน้อยๆ คาบการแกว่งเป็นกี่วินาที (g = 10 m/s²)",
            r"\ddot\theta=-\frac{g}{2(R-r)}\theta",
            [pi_radical(squared / 2), pi_radical(4 * 2 * hoop / 10), pi_radical(1 / squared * 16)],
        )


@_type(11, "คาบการแกว่งของห่วงรอบหมุดเล็ก", "การแกว่งของวัตถุแข็งเกร็ง")
class RimPendulum(PhysicsSheet):
    def expr(self, rng):
        hoop = Fraction(rng.randint(2, 25), 10)
        squared = 4 * 2 * hoop / 10
        agree(q11.solve(hoop=float(hoop)) ** 2, squared)
        return draw(
            11,
            pi_radical(squared),
            f"ห่วงบางรัศมี {number(hoop)} m แขวนบนหมุดเล็กที่ขอบห่วง แกว่งในระนาบของห่วงด้วยแอมพลิจูดน้อยๆ คาบการแกว่งเป็นกี่วินาที (g = 10 m/s²)",
            r"T=2\pi\sqrt{\frac{I}{MgR}},\quad I=2MR^2",
            [pi_radical(4 * hoop / 10), pi_radical(4 * hoop / 20), pi_radical(squared / 4)],
        )


ARM = {"left": "ระดับของเหลวในแขนซ้ายสูงขึ้น (แขนขวาลดลง)", "right": "ระดับของเหลวในแขนขวาสูงขึ้น (แขนซ้ายลดลง)"}


@_type(12, "ทิศแรงแม่เหล็กต่อของเหลวนำไฟฟ้าในท่อ", "แรงแม่เหล็กต่อกระแส")
class LiquidPumpDirection(ChoiceType):
    sheet_id = "tpho2545_physics"
    sheet = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 1 (2545)"

    def compose(self, rng):
        up, inward = rng.random() < 0.5, rng.random() < 0.5
        arm = q12.solve(current_up=up, field_in=inward)
        other = "right" if arm == "left" else "left"
        return (
            "ท่อแนวระดับรูปตัวยูหน้าตัดสี่เหลี่ยมบรรจุของเหลวนำไฟฟ้า ช่วงหนึ่งของท่อมีแผ่นโลหะด้านบนและล่าง ผ่านกระแสตรงในของเหลว"
            f"{'จากล่างขึ้นบน' if up else 'จากบนลงล่าง'} และมีสนามแม่เหล็กสม่ำเสมอ{'พุ่งเข้า' if inward else 'พุ่งออกจาก'}ระนาบกระดาษบริเวณนั้น "
            "แขนซ้ายและแขนขวาของท่อตั้งขึ้นเปิดสู่อากาศ ผลที่เกิดขึ้นคือข้อใด",
            ARM[arm],
            (
                named("phys.lorentz_force_direction_reversed", ARM[other]),
                named("phys.lorentz_force_ignored", "ระดับของเหลวทั้งสองแขนเท่าเดิม"),
                named("phys.lorentz_force_both_arms", "ระดับของเหลวสูงขึ้นทั้งสองแขน"),
            ),
        )


@_type(13, "ผลต่างระดับของเหลวจากแรงแม่เหล็ก", "แรงแม่เหล็กต่อกระแส")
class LiquidPumpLevel(PhysicsSheet):
    def expr(self, rng):
        current = Fraction(rng.randint(1, 30), 10)
        field = Fraction(rng.randint(1, 10), 10)
        density = rng.choice((1000, 1200, 800))
        width = Fraction(rng.randint(1, 4), 100)
        plate = Fraction(rng.randint(5, 20), 100)
        exact = current * field / (density * 10 * width)
        answer = agree(q13.solve(current=float(current), field=float(field), density=density, width=float(width), g=10), exact)
        cm = lambda v: tex(v * 100)
        return draw(
            13,
            cm(answer),
            f"ท่อหน้าตัดสี่เหลี่ยม (สูง a ระหว่างแผ่นโลหะ กว้าง b = {number(width * 100)} cm) บรรจุของเหลวนำไฟฟ้าความหนาแน่น {density} kg/m³ กระแส {number(current)} A ผ่านของเหลวระหว่างแผ่นโลหะยาว {number(plate * 100)} cm ในสนามแม่เหล็ก {number(field)} T ตั้งฉาก ทำให้ระดับของเหลวในสองแขนต่างกัน h กี่ cm (g = 10 m/s²)",
            r"\rho gh\,ab=IaB",
            [cm(2 * exact), cm(exact / 2), cm(current * field / (density * 10 * plate))],
        )


@_type(14, "ความร้อนในของเหลวนำไฟฟ้า", "พลังงานไฟฟ้าและความร้อนจูล")
class LiquidPumpHeat(PhysicsSheet):
    def expr(self, rng):
        gap = width = Fraction(1, 100)
        length = Fraction(rng.randint(5, 20), 100)
        level = Fraction(rng.randint(1, 3), 100)
        field = Fraction(rng.randint(5, 20), 10)
        sigma = rng.choice((1, 2, 4))
        density = 1200
        current = density * 10 * width * level / field
        exact = current**2 * gap / (sigma * width * length)
        answer = agree(
            q14.solve(gap=float(gap), width=float(width), length=float(length), level=float(level), field=float(field), sigma=sigma, density=density, g=10),
            exact,
        )
        return draw(
            14,
            tex(answer),
            f"ท่อหน้าตัด 1.0 cm × 1.0 cm บรรจุสารละลายนำไฟฟ้า (สภาพนำ {sigma} Ω⁻¹m⁻¹ ความหนาแน่น 1.2×10³ kg/m³) ระหว่างแผ่นโลหะยาว {number(length * 100)} cm ในสนาม {number(field)} T กระแสทำให้ระดับสองแขนต่างกัน {number(level * 100)} cm อัตราการเกิดความร้อนในของเหลวเป็นกี่วัตต์ (g = 10 m/s²)",
            r"I=\frac{Dgbh}{B},\quad W=I^2\frac{a}{\sigma bL}",
            [
                tex(current**2 * sigma * gap / (width * length)),
                tex(exact / 2),
                tex(current * gap / (sigma * width * length)),
            ],
        )


@_type(15, "อุณหภูมิตามกฎการเย็นตัวของนิวตัน", "การถ่ายโอนความร้อนและการเย็นตัว")
class NewtonCooling(PhysicsSheet):
    def expr(self, rng):
        room = rng.choice((20, 25, 30))
        start = room + 10 * rng.randint(3, 7)
        beta = 60 * rng.randint(5, 20)
        n = rng.randint(1, 3)
        excess = start - room
        agree(q15.solve(room=room, start=start, beta=beta, time=n * beta), room + excess * 2.718281828459045 ** (-n))
        return draw(
            15,
            rf"{room}+{excess}e^{{-{n}}}",
            f"กระป๋องน้ำร้อนเย็นตัวในห้องอุณหภูมิ {room} °C ตามกฎ dT/dt = −(T − Tₐ)/β โดย β = {beta} s เริ่มที่ {start} °C เมื่อเวลาผ่านไป {n * beta} s น้ำมีอุณหภูมิกี่ °C",
            r"T=T_a+(T_0-T_a)e^{-t/\beta}",
            [rf"{start}e^{{-{n}}}", tex(room + Fraction(excess, 1 + n)), rf"{room}+{excess}e^{{-{2 * n}}}"],
        )


@_type(16, "ค่าคงตัวการเย็นตัวจากข้อมูลสองค่า", "การถ่ายโอนความร้อนและการเย็นตัว")
class CoolingConstant(PhysicsSheet):
    def expr(self, rng):
        room = rng.choice((20, 25, 30))
        ratio = rng.choice((2, 3, 4))
        second_excess = 10 * rng.randint(1, 4)
        first = room + ratio * second_excess
        second = room + second_excess
        gap = 60 * rng.randint(2, 15)
        agree(q16.solve(room=room, first=first, second=second, gap=gap), gap / log(ratio))
        return draw(
            16,
            rf"\frac{{{gap}}}{{\ln {ratio}}}",
            f"กระป๋องน้ำร้อนเย็นตัวตามกฎการเย็นตัวของนิวตันในห้อง {room} °C อ่านอุณหภูมิได้ {first} °C แล้วอีก {gap} s ต่อมาอ่านได้ {second} °C ค่าคงตัว β ในสมการ dT/dt = −(T − Tₐ)/β เป็นกี่วินาที",
            r"\ln(T-T_a)=\ln(T_0-T_a)-\frac t\beta",
            [rf"{gap}\ln {ratio}", tex(Fraction(gap, ratio - 1)), tex(Fraction(gap, ratio))],
        )


@_type(17, "ความยาวคลื่นจากวงแหวนมืดของการเลี้ยวเบน", "การเลี้ยวเบนของแสง")
class AiryWavelength(PhysicsSheet):
    def expr(self, rng):
        diameter = rng.choice((20, 25, 30, 35))  # x 1e-4 cm
        distance = rng.choice((20, 25, 30, 40, 50))
        offset = rng.choice((Fraction(1, 2), Fraction(1)))
        exact = 1000 * diameter * offset / (Fraction(122, 100) * distance)
        answer = agree(q17.solve(diameter=diameter, distance=distance, offset=float(offset)), exact)
        return draw(
            17,
            tex(answer),
            f"ลำแสงขนานผ่านผงไลโคโพเดียมเส้นผ่านศูนย์กลาง {diameter}×10⁻⁴ cm เกิดวงแหวนมืดวงในสุดที่ D sin θ = 1.22λ เมื่อแผ่นกระจกอยู่ห่างแผ่นที่มีรูเป็น {distance} cm วงแหวนมืดวงในสุดทับรูที่อยู่ห่างรูกลาง {number(offset)} cm พอดี (θ ≈ ระยะรู/ระยะห่าง) ความยาวคลื่นแสงเป็นกี่นาโนเมตร",
            r"D\sin\theta=1.22\lambda,\quad\theta\approx\frac{s}{x}",
            [tex(exact * Fraction(122, 100)), tex(exact * Fraction(122, 100) ** 2), tex(2 * exact)],
        )
