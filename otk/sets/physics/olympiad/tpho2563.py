"""Seeded variants of the reviewed TPhO 19 (2563) national physics olympiad."""

from math import exp, floor, log, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2563_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2563_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

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
    1: ("phys.strobe_drop_period_only", "phys.strobe_drop_speed_gh", "phys.strobe_ratio_inverted"),
    2: ("phys.strobe_ratio_not_squared", "phys.strobe_true_acceleration", "phys.strobe_drop_period_only"),
    3: ("phys.strobe_terminal_speed_not_divided", "phys.angular_for_ordinary_frequency", "phys.amplitude_peak_to_peak"),
    4: ("phys.deviation_one_face", "phys.deviation_index_not_divided", "phys.deviation_wrong_beam"),
    5: ("phys.photon_energy_as_momentum", "phys.milliwatts_not_converted", "phys.photon_energy_hc_times_lambda"),
    6: ("phys.deviation_one_face", "phys.force_full_momentum_flux", "phys.deviation_index_not_divided"),
    7: ("phys.two_beams_counted_once", "phys.angular_frequency_as_hertz", "phys.deviation_index_not_divided"),
    8: ("phys.adiabatic_exponent_gamma", "phys.celsius_for_kelvin", "phys.adiabatic_exponent_cv"),
    9: ("phys.adiabatic_exponent_cv", "phys.lapse_isothermal_factor", "phys.molar_mass_grams"),
    10: ("phys.celsius_for_kelvin", "phys.adiabatic_exponent_gamma", "phys.adiabatic_exponent_cv"),
    11: ("phys.condensation_ignored", "phys.latent_heat_sign_flipped", "phys.moist_rate_half"),
    12: ("phys.condensation_ignored", "phys.latent_heat_sign_flipped", "phys.moist_rate_half"),
    13: ("phys.lens_factor_four_dropped", "phys.lens_newtonian_deflection", "phys.lens_distance_sum"),
    14: ("phys.lens_angle_wrong_distance", "phys.lens_factor_four_dropped", "phys.lens_newtonian_deflection"),
    15: ("phys.ring_diameter_for_radius", "phys.lens_distance_not_subtracted", "phys.lens_distances_swapped"),
    16: ("phys.friction_one_face", "phys.weight_as_mass", "phys.friction_largest_pull"),
    17: ("phys.friction_one_face", "phys.weight_as_mass", "phys.friction_line_through_origin"),
    18: ("phys.intercept_sign_flipped", "phys.intercept_on_wrong_axis", "phys.intercept_first_reading"),
    19: ("phys.led_log10_used", "phys.sqrt_gap_dropped", "phys.gap_not_inverted"),
    20: ("phys.sheets_not_squared", "phys.millimetres_not_converted", "phys.amplification_factor_two_dropped"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 19 (2563)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2563_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2563_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


STROBE_TOPIC = "หยดน้ำใต้ไฟกระพริบ"
TWEEZER_TOPIC = "แหนบเชิงแสง"
LAPSE_TOPIC = "อัตราการลดลงของอุณหภูมิตามความสูง"
LENS_TOPIC = "เลนส์แรงโน้มถ่วง"
BOOK_TOPIC = "แรงเสียดทานของสมุดที่สอดสลับกัน"

STROBE = "ในห้องมืด น้ำหยดจากก๊อกด้วยความเร็วต้นศูนย์ทุก ๆ {T} s ไฟกระพริบสว่างสั้น ๆ ด้วยคาบ {T} s {sign} {lag} ms (ไม่คิดแรงต้านอากาศ)"


def _lag(rng):
    lag = rng.choice((-3.0, -2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.0, 3.0))
    return lag, ("+" if lag > 0 else "−"), f"{abs(lag):g}"


@_type(1, "ความเร็วปรากฏของหยดน้ำใต้ไฟกระพริบ", STROBE_TOPIC)
class StrobeVelocity(PhysicsSheet):
    def _variant(self, rng):
        height = rng.randint(10, 80)
        interval = rng.choice((0.02, 0.04, 0.05, 0.08, 0.1))
        lag, sign, size = _lag(rng)
        u = q01.solve(height=height, interval=interval, lag=lag)
        true = sqrt(2 * 9.8 * height * 1e-2) * 1e2
        dt = lag * 1e-3
        return draw(
            1,
            measure(u),
            STROBE.format(T=f"{interval:g}", sign=sign, lag=size) + f" หยดน้ำที่อยู่ต่ำจากปลายก๊อก {height} cm มีความเร็วปรากฏกี่ cm/s (ทิศลงเป็นบวก, g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"s_n=u\,n\Delta t+\tfrac12g(n\Delta t)^2,\ t=n(T_0+\Delta t)\Rightarrow u'=\frac{\sqrt{2gh}\,\Delta t}{T_0+\Delta t}",
            [measure(true * dt / interval), measure(true / sqrt(2) * dt / (interval + dt)), measure(true * (interval + dt) / dt)],
        )


@_type(2, "ความเร่งปรากฏของหยดน้ำใต้ไฟกระพริบ", STROBE_TOPIC)
class StrobeAcceleration(PhysicsSheet):
    def _variant(self, rng):
        interval = rng.choice((0.02, 0.04, 0.05, 0.08, 0.1))
        lag, sign, size = _lag(rng)
        a = q02.solve(interval=interval, lag=lag)
        dt = lag * 1e-3
        return draw(
            2,
            measure(a),
            STROBE.format(T=f"{interval:g}", sign=sign, lag=size) + " หยดน้ำปรากฏเคลื่อนที่ด้วยความเร่งปรากฏขนาดกี่ mm/s² (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a'=g\left(\frac{\Delta t}{T_0+\Delta t}\right)^2",
            [measure(abs(9.8e3 * dt / (interval + dt))), measure(9.8e3), measure(9.8e3 * (dt / interval) ** 2)],
        )


@_type(3, "แอมพลิจูดปรากฏของหยดน้ำเมื่อคาบไฟกระพริบแกว่ง", STROBE_TOPIC)
class StrobeAmplitude(PhysicsSheet):
    def _variant(self, rng):
        spacing = rng.randint(5, 30)
        interval = rng.choice((0.01, 0.02, 0.025, 0.04))
        swing = rng.choice((0.02, 0.05, 0.1, 0.2))
        period = rng.choice((5, 8, 10, 12, 15, 20))
        a = q03.solve(spacing=spacing, interval=interval, swing=swing, period=period)
        return draw(
            3,
            measure(a),
            f"ในห้องมืด หยดน้ำตกด้วยความเร็วสุดท้ายแล้ว ระยะระหว่างหยด {spacing} cm หยดห่างกัน T₀ = {interval:g} s ไฟกระพริบด้วยคาบ T₀ + τ sin ωt โดย τ = {swing:g} ms และการแกว่งของคาบมีคาบ 2π/ω = {period} s (ช้ากว่าการหยดมาก) หยดน้ำปรากฏเคลื่อนที่ขึ้นลงด้วยแอมพลิจูดกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"u'\approx\frac{u_0\tau\sin\omega t}{T_0},\quad A=\frac{u_0\tau}{\omega T_0}=\frac{d_0\tau}{T_0^2\omega}",
            [measure(a * interval), measure(a * 2 * pi), measure(2 * a)],
        )


BEAD = "ลูกแก้วทรงกลมรัศมี {R} µm ดัชนีหักเห {n} ลำแสงเลเซอร์ลำเล็กขนานกันอยู่ที่ x = ±{a} µm จุดศูนย์กลางลูกแก้วอยู่ที่ x = {x} µm (x < a ≪ R อากาศมีดัชนีหักเห 1)"


def _bead(rng):
    index = rng.choice((1.4, 1.45, 1.5, 1.55, 1.6))
    radius = rng.randint(20, 100)
    beam = rng.randint(2, 6)
    shift = rng.randint(1, 2 * beam - 1) / 2
    return index, radius, beam, shift


@_type(4, "มุมเบี่ยงเบนของแสงผ่านลูกแก้วทรงกลม", TWEEZER_TOPIC)
class BeadDeviation(PhysicsSheet):
    def _variant(self, rng):
        index, radius, beam, shift = _bead(rng)
        d = q04.solve(index=index, beam=beam, shift=shift, radius=radius)
        return draw(
            4,
            measure(d),
            BEAD.format(R=radius, n=f"{index:g}", a=beam, x=f"{shift:g}") + " ลำแสงที่ x = +a ผ่านลูกแก้วแล้วเบี่ยงเบนไปกี่มิลลิเรเดียน (ใช้ sin θ ≈ θ, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\theta=\frac{a-x}{R},\quad\delta=2\left(\theta-\frac\theta n\right)=2\,\frac{n-1}{n}\,\frac{a-x}{R}",
            [measure(d / 2), measure(d * index), measure(d * (beam + shift) / (beam - shift))],
        )


@_type(5, "จำนวนโฟตอนของลำแสงเลเซอร์", TWEEZER_TOPIC)
class PhotonCount(PhysicsSheet):
    def _variant(self, rng):
        power = rng.randint(1, 100)
        wavelength = rng.choice((405, 532, 633, 780, 830, 1064))
        time = rng.randint(1, 50)
        count = q05.solve(power=power, wavelength=wavelength, time=time)
        return draw(
            5,
            scientific(count),
            f"แสงเลเซอร์กำลัง {power} mW ความยาวคลื่น {wavelength} nm ในช่วงเวลา {time} ns มีโฟตอนเข้าสู่ลูกแก้วกี่ตัว (h = 6.63×10⁻³⁴ J s, c = 3.00×10⁸ m/s, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"N=\frac{P\,\Delta t}{hc/\lambda}",
            [scientific(count * 3.00e8), scientific(count * 1e3), scientific(count / (wavelength * 1e-9) ** 2)],
        )


@_type(6, "แรงที่ลำแสงเลเซอร์กระทำต่อลูกแก้ว", TWEEZER_TOPIC)
class BeadForce(PhysicsSheet):
    def _variant(self, rng):
        index, radius, beam, shift = _bead(rng)
        power = rng.randint(5, 100)
        f = q06.solve(power=power, index=index, beam=beam, shift=shift, radius=radius)
        return draw(
            6,
            measure(f),
            BEAD.format(R=radius, n=f"{index:g}", a=beam, x=f"{shift:g}") + f" ลำแสงแต่ละลำมีกำลัง {power} mW และผ่านลูกแก้วได้ทั้งหมด ลำแสงที่ x = +a ผลักลูกแก้วในแนวแกน x ด้วยแรงกี่พิโคนิวตัน (c = 3.00×10⁸ m/s, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F_x=\frac Pc\sin\delta\approx2\,\frac Pc\,\frac{n-1}{n}\,\frac{a-x}{R}",
            [measure(f / 2), measure(power * 1e-3 / 3.00e8 * 1e12), measure(f * index)],
        )


@_type(7, "ความถี่เชิงมุมของลูกแก้วในแหนบเชิงแสง", TWEEZER_TOPIC)
class TweezerFrequency(PhysicsSheet):
    def _variant(self, rng):
        power = rng.randint(5, 100)
        index = rng.choice((1.4, 1.45, 1.5, 1.55, 1.6))
        radius = rng.randint(2, 10)
        density = rng.choice((1050, 2200, 2500))
        w = q07.solve(power=power, index=index, radius=radius, density=density)
        return draw(
            7,
            measure(w),
            f"ลูกแก้วทรงกลมรัศมี {radius} µm ความหนาแน่น {density} kg/m³ ดัชนีหักเห {index:g} ถูกจับด้วยลำแสงเลเซอร์ขนานสองลำ ลำละ {power} mW ที่ห่างแกนกลางเท่ากันและน้อยกว่ารัศมีมาก เมื่อลูกแก้วเลื่อนไปเล็กน้อยในแนวแกน x จะสั่นด้วยความถี่เชิงมุมกี่ rad/s (c = 3.00×10⁸ m/s, ไม่คิดแรงโน้มถ่วง, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=-4\,\frac Pc\,\frac{n-1}{n}\,\frac xR,\quad\omega^2=\frac{4P(n-1)}{mcRn}",
            [measure(w / sqrt(2)), measure(w / (2 * pi)), measure(w * sqrt(index))],
        )


def _rise(ground, base, station, exponent):
    return (ground + 273.15) * (station / base) ** exponent


@_type(8, "อุณหภูมิของอากาศแห้งที่ลอยขึ้นแบบแอเดียแบติก", LAPSE_TOPIC)
class DryTemperature(PhysicsSheet):
    def _variant(self, rng):
        ground = rng.randint(10, 35)
        base = rng.choice((100.0, 101.3))
        station = rng.randint(700, 920) / 10
        t = q08.solve(ground=ground, base=base, station=station)
        return draw(
            8,
            measure(t),
            f"ก้อนอากาศแห้ง (แก๊สอุดมคติอะตอมคู่ c_p = 7R/2, c_V = 5R/2) ที่พื้นมีความดัน {base:g} kPa อุณหภูมิ {ground} °C ลอยขึ้นแบบแอเดียแบติกจนความดันเป็น {station:g} kPa อุณหภูมิของก้อนอากาศเป็นกี่องศาเซลเซียส (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T\propto p^{1-1/\gamma}=p^{2/7}",
            [measure(_rise(ground, base, station, 5 / 7) - 273.15), measure(ground * (station / base) ** (2 / 7)), measure(_rise(ground, base, station, 2 / 5) - 273.15)],
        )


@_type(9, "อัตราการลดลงของอุณหภูมิของอากาศแห้ง", LAPSE_TOPIC)
class DryLapse(PhysicsSheet):
    def _variant(self, rng):
        planet = rng.choice((("โลก", 29.0, 9.81), ("ดาวอังคาร", 43.3, 3.71), ("ไททัน", 28.0, 1.35), ("โลก", 28.96, 9.80)))
        name, molar, gravity = planet
        a = q09.solve(molar=molar, gravity=gravity)
        return draw(
            9,
            measure(a),
            f"บรรยากาศของ{name}ถือเป็นแก๊สอุดมคติอะตอมคู่ (c_p = 7R/2) มวลโมเลกุลเฉลี่ย {molar:g} g/mol ความเร่งโน้มถ่วง {gravity:g} m/s² ก้อนอากาศแห้งที่ลอยขึ้นแบบแอเดียแบติกมีอุณหภูมิลดลงกี่เคลวินต่อกิโลเมตร (R = 8.31 J mol⁻¹ K⁻¹, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{dT}{dz}=\frac{2T}{7p}\frac{dp}{dz},\quad\frac{dp}{dz}=-\frac{p\mu g}{RT}\Rightarrow\alpha=\frac{2g\mu}{7R}",
            [measure(a * 7 / 5), measure(a * 7 / 2), measure(a * 1e3)],
        )


@_type(10, "ความสูงของสถานีจากความดันอากาศ", LAPSE_TOPIC)
class DryHeight(PhysicsSheet):
    def _variant(self, rng):
        ground = rng.randint(10, 35)
        station = rng.randint(700, 920) / 10
        z = q10.solve(ground=ground, station=station)
        alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)
        return draw(
            10,
            measure(z),
            f"สถานีบนพื้นวัดความดัน 100 kPa อุณหภูมิ {ground} °C อากาศแห้งลอยขึ้นแบบแอเดียแบติก (T ∝ p^(2/7), อัตราการลดลงของอุณหภูมิ α = 2gμ/(7R)) ถึงสถานีบนเขาที่วัดความดันได้ {station:g} kPa สถานีนี้สูงจากพื้นกี่เมตร (g = 9.81 m/s², μ = 29.0 g/mol, R = 8.31 J mol⁻¹ K⁻¹, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"z=\frac{T_0}{\alpha}\left[1-\left(\frac{p}{p_0}\right)^{2/7}\right]",
            [measure(ground / alpha * (1 - (station / 100) ** (2 / 7))), measure((ground + 273.15) / alpha * (1 - (station / 100) ** (5 / 7))), measure((ground + 273.15) / (alpha * 7 / 5) * (1 - (station / 100) ** (2 / 5)))],
        )


