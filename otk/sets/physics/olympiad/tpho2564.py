"""Seeded variants of the reviewed TPhO 20 (2564) national physics olympiad."""

from math import asin, atan, cos, degrees, floor, log, log10, pi, radians, sin, sqrt, tan

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2564_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2564_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.tpho2564_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def figures(value):
    """A nonzero float to three significant figures, as plain text."""
    digits = 2 - floor(log10(abs(value)))
    return f"{round(value, digits):.{digits}f}" if digits > 0 else str(int(round(value, digits)))


def scientific(value):
    """A nonzero float to three significant figures as mantissa × 10^n."""
    power = floor(log10(abs(value)))
    mantissa = round(value / 10**power, 2)
    if abs(mantissa) >= 10:
        mantissa, power = mantissa / 10, power + 1
    return rf"{mantissa:.2f}\times10^{{{power}}}"


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def stated(value):
    """A reading to three significant figures as stem text: plain in
    ordinary ranges, otherwise as mantissa×10ⁿ with a superscript power."""
    if 1e-3 <= abs(value) < 1e5:
        return figures(value)
    power = floor(log10(abs(value)))
    mantissa = round(value / 10**power, 2)
    if abs(mantissa) >= 10:
        mantissa, power = mantissa / 10, power + 1
    return f"{mantissa:.2f}×10" + str(power).translate(SUPERSCRIPT)


def measure(value):
    """A nonzero float to three significant figures: plain in ordinary
    ranges, otherwise as mantissa × 10^n."""
    if 1e-3 <= abs(value) < 1e5:
        return figures(value)
    return scientific(value)


SLIPS = {
    1: ("phys.rolling_solid_cylinder", "phys.slant_sine_for_cosine", "phys.rolling_ignored"),
    2: ("phys.friction_sideways_ignored", "phys.rolling_friction_half_dropped", "phys.friction_not_rooted"),
    3: ("phys.half_mass_ignored", "phys.half_cylinder_rotates", "phys.loose_masses_swapped"),
    4: ("phys.half_tilts_with_incline", "phys.tilt_complement_taken", "phys.half_mass_ignored"),
    5: ("phys.worst_turn_half_turn", "phys.system_cm_not_reduced", "phys.turn_angle_not_divided"),
    6: ("phys.half_on_top_inertia", "phys.half_mass_ignored", "phys.half_cm_at_axis"),
    7: ("phys.potential_sign_flipped", "phys.system_cm_not_reduced", "phys.potential_change_ignored"),
    8: ("phys.centripetal_ignored", "phys.centripetal_sign_flipped", "phys.centripetal_radius_r"),
    9: ("phys.initial_speed_ignored", "phys.position_full_gap", "phys.speeds_added_not_squares"),
    10: ("phys.child_langmuir_four_ninths_dropped", "phys.current_linear_in_voltage", "phys.gap_not_squared"),
    11: ("phys.potential_linear", "phys.child_exponent_inverted", "phys.potential_quadratic"),
    12: ("phys.space_charge_factor_dropped", "phys.charge_sign_flipped", "phys.plate_area_dropped"),
    13: ("phys.charge_sign_flipped", "phys.space_charge_factor_dropped", "phys.surface_charge_halved"),
    14: ("phys.led_log10_used", "phys.lung_wrong_ratio", "phys.per_kilopascal_confusion"),
    15: ("phys.work_pressure_times_volume", "phys.work_triangle", "phys.work_bracket_dropped"),
    16: ("phys.efficiency_not_divided", "phys.efficiency_multiplied", "phys.calories_not_kilo"),
    17: ("phys.monatomic_heat_capacity", "phys.cp_for_cv", "phys.absolute_pressure_used"),
    18: ("phys.first_law_sign", "phys.work_ignored", "phys.internal_energy_ignored"),
    19: ("phys.exhale_work_ignored", "phys.heat_as_internal_energy", "phys.exhale_work_added"),
    20: ("phys.lens_sign_convention", "phys.image_f_squared", "phys.image_from_source"),
    21: ("phys.separation_one_not_subtracted", "phys.separation_cut_only", "phys.separation_doubled"),
    22: ("phys.lens_height_not_reduced", "phys.overlap_half_distance", "phys.lmax_ratio_inverted"),
    23: ("phys.fringe_half_angle", "phys.fringe_doubled", "phys.fringe_lens_height"),
    24: ("phys.overlap_full_width", "phys.lens_height_not_reduced", "phys.overlap_quarter"),
    25: ("phys.deflection_factor_dropped", "phys.centimetres_not_converted", "phys.length_power_three"),
    26: ("phys.weight_as_mass", "phys.deflection_end_factor", "phys.slope_units_not_converted"),
    27: ("phys.percent_wrong_base", "phys.percent_sign_flipped", "phys.one_sided_slope"),
    28: ("phys.period_squared_skipped", "phys.grams_not_converted", "phys.angular_frequency_as_hertz"),
    29: ("phys.beam_full_length", "phys.intercept_sign_flipped", "phys.end_hardware_ignored"),
}


class _Clash(Exception):
    """Two choices came out equal, or the variant is unphysical: the draw is made again."""


