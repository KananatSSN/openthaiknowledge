"""Seeded variants of the reviewed TPhO 9 (2553) national physics olympiad."""

from fractions import Fraction
from math import acos, asin, atan, cos, degrees, floor, isqrt, log10, pi, radians, sin, sqrt, tan

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2553_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2553_physics import q11, q12, q13, q14

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
    1: ("phys.elastic_masses_swapped", "phys.bounce_heavy_ball_speed_given", "phys.elastic_velocities_exchanged"),
    2: ("phys.wall_return_halfway", "phys.wall_meeting_ratio_of_speeds", "phys.wall_meeting_sign"),
    3: ("phys.wall_distance_geometric", "phys.wall_recurrence_index_shift", "phys.wall_return_halfway"),
    4: ("phys.closest_approach_not_rooted", "phys.closest_approach_energy_halved", "phys.closest_approach_halved"),
    5: ("phys.piston_small_area_ignored", "phys.piston_area_sum", "phys.piston_atmosphere_dropped"),
    6: ("phys.piston_weight_dropped", "phys.piston_area_single", "phys.piston_area_sum"),
    7: ("phys.adiabatic_as_isothermal", "phys.piston_area_not_squared", "phys.helium_gamma_diatomic"),
    8: ("phys.adiabatic_as_isothermal", "phys.helium_gamma_diatomic", "phys.piston_pressure_without_weight"),
    10: ("phys.double_star_half_angle", "phys.double_star_single_spacing", "phys.double_star_spacing_sum"),
    11: ("phys.double_star_half_fringe_dropped", "phys.double_star_alpha_doubled", "phys.double_star_next_disappearance"),
    12: ("phys.brewster_as_critical", "phys.brewster_inverted", "phys.brewster_cosine"),
    13: ("phys.index_tangent_inverted", "phys.index_from_sine", "phys.index_from_cosine"),
    14: ("phys.seiche_pendulum_model", "phys.seiche_board_model", "phys.seiche_factor_twelve_dropped"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 9 (2553)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2553_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2553_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


def _pair(rng):
    big = rng.randint(2, 12)
    small = rng.randint(1, big - 1)
    return big, small


WALL = "มวล {M} kg ไถลบนพื้นลื่นด้วยอัตราเร็ว {V} m/s เข้าชนมวล {m} kg ที่หยุดนิ่งห่างผนัง {l} m จากนั้นมวลเบาไถลชนผนังและกลับมาชนมวลหนักไป-มา การชนทั้งหมดยืดหยุ่น"


@_type(1, "อัตราเร็วมวลเบาหลังถูกมวลหนักชน", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class WallFirstSpeed(PhysicsSheet):
    def _variant(self, rng):
        big, small = _pair(rng)
        speed = rng.randint(1, 10)
        exact = Fraction(2 * big * speed, big + small)
        agree(q01.solve(big=big, small=small, speed=speed), exact)
        return draw(
            1,
            tex(exact),
            WALL.format(M=big, V=speed, m=small, l="ระยะหนึ่ง").replace("ห่างผนัง ระยะหนึ่ง m", "ห่างผนังระยะหนึ่ง") + f" หลังการชนครั้งแรก มวล {small} kg มีอัตราเร็วกี่ m/s",
            r"MV_0=MV_1+mv_1,\quad V_0=v_1-V_1",
            [tex(Fraction(2 * small * speed, big + small)), tex(Fraction((big - small) * speed, big + small)), str(speed)],
        )


@_type(2, "ตำแหน่งการชนครั้งที่สองของมวลระหว่างผนัง", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class WallSecondMeeting(PhysicsSheet):
    def _variant(self, rng):
        big, small = _pair(rng)
        gap = Fraction(rng.randint(2, 30), 10)
        speed = rng.randint(1, 10)
        exact = gap * Fraction(big + small, 3 * big - small)
        agree(q02.solve(big=big, small=small, gap=float(gap)), exact)
        return draw(
            2,
            tex(exact),
            WALL.format(M=big, V=speed, m=small, l=number(gap)) + " การชนครั้งที่สองเกิดห่างผนังกี่เมตร",
            r"V_1t_1+v_1t_1=2\ell_0,\quad \ell_1=\ell_0-V_1t_1",
            [tex(gap / 2), tex(gap * Fraction(big - small, 2 * big)), tex(gap * Fraction(big + small, 3 * big + small))],
        )


def _after(big, small, speed, n):
    V, v = Fraction(speed), Fraction(0)
    for _ in range(n):
        V, v = ((big - small) * V + 2 * small * v) / (big + small), ((small - big) * v + 2 * big * V) / (big + small)
        v = -v
    return V, -v


@_type(3, "ตำแหน่งการชนครั้งที่สามจากความสัมพันธ์เวียนเกิด", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class WallThirdMeeting(PhysicsSheet):
    def _variant(self, rng):
        big, small = _pair(rng)
        gap = Fraction(rng.randint(2, 30), 10)
        speed = rng.randint(1, 10)
        V2, v2 = _after(big, small, speed, 2)
        exact = gap * speed / (v2 + V2)
        first = gap * Fraction(big + small, 3 * big - small)
        agree(q03.solve(big=big, small=small, speed=speed, gap=float(gap)), exact)
        return draw(
            3,
            tex(exact),
            WALL.format(M=big, V=speed, m=small, l=number(gap)) + " การชนครั้งที่สามเกิดห่างผนังกี่เมตร",
            r"\ell_n(v_n+V_n)=\ell_0V_0",
            [tex(first * first / gap), tex(first), tex(first / 2)],
        )


SQUARES = (100, 400, 900, 2500, 10000, 40000)


@_type(4, "ระยะใกล้ผนังที่สุดของมวลหนัก", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class WallClosestApproach(PhysicsSheet):
    def _variant(self, rng):
        ratio = rng.choice(SQUARES)
        gap = Fraction(rng.randint(5, 50), 10)
        root = isqrt(ratio)
        exact = gap / root
        agree(q04.solve(ratio=ratio, gap=float(gap)), exact)
        return draw(
            4,
            tex(exact),
            f"มวล M ไถลบนพื้นลื่นเข้าชนมวล m = M/{ratio} ที่หยุดนิ่งห่างผนัง {number(gap)} m แล้วมวลเบาไถลชนผนังและกลับมาชนมวลหนักไป-มาแบบยืดหยุ่นหลายครั้ง มวลหนักเข้าใกล้ผนังที่สุดประมาณกี่เมตร",
            r"\ell_n(v_n+V_n)=\ell_0V_0,\quad \tfrac12mv^2=\tfrac12MV_0^2",
            [tex(gap / ratio), radical(2 * gap * gap / ratio), tex(exact / 2)],
        )


def _piston(rng):
    outside = rng.choice((1.0e5, 1.013e5))
    mass = rng.randint(2, 40)
    big = rng.randint(20, 80)        # cm^2
    small = rng.randint(5, big - 5)  # cm^2
    return outside, mass, big, small


PISTON = "กระบอกสูบลื่นตั้งในแนวดิ่ง ลูกสูบใหญ่พื้นที่ {A} cm² อยู่ด้านบน ลูกสูบเล็กพื้นที่ {a} cm² อยู่ด้านล่าง เชื่อมด้วยก้านแข็ง มวลรวม {M} kg ระหว่างลูกสูบมีแก๊สฮีเลียม 1 โมล อากาศภายนอกมีความดัน {P} Pa (g = 9.8 m/s²)"


def _piston_stem(outside, mass, big, small):
    return PISTON.format(A=big, a=small, M=mass, P=measure(outside).replace(r"\times10^{5}", "×10⁵"))


@_type(5, "ความดันแก๊สระหว่างลูกสูบคู่ในภาวะสมดุล", "กฎแก๊สอุดมคติกับแรงดัน")
class PistonPressure(PhysicsSheet):
    def _variant(self, rng):
        outside, mass, big, small = _piston(rng)
        p = q05.solve(outside=outside, mass=mass, big=big * 1e-4, small=small * 1e-4)
        w = mass * 9.8
        return draw(
            5,
            measure(p),
            _piston_stem(outside, mass, big, small) + " ความดันของแก๊สในภาวะสมดุลเป็นกี่พาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"(P_0-P_a)(A-a)=Mg",
            [measure(outside + w / (big * 1e-4)), measure(outside + w / ((big + small) * 1e-4)), measure(w / ((big - small) * 1e-4))],
        )


@_type(6, "ระยะเลื่อนของลูกสูบคู่เมื่อแก๊สร้อนขึ้น", "กฎแก๊สอุดมคติกับแรงดัน")
class PistonWarming(PhysicsSheet):
    def _variant(self, rng):
        outside, mass, big, small = _piston(rng)
        warming = rng.randint(5, 60)
        s = q06.solve(outside=outside, mass=mass, big=big * 1e-4, small=small * 1e-4, warming=warming)
        area, w = (big - small) * 1e-4, mass * 9.8
        p0 = outside + w / area
        return draw(
            6,
            measure(s * 100),
            _piston_stem(outside, mass, big, small) + f" กระบอกสูบนำความร้อนได้ ทำให้อุณหภูมิเพิ่มขึ้นช้า ๆ {warming} K ลูกสูบเลื่อนขึ้นกี่เซนติเมตร (R = 8.31 J/mol·K, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_0\Delta V=R\Delta T,\quad S=\frac{\Delta V}{A-a}",
            [
                measure(8.31 * warming / (outside * area) * 100),
                measure(8.31 * warming / (p0 * big * 1e-4) * 100),
                measure(8.31 * warming / (outside * (big + small) * 1e-4 + w) * 100),
            ],
        )


@_type(7, "แรงคืนตัวของลูกสูบคู่ในกระบอกสูบฉนวน", "กระบวนการแอเดียแบติก")
class PistonRestoringForce(PhysicsSheet):
    def _variant(self, rng):
        outside, mass, big, small = _piston(rng)
        volume = rng.randint(5, 40) / 10     # litres
        shift = rng.randint(1, 10)           # mm
        area = (big - small) * 1e-4
        p0 = outside + mass * 9.8 / area
        f = q07.solve(pressure=p0, volume=volume * 1e-3, big=big * 1e-4, small=small * 1e-4, shift=shift * 1e-3)
        return draw(
            7,
            measure(f),
            _piston_stem(outside, mass, big, small) + f" ปริมาตรแก๊ส {volume:g} ลิตร กระบอกสูบเป็นฉนวน กดลูกสูบลงจากสมดุล {shift} mm แรงลัพธ์ที่กระทำต่อลูกสูบทั้งคู่มีขนาดกี่นิวตัน (γ = 5/3, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P=P_0\left(\frac{V_0}{V_0-y(A-a)}\right)^\gamma\approx P_0\left(1+\frac{\gamma y(A-a)}{V_0}\right)",
            [measure(f * 3 / 5), measure(f / area), measure(f * 21 / 25)],
        )


@_type(8, "คาบการสั่นของลูกสูบคู่บนแก๊สฮีเลียม", "กระบวนการแอเดียแบติก")
class PistonPeriod(PhysicsSheet):
    def _variant(self, rng):
        outside, mass, big, small = _piston(rng)
        volume = rng.randint(5, 40) / 10
        t = q08.solve(outside=outside, mass=mass, big=big * 1e-4, small=small * 1e-4, volume=volume * 1e-3)
        area = (big - small) * 1e-4
        bare = 2 * pi * sqrt(3 * mass * volume * 1e-3 / (5 * outside * area**2))
        return draw(
            8,
            measure(t),
            _piston_stem(outside, mass, big, small) + f" ปริมาตรแก๊ส {volume:g} ลิตร กระบอกสูบเป็นฉนวน กดลูกสูบเล็กน้อยแล้วปล่อย ลูกสูบสั่นด้วยคาบกี่วินาที (γ = 5/3, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T=2\pi\sqrt{\frac{MV_0}{\gamma P_0(A-a)^2}}",
            [measure(t * sqrt(5 / 3)), measure(t * sqrt(5 / 3 / 1.4)), measure(bare)],
        )


ROWS = {k: {name: q09.solve(position=k, quantity=name) for name in ("Vb", "Vd", "q", "Q")} for k in range(2, 7)}
STEADY = {"Vb": 2.0, "Vd": 2.0, "q": 1.0, "Q": 2.0}
WHEN = {3: "T/2", 4: "3T/4", 5: "T", 6: "5T/4"}


def _times(value, unit):
    """value x unit as text: 0, unit, or a fraction such as 5/4 unit."""
    value = Fraction(value).limit_denominator(8)
    if value == 0:
        return "0"
    if value == 1:
        return unit
    shown = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return f"{shown} {unit}"


def _row(values):
    return (
        f"V_b = {_times(values['Vb'], 'V₀')}, V_d = {_times(values['Vd'], 'V₀')}, "
        f"q = {_times(values['q'], 'CV₀')}, Q = {_times(values['Q'], 'CV₀')}"
    )


@_type(9, "ค่าในตารางของวงจรทวีแรงดัน", "วงจรไดโอดและตัวเก็บประจุ")
class VoltageDoubler(ChoiceType):
    sheet_id = "tpho2553_physics"
    sheet = SHEET

    def compose(self, rng):
        k = rng.choice((3, 4, 5, 6))
        neighbour = k + 1 if k < 6 else k - 2
        return (
            f"วงจรทวีแรงดัน: ตัวเก็บประจุ C ต่อจากจุด a ไปจุด b ไดโอด D₁ จาก b ไป d ตัวเก็บประจุ C จาก d ลงกราวด์ และไดโอด D₂ จากกราวด์ไป b เริ่มต้นไม่มีประจุ สัญญาณที่จุด a เป็น V₀ sin(2πt/T) (q คือประจุบนแผ่นด้าน b ของตัวเก็บประจุตัวแรก Q คือประจุบนแผ่นด้าน d ของตัวที่สอง) ที่เวลา t = {WHEN[k]} ค่าต่าง ๆ เป็นเท่าใด",
            _row(ROWS[k]),
            (
                named("phys.doubler_previous_row", _row(ROWS[k - 1])),
                named("phys.doubler_neighbour_row", _row(ROWS[neighbour])),
                named("phys.doubler_steady_state", _row(STEADY)),
            ),
        )


ARCSEC = 206264.806


@_type(10, "ระยะห่างเชิงมุมของดาวคู่จากการหายของริ้วแทรกสอด", "การแทรกสอดของสลิตคู่")
class DoubleStarSeparation(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.randint(45, 65) * 10
        first = rng.randint(2, 40)
        second = first + rng.randint(5, 80)
        angle = q10.solve(wavelength=wavelength, first=first, second=second)
        return draw(
            10,
            measure(angle),
            f"ดาวคู่ที่สว่างใกล้เคียงกันส่งแสงผ่านตัวกรองความยาวคลื่น {wavelength} nm ไปยังสลิตคู่ เมื่อเพิ่มระยะห่างสลิตถึง {first} mm ริ้วการแทรกสอดหายไป และหายอีกครั้งเมื่อห่าง {second} mm ระยะห่างเชิงมุมระหว่างดาวทั้งสองเป็นกี่พิลิปดา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2d\sin\alpha=\left(n+\tfrac12\right)\lambda,\quad 2\alpha\approx\frac{\lambda}{d_1-d_0}",
            [
                measure(angle / 2),
                measure(wavelength * 1e-9 / (second * 1e-3) * ARCSEC),
                measure(wavelength * 1e-9 / ((second + first) * 1e-3) * ARCSEC),
            ],
        )


@_type(11, "ระยะห่างสลิตที่ริ้วแทรกสอดของดาวคู่หายครั้งแรก", "การแทรกสอดของสลิตคู่")
class DoubleStarFirstVanish(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.randint(45, 65) * 10
        separation = rng.randint(5, 100) / 10
        d0 = q11.solve(wavelength=wavelength, separation=separation)
        return draw(
            11,
            measure(d0),
            f"ดาวคู่ที่สว่างใกล้เคียงกันอยู่ห่างกันเชิงมุม {separation:g} พิลิปดา ส่งแสงผ่านตัวกรองความยาวคลื่น {wavelength} nm ไปยังสลิตคู่ ค่อย ๆ เพิ่มระยะห่างสลิตจากศูนย์ ริ้วการแทรกสอดหายไปครั้งแรกเมื่อสลิตห่างกันกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2d_0\sin\alpha=\tfrac12\lambda",
            [measure(2 * d0), measure(d0 / 2), measure(3 * d0)],
        )


INDICES = (1.33, 1.3325, 1.36, 1.40, 1.45, 1.50)


@_type(12, "มุมบริวสเตอร์ของการสะท้อนจากของเหลว", "แสงโพลาไรซ์จากการสะท้อน")
class BrewsterAngle(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(INDICES)
        theta = q12.solve(index=n)
        return draw(
            12,
            measure(theta),
            f"แสงจากอากาศ (n = 1.00) สะท้อนจากผิวของเหลวดัชนีหักเห {n} มุมตกกระทบเท่าใด (องศา) ที่ทำให้แสงสะท้อนเป็นแสงโพลาไรซ์ (มุมบริวสเตอร์) (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\theta_B+\theta_t=90^\circ\Rightarrow\tan\theta_B=n",
            [measure(degrees(asin(1 / n))), measure(degrees(atan(1 / n))), measure(degrees(acos(1 / n)))],
        )


@_type(13, "ดัชนีหักเหจากมุมบริวสเตอร์", "แสงโพลาไรซ์จากการสะท้อน")
class IndexFromBrewster(PhysicsSheet):
    def _variant(self, rng):
        angle = rng.randint(530, 600) / 10
        n = q13.solve(angle=angle)
        t = radians(angle)
        return draw(
            13,
            measure(n),
            f"ส่องแสงเลเซอร์โพลาไรซ์ขนานกับระนาบตกกระทบลงบนผิวน้ำเชื่อม พบว่าแสงสะท้อนน้อยที่สุดที่มุมตกกระทบ {angle:g}° ดัชนีหักเหของน้ำเชื่อมเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tan\theta_B=n",
            [measure(1 / tan(t)), measure(1 / sin(t)), measure(1 / cos(t))],
        )


@_type(14, "คาบการกระเพื่อมของน้ำในอ่างตามแบบจำลอง", "การกระเพื่อมของน้ำในอ่าง")
class SeichePeriod(PhysicsSheet):
    def _variant(self, rng):
        length = rng.randint(30, 60)
        depth = rng.randint(2, 10)
        t = q14.solve(length=length, depth=depth)
        L, H = length / 100, depth / 100
        return draw(
            14,
            measure(t),
            f"น้ำลึก {depth} cm ในอ่างยาว {length} cm กระเพื่อมขึ้นลงคล้ายกระดานกระดก ตามแบบจำลองของนักเรียนคนที่ 3 ซึ่งคิดว่าผลต่างความดันที่ผนังทำให้ศูนย์กลางมวลของน้ำเคลื่อนที่ซ้ายขวา คาบการกระเพื่อมเป็นกี่วินาที (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T=2\pi\sqrt{\frac{L^2}{12gH}}",
            [
                measure(2 * pi * sqrt(H / (2 * 9.8))),
                measure(2 * pi * sqrt(2 * (H * H / 3 + L * L / 12) / (9.8 * H))),
                measure(2 * pi * L / sqrt(9.8 * H)),
            ],
        )