MOIST = "ก้อนอากาศอิ่มตัวด้วยไอน้ำที่ความสูง {z1} m อุณหภูมิ {t1} °C ลอยขึ้นถึงยอดเขาสูง {z2} m โดยไอน้ำควบแน่นตลอดทาง ใช้ T₂ − T₁ = −α(z₂ − z₁) − (αL_v/g)[β(T₂) − β(T₁)] ด้วย α = 9.78 K/km, L_v = 2.5×10⁶ J/kg, g = 9.81 m/s² และประมาณอัตราส่วนมวลไอน้ำต่อมวลอากาศเป็นเส้นตรง β(T) = β(T₁) + s(T − T₁) โดย s = {s}×10⁻³ ต่อ °C"


def _moist(rng):
    lower = rng.randint(0, 150) / 10
    start = rng.randint(5, 20) * 100
    top = start + rng.randint(5, 25) * 100
    slope = rng.choice((0.2, 0.25, 0.3, 0.349, 0.4, 0.5))
    alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)
    gain = alpha * 2.5e6 / 9.81 * slope * 1e-3
    if abs(1 - gain) < 0.2:
        raise _Clash  # the sign slip would blow up
    return lower, start, top, slope, alpha * (top - start), gain


@_type(11, "อุณหภูมิของอากาศชื้นที่ยอดเขา", LAPSE_TOPIC)
class MoistTemperature(PhysicsSheet):
    def _variant(self, rng):
        lower, start, top, slope, dry, gain = _moist(rng)
        t = q11.solve(lower=lower, start=start, top=top, slope=slope)
        return draw(
            11,
            measure(t),
            MOIST.format(z1=start, t1=f"{lower:g}", z2=top, s=f"{slope:g}") + " อุณหภูมิที่ยอดเขาเป็นกี่องศาเซลเซียส (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T_2-T_1=-\frac{\alpha(z_2-z_1)}{1+\alpha L_vs/g}",
            [measure(lower - dry), measure(lower - dry / (1 - gain)), measure(lower - dry / 2)],
        )


