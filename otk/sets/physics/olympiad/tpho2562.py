"""Seeded variants of the reviewed TPhO 18 (2562) national physics olympiad."""

from math import exp, floor, log, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2562_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12

from otk.sheets.tpho2562_physics import q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24

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
    1: ("phys.momentum_flux_speed_not_squared", "phys.momentum_flux_halved", "phys.centimetres_not_converted"),
    2: ("phys.hydrostatic_depth_not_squared", "phys.hydrostatic_half_dropped", "phys.hydrostatic_difference_squared"),
    3: ("phys.jump_factor_four_for_eight", "phys.jump_half_dropped", "phys.jump_one_not_subtracted"),
    4: ("phys.jump_loss_k_half", "phys.jump_loss_pressure_head", "phys.jump_loss_potential_dropped"),
    5: ("phys.jet_diameter_as_radius", "phys.hydrostatic_half_dropped", "phys.jump_rim_pi_r"),
    6: ("phys.loss_ratio_inverted", "phys.loss_voltage_not_squared", "phys.loss_over_total_power"),
    7: ("phys.solenoid_length_dropped", "phys.solenoid_circumference_for_area", "phys.solenoid_diameter_for_radius"),
    8: ("phys.mutual_primary_self_inductance", "phys.mutual_secondary_self_inductance", "phys.mutual_arithmetic_mean"),
    9: ("phys.transformer_magnetising_ignored", "phys.transformer_load_current_ignored", "phys.turns_ratio_inverted"),
    10: ("phys.turns_ratio_not_squared", "phys.kilowatts_not_converted", "phys.rms_peak_confused"),
    11: ("phys.flux_distance_not_squared", "phys.flux_dilution_ignored", "phys.sun_hemisphere_area"),
    12: ("phys.binary_separation_as_radius", "phys.binary_one_body_only", "phys.binary_potential_for_kinetic"),
    13: ("phys.self_energy_shell", "phys.self_energy_point_masses", "phys.self_energy_virial_halved"),
    14: ("phys.virial_fallback_constant", "phys.virial_halving_dropped", "phys.kinetic_energy_per_particle_kt"),
    15: ("phys.negative_heat_capacity_sign", "phys.kinetic_three_halves_dropped", "phys.virial_energy_doubled"),
    16: ("phys.central_pressure_fallback_alpha", "phys.central_pressure_surface_gravity", "phys.central_pressure_mean_pressure"),
    17: ("phys.degeneracy_per_particle", "phys.degeneracy_exponent_inverted", "phys.degeneracy_half_ideal"),
    18: ("phys.central_pressure_fallback_alpha", "phys.ignition_factor_two_dropped", "phys.sphere_radius_volume_factor_dropped"),
    19: ("phys.led_log10_used", "phys.celsius_for_kelvin", "phys.ideality_inverted"),
    20: ("phys.led_log10_used", "phys.intercept_sign_flipped", "phys.saturation_first_reading"),
    21: ("phys.series_resistance_total", "phys.ideality_dropped", "phys.led_log10_used"),
    22: ("phys.threshold_as_photon_energy", "phys.linear_in_wavelength", "phys.intercept_sign_flipped"),
    23: ("phys.fill_factor_inverted", "phys.fill_factor_voltage_only", "phys.fill_factor_current_only"),
    24: ("phys.shunt_series_not_subtracted", "phys.shunt_series_added", "phys.slope_not_inverted"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 18 (2562)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2562_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2562_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


JUMP_TOPIC = "ไฮดรอลิกจัมพ์"
GRID_TOPIC = "การส่งพลังงานไฟฟ้าและหม้อแปลง"
STAR_TOPIC = "อุณหภูมิและมวลขั้นต่ำของดาว"
LED_TOPIC = "สมบัติทางไฟฟ้าและแสงของหลอด LED"
PV_TOPIC = "สมบัติโฟโตวอลเทอิกของหลอด LED"

CHANNEL = "น้ำ (ความหนาแน่น 1000 kg/m³) ไหลในท่อหน้าตัดสี่เหลี่ยมกว้าง {w} m เกิดไฮดรอลิกจัมพ์ ก่อนจัมพ์ชั้นน้ำสูง {h} cm ไหลด้วยอัตราเร็ว {v} m/s (ความเร็วสม่ำเสมอทั่วหน้าตัด ไม่คิดความหนืด)"
JUMP = "น้ำ (ความหนาแน่น 1000 kg/m³) ไหลในท่อหน้าตัดสี่เหลี่ยม ก่อนไฮดรอลิกจัมพ์ชั้นน้ำสูง {h} cm ไหลด้วยอัตราเร็ว {v} m/s (ความเร็วสม่ำเสมอทั่วหน้าตัด ไม่คิดความหนืด แรงดันน้ำเป็นแบบของไหลหยุดนิ่ง ไม่คิดความดันบรรยากาศ)"


@_type(1, "โมเมนตัมต่อวินาทีของน้ำที่ไหลเข้าบริเวณจัมพ์", JUMP_TOPIC)
class JumpMomentum(PhysicsSheet):
    def _variant(self, rng):
        width = rng.randint(2, 20) / 10
        depth = rng.randint(5, 50) / 10
        speed = rng.randint(10, 60) / 10
        p = q01.solve(width=width, depth=depth, speed=speed)
        return draw(
            1,
            measure(p),
            CHANNEL.format(w=f"{width:g}", h=f"{depth:g}", v=f"{speed:g}") + " โมเมนตัมของน้ำที่ไหลเข้าบริเวณจัมพ์ต่อหนึ่งหน่วยเวลาเป็นกี่นิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dp}{dt}=\rho Av^2=\rho Lh_1v_1^2",
            [measure(p / speed), measure(p / 2), measure(p * 100)],
        )


@_type(2, "แรงลัพธ์จากความดันน้ำหยุดนิ่งบนบริเวณจัมพ์", JUMP_TOPIC)
class JumpForce(PhysicsSheet):
    def _variant(self, rng):
        width = rng.randint(2, 20) / 10
        before = rng.randint(10, 50) / 10
        after = before + rng.randint(10, 100) / 10
        f = q02.solve(width=width, before=before, after=after)
        h1, h2 = before * 1e-2, after * 1e-2
        base = 1000 * 9.8 * width
        return draw(
            2,
            measure(f),
            f"น้ำ (ความหนาแน่น 1000 kg/m³) ไหลในท่อหน้าตัดสี่เหลี่ยมกว้าง {width:g} m ชั้นน้ำก่อนจัมพ์สูง {before:g} cm หลังจัมพ์สูง {after:g} cm ถ้าแรงดันน้ำบนหน้าตัดทั้งสองเป็นแบบของไหลหยุดนิ่ง (ไม่คิดความดันบรรยากาศ) แรงลัพธ์ที่กระทำต่อน้ำในบริเวณจัมพ์มีขนาดกี่นิวตัน (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=\tfrac12\rho gL\left(h_2^2-h_1^2\right)",
            [measure(base * (h2 - h1)), measure(2 * f), measure(0.5 * base * (h2 - h1) ** 2)],
        )


@_type(3, "ความสูงของน้ำหลังไฮดรอลิกจัมพ์", JUMP_TOPIC)
class JumpDepth(PhysicsSheet):
    def _variant(self, rng):
        depth = rng.randint(5, 50) / 10
        speed = rng.randint(10, 60) / 10
        if speed**2 <= 9.8 * depth * 1e-2:
            raise _Clash  # too slow for a jump
        h2 = q03.solve(depth=depth, speed=speed)
        root4 = sqrt(1 + 4 * speed**2 / (9.8 * depth * 1e-2))
        root8 = sqrt(1 + 8 * speed**2 / (9.8 * depth * 1e-2))
        return draw(
            3,
            measure(h2),
            JUMP.format(h=f"{depth:g}", v=f"{speed:g}") + " ชั้นน้ำหลังจัมพ์สูงกี่เซนติเมตร (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"h_1v_1=h_2v_2,\quad \rho L\left(h_2v_2^2-h_1v_1^2\right)=\tfrac12\rho gL\left(h_1^2-h_2^2\right)",
            [measure(depth / 2 * (root4 - 1)), measure(2 * h2), measure(depth / 2 * root8)],
        )


@_type(4, "พลังงานที่สูญเสียต่อปริมาตรในไฮดรอลิกจัมพ์", JUMP_TOPIC)
class JumpLoss(PhysicsSheet):
    def _variant(self, rng):
        depth = rng.randint(5, 50) / 10
        speed = rng.randint(10, 60) / 10
        if speed**2 <= 9.8 * depth * 1e-2:
            raise _Clash
        loss = q04.solve(depth=depth, speed=speed)
        h1, h2 = depth * 1e-2, q03.solve(depth=depth, speed=speed) * 1e-2
        v2 = speed * h1 / h2
        return draw(
            4,
            measure(loss),
            JUMP.format(h=f"{depth:g}", v=f"{speed:g}") + " ถ้าพลังงานต่อหนึ่งหน่วยปริมาตรของน้ำคือ ½ρv² + ½ρgh (จุดศูนย์กลางมวลของชั้นน้ำอยู่ที่ h/2) พลังงานที่หายไปต่อหนึ่งหน่วยปริมาตรในจัมพ์เป็นกี่ J/m³ (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta E=\frac14\,\frac{\rho g(h_2-h_1)\left(h_2^2+h_1^2\right)}{h_1h_2}",
            [measure(2 * loss), measure(1000 * 9.8 * (h2 - h1) ** 3 / (4 * h1 * h2)), measure(500 * (speed**2 - v2**2))],
        )


@_type(5, "รัศมีของไฮดรอลิกจัมพ์รูปวงกลม", JUMP_TOPIC)
class JumpRadius(PhysicsSheet):
    def _variant(self, rng):
        flow = rng.randint(10, 60)
        diameter = rng.randint(3, 10)
        depth = rng.randint(2, 6)
        v = flow * 1e-6 / (pi * (diameter * 1e-3 / 2) ** 2)
        if 9.8 * (depth * 1e-3) ** 2 / (2 * v**2) > depth * 1e-3 / 5:
            raise _Clash  # the layer must be much thinner than H
        r = q05.solve(flow=flow, diameter=diameter, depth=depth)
        return draw(
            5,
            measure(r),
            f"ลำน้ำจากก๊อกในแนวดิ่งอัตราการไหล {flow} cm³/s มีเส้นผ่านศูนย์กลาง {diameter} mm ขณะกระทบพื้น แผ่เป็นชั้นบาง ๆ ด้วยอัตราเร็วเท่ากับลำน้ำแล้วเกิดไฮดรอลิกจัมพ์รูปวงกลม ชั้นน้ำหลังจัมพ์สูง {depth} mm (หนากว่าชั้นน้ำก่อนจัมพ์มาก) รัศมีของจัมพ์เป็นกี่เซนติเมตร (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"H^2=\frac{2hv^2}{g},\quad Q=2\pi Rhv,\quad v=\frac{4Q}{\pi d^2}",
            [measure(r / 4), measure(r / 2), measure(2 * r)],
        )


@_type(6, "อัตราส่วนกำลังสูญเสียในสายส่งไฟฟ้ากระแสตรง", GRID_TOPIC)
class LineLossDC(PhysicsSheet):
    def _variant(self, rng):
        power = rng.randint(5, 50) / 10
        voltage = rng.choice((110, 220, 230, 240))
        wire = rng.randint(1, 20)
        r = q06.solve(power=power, voltage=voltage, wire=wire)
        return draw(
            6,
            measure(r),
            f"ส่งพลังงานไฟฟ้ากระแสตรงให้โหลดที่ใช้กำลัง {power:g} kW และมีความต่างศักย์ตกคร่อม {voltage} V ผ่านสายไฟความต้านทานรวม {wire} Ω อัตราส่วนของกำลังไฟฟ้าในสายไฟต่อกำลังไฟฟ้าในโหลดเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{P_w}{P_L}=\frac{I^2R_w}{P_L}=\frac{P_LR_w}{V_L^2}",
            [measure(1 / r), measure(r * voltage), measure(r / (1 + r))],
        )


@_type(7, "ความเหนี่ยวนำตัวเองของโซเลนอยด์", GRID_TOPIC)
class SolenoidSelf(PhysicsSheet):
    def _variant(self, rng):
        turns = rng.randint(10, 30)
        diameter = rng.randint(10, 60) / 10
        length = rng.randint(20, 80)
        henry = q07.solve(turns=turns, radius=diameter / 2, length=length)
        r = diameter / 2 * 1e-2
        return draw(
            7,
            measure(henry),
            f"ขดลวดโซเลนอยด์ยาว {length} cm เส้นผ่านศูนย์กลาง {diameter:g} cm (ยาวกว่ารัศมีมาก) พัน {turns} รอบต่อเซนติเมตร ความเหนี่ยวนำตัวเองเป็นกี่มิลลิเฮนรี (μ₀ = 4π×10⁻⁷ T m/A, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"L=\frac{N\phi}{I}=\mu_0n^2\pi r^2\ell",
            [measure(henry / (length * 1e-2)), measure(henry * 2 / r), measure(4 * henry)],
        )


@_type(8, "ความเหนี่ยวนำร่วมของโซเลนอยด์ซ้อนกัน", GRID_TOPIC)
class SolenoidMutual(PhysicsSheet):
    def _variant(self, rng):
        first = rng.randint(5, 20)
        second = rng.randint(21, 60)
        diameter = rng.randint(10, 60) / 10
        length = rng.randint(20, 80)
        m = q08.solve(first=first, second=second, radius=diameter / 2, length=length)
        own1 = q07.solve(turns=first, radius=diameter / 2, length=length)
        own2 = q07.solve(turns=second, radius=diameter / 2, length=length)
        return draw(
            8,
            measure(m),
            f"ขดลวดโซเลนอยด์สองอันซ้อนกันพันเวียนไปทางเดียวกัน ยาว {length} cm เส้นผ่านศูนย์กลาง {diameter:g} cm เท่ากัน ขดลวด 1 พัน {first} รอบต่อเซนติเมตร ขดลวด 2 พัน {second} รอบต่อเซนติเมตร ความเหนี่ยวนำร่วมเป็นกี่มิลลิเฮนรี (μ₀ = 4π×10⁻⁷ T m/A, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"M=\frac{\phi_2}{I_1}=\mu_0n_1n_2\pi r^2\ell=\sqrt{L_1L_2}",
            [measure(own1), measure(own2), measure((own1 + own2) / 2)],
        )


@_type(9, "กระแสในขดลวดปฐมภูมิของหม้อแปลง", GRID_TOPIC)
class TransformerCurrent(PhysicsSheet):
    def _variant(self, rng):
        voltage = rng.choice((110, 220, 230))
        load = rng.randint(20, 200)
        secondary = rng.randint(5, 50) / 100
        step = rng.choice((2, 4, 5, 10, 20))
        mutual = step * secondary
        i = q09.solve(voltage=voltage, load=load, secondary=secondary, mutual=mutual)
        w = 2 * pi * 50
        return draw(
            9,
            measure(i),
            f"หม้อแปลงลดแรงดันความถี่ 50 Hz ขดลวดทุติยภูมิมีความเหนี่ยวนำ {secondary:g} H ความเหนี่ยวนำร่วม {mutual:g} H ต่อกับโหลด {load} Ω ซึ่งมีความต่างศักย์ยังผลคร่อม {voltage} V (ไม่คิดความต้านทานของขดลวด) กระแสยังผลในขดลวดปฐมภูมิเป็นกี่แอมแปร์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"I_LR_L=-i\omega\left(L_LI_L+MI_S\right)\Rightarrow |I_S|=\frac{V_L\sqrt{R_L^2+\omega^2L_L^2}}{\omega MR_L}",
            [measure(voltage / load / step), measure(voltage / (w * mutual)), measure(voltage / load * step)],
        )


@_type(10, "อัตราส่วนกำลังสูญเสียในสายส่งเมื่อใช้หม้อแปลง", GRID_TOPIC)
class LineLossAC(PhysicsSheet):
    def _variant(self, rng):
        ratio = rng.choice((100, 200, 500, 1000))
        voltage = rng.choice((110, 220, 230))
        line = rng.randint(1, 50)
        power = rng.randint(5, 50) / 10
        r = q10.solve(ratio=ratio, voltage=voltage, line=line, power=power)
        return draw(
            10,
            scientific(r),
            f"ส่งไฟฟ้ากระแสสลับผ่านสายส่งความต้านทาน {line} Ω เข้าหม้อแปลงที่มี V_S/V_L = {ratio} (ωL_L ≫ R_L) ให้โหลดตัวต้านทานที่ใช้กำลัง {power:g} kW ที่ความต่างศักย์ยังผล {voltage} V อัตราส่วนของกำลังไฟฟ้าในสายส่งต่อกำลังไฟฟ้าในโหลดเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{P_S}{P_L}=\frac{R_S\left(R_L^2+\omega^2L_L^2\right)}{\omega^2M^2R_L}\approx\frac{R_S}{R_L}\left(\frac{V_L}{V_S}\right)^2",
            [scientific(r * ratio), scientific(r / 1000), scientific(r / 2)],
        )


STAR = "(G = 6.67×10⁻¹¹ N m² kg⁻², k_B = 1.38×10⁻²³ J/K, m_p = 1.67×10⁻²⁷ kg, ตอบเลขนัยสำคัญ 3 ตัว)"


@_type(11, "อุณหภูมิผิวดวงอาทิตย์จากความเข้มแสงที่โลก", STAR_TOPIC)
class SunSurface(PhysicsSheet):
    def _variant(self, rng):
        intensity = rng.randint(10, 20) * 100
        distance = rng.randint(10, 25) / 10
        radius = rng.randint(5, 10)
        t = q11.solve(intensity=intensity, distance=distance, radius=radius)
        ratio = distance * 1e11 / (radius * 1e8)
        return draw(
            11,
            measure(t),
            f"ดาวฤกษ์รัศมี {radius}.0×10⁸ m แผ่รังสีแบบวัตถุดำ ดาวเคราะห์ที่อยู่ห่าง {distance:g}×10¹¹ m วัดความเข้มแสงจากดาวได้ {intensity} W/m² อุณหภูมิผิวของดาวฤกษ์เป็นกี่เคลวิน (σ = 5.67×10⁻⁸ W m⁻² K⁻⁴, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\sigma T^4\,4\pi R^2=I\,4\pi d^2",
            [measure((intensity * ratio / 5.67e-8) ** 0.25), measure((intensity / 5.67e-8) ** 0.25), measure(t * 2**0.25)],
        )


@_type(12, "พลังงานจลน์ของระบบมวลคู่ที่โคจรรอบกัน", STAR_TOPIC)
class BinaryKinetic(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(5, 40) / 10
        radius = rng.randint(5, 50) / 10
        k = q12.solve(mass=mass, radius=radius)
        return draw(
            12,
            scientific(k),
            f"ดาวสองดวงมวล {mass:g}×10³⁰ kg เท่ากัน ดึงดูดกันด้วยแรงโน้มถ่วงและโคจรเป็นวงกลมรัศมี {radius:g}×10¹¹ m รอบจุดศูนย์กลางมวล พลังงานจลน์รวมของระบบเป็นกี่จูล (G = 6.67×10⁻¹¹ N m² kg⁻², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{mv^2}{r}=\frac{Gm^2}{(2r)^2}\Rightarrow K=2\cdot\tfrac12mv^2=\frac{Gm^2}{4r}",
            [scientific(4 * k), scientific(k / 2), scientific(2 * k)],
        )


@_type(13, "พลังงานศักย์โน้มถ่วงของทรงกลมความหนาแน่นสม่ำเสมอ", STAR_TOPIC)
class SphereSelfEnergy(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(5, 40) / 10
        radius = rng.randint(3, 20)
        u = q13.solve(mass=mass, radius=radius)
        return draw(
            13,
            scientific(u),
            f"กลุ่มแก๊สทรงกลมมวล {mass:g}×10³⁰ kg รัศมี {radius}×10⁸ m ความหนาแน่นสม่ำเสมอ พลังงานศักย์โน้มถ่วงของกลุ่มแก๊ส (เป็นศูนย์เมื่อมวลทุกส่วนอยู่ห่างกันเป็นอนันต์) เป็นกี่จูล (G = 6.67×10⁻¹¹ N m² kg⁻², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"U=-\int_0^R\frac{G\,m(r)\,dm}{r}=-\frac{3}{5}\frac{GM^2}{R}",
            [scientific(u * 5 / 6), scientific(u * 5 / 3), scientific(u / 2)],
        )


@_type(14, "อุณหภูมิเฉลี่ยของกลุ่มแก๊สจากทฤษฎีบทไวเรียล", STAR_TOPIC)
class VirialTemperature(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(5, 40) / 10
        radius = rng.randint(3, 20)
        t = q14.solve(mass=mass, radius=radius)
        return draw(
            14,
            scientific(t),
            f"กลุ่มแก๊สไฮโดรเจนทรงกลมมวล {mass:g}×10³⁰ kg รัศมี {radius}×10⁸ m ความหนาแน่นสม่ำเสมอ ยึดกันด้วยแรงโน้มถ่วงเท่านั้นและเป็นแก๊สอุดมคติ ใช้ทฤษฎีบทไวเรียล (P.E. = −2 K.E.) อุณหภูมิเฉลี่ยของกลุ่มแก๊สเป็นกี่เคลวิน " + STAR,
            r"\tfrac32\frac{M}{m_p}k_BT=\tfrac12\cdot\frac35\frac{GM^2}{R}",
            [scientific(t * 5 / 6), scientific(2 * t), scientific(1.5 * t)],
        )


@_type(15, "อัตราการเปลี่ยนพลังงานรวมเทียบกับอุณหภูมิของกลุ่มแก๊ส", STAR_TOPIC)
class VirialHeatCapacity(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(1, 60) / 10
        c = q15.solve(mass=mass)
        return draw(
            15,
            scientific(c),
            f"กลุ่มแก๊สไฮโดรเจนมวล {mass:g}×10³⁰ kg ยึดกันด้วยแรงโน้มถ่วงเท่านั้นและเป็นแก๊สอุดมคติ ใช้ทฤษฎีบทไวเรียล (P.E. = −2 K.E.) อัตราการเปลี่ยนแปลงพลังงานรวมของกลุ่มแก๊สเทียบกับอุณหภูมิ dE/dT เป็นกี่ J/K " + STAR,
            r"E=K+U=-K=-\tfrac32\frac{M}{m_p}k_BT",
            [scientific(-c), scientific(c / 1.5), scientific(2 * c)],
        )


@_type(16, "ความดันที่ใจกลางทรงกลมแก๊สจากแรงโน้มถ่วง", STAR_TOPIC)
class CentralPressure(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(5, 40) / 10
        radius = rng.randint(3, 20)
        p = q16.solve(mass=mass, radius=radius)
        return draw(
            16,
            scientific(p),
            f"กลุ่มแก๊สทรงกลมมวล {mass:g}×10³⁰ kg รัศมี {radius}×10⁸ m ความหนาแน่นสม่ำเสมอ ความดันที่จุดศูนย์กลางเนื่องจากแรงโน้มถ่วงของกลุ่มแก๊สเป็นกี่พาสคัล (G = 6.67×10⁻¹¹ N m² kg⁻², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dP}{dr}=-\rho\,\frac{4}{3}\pi G\rho r\Rightarrow P_c=\frac23\pi G\rho^2R^2=\frac12\frac{GM\rho}{R}",
            [scientific(p * 1.2), scientific(2 * p), scientific(p * 0.4)],
        )


DEGENERACY = "ความดัน degeneracy ของอิเล็กตรอนคือ P_deg = 2.4×10⁻³⁸ (N/V)^(5/3) Pa และความดันแก๊สอุดมคติ P_ideal = (N/V)k_BT"


@_type(17, "ความหนาแน่นจำนวนอะตอมที่กลุ่มแก๊สเริ่มฟิวชันได้", STAR_TOPIC)
class IgnitionDensity(PhysicsSheet):
    def _variant(self, rng):
        temperature = rng.choice((5, 8, 10, 12, 15, 20, 30))
        n = q17.solve(temperature=temperature)
        ratio = 1.38e-23 * temperature * 1e6 / 2.4e-38
        return draw(
            17,
            scientific(n),
            f"กลุ่มแก๊สไฮโดรเจนยุบตัวด้วยแรงโน้มถ่วง {DEGENERACY} กลุ่มแก๊สที่เบาที่สุดที่ยังร้อนถึง {temperature}×10⁶ K ได้ จะถึงอุณหภูมินี้เมื่อ P_deg = P_ideal ที่ความหนาแน่นจำนวนอะตอม N/V กี่อะตอมต่อลูกบาศก์เมตร (k_B = 1.38×10⁻²³ J/K, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2.4\times10^{-38}\left(\frac NV\right)^{5/3}=\frac NVk_BT\Rightarrow\frac NV=\left(\frac{k_BT}{K}\right)^{3/2}",
            [scientific(ratio**0.6), scientific(ratio ** (2 / 3)), scientific((ratio / 2) ** 1.5)],
        )


@_type(18, "มวลน้อยที่สุดของกลุ่มแก๊สที่จุดฟิวชันได้", STAR_TOPIC)
class IgnitionMass(PhysicsSheet):
    def _variant(self, rng):
        temperature = rng.choice((5, 8, 10, 12, 15, 20, 30))
        m = q18.solve(temperature=temperature)
        return draw(
            18,
            scientific(m),
            f"กลุ่มแก๊สไฮโดรเจนทรงกลมความหนาแน่นสม่ำเสมอยุบตัวด้วยแรงโน้มถ่วง ความดันที่ใจกลาง P_grav = ½GMρ/R ถูกต้านด้วย P_ideal + P_deg โดย{DEGENERACY} มวลน้อยที่สุดที่กลุ่มแก๊สยุบตัวจนอุณหภูมิถึง {temperature}×10⁶ K เพื่อจุดฟิวชันได้เป็นกี่กิโลกรัม " + STAR,
            r"k_BT=CN^{1/3}V^{-1/3}-K\left(\frac NV\right)^{2/3}\le\frac{C^2}{4K},\quad C=\tfrac12G\left(\tfrac{4\pi}{3}\right)^{1/3}m_p^{4/3}M^{2/3}",
            [scientific(q18.solve(temperature=temperature, alpha=0.6)), scientific(m / 2**1.5), scientific(m * (4 * pi / 3) ** 0.5)],
        )


THERMAL = 1.38e-23 * 300 / 1.6e-19


def _reading(current):
    """A current rounded to three significant figures, as the meter shows it."""
    return float(f"{current:.2e}")


def _diode(rng):
    """A green LED's ideality factor, saturation current and four readings."""
    ideality = rng.randint(20, 40) / 10
    saturation = rng.randint(1, 9) * 10.0 ** -rng.randint(15, 19)
    start = round(ideality * THERMAL * log(3e-5 / saturation) / 0.05) * 0.05
    volts = tuple(round(start + 0.1 * k, 2) for k in range(4))
    amps = tuple(_reading(saturation * exp(v / (ideality * THERMAL))) for v in volts)
    return ideality, saturation, volts, amps


def _table(volts, amps):
    return ", ".join(f"({v:.2f} V, {stated(i)} A)" for v, i in zip(volts, amps))


LED = "วัดกระแส I ผ่านหลอด LED สีเขียวที่ความต่างศักย์ V ช่วงกระแสน้อยซึ่ง I ≈ I₀ exp(eV/(nkT)) ได้ (V, I) = {t} (e = 1.60×10⁻¹⁹ C, k = 1.38×10⁻²³ J/K, T = 300 K)"


@_type(19, "แฟกเตอร์อุดมคติของ LED จากกราฟ ln I กับ V", LED_TOPIC)
class LedIdeality(PhysicsSheet):
    def _variant(self, rng):
        _, _, volts, amps = _diode(rng)
        n = q19.solve(volts=volts, amps=amps)
        return draw(
            19,
            measure(n),
            LED.format(t=_table(volts, amps)) + " จากความชันของกราฟ ln I กับ V (วิธีกำลังสองน้อยที่สุด) แฟกเตอร์อุดมคติ n เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\ln I=\ln I_0+\frac{e}{nkT}V",
            [measure(n * log(10)), measure(n * 300 / 27), measure(1 / n)],
        )


@_type(20, "กระแสอิ่มตัวย้อนกลับของ LED จากจุดตัดแกน", LED_TOPIC)
class LedSaturation(PhysicsSheet):
    def _variant(self, rng):
        _, _, volts, amps = _diode(rng)
        i0 = q20.solve(volts=volts, amps=amps)
        intercept = log(i0)
        return draw(
            20,
            scientific(i0),
            LED.format(t=_table(volts, amps)) + " จากจุดตัดแกนตั้งของกราฟ ln I กับ V (วิธีกำลังสองน้อยที่สุด) กระแสอิ่มตัวย้อนกลับ I₀ เป็นกี่แอมแปร์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\ln I=\ln I_0+\frac{e}{nkT}V,\quad I_0=e^{\text{จุดตัด}}",
            [scientific(10**intercept), scientific(exp(-intercept)), scientific(amps[0])],
        )


@_type(21, "ความต้านทานอนุกรมภายในของ LED", LED_TOPIC)
class LedSeries(PhysicsSheet):
    def _variant(self, rng):
        ideality, saturation, _, _ = _diode(rng)
        amps = rng.randint(10, 40) / 100
        series = rng.randint(3, 20) / 10
        volts = round(ideality * THERMAL * log(amps / saturation) + amps * series, 2)
        rs = q21.solve(volts=volts, amps=amps, ideality=ideality, saturation=saturation)
        drop = THERMAL * log(amps / saturation)
        return draw(
            21,
            measure(rs),
            f"จากกราฟ ln I กับ V ของหลอด LED สีเขียวในช่วงกระแสน้อยได้ n = {ideality:g} และ I₀ = {stated(saturation)} A ที่กระแสสูง {amps:g} A วัดความต่างศักย์ได้ {volts:.2f} V ซึ่งเบี่ยงเบนจากเส้นตรงเพราะ I ≈ I₀ exp(e(V − IR_s)/(nkT)) ความต้านทานอนุกรมภายใน R_s เป็นกี่โอห์ม (e = 1.60×10⁻¹⁹ C, k = 1.38×10⁻²³ J/K, T = 300 K, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"R_s=\frac{V-\frac{nkT}{e}\ln\frac{I}{I_0}}{I}",
            [measure(volts / amps), measure((volts - drop) / amps), measure((volts - ideality * drop / log(10)) / amps)],
        )


@_type(22, "ความยาวคลื่นของ LED อินฟราเรดจากความต่างศักย์ขีดเริ่ม", LED_TOPIC)
class LedInfrared(PhysicsSheet):
    def _variant(self, rng):
        offset = rng.randint(20, 50) / 100
        target = rng.randint(780, 980)
        hc = 6.63e-34 * 3.00e8 / 1.60e-19 * 1e9  # V nm
        thresholds = tuple(round(hc / x - offset, 2) for x in q22.LAMBDAS)
        infrared = round(hc / target - offset, 2)
        lam = q22.solve(thresholds=thresholds, infrared=infrared)
        inv = [1 / x for x in q22.LAMBDAS]
        mx, my = sum(inv) / 5, sum(thresholds) / 5
        slope = sum((x - mx) * (y - my) for x, y in zip(inv, thresholds)) / sum((x - mx) ** 2 for x in inv)
        intercept = my - slope * mx
        lx = sum(q22.LAMBDAS) / 5
        lin = sum((x - lx) * (y - my) for x, y in zip(q22.LAMBDAS, thresholds)) / sum((x - lx) ** 2 for x in q22.LAMBDAS)
        table = ", ".join(f"({x:g} nm, {v:.2f} V)" for x, v in zip(q22.LAMBDAS, thresholds))
        return draw(
            22,
            measure(lam),
            f"ความต่างศักย์ขีดเริ่มของ LED เป็นไปตาม eV_t = hc/λ − E₀ โดย E₀ เท่ากันทุกหลอด วัด (λ, V_t) ของ LED สีม่วง น้ำเงิน เขียว ส้ม และแดงได้ {table} ถ้า LED อินฟราเรดมี V_t = {infrared:.2f} V จากกราฟเส้นตรงของ V_t กับ 1/λ (วิธีกำลังสองน้อยที่สุด) LED อินฟราเรดให้ความยาวคลื่นกี่นาโนเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V_t=\frac{hc}{e}\cdot\frac1\lambda-\frac{E_0}{e}",
            [measure(hc / infrared), measure(lx + (infrared - my) / lin), measure(slope / (infrared + intercept))],
        )


CELL = "ใช้ LED สีม่วงส่องแสงให้ LED สีเขียวซึ่งทำหน้าที่เป็นเซลล์โฟโตวอลเทอิก"


@_type(23, "ฟิลแฟกเตอร์ของ LED ที่ใช้เป็นเซลล์โฟโตวอลเทอิก", PV_TOPIC)
class CellFillFactor(PhysicsSheet):
    def _variant(self, rng):
        open_volts = rng.randint(160, 200) / 100
        short_ma = rng.randint(30, 60) / 100
        volts = round(open_volts * rng.randint(70, 85) / 100, 2)
        ma = round(short_ma * rng.randint(75, 90) / 100, 3)
        ff = q23.solve(open_volts=open_volts, short_ma=short_ma, volts=volts, ma=ma)
        return draw(
            23,
            measure(ff),
            CELL + f" จากกราฟ I-V ได้ V_OC = {open_volts:.2f} V, I_SC = {short_ma:.2f} mA และกำลังสูงสุดเกิดที่ {volts:.2f} V, {ma:.3f} mA ฟิลแฟกเตอร์ FF เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"FF=\frac{P_{\max}}{V_{OC}I_{SC}}",
            [measure(1 / ff), measure(volts / open_volts), measure(ma / short_ma)],
        )


@_type(24, "ความต้านทานขนานของ LED ที่ใช้เป็นเซลล์โฟโตวอลเทอิก", PV_TOPIC)
class CellShunt(PhysicsSheet):
    def _variant(self, rng):
        series = rng.randint(2, 15) / 10
        shunt = rng.randint(10, 60)
        short_ma = rng.randint(30, 60) / 100
        v2 = rng.choice((0.5, 0.6, 0.7))
        first = (0.10, round(short_ma - 0.10 / (shunt + series), 4))
        second = (v2, round(short_ma - v2 / (shunt + series), 4))
        r = q24.solve(first=first, second=second, series=series)
        slope = (second[1] - first[1]) / (second[0] - first[0])
        return draw(
            24,
            measure(r),
            CELL + f" ในช่วงความต่างศักย์น้อย (V < V_OC/2) ซึ่ง dI/dV ≈ −1/(R_SH + R_S) วัดได้ ({first[0]:.2f} V, {first[1]:.4f} mA) และ ({second[0]:.2f} V, {second[1]:.4f} mA) ถ้าความชันใกล้ V_OC ให้ R_S = {series:g} kΩ ความต้านทานขนาน R_SH เป็นกี่กิโลโอห์ม (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"R_{SH}=-\frac{\Delta V}{\Delta I}-R_S",
            [measure(r + series), measure(r + 2 * series), measure(-slope)],
        )