def draw(number_, answer, prompt, hint, slips):
    if len({answer, *slips}) != 4:
        raise _Clash
    if len({r"\times" in choice for choice in (answer, *slips)}) != 1:
        raise _Clash  # plain and scientific choices mixed
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number_], slips)],
    )


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 20 (2564)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2564_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2564_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


ROLL_TOPIC = "ท่อกลิ้งบนพื้นเอียง"
DIODE_TOPIC = "หลอดสุญญากาศไดโอด"
LUNG_TOPIC = "กลไกการหายใจ"
BILENS_TOPIC = "การแทรกสอดด้วยไบเลนส์"
BEAM_TOPIC = "คานยื่น"

G = 9.81
HALF = 4 / (3 * pi)
TUBE = "ท่อทรงกระบอกกลวงบาง (I = m′R²)"


def _slope(rng):
    return rng.randint(10, 40), rng.randint(10, 70)


@_type(1, "ความเร่งของท่อกลวงที่กลิ้งเฉียงลงพื้นเอียง", ROLL_TOPIC)
class RollOblique(PhysicsSheet):
    def _variant(self, rng):
        incline, slant = _slope(rng)
        a = q01.solve(incline=incline, slant=slant)
        drive = G * sin(radians(incline))
        return draw(
            1,
            measure(a),
            TUBE + f" กลิ้งโดยไม่ไถลลงพื้นเอียงมุม {incline}° โดยแนวการกลิ้งทำมุม {slant}° กับแนวเอียงสูงสุด ท่อมีความเร่งเชิงเส้นกี่ m/s² (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a=\frac{g\sin\theta\cos\phi}{1+I/(m'R^2)}=\tfrac12g\sin\theta\cos\phi",
            [measure(drive * cos(radians(slant)) / 1.5), measure(drive * sin(radians(slant)) / 2), measure(drive * cos(radians(slant)))],
        )


@_type(2, "สัมประสิทธิ์ความเสียดทานน้อยที่สุดของท่อที่กลิ้งเฉียง", ROLL_TOPIC)
class RollFriction(PhysicsSheet):
    def _variant(self, rng):
        incline, slant = _slope(rng)
        mu = q02.solve(incline=incline, slant=slant)
        t, s2 = tan(radians(incline)), sin(radians(slant)) ** 2
        return draw(
            2,
            measure(mu),
            TUBE + f" กลิ้งลงพื้นเอียงมุม {incline}° โดยแนวการกลิ้งทำมุม {slant}° กับแนวเอียงสูงสุด สัมประสิทธิ์ความเสียดทานสถิตต้องมีค่าอย่างน้อยเท่าใดท่อจึงกลิ้งโดยไม่ไถล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"f_1=\tfrac12m'g\sin\theta\cos\phi,\ f_2=m'g\sin\theta\sin\phi\Rightarrow\mu\ge\tfrac12\tan\theta\sqrt{1+3\sin^2\phi}",
            [measure(t / 2), measure(t * sqrt(1 + 3 * s2)), measure(t / 2 * (1 + 3 * s2))],
        )


def _masses(rng):
    tube = rng.randint(2, 30) / 10
    half = rng.randint(1, 30) / 10
    if tube == half:
        raise _Clash
    return tube, half


LOOSE = "ท่อทรงกระบอกกลวงบางมวล {M} kg (I = m′R²) มีครึ่งทรงกระบอกตันมวล {m} kg สอดอยู่ภายในโดยผิวในท่อลื่น ปล่อยให้กลิ้งโดยไม่ไถลลงพื้นเอียงมุม {t}° เมื่อการแกว่งตอนเริ่มหายไปแล้ว"


@_type(3, "ความเร่งของท่อที่มีครึ่งทรงกระบอกหลวมอยู่ภายใน", ROLL_TOPIC)
class LooseAcceleration(PhysicsSheet):
    def _variant(self, rng):
        tube, half = _masses(rng)
        incline = rng.randint(10, 40)
        a = q03.solve(tube=tube, half=half, incline=incline)
        drive = G * sin(radians(incline))
        return draw(
            3,
            measure(a),
            LOOSE.format(M=f"{tube:g}", m=f"{half:g}", t=incline) + " ท่อมีความเร่งเชิงเส้นกี่ m/s² (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a=\frac{m'+m}{2m'+m}\,g\sin\theta\quad(\text{ครึ่งทรงกระบอกไม่หมุน})",
            [measure(drive / 2), measure((tube + half) / (2 * tube + 1.5 * half) * drive), measure((tube + half) / (2 * half + tube) * drive)],
        )


@_type(4, "มุมเอียงของครึ่งทรงกระบอกในท่อที่กลิ้ง", ROLL_TOPIC)
class LooseTilt(PhysicsSheet):
    def _variant(self, rng):
        tube, half = _masses(rng)
        incline = rng.randint(10, 40)
        beta = q04.solve(tube=tube, half=half, incline=incline)
        t = radians(incline)
        return draw(
            4,
            measure(beta),
            LOOSE.format(M=f"{tube:g}", m=f"{half:g}", t=incline) + " ผิวเรียบของครึ่งทรงกระบอกเอียงทำมุมกี่องศากับแนวระดับ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\beta=\theta-\tan^{-1}\left[\frac{m'}{2m'+m}\tan\theta\right]",
            [measure(incline), measure(degrees(atan(tube / (2 * tube + half) * tan(t)))), measure(degrees(t - atan(tan(t) / 2)))],
        )