@_type(12, "อัตราเฉลี่ยการลดลงของอุณหภูมิของอากาศชื้น", LAPSE_TOPIC)
class MoistLapse(PhysicsSheet):
    def _variant(self, rng):
        lower, start, top, slope, dry, gain = _moist(rng)
        rate = q12.solve(lower=lower, start=start, top=top, slope=slope)
        alpha = dry / (top - start) * 1e3
        return draw(
            12,
            measure(rate),
            MOIST.format(z1=start, t1=f"{lower:g}", z2=top, s=f"{slope:g}") + " อัตราเฉลี่ยของการเปลี่ยนแปลงอุณหภูมิเทียบกับความสูงเป็นกี่ °C/km (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{\Delta T}{\Delta z}=-\frac{\alpha}{1+\alpha L_vs/g}",
            [measure(-alpha), measure(-alpha / (1 - gain)), measure(-alpha / 2)],
        )


LENS = "(G = 6.67×10⁻¹¹ N m² kg⁻², c = 3.00×10⁸ m/s, 1 pc = 3.086×10¹⁶ m, ดัชนีหักเหเสมือน n = 1 + 2GM/(rc²), ตอบเลขนัยสำคัญ 3 ตัว)"


def _lens(rng):
    mass = rng.randint(5, 80) / 10
    observer = rng.randint(30, 150) * 10
    source = rng.randint(30, 300) * 10
    return mass, observer, source


