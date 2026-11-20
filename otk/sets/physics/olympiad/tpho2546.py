"""Seeded variants of the reviewed TPhO 2 (2546) national physics olympiad."""

from fractions import Fraction
from math import acos, degrees, floor, isqrt, log10, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2546_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2546_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21

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


def figures(value):
    """A nonzero float to three significant figures, as plain text."""
    digits = 2 - floor(log10(abs(value)))
    return f"{round(value, digits):.{digits}f}" if digits > 0 else str(int(round(value, digits)))




SLIPS = {
    1: ("phys.slide_cylinder_fixed", "phys.slide_total_mass_dropped", "phys.slide_sine_cosine_swapped"),
    2: ("phys.slide_recoil_mass_only", "phys.slide_recoil_cosine_dropped", "phys.slide_recoil_sine"),
    3: ("phys.slide_first_order_half_dropped", "phys.slide_first_order_sine", "phys.slide_first_order_angle_dropped"),
    5: ("phys.fuse_scale_area_once", "phys.fuse_scale_current_not_squared", "phys.fuse_scale_radius_inverted"),
    6: ("phys.fuse_rate_pi_once", "phys.fuse_rate_radius_squared", "phys.fuse_rate_current_not_squared"),
    7: ("phys.fuse_loss_sign", "phys.fuse_loss_perimeter_halved", "phys.fuse_loss_area_for_perimeter"),
    8: ("phys.fuse_final_factor_two_dropped", "phys.fuse_final_radius_power", "phys.fuse_final_pi_once"),
    9: ("phys.fuse_melt_factor_two_dropped", "phys.fuse_melt_radius_power", "phys.fuse_melt_pi_dropped"),
    10: ("phys.shell_potential_point_distance", "phys.shell_potential_radius_not_divided", "phys.shell_potential_four_pi_kept"),
    11: ("phys.shell_integral_half_dropped", "phys.shell_integral_lower_limit_dropped", "phys.shell_integral_power_raised"),
    12: ("phys.ball_potential_distance_not_divided", "phys.ball_potential_shell_formula", "phys.ball_potential_four_pi_kept"),
    13: ("phys.ball_potential_inner_dropped", "phys.ball_potential_surface_value", "phys.ball_potential_parts_subtracted"),
    14: ("phys.point_charge_sign_dropped", "phys.point_charge_distance_difference", "phys.point_charge_distance_to_centre"),
    15: ("phys.field_gradient_sign", "phys.field_point_charge_not_squared", "phys.field_outside_formula_inside"),
    16: ("phys.equilibrium_separation_not_doubled", "phys.equilibrium_ball_field_third_dropped", "phys.equilibrium_cube_as_square"),
    17: ("phys.rc_rms_amplitude", "phys.rc_voltage_across_resistor", "phys.rc_impedance_not_rooted"),
    18: ("phys.rc_angular_frequency_as_f", "phys.rc_slope_ratio_not_rooted", "phys.rc_omega_omitted"),
    19: ("phys.bifilar_quarter_dropped", "phys.bifilar_separation_not_squared", "phys.bifilar_period_not_squared"),
    21: ("phys.black_box_factor_two_dropped", "phys.black_box_sphere_formula", "phys.black_box_root_order"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 2 (2546)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2546_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2546_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


COSINES = (Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13), Fraction(1, 2))
SLIDE = "ทรงกระบอกตันเสี้ยวหนึ่งในสี่ PCQ มวล {big} kg รัศมี {radius} m ผิวลื่น วางบนพื้นราบลื่น มวลเล็ก {small} kg ไถลจากใกล้ยอด P จากหยุดนิ่ง ขณะเส้นจากจุด C ถึงมวลเล็กทำมุม θ กับแนวดิ่ง (cos θ = {cos})"
SLIDE_HINT = r"m(v\cos\theta-V)=MV,\quad\tfrac12m\left[(v\cos\theta-V)^2+v^2\sin^2\theta\right]+\tfrac12MV^2=mgR(1-\cos\theta)"


def _slide(rng):
    small = rng.randint(1, 4)
    big = rng.randint(1, 10)
    radius = Fraction(rng.randint(2, 20), 10)
    cos = rng.choice(COSINES)
    squared = 20 * radius * (big + small) * (1 - cos) / (big + small * (1 - cos * cos))
    return small, big, radius, cos, squared


@_type(1, "อัตราเร็วของมวลที่ไถลบนทรงกระบอกที่เลื่อนได้", "โมเมนตัมแนวระดับของลิ่มและมวล")
class SlidingMassSpeed(PhysicsSheet):
    def _variant(self, rng):
        small, big, radius, cos, squared = _slide(rng)
        agree(q01.solve(big=big, small=small, radius=float(radius), angle=degrees(acos(cos)), g=10) ** 2, squared)
        stem = SLIDE.format(big=big, radius=number(radius), small=small, cos=number(cos))
        return draw(
            1,
            radical(squared),
            f"{stem} อัตราเร็ว v ของมวลเล็กเทียบกับทรงกระบอกเป็นกี่ m/s (g = 10 m/s²)",
            SLIDE_HINT,
            [
                radical(20 * radius * (1 - cos)),
                radical(20 * radius * big * (1 - cos) / (big + small * (1 - cos * cos))),
                radical(20 * radius * (big + small) * (1 - cos) / (big + small * cos * cos)),
            ],
        )


@_type(2, "อัตราเร็วของทรงกระบอกที่ถูกมวลไถลดัน", "โมเมนตัมแนวระดับของลิ่มและมวล")
class CylinderRecoil(PhysicsSheet):
    def _variant(self, rng):
        small, big, radius, cos, squared = _slide(rng)
        exact = small**2 * cos**2 * squared / (big + small) ** 2
        agree(q02.solve(big=big, small=small, radius=float(radius), angle=degrees(acos(cos)), g=10) ** 2, exact)
        stem = SLIDE.format(big=big, radius=number(radius), small=small, cos=number(cos))
        return draw(
            2,
            radical(exact),
            f"{stem} ทรงกระบอกเคลื่อนที่ด้วยอัตราเร็ว V กี่ m/s (g = 10 m/s²)",
            SLIDE_HINT,
            [
                radical(small**2 * cos**2 * squared / big**2),
                radical(small**2 * squared / (big + small) ** 2),
                radical(small**2 * (1 - cos * cos) * squared / (big + small) ** 2),
            ],
        )


@_type(3, "การประมาณอันดับหนึ่งเมื่อมวลเล็กมาก", "โมเมนตัมแนวระดับของลิ่มและมวล")
class SlideFirstOrder(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice((50, 100, 200, 250, 500, 1000))
        cos = rng.choice(COSINES)
        exact = cos * cos / (2 * n)
        agree(q03.solve(ratio=1 / n, angle=degrees(acos(cos))), exact)
        return draw(
            3,
            tex(exact),
            f"มวลเล็ก m ไถลจากยอดทรงกระบอกตันเสี้ยวหนึ่งในสี่มวล M = {n}m ที่วางบนพื้นราบลื่น ขณะเส้นจากจุด C ถึงมวลทำมุม θ กับแนวดิ่ง (cos θ = {number(cos)}) อัตราเร็ว v ของมวลเทียบกับทรงกระบอกมากกว่าค่า √(2gR(1 − cos θ)) ของทรงกระบอกที่ถูกยึดเป็นสัดส่วน (v − v₀)/v₀ ประมาณเท่าใด (ถึงอันดับหนึ่งของ m/M)",
            r"v^2=\frac{2gR(1+m/M)(1-\cos\theta)}{1+(m/M)\sin^2\theta},\quad(1\pm x)^n\approx1\pm nx",
            [tex(cos * cos / n), tex((1 - cos * cos) / (2 * n)), tex(Fraction(1, 2 * n))],
        )


DETACH = {
    "smaller": "เล็กกว่า cos⁻¹(2/3) เพราะทรงกระบอกเร่งหนีทำให้แรงปฏิกิริยาหมดเร็วขึ้น",
    "equal": "เท่ากับ cos⁻¹(2/3) พอดี เพราะแรงปฏิกิริยาหมดเมื่อ cos θ = 2/3",
    "larger": "ใหญ่กว่า cos⁻¹(2/3) เพราะมวลเล็กเคลื่อนช้าลงจึงเกาะผิวได้นานขึ้น",
    "never": "ไม่หลุดเลยจนถึง θ = 90° เพราะแรงปฏิกิริยาไม่เคยเป็นศูนย์",
}


@_type(4, "มุมที่มวลหลุดจากผิวทรงกระบอกที่เลื่อนได้", "แรงในกรอบอ้างอิงที่มีความเร่ง")
class DetachAngle(ChoiceType):
    sheet_id = "tpho2546_physics"
    sheet = SHEET

    def compose(self, rng):
        ratio = rng.choice((0, 1, 2, 3, 5, 10))
        answer = q04.solve(mass_ratio=ratio)
        setting = (
            "ทรงกระบอกถูกยึดติดกับพื้น"
            if ratio == 0
            else f"ทรงกระบอกมีมวล M = {ratio}m วางบนพื้นราบลื่น" if ratio != 1 else "ทรงกระบอกมีมวล M = m วางบนพื้นราบลื่น"
        )
        if answer == "equal":
            wrongs = (
                named("phys.detach_fixed_as_free", DETACH["smaller"]),
                named("phys.detach_direction_reversed", DETACH["larger"]),
                named("phys.detach_never", DETACH["never"]),
            )
        else:
            wrongs = (
                named("phys.detach_free_cylinder_ignored", DETACH["equal"]),
                named("phys.detach_direction_reversed", DETACH["larger"]),
                named("phys.detach_never", DETACH["never"]),
            )
        return (
            f"มวลเล็ก m ไถลจากใกล้ยอด P ของทรงกระบอกตันเสี้ยวหนึ่งในสี่ผิวลื่นรัศมี R โดย{setting} "
            "มุม θ (จากแนวดิ่ง) ที่มวลหลุดจากผิวทรงกระบอกเป็นอย่างไร",
            DETACH[answer],
            wrongs,
        )


METALS = (
    ("ดีบุก", Fraction(115, 10), Fraction(23, 100), Fraction(73, 10)),
    ("ทองแดง", Fraction(17, 10), Fraction(39, 100), Fraction(89, 10)),
    ("อะลูมิเนียม", Fraction(28, 10), Fraction(9, 10), Fraction(27, 10)),
    ("ตะกั่ว", Fraction(21), Fraction(13, 100), Fraction(113, 10)),
)


def _wire(metal):
    name, rho, heat, density = metal
    return (
        f"ลวด{name}ยาว 5.0 cm (สภาพต้านทาน {number(rho)}×10⁻⁶ Ω·cm ความจุความร้อนจำเพาะ {number(heat)} J/g°C "
        f"ความหนาแน่น {number(density)} g/cm³)"
    )


@_type(5, "อัตราการเพิ่มอุณหภูมิของฟิวส์เมื่อเปลี่ยนกระแสและรัศมี", "พลังงานไฟฟ้าและความร้อนจูล")
class FuseScaling(PhysicsSheet):
    def _variant(self, rng):
        k = rng.choice((2, 3))
        s = rng.choice((Fraction(1, 2), Fraction(2), Fraction(3, 2), Fraction(1, 3), Fraction(3)))
        exact = k * k / s**4
        agree(q05.solve(current_factor=k, radius_factor=float(s)), exact)
        return draw(
            5,
            tex(exact),
            f"ลวดฟิวส์ที่ไม่มีการสูญเสียความร้อนออกสู่ภายนอก ถ้าเพิ่มกระแสเป็น {k} เท่า และเปลี่ยนเป็นลวดชนิดเดียวกันยาวเท่าเดิมแต่รัศมีเป็น {number(s)} เท่าของเดิม อัตราการเพิ่มอุณหภูมิ dT/dt เป็นกี่เท่าของเดิม",
            r"\frac{dT}{dt}=\frac{P}{c\,m}=\frac{i^2\rho\ell/(\pi r^2)}{cD\pi r^2\ell}",
            [tex(k * k / s**2), tex(k / s**4), tex(k * k * s**4)],
        )


@_type(6, "อัตราการเพิ่มอุณหภูมิของลวดฟิวส์", "พลังงานไฟฟ้าและความร้อนจูล")
class FuseRate(PhysicsSheet):
    def _variant(self, rng):
        metal = rng.choice(METALS)
        _, rho, heat, density = metal
        current = rng.randint(2, 20)
        radius = Fraction(rng.randint(5, 20), 100)
        exact = current**2 * rho / 10**6 / (radius**4 * heat * density)
        rate = agree(
            q06.solve(current=current, resistivity=float(rho) * 1e-6, radius=float(radius), heat=float(heat), density=float(density)),
            float(exact) / pi**2,
        )
        return draw(
            6,
            figures(rate),
            f"กระแส {current} A ไหลผ่าน{_wire(metal)} รัศมี {number(radius)} cm ถ้าไม่มีการสูญเสียความร้อนออกสู่ภายนอก อุณหภูมิของลวดเพิ่มขึ้นในอัตรากี่ °C/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dT}{dt}=\frac{i^2\rho}{\pi^2r^4cD}",
            [figures(rate * pi), figures(rate * float(radius) ** 2), figures(rate / current)],
        )


@_type(7, "อัตราการเปลี่ยนอุณหภูมิของฟิวส์ที่เสียความร้อน", "การถ่ายโอนความร้อนและการเย็นตัว")
class FuseLoss(PhysicsSheet):
    def _variant(self, rng):
        metal = rng.choice(METALS)
        _, rho, heat, density = metal
        current = rng.randint(5, 20)
        radius = Fraction(rng.randint(5, 20), 100)
        alpha = Fraction(rng.randint(1, 5), 10**4)
        excess = 10 * rng.randint(1, 20)
        gain = current**2 * rho / 10**6 / (radius**4 * heat * density)
        loss = 2 * alpha * excess / (heat * radius * density)
        rate = agree(
            q07.solve(
                current=current, resistivity=float(rho) * 1e-6, radius=float(radius), heat=float(heat),
                density=float(density), alpha=float(alpha), excess=excess,
            ),
            float(gain) / pi**2 - float(loss),
        )
        show = lambda value: figures(float(gain) / pi**2 + value)  # noqa: E731
        return draw(
            7,
            figures(rate),
            f"กระแส {current} A ไหลผ่าน{_wire(metal)} รัศมี {number(radius)} cm ลวดเสียความร้อนในอัตรา α × (พื้นที่ผิวรอบลวด) × (T − Tₐ) โดย α = {number(alpha)} W/(cm²·°C) ขณะลวดร้อนกว่าห้อง {excess} °C อุณหภูมิของลวดเปลี่ยนในอัตรากี่ °C/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dT}{dt}=\frac{i^2\rho}{\pi^2r^4cD}-\frac{2\alpha(T-T_a)}{crD}",
            [show(float(loss)), show(-float(loss) / 2), show(-float(loss / radius))],
        )


@_type(8, "อุณหภูมิสุดท้ายของลวดฟิวส์", "การถ่ายโอนความร้อนและการเย็นตัว")
class FuseFinal(PhysicsSheet):
    def _variant(self, rng):
        _, rho, _, _ = rng.choice(METALS)
        current = rng.randint(2, 20)
        radius = Fraction(rng.randint(5, 20), 100)
        alpha = Fraction(rng.randint(1, 9), 10**4)
        room = rng.choice((20, 25, 30))
        excess = current**2 * rho / 10**6 / (2 * alpha * radius**3)
        final = agree(
            q08.solve(current=current, resistivity=float(rho) * 1e-6, radius=float(radius), alpha=float(alpha), room=room),
            room + float(excess) / pi**2,
        )
        return draw(
            8,
            figures(final),
            f"กระแส {current} A ไหลผ่านลวดฟิวส์รัศมี {number(radius)} cm สภาพต้านทาน {number(rho)}×10⁻⁶ Ω·cm ในห้องอุณหภูมิ {room} °C ลวดเสียความร้อนในอัตรา α × (พื้นที่ผิวรอบลวด) × (T − Tₐ) โดย α = {number(alpha)} W/(cm²·°C) อุณหภูมิสูงสุดของลวดเป็นกี่ °C (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dT}{dt}=0\Rightarrow T=T_a+\frac{i^2\rho}{2\alpha\pi^2r^3}",
            [figures(room + 2 * float(excess) / pi**2), figures(room + float(excess / radius) / pi**2), figures(room + float(excess) / pi)],
        )


@_type(9, "กระแสน้อยสุดที่ทำให้ฟิวส์ละลาย", "การถ่ายโอนความร้อนและการเย็นตัว")
class FuseMelt(PhysicsSheet):
    def _variant(self, rng):
        _, rho, _, _ = rng.choice(METALS)
        radius = Fraction(rng.randint(2, 10), 100)
        alpha = Fraction(rng.randint(1, 9), 10**4)
        rise = 10 * rng.randint(10, 60)
        square = 2 * alpha * radius**3 * rise / (rho / 10**6)
        agree(q09.solve(resistivity=float(rho) * 1e-6, radius=float(radius), alpha=float(alpha), rise=rise) ** 2, float(square) * pi**2)
        return draw(
            9,
            pi_radical(square),
            f"ลวดฟิวส์รัศมี {number(radius)} cm สภาพต้านทาน {number(rho)}×10⁻⁶ Ω·cm เสียความร้อนในอัตรา α × (พื้นที่ผิวรอบลวด) × (T − Tₐ) โดย α = {number(alpha)} W/(cm²·°C) จุดหลอมเหลวของลวดสูงกว่าอุณหภูมิห้อง {rise} °C กระแสน้อยที่สุดที่ทำให้ลวดละลายได้เป็นกี่แอมแปร์",
            r"\frac{i^2\rho}{2\alpha\pi^2r^3}>T_o-T_a",
            [pi_radical(square / 2), pi_radical(square / radius), radical(square)],
        )


UNITS = "ตอบเป็นจำนวนเท่าของ ρ/ε₀ (ระยะเป็นเมตร)"


@_type(10, "ศักย์ไฟฟ้าภายในชั้นทรงกลมบางที่มีประจุ", "การอินทิเกรตสนามและสมมาตร")
class ThinShellPotential(PhysicsSheet):
    def _variant(self, rng):
        shell = Fraction(rng.choice((2, 3, 4, 5, 6, 8, 12, 15, 20)), 10)
        thickness = Fraction(rng.randint(1, 5), 100)
        point = Fraction(rng.randint(1, int(shell * 10) - 1), 10)
        if point == 1:
            point = Fraction(1, 10)
        exact = shell * thickness
        agree(q10.solve(shell=float(shell), thickness=float(thickness), point=float(point)), exact)
        return draw(
            10,
            tex(exact),
            f"ทรงกลมตันมีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ ชั้นทรงกลมบางรัศมี ξ = {number(shell)} m หนา δξ = {number(thickness)} m ทำให้เกิดศักย์ไฟฟ้า δV ที่จุดห่างจากศูนย์กลาง r = {number(point)} m (อยู่ภายในชั้นนั้น) เท่าใด {UNITS}",
            r"\delta V=\frac{\rho\,4\pi\xi^2\delta\xi}{4\pi\varepsilon_0\xi}",
            [tex(shell**2 * thickness / point), tex(shell**2 * thickness), times_pi(4 * exact)],
        )


def _ball(rng):
    radius = Fraction(rng.randint(5, 30), 10)
    point = Fraction(rng.randint(1, int(radius * 10) - 1), 10)
    return radius, point


@_type(11, "ศักย์ไฟฟ้าจากประจุชั้นนอกของทรงกลม", "การอินทิเกรตสนามและสมมาตร")
class OuterShellsPotential(PhysicsSheet):
    def _variant(self, rng):
        while True:
            radius, point = _ball(rng)
            exact = (radius**2 - point**2) / 2
            slips = [radius**2 - point**2, radius**2 / 2, (radius**3 - point**3) / 3]
            if len({exact, *slips}) == 4:
                break
        agree(q11.solve(radius=float(radius), point=float(point)), exact)
        return draw(
            11,
            tex(exact),
            f"ทรงกลมตันรัศมี R = {number(radius)} m มีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ ศักย์ไฟฟ้า V₁ ที่ระยะ r = {number(point)} m จากศูนย์กลาง เนื่องจากประจุในช่วงรัศมี ξ = r ถึง ξ = R มีค่าเท่าใด {UNITS}",
            r"V_1=\int_r^R\frac{\rho}{\varepsilon_0}\xi\,d\xi",
            [tex(s) for s in slips],
        )


@_type(12, "ศักย์ไฟฟ้าจากประจุภายในรัศมี r", "การอินทิเกรตสนามและสมมาตร")
class InnerBallPotential(PhysicsSheet):
    def _variant(self, rng):
        point = Fraction(rng.choice((1, 2, 3, 4, 5, 6, 8, 12, 20, 25)), 10)
        exact = point**2 / 3
        agree(q12.solve(point=float(point)), exact)
        return draw(
            12,
            tex(exact),
            f"ทรงกลมตันมีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ ศักย์ไฟฟ้า V₂ ที่ระยะ r = {number(point)} m จากศูนย์กลาง เนื่องจากประจุภายในรัศมี r นั้นมีค่าเท่าใด {UNITS}",
            r"V_2=\frac{1}{4\pi\varepsilon_0}\cdot\frac{\tfrac43\pi r^3\rho}{r}",
            [tex(point**3 / 3), tex(point**2 / 2), times_pi(4 * exact)],
        )


@_type(13, "ศักย์ไฟฟ้าภายในทรงกลมประจุสม่ำเสมอ", "การอินทิเกรตสนามและสมมาตร")
class BallInsidePotential(PhysicsSheet):
    def _variant(self, rng):
        while True:
            radius, point = _ball(rng)
            exact = (3 * radius**2 - point**2) / 6
            slips = [(radius**2 - point**2) / 2, radius**2 / 3, (3 * radius**2 - 5 * point**2) / 6]
            if len({exact, *slips}) == 4:
                break
        agree(q13.solve(radius=float(radius), point=float(point)), exact)
        return draw(
            13,
            tex(exact),
            f"ทรงกลมตันรัศมี R = {number(radius)} m มีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ ศักย์ไฟฟ้ารวมที่ระยะ r = {number(point)} m จากศูนย์กลางมีค่าเท่าใด {UNITS}",
            r"V=V_1+V_2=\frac{\rho}{2\varepsilon_0}\left(R^2-\frac{r^2}{3}\right)",
            [tex(s) for s in slips],
        )


def _pair(rng):
    """R, r (Q), r0 (P) and s, with r != r0 and both inside the ball."""
    radius = Fraction(rng.randint(10, 30), 10)
    top = int(radius * 10)
    point, source = (Fraction(x, 10) for x in rng.sample(range(1, top + 1), 2))
    size = Fraction(rng.randint(2, 10), 10)
    return radius, point, source, size


PAIR = "ทรงกลมตันรัศมี R = {radius} m มีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ วางประจุจุด −q′ ที่จุด P ห่างจากศูนย์กลาง r₀ = {source} m โดย q′ เท่ากับประจุของทรงกลมรัศมี {size} m ที่มีความหนาแน่น ρ จุด Q อยู่ฝั่งตรงข้ามกับ P ห่างจากศูนย์กลาง r = {point} m"


@_type(14, "ศักย์ไฟฟ้าในทรงกลมประจุที่มีจุดประจุลบ", "ศักย์ไฟฟ้าของทรงกลมประจุร่วมจุดประจุ")
class PairPotential(PhysicsSheet):
    def _variant(self, rng):
        while True:
            radius, point, source, size = _pair(rng)
            ball = (3 * radius**2 - point**2) / 6
            exact = ball - size**3 / (3 * (source + point))
            slips = [
                ball + size**3 / (3 * (source + point)),
                ball - size**3 / (3 * abs(source - point)),
                ball - size**3 / (3 * source),
            ]
            if len({exact, *slips}) == 4:
                break
        agree(q14.solve(radius=float(radius), point=float(point), source=float(source), size=float(size)), exact)
        stem = PAIR.format(radius=number(radius), source=number(source), size=number(size), point=number(point))
        return draw(
            14,
            tex(exact),
            f"{stem} ศักย์ไฟฟ้าที่ Q มีค่าเท่าใด {UNITS}",
            r"V_Q=\frac{\rho}{2\varepsilon_0}\left(R^2-\frac{r^2}{3}\right)-\frac{q'}{4\pi\varepsilon_0(r_0+r)}",
            [tex(s) for s in slips],
        )


@_type(15, "สนามไฟฟ้าในทรงกลมประจุที่มีจุดประจุลบ", "ศักย์ไฟฟ้าของทรงกลมประจุร่วมจุดประจุ")
class PairField(PhysicsSheet):
    def _variant(self, rng):
        while True:
            radius, point, source, size = _pair(rng)
            charge = size**3 / 3
            exact = point / 3 - charge / (source + point) ** 2
            slips = [
                -exact,
                point / 3 - charge / (source + point),
                radius**3 / (3 * point**2) - charge / (source + point) ** 2,
            ]
            if exact != 0 and len({exact, *slips}) == 4:
                break
        agree(q15.solve(radius=float(radius), point=float(point), source=float(source), size=float(size)), exact)
        stem = PAIR.format(radius=number(radius), source=number(source), size=number(size), point=number(point))
        return draw(
            15,
            tex(exact),
            f"{stem} สนามไฟฟ้าที่ Q ในแนวรัศมี (ทิศออกจากศูนย์กลางเป็นบวก) มีค่าเท่าใด {UNITS}",
            r"E_r=-\frac{dV}{dr}",
            [tex(s) for s in slips],
        )


@_type(16, "ตำแหน่งสมดุลของประจุลบคู่ในทรงกลมประจุ", "ศักย์ไฟฟ้าของทรงกลมประจุร่วมจุดประจุ")
class PairEquilibrium(PhysicsSheet):
    def _variant(self, rng):
        size = rng.randint(1, 20)
        radius = size + rng.randint(1, 10)
        agree(q16.solve(size=size), size / 4 ** (1 / 3))
        root = lambda n: rf"\frac{{{size}}}{{\sqrt[3]{{{n}}}}}"  # noqa: E731
        return draw(
            16,
            root(4),
            f"ทรงกลมตันรัศมี {radius} cm มีประจุบวกกระจายสม่ำเสมอความหนาแน่น ρ ประจุจุด −q′ สองตัวอยู่ที่จุด P และ Q ซึ่งอยู่คนละฝั่งของศูนย์กลางบนเส้นผ่านศูนย์กลางเดียวกัน ห่างจากศูนย์กลางเท่ากันเป็นระยะ r₀ โดย q′ เท่ากับประจุของทรงกลมรัศมี {size} cm ที่มีความหนาแน่น ρ ประจุทั้งสองอยู่ในสมดุลเมื่อ r₀ เป็นกี่ cm",
            r"\frac{\rho r_0}{3\varepsilon_0}=\frac{q'}{4\pi\varepsilon_0(2r_0)^2}",
            [str(size), root(12), tex(Fraction(size, 2))],
        )


RATIOS = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5), Fraction(8, 15), Fraction(15, 8))
RC_PAIRS = tuple((x, n) for x in RATIOS for n in range(1, 6) if (x * 1000 / n).denominator == 1)


