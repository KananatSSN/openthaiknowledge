"""Seeded variants of the reviewed TPhO 10 (2554) national physics olympiad."""

from fractions import Fraction
from math import acos, asin, cos, degrees, floor, log10, pi, radians, sin, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sheets.tpho2554_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2554_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20
from otk.sheets.tpho2554_physics._spin import beta_fixed

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


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
    1: ("phys.flux_radius_not_squared", "phys.flux_total_field_used", "phys.flux_area_without_pi"),
    2: ("phys.radial_field_radius_dropped", "phys.ring_force_single_pi", "phys.ring_circumference_as_pi_r"),
    3: ("phys.equilibrium_as_lowest_point", "phys.weight_as_mass", "phys.ring_force_single_pi"),
    4: ("phys.frequency_for_angular_frequency", "phys.period_for_angular_frequency", "phys.ring_omega_not_rooted"),
    5: ("phys.equilibrium_as_lowest_point", "phys.flux_area_without_pi", "phys.flux_radius_not_squared"),
    6: ("phys.com_same_side", "phys.half_length_dropped", "phys.com_masses_swapped"),
    7: ("phys.upper_tension_lower_mass_dropped", "phys.tension_cos_multiplied", "phys.tension_wrong_angle"),
    8: ("phys.com_masses_swapped", "phys.mass_ratio_inverted", "phys.angle_relation_signs_swapped"),
    9: ("phys.mass_ratio_inverted", "phys.small_angle_not_rooted", "phys.com_masses_swapped"),
    10: ("phys.com_masses_swapped", "phys.sliding_cos_alpha_dropped", "phys.cos_as_sin"),
    11: ("phys.length_ratio_inverted", "phys.com_masses_swapped", "phys.ratio_mass_term_dropped"),
    12: ("phys.radius_as_diameter_halved", "phys.jet_speed_not_squared", "phys.continuity_radius_not_rooted"),
    13: ("phys.laplace_sphere_for_cylinder", "phys.laplace_diameter_for_radius", "phys.laplace_bubble"),
    14: ("phys.binomial_power_dropped", "phys.laplace_sphere_for_cylinder", "phys.laplace_diameter_for_radius"),
    15: ("phys.distance_power_of_ten", "phys.initial_speed_dropped", "phys.free_fall_half_dropped"),
    16: ("phys.sphere_area_halved", "phys.drop_volume_rayleigh_length", "phys.drop_area_rayleigh_length"),
    17: ("phys.diode_threshold_averaged", "phys.diode_boxes_counted", "phys.diode_branch_boxes_counted"),
    18: ("phys.current_not_from_reference_resistor", "phys.resistance_from_single_point", "phys.reference_resistor_included"),
    19: ("phys.clip_mass_dropped", "phys.friction_slope_inverted", "phys.weight_on_one_axis"),
    20: ("phys.friction_ratio_inverted", "phys.static_coefficient_dropped", "phys.ratio_as_coefficient"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 10 (2554)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2554_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2554_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


RING_TOPIC = "ตัวนำยวดยิ่งลอยในสนามแม่เหล็ก"
SPIN_TOPIC = "การหมุนของมวลสองก้อนบนเชือก"
JET_TOPIC = "ลำน้ำและแรงตึงผิว"
DIODE_TOPIC = "กล่องดำไดโอด"
FRICTION_TOPIC = "สัมประสิทธิ์ความเสียดทานสถิตและจลน์"

INDUCTANCE = 1.3e-8
RING = (
    "วงแหวนตัวนำยวดยิ่งมวล {m} mg รัศมี {R} cm ความเหนี่ยวนำ 1.3×10⁻⁸ H ถูกปล่อยจากจุด A ซึ่งไม่มีกระแส "
    "เหนือก้อนแม่เหล็กที่มีสนาม B_z = B₀(1 + αz) และ B_r = B₀βr (z วัดจาก A ลงเป็นบวก r วัดจากแกน) "
    "โดย B₀ = {B} T, α = {a} m⁻¹, β = {b} m⁻¹ (g = 9.8 m/s²)"
)


def _ring(rng):
    mass = rng.randint(2, 10) * 10            # mg
    radius = rng.choice((0.30, 0.40, 0.50, 0.60))   # cm
    field = rng.choice((0.008, 0.010, 0.012, 0.015, 0.020))
    alpha = rng.choice((1.0, 1.5, 2.0, 2.5, 3.0))
    beta = rng.choice((16, 20, 24, 32, 40))
    return mass, radius, field, alpha, beta


def _ring_stem(mass, radius, field, alpha, beta):
    return RING.format(m=mass, R=f"{radius:.2f}", B=f"{field:g}", a=f"{alpha:g}", b=beta)


@_type(1, "กระแสในวงแหวนตัวนำยวดยิ่งที่ตกลงมา", RING_TOPIC)
class RingCurrent(PhysicsSheet):
    def _variant(self, rng):
        mass, radius, field, alpha, beta = _ring(rng)
        depth = rng.randint(2, 15)                # cm
        R, z = radius / 100, depth / 100
        i = q01.solve(B0=field, alpha=alpha, radius=R, inductance=INDUCTANCE, depth=z)
        return draw(
            1,
            measure(i),
            _ring_stem(mass, radius, field, alpha, beta) + f" เมื่อวงแหวนตกลงมาได้ {depth} cm มีกระแสไหลในวงแหวนขนาดกี่แอมแปร์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\pi R^2B_z+LI=\pi R^2B_0",
            [
                measure(i / R),
                measure(pi * R * R * field * (1 + alpha * z) / INDUCTANCE),
                measure(i / pi),
            ],
        )


@_type(2, "ค่าคงที่ของแรงคืนตัวบนวงแหวนตัวนำยวดยิ่ง", RING_TOPIC)
class RingStiffness(PhysicsSheet):
    def _variant(self, rng):
        mass, radius, field, alpha, beta = _ring(rng)
        R = radius / 100
        k = q02.solve(B0=field, alpha=alpha, beta=beta, radius=R, inductance=INDUCTANCE) * 1000
        return draw(
            2,
            measure(k),
            _ring_stem(mass, radius, field, alpha, beta) + " แรงลัพธ์บนวงแหวนเขียนได้เป็น mg − kz ค่า k เป็นกี่มิลลินิวตันต่อเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=|I|\,2\pi R\,B_r,\quad B_r=B_0\beta R",
            [measure(k / R), measure(k / pi), measure(k / 2)],
        )


@_type(3, "ตำแหน่งสมดุลของวงแหวนตัวนำยวดยิ่ง", RING_TOPIC)
class RingEquilibrium(PhysicsSheet):
    def _variant(self, rng):
        mass, radius, field, alpha, beta = _ring(rng)
        z0 = q03.solve(mass=mass * 1e-6, B0=field, alpha=alpha, beta=beta, radius=radius / 100, inductance=INDUCTANCE) * 100
        if not 0.5 <= z0 <= 60:
            raise _Clash
        return draw(
            3,
            measure(z0),
            _ring_stem(mass, radius, field, alpha, beta) + " วงแหวนอยู่ในสมดุล (แรงลัพธ์เป็นศูนย์) ที่ระยะกี่เซนติเมตรใต้จุด A (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mg=kz_0,\quad k=\frac{2B_0^2\alpha\beta\pi^2R^4}{L}",
            [measure(2 * z0), measure(z0 / 9.8), measure(z0 * pi)],
        )


@_type(4, "ความถี่เชิงมุมของการสั่นของวงแหวนตัวนำยวดยิ่ง", RING_TOPIC)
class RingOmega(PhysicsSheet):
    def _variant(self, rng):
        mass, radius, field, alpha, beta = _ring(rng)
        w = q04.solve(mass=mass * 1e-6, B0=field, alpha=alpha, beta=beta, radius=radius / 100, inductance=INDUCTANCE)
        return draw(
            4,
            measure(w),
            _ring_stem(mass, radius, field, alpha, beta) + " วงแหวนสั่นแบบฮาร์มอนิกอย่างง่ายรอบจุดสมดุลด้วยความถี่เชิงมุมกี่เรเดียนต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m\ddot s+ks=0,\quad \omega=\sqrt{k/m}",
            [measure(w / (2 * pi)), measure(2 * pi / w), measure(w * w)],
        )


@_type(5, "กระแสสูงสุดในวงแหวนตัวนำยวดยิ่ง", RING_TOPIC)
class RingPeakCurrent(PhysicsSheet):
    def _variant(self, rng):
        mass, radius, field, alpha, beta = _ring(rng)
        R = radius / 100
        i = q05.solve(mass=mass * 1e-6, B0=field, beta=beta, radius=R)
        return draw(
            5,
            measure(i),
            _ring_stem(mass, radius, field, alpha, beta) + " ขณะสั่น กระแสในวงแหวนมีค่าสูงสุดกี่แอมแปร์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"|I|=\frac{\pi R^2\alpha B_0z}{L}\text{ สูงสุดที่ }z=2z_0",
            [measure(i / 2), measure(i * pi), measure(i * R)],
        )


SPIN = (
    "เชือกเบายาว {L} m ปลายบนยึดอยู่กับที่ ปลายล่างผูกมวล m₁ = {m1} kg และมีมวล m₂ = {m2} kg ผูกที่จุดกึ่งกลางเชือก "
    "ทั้งสองหมุนเป็นวงกลมรอบแกนดิ่งที่ผ่านจุดยึดด้วยอัตราเร็วเชิงมุมคงที่ เชือกส่วนบนทำมุม α = {a}° "
    "และเชือกส่วนล่างทำมุม β = {b}° กับแนวดิ่ง โดย m₁ อยู่คนละด้านของแกนกับ m₂"
)


def _spin(rng):
    while True:
        m1, m2 = rng.randint(1, 6), rng.randint(1, 6)
        alpha = rng.randint(10, 40)
        if m1 != m2 and m1 / (m1 + m2) > sin(radians(alpha)) + 0.05:
            beta = round(degrees(beta_fixed(radians(alpha), m1, m2)), 1)
            return m1, m2, alpha, beta


@_type(6, "ศูนย์กลางมวลของมวลสองก้อนที่หมุนบนเชือก", SPIN_TOPIC)
class SpinCentre(PhysicsSheet):
    def _variant(self, rng):
        m1, m2, alpha, beta = _spin(rng)
        length = rng.randint(5, 20) / 10
        x = q06.solve(m1=m1, m2=m2, length=length, alpha=alpha, beta=beta) * 100
        half = length / 2 * 100
        sa, sb = sin(radians(alpha)), sin(radians(beta))
        return draw(
            6,
            measure(x),
            SPIN.format(L=f"{length:g}", m1=m1, m2=m2, a=alpha, b=f"{beta:g}") + " ศูนย์กลางมวลของมวลทั้งสองอยู่ห่างจากแกนหมุนกี่เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"x=\frac{L}{2}\sin\alpha-\frac{m_1}{m_1+m_2}\frac{L}{2}\sin\beta",
            [
                measure(half * sa + m1 / (m1 + m2) * half * sb),
                measure(2 * x),
                measure(half * sa - m2 / (m1 + m2) * half * sb),
            ],
        )


@_type(7, "แรงตึงเชือกส่วนบนของมวลสองก้อนที่หมุน", SPIN_TOPIC)
class SpinUpperTension(PhysicsSheet):
    def _variant(self, rng):
        m1, m2, alpha, beta = _spin(rng)
        t = q07.solve(m1=m1, m2=m2, alpha=alpha, beta=beta)
        return draw(
            7,
            measure(t),
            SPIN.format(L="1", m1=m1, m2=m2, a=alpha, b=f"{beta:g}") + " แรงตึงในเชือกส่วนบนเป็นกี่นิวตัน (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T_1\cos\beta=m_1g,\quad T_2\cos\alpha=m_2g+T_1\cos\beta",
            [
                measure(m2 * 9.8 / cos(radians(alpha))),
                measure((m1 + m2) * 9.8 * cos(radians(alpha))),
                measure((m1 + m2) * 9.8 / cos(radians(beta))),
            ],
        )


def _ratio(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _constants(a, c, d):
    return f"A = {_ratio(a)}, B = 1, C = {'−1' if c < 0 else '1'}, D = {'−1' if d < 0 else '1'}"


@_type(8, "ค่าคงที่ในความสัมพันธ์ของมุมเชือกสองส่วน", SPIN_TOPIC)
class SpinConstants(ChoiceType):
    sheet_id = "tpho2554_physics"
    sheet = SHEET

    def compose(self, rng):
        while True:
            m1, m2 = rng.randint(1, 9), rng.randint(1, 9)
            if m1 != m2:
                break
        a, b, c, d = q08.solve(m1=m1, m2=m2)
        share = Fraction(m1, m1 + m2)
        assert abs(float(share) - a) < 1e-12 and (b, c, d) == (1.0, -1.0, 1.0)
        return (
            f"เชือกเบายาว L ปลายบนยึดอยู่กับที่ ปลายล่างผูกมวล m₁ = {m1} kg มีมวล m₂ = {m2} kg ผูกที่จุดกึ่งกลาง ทั้งสองหมุนรอบแกนดิ่งด้วยอัตราเร็วเชิงมุมคงที่ "
            "เชือกส่วนบนทำมุม α และส่วนล่างทำมุม β กับแนวดิ่ง (m₁ อยู่คนละด้านของแกนกับ m₂) "
            "ความสัมพันธ์ของมุมเขียนได้เป็น A sin²β/cos β = B sin α tan β + C tan α sin β + D tan α sin α ค่าคงที่เป็นเท่าใด",
            _constants(share, c, d),
            (
                named("phys.com_masses_swapped", _constants(1 - share, c, d)),
                named("phys.mass_ratio_inverted", _constants(1 / share, c, d)),
                named("phys.angle_relation_signs_swapped", _constants(share, -c, -d)),
            ),
        )


SMALL = (
    "เชือกเบาปลายบนยึดอยู่กับที่ ปลายล่างผูกมวล m₁ = {m1} kg มีมวล m₂ = {m2} kg ผูกที่จุดกึ่งกลาง ทั้งสองหมุนรอบแกนดิ่งด้วยอัตราเร็วเชิงมุมคงที่ "
    "โดยเชือกเอียงเพียงเล็กน้อย (tan θ ≈ sin θ ≈ θ) ถ้าเชือกส่วนบนทำมุม {a}° กับแนวดิ่ง เชือกส่วนล่างทำมุมประมาณกี่องศากับแนวดิ่ง (m₁ อยู่คนละด้านของแกนกับ m₂) (ตอบเลขนัยสำคัญ 3 ตัว)"
)


@_type(9, "มุมเชือกส่วนล่างเมื่อมุมเล็ก", SPIN_TOPIC)
class SpinSmallAngle(PhysicsSheet):
    def _variant(self, rng):
        m1, m2 = rng.randint(1, 9), rng.randint(1, 9)
        if m1 == m2:
            raise _Clash
        alpha = rng.randint(4, 12) / 2
        b = q09.solve(m1=m1, m2=m2, alpha=alpha)
        return draw(
            9,
            measure(b),
            SMALL.format(m1=m1, m2=m2, a=f"{alpha:g}"),
            r"\frac{m_1}{m_1+m_2}\beta^2=\alpha^2",
            [
                measure(alpha * sqrt(m1 / (m1 + m2))),
                measure(alpha * (m1 + m2) / m1),
                measure(alpha * sqrt((m1 + m2) / m2)),
            ],
        )


SLIDE = (
    "เชือกเบาปลายบนยึดอยู่กับที่ ปลายล่างผูกมวล m₁ = {m1} kg และร้อยผ่านมวล m₂ = {m2} kg ซึ่งไถลบนเชือกได้อย่างอิสระ "
    "ทั้งสองหมุนรอบแกนดิ่งด้วยอัตราเร็วเชิงมุมคงที่ (m₁ อยู่คนละด้านของแกนกับ m₂) เชือกส่วนบนทำมุม {a}° กับแนวดิ่ง"
)


def _slide(rng):
    m1, m2 = rng.randint(1, 9), rng.randint(1, 9)
    if m1 == m2:
        raise _Clash
    return m1, m2, rng.randint(10, 50)


@_type(10, "มุมเชือกส่วนล่างเมื่อมวลกลางไถลได้", SPIN_TOPIC)
class SlideAngle(PhysicsSheet):
    def _variant(self, rng):
        m1, m2, alpha = _slide(rng)
        b = q10.solve(m1=m1, m2=m2, alpha=alpha)
        c = cos(radians(alpha))
        return draw(
            10,
            measure(b),
            SLIDE.format(m1=m1, m2=m2, a=alpha) + " เชือกส่วนล่างทำมุมกี่องศากับแนวดิ่ง (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T\cos\beta=m_1g,\quad T\cos\alpha=(m_1+m_2)g",
            [
                measure(degrees(acos(m2 * c / (m1 + m2)))),
                measure(degrees(acos(m1 / (m1 + m2)))),
                measure(degrees(asin(m1 * c / (m1 + m2)))),
            ],
        )


@_type(11, "อัตราส่วนความยาวเชือกเมื่อมวลกลางไถลได้", SPIN_TOPIC)
class SlideLengths(PhysicsSheet):
    def _variant(self, rng):
        m1, m2, alpha = _slide(rng)
        ratio = q11.solve(m1=m1, m2=m2, alpha=alpha)
        b = radians(q10.solve(m1=m1, m2=m2, alpha=alpha))
        return draw(
            11,
            measure(ratio),
            SLIDE.format(m1=m1, m2=m2, a=alpha) + " อัตราส่วนความยาวเชือกส่วนบนต่อส่วนล่าง L₂/L₁ เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T(\sin\alpha+\sin\beta)=m_2\omega^2L_2\sin\alpha,\quad T\sin\beta=m_1\omega^2(L_1\sin\beta-L_2\sin\alpha)",
            [
                measure(1 / ratio),
                measure(q11.solve(m1=m2, m2=m1, alpha=alpha)),
                measure(sin(b) / sin(radians(alpha))),
            ],
        )


JET = "น้ำไหลออกจากปลายท่อรัศมี {R0} cm ลงในแนวดิ่งด้วยความเร็ว {v0} m/s (ρ = 1000 kg/m³, g = 9.8 m/s²)"


def _jet(rng):
    return rng.choice((0.30, 0.40, 0.50, 0.60, 0.80)), rng.choice((0.05, 0.08, 0.10, 0.15, 0.20))


@_type(12, "รัศมีลำน้ำที่ตกลงมาตามสมการแบร์นูลลี", JET_TOPIC)
class JetRadius(PhysicsSheet):
    def _variant(self, rng):
        radius0, speed0 = _jet(rng)
        height = rng.randint(2, 20)                 # cm
        h = height / 100
        r = q12.solve(radius0=radius0, speed0=speed0, height=h)
        base = 1 + 2 * 9.8 * h / speed0**2
        return draw(
            12,
            measure(r),
            JET.format(R0=f"{radius0:.2f}", v0=f"{speed0:g}") + f" ถ้าไม่คิดความหนืดและแรงตึงผิว ที่ระยะ {height} cm ใต้ปลายท่อ ลำน้ำมีรัศมีกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"v=\sqrt{v_0^2+2gh},\quad \pi R_0^2v_0=\pi R^2v",
            [
                measure(r / 2),
                measure(radius0 * 10 * (1 + 2 * 9.8 * h / speed0) ** -0.25),
                measure(radius0 * 10 * base**-0.5),
            ],
        )


@_type(13, "ความดันส่วนเกินในลำน้ำจากแรงตึงผิว", JET_TOPIC)
class JetPressure(PhysicsSheet):
    def _variant(self, rng):
        tension = rng.choice((0.072, 0.065, 0.050, 0.030))
        radius = rng.randint(4, 30) / 10            # mm
        p = q13.solve(tension=tension, radius=radius)
        return draw(
            13,
            measure(p),
            f"ลำน้ำทรงกระบอกรัศมี {radius:g} mm มีความตึงผิว {tension:g} N/m และอยู่ในสมดุล ความดันภายในลำน้ำมากกว่าความดันอากาศภายนอกกี่พาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P\,2Rh=P_0\,2Rh+2\gamma h",
            [measure(2 * p), measure(p / 2), measure(4 * p)],
        )


def _correction(radius0, speed0, height, tension, factor=4.0):
    R0 = radius0 * 1e-2
    R1 = R0 * (1 + 2 * 9.8 * height / speed0**2) ** -0.25
    k = 2 * tension / 1000
    return k * (1 / R1 - 1 / R0) / (factor * R0**4 * speed0**2 / R1**5 + k / R1**2) * 1e6


@_type(14, "การแก้รัศมีลำน้ำเนื่องจากแรงตึงผิว", JET_TOPIC)
class JetCorrection(PhysicsSheet):
    def _variant(self, rng):
        radius0, speed0 = _jet(rng)
        height = rng.randint(5, 20)
        h = height / 100
        dr = q14.solve(radius0=radius0, speed0=speed0, height=h)
        assert abs(dr - _correction(radius0, speed0, h, 0.072)) <= 1e-9 * dr
        return draw(
            14,
            measure(dr),
            JET.format(R0=f"{radius0:.2f}", v0=f"{speed0:g}")
            + f" ความตึงผิว 0.072 N/m ทำให้ความดันในลำน้ำรัศมี R มากกว่าอากาศ γ/R ที่ระยะ {height} cm ใต้ปลายท่อ รัศมีลำน้ำต่างจากค่า R₁ ที่ไม่คิดแรงตึงผิวเป็น R₁ + ΔR ใช้การประมาณอันดับหนึ่ง ΔR เป็นกี่ไมโครเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{R_0^4}{R^4}v_0^2+\frac{2\gamma}{\rho R}-2gh=v_0^2+\frac{2\gamma}{\rho R_0}",
            [
                measure(_correction(radius0, speed0, h, 0.072, factor=1.0)),
                measure(_correction(radius0, speed0, h, 0.144)),
                measure(_correction(radius0, speed0, h, 0.036)),
            ],
        )


@_type(15, "ระยะที่ลำน้ำตกก่อนแตกเป็นหยด", JET_TOPIC)
class JetBreakup(PhysicsSheet):
    def _variant(self, rng):
        radius0, speed0 = _jet(rng)
        tension = rng.choice((0.072, 0.065, 0.050))
        h = q15.solve(radius0=radius0, speed0=speed0, tension=tension)
        t = 2.91 * sqrt(1000 * (radius0 / 100) ** 3 / tension)
        return draw(
            15,
            measure(h),
            JET.format(R0=f"{radius0:.2f}", v0=f"{speed0:g}")
            + f" ความตึงผิว {tension:g} N/m ตามผลของ Plateau และ Rayleigh ลำน้ำเริ่มแตกเป็นหยดหลังเวลา 2.91√(ρR₀³/γ) น้ำเคลื่อนที่ลงมาได้กี่เซนติเมตรก่อนเริ่มแตกเป็นหยด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"h=v_0t+\tfrac12gt^2",
            [measure(10 * h), measure(4.9 * t * t * 100), measure((speed0 * t + 9.8 * t * t) * 100)],
        )


@_type(16, "รัศมีหยดน้ำจากทรงกระบอกที่แตกออก", JET_TOPIC)
class DropRadius(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(5, 30) / 10
        r = q16.solve(radius=radius)
        return draw(
            16,
            measure(r),
            f"ลำน้ำรัศมี {radius:g} mm แตกออกเป็นทรงกระบอกสั้น ๆ แต่ละท่อนหดเป็นหยดทรงกลมทันทีโดยปริมาตรคงเดิม และพลังงานแรงตึงผิว (แปรผันตรงกับพื้นที่ผิว) คงเดิม ไม่คิดพื้นที่ปลายทั้งสองของทรงกระบอก หยดน้ำมีรัศมีกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\pi R^2L=\tfrac43\pi r^3,\quad 2\pi RL=4\pi r^2",
            [measure(0.75 * radius), measure((0.75 * 9.1) ** (1 / 3) * radius), measure(sqrt(9.1 / 2) * radius)],
        )


@_type(17, "ความต่างศักย์ขีดเริ่มของไดโอดหนึ่งตัวจากกล่องดำ", DIODE_TOPIC)
class DiodeThreshold(PhysicsSheet):
    def _variant(self, rng):
        n = rng.randint(1, 4)
        each = rng.randint(55, 75) / 100
        forward, reverse = round(n * each, 2), round((5 - n) * each, 2)
        v = q17.solve(forward=forward, reverse=reverse)
        total = forward + reverse
        return draw(
            17,
            measure(v),
            "กล่องดำมีไดโอดชนิดเดียวกัน 5 ตัวต่ออยู่บนวงจรขนานสองเส้น เส้นละ 4 ช่อง (แต่ละช่องเป็นไดโอดหรือลวด) ให้กระแสไหลได้ทั้งสองทิศ "
            f"จากกราฟกระแสกับความต่างศักย์ ความต่างศักย์ขีดเริ่มในทิศหนึ่งเป็น {forward:.2f} V และเมื่อกลับขั้วเป็น {reverse:.2f} V "
            "ไดโอดหนึ่งตัวมีความต่างศักย์ขีดเริ่มกี่โวลต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V_+=nV_d,\quad V_-=(5-n)V_d",
            [measure(total / 2), measure(total / 8), measure(total / 4)],
        )


@_type(18, "ความต้านทานในกล่องดำไดโอดจากความชันกราฟ", DIODE_TOPIC)
class DiodeResistance(PhysicsSheet):
    def _variant(self, rng):
        resistance = rng.randint(5, 30) * 100
        onset = rng.choice((1, 2)) * rng.randint(60, 70) / 100
        start = rng.choice((1.0, 1.2, 1.5, 2.0))
        step = rng.choice((0.4, 0.5))
        count = rng.randint(4, 5)
        readings = []
        for k in range(count):
            a = round(start + k * step, 2)
            readings.append((a, round(onset + a / 2000 * resistance + rng.choice((-0.01, 0, 0, 0.01)), 2)))
        readings = tuple(readings)
        r = q18.solve(readings=readings)
        a, b = readings[-1]
        table = ", ".join(f"({x:.2f} V, {y:.2f} V)" for x, y in readings)
        return draw(
            18,
            measure(r),
            "กล่องดำไดโอดต่ออนุกรมกับตัวต้านทาน R ไม่ทราบค่าและตัวต้านทาน 2.00 kΩ ในทิศที่ไดโอดนำไฟฟ้าเต็มที่ "
            f"วัดความต่างศักย์คร่อมตัวต้านทาน 2.00 kΩ และคร่อมชุดไดโอดกับ R ได้ดังนี้ {table} "
            "หาค่า R จากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) ได้กี่โอห์ม (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"I=\frac{V_{2k}}{2000\ \Omega},\quad V=V_{\text{on}}+IR",
            [measure(r / 2000), measure(b / (a / 2000)), measure(r + 2000)],
        )


@_type(19, "สัมประสิทธิ์ความเสียดทานสถิตจากกราฟ", FRICTION_TOPIC)
class StaticFriction(PhysicsSheet):
    def _variant(self, rng):
        mu = rng.randint(25, 70) / 100
        clip = rng.choice((0.5, 1.5, 2.0, 2.5))
        start = rng.randint(2, 4) * 40
        step = rng.choice((40, 50, 60))
        loads = tuple(start + k * step for k in range(5))
        counts = tuple(round(mu * m / clip + rng.choice((-0.6, 0, 0.6))) for m in loads)
        s = q19.solve(clip=clip, loads=loads, counts=counts)
        table = ", ".join(f"({m} g, {c} ตัว)" for m, c in zip(loads, counts))
        return draw(
            19,
            measure(s),
            f"กล่องที่มีดินสอติดด้านล่างวางบนไม้บรรทัด ถูกดึงด้วยเชือกผ่านรอกไปยังถุงที่ใส่ลวดหนีบกระดาษตัวละ {clip:g} g "
            f"(ไม่คิดมวลถุง) เปลี่ยนมวลกล่องแล้วนับจำนวนลวดหนีบที่ทำให้กล่องเริ่มเลื่อนได้ดังนี้ {table} "
            "สัมประสิทธิ์ความเสียดทานสถิตจากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F_s=\mu_sN\Rightarrow m_{\text{clips}}=\mu_s m_{\text{box}}",
            [measure(s / clip), measure(1 / s), measure(9.8 * s)],
        )


@_type(20, "สัมประสิทธิ์ความเสียดทานจลน์จากการเลื่อนดินสอ", FRICTION_TOPIC)
class KineticFriction(PhysicsSheet):
    def _variant(self, rng):
        static = rng.randint(30, 70) / 100
        ratio = rng.randint(110, 160) / 100
        start = rng.randint(3, 6)
        near = tuple(float(start + 2 * k) for k in range(5))
        far = tuple(round(x / ratio + rng.choice((-0.1, 0.0, 0.1)), 1) for x in near)
        mk = q20.solve(static=static, near=near, far=far)
        slope = static / mk
        table = ", ".join(f"({a:g} cm, {b:g} cm)" for a, b in zip(near, far))
        return draw(
            20,
            measure(mk),
            "ไม้บรรทัดวางบนดินสอสองแท่ง จับแท่ง A ไว้กับที่แล้วค่อย ๆ เลื่อนแท่ง B เข้าหาศูนย์กลางมวล บันทึกระยะ x_A จากแท่ง A ถึงศูนย์กลางมวล "
            f"และระยะ x_B จากแท่ง B ถึงศูนย์กลางมวลเมื่อไม้บรรทัดเริ่มเลื่อน (x_A, x_B) ได้ดังนี้ {table} "
            f"ถ้าสัมประสิทธิ์ความเสียดทานสถิตเป็น {static:.2f} สัมประสิทธิ์ความเสียดทานจลน์จากความชันของกราฟ x_A กับ x_B (วิธีกำลังสองน้อยที่สุด) เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mu_kN_B=\mu_sN_A,\quad \frac{N_B}{N_A}=\frac{x_A}{x_B}",
            [measure(static * slope), measure(1 / slope), measure(slope)],
        )
