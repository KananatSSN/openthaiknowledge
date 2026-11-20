"""Seeded variants of the reviewed TPhO 17 (2561) national physics olympiad."""

from math import asin, atan, cos, degrees, floor, log10, pi, radians, sin, sqrt, tan

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2561_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11

from otk.sheets.tpho2561_physics import q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22

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
    1: ("phys.launch_angle_from_horizontal", "phys.projectile_range_half", "phys.projectile_sine_cosine_swapped"),
    2: ("phys.bounce_impulse_once", "phys.beam_inertia_about_end", "phys.beam_arm_full_length"),
    3: ("phys.angle_in_degrees_not_radians", "phys.beam_turn_theta_only", "phys.tangent_for_sine"),
    4: ("phys.reflections_ignored", "phys.single_wall_emissivity", "phys.net_flow_doubled"),
    5: ("phys.reflections_ignored", "phys.days_seconds_confused", "phys.ice_area_ends_included"),
    6: ("phys.falling_rod_free_fall", "phys.falling_rod_end_for_centre", "phys.falling_rod_sine_for_cosine"),
    7: ("phys.falling_rod_free_fall", "phys.falling_rod_end_for_centre", "phys.falling_rod_sine_for_cosine"),
    8: ("phys.coil_area_for_circumference", "phys.peak_speed_frequency_dropped", "phys.turns_dropped"),
    9: ("phys.weight_as_mass", "phys.coil_area_for_circumference", "phys.turns_dropped"),
    10: ("phys.weight_as_mass", "phys.watt_balance_ratio_inverted", "phys.millivolts_not_converted"),
    11: ("phys.josephson_factor_dropped", "phys.gigahertz_as_megahertz", "phys.josephson_doubled"),
    12: ("phys.hall_filling_ignored", "phys.hall_filling_multiplied", "phys.hall_planck_reduced"),
    13: ("phys.relative_errors_rooted", "phys.charge_error_included", "phys.frequency_errors_doubled"),
    14: ("phys.pressure_amplitude_doubled", "phys.acoustic_speed_dropped", "phys.acoustic_density_dropped"),
    15: ("phys.sound_isothermal", "phys.sound_gamma_inverted", "phys.sound_gamma_not_rooted"),
    16: ("phys.kinetic_average_dropped", "phys.kinetic_half_missing", "phys.speed_not_squared"),
    17: ("phys.momentum_average_dropped", "phys.momentum_speed_not_divided", "phys.momentum_density_first_order"),
    18: ("phys.radiation_pressure_peak_for_mean", "phys.radiation_pressure_doubled", "phys.radiation_pressure_density_dropped"),
    19: ("phys.reflection_amplitude_not_doubled", "phys.reflection_not_counted", "phys.radiation_pressure_doubled"),
    20: ("phys.repose_ratio_inverted", "phys.repose_diameter_for_radius", "phys.repose_sine_for_tangent"),
    21: ("phys.repose_coefficient_dropped", "phys.repose_tangent_for_sine", "phys.repose_slope_inverted"),
    22: ("phys.packing_water_fraction", "phys.packing_ratio_inverted", "phys.packing_water_over_grains"),
}


class _Clash(Exception):
    """Two choices came out equal, or the variant is unphysical: the draw is made again."""


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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 17 (2561)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2561_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2561_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


BOUNCE_TOPIC = "การกระดอนซ้ำรอยบนคานหมุน"
FLASK_TOPIC = "การแผ่รังสีในภาชนะผนังสองชั้น"
ROD_TOPIC = "การตกของท่อนไม้กับมวลแขวน"
WATT_TOPIC = "ตาชั่งแม่เหล็กไฟฟ้า"
QUANTUM_TOPIC = "มาตรฐานทางไฟฟ้าเชิงควอนตัม"
SOUND_TOPIC = "การยกตัวด้วยเสียง"
RICE_TOPIC = "มุมทรงตัวและความหนาแน่นการอัดของข้าว"

