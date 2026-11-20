"""Seeded variants of the reviewed TPhO 7 (2551) national physics olympiad."""

from fractions import Fraction
from math import acos, asin, degrees, floor, isqrt, log10, pi, radians, sin, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2551_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2551_physics import q11, q12, q13, q14, q15
from otk.sheets.tpho2551_physics._wedge import lagrange as _wedge_lagrange

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
    1: ("phys.mirror_lens_new_distance_given", "phys.mirror_lens_index_scaling", "phys.mirror_lens_single_refraction"),
    2: ("phys.drop_reflection_turn_halved", "phys.drop_deviation_supplement", "phys.drop_refraction_turn_once"),
    3: ("phys.rainbow_second_order_formula", "phys.rainbow_sine_cosine_swapped", "phys.rainbow_factor_wrong"),
    4: ("phys.attraction_sign_reversed", "phys.energy_factor_two_dropped", "phys.speed_not_rooted"),
    5: ("phys.inside_work_outside_formula", "phys.work_sign_reversed", "phys.inside_work_radius_power"),
    6: ("phys.centre_speed_sign", "phys.centre_speed_work_doubled", "phys.centre_speed_work_halved"),
    7: ("phys.shm_quarter_period_assumed", "phys.uniform_speed_assumed", "phys.uniform_speed_assumed_max"),
    8: ("phys.pulley_inertia_ignored", "phys.pulley_inertia_as_hoop", "phys.incline_cosine_used"),
    9: ("phys.pulley_inertia_as_hoop", "phys.tension_static_weight", "phys.tension_equals_block_force"),
    10: ("phys.wedge_normal_unreduced", "phys.wedge_total_mass", "phys.wedge_light"),
    11: ("phys.wedge_fixed_assumed", "phys.wedge_relative_mass_dropped", "phys.wedge_relative_denominator_unreduced"),
    12: ("phys.string_ignored", "phys.pulley_inertia_as_hoop", "phys.wedge_total_mass"),
    13: ("phys.wedge_normal_static", "phys.string_ignored", "phys.wedge_pseudo_force_sign"),
    14: ("phys.boyle_gravity_dropped", "phys.boyle_ratio_inverted", "phys.boyle_intercept_dropped"),
    15: ("phys.potentiometer_ratio_inverted", "phys.potentiometer_ratio_ignored", "phys.potentiometer_divider_used"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 7 (2551)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2551_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2551_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


LIQUIDS = (Fraction(4, 3), Fraction(3, 2), Fraction(5, 4), Fraction(6, 5), Fraction(8, 5))


@_type(1, "ระยะเลื่อนสลิตเมื่อเติมของเหลวในกระจกเลนส์", "กระจกเว้าและเลนส์ของเหลว")
class LiquidMirrorLens(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(10, 40)
        n = rng.choice(LIQUIDS)
        exact = radius - radius / (2 * n - 1)
        agree(q01.solve(radius=radius, index=float(n)), exact)
        return draw(
            1,
            tex(exact),
            f"แผ่นแก้วโค้งบางมากสองแผ่นเหมือนกัน A และ B (B เคลือบเงินด้านหลัง) ประกบกัน เมื่อมีอากาศอยู่ระหว่างแผ่น ภาพของสลิตที่อยู่ห่าง {radius} cm ตกกลับมาที่สลิตเองพอดี ถ้าเติมของเหลวดัชนีหักเห {number(n)} ระหว่างแผ่น ต้องเลื่อนสลิตเข้าหาแผ่นแก้วกี่เซนติเมตรจึงได้ภาพชัดที่สลิตอีกครั้ง (รังสีใกล้แกน)",
            r"L'=\frac{R}{2n-1}",
            [tex(radius / (2 * n - 1)), tex(radius - radius / n), tex(radius - 2 * radius / (3 * n - 1))],
        )


DROPS = (Fraction(4, 3), Fraction(3, 2), Fraction(133, 100), Fraction(5, 4))


@_type(2, "มุมเบี่ยงเบนของแสงที่สะท้อนภายในหยดน้ำหนึ่งครั้ง", "การหักเหในหยดน้ำและรุ้ง")
class DropDeviation(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(DROPS)
        phi = rng.choice((30, 40, 45, 50, 60, 70))
        delta = q02.solve(index=float(n), incidence=phi)
        alpha = degrees(asin(sin(radians(phi)) / float(n)))
        return draw(
            2,
            measure(delta),
            f"แสงตกกระทบหยดของเหลวทรงกลมดัชนีหักเห {number(n)} ด้วยมุมตกกระทบ {phi}° หักเหเข้า สะท้อนภายในหนึ่งครั้ง แล้วหักเหออก มุมเบี่ยงเบน δ = π − 4α + 2φ ของรังสีเป็นกี่องศา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\sin\phi=n\sin\alpha,\quad\delta=\pi-4\alpha+2\phi",
            [measure(180 - 2 * alpha + 2 * phi), measure(4 * alpha - 2 * phi), measure(180 - 4 * alpha + phi)],
        )


@_type(3, "มุมตกกระทบที่ให้มุมเบี่ยงเบนน้อยที่สุดในหยดน้ำ", "การหักเหในหยดน้ำและรุ้ง")
class RainbowAngle(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(DROPS)
        phi = q03.solve(index=float(n))
        x = float(n) ** 2 - 1
        return draw(
            3,
            measure(phi),
            f"แสงหักเหเข้าหยดของเหลวทรงกลมดัชนีหักเห {number(n)} สะท้อนภายในหนึ่งครั้งแล้วหักเหออก มุมตกกระทบเท่าใด (องศา) ทำให้มุมเบี่ยงเบนน้อยที่สุด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{d\delta}{d\phi}=0\Rightarrow n\cos\alpha=2\cos\phi",
            [measure(degrees(acos(sqrt(x / 8)))), measure(degrees(asin(sqrt(x / 3)))), measure(degrees(acos(sqrt(x / 2))))],
        )


def _ball(rng):
    radius = Fraction(rng.randint(2, 10), 10)
    start = radius * rng.randint(2, 6)
    strength = rng.randint(1, 20)  # K = kqQ/m in m^3/s^2
    speed = rng.randint(1, 10)
    return radius, start, strength, speed


BALL = "อนุภาคมวล m ประจุ −q ถูกยิงด้วยความเร็วต้น {speed} m/s ตรงเข้าหาจุดศูนย์กลางของฉนวนทรงกลมรัศมี {radius} m ที่มีประจุ +Q กระจายสม่ำเสมอทั่วปริมาตร ผ่านรูเล็ก ๆ ตามแนวเส้นผ่านศูนย์กลาง เริ่มห่างจากศูนย์กลาง {start} m โดย kqQ/m = {strength} m³/s²"


@_type(4, "อัตราเร็วของประจุลบที่ทะลุทรงกลมประจุบวก", "การเคลื่อนที่ของประจุผ่านทรงกลมประจุ")
class ChargeExitSpeed(PhysicsSheet):
    def _variant(self, rng):
        radius, start, strength, speed = _ball(rng)
        gain = 2 * strength * (1 / radius - 1 / start)
        exact = speed**2 + gain
        agree(q04.solve(speed=speed, strength=strength, radius=float(radius), start=float(start)) ** 2, exact)
        if speed**2 - gain <= 0:
            raise _Clash
        return draw(
            4,
            radical(exact),
            BALL.format(speed=speed, radius=number(radius), start=number(start), strength=strength) + " เมื่อถึงผิวด้านหลังของทรงกลม (จุด B) อนุภาคมีอัตราเร็วกี่ m/s",
            r"\tfrac12mv_i^2-\frac{kqQ}{a}=\tfrac12mv_B^2-\frac{kqQ}{R}",
            [radical(speed**2 - gain), radical(speed**2 + gain / 2), tex(exact)],
        )


@_type(5, "งานของแรงไฟฟ้าภายในทรงกลมประจุ", "การเคลื่อนที่ของประจุผ่านทรงกลมประจุ")
class InsideWork(PhysicsSheet):
    def _variant(self, rng):
        product = Fraction(rng.randint(1, 40), 10)
        radius = Fraction(rng.randint(1, 20), 10)
        exact = -product / (2 * radius)
        agree(q05.solve(product=float(product), radius=float(radius)), exact)
        return draw(
            5,
            tex(exact),
            f"ฉนวนทรงกลมรัศมี {number(radius)} m มีประจุ +Q กระจายสม่ำเสมอทั่วปริมาตร ประจุ −q เคลื่อนที่ภายในตามรูแนวเส้นผ่านศูนย์กลางจากจุดศูนย์กลาง O ไปถึงผิว B งานของแรงไฟฟ้าที่ Q กระทำต่อ −q เป็นกี่จูล (kqQ = {number(product)} J·m)",
            r"F=-\frac{kqQ}{R^3}x,\quad W=\int_0^RF\,dx",
            [tex(-product / radius), tex(-exact), tex(-product / (2 * radius**2))],
        )


@_type(6, "อัตราเร็วของประจุที่จุดศูนย์กลางทรงกลมประจุ", "การเคลื่อนที่ของประจุผ่านทรงกลมประจุ")
class CentreSpeed(PhysicsSheet):
    def _variant(self, rng):
        radius, _, strength, speed = _ball(rng)
        exact = speed**2 + strength / radius
        agree(q06.solve(speed=speed, strength=strength, radius=float(radius)) ** 2, exact)
        if speed**2 - strength / radius <= 0:
            raise _Clash
        return draw(
            6,
            radical(exact),
            f"ประจุ −q มวล m เคลื่อนที่ตามรูแนวเส้นผ่านศูนย์กลางของฉนวนทรงกลมรัศมี {number(radius)} m ที่มีประจุ +Q สม่ำเสมอ (kqQ/m = {strength} m³/s²) ไปออกที่ผิว B ด้วยอัตราเร็ว {speed} m/s ขณะผ่านจุดศูนย์กลาง O มันมีอัตราเร็วกี่ m/s",
            r"W_{O\to B}=-\frac{kqQ}{2R}=\tfrac12mv_B^2-\tfrac12mv_O^2",
            [radical(speed**2 - strength / radius), radical(speed**2 + 2 * strength / radius), radical(speed**2 + strength / (2 * radius))],
        )


@_type(7, "เวลาที่ประจุเคลื่อนจากศูนย์กลางถึงผิวทรงกลมประจุ", "การเคลื่อนที่ของประจุผ่านทรงกลมประจุ")
class CentreToSurfaceTime(PhysicsSheet):
    def _variant(self, rng):
        radius, _, strength, speed = _ball(rng)
        t = q07.solve(speed=speed, strength=strength, radius=float(radius))
        r = float(radius)
        v_o = sqrt(speed**2 + strength / r)
        return draw(
            7,
            measure(t),
            f"ประจุ −q มวล m เคลื่อนที่ตามรูแนวเส้นผ่านศูนย์กลางของฉนวนทรงกลมรัศมี {number(radius)} m ที่มีประจุ +Q สม่ำเสมอ (kqQ/m = {strength} m³/s²) จากจุดศูนย์กลาง O ไปออกที่ผิว B ด้วยอัตราเร็ว {speed} m/s ใช้เวลาจาก O ถึง B กี่วินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\omega=\sqrt{\frac{kqQ}{mR^3}},\quad v_B=v_O\cos\omega t",
            [measure(pi / 2 * sqrt(r**3 / strength)), measure(r / speed), measure(r / v_o)],
        )


def _masses(rng):
    wedge = rng.randint(4, 20)
    block = rng.randint(1, 10)
    pulley = rng.randint(1, 6)
    sine = rng.choice((0.6, 0.8))
    return wedge, block, pulley, sine


WEDGE = "ลิ่ม A มวล {a} kg มีรอก C (จานกลม มวล {c} kg, I = MR²/2) ติดที่ยอด เชือกเบาพันรอบรอกโดยปลายผูกกับกล่อง B มวล {b} kg บนผิวเอียงของลิ่มที่ sin θ = {s} ไม่มีแรงเสียดทานที่ผิวทุกแห่ง (g = 9.80 m/s²)"


def _wedge_stem(a, b, c, s):
    return WEDGE.format(a=a, b=b, c=c, s=s)


@_type(8, "ความเร่งของกล่องบนลิ่มที่ยึดไว้เมื่อเชือกหมุนรอก", "แรงตึงเชือกและรอกที่มีมวล")
class HeldWedgeAcceleration(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        a = q08.solve(block=block, pulley=pulley, sine=sine)
        cos_ = sqrt(1 - sine * sine)
        return draw(
            8,
            measure(a),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าจับลิ่มไว้นิ่ง ปล่อยให้กล่องไถลลงขณะเชือกดึงรอกหมุน กล่องมีความเร่งกี่ m/s² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m_Bg\sin\theta-T=m_Ba,\quad TR=\tfrac12m_CR^2\frac aR",
            [measure(9.8 * sine), measure(block * 9.8 * sine / (block + pulley)), measure(block * 9.8 * cos_ / (block + pulley / 2))],
        )


@_type(9, "แรงตึงเชือกที่หมุนรอกบนลิ่มที่ยึดไว้", "แรงตึงเชือกและรอกที่มีมวล")
class HeldWedgeTension(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        tension = q09.solve(block=block, pulley=pulley, sine=sine)
        a = tension / (pulley / 2)
        return draw(
            9,
            measure(tension),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าจับลิ่มไว้นิ่ง ปล่อยให้กล่องไถลลงขณะเชือกดึงรอกหมุน แรงตึงเชือกเป็นกี่นิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T=\tfrac12m_Ca,\quad a=\frac{m_Bg\sin\theta}{m_B+m_C/2}",
            [
                measure(pulley * block * 9.8 * sine / (block + pulley)),
                measure(block * 9.8 * sine),
                measure(block * a),
            ],
        )


@_type(10, "ความเร่งของลิ่มเมื่อเชือกขาด", "โมเมนตัมแนวระดับของลิ่มและมวล")
class CutWedgeAcceleration(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        a = q10.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        c, big = sqrt(1 - sine * sine), wedge + pulley
        return draw(
            10,
            measure(a),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าเชือกขาดและปล่อยให้ลิ่มเคลื่อนที่ได้บนพื้นลื่น ลิ่ม (พร้อมรอก) มีความเร่งกี่ m/s² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a_A=\frac{mg\sin\theta\cos\theta}{M+m\sin^2\theta}",
            [measure(block * 9.8 * sine * c / big), measure(block * 9.8 * sine * c / (big + block)), measure(9.8 * sine * c)],
        )


@_type(11, "ความเร่งของกล่องเทียบกับลิ่มเมื่อเชือกขาด", "โมเมนตัมแนวระดับของลิ่มและมวล")
class CutRelativeAcceleration(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        a = q11.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        big = wedge + pulley
        return draw(
            11,
            measure(a),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าเชือกขาดและปล่อยให้ลิ่มเคลื่อนที่ได้บนพื้นลื่น ผู้สังเกตบนลิ่มวัดความเร่งของกล่องได้กี่ m/s² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a_{B/A}=\frac{(M+m)g\sin\theta}{M+m\sin^2\theta}",
            [measure(9.8 * sine), measure(big * 9.8 * sine / (big + block * sine * sine)), measure((big + block) * 9.8 * sine / big)],
        )


@_type(12, "ความเร่งของลิ่มเมื่อเชือกดึงรอกหมุน", "โมเมนตัมแนวระดับของลิ่มและมวล")
class IntactWedgeAcceleration(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        a = q12.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        cut = q10.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        hoop = _wedge_lagrange(wedge + pulley, block, float(pulley), sine, 9.8)[0]
        c = sqrt(1 - sine * sine)
        return draw(
            12,
            measure(a),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าปล่อยให้ลิ่มเคลื่อนที่ได้บนพื้นลื่นโดยเชือกไม่ขาด (เชือกดึงรอกหมุนโดยไม่ไถล) ลิ่มมีความเร่งกี่ m/s² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac12M\dot X^2+\tfrac12m\left[(\dot X-\dot s\cos\theta)^2+(\dot s\sin\theta)^2\right]+\tfrac12\frac{I}{R^2}\dot s^2",
            [measure(cut), measure(hoop), measure(block * 9.8 * sine * c / (wedge + pulley + block))],
        )


@_type(13, "แรงที่กล่องกระทำต่อลิ่มเมื่อเชือกดึงรอกหมุน", "โมเมนตัมแนวระดับของลิ่มและมวล")
class IntactNormalForce(PhysicsSheet):
    def _variant(self, rng):
        wedge, block, pulley, sine = _masses(rng)
        normal = q13.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        c = sqrt(1 - sine * sine)
        cut = q10.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        a = q12.solve(wedge=wedge, block=block, pulley=pulley, sine=sine)
        return draw(
            13,
            measure(normal),
            _wedge_stem(wedge, block, pulley, sine) + " ถ้าปล่อยให้ลิ่มเคลื่อนที่ได้บนพื้นลื่นโดยเชือกไม่ขาด (เชือกดึงรอกหมุนโดยไม่ไถล) แรงที่กล่องกดตั้งฉากบนผิวลิ่มเป็นกี่นิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m g\cos\theta-N=m a_A\sin\theta",
            [measure(block * 9.8 * c), measure(block * (9.8 * c - cut * sine)), measure(block * (9.8 * c + a * sine))],
        )


@_type(14, "ความดันบรรยากาศจากกราฟของลำอากาศในสายยาง", "กฎของบอยล์กับความดันของของเหลว")
class HoseAtmosphere(PhysicsSheet):
    def _variant(self, rng):
        intercept = rng.randint(100, 400) / 100  # 1/L0 in 1/m
        pressure = rng.randint(950, 1050) * 100
        slope = -round(9800 * intercept / pressure, 4)
        value = q14.solve(slope=slope, intercept=intercept)
        return draw(
            14,
            measure(value / 1000),
            f"ลำอากาศปิดในสายยางสูง h เหนือระดับน้ำในถัง (P = P_atm − ρgh) ความยาวลำอากาศ L เปลี่ยนตาม h เขียนกราฟ 1/L กับ h ได้เส้นตรงความชัน {slope} m⁻² และจุดตัดแกน 1/L ที่ {intercept} m⁻¹ ความดันบรรยากาศเป็นกี่กิโลพาสคัล (ρ = 1000 kg/m³, g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac1L=\frac1{L_0}-\frac{\rho g}{P_{atm}L_0}h",
            [measure(intercept / abs(slope)), measure(9.8 * abs(slope) / intercept), measure(9.8 / abs(slope))],
        )


CELL = Fraction(33, 20)


@_type(15, "แรงเคลื่อนไฟฟ้าจากโพเทนชิออมิเตอร์", "โพเทนชิออมิเตอร์")
class Potentiometer(PhysicsSheet):
    def _variant(self, rng):
        standard = 10 * rng.randint(30, 110)
        unknown = 10 * rng.randint(20, 120)
        exact = CELL * unknown / standard
        agree(q15.solve(unknown=unknown, standard=standard), exact)
        return draw(
            15,
            tex(exact),
            f"โพเทนชิออมิเตอร์ปรับให้แกลแวนอมิเตอร์ไม่มีกระแสเมื่อต่อเซลล์มาตรฐาน 1.65 V คร่อมความต้านทาน {standard} Ω และเมื่อเปลี่ยนเป็นเซลล์ที่ไม่ทราบค่า (กระแสวงจรล่างเท่าเดิม) สมดุลที่ {unknown} Ω แรงเคลื่อนไฟฟ้าของเซลล์นั้นเป็นกี่โวลต์",
            r"E_x=\frac{R_x}{R_s}E_s",
            [tex(CELL * standard / unknown), tex(CELL), tex(CELL * unknown / (standard + unknown))],
        )