@_type(13, "ระยะที่แสงเลี้ยวผ่านมวลตามหลักการของแฟร์มาต์", LENS_TOPIC)
class LensImpact(PhysicsSheet):
    def _variant(self, rng):
        mass, observer, source = _lens(rng)
        y = q13.solve(mass=mass, source=source, observer=observer)
        return draw(
            13,
            measure(y),
            f"แสงจากเควซาร์ที่อยู่หลังกาแล็กซีมวล {mass:g}×10⁴¹ kg เป็นระยะ {source} Mpc เดินทางมายังโลกซึ่งห่างจากกาแล็กซี {observer} Mpc ตามเส้นทางที่ใช้เวลาน้อยที่สุด แสงเลี้ยวผ่านกาแล็กซีที่ระยะห่างกี่กิโลพาร์เซก " + LENS,
            r"t=\frac{\ell_1}{c}+\frac{2GM}{c^3}\ln\frac{4d_1d_2}{y^2},\quad\frac{dt}{dy}=0\Rightarrow y^2=\frac{4GM}{c^2}\frac{d_1d_2}{d_1+d_2}",
            [measure(y / 2), measure(y / sqrt(2)), measure(y * (source + observer) / sqrt(source * observer))],
        )


@_type(14, "ระยะเชิงมุมของภาพจากเลนส์แรงโน้มถ่วง", LENS_TOPIC)
class LensAngle(PhysicsSheet):
    def _variant(self, rng):
        mass, observer, source = _lens(rng)
        beta = q14.solve(mass=mass, source=source, observer=observer)
        return draw(
            14,
            measure(beta),
            f"เควซาร์อยู่หลังกาแล็กซีมวล {mass:g}×10⁴¹ kg เป็นระยะ {source} Mpc และโลกห่างจากกาแล็กซี {observer} Mpc ผู้สังเกตบนโลกเห็นภาพของเควซาร์ห่างจากแนวเล็งที่ผ่านกาแล็กซีเป็นมุมกี่พิลิปดา " + LENS,
            r"\beta=\frac{y}{d_2}=\sqrt{\frac{4GM}{c^2}\,\frac{d_1}{d_2(d_1+d_2)}}",
            [measure(beta * observer / source), measure(beta / 2), measure(beta / sqrt(2))],
        )