@_type(17, "ความต่างศักย์ยังผลคร่อมตัวเก็บประจุในวงจร RC", "วงจรตัวต้านทานและตัวเก็บประจุ")
class CapacitorRms(PhysicsSheet):
    def _variant(self, rng):
        x, micro = rng.choice(RC_PAIRS)
        resistance = x * 1000 / micro
        amplitude = rng.randint(5, 30)
        squared = amplitude**2 / (2 * (1 + x * x))
        agree(q17.solve(amplitude=amplitude, omega=1000, resistance=float(resistance), capacitance=micro * 1e-6) ** 2, squared)
        return draw(
            17,
            radical(squared),
            f"ตัวเก็บประจุ {micro} μF ต่ออนุกรมกับตัวต้านทาน {number(resistance)} Ω และแหล่งจ่ายไฟฟ้ากระแสสลับ ℰ₀ sin ωt ที่มีแอมพลิจูด ℰ₀ = {amplitude} V และ ω = 1000 rad/s ความต่างศักย์ยังผล (rms) คร่อมตัวเก็บประจุเป็นกี่โวลต์",
            r"V_C=\frac{\mathcal E_0}{\sqrt2}\cdot\frac{1}{\sqrt{1+\omega^2R^2C^2}}",
            [
                radical(amplitude**2 / (1 + x * x)),
                radical(amplitude**2 * x * x / (2 * (1 + x * x))),
                radical(amplitude**2 / (2 * (1 + x * x) ** 2)),
            ],
        )


