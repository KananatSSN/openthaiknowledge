"""Seeded variants of the reviewed TPhO 6 (2550) national physics olympiad."""

from fractions import Fraction
from math import atan2, degrees, exp, floor, log, log10, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2550_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2550_physics import q11, q12, q13, q14, q15, q16

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


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
    1: ("phys.sound_bar_ratio_inverted", "phys.sound_bar_slowness_ratio", "phys.sound_bar_speed_for_time"),
    2: ("phys.plano_convex_thickness_ignored", "phys.lensmaker_inverted", "phys.lensmaker_biconvex_used"),
    3: ("phys.lens_reflection_plane_refraction_ignored", "phys.lens_reflection_depth_multiplied", "phys.lens_reflection_mirror_focal_as_radius"),
    4: ("phys.adiabatic_piston_own_mass_ignored", "phys.adiabatic_piston_final_equilibrium", "phys.adiabatic_temperature_exponent"),
    5: ("phys.motional_emf_length_divided", "phys.motional_emf_halved", "phys.motional_emf_length_squared"),
    6: ("phys.rotating_rod_half_dropped", "phys.rotating_rod_length_not_squared", "phys.rotating_rod_angular_as_linear"),
    7: ("phys.wheel_emf_half_dropped", "phys.wheel_spokes_in_series", "phys.wheel_radius_not_squared"),
    8: ("phys.wheel_emf_half_dropped", "phys.wheel_torque_half_doubled", "phys.wheel_radius_power"),
    9: ("phys.incline_friction_on_roller", "phys.incline_friction_direction_reversed", "phys.incline_roller_weight_ignored"),
    10: ("phys.incline_friction_on_roller", "phys.incline_friction_direction_reversed", "phys.incline_roller_weight_ignored"),
    11: ("phys.cylinder_rotation_ignored", "phys.incline_friction_on_roller", "phys.cylinder_inertia_as_hoop"),
    12: ("phys.rolling_friction_half_dropped", "phys.rolling_friction_sine_used", "phys.rolling_friction_contact_inertia"),
    13: ("phys.thermistor_celsius_used", "phys.thermistor_log10_used", "phys.thermistor_sign"),
    14: ("phys.spring_pi_not_squared", "phys.spring_slope_inverted", "phys.spring_intercept_used"),
    15: ("phys.spring_mass_ratio_inverted", "phys.spring_intercept_as_mass", "phys.spring_intercept_scaled"),
    16: ("phys.beam_spring_point_mass", "phys.beam_spring_pi_not_squared", "phys.beam_spring_ratio_inverted"),
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


SHEET = "ฟิสิกส์โอลิมปิก สอวน. ครั้งที่ 6 (2550)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2550_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2550_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


SLOW_FAST = (Fraction(3, 2), Fraction(2), Fraction(3), Fraction(4))
SLOW_SLOW = (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4))


@_type(1, "อัตราส่วนความยาวแท่งโลหะจากเวลาเดินทางของเสียง", "อัตราเร็วเสียงในของแข็ง")
class SoundBars(PhysicsSheet):
    def _variant(self, rng):
        s1, s2 = rng.choice(SLOW_FAST), rng.choice(SLOW_SLOW)
        y1 = rng.choice((Fraction(1, 3), Fraction(1, 2), Fraction(1, 4), Fraction(1)))
        y2 = rng.choice((Fraction(2), Fraction(3), Fraction(4), Fraction(1)))
        rho1, rho2 = s1 * s1 * y1, s2 * s2 * y2
        exact = (1 - s2) / (s1 - 1)
        agree(q01.solve(slow1=float(s1), slow2=float(s2)), exact)
        return draw(
            1,
            tex(exact),
            f"แท่งโลหะชนิดที่ 1 ยาว L₁ ต่อกับแท่งโลหะชนิดที่ 2 ยาว L₂ วางขนานกับแท่งโลหะชนิดที่ 3 ยาว L₁ + L₂ มอดุลัสของยังของโลหะชนิดที่ 1 และ 2 เป็น {number(y1)} เท่าและ {number(y2)} เท่าของชนิดที่ 3 ความหนาแน่นเป็น {number(rho1)} เท่าและ {number(rho2)} เท่าของชนิดที่ 3 ตามลำดับ ถ้าเสียงใช้เวลาผ่านสองเส้นทางเท่ากัน L₁/L₂ เป็นเท่าใด (v = √(Y/ρ))",
            r"\frac{L_1}{v_1}+\frac{L_2}{v_2}=\frac{L_1+L_2}{v_3}",
            [tex((s1 - 1) / (1 - s2)), tex(s2 / s1), tex((1 - 1 / s2) / (1 / s1 - 1))],
        )