BOUNCE = "คานยาวหมุนรอบจุดหมุนลื่นที่กึ่งกลางด้วยอัตราเร็วเชิงมุมคงตัวในระนาบดิ่ง มวล m กระทบปลายคานด้วยอัตราเร็ว {v} m/s ขณะคานเอียง {t}° กับแนวระดับ แล้วกระดอนไปกระทบปลายอีกข้างและกระดอนกลับไปมาซ้ำรอยเดิม (ชนแบบยืดหยุ่น)"


@_type(1, "ความยาวคานจากวิถีโพรเจกไทล์ของมวลที่กระดอน", BOUNCE_TOPIC)
class BounceLength(PhysicsSheet):
    def _variant(self, rng):
        speed = rng.randint(10, 60) / 10
        angle = rng.randint(10, 60)
        L = q01.solve(speed=speed, angle=angle)
        t = radians(angle)
        return draw(
            1,
            measure(L),
            BOUNCE.format(v=f"{speed:g}", t=angle) + " คานยาวกี่เมตร (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"L\cos\theta_0=\frac{v^2\sin2\theta_0}{g}",
            [measure(2 * speed**2 * cos(t) / 9.8), measure(L / 2), measure(2 * speed**2 * sin(t) * tan(t) / 9.8)],
        )


@_type(2, "อัตราเร็วเชิงมุมของคานที่มวลกระดอนซ้ำรอย", BOUNCE_TOPIC)
class BounceSpin(PhysicsSheet):
    def _variant(self, rng):
        beam = rng.randint(5, 50) / 10
        length = rng.randint(5, 30) / 10
        mass = rng.randint(1, 20) / 20
        speed = rng.randint(10, 60) / 10
        w = q02.solve(beam=beam, length=length, mass=mass, speed=speed)
        return draw(
            2,
            measure(w),
            f"คานมวล {beam:g} kg ยาว {length:g} m หมุนรอบจุดหมุนลื่นที่กึ่งกลาง มวล {mass:g} kg กระทบปลายคานด้วยอัตราเร็ว {speed:g} m/s ในแนวตั้งฉากกับคานแล้วกระดอนกลับด้วยอัตราเร็วเท่าเดิม (ชนแบบยืดหยุ่น คานหมุนกลับทิศด้วยอัตราเร็วเชิงมุมเท่าเดิม) คานหมุนด้วยอัตราเร็วเชิงมุมกี่ rad/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2\cdot\tfrac{1}{12}ML^2\omega=2mv\cdot\tfrac{L}{2}",
            [measure(w / 2), measure(w / 4), measure(2 * w)],
        )


@_type(3, "อัตราส่วนมวลที่ทำให้การกระดอนซ้ำรอย", BOUNCE_TOPIC)
class BounceRatio(PhysicsSheet):
    def _variant(self, rng):
        angle = rng.randint(10, 60)
        ratio = q03.solve(angle=angle)
        t = radians(angle)
        return draw(
            3,
            measure(ratio),
            BOUNCE.format(v="v", t=angle).replace("v m/s", "v") + " ถ้าคานหมุนไป 2θ₀ ระหว่างการกระทบสองครั้งที่ติดกัน อัตราส่วนมวล m/M ของมวลต่อคานเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"ML\omega=6mv,\quad \omega T=2\theta_0,\quad T=\frac{L\cos\theta_0}{v\sin\theta_0}",
            [measure(angle * tan(t) / 3), measure(t * tan(t) / 6), measure(t * sin(t) / 3)],
        )


SIGMA = 5.670373e-8
FLASK = "ภาชนะเก็บน้ำแข็งผนังสองชั้นทรงกระบอก ช่องว่างระหว่างผนังเป็นสุญญากาศ ผนังทั้งสองมีสัมประสิทธิ์การแผ่รังสี (= การดูดกลืน) {e} ผนังนอก {T} °C ผนังในเท่ากับน้ำแข็ง 0 °C (σ = 5.670373×10⁻⁸ W m⁻² K⁻⁴, 0 °C = 273 K)"