@_type(18, "ความจุจากกราฟเส้นตรงของ 1/V² กับ R²", "วงจรตัวต้านทานและตัวเก็บประจุ")
class CapacitanceFromLine(PhysicsSheet):
    def _variant(self, rng):
        amplitude = rng.choice((5, 10, 20))
        n = rng.randint(2, 10)
        intercept = Fraction(2, amplitude**2)
        slope = intercept * n * n / 10**8
        agree(q18.solve(slope=float(slope), intercept=float(intercept)) * 1e6, n / pi)
        return draw(
            18,
            over_pi(n),
            f"วงจรตัวเก็บประจุ C ต่ออนุกรมกับตัวต้านทาน R และหม้อแปลงไฟฟ้ากระแสสลับความถี่ 50 Hz วัดความต่างศักย์ยังผล V_C คร่อมตัวเก็บประจุที่ R หลายค่า แล้วเขียนกราฟ 1/V_C² กับ R² ได้เส้นตรงที่มีความชัน {sci(slope, force=True)} V⁻²Ω⁻² และจุดตัดแกนตั้ง {number(intercept)} V⁻² ความจุ C เป็นกี่ไมโครฟารัด",
            r"\frac{1}{V_C^2}=\frac{2}{\mathcal E_0^2}+\frac{2\omega^2C^2}{\mathcal E_0^2}R^2",
            [tex(2 * n), over_pi(Fraction(n * n, 10**4)), tex(100 * n)],
        )


