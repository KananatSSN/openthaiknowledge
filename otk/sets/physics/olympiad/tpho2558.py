"""Seeded variants of the reviewed TPhO 14 (2558) national physics olympiad."""

from math import acos, asin, atan, degrees, floor, log, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2558_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2558_physics import q11, q12, q13, q14, q15, q16, q17

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
    1: ("phys.max_swing_as_equilibrium", "phys.field_weight_ratio_inverted", "phys.field_work_full_length"),
    2: ("phys.equilibrium_as_max_swing", "phys.field_weight_ratio_inverted", "phys.equilibrium_sine_for_tangent"),
    3: ("phys.field_ignored_in_period", "phys.frequency_angular_confused", "phys.effective_gravity_added_linearly"),
    4: ("phys.motor_torque_balanced_assumed", "phys.counterweight_torque_sign", "phys.beam_inertia_about_centre"),
    5: ("phys.beam_inertia_factor_dropped", "phys.beam_inertia_about_centre", "phys.counterweight_not_rooted"),
    6: ("phys.charles_ratio_inverted", "phys.celsius_for_kelvin", "phys.pressure_rise_only"),
    7: ("phys.vapour_pressure_includes_gas", "phys.vapour_temperature_initial", "phys.sphere_area_for_circle"),
    8: ("phys.latent_heat_dropped", "phys.vapour_heating_dropped", "phys.extra_heat_for_total"),
    9: ("phys.adiabatic_as_isothermal", "phys.adiabatic_exponent_inverted", "phys.atmosphere_force_dropped"),
    10: ("phys.adiabatic_as_isothermal", "phys.atmosphere_work_dropped", "phys.kinetic_half_missing"),
    11: ("phys.adiabatic_as_isothermal", "phys.adiabatic_exponent_inverted", "phys.barrel_length_from_end"),
    12: ("phys.circumference_for_area", "phys.emf_frequency_dropped", "phys.emf_amplitude_halved"),
    13: ("phys.peak_power_for_average", "phys.disc_as_single_ring", "phys.average_halved_twice"),
    14: ("phys.radius_not_rooted", "phys.projectile_half_dropped", "phys.diameter_for_radius"),
    15: ("phys.centimetres_not_converted", "phys.diameter_for_radius", "phys.poiseuille_factor_eight_dropped"),
    16: ("phys.series_tube_ignored", "phys.series_needle_ignored", "phys.series_as_parallel"),
    17: ("phys.inner_radius_for_outer", "phys.diameter_for_radius", "phys.drop_factor_dropped"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 14 (2558)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2558_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2558_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


SWING_TOPIC = "ประจุแกว่งในสนามไฟฟ้า"
BARRIER_TOPIC = "คานกั้นรถไฟ"
FILM_TOPIC = "ชั้นน้ำในภาชนะปิดที่ร้อนขึ้น"
POPGUN_TOPIC = "ฉับโผง"
EDDY_TOPIC = "การให้ความร้อนด้วยการเหนี่ยวนำแม่เหล็ก"
SALINE_TOPIC = "ความหนืดและความตึงผิวของน้ำเกลือ"

SWING = "ลูกตุ้มประจุ {q} µC มวล {m} g แขวนด้วยเชือกเบายาว {l} m อยู่ในสนามไฟฟ้าแนวราบ {E} kN/C และสนามโน้มถ่วง 9.8 m/s²"


def _swing(rng, most):
    while True:
        charge, field, mass = rng.randint(1, 10), rng.randint(1, 20), rng.randint(1, 20)
        ratio = charge * field / (mass * 9.8)
        if 0.1 <= ratio <= most:
            return charge, field, mass, ratio


@_type(1, "มุมสูงสุดของประจุที่แกว่งในสนามไฟฟ้า", SWING_TOPIC)
class SwingMax(PhysicsSheet):
    def _variant(self, rng):
        charge, field, mass, ratio = _swing(rng, 1.5)
        theta = q01.solve(charge=charge, field=field, mass=mass)
        return draw(
            1,
            measure(theta),
            SWING.format(q=charge, m=mass, l="0.5", E=field) + " เริ่มจากเชือกอยู่ในแนวดิ่งแล้วปล่อย ประจุแกว่งขึ้นไปได้มุมสูงสุดกี่องศาจากแนวดิ่ง (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"qE\ell\sin\theta_m=mg\ell(1-\cos\theta_m)\Rightarrow\tan\frac{\theta_m}{2}=\frac{qE}{mg}",
            [measure(degrees(atan(ratio))), measure(degrees(2 * atan(1 / ratio))), measure(degrees(acos(1 - ratio)))],
        )


@_type(2, "มุมสมดุลของประจุในสนามไฟฟ้า", SWING_TOPIC)
class SwingRest(PhysicsSheet):
    def _variant(self, rng):
        charge, field, mass, ratio = _swing(rng, 0.95)
        theta = q02.solve(charge=charge, field=field, mass=mass)
        return draw(
            2,
            measure(theta),
            SWING.format(q=charge, m=mass, l="0.5", E=field) + " หลังจากพลังงานสูญเสียไปจนประจุหยุดนิ่ง เชือกเอียงทำมุมกี่องศากับแนวดิ่ง (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mg\sin\theta_0=qE\cos\theta_0",
            [measure(2 * theta), measure(degrees(atan(1 / ratio))), measure(degrees(asin(ratio)))],
        )


@_type(3, "ความถี่การสั่นของประจุในสนามไฟฟ้า", SWING_TOPIC)
class SwingFrequency(PhysicsSheet):
    def _variant(self, rng):
        charge, field, mass, ratio = _swing(rng, 2.0)
        length = rng.randint(2, 15) / 10
        f = q03.solve(charge=charge, field=field, mass=mass, length=length)
        return draw(
            3,
            measure(f),
            SWING.format(q=charge, m=mass, l=f"{length:g}", E=field) + " ประจุสั่นด้วยแอมพลิจูดเล็ก ๆ รอบตำแหน่งสมดุล ความถี่ของการสั่นเป็นกี่เฮิรตซ์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\omega^2=\frac{mg\cos\theta_0+qE\sin\theta_0}{m\ell}",
            [
                measure(sqrt(9.8 / length) / (2 * pi)),
                measure(2 * pi * f),
                measure(sqrt(9.8 * (1 + ratio) / length) / (2 * pi)),
            ],
        )


def _barrier_l(torque, beam, length, weight, inertia, sign=1, g=9.8):
    b = sign * (torque / g - beam * length / 2)
    return (-b + sqrt(b * b + weight * inertia)) / weight


@_type(4, "ระยะตุ้มถ่วงที่ทำให้คานหมุนเร็วที่สุด", BARRIER_TOPIC)
class BarrierFastest(PhysicsSheet):
    def _variant(self, rng):
        beam = rng.randint(10, 40)
        length = rng.randint(10, 40) / 10
        weight = rng.randint(5, 40)
        torque = round(beam * 9.8 * length / 2 * rng.randint(12, 30) / 10)
        arm = q04.solve(torque=torque, beam=beam, length=length, weight=weight)
        return draw(
            4,
            measure(arm),
            f"คานกั้นรถไฟยาว {length:g} m มวล {beam} kg หมุนรอบปลายข้างหนึ่ง มีตุ้มถ่วงขนาดเล็กมวล {weight} kg บนแกนเบาที่ระยะ ℓ จากจุดหมุนด้านตรงข้าม "
            f"เครื่องยนต์ที่จุดหมุนให้ทอร์กคงที่ {torque} N·m ระยะ ℓ เท่าใด (เมตร) จึงทำให้คานหมุนขึ้นได้เร็วที่สุด (I = ML²/3 รอบปลาย, g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\alpha=\frac{\tau+mg\ell-MgL/2}{ML^2/3+m\ell^2},\quad \frac{d\alpha}{d\ell}=0",
            [
                measure(length * sqrt(beam / (3 * weight))),
                measure(_barrier_l(torque, beam, length, weight, beam * length**2 / 3, sign=-1)),
                measure(_barrier_l(torque, beam, length, weight, beam * length**2 / 12)),
            ],
        )


@_type(5, "ระยะตุ้มถ่วงโดยประมาณของคานกั้นรถไฟ", BARRIER_TOPIC)
class BarrierApprox(PhysicsSheet):
    def _variant(self, rng):
        beam = rng.randint(10, 40)
        length = rng.randint(10, 40) / 10
        weight = rng.randint(5, 40)
        if 3 * weight == beam or weight == beam:
            raise _Clash
        arm = q05.solve(beam=beam, length=length, weight=weight)
        return draw(
            5,
            measure(arm),
            f"คานกั้นรถไฟยาว {length:g} m มวล {beam} kg เครื่องยนต์ที่จุดหมุนปลายคานยกคานเปล่าขึ้นได้อย่างช้า ๆ เท่านั้น เมื่อถ่วงด้วยมวล {weight} kg ที่ระยะ ℓ ด้านตรงข้าม "
            "ระยะ ℓ ประมาณกี่เมตรที่ทำให้คานหมุนได้เร็วที่สุด (I = ML²/3 รอบปลาย, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tau\approx\frac{MgL}{2}\Rightarrow m\ell^2=\frac{ML^2}{3}",
            [
                measure(length * sqrt(beam / weight)),
                measure(length * sqrt(beam / (12 * weight))),
                measure(length * beam / (3 * weight)),
            ],
        )


def _film(rng):
    start = rng.randint(15, 30)
    end = rng.randint(70, 120)
    pressure = rng.randint(90, 110)
    gas = pressure * (end + 273.15) / (start + 273.15)
    final = round(gas + rng.randint(2, 15), 1)
    return start, end, pressure, final


@_type(6, "ความดันก๊าซในภาชนะปิดเมื่อร้อนขึ้น", FILM_TOPIC)
class FilmGasPressure(PhysicsSheet):
    def _variant(self, rng):
        start, end, pressure, _ = _film(rng)
        p = q06.solve(pressure=pressure, start=start, end=end)
        return draw(
            6,
            measure(p),
            f"ภาชนะปิดปริมาตรคงตัวบรรจุก๊าซอุดมคติความดัน {pressure} kPa ที่ {start} °C เมื่อเพิ่มอุณหภูมิเป็น {end} °C ถ้าคิดเฉพาะก๊าซ ความดันเป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{P}{T}=\text{ค่าคงที่}",
            [
                measure(pressure * (start + 273.15) / (end + 273.15)),
                measure(pressure * end / start),
                measure(pressure * (end - start) / (start + 273.15)),
            ],
        )


@_type(7, "ความหนาของฟิล์มน้ำในภาชนะปิด", FILM_TOPIC)
class FilmThickness(PhysicsSheet):
    def _variant(self, rng):
        start, end, pressure, final = _film(rng)
        volume = rng.randint(1, 10)
        t = q07.solve(volume=volume, pressure=pressure, final=final, start=start, end=end)
        T0, T1 = start + 273.15, end + 273.15
        vapour = final - pressure * T1 / T0
        return draw(
            7,
            measure(t),
            f"ภาชนะปิดทรงกลมปริมาตร {volume} L มีก๊าซความดัน {pressure} kPa ที่ {start} °C ผนังด้านในเคลือบด้วยฟิล์มน้ำบาง ๆ สม่ำเสมอ "
            f"เมื่อให้ความร้อนจนถึง {end} °C น้ำระเหยหมดและความดันเป็น {final:g} kPa ฟิล์มน้ำเดิมหนาประมาณกี่ไมโครเมตร (น้ำ 18 g/mol, 1000 kg/m³, R = 8.314 J/(mol·K), ตอบเลขนัยสำคัญ 3 ตัว)",
            r"n_W=\frac{(P_1-P_0T_1/T_0)V}{RT_1},\quad \text{ความหนา}=\frac{M_Wn_W/\rho}{4\pi r^2}",
            [measure(t * final / vapour), measure(t * T1 / T0), measure(4 * t)],
        )


@_type(8, "อัตราส่วนเวลาให้ความร้อนเมื่อมีน้ำเกาะ", FILM_TOPIC)
class FilmHeatingTime(PhysicsSheet):
    def _variant(self, rng):
        start, end, pressure, final = _film(rng)
        ratio = q08.solve(pressure=pressure, final=final, start=start, end=end)
        T0, T1 = start + 273.15, end + 273.15
        moles = T0 * final / (T1 * pressure) - 1
        return draw(
            8,
            measure(ratio),
            f"ภาชนะปิดมีก๊าซความดัน {pressure} kPa ที่ {start} °C ให้ความร้อนในอัตราคงตัวจนถึง {end} °C กรณี ก ไม่มีน้ำเกาะผนัง ใช้เวลา t_A กรณี ข มีฟิล์มน้ำเกาะซึ่งระเหยหมด (ใกล้ {start} °C) จนความดันสุดท้ายเป็น {final:g} kPa ใช้เวลา t_B "
            "อัตราส่วน t_B/t_A เป็นเท่าใด (c_V ของก๊าซ 20.8 และของไอน้ำ 25.0 J/(mol·K) ความร้อนแฝง 40.7 kJ/mol, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{t_B}{t_A}=1+\frac{n_Wc_{VW}\Delta T+n_WL}{n_Gc_{VG}\Delta T}",
            [measure(1 + 25.0 * moles / 20.8), measure(1 + 40700 / (T1 - T0) * moles / 20.8), measure(ratio - 1)],
        )


AIR = 1.0e5
POPGUN = (
    "ฉับโผงมีรูพื้นที่หน้าตัด {A} cm² ก้านยิงยาว {L0} cm ลูกปอลูกแรกติดที่ปลายกระบอกด้วยแรงเสียดทานสถิตสูงสุด {F} N "
    "ดันลูกที่สองเข้าไปอย่างรวดเร็ว อากาศระหว่างลูกถูกอัดแบบแอเดียแบติก (γ = 1.4, ความดันบรรยากาศ 1.0×10⁵ Pa)"
)


def _popgun(rng):
    return rng.choice((0.5, 1.0, 1.5)), rng.randint(20, 40), rng.randint(5, 30)


@_type(9, "ระยะอัดอากาศในฉับโผงก่อนลูกปอเคลื่อน", POPGUN_TOPIC)
class PopgunGap(PhysicsSheet):
    def _variant(self, rng):
        area, rest, grip = _popgun(rng)
        L = q09.solve(rest=rest, grip=grip, area=area)
        PA = AIR * area * 1e-4
        return draw(
            9,
            measure(L),
            POPGUN.format(A=f"{area:g}", L0=rest, F=grip) + " ลูกปอทั้งสองห่างกันกี่เซนติเมตรเมื่อลูกแรกเริ่มเคลื่อนที่ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_aL_0^\gamma=PL^\gamma,\quad PA=F+P_aA",
            [measure(rest * PA / (grip + PA)), measure(rest * (PA / (grip + PA)) ** 1.4), measure(rest * (PA / grip) ** (1 / 1.4))],
        )


def _speed(gap, grip, slide, area, barrel, mass, iso=False, atmosphere=True, half=True):
    PA = AIR * area
    if iso:
        work = (grip + PA) * gap * log((gap + barrel) / gap)
    else:
        work = (grip + PA) / 0.4 * (gap - gap**1.4 * (gap + barrel) ** -0.4)
    work -= (slide + (PA if atmosphere else 0)) * barrel
    if work <= 0:
        return None
    return sqrt((2 if half else 1) * work / mass)


@_type(10, "อัตราเร็วลูกปอที่หลุดจากฉับโผง", POPGUN_TOPIC)
class PopgunSpeed(PhysicsSheet):
    def _variant(self, rng):
        area, rest, grip = _popgun(rng)
        slide = rng.randint(1, 10) / 10
        barrel = rng.randint(2, 10)
        mass = rng.randint(5, 30) / 10
        A, D, m = area * 1e-4, barrel * 1e-2, mass * 1e-3
        gap = q09.solve(rest=rest, grip=grip, area=area) * 1e-2
        if _speed(gap, grip, slide, A, D, m) is None:
            raise _Clash                       # the pellet would stop inside the barrel
        v = q10.solve(rest=rest, grip=grip, slide=slide, area=area, barrel=barrel, mass=mass)
        iso_gap = rest * 1e-2 * AIR * A / (grip + AIR * A)
        others = [
            _speed(iso_gap, grip, slide, A, D, m, iso=True),
            _speed(gap, grip, slide, A, D, m, atmosphere=False),
            _speed(gap, grip, slide, A, D, m, half=False),
        ]
        if None in others:
            raise _Clash
        return draw(
            10,
            measure(v),
            POPGUN.format(A=f"{area:g}", L0=rest, F=grip) + f" ลูกปอมวล {mass:g} g ขณะเคลื่อนแรงเสียดทานเหลือ {slide:g} N และวิ่งในกระบอกได้อีก {barrel} cm (ก้านยิงแทบไม่เคลื่อน) ลูกปอหลุดจากปลายกระบอกด้วยอัตราเร็วกี่เมตรต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac12mv^2=\int_0^D\left[(F+P_aA)\left(\frac{L}{L+x}\right)^\gamma-P_aA-f\right]dx",
            [measure(x) for x in others],
        )


@_type(11, "ระยะ D ที่ให้ลูกปอเร็วที่สุด", POPGUN_TOPIC)
class PopgunBestBarrel(PhysicsSheet):
    def _variant(self, rng):
        area, rest, grip = _popgun(rng)
        slide = rng.randint(1, 10) / 10
        D = q11.solve(rest=rest, grip=grip, slide=slide, area=area)
        PA = AIR * area * 1e-4
        L = q09.solve(rest=rest, grip=grip, area=area)
        iso_L = rest * PA / (grip + PA)
        ratio = (grip + PA) / (slide + PA)
        return draw(
            11,
            measure(D),
            POPGUN.format(A=f"{area:g}", L0=rest, F=grip) + f" ขณะเคลื่อนแรงเสียดทานเหลือ {slide:g} N ระยะ D (ส่วนของกระบอกที่ยาวกว่าก้านยิง) ควรเป็นกี่เซนติเมตรจึงยิงลูกปอได้เร็วที่สุด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"(F+P_aA)\left(\frac{L}{L+D}\right)^\gamma=f+P_aA",
            [measure(iso_L * (ratio - 1)), measure(L * (ratio**1.4 - 1)), measure(L * ratio ** (1 / 1.4))],
        )


@_type(12, "อีเอ็มเอฟเหนี่ยวนำสูงสุดในแผ่นทองแดง", EDDY_TOPIC)
class EddyEmf(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(2, 20)
        field = rng.randint(1, 10) / 20
        omega = rng.choice((50, 100, 150, 200, 314))
        e = q12.solve(radius=radius, field=field, omega=omega)
        r = radius * 1e-2
        return draw(
            12,
            measure(e),
            f"แผ่นทองแดงบางอยู่ในสนามแม่เหล็ก B = B₀ cos ωt ตั้งฉากกับแผ่น โดย B₀ = {field:g} T และ ω = {omega} rad/s อีเอ็มเอฟเหนี่ยวนำรอบวงกลมรัศมี {radius} cm บนแผ่นมีค่าสูงสุดกี่มิลลิโวลต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\varepsilon=-\frac{d\phi}{dt}=\pi r^2B_0\omega\sin\omega t",
            [measure(2 * pi * r * field * omega * 1e3), measure(pi * r * r * field * 1e3), measure(e / 2)],
        )


@_type(13, "กำลังเฉลี่ยจากกระแสไหลวนในแผ่นทองแดง", EDDY_TOPIC)
class EddyPower(PhysicsSheet):
    def _variant(self, rng):
        thickness = rng.randint(1, 10) / 10
        radius = rng.randint(2, 10)
        field = rng.randint(1, 10) / 100
        omega = rng.choice((50, 100, 150, 200, 314))
        p = q13.solve(thickness=thickness, radius=radius, field=field, omega=omega)
        return draw(
            13,
            measure(p),
            f"แผ่นทองแดงกลมหนา {thickness:g} mm รัศมี {radius} cm (สภาพต้านทาน 1.7×10⁻⁸ Ω·m) อยู่ในสนามแม่เหล็ก B₀ cos ωt ตั้งฉากกับแผ่น โดย B₀ = {field:g} T และ ω = {omega} rad/s "
            "กำลังเฉลี่ยที่สูญเสียเนื่องจากกระแสเหนี่ยวนำในแผ่นเป็นกี่วัตต์ (ไม่คิดสนามจากกระแสไหลวน, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta P=\frac{\varepsilon^2}{R_{\text{ring}}},\quad R_{\text{ring}}=\frac{\rho\,2\pi r}{z\,\Delta r}",
            [measure(2 * p), measure(4 * p), measure(p / 2)],
        )


NEEDLE = 4.0
WALL = 0.220


@_type(14, "รัศมีรูเข็มจากระยะตกของน้ำ", SALINE_TOPIC)
class NeedleBore(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(30, 50) / 100       # mm
        height = rng.randint(50, 100) / 10       # cm
        ranges = tuple(round(6.0 + 1.5 * k + rng.choice((-0.2, 0, 0.2)), 1) for k in range(6))
        coef = sqrt(9.8 / (2 * height * 1e-2)) * pi * (radius * 1e-3) ** 2 * 1e-2 / 1e-6   # ml/s per cm
        flows = tuple(round(coef * x + rng.choice((-0.01, 0, 0.01)), 2) for x in ranges)
        r = q14.solve(ranges=ranges, flows=flows, height=height)
        table = ", ".join(f"({x:g} cm, {q:.2f} ml/s)" for x, q in zip(ranges, flows))
        return draw(
            14,
            measure(r),
            f"น้ำเกลือพุ่งออกจากเข็มที่วางแนวนอนสูง {height:g} cm จากพื้น วัด (ระยะตก x, อัตราการไหล Q) ได้ {table} "
            "จากความชันของกราฟ Q กับ x (วิธีกำลังสองน้อยที่สุด) รัศมีรูเข็มเป็นกี่มิลลิเมตร (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"x=ut,\ y=\tfrac12gt^2\Rightarrow Q=\left(\sqrt{\frac{g}{2y}}\pi r^2\right)x",
            [measure(r * r), measure(r / 2 ** 0.25), measure(2 * r)],
        )


@_type(15, "ความหนืดของน้ำเกลือจากการไหลผ่านเข็ม", SALINE_TOPIC)
class NeedleViscosity(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(35, 50) / 100
        eta = rng.randint(10, 30) / 10           # mPa s
        heights = tuple(float(40 + 6 * k) for k in range(6))
        coef = pi * (radius * 1e-3) ** 4 * 1030 * 9.8 / (8 * eta * 1e-3 * NEEDLE * 1e-2) * 1e-2 / 1e-6   # ml/s per cm
        flows = tuple(round(coef * (h - 6.0) + rng.choice((-0.01, 0, 0.01)), 2) for h in heights)
        if min(flows) <= 0.05:
            raise _Clash
        got = q15.solve(heights=heights, flows=flows, radius=radius)
        table = ", ".join(f"({h:g} cm, {q:.2f} ml/s)" for h, q in zip(heights, flows))
        return draw(
            15,
            measure(got),
            f"น้ำเกลือ (1030 kg/m³) ไหลจากถุงผ่านเข็มยาว 4.0 cm รัศมีรู {radius:g} mm ที่ระดับผิวน้ำในถุงสูง h ต่าง ๆ วัด (h, Q) ได้ {table} "
            "ถ้าคิดการไหลผ่านเข็มอย่างเดียว ความหนืดของน้ำเกลือจากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) เป็นกี่มิลลิพาสคัลวินาที (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=\frac{\pi r^4\rho g}{8\eta\ell}(h-y)",
            [measure(got / 100), measure(16 * got), measure(8 * got)],
        )


@_type(16, "ความหนืดเมื่อคิดสายน้ำเกลือและเข็มอนุกรมกัน", SALINE_TOPIC)
class SeriesViscosity(PhysicsSheet):
    def _variant(self, rng):
        slope = rng.randint(80, 140) / 10000     # cm^2/s
        tube = rng.randint(100, 180)
        radius = rng.randint(38, 48) / 100
        eta = q16.solve(slope=slope, tube=tube, radius=radius)
        needle_r = NEEDLE * 1e-2 / (radius * 1e-3) ** 4
        tube_r = tube * 1e-2 / (1.1e-3) ** 4
        base = pi * 1030 * 9.8 / (8 * slope * 1e-4) * 1e3
        return draw(
            16,
            measure(eta),
            f"น้ำเกลือ (1030 kg/m³) ไหลผ่านสายน้ำเกลือรัศมีใน 1.1 mm ยาว {tube} cm ต่ออนุกรมกับเข็มยาว 4.0 cm รัศมีรู {radius:g} mm "
            f"กราฟอัตราการไหลกับระดับผิวน้ำมีความชัน {slope:g} cm²/s ความหนืดของน้ำเกลือเป็นกี่มิลลิพาสคัลวินาที (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=\frac{\pi\rho g(h-y)}{8\eta_c\left(\ell/r^4+L/R^4\right)}",
            [measure(base / needle_r), measure(base / tube_r), measure(base * (1 / needle_r + 1 / tube_r))],
        )


@_type(17, "ความตึงผิวของน้ำเกลือจากหยดน้ำ", SALINE_TOPIC)
class DropTension(PhysicsSheet):
    def _variant(self, rng):
        drops = rng.choice((30, 40, 50, 60))
        volume = rng.randint(70, 160) / 100
        radius = rng.randint(38, 48) / 100
        gamma = q17.solve(drops=drops, volume=volume, radius=radius)
        return draw(
            17,
            measure(gamma),
            f"น้ำเกลือ (1030 kg/m³) หยดออกจากปลายเข็มแนวดิ่งช้า ๆ ได้ {drops} หยด ปริมาตรรวม {volume:g} ml รูเข็มรัศมี {radius:g} mm ผนังเข็มหนา 0.220 mm "
            "ใช้ mg = 1.4(πr_o)γ เมื่อ r_o คือรัศมีภายนอกของเข็ม ความตึงผิวของน้ำเกลือเป็นกี่มิลลินิวตันต่อเมตร (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\gamma=\frac{\rho Vg}{1.4\pi r_o},\quad r_o=r+\text{ความหนาผนัง}",
            [measure(gamma * (radius + WALL) / radius), measure(gamma / 2), measure(gamma * 1.4)],
        )