@_type(4, "อัตราความร้อนสุทธิผ่านผนังสองชั้นสุญญากาศ", FLASK_TOPIC)
class FlaskFlux(PhysicsSheet):
    def _variant(self, rng):
        e = rng.choice((0.03, 0.05, 0.08, 0.1, 0.15))
        warm = rng.randint(15, 40)
        q = q04.solve(outer=e, inner=e, warm=warm)
        d4 = (warm + 273.0) ** 4 - 273.0**4
        return draw(
            4,
            measure(q),
            FLASK.format(e=f"{e:g}", T=warm) + " อัตราความร้อนสุทธิต่อตารางเมตรที่ผ่านผนังชั้นในเป็นกี่ W/m² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"q=\frac{\varepsilon_1\varepsilon_2\sigma(T_1^4-T_2^4)}{\varepsilon_1+\varepsilon_2-\varepsilon_1\varepsilon_2}",
            [measure(e * e * SIGMA * d4), measure(e * SIGMA * d4), measure(2 * q)],
        )


@_type(5, "เวลาที่น้ำแข็งในภาชนะสุญญากาศละลายหมด", FLASK_TOPIC)
class FlaskMelt(PhysicsSheet):
    def _variant(self, rng):
        ice = rng.randint(2, 10) * 100
        e = rng.choice((0.03, 0.05, 0.08, 0.1))
        warm = rng.randint(20, 40)
        days = q05.solve(ice=ice, emissivity=e, warm=warm)
        q = q04.solve(outer=e, inner=e, warm=warm)
        side = 2 * pi * 0.03 * 0.30
        ends = side + 2 * pi * 0.03**2
        bare = e * e * SIGMA * ((warm + 273.0) ** 4 - 273.0**4)
        return draw(
            5,
            measure(days),
            FLASK.format(e=f"{e:g}", T=warm) + f" ภาชนะสูง 30 cm รัศมี 3.0 cm (ฝาและก้นเป็นฉนวน) บรรจุน้ำแข็ง 0 °C มวล {ice} g ความร้อนแฝง 336 kJ/kg น้ำแข็งละลายหมดในเวลากี่วัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"t=\frac{mL_f}{q\cdot2\pi rh}",
            [measure(ice * 1e-3 * 336e3 / (bare * side) / 86400), measure(days * 24), measure(ice * 1e-3 * 336e3 / (q * ends) / 86400)],
        )


@_type(6, "ความเร่งของจุดกึ่งกลางท่อนไม้ที่ล้มบนพื้นลื่น", ROD_TOPIC)
class RodCentre(PhysicsSheet):
    def _variant(self, rng):
        angle = rng.randint(5, 80)
        a = q06.solve(angle=angle)
        s2 = sin(radians(angle)) ** 2
        return draw(
            6,
            measure(a),
            f"ท่อนไม้สม่ำเสมอเอียงทำมุม {angle}° กับแนวระดับ ปลาย A แตะพื้นระดับลื่นขณะหยุดนิ่งแล้วเริ่มล้ม จุดกึ่งกลางท่อนไม้มีความเร่งในแนวดิ่งกี่เท่าของ g (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Mg-N=Ma,\quad N\tfrac L2\cos\theta=\tfrac{1}{12}ML^2\alpha,\quad a=\tfrac L2\cos\theta\,\alpha",
            [measure(1.0), measure(2 * a), measure(3 * s2 / (1 + 3 * s2))],
        )


@_type(7, "ความเร่งของปลายท่อนไม้ที่ล้มบนพื้นลื่น", ROD_TOPIC)
class RodEnd(PhysicsSheet):
    def _variant(self, rng):
        angle = rng.randint(5, 80)
        a = q07.solve(angle=angle)
        s2 = sin(radians(angle)) ** 2
        return draw(
            7,
            measure(a),
            f"ท่อนไม้สม่ำเสมอเอียงทำมุม {angle}° กับแนวระดับ ปลายล่าง A แตะพื้นระดับลื่นขณะหยุดนิ่งแล้วเริ่มล้ม ปลายบน C มีความเร่งในแนวดิ่งกี่เท่าของ g (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a_C=L\cos\theta\,\alpha=\frac{6g\cos^2\theta}{1+3\cos^2\theta}",
            [measure(1.0), measure(a / 2), measure(6 * s2 / (1 + 3 * s2))],
        )