@_type(15, "มวลของกาแล็กซีจากวงแหวนของไอน์สไตน์", LENS_TOPIC)
class EinsteinRing(PhysicsSheet):
    def _variant(self, rng):
        ring = rng.randint(50, 200) / 100
        galaxy = rng.randint(30, 150) * 10
        quasar = galaxy + rng.randint(50, 300) * 10
        m = q15.solve(ring=ring, quasar=quasar, galaxy=galaxy)
        d1, d2 = quasar - galaxy, galaxy
        return draw(
            15,
            measure(m),
            f"วงแหวนของไอน์สไตน์มีรัศมีเชิงมุม {ring:g} พิลิปดา เควซาร์อยู่ห่างโลก {quasar} Mpc และกาแล็กซีที่เป็นเลนส์อยู่ห่างโลก {galaxy} Mpc ในแนวเดียวกัน มวลของกาแล็กซีเป็นกี่ ×10⁴¹ kg (G = 6.67×10⁻¹¹ N m² kg⁻², c = 3.00×10⁸ m/s, 1 pc = 3.086×10¹⁶ m, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\beta^2=\frac{4GM}{c^2}\,\frac{d_1}{d_2(d_1+d_2)},\quad d_1=D_{\text{เควซาร์}}-d_2",
            [measure(4 * m), measure(m * (quasar + d2) / quasar * d1 / (d1 + d2)), measure(m * (d1 / d2) ** 2)],
        )