@_type(19, "โมเมนต์ความเฉื่อยจากคาบการแกว่งแบบสองเส้นเชือก", "การแกว่งของวัตถุแข็งเกร็ง")
class BifilarInertia(PhysicsSheet):
    def _variant(self, rng):
        while True:
            mass = 50 * rng.randint(4, 16)
            separation = rng.randint(3, 8)
            length = 5 * rng.randint(4, 12)
            period = Fraction(rng.randint(50, 200), 100)
            exact = mass * 978 * separation**2 * period**2 / (16 * length)
            slips = [4 * exact, exact / separation, exact / period]
            if len({exact, *slips}) == 4:
                break
        inertia = agree(
            q19.solve(mass=mass, separation=separation, length=length, period=float(period)),
            float(exact) / pi**2,
        )
        return draw(
            19,
            figures(inertia),
            f"ลูกบาศก์มวล {mass} g แขวนด้วยเชือกสองเส้นยาว {length} cm ที่ห่างกัน {separation} cm แล้วแกว่งบิดรอบแกนดิ่งด้วยคาบ {number(period)} s โดย T² = (16π²I/(m₀gd²))ℓ โมเมนต์ความเฉื่อยของลูกบาศก์เป็นกี่ g·cm² (g = 978 cm/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"I=\frac{m_0gd^2T^2}{16\pi^2\ell}",
            [figures(float(s) / pi**2) for s in slips],
        )