COIL = "ขดลวดรัศมี {r} cm จำนวน {N} รอบ อยู่ในสนามแม่เหล็กแนวรัศมี B_r"


@_type(8, "สนามแม่เหล็กแนวรัศมีจากอีเอ็มเอฟของขดลวด", WATT_TOPIC)
class WattField(PhysicsSheet):
    def _variant(self, rng):
        amplitude = rng.randint(5, 20) / 10
        period = rng.choice((0.05, 0.08, 0.1, 0.125, 0.2))
        peak = rng.randint(10, 60) * 10
        radius = rng.randint(5, 15)
        turns = rng.choice((50, 100, 200))
        b = q08.solve(amplitude=amplitude, period=period, peak=peak, radius=radius, turns=turns)
        return draw(
            8,
            measure(b),
            COIL.format(r=radius, N=turns) + f" ขดลวดสั่นขึ้นลงแบบฮาร์มอนิกแอมพลิจูด {amplitude:g} mm คาบ {period:g} s วัดอีเอ็มเอฟสูงสุดได้ {peak} mV B_r มีค่ากี่เทสลา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V=2\pi rNB_ru,\quad u_{\max}=\frac{2\pi}{T}A",
            [measure(2 * b / (radius * 1e-2)), measure(b * 2 * pi), measure(b * turns)],
        )


@_type(9, "มวลจากกระแสที่ทำให้ตาชั่งแม่เหล็กไฟฟ้าสมดุล", WATT_TOPIC)
class WattMass(PhysicsSheet):
    def _variant(self, rng):
        current = rng.randint(100, 400) / 100
        field = rng.randint(40, 150) / 1000
        m = q09.solve(current=current, field=field)
        return draw(
            9,
            measure(m),
            COIL.format(r=10, N=100) + f" = {field:g} T ตาชั่งแม่เหล็กไฟฟ้าสมดุลเมื่อกระแส {current:g} A ไหลผ่านขดลวด มวลบนถาดอีกข้างเป็นกี่กิโลกรัม (g = 9.8122567 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mg=IN\,2\pi r\,B_r",
            [measure(m * 9.8122567), measure(m * 0.1 / 2), measure(m / 100)],
        )


@_type(10, "มวลจากการวัดทางไฟฟ้าของตาชั่ง watt balance", WATT_TOPIC)
class WattPower(PhysicsSheet):
    def _variant(self, rng):
        voltage = rng.randint(10, 60) * 10
        current = rng.randint(100, 400) / 100
        speed = rng.randint(20, 120)
        m = q10.solve(voltage=voltage, current=current, speed=speed)
        return draw(
            10,
            measure(m),
            f"ตาชั่งแม่เหล็กไฟฟ้า: เมื่อขดลวดเคลื่อนที่ด้วยอัตราเร็ว {speed} mm/s วัดอีเอ็มเอฟได้ {voltage} mV และกระแสที่ทำให้ตาชั่งสมดุลเป็น {current:g} A มวลเป็นกี่กิโลกรัม (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m=\frac{VI}{ug}",
            [measure(m * 9.8122567), measure(1 / m), measure(m * 1e3)],
        )


@_type(11, "ความต่างศักย์โจเซฟสันจากความถี่", QUANTUM_TOPIC)
class Josephson(PhysicsSheet):
    def _variant(self, rng):
        factor = rng.choice((0.25, 0.5, 1.0))
        frequency = rng.randint(10, 90)
        v = q11.solve(factor=factor, frequency=frequency)
        return draw(
            11,
            measure(v),
            f"ความต่างศักย์จากปรากฏการณ์โจเซฟสันเขียนได้ V = A f h/e โดย A = {factor:g} ถ้าความถี่ f = {frequency} GHz ความต่างศักย์เป็นกี่ไมโครโวลต์ (h = 6.626069×10⁻³⁴ J s, e = 1.602177×10⁻¹⁹ C, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V=A\frac{fh}{e}",
            [measure(v / factor), measure(v / 1000), measure(2 * v)],
        )