WELDED = "ท่อทรงกระบอกกลวงบางมวล {M} kg (I = m′R²) เชื่อมติดกับครึ่งทรงกระบอกตันมวล {m} kg รัศมีเท่ากับท่อ (จุดศูนย์กลางมวลของครึ่งทรงกระบอกห่างแกน 4R/(3π), I ของแผ่นครึ่งวงกลมรอบแกน = ½mR²)"


@_type(5, "มุมพื้นเอียงน้อยที่สุดที่ท่อเชื่อมครึ่งทรงกระบอกกลิ้งลงได้ตลอด", ROLL_TOPIC)
class WeldedStart(PhysicsSheet):
    def _variant(self, rng):
        tube, half = _masses(rng)
        theta = q05.solve(tube=tube, half=half)
        k = HALF * half / (half + tube)
        root = 2.3311223704144226
        return draw(
            5,
            measure(theta),
            WELDED.format(M=f"{tube:g}", m=f"{half:g}") + " วางบนพื้นเอียงโดยผิวเรียบของครึ่งทรงกระบอกขนานแนวระดับแล้วปล่อยจากหยุดนิ่ง พื้นเอียงต้องทำมุมอย่างน้อยกี่องศาจึงกลิ้งลงได้ตลอด (คำตอบของ x = tan(x/2) คือ 2.33 rad, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\sin\theta\ \ge\ k'\,\frac{1-\cos\beta}{\beta}\ \ \forall\beta\Rightarrow\sin\theta_{\min}=k'\sin\theta_0,\quad k'=\frac{mk}{m+m'}",
            [measure(degrees(asin(2 * k / pi))), measure(degrees(asin(HALF * sin(root)))), measure(degrees(asin(k * (1 - cos(root)))))],
        )


def _spin(rng):
    tube, half = _masses(rng)
    radius = rng.randint(5, 20)
    spin = rng.randint(10, 40)
    return tube, half, radius, spin


GROUND = WELDED + " รัศมี R = {R} cm กลิ้งโดยไม่ไถลบนพื้นราบ ขณะครึ่งทรงกระบอกอยู่ด้านล่างระบบมีอัตราเร็วเชิงมุม {w} rad/s"


@_type(6, "พลังงานจลน์ของท่อเชื่อมครึ่งทรงกระบอกที่กลิ้งบนพื้นราบ", ROLL_TOPIC)
class WeldedEnergy(PhysicsSheet):
    def _variant(self, rng):
        tube, half, radius, spin = _spin(rng)
        e = q06.solve(tube=tube, half=half, radius=radius, spin=spin)
        r2w2 = (radius * 1e-2 * spin) ** 2
        return draw(
            6,
            measure(e),
            GROUND.format(M=f"{tube:g}", m=f"{half:g}", R=radius, w=spin) + " ขณะนั้นระบบมีพลังงานจลน์กี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E_k=\tfrac12I_A\omega_0^2=\left[m'+\left(\tfrac34-k\right)m\right]R^2\omega_0^2",
            [measure((tube + (0.75 + HALF) * half) * r2w2), measure(tube * r2w2), measure((tube + 0.75 * half) * r2w2)],
        )


@_type(7, "อัตราเร็วเชิงมุมเมื่อครึ่งทรงกระบอกอยู่ด้านบน", ROLL_TOPIC)
class WeldedTopSpin(PhysicsSheet):
    def _variant(self, rng):
        tube, half, radius, spin = _spin(rng)
        w = q07.solve(tube=tube, half=half, radius=radius, spin=spin)
        r = radius * 1e-2
        kinetic = (tube + (0.75 - HALF) * half) * r * r * spin**2
        lift = 2 * half * G * HALF * r
        below = (tube + (0.75 + HALF) * half) * r * r
        return draw(
            7,
            measure(w),
            GROUND.format(M=f"{tube:g}", m=f"{half:g}", R=radius, w=spin) + " เมื่อกลิ้งจนครึ่งทรงกระบอกอยู่ด้านบน ระบบมีอัตราเร็วเชิงมุมกี่ rad/s (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\omega^2=\frac{\left[m'+\left(\frac34-k\right)m\right]R^2\omega_0^2-2(m+m')gk'R}{\left[m'+\left(\frac34+k\right)m\right]R^2}",
            [measure(sqrt((kinetic + lift) / below)), measure(sqrt((kinetic - lift * (tube + half) / half) / below)), measure(sqrt(kinetic / below))],
        )


@_type(8, "แรงตั้งฉากจากพื้นเมื่อครึ่งทรงกระบอกอยู่ด้านบน", ROLL_TOPIC)
class WeldedNormal(PhysicsSheet):
    def _variant(self, rng):
        tube, half, radius, spin = _spin(rng)
        n = q08.solve(tube=tube, half=half, radius=radius, spin=spin)
        if n <= 0:
            raise _Clash  # the system would leave the ground
        w = q07.solve(tube=tube, half=half, radius=radius, spin=spin)
        weight = (tube + half) * G
        shift = half * HALF * radius * 1e-2 * w * w
        return draw(
            8,
            measure(n),
            GROUND.format(M=f"{tube:g}", m=f"{half:g}", R=radius, w=spin) + " เมื่อกลิ้งจนครึ่งทรงกระบอกอยู่ด้านบน พื้นดันระบบด้วยแรงตั้งฉากกี่นิวตัน (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"N=(m+m')\left(g-k'R\omega^2\right)",
            [measure(weight), measure(weight + shift), measure(weight - shift * (tube + half) / (half * HALF))],
        )