NUT = 38.4e-3 * 9.81


@_type(16, "สัมประสิทธิ์ความเสียดทานระหว่างกระดาษอย่างง่าย", BOOK_TOPIC)
class PaperFriction(PhysicsSheet):
    def _variant(self, rng):
        nuts = rng.randint(2, 6)
        mu = rng.randint(30, 60) / 100
        pulls = tuple(round(2 * mu * nuts * NUT * (1 + rng.randint(-30, 30) / 1000), 3) for _ in range(5))
        m = q16.solve(nuts=nuts, pulls=pulls)
        load = nuts * NUT
        return draw(
            16,
            measure(m),
            f"สอดกระดาษแผ่นหนึ่งระหว่างกระดาษสองแผ่น วางน็อตขนาด 38.4 g จำนวน {nuts} ตัวกดทับด้านบน แล้วดึงแผ่นกลางออก วัดแรงดึงที่ทำให้เริ่มเคลื่อนได้ " + ", ".join(f"{t:.3f}" for t in pulls) + " N สัมประสิทธิ์ความเสียดทานสถิตระหว่างกระดาษกับกระดาษเป็นเท่าใด (g = 9.81 m/s², ไม่คิดมวลกระดาษ, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mu=\frac{\langle T\rangle}{2W_0}\quad(\text{แผ่นกลางมีผิวสัมผัสสองด้าน})",
            [measure(2 * m), measure(m * 9.81), measure(max(pulls) / (2 * load))],
        )