@_type(12, "ความต้านทานฮอลล์เชิงควอนตัม", QUANTUM_TOPIC)
class HallResistance(PhysicsSheet):
    def _variant(self, rng):
        filling = rng.randint(1, 6)
        r = q12.solve(filling=filling)
        return draw(
            12,
            measure(r),
            f"ในปรากฏการณ์ฮอลล์เชิงควอนตัมที่ filling factor ν = {filling} ความต้านทานฮอลล์ R = h/(νe²) มีค่ากี่กิโลโอห์ม (h = 6.626069×10⁻³⁴ J s, e = 1.602177×10⁻¹⁹ C, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"R_H=\frac{h}{\nu e^2}",
            [measure(r * filling), measure(r * filling * filling), measure(r / (2 * pi))],
        )


@_type(13, "ความคลาดเคลื่อนสัมพัทธ์ของมวลจาก watt balance", QUANTUM_TOPIC)
class WattError(PhysicsSheet):
    def _variant(self, rng):
        planck = rng.randint(5, 20)
        speed = rng.randint(5, 30) / 10
        gravity = rng.randint(10, 60) / 10
        err = q13.solve(planck=planck, speed=speed, gravity=gravity)
        rooted = sqrt(planck**2 + speed**2 + gravity**2) / 10
        return draw(
            13,
            measure(err),
            f"ตาชั่งแม่เหล็กไฟฟ้าให้ m ∝ f₁f₂h/(ug) ความคลาดเคลื่อนสัมพัทธ์ของ h, u และ g เป็น {planck}×10⁻⁹, {speed:g}×10⁻⁹ และ {gravity:g}×10⁻⁹ ส่วนของความถี่น้อยกว่า 10⁻¹⁵ (e มีความคลาดเคลื่อน 6.1×10⁻⁹) ความคลาดเคลื่อนสัมพัทธ์ของมวลเป็นกี่ ×10⁻⁸ (บวกตรง ๆ, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{\delta m}{m}=\frac{\delta h}{h}+\frac{\delta u}{u}+\frac{\delta g}{g}+\frac{\delta f_1}{f_1}+\frac{\delta f_2}{f_2}",
            [measure(rooted), measure(err + 0.61), measure(err + 0.61 * 2)],
        )


SOUND = "คลื่นเสียงในอากาศความหนาแน่น {rho} kg/m³ อัตราเร็วเสียง {c} m/s"


@_type(14, "แอมพลิจูดคลื่นความดันจากคลื่นความเร็ว", SOUND_TOPIC)
class SoundPressure(PhysicsSheet):
    def _variant(self, rng):
        density = rng.choice((1.1, 1.2, 1.29))
        sound = rng.randint(330, 350)
        velocity = rng.randint(5, 50) * 10
        p = q14.solve(density=density, sound=sound, velocity=velocity)
        vm = velocity * 1e-3
        return draw(
            14,
            measure(p),
            SOUND.format(rho=f"{density:g}", c=sound) + f" อนุภาคอากาศสั่นด้วยแอมพลิจูดความเร็ว {velocity} mm/s แอมพลิจูดคลื่นความดันเป็นกี่พาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{\partial P}{\partial x}=-\rho_0\frac{\partial v}{\partial t}\Rightarrow P_m=\rho_0cv_m",
            [measure(2 * p), measure(density * vm), measure(sound * vm)],
        )