DIODE = "ไดโอดสุญญากาศแบบแผ่นคู่ขนานจัตุรัสด้านละ {a} cm ห่างกัน {d} mm แอโนดมีศักย์ {V} V เทียบกับแคโทด"
CONST = "(e = 1.602×10⁻¹⁹ C, m = 9.109×10⁻³¹ kg, ε₀ = 8.854×10⁻¹² F/m, ตอบเลขนัยสำคัญ 3 ตัว)"


def _diode(rng):
    return rng.randint(2, 10), rng.randint(2, 20), rng.choice((25, 50, 100, 150, 200, 300, 400))


@_type(9, "อัตราเร็วของอิเล็กตรอนตัวเดียวระหว่างขั้วไดโอด", DIODE_TOPIC)
class DiodeElectron(PhysicsSheet):
    def _variant(self, rng):
        _, gap, volts = _diode(rng)
        depth = rng.randint(1, gap * 10 - 1) / 10
        launch = rng.randint(1, 20) * 100
        v = q09.solve(volts=volts, gap=gap, depth=depth, launch=launch)
        gain = q09.solve(volts=volts, gap=gap, depth=depth, launch=0.0)
        return draw(
            9,
            measure(v),
            f"อิเล็กตรอนตัวเดียวหลุดจากแคโทดด้วยอัตราเร็ว {launch} km/s เคลื่อนที่ในสนามสม่ำเสมอระหว่างแผ่นคู่ขนานห่างกัน {gap} mm ที่ต่อความต่างศักย์ {volts} V เมื่อเคลื่อนที่ห่างแคโทด {depth:g} mm มีอัตราเร็วกี่ km/s " + CONST,
            r"\tfrac12mv_x^2=\tfrac12mv_0^2+\frac{exV_d}{d}",
            [measure(gain), measure(q09.solve(volts=volts, gap=gap, depth=gap, launch=launch)), measure(gain + launch)],
        )


@_type(10, "กระแสจำกัดด้วยประจุสเปซของไดโอดสุญญากาศ", DIODE_TOPIC)
class DiodeCurrent(PhysicsSheet):
    def _variant(self, rng):
        side, gap, volts = _diode(rng)
        i = q10.solve(volts=volts, side=side, gap=gap)
        return draw(
            10,
            measure(i),
            DIODE.format(a=side, d=gap, V=volts) + " แคโทดร้อนปล่อยอิเล็กตรอนด้วยความเร็วต้นประมาณศูนย์จนถึงสภาวะคงตัว กระแสผ่านไดโอดเป็นกี่มิลลิแอมแปร์ " + CONST,
            r"V_x=kx^{4/3}\Rightarrow I=\frac{4\epsilon_0a^2}{9d^2}\sqrt{\frac{2e}{m}}\,V_d^{3/2}",
            [measure(i * 9 / 4), measure(i / sqrt(volts)), measure(i * gap * 1e-3)],
        )


@_type(11, "ศักย์ไฟฟ้าระหว่างขั้วของไดโอดที่สภาวะคงตัว", DIODE_TOPIC)
class DiodePotential(PhysicsSheet):
    def _variant(self, rng):
        _, gap, volts = _diode(rng)
        depth = rng.randint(1, gap * 10 - 1) / 10
        v = q11.solve(volts=volts, fraction=depth / gap)
        return draw(
            11,
            measure(v),
            f"ไดโอดสุญญากาศแบบแผ่นคู่ขนานห่างกัน {gap} mm แอโนดมีศักย์ {volts} V ที่สภาวะคงตัวกระแสถูกจำกัดด้วยประจุสเปซ (ศักย์ V_x = kxⁿ) ที่ระยะ {depth:g} mm จากแคโทดศักย์ไฟฟ้าเป็นกี่โวลต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V_x=V_d\left(\frac xd\right)^{4/3}",
            [measure(volts * depth / gap), measure(volts * (depth / gap) ** 0.75), measure(volts * (depth / gap) ** 2)],
        )


@_type(12, "ประจุสเปซทั้งหมดระหว่างขั้วไดโอด", DIODE_TOPIC)
class DiodeCharge(PhysicsSheet):
    def _variant(self, rng):
        side, gap, volts = _diode(rng)
        q = q12.solve(volts=volts, side=side, gap=gap)
        return draw(
            12,
            measure(q),
            DIODE.format(a=side, d=gap, V=volts) + " ที่สภาวะคงตัวกระแสถูกจำกัดด้วยประจุสเปซ ประจุทั้งหมดของอิเล็กตรอนระหว่างแผ่นเป็นกี่นาโนคูลอมบ์ (ε₀ = 8.854×10⁻¹² F/m, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=\int\rho\,a^2dx=-\epsilon_0a^2E_d=-\frac43\,\frac{\epsilon_0a^2V_d}{d}",
            [measure(q * 3 / 4), measure(-q), measure(q / (side * 1e-2) ** 2)],
        )