SHEETS = (1, 2, 3, 4, 6, 8)


def _stack(rng):
    nuts = rng.randint(2, 3)
    mu = rng.randint(40, 70) / 100
    other = rng.randint(-3, 3) / 10
    pulls = tuple(round(2 * mu * nuts * NUT * n + other + rng.randint(-15, 15) / 100, 2) for n in SHEETS)
    return nuts, pulls


def _table(pulls):
    return ", ".join(f"({n}, {t:.2f} N)" for n, t in zip(SHEETS, pulls))


STACK = "ซ้อนหน้าสมุดสองเล่มสลับกัน กดทับด้วยน็อตขนาด 38.4 g จำนวน {k} ตัว แรงดึงแยกสมุดเป็นไปตาม T = 2μW₀N + T₀ วัด (N, T) ได้ {t}"


@_type(17, "สัมประสิทธิ์ความเสียดทานจากกราฟแรงดึงกับจำนวนแผ่นที่ซ้อน", BOOK_TOPIC)
class StackFriction(PhysicsSheet):
    def _variant(self, rng):
        nuts, pulls = _stack(rng)
        m = q17.solve(nuts=nuts, sheets=SHEETS, pulls=pulls)
        load = nuts * NUT
        origin = sum(n * t for n, t in zip(SHEETS, pulls)) / sum(n * n for n in SHEETS)
        return draw(
            17,
            measure(m),
            STACK.format(k=nuts, t=_table(pulls)) + " จากความชันของกราฟ T กับ N (วิธีกำลังสองน้อยที่สุด) สัมประสิทธิ์ความเสียดทานสถิตระหว่างกระดาษเป็นเท่าใด (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{ความชัน}=2\mu W_0",
            [measure(2 * m), measure(m * 9.81), measure(origin / (2 * load))],
        )


