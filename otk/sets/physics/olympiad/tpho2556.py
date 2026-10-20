"""Seeded variants of the reviewed TPhO 12 (2556) national physics olympiad."""

from math import acos, asin, atan, cos, degrees, exp, floor, log, log10, pi, radians, sin, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2556_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2556_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21

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
    1: ("phys.hinged_rod_rotation_ignored", "phys.rod_as_point_mass", "phys.rod_angle_sin_cos_swapped"),
    2: ("phys.rod_as_point_mass", "phys.rod_angle_sin_cos_swapped", "phys.rod_angle_factor_dropped"),
    3: ("phys.hinged_rod_rotation_ignored", "phys.rod_as_point_mass", "phys.rod_angle_sin_cos_swapped"),
    4: ("phys.stagnation_half_dropped", "phys.drag_full_sphere_area", "phys.radius_taken_as_diameter"),
    5: ("phys.stagnation_half_dropped", "phys.drag_coefficient_dropped", "phys.drag_full_sphere_area"),
    6: ("phys.meteor_entry_angle_dropped", "phys.meteor_sin_cos_swapped", "phys.stagnation_half_dropped"),
    7: ("phys.meteor_peak_force_for_power", "phys.meteor_power_factor_dropped", "phys.natural_log_as_common"),
    8: ("phys.meteor_speed_loss_ignored", "phys.stagnation_half_dropped", "phys.meteor_peak_force_for_power"),
    9: ("phys.pressure_shared_between_cylinders", "phys.weight_as_mass", "phys.both_pistons_counted"),
    10: ("phys.spring_extension_halved", "phys.weight_as_mass", "phys.centimetres_not_converted"),
    11: ("phys.transfer_isothermal_assumed", "phys.work_on_wrong_gas", "phys.temperature_ratio_inverted"),
    12: ("phys.spring_work_half_dropped", "phys.weight_not_squared", "phys.work_on_wrong_gas"),
    13: ("phys.transfer_isothermal_assumed", "phys.spring_work_ignored", "phys.internal_energy_gamma_misused"),
    14: ("phys.transfer_isothermal_assumed", "phys.temperature_ratio_inverted", "phys.temperature_gamma_ratio"),
    15: ("phys.rainbow_refraction_for_incidence", "phys.rainbow_condition_minus_one_dropped", "phys.angle_from_surface"),
    16: ("phys.rainbow_deviation_for_angle", "phys.rainbow_condition_minus_one_dropped", "phys.rainbow_order_confused"),
    17: ("phys.rainbow_deviation_for_angle", "phys.rainbow_condition_minus_one_dropped", "phys.rainbow_order_confused"),
    18: ("phys.period_for_frequency", "phys.torsion_two_pi_dropped", "phys.disc_axis_inertia"),
    19: ("phys.period_squared_dropped", "phys.pendulum_formula_for_graph", "phys.graph_ratio_inverted"),
    20: ("phys.coupling_factor_two_dropped", "phys.coupling_ratio_inverted", "phys.frequency_for_period"),
    21: ("phys.inclination_ratio_inverted", "phys.inclination_sine", "phys.radians_for_degrees"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 12 (2556)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2556_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2556_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


RODS_TOPIC = "การดลท่อนไม้ที่ต่อด้วยจุดหมุน"
METEOR_TOPIC = "แรงต้านอากาศต่ออุกกาบาต"
VALVE_TOPIC = "การถ่ายเทก๊าซผ่านวาล์ว"
RAINBOW_TOPIC = "รุ้งกินน้ำ"
MAGNET_TOPIC = "การแกว่งคู่ควบและสนามแม่เหล็กโลก"

RODS = (
    "ท่อนไม้สม่ำเสมอสามท่อน แต่ละท่อนมวล {m} kg ยาว {l} m ต่อกันด้วยจุดหมุนลื่นที่ B และ C วางนิ่งบนพื้นลื่น "
    "ท่อน AB และ CD ทำมุม {t}° กับท่อน BC ดีดที่กึ่งกลาง BC ในทิศตั้งฉากกับ BC (แกน Y) ทำให้ BC เคลื่อนที่ด้วยอัตราเร็ว {u} m/s (I_cm = ml²/12)"
)


def _rods(rng):
    angle = rng.choice((20, 30, 35, 40, 50, 55, 60, 70, 75, 80))
    return angle, rng.randint(1, 6), rng.randint(2, 15) / 10, rng.randint(2, 20) / 10


@_type(1, "อัตราเร็วแนว Y ของท่อนไม้ที่ถูกดีด", RODS_TOPIC)
class RodSideSpeed(PhysicsSheet):
    def _variant(self, rng):
        angle, speed, length, mass = _rods(rng)
        vy = q01.solve(angle=angle, speed=speed)
        s = sin(radians(angle))
        return draw(
            1,
            measure(vy),
            RODS.format(m=f"{mass:g}", l=f"{length:g}", t=angle, u=speed) + " ทันทีหลังการดีด จุดศูนย์กลางมวลของท่อน CD มีอัตราเร็วในแนวแกน Y กี่เมตรต่อวินาทีเทียบกับพื้น (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"L_C=\tfrac{1}{12}ml^2\omega+\vec r\times m\vec v_{cm}=0",
            [measure(speed), measure(speed * s * s), measure(speed * (1 - 0.75 * s * s))],
        )


@_type(2, "อัตราเร็วเชิงมุมของท่อนไม้ข้างที่ถูกดีด", RODS_TOPIC)
class RodSideSpin(PhysicsSheet):
    def _variant(self, rng):
        angle, speed, length, mass = _rods(rng)
        w = q02.solve(angle=angle, speed=speed, length=length)
        c, s = cos(radians(angle)), sin(radians(angle))
        return draw(
            2,
            measure(w),
            RODS.format(m=f"{mass:g}", l=f"{length:g}", t=angle, u=speed) + " ทันทีหลังการดีด ท่อน CD หมุนรอบ C ด้วยอัตราเร็วเชิงมุมกี่เรเดียนต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac13ml^2\omega=\tfrac12mlu\cos\theta",
            [measure(2 * speed * c / length), measure(3 * speed * s / (2 * length)), measure(3 * speed / (2 * length))],
        )


@_type(3, "การดลที่ใช้ดีดท่อนไม้สามท่อน", RODS_TOPIC)
class RodJerk(PhysicsSheet):
    def _variant(self, rng):
        angle, speed, length, mass = _rods(rng)
        j = q03.solve(mass=mass, speed=speed, angle=angle)
        c, s = cos(radians(angle)), sin(radians(angle))
        return draw(
            3,
            measure(j),
            RODS.format(m=f"{mass:g}", l=f"{length:g}", t=angle, u=speed) + " การดลของแรงดีดมีขนาดกี่นิวตันวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"J=mu+2mv_y,\quad v_y=u\left(1-\tfrac34\cos^2\theta\right)",
            [measure(3 * mass * speed), measure(mass * speed * (1 + 2 * s * s)), measure(1.5 * mass * speed * (1 + c * c))],
        )


@_type(4, "แรงจากความดันอากาศด้านหน้าอุกกาบาต", METEOR_TOPIC)
class MeteorPush(PhysicsSheet):
    def _variant(self, rng):
        density = rng.choice((0.01, 0.02, 0.05, 0.1, 0.2, 0.5))
        speed = rng.randint(10, 40)
        radius = rng.randint(2, 20) / 10
        f = q04.solve(density=density, speed=speed, radius=radius) / 1e6
        return draw(
            4,
            measure(f),
            f"อุกกาบาตทรงกลมรัศมี {radius:g} m เคลื่อนที่ด้วยอัตราเร็ว {speed} km/s ในอากาศความหนาแน่น {density:g} kg/m³ ถ้าอากาศที่พุ่งเข้าหาหยุดนิ่งเทียบกับอุกกาบาต แรงจากความดันด้านหน้ามีขนาดกี่เมกะนิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta P=\tfrac12\rho v^2,\quad F=\Delta P\,\pi r^2",
            [measure(2 * f), measure(4 * f), measure(f / 4)],
        )


@_type(5, "ความเร่งของอุกกาบาตจากแรงต้าน", METEOR_TOPIC)
class MeteorDeceleration(PhysicsSheet):
    def _variant(self, rng):
        drag = rng.choice((0.5, 0.6, 0.8, 1.2, 1.5))
        density = rng.choice((0.01, 0.02, 0.05, 0.1))
        speed = rng.randint(10, 40)
        radius = rng.randint(2, 10) / 10
        mass = round(4 / 3 * pi * radius**3 * 3000, -1)
        a = q05.solve(drag=drag, density=density, speed=speed, radius=radius, mass=mass)
        return draw(
            5,
            measure(a),
            f"อุกกาบาตทรงกลมมวล {mass:g} kg รัศมี {radius:g} m เคลื่อนที่ด้วยอัตราเร็ว {speed} km/s ในอากาศความหนาแน่น {density:g} kg/m³ แรงต้านเป็น {drag:g} เท่าของแรงจากความดันหยุดนิ่ง ½ρv²πr² อุกกาบาตมีความหน่วงกี่เมตรต่อวินาทีกำลังสอง (ไม่คิดน้ำหนัก ตอบเลขนัยสำคัญ 3 ตัว)",
            r"ma=C_d\tfrac12\rho v^2\pi r^2",
            [measure(2 * a), measure(a / drag), measure(4 * a)],
        )


ENTRY = (
    "อุกกาบาตทรงกลมมวล {m:g} kg รัศมี {r:g} m พุ่งเข้าสู่บรรยากาศด้วยอัตราเร็วต้น {u} km/s ทำมุม {t}° กับแนวระดับ "
    "ความหนาแน่นอากาศ ρ = ρ₀e^(−αz) โดย ρ₀ = 1.2 kg/m³, 1/α = 8.0 km แรงต้าน C_d(½ρv²πr²) กับ C_d = {c:g} ไม่คิดน้ำหนัก"
)


def _entry(rng):
    while True:
        angle = rng.choice((20, 30, 35, 40, 50, 55, 60, 70))
        radius = rng.randint(2, 15) / 10
        mass = round(4 / 3 * pi * radius**3 * rng.choice((2500, 3000, 3500)), -1)
        drag = rng.choice((0.6, 0.8, 1.0, 1.2))
        A = -q06.solve(drag=drag, radius=radius, mass=mass, angle=angle)
        if 1.5 <= A <= 30:
            return angle, radius, mass, drag, A


@_type(6, "ค่าคงที่ในสมการความเร็วของอุกกาบาต", METEOR_TOPIC)
class MeteorConstant(PhysicsSheet):
    def _variant(self, rng):
        angle, radius, mass, drag, A = _entry(rng)
        s, c = sin(radians(angle)), cos(radians(angle))
        return draw(
            6,
            measure(-A),
            ENTRY.format(m=mass, r=radius, u=20, t=angle, c=drag) + " อัตราเร็วที่ความสูง z เป็น v = u·e^(a·e^(bz)) ค่า a เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"-\sin\theta\,v\frac{dv}{dz}=-\frac{C_d\rho_0e^{-\alpha z}\pi r^2}{2m}v^2",
            [measure(-A * s), measure(-A * s / c), measure(-2 * A)],
        )


@_type(7, "ความสูงที่อุกกาบาตสว่างที่สุด", METEOR_TOPIC)
class MeteorBrightest(PhysicsSheet):
    def _variant(self, rng):
        angle, radius, mass, drag, A = _entry(rng)
        z = q07.solve(drag=drag, radius=radius, mass=mass, angle=angle)
        scale = 8.0
        return draw(
            7,
            measure(z),
            ENTRY.format(m=mass, r=radius, u=20, t=angle, c=drag) + " อุกกาบาตสว่างที่สุด (อัตราการสูญเสียพลังงานจลน์ ∝ ρv³ มากที่สุด) ที่ความสูงกี่กิโลเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"v=u\,e^{-Ae^{-\alpha z}},\quad \frac{d}{dz}\left(\rho v^3\right)=0",
            [measure(scale * log(2 * A)), measure(scale * log(A)), measure(scale * log10(3 * A))],
        )


@_type(8, "ความดันที่อุกกาบาตต้องทนได้", METEOR_TOPIC)
class MeteorPressure(PhysicsSheet):
    def _variant(self, rng):
        angle, radius, mass, drag, A = _entry(rng)
        speed = rng.randint(12, 60)
        p = q08.solve(drag=drag, radius=radius, mass=mass, angle=angle, speed=speed)
        u2 = (speed * 1e3) ** 2
        return draw(
            8,
            measure(p),
            ENTRY.format(m=mass, r=radius, u=speed, t=angle, c=drag) + " ที่ความสูงที่อุกกาบาตสว่างที่สุด (ρv³ มากที่สุด) ความดันหยุดนิ่ง ½ρv² ด้านหน้ามีค่ากี่เมกะพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"e^{-\alpha z_{\max}}=\frac{1}{3A},\quad v=u\,e^{-1/3}",
            [measure(p * exp(2 / 3)), measure(2 * p), measure(1.2 * 0.5 * u2 * exp(-1) / (2 * A) / 1e6)],
        )


VALVE = (
    "กระบอกสูบ A และ B พื้นที่หน้าตัด {a} cm² เท่ากัน อยู่ในสุญญากาศและเป็นฉนวน ลูกสูบเบาของ A มีมวล {m} kg ทับอยู่ "
    "ลูกสูบเบาของ B ติดสปริงค่าคงตัว {k} N/m ความยาวธรรมชาติเท่ากับความสูงกระบอกสูบ (B เดิมเป็นสุญญากาศ) "
    "เปิดวาล์วเล็กน้อยให้ก๊าซอุดมคติ (γ = {g}) ไหลจาก A ไป B ช้า ๆ จนหยุดไหล (g = 9.8 m/s²)"
)
GAMMAS = ((1.4, "1.4"), (5 / 3, "5/3"), (1.3, "1.3"))


def _valve(rng):
    gamma, shown = rng.choice(GAMMAS)
    return rng.randint(1, 20), rng.randint(2, 20) * 5, rng.randint(2, 40) * 100, gamma, shown


@_type(9, "ความดันสุดท้ายในกระบอกสูบสปริง", VALVE_TOPIC)
class ValvePressure(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        p = q09.solve(mass=mass, area=area)
        return draw(
            9,
            measure(p),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + " ความดันสุดท้ายของก๊าซในกระบอกสูบ B เป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_B=P_A=\frac{mg}{a}",
            [measure(p / 2), measure(p / 9.8), measure(2 * p)],
        )


@_type(10, "ปริมาตรก๊าซในกระบอกสูบสปริง", VALVE_TOPIC)
class ValveVolume(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        v = q10.solve(mass=mass, area=area, spring=spring)
        return draw(
            10,
            measure(v),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + " ปริมาตรสุดท้ายของก๊าซในกระบอกสูบ B เป็นกี่ลูกบาศก์เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"kx=P_Ba=mg,\quad V_B=ax",
            [measure(v / 2), measure(v / 9.8), measure(v / 100)],
        )


def _energies(mass, spring, gamma):
    base = (mass * 9.8) ** 2 / spring
    return base, base * (gamma + 1) / (2 * gamma), base / 2


@_type(11, "งานที่แรงกดทำต่อก๊าซที่ถูกถ่ายเท", VALVE_TOPIC)
class ValveWorkIn(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        w = q11.solve(mass=mass, spring=spring, gamma=gamma)
        base, _, spring_work = _energies(mass, spring, gamma)
        return draw(
            11,
            measure(w),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + " น้ำหนักบนลูกสูบ A ทำงานต่อก๊าซที่ถูกถ่ายเทไปกี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"W_A=P\,\Delta V_A=P\,V_B\frac{T_A}{T_B},\quad \frac{T_B}{T_A}=\frac{2\gamma}{\gamma+1}",
            [measure(base), measure(spring_work), measure(base * 2 * gamma / (gamma + 1))],
        )


@_type(12, "งานที่ก๊าซทำต่อลูกสูบสปริง", VALVE_TOPIC)
class ValveWorkOut(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        w = q12.solve(mass=mass, spring=spring)
        base, work_in, _ = _energies(mass, spring, gamma)
        return draw(
            12,
            measure(w),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + " ก๊าซในกระบอกสูบ B ทำงานต่อลูกสูบ (กดสปริง) กี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"W_B=\tfrac12kx^2,\quad x=\frac{mg}{k}",
            [measure(base), measure(mass * 9.8**2 / (2 * spring)), measure(work_in)],
        )


@_type(13, "พลังงานภายในที่เปลี่ยนไปของก๊าซที่ถูกถ่ายเท", VALVE_TOPIC)
class ValveEnergy(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        du = q13.solve(mass=mass, spring=spring, gamma=gamma)
        base, work_in, _ = _energies(mass, spring, gamma)
        return draw(
            13,
            measure(du),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + " พลังงานภายในของก๊าซที่ถูกถ่ายเทเพิ่มขึ้นกี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta U=W_A-W_B",
            [measure(base / 2), measure(work_in), measure(base * (gamma - 1) / 2)],
        )


@_type(14, "อุณหภูมิก๊าซหลังการถ่ายเท", VALVE_TOPIC)
class ValveTemperature(PhysicsSheet):
    def _variant(self, rng):
        mass, area, spring, gamma, shown = _valve(rng)
        temp = rng.randint(50, 80) * 5
        t = q14.solve(temp=temp, gamma=gamma)
        return draw(
            14,
            measure(t),
            VALVE.format(a=area, m=mass, k=spring, g=shown) + f" ก๊าซใน A มีอุณหภูมิคงตัว {temp} K หลังการถ่ายเทสิ้นสุด ก๊าซใน B มีอุณหภูมิกี่เคลวิน (U = PV/(γ − 1), ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{PV_B}{\gamma-1}\left(1-\frac{T_A}{T_B}\right)=PV_B\left(\frac{T_A}{T_B}-\frac12\right)",
            [str(temp), measure(temp * (gamma + 1) / (2 * gamma)), measure(temp * gamma)],
        )


INDICES = (1.329, 1.331, 1.333, 1.335, 1.338, 1.343)
NAMES = {1: "หนึ่งครั้ง (รุ้งปฐมภูมิ)", 2: "สองครั้ง (รุ้งทุติยภูมิ)"}


def _bow_angles(n, N, minus_one=True):
    theta = acos(sqrt((n * n - 1) / ((N + 1) ** 2 - (1 if minus_one else 0))))
    phi = asin(sin(theta) / n)
    alpha = abs(degrees(2 * pi - (N + 1) * (pi - 2 * phi) - 2 * theta))
    return degrees(theta), degrees(phi), alpha


@_type(15, "มุมตกกระทบที่ให้รุ้งสว่างที่สุด", RAINBOW_TOPIC)
class RainbowIncidence(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(INDICES)
        N = rng.choice((1, 2))
        theta = q15.solve(index=n, reflections=N)
        _, phi, _ = _bow_angles(n, N)
        return draw(
            15,
            measure(theta),
            f"แสงอาทิตย์ตกกระทบหยดน้ำทรงกลมดัชนีหักเห {n} หักเหเข้าไป สะท้อนภายใน{NAMES[N]} แล้วหักเหออก มุมตกกระทบเท่าใด (องศา) ที่ทำให้แสงเบี่ยงเบนออกมาเข้มที่สุด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{d\alpha}{d\theta}=0\Rightarrow\cos^2\theta=\frac{n^2-1}{(N+1)^2-1}",
            [measure(phi), measure(_bow_angles(n, N, minus_one=False)[0]), measure(90 - theta)],
        )


@_type(16, "มุมของรุ้งปฐมภูมิ", RAINBOW_TOPIC)
class RainbowPrimary(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(INDICES)
        alpha = q16.solve(index=n)
        return draw(
            16,
            measure(alpha),
            f"หยดน้ำทรงกลมมีดัชนีหักเห {n} สำหรับรุ้งปฐมภูมิ (สะท้อนภายในหนึ่งครั้ง) แสงที่เข้มที่สุดเบี่ยงจากแนวแสงอาทิตย์เดิมทำมุม α = 2π − 2(π − 2φ) − 2θ กี่องศา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\alpha=4\varphi-2\theta,\quad \cos^2\theta=\frac{n^2-1}{3}",
            [measure(180 - alpha), measure(_bow_angles(n, 1, minus_one=False)[2]), measure(q17.solve(index=n))],
        )


@_type(17, "มุมของรุ้งทุติยภูมิ", RAINBOW_TOPIC)
class RainbowSecondary(PhysicsSheet):
    def _variant(self, rng):
        n = rng.choice(INDICES)
        alpha = q17.solve(index=n)
        return draw(
            17,
            measure(alpha),
            f"หยดน้ำทรงกลมมีดัชนีหักเห {n} สำหรับรุ้งทุติยภูมิ (สะท้อนภายในสองครั้ง) แสงที่เข้มที่สุดออกมาทำมุม |α| กับแนวแสงอาทิตย์เดิมกี่องศา โดย α = 2π − 3(π − 2φ) − 2θ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\cos^2\theta=\frac{n^2-1}{8}",
            [measure(180 + alpha), measure(_bow_angles(n, 2, minus_one=False)[2]), measure(q16.solve(index=n))],
        )


MAGNET = "แม่เหล็กจานสองอันประกบกัน มวลรวม 27.6 g รัศมี 14.0 mm หนารวม 6.00 mm (I = mR²/4 + md²/12)"
INERTIA = 27.6e-3 * (14e-3**2 / 4 + 6e-3**2 / 12)


@_type(18, "โมเมนต์แม่เหล็กจากการแกว่งแบบบิด", MAGNET_TOPIC)
class MagnetMoment(PhysicsSheet):
    def _variant(self, rng):
        time50 = rng.randint(280, 400) / 10
        field = rng.randint(30, 50) / 100
        mu = q18.solve(time50=time50, field=field)
        f = 50 / time50
        return draw(
            18,
            measure(mu),
            MAGNET + f" แขวนให้แกว่งแบบบิดอย่างเดียวในสนามแม่เหล็กโลกแนวราบ {field:g} G จับเวลา 50 รอบได้ {time50:g} s "
            "magnetic moment ของแม่เหล็กเป็นกี่ A·m² (f = (1/2π)√(μB_h/I), ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mu=\frac{I(2\pi f)^2}{B_h}",
            [
                measure(INERTIA * (2 * pi / f) ** 2 / (field * 1e-4)),
                measure(mu / (2 * pi) ** 2),
                measure(27.6e-3 * 14e-3**2 / 2 * (2 * pi * f) ** 2 / (field * 1e-4)),
            ],
        )


LENGTHS = (15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0)


@_type(19, "ความยาวเชือกที่คาบลูกตุ้มเท่าคาบการบิด", MAGNET_TOPIC)
class MagnetMatchLength(PhysicsSheet):
    def _variant(self, rng):
        slope = rng.randint(36, 42) / 1000
        periods = tuple(round(sqrt(slope * x) + rng.choice((-0.01, 0, 0.01)), 2) for x in LENGTHS)
        time50 = rng.randint(280, 360) / 10
        lm = q19.solve(lengths=LENGTHS, periods=periods, time50=time50)
        t = time50 / 50
        fit = t * t / lm
        table = ", ".join(f"({x:g} cm, {p:.2f} s)" for x, p in zip(LENGTHS, periods))
        return draw(
            19,
            measure(lm),
            f"แขวนแม่เหล็กแกว่งแบบลูกตุ้มที่ความยาวเชือกต่าง ๆ วัดคาบได้ (ℓ, T) {table} และแกว่งแบบบิด 50 รอบได้ {time50:g} s "
            "ใช้กราฟ T² กับ ℓ (เส้นตรงผ่านจุดกำเนิด วิธีกำลังสองน้อยที่สุด) หาความยาวเชือกที่คาบทั้งสองแบบเท่ากันได้กี่เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T_p^2=s\,\ell,\quad \ell_m=\frac{T_t^2}{s}",
            [measure(t / fit), measure(9.8 * t * t / (4 * pi * pi) * 100), measure(fit / (t * t))],
        )


@_type(20, "สนามแม่เหล็กโลกแนวดิ่งจากการแกว่งคู่ควบ", MAGNET_TOPIC)
class MagnetVertical(PhysicsSheet):
    def _variant(self, rng):
        tau = rng.randint(20, 50)
        freq = rng.randint(130, 160) / 100
        length = rng.randint(100, 140) / 10
        field = 0.41
        bv = q20.solve(tau=tau, freq=freq, length=length, field=field)
        root = sqrt(14e-3**2 + 6e-3**2 / 3)
        return draw(
            20,
            measure(bv),
            MAGNET + f" สนามแม่เหล็กโลกแนวราบ 0.41 G ความถี่การบิด {freq:g} Hz ที่ความยาวเชือก {length:g} cm ช่วงเวลาถ่ายโอนพลังงานสูงสุด τ_max = {tau} s "
            "ใช้ τ_max ≅ (B_h/B_v)(1/f)(2ℓ_max/√(R² + d²/3)) สนามแม่เหล็กโลกแนวดิ่งเป็นกี่เกาส์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B_v=\frac{2\ell_{\max}B_h}{\tau_{\max}f\sqrt{R^2+d^2/3}}",
            [measure(bv / 2), measure(field * tau * freq * root / (2 * length * 1e-2)), measure(bv * freq * freq)],
        )


@_type(21, "มุมเอียงของสนามแม่เหล็กโลก", MAGNET_TOPIC)
class MagnetInclination(PhysicsSheet):
    def _variant(self, rng):
        vertical = rng.randint(5, 24) / 100
        horizontal = rng.randint(25, 45) / 100
        g = q21.solve(vertical=vertical, horizontal=horizontal)
        return draw(
            21,
            measure(g),
            f"สนามแม่เหล็กโลกที่ตำแหน่งหนึ่งมีองค์ประกอบแนวราบ {horizontal:g} G และแนวดิ่ง {vertical:g} G มุมเอียง (inclination) ของสนามเป็นกี่องศา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tan\gamma=\frac{B_v}{B_h}",
            [
                measure(degrees(atan(horizontal / vertical))),
                measure(degrees(asin(vertical / horizontal))),
                measure(atan(vertical / horizontal)),
            ],
        )