@_type(13, "ความหนาแน่นประจุที่แผ่นแอโนด", DIODE_TOPIC)
class DiodeSurface(PhysicsSheet):
    def _variant(self, rng):
        _, gap, volts = _diode(rng)
        s = q13.solve(volts=volts, gap=gap)
        return draw(
            13,
            measure(s),
            f"ไดโอดสุญญากาศแบบแผ่นคู่ขนานห่างกัน {gap} mm แอโนดมีศักย์ {volts} V ที่สภาวะคงตัวกระแสถูกจำกัดด้วยประจุสเปซ (สนามที่แคโทดเป็นศูนย์) ความหนาแน่นประจุต่อพื้นที่ที่ผิวแอโนดเป็นกี่ nC/m² (ε₀ = 8.854×10⁻¹² F/m, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E_d=\frac43\,\frac{V_d}{d}\Rightarrow\sigma_+=\frac43\,\frac{\epsilon_0V_d}{d}",
            [measure(-s), measure(s * 3 / 4), measure(s / 2)],
        )


LUNG = "ปอดมีความสัมพันธ์ระหว่างผลต่างความดัน p_D กับปริมาตร V ขณะหายใจเข้าเป็น p_D = (1/k) ln(α/(α − V)) โดย α = {a} L และ k = {k}×10⁻³ Pa⁻¹ หายใจเข้าจนสุดปอดมีปริมาตร {v} L"


def _lung(rng):
    volume = rng.randint(280, 340) / 100
    alpha = round(volume + rng.randint(15, 40) / 100, 2)
    k = rng.choice((0.8, 0.9, 0.964, 1.0, 1.1, 1.2))
    return volume, alpha, k


@_type(14, "ผลต่างความดันเมื่อหายใจเข้าสุดปอด", LUNG_TOPIC)
class LungPressure(PhysicsSheet):
    def _variant(self, rng):
        volume, alpha, k = _lung(rng)
        p = q14.solve(volume=volume, alpha=alpha, k=k)
        return draw(
            14,
            measure(p),
            LUNG.format(a=f"{alpha:g}", k=f"{k:g}", v=f"{volume:g}") + " ขณะนั้นผลต่างความดัน p_D เป็นกี่พาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"p_D=\frac1k\ln\frac{\alpha}{\alpha-V}",
            [measure(p / log(10)), measure(log(alpha / volume) / (k * 1e-3)), measure(p / 1000)],
        )


@_type(15, "งานที่ใช้ขยายเนื้อเยื่อปอดขณะหายใจเข้า", LUNG_TOPIC)
class LungWork(PhysicsSheet):
    def _variant(self, rng):
        volume, alpha, k = _lung(rng)
        w = q15.solve(volume=volume, alpha=alpha, k=k)
        p = q14.solve(volume=volume, alpha=alpha, k=k)
        return draw(
            15,
            measure(w),
            LUNG.format(a=f"{alpha:g}", k=f"{k:g}", v=f"{volume:g}") + " งานที่ใช้ขยายเนื้อเยื่อปอด (dw = p_D dV) ตลอดการหายใจเข้าเป็นกี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"w=\int p_D\,dV=\frac{\alpha}{k}\left[1-e^{-kp_f}\left(1+kp_f\right)\right]",
            [measure(p * volume * 1e-3), measure(p * volume * 1e-3 / 2), measure(alpha / k)],
        )


@_type(16, "พลังงานที่กะบังลมใช้ต่อวัน", LUNG_TOPIC)
class Diaphragm(PhysicsSheet):
    def _variant(self, rng):
        work = rng.randint(15, 40) / 10
        rate = rng.randint(8, 20)
        share = rng.choice((20, 25, 30, 35, 40))
        kcal = q16.solve(work=work, rate=rate, share=share)
        return draw(
            16,
            measure(kcal),
            f"การหายใจเข้าแต่ละครั้งใช้งานขยายเนื้อเยื่อปอด {work:g} J หายใจ {rate} ครั้งต่อนาที ถ้างานนี้เป็น {share}% ของพลังงานที่กล้ามเนื้อกะบังลมใช้ในการหดตัว กะบังลมใช้พลังงานกี่กิโลแคลอรีต่อวัน (1 cal = 4.2 J, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E=\frac{w\times\text{ครั้งต่อวัน}}{\eta}",
            [measure(kcal * share / 100), measure(kcal * (share / 100) ** 2), measure(kcal * 1000)],
        )


@_type(17, "พลังงานภายในของอากาศในปอดที่เพิ่มขึ้น", LUNG_TOPIC)
class LungEnergy(PhysicsSheet):
    def _variant(self, rng):
        volume, alpha, k = _lung(rng)
        u = q17.solve(volume=volume, alpha=alpha, k=k)
        return draw(
            17,
            measure(u),
            LUNG.format(a=f"{alpha:g}", k=f"{k:g}", v=f"{volume:g}") + " อากาศ (แก๊สอะตอมคู่) ที่เต็มปอดต้องได้พลังงานภายในเพิ่มขึ้นกี่จูลเพื่อรักษาความดันไม่ให้ลดลงตามช่องโพรงอก (ความดันบรรยากาศ 101 kPa, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta U=\tfrac52p_0V_f-\tfrac52(p_0-p_D)V_f=\tfrac52p_DV_f",
            [measure(u * 3 / 5), measure(u * 7 / 5), measure(2.5 * 101e3 * volume * 1e-3)],
        )