BOX = {
    ("sphere", True): "ทรงกลม เพราะโมเมนต์ความเฉื่อยทั้งสองแบบเท่ากัน",
    ("cylinder", False): "ทรงกระบอก เพราะโมเมนต์ความเฉื่อยทั้งสองแบบไม่เท่ากัน",
    ("cylinder", True): "ทรงกระบอก เพราะโมเมนต์ความเฉื่อยทั้งสองแบบเท่ากัน",
    ("sphere", False): "ทรงกลม เพราะโมเมนต์ความเฉื่อยทั้งสองแบบไม่เท่ากัน",
}


def _inertias(shape, side, density, hole):
    full = density * side**5 / 6
    if shape == "sphere":
        value = full - 8 * pi * density * hole**5 / 15
        return value, value
    first = full - pi * density * side * hole**4 / 2
    second = full - pi * density * (side**3 * hole**2 / 12 + side * hole**4 / 4)
    return first, second


@_type(20, "รูปร่างโพรงในลูกบาศก์จากโมเมนต์ความเฉื่อย", "การแกว่งของวัตถุแข็งเกร็ง")
class BlackBoxShape(ChoiceType):
    sheet_id = "tpho2546_physics"
    sheet = SHEET

    def compose(self, rng):
        shape = rng.choice(("sphere", "cylinder"))
        side = rng.choice((4, 5, 6))
        hole = rng.randint(5, 4 * side) / 10
        first, second = (round(v, 1) for v in _inertias(shape, side, 8.5, hole))
        answer = q20.solve(side=side, density=8.5, first=first, second=second)
        equal = answer == "sphere"
        other = "cylinder" if equal else "sphere"
        return (
            f"ลูกบาศก์ทองเหลืองด้านยาว {side} cm (ความหนาแน่น 8.5 g/cm³) มีโพรงตรงกลางเป็นทรงกลมรัศมี b หรือทรงกระบอกรัศมี b ยาว {side} cm ที่แกนขนานกับด้าน AB "
            f"จากคาบการแกว่งเมื่อแขวนแบบ 2.2(ก) (หมุนรอบแกนขนาน AB) และแบบ 2.2(ข) (หมุนรอบแกนตั้งฉากกับ AB) คำนวณโมเมนต์ความเฉื่อยได้ {first:.1f} g·cm² และ {second:.1f} g·cm² ตามลำดับ ข้อสรุปใดถูกต้อง",
            BOX[(answer, equal)],
            (
                named("phys.black_box_rule_reversed", BOX[(other, equal)]),
                named("phys.black_box_values_misread", BOX[(other, not equal)]),
                named("phys.black_box_radius_needed", "บอกไม่ได้จนกว่าจะรู้รัศมี b ของโพรงก่อน"),
            ),
        )