@_type(15, "อัตราเร็วเสียงจากกระบวนการแอเดียแบติก", SOUND_TOPIC)
class SoundSpeed(PhysicsSheet):
    def _variant(self, rng):
        gamma = rng.choice((1.3, 1.4, 5 / 3))
        pressure = rng.randint(80, 110)
        density = rng.randint(100, 140) / 100
        c = q15.solve(gamma=gamma, pressure=pressure, density=density)
        base = pressure * 1e3 / density
        shown = "5/3" if abs(gamma - 5 / 3) < 1e-9 else f"{gamma:g}"
        return draw(
            15,
            measure(c),
            f"อากาศความดัน {pressure} kPa ความหนาแน่น {density:g} kg/m³ เปลี่ยนแปลงแบบแอเดียแบติก P = Kρ^γ โดย γ = {shown} อัตราเร็วเสียงเป็นกี่เมตรต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"c^2=\frac{dP}{d\rho}=\frac{\gamma P_a}{\rho_0}",
            [measure(sqrt(base)), measure(sqrt(base / gamma)), measure(gamma * sqrt(base))],
        )


@_type(16, "ความหนาแน่นพลังงานจลน์เฉลี่ยของคลื่นเสียง", SOUND_TOPIC)
class SoundKinetic(PhysicsSheet):
    def _variant(self, rng):
        density = rng.choice((1.1, 1.2, 1.29))
        velocity = rng.randint(5, 50) * 10
        k = q16.solve(density=density, velocity=velocity)
        return draw(
            16,
            measure(k),
            f"อากาศความหนาแน่น {density:g} kg/m³ สั่นด้วยแอมพลิจูดความเร็ว {velocity} mm/s ในคลื่นเสียง ความหนาแน่นพลังงานจลน์เฉลี่ยเชิงเวลาเป็นกี่ mJ/m³ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\langle K\rangle=\tfrac12\rho_0\langle v^2\rangle=\tfrac14\rho_0v_m^2",
            [measure(2 * k), measure(4 * k), measure(density * velocity * 1e-3 / 4 * 1e3)],
        )


@_type(17, "ความหนาแน่นโมเมนตัมเฉลี่ยของคลื่นเสียง", SOUND_TOPIC)
class SoundMomentum(PhysicsSheet):
    def _variant(self, rng):
        density = rng.choice((1.1, 1.2, 1.29))
        sound = rng.randint(330, 350)
        velocity = rng.randint(5, 50) * 10
        p = q17.solve(density=density, sound=sound, velocity=velocity)
        return draw(
            17,
            measure(p),
            SOUND.format(rho=f"{density:g}", c=sound) + f" อนุภาคอากาศสั่นด้วยแอมพลิจูดความเร็ว {velocity} mm/s ความหนาแน่นโมเมนตัมเฉลี่ยเชิงเวลาในทิศของคลื่นเป็นกี่ ×10⁻⁶ kg m⁻² s⁻¹ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\langle\rho v\rangle=\tfrac12\rho_mv_m=\frac{\rho_0v_m^2}{2c}",
            [measure(2 * p), measure(p * sound), measure(density * velocity * 1e-3 / 2 * 1e6)],
        )


@_type(18, "ความดันเฉลี่ยส่วนเกินอันดับสองของคลื่นเสียง", SOUND_TOPIC)
class SoundMeanPressure(PhysicsSheet):
    def _variant(self, rng):
        amplitude = rng.randint(5, 100)
        density = rng.choice((1.1, 1.2, 1.29))
        sound = rng.randint(330, 350)
        p = q18.solve(amplitude=amplitude, density=density, sound=sound)
        return draw(
            18,
            measure(p),
            f"คลื่นเสียงแอมพลิจูดความดัน {amplitude} Pa ในอากาศ {density:g} kg/m³ อัตราเร็ว {sound} m/s เมื่อคิดพจน์อันดับสอง ความดันเฉลี่ยเชิงเวลาสูงกว่าความดันบรรยากาศกี่มิลลิพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B=\frac{P_m^2}{2\rho_0c^2},\quad\langle P\rangle-P_a=\frac B2",
            [measure(2 * p), measure(4 * p), measure(p * density)],
        )