@_type(18, "แรงเสียดทานอื่นของระบบจากจุดตัดแกน", BOOK_TOPIC)
class StackOffset(PhysicsSheet):
    def _variant(self, rng):
        nuts, pulls = _stack(rng)
        t0 = q18.solve(sheets=SHEETS, pulls=pulls)
        mx, my = sum(SHEETS) / 6, sum(pulls) / 6
        slope = sum((n - mx) * (t - my) for n, t in zip(SHEETS, pulls)) / sum((n - mx) ** 2 for n in SHEETS)
        return draw(
            18,
            measure(t0),
            STACK.format(k=nuts, t=_table(pulls)) + " จากจุดตัดแกนของกราฟ T กับ N (วิธีกำลังสองน้อยที่สุด) แรงเสียดทานอื่นของระบบ T₀ เป็นกี่นิวตัน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T=2\mu W_0N+T_0",
            [measure(-t0), measure(-t0 / slope), measure(pulls[0])],
        )


GAPS = (0.015, 0.018, 0.021, 0.025, 0.030)
DELTA = 0.106e-3


def _amplified(rng):
    mu = rng.randint(25, 45) / 100
    k = 2 * mu * DELTA * 24**2
    load = 2 * 2.1e-3 * 9.81
    pulls = tuple(
        round(2 * mu * 24 * load * sqrt(pi / (4 * k)) * sqrt(d) * exp(k / d) * (1 + rng.randint(-40, 40) / 1000), 2)
        for d in GAPS
    )
    return pulls


@_type(19, "ค่าคงตัว k จากกราฟของสมุดที่สอดสลับกัน", BOOK_TOPIC)
class AmplifiedSlope(PhysicsSheet):
    def _variant(self, rng):
        pulls = _amplified(rng)
        k = q19.solve(gaps=GAPS, pulls=pulls)
        ten = k / log(10)
        bare = q19.solve(gaps=GAPS, pulls=tuple(t * sqrt(d) for t, d in zip(pulls, GAPS)))
        ys = [log(t / sqrt(d)) for t, d in zip(pulls, GAPS)]
        mx, my = sum(GAPS) / 5, sum(ys) / 5
        direct = sum((d - mx) * (y - my) for d, y in zip(GAPS, ys)) / sum((d - mx) ** 2 for d in GAPS)
        table = ", ".join(f"({d * 100:g} cm, {t:.2f} N)" for d, t in zip(GAPS, pulls))
        return draw(
            19,
            measure(k),
            f"สมุดสองเล่มซ้อนสลับกันทีละแผ่น (N = 24) แรงดึงแยกเป็นไปตาม T = 2μNW₁√(π/(4k)) √d exp(k/d) + T₀ โดย T₀ ≈ 0 วัดแรงดึงที่ระยะส่วนที่ไม่ซ้อนกัน d ได้ (d, T) = {table} จากความชันของกราฟเส้นตรง ln(T/√d) กับ 1/d (วิธีกำลังสองน้อยที่สุด) ค่าคงตัว k เป็นกี่เมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\ln\frac{T-T_0}{\sqrt d}=\ln\left(2\mu NW_1\sqrt{\frac{\pi}{4k}}\right)+\frac kd",
            [measure(ten), measure(bare), measure(direct)],
        )


@_type(20, "สัมประสิทธิ์ความเสียดทานจากการเสริมกันเองของแรงเสียดทาน", BOOK_TOPIC)
class AmplifiedFriction(PhysicsSheet):
    def _variant(self, rng):
        k = rng.randint(25, 70) / 1000
        sheets = rng.choice((16, 20, 24, 30))
        thickness = rng.choice((0.08, 0.09, 0.1, 0.106, 0.12))
        m = q20.solve(k=k, sheets=sheets, thickness=thickness)
        return draw(
            20,
            measure(m),
            f"จากกราฟของสมุดสองเล่มที่ซ้อนสลับกันทีละแผ่น N = {sheets} แผ่น ได้ k = {k:g} m โดย k = 2μδN² และกระดาษแต่ละแผ่นหนา δ = {thickness:g} mm สัมประสิทธิ์ความเสียดทานสถิตระหว่างกระดาษเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mu=\frac{k}{2\delta N^2}",
            [measure(m * sheets), measure(m * 1e-3), measure(2 * m)],
        )