BRASS = ((Fraction(85, 10), "ทองเหลือง"), (Fraction(78, 10), "เหล็ก"), (Fraction(27, 10), "อะลูมิเนียม"))


@_type(21, "รัศมีโพรงทรงกระบอกจากโมเมนต์ความเฉื่อย", "การแกว่งของวัตถุแข็งเกร็ง")
class CylinderHoleRadius(PhysicsSheet):
    def _variant(self, rng):
        while True:
            density, name = rng.choice(BRASS)
            side = rng.choice((3, 4, 5, 6))
            hole = rng.randint(5, 5 * side - 3) / 10
            inertia = round(_inertias("cylinder", side, float(density), hole)[0], 2)
            full = float(density) * side**5 / 6
            removed = full - inertia
            answer = three_figures(q21.solve(side=side, density=float(density), inertia=inertia))
            slips = [
                three_figures((removed / (pi * float(density) * side)) ** 0.25),
                three_figures((15 * removed / (8 * pi * float(density))) ** 0.2),
                three_figures((2 * removed / (pi * float(density) * side)) ** 0.5),
            ]
            if len({answer, *slips}) == 4:
                break
        return draw(
            21,
            answer,
            f"ลูกบาศก์{name}ด้านยาว {side} cm (ความหนาแน่น {number(density)} g/cm³) มีโพรงทรงกระบอกรัศมี b ยาว {side} cm ที่แกนผ่านจุดกึ่งกลางและขนานกับด้าน AB เมื่อแกว่งรอบแกนขนาน AB วัดโมเมนต์ความเฉื่อยได้ I = {inertia:.2f} g·cm² โดย I = ρa⁵/6 − πρab⁴/2 รัศมี b เป็นกี่ cm (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"b^4=\frac{2(\rho a^5/6-I)}{\pi\rho a}",
            slips,
        )