@_type(19, "แรงผลักของเสียงที่สะท้อนจากผิว", SOUND_TOPIC)
class SoundPush(PhysicsSheet):
    def _variant(self, rng):
        level = rng.choice((110, 115, 120, 125, 130, 135, 140))
        density = rng.choice((1.1, 1.2, 1.29))
        sound = rng.randint(330, 350)
        f = q19.solve(level=level, density=density, sound=sound)
        return draw(
            19,
            measure(f),
            f"เสียงความดัง {level} dB ในอากาศ {density:g} kg/m³ อัตราเร็ว {sound} m/s ตกกระทบตั้งฉากและสะท้อนจากผิวแข็ง เกิดแรงผลักกี่มิลลินิวตันต่อตารางเมตร (เสียงเบาที่สุด 20 µPa ที่ 0 dB, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_0=20\ \mu\text{Pa}\times10^{L/20},\quad \frac Fa=\frac{P_0^2}{\rho_0c^2}",
            [measure(f / 4), measure(f / 2), measure(2 * f)],
        )


@_type(20, "มุมทรงตัวจากความสูงและรัศมีกองข้าว", RICE_TOPIC)
class RiceHeap(PhysicsSheet):
    def _variant(self, rng):
        height = rng.randint(20, 80) / 10
        radius = rng.randint(50, 150) / 10
        a = q20.solve(height=height, radius=radius)
        return draw(
            20,
            measure(a),
            f"กองข้าวรูปกรวยสูง {height:g} cm รัศมีฐาน {radius:g} cm มุมทรงตัวที่สองของข้าวเป็นกี่องศา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tan\alpha_2=\frac{h}{r}",
            [measure(degrees(atan(radius / height))), measure(degrees(atan(height / (2 * radius)))), measure(degrees(asin(height / radius)))],
        )


FILLS = (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1)


@_type(21, "มุมทรงตัวแรกจากมุมวิกฤติของทรงกระบอกบรรจุข้าว", RICE_TOPIC)
class RiceRoll(PhysicsSheet):
    def _variant(self, rng):
        alpha = rng.randint(25, 45)
        const = rng.randint(15, 25) / 100
        angles = tuple(round(degrees(asin(0.508 * eta * sin(radians(alpha)) + const)) + rng.choice((-0.1, 0, 0.1)), 1) for eta in FILLS)
        a = q21.solve(fills=FILLS, angles=angles)
        ys = [sin(radians(t)) for t in angles]
        mx, my = sum(FILLS) / 6, sum(ys) / 6
        slope = sum((x - mx) * (y - my) for x, y in zip(FILLS, ys)) / sum((x - mx) ** 2 for x in FILLS)
        table = ", ".join(f"({e:g}, {t:g}°)" for e, t in zip(FILLS, angles))
        return draw(
            21,
            measure(a),
            "ทรงกระบอกบรรจุข้าวบนพื้นเอียงเริ่มกลิ้งที่มุมวิกฤติ θ_c ตามสมการ sin θ_c = 0.508η sin α₁ + ค่าคงตัว (η = R₁/R) "
            f"วัด (η, θ_c) ได้ {table} จากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) มุมทรงตัวแรก α₁ เป็นกี่องศา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{ความชันของ }\sin\theta_c\text{ กับ }\eta=0.508\sin\alpha_1",
            [measure(degrees(asin(slope))), measure(degrees(atan(slope / 0.508))), measure(degrees(asin(0.508 * slope)))],
        )


@_type(22, "ความหนาแน่นการอัดของข้าว", RICE_TOPIC)
class RicePacking(PhysicsSheet):
    def _variant(self, rng):
        rice = rng.randint(10, 40)
        water = round(rice * rng.randint(35, 45) / 100, 1)
        phi = q22.solve(rice=rice, water=water)
        return draw(
            22,
            measure(phi),
            f"ใส่ข้าวลงขวดถึงขีดปริมาตร {rice} ml แล้วใช้กระบอกฉีดยาเติมน้ำจนเต็มช่องว่างระหว่างเมล็ดพอดี ใช้น้ำ {water:g} ml ความหนาแน่นการอัดของข้าวเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\phi=\frac{V_{\text{ข้าว}}-V_{\text{น้ำ}}}{V_{\text{ข้าว}}}",
            [measure(water / rice), measure(1 / phi), measure(water / (rice - water))],
        )