INDICES = (Fraction(3, 2), Fraction(8, 5), Fraction(7, 5), Fraction(4, 3))


def _lens(rng):
    index = rng.choice(INDICES)
    thickness = rng.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2)))
    span = rng.randint(6, 30)
    return index, thickness, thickness + span, (index - 1) * span


LENS = "เลนส์นูนแกมระนาบหนาตรงกลาง {t} cm ดัชนีหักเห {n} แสงขนานเข้าทางผิวระนาบแล้วโฟกัสที่ระยะ {d} cm หลังผิวระนาบ"


@_type(2, "รัศมีความโค้งของเลนส์นูนแกมระนาบจากจุดโฟกัส", "การหักเหและการสะท้อนในเลนส์หนา")
class PlanoConvexRadius(PhysicsSheet):
    def _variant(self, rng):
        index, thickness, focus, radius = _lens(rng)
        agree(q02.solve(index=float(index), thickness=float(thickness), focus=float(focus)), radius)
        return draw(
            2,
            tex(radius),
            LENS.format(t=number(thickness), n=number(index), d=number(focus)) + " รัศมีความโค้งของผิวโค้งเป็นกี่เซนติเมตร (รังสีใกล้แกน)",
            r"\frac{1}{D-t}=\frac{n-1}{R}",
            [tex((index - 1) * focus), tex((focus - thickness) / (index - 1)), tex(2 * radius)],
        )


@_type(3, "ตำแหน่งภาพจากแสงสะท้อนภายในเลนส์หนา", "การหักเหและการสะท้อนในเลนส์หนา")
class LensInnerReflection(PhysicsSheet):
    def _variant(self, rng):
        index, thickness, focus, radius = _lens(rng)
        if radius / 2 <= thickness:
            raise _Clash
        exact = (radius / 2 - thickness) / index
        agree(q03.solve(index=float(index), thickness=float(thickness), focus=float(focus)), exact)
        return draw(
            3,
            tex(exact),
            LENS.format(t=number(thickness), n=number(index), d=number(focus)) + " แสงส่วนน้อยสะท้อนจากผิวโค้งด้านในแล้วออกทางผิวระนาบไปรวมที่จุด A หน้าเลนส์ A อยู่ห่างผิวระนาบกี่เซนติเมตร (รังสีใกล้แกน)",
            r"f_{\text{mirror}}=\frac R2,\quad x=\frac{R/2-t}{n}",
            [tex(radius / 2 - thickness), tex(index * (radius / 2 - thickness)), tex((radius - thickness) / index)],
        )