@_type(18, "ความร้อนที่อากาศในปอดได้รับจากร่างกาย", LUNG_TOPIC)
class LungHeat(PhysicsSheet):
    def _variant(self, rng):
        volume, alpha, k = _lung(rng)
        q = q18.solve(volume=volume, alpha=alpha, k=k)
        u = q17.solve(volume=volume, alpha=alpha, k=k)
        w = q15.solve(volume=volume, alpha=alpha, k=k)
        return draw(
            18,
            measure(q),
            LUNG.format(a=f"{alpha:g}", k=f"{k:g}", v=f"{volume:g}") + " อากาศในปอดได้พลังงานภายในเพิ่ม (5/2)p_DV และทำงานขยายเนื้อเยื่อปอด อากาศได้รับความร้อนจากร่างกายกี่จูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=\Delta U+w,\quad\Delta U=\tfrac52p_DV_f,\quad w=\frac\alpha k\left[1-e^{-kp_f}(1+kp_f)\right]",
            [measure(u - w), measure(u), measure(w)],
        )


@_type(19, "อัตราส่วนความร้อนต่องานสุทธิในการหายใจหนึ่งรอบ", LUNG_TOPIC)
class LungRatio(PhysicsSheet):
    def _variant(self, rng):
        volume, alpha, _ = _lung(rng)
        exhale = round(volume + rng.randint(4, 30) / 100, 2)
        if exhale >= alpha:
            raise _Clash
        r = q19.solve(volume=volume, inhale=alpha, exhale=exhale)
        q = q18.solve(volume=volume, alpha=alpha)
        u = q17.solve(volume=volume, alpha=alpha)
        win = q15.solve(volume=volume, alpha=alpha)
        wout = q15.solve(volume=volume, alpha=exhale, k=1.644)
        if win <= wout:
            raise _Clash
        return draw(
            19,
            measure(r),
            f"ปอดเป็นไปตาม p_D = (1/k) ln(α/(α − V)) หายใจเข้าด้วย α = {alpha:g} L, k = 0.964×10⁻³ Pa⁻¹ และหายใจออกด้วย α = {exhale:g} L, k = 1.644×10⁻³ Pa⁻¹ ระหว่างปริมาตร 0 กับ {volume:g} L อากาศ (อะตอมคู่) ได้ความร้อน Q = (5/2)p_DV + w ขณะหายใจเข้า Q เป็นกี่เท่าของงานสุทธิที่ทำกับเนื้อเยื่อปอดใน 1 รอบ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{Q}{w_I+w_O},\quad w=\pm\frac\alpha k\left[1-e^{-x}(1+x)\right],\ x=\ln\frac{\alpha}{\alpha-V_f}",
            [measure(q / win), measure(u / (win - wout)), measure(q / (win + wout))],
        )


BILENS = "ไบเลนส์ทำจากเลนส์นูนบางสูง {D} mm ความยาวโฟกัส {f} cm ที่ตัดส่วนกลางสูง {a} mm ออกแล้วนำสองส่วนที่เหลือมาประกบกัน"


def _bilens(rng):
    focal = rng.randint(10, 50)
    cut = rng.randint(5, 30) / 10
    height = rng.randint(20, 60)
    return focal, cut, height


@_type(20, "ระยะภาพจากไบเลนส์", BILENS_TOPIC)
class BilensImage(PhysicsSheet):
    def _variant(self, rng):
        focal, cut, height = _bilens(rng)
        source = rng.randint(3, focal - 1)
        v = q20.solve(source=source, focal=focal)
        return draw(
            20,
            measure(v),
            BILENS.format(D=height, f=focal, a=f"{cut:g}") + f" แหล่งกำเนิดแสงจุดอยู่บนแกนห่างไบเลนส์ {source} cm (น้อยกว่าความยาวโฟกัส) ภาพเสมือนอยู่ห่างไบเลนส์กี่เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac1f=\frac1u+\frac1v\Rightarrow|v|=\frac{uf}{f-u}",
            [measure(source * focal / (source + focal)), measure(focal**2 / (focal - source)), measure(v - source)],
        )


@_type(21, "ระยะห่างระหว่างภาพสองภาพจากไบเลนส์", BILENS_TOPIC)
class BilensSeparation(PhysicsSheet):
    def _variant(self, rng):
        focal, cut, height = _bilens(rng)
        source = rng.randint(3, focal - 1)
        d = q21.solve(source=source, focal=focal, cut=cut)
        return draw(
            21,
            measure(d),
            BILENS.format(D=height, f=focal, a=f"{cut:g}") + f" แหล่งกำเนิดแสงจุดอยู่บนแกนห่างไบเลนส์ {source} cm ภาพเสมือนสองภาพที่เกิดจากสองส่วนของไบเลนส์อยู่ห่างกันกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"d=a\left(\frac{|v|}{u}-1\right)=\frac{au}{f-u}",
            [measure(cut * focal / (focal - source)), measure(cut), measure(2 * d)],
        )