@_type(4, "อัตราส่วนมวลที่อัดอากาศแบบแอเดียแบติก", "กระบวนการแอเดียแบติก")
class AdiabaticPiston(PhysicsSheet):
    def _variant(self, rng):
        k = rng.choice((1.5, 2.0, 2.5, 3.0, 4.0))
        value = q04.solve(ratio=k)
        drop = 2 * (1 - 1 / k)
        return draw(
            4,
            measure(value),
            f"ลูกสูบฉนวนมวล M ปิดอากาศในกระบอกสูบฉนวนในสุญญากาศอย่างสมดุล วางมวล M′ บนลูกสูบแล้วปล่อยทันที ลูกสูบเลื่อนลงอัดอากาศแบบแอเดียแบติก (γ = 1.4, U = (5/2)nRT) จนที่ตำแหน่งต่ำสุดอากาศเหลือปริมาตร 1/{number(Fraction(k).limit_denominator(10))} ของเดิม M′/M มีค่าเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"(M+M')gh=\tfrac52nR(T-T_0),\quad TV^{\gamma-1}=\text{const}",
            [measure(value + 1), measure(k**1.4 - 1), measure(5 * (k**1.4 - 1) / drop - 1)],
        )


def _rod(rng):
    return Fraction(rng.randint(1, 20), 10), Fraction(rng.randint(5, 50), 100)


@_type(5, "ความต่างศักย์ระหว่างปลายแท่งที่เคลื่อนที่ในสนามแม่เหล็ก", "แรงเคลื่อนไฟฟ้าเหนี่ยวนำ")
class MovingRodVoltage(PhysicsSheet):
    def _variant(self, rng):
        field, length = _rod(rng)
        speed = rng.randint(1, 20)
        exact = speed * field * length
        agree(q05.solve(speed=speed, field=float(field), length=float(length)), exact)
        return draw(
            5,
            tex(exact),
            f"แท่งตัวนำยาว {number(length)} m เคลื่อนที่ด้วยความเร็ว {speed} m/s ตั้งฉากกับตัวเองผ่านสนามแม่เหล็ก {number(field)} T ที่ตั้งฉากกับทั้งแท่งและความเร็ว ความต่างศักย์ระหว่างปลายทั้งสองเป็นกี่โวลต์",
            r"E=vB,\quad V=\int_0^\ell E\,d\ell",
            [tex(speed * field / length), tex(exact / 2), tex(exact * length)],
        )


@_type(6, "ความต่างศักย์ระหว่างปลายแท่งที่หมุนในสนามแม่เหล็ก", "แรงเคลื่อนไฟฟ้าเหนี่ยวนำ")
class SpinningRodVoltage(PhysicsSheet):
    def _variant(self, rng):
        field, length = _rod(rng)
        omega = rng.randint(2, 60)
        exact = field * omega * length**2 / 2
        agree(q06.solve(field=float(field), omega=omega, length=float(length)), exact)
        return draw(
            6,
            tex(exact),
            f"แท่งตัวนำยาว {number(length)} m หมุนรอบปลายข้างหนึ่งด้วยความเร็วเชิงมุม {omega} rad/s ในสนามแม่เหล็ก {number(field)} T ที่ตั้งฉากกับระนาบการหมุน ความต่างศักย์ระหว่างปลายทั้งสองเป็นกี่โวลต์",
            r"d\mathcal E=B\omega r\,dr",
            [tex(2 * exact), tex(field * omega * length / 2), tex(field * omega * length)],
        )


def _wheel(rng):
    field = Fraction(rng.randint(1, 20), 10)
    radius = Fraction(rng.randint(5, 40), 100)
    resistor = Fraction(rng.randint(1, 20), 2)
    return field, radius, resistor


@_type(7, "กระแสจากวงล้อตัวนำที่หมุนในสนามแม่เหล็ก", "จานฟาราเดย์และแรงหน่วงแม่เหล็ก")
class WheelCurrent(PhysicsSheet):
    def _variant(self, rng):
        field, radius, resistor = _wheel(rng)
        omega = rng.randint(5, 100)
        exact = omega * field * radius**2 / (2 * resistor)
        agree(q07.solve(omega=omega, field=float(field), radius=float(radius), resistor=float(resistor)), exact)
        return draw(
            7,
            tex(exact),
            f"วงล้อตัวนำรัศมี {number(radius)} m มีซี่ล้อตัวนำ 8 ซี่ หมุนด้วยความเร็วเชิงมุม {omega} rad/s ในสนามแม่เหล็ก {number(field)} T ตั้งฉากกับระนาบวงล้อ ตัวต้านทาน {number(resistor)} Ω ต่อระหว่างขอบวงล้อกับแกน กระแสผ่านตัวต้านทานเป็นกี่แอมแปร์ (ไม่คิดความต้านทานของวงล้อ)",
            r"V=\tfrac12\omega Br_0^2,\quad i=\frac VR",
            [tex(2 * exact), tex(8 * exact), tex(exact / radius)],
        )


@_type(8, "ความเร็วเชิงมุมสุดท้ายของวงล้อที่ถูกมวลถ่วง", "จานฟาราเดย์และแรงหน่วงแม่เหล็ก")
class WheelTerminal(PhysicsSheet):
    def _variant(self, rng):
        field, radius, resistor = _wheel(rng)
        mass = Fraction(rng.randint(1, 50), 100)
        exact = 4 * mass * 10 * resistor / (field**2 * radius**3)
        agree(q08.solve(mass=float(mass), field=float(field), radius=float(radius), resistor=float(resistor)), exact)
        return draw(
            8,
            tex(exact),
            f"วงล้อตัวนำรัศมี {number(radius)} m อยู่ในสนามแม่เหล็ก {number(field)} T ตั้งฉากกับระนาบวงล้อ ตัวต้านทาน {number(resistor)} Ω ต่อระหว่างขอบวงล้อกับแกน แขวนมวล {number(mass)} kg ที่เชือกพันรอบขอบวงล้อ ในที่สุดวงล้อหมุนด้วยความเร็วเชิงมุมคงที่กี่ rad/s (g = 10 m/s², ไม่คิดแรงเสียดทาน)",
            r"Mgr_0\omega_f=i^2R,\quad i=\frac{\omega_fBr_0^2}{2R}",
            [tex(exact / 2), tex(exact / 4), tex(exact * radius)],
        )


SLOPE = {37: (Fraction(3, 5), Fraction(4, 5)), 53: (Fraction(4, 5), Fraction(3, 5))}


def _incline(rng):
    angle = rng.choice((37, 53))
    sin_, cos_ = SLOPE[angle]
    roller, block = rng.randint(1, 8), rng.randint(1, 8)
    friction = Fraction(rng.randint(1, 6), 10)
    return angle, sin_, cos_, roller, block, friction


def _exact_angle(angle):
    return degrees(atan2(*((3, 4) if angle == 37 else (4, 3))))


ROLLER = "ทรงกระบอกตันมวล {m1} kg (แกนหมุนลื่น) ผูกเชือกกับกล่องมวล {m2} kg บนพื้นเอียงที่ sin θ = {s} (กล่องอยู่สูงกว่า) สัมประสิทธิ์ความเสียดทานสถิตระหว่างพื้นกับกล่อง {mu}"


@_type(9, "แรงดึงน้อยสุดที่ตรึงทรงกระบอกและกล่องบนพื้นเอียง", "แรงเสียดทานสถิตและจลน์บนพื้นเอียง")
class InclineLeastPull(PhysicsSheet):
    def _variant(self, rng):
        angle, s, c, m1, m2, mu = _incline(rng)
        exact = (m1 + m2) * 10 * s - mu * m2 * 10 * c
        if exact <= 0:
            raise _Clash
        agree(q09.solve(roller=m1, block=m2, angle=_exact_angle(angle), friction=float(mu)), exact)
        return draw(
            9,
            tex(exact),
            ROLLER.format(m1=m1, m2=m2, s=number(s), mu=number(mu)) + " แรงดึงกล่องขนานพื้นเอียงขึ้นไปน้อยที่สุดกี่นิวตันจึงทำให้ระบบไม่เคลื่อนที่ (g = 10 m/s²)",
            r"F+f_2=(m_1+m_2)g\sin\theta,\quad f_2\le\mu_sm_2g\cos\theta",
            [tex((m1 + m2) * 10 * (s - mu * c)), tex((m1 + m2) * 10 * s + mu * m2 * 10 * c), tex(m2 * 10 * s - mu * m2 * 10 * c)],
        )


@_type(10, "แรงดึงมากสุดที่ตรึงทรงกระบอกและกล่องบนพื้นเอียง", "แรงเสียดทานสถิตและจลน์บนพื้นเอียง")
class InclineGreatestPull(PhysicsSheet):
    def _variant(self, rng):
        angle, s, c, m1, m2, mu = _incline(rng)
        exact = (m1 + m2) * 10 * s + mu * m2 * 10 * c
        low = (m1 + m2) * 10 * s - mu * m2 * 10 * c
        if low <= 0:
            raise _Clash
        agree(q10.solve(roller=m1, block=m2, angle=_exact_angle(angle), friction=float(mu)), exact)
        return draw(
            10,
            tex(exact),
            ROLLER.format(m1=m1, m2=m2, s=number(s), mu=number(mu)) + " แรงดึงกล่องขนานพื้นเอียงขึ้นไปมากที่สุดกี่นิวตันที่ระบบยังไม่เคลื่อนที่ (g = 10 m/s²)",
            r"F=(m_1+m_2)g\sin\theta+f_2,\quad f_2\le\mu_sm_2g\cos\theta",
            [tex((m1 + m2) * 10 * (s + mu * c)), tex(low), tex(m2 * 10 * s + mu * m2 * 10 * c)],
        )


def _hauled(rng):
    angle, s, c, m1, m2, _ = _incline(rng)
    kinetic = Fraction(rng.randint(1, 4), 10)
    hanging = rng.randint(2, 20)
    drive = hanging - (m1 + m2) * s - kinetic * m2 * c
    if drive <= 0:
        raise _Clash
    return angle, s, c, m1, m2, kinetic, hanging, drive


HAUL = "ทรงกระบอกตันมวล {m1} kg (I = mr²/2, แกนหมุนลื่น) ผูกเชือกกับกล่องมวล {m2} kg บนพื้นเอียงที่ sin θ = {s} กล่องผูกเชือกผ่านรอกเบาที่ยอดพื้นเอียงไปยังมวล {m3} kg ที่แขวนอยู่ ระบบเคลื่อนขึ้นโดยทรงกระบอกกลิ้งไม่ไถล และสัมประสิทธิ์ความเสียดทานจลน์ระหว่างกล่องกับพื้น {mu}"


@_type(11, "ความเร่งของทรงกระบอกกลิ้งและกล่องที่ถูกดึงขึ้นพื้นเอียง", "สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง")
class HauledAcceleration(PhysicsSheet):
    def _variant(self, rng):
        angle, s, c, m1, m2, kinetic, m3, drive = _hauled(rng)
        exact = 10 * drive / (Fraction(3, 2) * m1 + m2 + m3)
        agree(q11.solve(roller=m1, block=m2, hanging=m3, angle=_exact_angle(angle), kinetic=float(kinetic)), exact)
        return draw(
            11,
            tex(exact),
            HAUL.format(m1=m1, m2=m2, s=number(s), m3=m3, mu=number(kinetic)) + " ความเร่งของระบบเป็นกี่ m/s² (g = 10 m/s²)",
            r"\left(m_1+m_2+m_3+\frac{I}{r^2}\right)a=g\left[m_3-(m_1+m_2)\sin\theta-\mu_km_2\cos\theta\right]",
            [
                tex(10 * drive / (m1 + m2 + m3)),
                tex(10 * (drive - kinetic * m1 * c) / (Fraction(3, 2) * m1 + m2 + m3)),
                tex(10 * drive / (2 * m1 + m2 + m3)),
            ],
        )


@_type(12, "สัมประสิทธิ์ความเสียดทานสถิตที่ทรงกระบอกกลิ้งไม่ไถล", "สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง")
class HauledRollingFriction(PhysicsSheet):
    def _variant(self, rng):
        angle, s, c, m1, m2, kinetic, m3, drive = _hauled(rng)
        a = 10 * drive / (Fraction(3, 2) * m1 + m2 + m3)
        exact = a / (2 * 10 * c)
        agree(q12.solve(roller=m1, block=m2, hanging=m3, angle=_exact_angle(angle), kinetic=float(kinetic)), exact)
        return draw(
            12,
            tex(exact),
            HAUL.format(m1=m1, m2=m2, s=number(s), m3=m3, mu=number(kinetic)) + " สัมประสิทธิ์ความเสียดทานสถิตระหว่างทรงกระบอกกับพื้นต้องมีค่าอย่างน้อยเท่าใด (g = 10 m/s²)",
            r"f_1=\frac{I}{r^2}a\le\mu_sm_1g\cos\theta",
            [tex(a / (10 * c)), tex(a / (2 * 10 * s)), tex(a / (3 * 10 * c))],
        )


@_type(13, "ค่าคงตัว B ของเทอร์มิสเตอร์", "เทอร์มิสเตอร์และการวัดอุณหภูมิ")
class ThermistorB(PhysicsSheet):
    def _variant(self, rng):
        cold = rng.choice((5, 10, 15, 20))
        warm = cold + 10 * rng.randint(2, 5)
        b_true = rng.randint(30, 45) * 100
        r_cold = rng.randint(100, 400) / 10
        r_warm = round(r_cold * exp(b_true * (1 / (warm + 273.15) - 1 / (cold + 273.15))), 2)
        b = q13.solve(cold=cold, warm=warm, r_cold=r_cold, r_warm=r_warm)
        ratio = log(r_cold / r_warm)
        return draw(
            13,
            measure(b),
            f"เทอร์มิสเตอร์ชนิด NTC มีความต้านทาน {r_cold} kΩ ที่ {cold} °C และ {r_warm:.2f} kΩ ที่ {warm} °C ถ้า R = R₀ exp[B(1/T − 1/T₀)] ค่า B เป็นกี่เคลวิน (T(K) = T(°C) + 273.15, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\ln\frac{R_1}{R_2}=B\left(\frac1{T_1}-\frac1{T_2}\right)",
            [measure(ratio / (1 / cold - 1 / warm)), measure(log10(r_cold / r_warm) / (1 / (cold + 273.15) - 1 / (warm + 273.15))), measure(-b)],
        )


@_type(14, "ค่าคงตัวสปริงจากกราฟ T² กับมวล", "การสั่นของมวลติดสปริง")
class SpringConstantLine(PhysicsSheet):
    def _variant(self, rng):
        slope = rng.randint(10, 200) / 100
        intercept = rng.randint(1, 10) / 100
        k = q14.solve(slope=slope, intercept=intercept)
        return draw(
            14,
            measure(k),
            f"แขวนมวล M ต่าง ๆ กับสปริงแล้ววัดคาบการสั่นขึ้นลง เขียนกราฟ T² กับ M ได้เส้นตรงความชัน {slope} s²/kg และจุดตัดแกน T² ที่ {intercept} s² ค่าคงตัวสปริงเป็นกี่ N/m (T = 2π√((M + m_s)/k), ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T^2=\frac{4\pi^2}{k}M+\frac{4\pi^2}{k}m_s",
            [measure(2 * pi / slope), measure(4 * pi**2 * slope), measure(4 * pi**2 / intercept)],
        )


@_type(15, "มวลยังผลของสปริงจากกราฟ T² กับมวล", "การสั่นของมวลติดสปริง")
class SpringEffectiveMass(PhysicsSheet):
    def _variant(self, rng):
        slope = rng.randint(10, 200) / 100
        intercept = rng.randint(1, 10) / 100
        mass = q15.solve(slope=slope, intercept=intercept)
        return draw(
            15,
            measure(mass),
            f"แขวนมวล M ต่าง ๆ กับสปริงแล้ววัดคาบการสั่นขึ้นลง เขียนกราฟ T² กับ M ได้เส้นตรงความชัน {slope} s²/kg และจุดตัดแกน T² ที่ {intercept} s² มวลยังผลของสปริง m_s เป็นกี่กิโลกรัม (T = 2π√((M + m_s)/k), ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T^2=\frac{4\pi^2}{k}(M+m_s)",
            [measure(slope / intercept), measure(intercept), measure(intercept / (4 * pi**2))],
        )


@_type(16, "มวลของคานที่แขวนกับสปริงจากคาบการสั่น", "การแกว่งของวัตถุแข็งเกร็ง")
class BeamOnSpring(PhysicsSheet):
    def _variant(self, rng):
        spring = rng.randint(10, 80)
        period = rng.randint(20, 120) / 100
        mass = q16.solve(spring=spring, period=period)
        return draw(
            16,
            measure(mass),
            f"คานสม่ำเสมอวางแนวระดับ ปลาย A เป็นจุดหมุน ปลาย B แขวนกับสปริงค่าคงตัว {spring} N/m เมื่อปลาย B สั่นขึ้นลงเล็กน้อยมีคาบ {period} s คานมีมวลกี่กิโลกรัม (I = ML²/3, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac13ML^2\ddot\theta=-kL^2\theta,\quad T=2\pi\sqrt{\frac{M}{3k}}",
            [measure(mass / 3), measure(mass * pi), measure(mass / 9)],
        )