@_type(22, "ระยะฉากที่ริ้วการแทรกสอดของไบเลนส์หายไป", BILENS_TOPIC)
class BilensRange(PhysicsSheet):
    def _variant(self, rng):
        focal, cut, height = _bilens(rng)
        lmax = q22.solve(focal=focal, height=height, cut=cut)
        return draw(
            22,
            measure(lmax),
            BILENS.format(D=height, f=focal, a=f"{cut:g}") + " วางแหล่งกำเนิดแสงจุดบนแกนที่จุดโฟกัสแล้วเลื่อนฉากออกห่าง ริ้วการแทรกสอดหายไปเมื่อฉากห่างไบเลนส์กี่เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{D-a}{L_{\max}}=\frac af\Rightarrow L_{\max}=\frac{f(D-a)}{a}",
            [measure(focal * height / cut), measure(lmax / 2), measure(focal * cut / (height - cut))],
        )


@_type(23, "ระยะห่างระหว่างริ้วการแทรกสอดของไบเลนส์", BILENS_TOPIC)
class BilensFringe(PhysicsSheet):
    def _variant(self, rng):
        focal, cut, height = _bilens(rng)
        wavelength = rng.choice((450, 500, 532, 589, 633, 650))
        dx = q23.solve(wavelength=wavelength, focal=focal, cut=cut)
        return draw(
            23,
            measure(dx),
            BILENS.format(D=height, f=focal, a=f"{cut:g}") + f" แหล่งกำเนิดแสงจุดความยาวคลื่น {wavelength} nm อยู่บนแกนที่จุดโฟกัส ริ้วการแทรกสอดบนฉากห่างกันกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta x=\frac{\lambda|v|}{d}=\frac{\lambda f}{a}",
            [measure(dx / 2), measure(2 * dx), measure(dx * cut / (height - cut))],
        )


@_type(24, "จำนวนริ้วการแทรกสอดมากที่สุดของไบเลนส์", BILENS_TOPIC)
class BilensCount(PhysicsSheet):
    def _variant(self, rng):
        focal, cut, height = _bilens(rng)
        wavelength = rng.choice((450, 500, 532, 589, 633, 650))
        n = q24.solve(wavelength=wavelength, focal=focal, height=height, cut=cut)
        return draw(
            24,
            measure(n),
            BILENS.format(D=height, f=focal, a=f"{cut:g}") + f" แหล่งกำเนิดแสงจุดความยาวคลื่น {wavelength} nm อยู่บนแกนที่จุดโฟกัส เมื่อวางฉากที่ระยะที่เหมาะสม จะเห็นริ้วการแทรกสอดได้มากที่สุดประมาณกี่ริ้ว (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"N=\frac{W}{\Delta x}=\frac{(D-a)/2}{\lambda f/a}",
            [measure(2 * n), measure(n * height / (height - cut)), measure(n / 2)],
        )


B_W, B_H, MU = 0.025, 1.75e-3, 0.122
STRIP = "คานอะลูมิเนียมแบนกว้าง 2.5 cm หนา 1.75 mm มวลต่อความยาว 0.122 kg/m ยึดแน่นที่โคนเป็นคานยื่น"


@_type(25, "มอดุลัสของยังจากการโก่งของคานยื่นเปล่า", BEAM_TOPIC)
class BeamSag(PhysicsSheet):
    def _variant(self, rng):
        length = rng.randint(50, 90)
        modulus = rng.randint(55, 75) * 1e9
        sag = round(3 * MU * G * (length * 1e-2) ** 4 / (2 * modulus * B_W * B_H**3) * 100, 1)
        e = q25.solve(length=length, sag=sag)
        return draw(
            25,
            measure(e),
            STRIP + f" ยื่นออกมา {length} cm ปลายคานเปล่าโก่งลงจากแนวระดับ {sag:g} cm เพราะน้ำหนักตัวเอง (Δy = 3μgL⁴/(2Ebh³)) มอดุลัสของยังเป็นกี่จิกะพาสคัล (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E=\frac{3\mu gL^4}{2bh^3\,\Delta y}",
            [measure(e * 2 / 3), measure(e / 100), measure(e / (length * 1e-2))],
        )


MASSES = (0.0, 15.2, 25.6, 36.0, 46.4, 56.8, 67.2, 77.6, 88.0, 98.4, 108.8, 119.2)


@_type(26, "มอดุลัสของยังจากความชันของกราฟการโก่งกับมวล", BEAM_TOPIC)
class BeamSlope(PhysicsSheet):
    def _variant(self, rng):
        modulus = rng.randint(55, 75) * 1e9
        L = 0.6
        base = 3 * MU * G * L**4 / (2 * modulus * B_W * B_H**3)
        slope = 4 * L**3 * G / (modulus * B_W * B_H**3)
        sags = tuple(round((base + slope * m * 1e-3) * 100 + rng.randint(-1, 1) / 10, 1) for m in MASSES)
        e = q26.solve(masses=MASSES, sags=sags)
        table = ", ".join(f"({m:g}, {s:g})" for m, s in zip(MASSES, sags))
        return draw(
            26,
            measure(e),
            STRIP + f" ยื่นออกมา 60 cm แขวนมวล m ที่ปลายแล้ววัดการโก่ง Δy ได้ (m เป็นกรัม, Δy เป็นเซนติเมตร) = {table} จากความชันของกราฟ Δy กับ m (วิธีกำลังสองน้อยที่สุด, ความชัน = 4L³g/(Ebh³)) มอดุลัสของยังเป็นกี่จิกะพาสคัล (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta y=\frac{L^3(3\mu Lg+8mg)}{2Ebh^3}\Rightarrow E=\frac{4L^3g}{bh^3\cdot\text{ความชัน}}",
            [measure(e / G), measure(2 * e), measure(e * 10)],
        )


@_type(27, "เปอร์เซ็นต์ผลต่างความชันของคานยื่นที่โก่งมาก", BEAM_TOPIC)
class BeamNonlinear(PhysicsSheet):
    def _variant(self, rng):
        masses = MASSES[:7]
        base = rng.randint(120, 150) / 10
        slope = rng.randint(28, 34) / 100
        bend = rng.randint(4, 12) / 10000
        sags = tuple(round(base + slope * m - bend * m * m, 1) for m in masses)
        washers = rng.randint(2, 5)
        e = q27.solve(masses=masses, sags=sags, washers=washers)

        def chord(n):
            return (sags[n + 1] - sags[n - 1]) / (masses[n + 1] - masses[n - 1])

        one = (sags[washers] - sags[washers - 1]) / (masses[washers] - masses[washers - 1])
        table = ", ".join(f"({m:g}, {s:g})" for m, s in zip(masses, sags))
        return draw(
            27,
            measure(e),
            f"คานยื่นยาว 90 cm เมื่อแขวนแหวน N = 0 ถึง 6 ตัว วัด (m เป็นกรัม, Δy เป็นเซนติเมตร) = {table} ให้ t_N = (Δy_(N+1) − Δy_(N−1))/(m_(N+1) − m_(N−1)) และ e_N = (t_N − t₁)/t₁ × 100% ค่า e_{washers} เป็นกี่เปอร์เซ็นต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"e_N=\frac{t_N-t_1}{t_1}\times100\%",
            [measure((chord(washers) - chord(1)) / chord(washers) * 100), measure(-e), measure((one - chord(1)) / chord(1) * 100)],
        )


PERIOD_MASSES = (29.19, 39.59, 49.99, 60.39, 70.79, 81.19, 91.59, 101.99, 112.39, 122.79)


def _vibration(rng):
    modulus = rng.randint(65, 80) * 1e9
    share = rng.randint(24, 40) / 100
    L = 0.6
    scale = 16 * pi**2 * L**3 / (modulus * B_W * B_H**3)
    return tuple(round(scale * (share * MU * L + m * 1e-3) * (1 + rng.randint(-15, 15) / 1000), 3) for m in PERIOD_MASSES)


VIBRATE = STRIP + " ยื่นออกมา 60 cm ติดมวล m ที่ปลายแล้ววัดคาบการสั่นพื้นฐาน T ได้ (m เป็นกรัม, T² เป็น s²) = {t} โดย T² = 16π²L³(aμL + m)/(Ebh³)"


@_type(28, "มอดุลัสของยังจากการสั่นของคานยื่น", BEAM_TOPIC)
class BeamVibration(PhysicsSheet):
    def _variant(self, rng):
        squares = _vibration(rng)
        e = q28.solve(masses=PERIOD_MASSES, squares=squares)
        table = ", ".join(f"({m:g}, {s:.3f})" for m, s in zip(PERIOD_MASSES, squares))
        roots = tuple(sqrt(s) for s in squares)
        loose = q28.solve(masses=PERIOD_MASSES, squares=roots)
        return draw(
            28,
            measure(e),
            VIBRATE.format(t=table) + " จากความชันของกราฟ T² กับ m (วิธีกำลังสองน้อยที่สุด) มอดุลัสของยังเป็นกี่จิกะพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E=\frac{16\pi^2L^3}{bh^3\cdot\text{ความชัน}}",
            [measure(loose), measure(e * 1000), measure(e / (4 * pi**2))],
        )


@_type(29, "มวลสมมูลของคานยื่นจากจุดตัดแกน", BEAM_TOPIC)
class BeamShare(PhysicsSheet):
    def _variant(self, rng):
        squares = _vibration(rng)
        a = q29.solve(masses=PERIOD_MASSES, squares=squares)
        table = ", ".join(f"({m:g}, {s:.3f})" for m, s in zip(PERIOD_MASSES, squares))
        bare = q29.solve(masses=tuple(m - 7.84 for m in PERIOD_MASSES), squares=squares)
        return draw(
            29,
            measure(a),
            VIBRATE.format(t=table) + " (m รวมน็อตยาว น็อตหางปลา และแหวน) จากจุดตัดแกน m ของกราฟ T² กับ m (วิธีกำลังสองน้อยที่สุด) ค่าคงตัว a ของมวลสมมูลของคานเป็นเท่าใด (μL = 0.122 kg/m × 0.60 m, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T^2=0\Rightarrow m_0=-a\mu L",
            [measure(a * 0.6), measure(-a), measure(bare)],
        )
