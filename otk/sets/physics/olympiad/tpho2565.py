"""Seeded variants of the reviewed TPhO 21 (2565) national physics olympiad."""

from math import cos, exp, floor, log, log10, pi, radians, sin, sqrt, tanh

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2565_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11

from otk.sheets.tpho2565_physics import q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22

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
    1: ("phys.dipole_equatorial_for_axial", "phys.dipole_single_charge", "phys.dipole_distance_power_two"),
    2: ("phys.dipole_magnitude_not_rooted", "phys.dipole_radial_only", "phys.dipole_sine_for_cosine"),
    3: ("phys.orbit_factor_dropped", "phys.orbit_sine_squared", "phys.orbit_root_three_dropped"),
    4: ("phys.energy_half_dropped", "phys.speed_angular_confused", "phys.speed_not_rooted"),
    5: ("phys.period_scheme_rounding", "phys.period_quarter_only", "phys.period_half_only"),
    6: ("phys.tanh_linearised", "phys.boltzmann_energy_doubled", "phys.magnetisation_up_fraction"),
    7: ("phys.entropy_field_ignored", "phys.boltzmann_energy_doubled", "phys.led_log10_used"),
    8: ("phys.susceptibility_half", "phys.susceptibility_doubled", "phys.celsius_for_kelvin"),
    9: ("phys.neighbour_count_dropped", "phys.dipole_axial_factor", "phys.dipole_distance_power_two"),
    10: ("phys.field_ratio_squared", "phys.field_ratio_rooted", "phys.adiabatic_temperature_unchanged"),
    11: ("phys.entropy_maximum_used", "phys.entropy_final_only", "phys.magnetic_energy_for_heat"),
    12: ("phys.bernoulli_half_dropped", "phys.bernoulli_sign_flipped", "phys.area_cm2_not_converted"),
    13: ("phys.mach_half_dropped", "phys.mach_gamma_for_gamma_minus_one", "phys.mach_linearised"),
    14: ("phys.adiabatic_density_exponent", "phys.pressure_exponent_gamma", "phys.pressure_isothermal_ratio"),
    15: ("phys.flow_factor_prefactor_dropped", "phys.flow_incompressible", "phys.flow_density_unchanged"),
    16: ("phys.critical_ratio_half", "phys.adiabatic_density_exponent", "phys.critical_temperature_ratio"),
    17: ("phys.choked_stagnation_values", "phys.flow_incompressible", "phys.choked_temperature_unchanged"),
    18: ("phys.log_bases_mixed", "phys.slope_axes_swapped", "phys.slope_sign_flipped"),
    19: ("phys.magnet_diameter_for_radius", "phys.dipole_axial_factor", "phys.millitesla_not_converted"),
    20: ("phys.gap_slope_not_halved", "phys.gap_full_width_as_d", "phys.line_forced_through_origin"),
    21: ("phys.flux_geometry_dropped", "phys.flux_full_length", "phys.magnet_diameter_for_radius"),
    22: ("phys.ring_disc_area", "phys.ring_width_doubled", "phys.millitesla_not_converted"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 21 (2565)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2565_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2565_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


DIPOLE_TOPIC = "ไดโพลไฟฟ้ากับประจุจุด"
COOLING_TOPIC = "การทำความเย็นด้วยสนามแม่เหล็ก"
NOZZLE_TOPIC = "การไหลของแก๊สในหัวฉีด"
MAGNET_TOPIC = "แม่เหล็กถาวรและสนามแม่เหล็ก"

K = 1 / (4 * pi * 8.854e-12)
DIPOLE = "ไดโพลไฟฟ้าประกอบด้วยประจุ ±{q} nC ห่างกัน {d} mm"
EPS = "(ε₀ = 8.854×10⁻¹² F/m, ตอบเลขนัยสำคัญ 3 ตัว)"


@_type(1, "สนามไฟฟ้าบนแกนของไดโพล", DIPOLE_TOPIC)
class DipoleAxis(PhysicsSheet):
    def _variant(self, rng):
        charge = rng.randint(1, 20) * 100
        spacing = rng.randint(5, 30) / 10
        distance = rng.randint(3, 30)
        e = q01.solve(charge=charge, spacing=spacing, distance=distance)
        z = distance * 1e-2
        return draw(
            1,
            scientific(e),
            DIPOLE.format(q=charge, d=f"{spacing:g}") + f" บนแกนของไดโพลที่ระยะ {distance} cm จากกึ่งกลาง (ไกลกว่า d มาก) สนามไฟฟ้ามีขนาดกี่ V/m " + EPS,
            r"E=\frac{1}{4\pi\epsilon_0}\,\frac{2p}{z^3}",
            [scientific(e / 2), scientific(K * charge * 1e-9 / z**2), scientific(e * z)],
        )


@_type(2, "ขนาดสนามไฟฟ้าของไดโพลที่ตำแหน่ง (r, θ)", DIPOLE_TOPIC)
class DipoleField(PhysicsSheet):
    def _variant(self, rng):
        charge = rng.randint(1, 20) * 100
        spacing = rng.randint(5, 30) / 10
        distance = rng.randint(3, 30)
        angle = rng.choice((20, 30, 40, 50, 60, 70, 110, 120, 135, 150))
        e = q02.solve(charge=charge, spacing=spacing, distance=distance, angle=angle)
        base = K * charge * 1e-9 * spacing * 1e-3 / (distance * 1e-2) ** 3
        c, s = cos(radians(angle)), sin(radians(angle))
        return draw(
            2,
            scientific(e),
            DIPOLE.format(q=charge, d=f"{spacing:g}") + f" ที่ระยะ {distance} cm จากกึ่งกลาง ทำมุม {angle}° กับแกนของไดโพล (ไกลกว่า d มาก) สนามไฟฟ้ามีขนาดกี่ V/m " + EPS,
            r"\vec E=\frac{1}{4\pi\epsilon_0}\left(\frac{2p\cos\theta}{r^3}\hat r+\frac{p\sin\theta}{r^3}\hat\theta\right)",
            [scientific(base * (1 + 3 * c * c)), scientific(base * 2 * abs(c)), scientific(base * sqrt(1 + 3 * s * s))],
        )


ORBIT = "ไดโพลไฟฟ้าโมเมนต์ {p} nC m ถูกตรึงไว้ ประจุบวก {q} µC มวล {m} g"


def _orbit(rng):
    return rng.randint(5, 50) / 10, rng.randint(5, 50) / 10, rng.randint(5, 50) / 10


@_type(3, "โมเมนตัมเชิงมุมของประจุที่โคจรเป็นวงกลมรอบไดโพล", DIPOLE_TOPIC)
class DipoleOrbit(PhysicsSheet):
    def _variant(self, rng):
        moment, charge, mass = _orbit(rng)
        lz = q03.solve(moment=moment, charge=charge, mass=mass)
        pqm = K * moment * 1e-9 * charge * 1e-6 * mass * 1e-3
        return draw(
            3,
            measure(lz),
            ORBIT.format(p=f"{moment:g}", q=f"{charge:g}", m=f"{mass:g}") + " เคลื่อนที่เป็นวงกลมรอบแกนของไดโพล (ไม่คิดแรงโน้มถ่วง) โมเมนตัมเชิงมุมรอบแกนเป็นกี่ ×10⁻⁵ kg m²/s " + EPS,
            r"E_z=0\Rightarrow\cos\theta_c=-\tfrac1{\sqrt3},\quad L_z^2=\frac{1}{4\pi\epsilon_0}\,\frac{4}{3\sqrt3}\,pq_0m_0",
            [measure(sqrt(pqm) * 1e5), measure(sqrt(pqm * 2 / sqrt(3)) * 1e5), measure(sqrt(pqm * 4 / 3) * 1e5)],
        )


RELEASE = ORBIT + " ถูกปล่อยจากหยุดนิ่งที่ระยะ {r} cm บนแนวตั้งฉากกับแกนของไดโพล (ไม่คิดแรงโน้มถ่วง)"


@_type(4, "อัตราเร็วสูงสุดของประจุที่ปล่อยใกล้ไดโพล", DIPOLE_TOPIC)
class DipoleSwingSpeed(PhysicsSheet):
    def _variant(self, rng):
        moment, charge, mass = _orbit(rng)
        radius = rng.randint(2, 20)
        v = q04.solve(moment=moment, charge=charge, mass=mass, radius=radius)
        return draw(
            4,
            measure(v),
            RELEASE.format(p=f"{moment:g}", q=f"{charge:g}", m=f"{mass:g}", r=radius) + " ประจุเคลื่อนที่ตามส่วนโค้งวงกลม อัตราเร็วสูงสุดเป็นกี่ m/s " + EPS,
            r"\tfrac12m_0v^2=\frac{q_0p}{4\pi\epsilon_0r_0^2}\quad(\theta=\pi)",
            [measure(v / sqrt(2)), measure(v / (radius * 1e-2)), measure(v * v)],
        )


@_type(5, "เวลาที่ประจุแกว่งกลับมาที่จุดปล่อย", DIPOLE_TOPIC)
class DipoleSwingPeriod(PhysicsSheet):
    def _variant(self, rng):
        moment, charge, mass = _orbit(rng)
        radius = rng.randint(2, 20)
        t = q05.solve(moment=moment, charge=charge, mass=mass, radius=radius)
        beta = q04.solve(moment=moment, charge=charge, mass=mass, radius=radius) / (radius * 1e-2)
        return draw(
            5,
            measure(t),
            RELEASE.format(p=f"{moment:g}", q=f"{charge:g}", m=f"{mass:g}", r=radius) + " ประจุแกว่งกลับมาที่จุดปล่อยในเวลากี่วินาที (ใช้ ∫₀^φ dx/√sin x ≈ 2√φ + √φ⁵/30, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\dot\phi=\beta\sqrt{\sin\phi},\ \beta=\sqrt{\frac{pq_0}{2\pi\epsilon_0m_0r_0^4}},\quad T=\frac4\beta\int_0^{\pi/2}\frac{d\phi}{\sqrt{\sin\phi}}",
            [measure(10.3 / beta), measure(t / 4), measure(t / 2)],
        )


SPINS = "วัสดุพาราแมกเนติกประกอบด้วยไดโพลแม่เหล็ก μ = 9.274×10⁻²⁴ J/T ที่ชี้ขึ้นหรือลงได้เท่านั้น (E = −μ⃗·B⃗, k_B = 1.38×10⁻²³ J/K)"


def _state(rng):
    # cold enough that mu B/(k_B T) is not small, so the choices stay apart
    return rng.choice((1.0, 1.5, 2.0, 3.0, 5.0)), rng.choice((0.5, 1.0, 1.5, 2.0))


@_type(6, "สภาพแม่เหล็กของวัสดุพาราแมกเนติกสองระดับ", COOLING_TOPIC)
class SpinMagnetisation(PhysicsSheet):
    def _variant(self, rng):
        field, temperature = _state(rng)
        m = q06.solve(field=field, temperature=temperature)
        x = 9.274e-24 * field / (1.38e-23 * temperature)
        return draw(
            6,
            measure(m),
            SPINS + f" ในสนาม {field:g} T ที่อุณหภูมิ {temperature:g} K สภาพแม่เหล็กต่อ Nμ (M/(Nμ)) เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{N_\uparrow}{N}=\frac{1}{e^{-2x}+1},\quad\frac{M}{N\mu}=\tanh x,\ x=\frac{\mu B}{k_BT}",
            [measure(x), measure(tanh(2 * x)), measure(1 / (exp(-2 * x) + 1))],
        )


@_type(7, "เอนโทรปีต่ออนุภาคของวัสดุพาราแมกเนติกสองระดับ", COOLING_TOPIC)
class SpinEntropy(PhysicsSheet):
    def _variant(self, rng):
        field, temperature = _state(rng)
        s = q07.solve(field=field, temperature=temperature)
        return draw(
            7,
            measure(s),
            SPINS + f" ในสนาม {field:g} T ที่อุณหภูมิ {temperature:g} K เอนโทรปีต่ออนุภาค S/(Nk_B) เป็นเท่าใด (S/k_B = N ln N − N↑ ln N↑ − N↓ ln N↓, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{S}{Nk_B}=\frac{\ln(e^{-2x}+1)}{e^{-2x}+1}+\frac{\ln(e^{2x}+1)}{e^{2x}+1}",
            [measure(log(2)), measure(q07.solve(field=2 * field, temperature=temperature)), measure(s / log(10))],
        )


@_type(8, "ความไวแม่เหล็กของวัสดุพาราแมกเนติกที่อุณหภูมิสูง", COOLING_TOPIC)
class SpinSusceptibility(PhysicsSheet):
    def _variant(self, rng):
        count = rng.randint(10, 100) / 10
        temperature = rng.choice((290, 300, 310, 350, 400))
        chi = q08.solve(count=count, temperature=temperature)
        return draw(
            8,
            scientific(chi),
            SPINS + f" มีไดโพล {count:g}×10²³ ตัว ที่อุณหภูมิ {temperature} K (สูงพอ) สภาพแม่เหล็กเป็น M = χB ค่า χ เป็นกี่ J/T² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"M=N\mu\tanh\frac{\mu B}{k_BT}\approx\frac{N\mu^2}{k_BT}B",
            [scientific(chi / 2), scientific(2 * chi), scientific(chi * temperature / (temperature - 273))],
        )


@_type(9, "สนามแม่เหล็กจากไดโพลเพื่อนบ้าน", COOLING_TOPIC)
class NeighbourField(PhysicsSheet):
    def _variant(self, rng):
        spacing = rng.randint(5, 30) / 10
        neighbours = rng.randint(2, 6)
        b = q09.solve(spacing=spacing, neighbours=neighbours)
        return draw(
            9,
            measure(b),
            f"ไดโพลแม่เหล็ก μ = 9.274×10⁻²⁴ J/T แต่ละตัวมีเพื่อนบ้านชี้ทิศเดียวกัน {neighbours} ตัว อยู่ห่าง {spacing:g} nm สนามจากไดโพลหนึ่งตัวประมาณ B = (μ₀/4π)μ/r³ สนามที่ไดโพลรู้สึกเป็นกี่มิลลิเทสลา (μ₀ = 4π×10⁻⁷ T m/A, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B_L=n\,\frac{\mu_0}{4\pi}\,\frac{\mu}{r^3}",
            [measure(b / neighbours), measure(2 * b), measure(b * spacing)],
        )


@_type(10, "อุณหภูมิสุดท้ายหลังลดสนามแม่เหล็กแบบแอเดียแบติก", COOLING_TOPIC)
class Demagnetise(PhysicsSheet):
    def _variant(self, rng):
        start = rng.choice((0.3, 0.5, 1.0, 1.5, 2.0, 4.2))
        high = rng.randint(1, 8)
        low = rng.randint(10, 100) / 10
        t = q10.solve(start=start, high=high, low=low)
        ratio = low * 1e-3 / high
        return draw(
            10,
            measure(t),
            f"วัสดุพาราแมกเนติกสองระดับอยู่ในสมดุลกับฮีเลียมเหลวที่ {start:g} K ขณะเพิ่มสนามจาก B_L = {low:g} mT เป็น B_H = {high} T แล้วแยกออกและลดสนามแบบแอเดียแบติกกลับเป็น B_L อุณหภูมิสุดท้ายเป็นกี่มิลลิเคลวิน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"S=S\!\left(\frac{\mu B}{k_BT}\right)\text{ คงที่}\Rightarrow T_f=\frac{B_L}{B_H}T_i",
            [measure(start * ratio**2 * 1e3), measure(start * sqrt(ratio) * 1e3), measure(start * 1e3)],
        )


@_type(11, "ความร้อนต่ออนุภาคที่ถ่ายเทออกในการทำความเย็นด้วยสนามแม่เหล็ก", COOLING_TOPIC)
class DemagnetiseHeat(PhysicsSheet):
    def _variant(self, rng):
        start = rng.choice((0.5, 1.0, 1.5, 2.0))
        high = rng.choice((0.5, 1.0, 2.0, 3.0))
        low = rng.randint(10, 50) / 10
        q = q11.solve(start=start, high=high, low=low)
        kb = 1.38e-23
        x = 9.274e-24 * high / (kb * start)
        return draw(
            11,
            measure(q),
            f"วัสดุพาราแมกเนติกสองระดับ (μ = 9.274×10⁻²⁴ J/T) อยู่ในสมดุลกับฮีเลียมเหลวที่ {start:g} K ขณะเพิ่มสนามจาก {low:g} mT เป็น {high:g} T จากนั้นแยกออกแล้วลดสนามแบบแอเดียแบติก ความร้อนต่ออนุภาคที่ถ่ายเทออกจากวัสดุตลอดกระบวนการเป็นกี่ ×10⁻²⁴ J (k_B = 1.38×10⁻²³ J/K, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac QN=T_i\,\frac{S(B_L)-S(B_H)}{N}",
            [measure(start * kb * log(2) * 1e24), measure(start * kb * q07.solve(field=high, temperature=start) * 1e24), measure(9.274e-24 * high * tanh(x) * 1e24)],
        )


GAS = "แก๊สในภาชนะใหญ่มีความดัน {P} kPa ความหนาแน่น {rho} kg/m³ ไหลออกทางท่อที่ปลายเปิดมีพื้นที่หน้าตัด {A} cm²"


def _gas(rng):
    return rng.randint(100, 500), rng.randint(12, 60) / 10, rng.choice((0.5, 1.0, 2.0, 3.0))


@_type(12, "ความดันที่ปลายหัวฉีดเมื่อแก๊สไม่อัดตัว", NOZZLE_TOPIC)
class NozzleIncompressible(PhysicsSheet):
    def _variant(self, rng):
        pressure, density, area = _gas(rng)
        flow = rng.randint(10, 60)
        p = q12.solve(pressure=pressure, density=density, area=area, flow=flow)
        if p <= 0:
            raise _Clash
        drop = pressure - p
        return draw(
            12,
            measure(p),
            GAS.format(P=pressure, rho=f"{density:g}", A=f"{area:g}") + f" ด้วยอัตราการไหล {flow} g/s ถ้าถือว่าความหนาแน่นคงที่ (P/ρ + v²/2 คงที่) ความดันที่ปลายเปิดเป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_1=P_0-\frac{Q^2}{2\rho_0A^2}",
            [measure(pressure - 2 * drop), measure(pressure + drop), measure(pressure - drop * 1e-8)],
        )


@_type(13, "อุณหภูมิของแก๊สที่ปลายหัวฉีดจากเลขมัค", NOZZLE_TOPIC)
class NozzleTemperature(PhysicsSheet):
    def _variant(self, rng):
        start = rng.randint(250, 600)
        mach = rng.randint(2, 10) / 10
        gamma = rng.choice((1.4, 5 / 3, 1.3))
        t = q13.solve(start=start, mach=mach, gamma=gamma)
        shown = "5/3" if gamma > 1.6 else f"{gamma:g}"
        return draw(
            13,
            measure(t),
            f"แก๊สอุดมคติ (γ = {shown}) อุณหภูมิ {start} K ในภาชนะใหญ่ไหลออกทางหัวฉีดแบบแอเดียแบติก ที่ปลายท่อมีเลขมัค {mach:g} อุณหภูมิที่ปลายท่อเป็นกี่เคลวิน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{c^2}{\gamma-1}+\frac{v^2}2=\text{คงที่}\Rightarrow T_1=\frac{T_0}{1+(\gamma-1)M^2/2}",
            [measure(start / (1 + (gamma - 1) * mach**2)), measure(start / (1 + gamma * mach**2 / 2)), measure(start * (1 - (gamma - 1) * mach**2 / 2))],
        )


@_type(14, "ความดันของแก๊สที่ปลายหัวฉีดจากเลขมัค", NOZZLE_TOPIC)
class NozzlePressure(PhysicsSheet):
    def _variant(self, rng):
        pressure = rng.randint(100, 500)
        mach = rng.randint(2, 10) / 10
        gamma = rng.choice((1.4, 5 / 3, 1.3))
        p = q14.solve(pressure=pressure, mach=mach, gamma=gamma)
        base = 1 + (gamma - 1) * mach**2 / 2
        shown = "5/3" if gamma > 1.6 else f"{gamma:g}"
        return draw(
            14,
            measure(p),
            f"แก๊สอุดมคติ (γ = {shown}) ในภาชนะใหญ่ความดัน {pressure} kPa ไหลออกทางหัวฉีดแบบแอเดียแบติก ที่ปลายท่อมีเลขมัค {mach:g} ความดันที่ปลายท่อเป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P\propto T^{\gamma/(\gamma-1)}\Rightarrow P_1=P_0\left[1+\tfrac{\gamma-1}2M^2\right]^{-\gamma/(\gamma-1)}",
            [measure(pressure * base ** (-1 / (gamma - 1))), measure(pressure * base ** (-gamma)), measure(pressure / base)],
        )


@_type(15, "อัตราการไหลของแก๊สจากอัตราส่วนความดัน", NOZZLE_TOPIC)
class NozzleFlow(PhysicsSheet):
    def _variant(self, rng):
        pressure, density, area = _gas(rng)
        ratio = rng.randint(55, 95) / 100
        gamma = 1.4
        q = q15.solve(pressure=pressure, density=density, area=area, ratio=ratio, gamma=gamma)
        a = area * 1e-4
        plain = a * sqrt(2 * density * pressure * 1e3 * (1 - ratio)) * 1e3
        same = q / ratio ** (1 / gamma)
        return draw(
            15,
            measure(q),
            GAS.format(P=pressure, rho=f"{density:g}", A=f"{area:g}") + f" แก๊สเป็นแก๊สอุดมคติ γ = 1.4 ขยายตัวแบบแอเดียแบติก ถ้าความดันที่ปลายเปิดเป็น {ratio:g} เท่าของความดันในภาชนะ อัตราการไหลเป็นกี่ g/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q^2=P_0\rho_0A^2\,\frac{2\gamma}{\gamma-1}\left(\beta^{2/\gamma}-\beta^{1+1/\gamma}\right)",
            [measure(q * sqrt((gamma - 1) / (2 * gamma))), measure(plain), measure(same)],
        )


@_type(16, "ความดันวิกฤติที่ให้อัตราการไหลสูงสุด", NOZZLE_TOPIC)
class NozzleCritical(PhysicsSheet):
    def _variant(self, rng):
        pressure = rng.randint(100, 800)
        gamma = rng.choice((1.4, 5 / 3, 1.3, 1.2))
        p = q16.solve(pressure=pressure, gamma=gamma)
        shown = "5/3" if gamma > 1.6 else f"{gamma:g}"
        return draw(
            16,
            measure(p),
            f"แก๊สอุดมคติ (γ = {shown}) ในภาชนะใหญ่ความดัน {pressure} kPa ไหลออกทางหัวฉีดแบบแอเดียแบติก อัตราการไหลสูงสุดเมื่อความดันที่ปลายท่อเป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{d}{d\beta}\left(\beta^{2/\gamma}-\beta^{1+1/\gamma}\right)=0\Rightarrow P_1^*=P_0\left(\frac{2}{\gamma+1}\right)^{\gamma/(\gamma-1)}",
            [measure(pressure / 2), measure(pressure * (2 / (gamma + 1)) ** (1 / (gamma - 1))), measure(pressure * 2 / (gamma + 1))],
        )


@_type(17, "อัตราการไหลสูงสุดของแก๊สผ่านหัวฉีด", NOZZLE_TOPIC)
class NozzleChoked(PhysicsSheet):
    def _variant(self, rng):
        pressure, density, area = _gas(rng)
        gamma = 1.4
        q = q17.solve(pressure=pressure, density=density, area=area, gamma=gamma)
        a, p0 = area * 1e-4, pressure * 1e3
        sound = sqrt(gamma * p0 / density)
        star = q16.solve(pressure=pressure, gamma=gamma) * 1e3
        rho_star = density * (2 / (gamma + 1)) ** (1 / (gamma - 1))
        return draw(
            17,
            measure(q),
            GAS.format(P=pressure, rho=f"{density:g}", A=f"{area:g}") + " แก๊สเป็นแก๊สอุดมคติ γ = 1.4 ขยายตัวแบบแอเดียแบติก อัตราการไหลสูงสุดที่เป็นไปได้เป็นกี่ g/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q_{\max}=\rho^*c^*A,\quad M=1",
            [measure(density * sound * a * 1e3), measure(a * sqrt(2 * density * (p0 - star)) * 1e3), measure(rho_star * sound * a * 1e3)],
        )


MU0 = 4e-7 * pi
AXIS = (17, 22, 24, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49, 52)


def _axis(rng):
    moment = rng.randint(20, 60) / 100
    fields = tuple(round(MU0 * moment / (2 * pi * (x * 1e-3) ** 3) * 1e3 * (1 + rng.randint(-30, 30) / 1000), 3) for x in AXIS)
    return fields


def _axis_table(fields):
    return ", ".join(f"({x}, {b:g})" for x, b in zip(AXIS, fields))


HALL = "วัดสนามแม่เหล็ก B บนแกนของแม่เหล็กทรงกระบอกสั้นรัศมี 5.00 mm ยาว 4.00 mm ที่ระยะ x จากกึ่งกลาง ได้ (x เป็น mm, B เป็น mT) = {t} โดย B(x) แปรผันตาม x^n"


@_type(18, "เลขชี้กำลังของสนามแม่เหล็กตามระยะบนแกนแม่เหล็ก", MAGNET_TOPIC)
class MagnetExponent(PhysicsSheet):
    def _variant(self, rng):
        fields = _axis(rng)
        n = q18.solve(fields=fields)
        lx = [log10(x) for x in AXIS]
        lb = [log10(b) for b in fields]
        mx, my = sum(lx) / len(lx), sum(lb) / len(lb)
        flip = sum((y - my) * (x - mx) for x, y in zip(lx, lb)) / sum((y - my) ** 2 for y in lb)
        return draw(
            18,
            measure(n),
            HALL.format(t=_axis_table(fields)) + " จากความชันของกราฟ log B กับ log x (วิธีกำลังสองน้อยที่สุด) ค่า n เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\log B=\log\frac{\mu_0m}{2\pi}+n\log x",
            [measure(n * log(10)), measure(flip), measure(-n)],
        )


@_type(19, "magnetization ของแม่เหล็กจากกราฟสนามตามระยะ", MAGNET_TOPIC)
class MagnetMagnetisation(PhysicsSheet):
    def _variant(self, rng):
        fields = _axis(rng)
        m = q19.solve(fields=fields)
        return draw(
            19,
            measure(m),
            HALL.format(t=_axis_table(fields)) + " และ B(x) = μ₀m/(2π)·xⁿ จากกราฟ log B กับ log x (วิธีกำลังสองน้อยที่สุด) magnetization ของแม่เหล็กเป็นกี่ ×10⁶ A/m (μ₀ = 4π×10⁻⁷ T m/A, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m=\frac{2\pi}{\mu_0}\,10^{\text{จุดตัด}},\quad M=\frac{m}{\pi R^2L}",
            [measure(m / 4), measure(2 * m), measure(m * 1000)],
        )


GAPS = (6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0)


@_type(20, "สนามอ้างอิง B0 ของลูปเหล็กที่มีช่องอากาศ", MAGNET_TOPIC)
class IronGap(PhysicsSheet):
    def _variant(self, rng):
        base = rng.randint(20, 40)
        offset = rng.randint(0, 20) / 10
        shape = [1 - (g / 2) / sqrt((g / 2) ** 2 + 25) for g in GAPS]
        fields = tuple(round(2 * base * u + offset + rng.randint(-3, 3) / 10, 1) for u in shape)
        b0 = q20.solve(fields=fields)
        wide = q20.solve(gaps=tuple(2 * g for g in GAPS), fields=fields)
        origin = sum(u * b for u, b in zip(shape, fields)) / sum(u * u for u in shape) / 2
        table = ", ".join(f"({g:g}, {b:g})" for g, b in zip(GAPS, fields))
        return draw(
            20,
            measure(b0),
            f"ลูปท่อนเหล็กรัศมี R = 5.0 mm ต่อกับแม่เหล็กถาวรมีช่องอากาศกว้าง 2d สนามที่กึ่งกลางช่องคือ B_g ≈ 2B₀(1 − d/√(d² + R²)) วัดได้ (2d เป็น mm, B_g เป็น mT) = {table} จากความชันของกราฟเส้นตรง (วิธีกำลังสองน้อยที่สุด) B₀ เป็นกี่มิลลิเทสลา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B_g=2B_0\left(1-\frac{d}{\sqrt{d^2+R^2}}\right)",
            [measure(2 * b0), measure(wide), measure(origin)],
        )


@_type(21, "magnetization จากฟลักซ์ครึ่งแท่งแม่เหล็ก", MAGNET_TOPIC)
class MagnetFlux(PhysicsSheet):
    def _variant(self, rng):
        flux = rng.randint(500, 1500) / 100
        radius = rng.randint(30, 80) / 10
        length = rng.randint(15, 50)
        m = q21.solve(flux=flux, radius=radius, length=length)
        r, half = radius * 1e-3, length * 1e-3 / 2
        bare = flux * 1e-5 / (MU0 * pi * r * r) / 1e6
        full = flux * 1e-5 * sqrt(r * r + 4 * half * half) / (MU0 * 2 * half * pi * r * r) / 1e6
        return draw(
            21,
            measure(m),
            f"ฟลักซ์แม่เหล็กที่ออกจากครึ่งบนของแท่งแม่เหล็กทรงกระบอกยาว {length} mm รัศมี {radius:g} mm วัดได้ {flux:g}×10⁻⁵ Wb โดย Φ ≈ μ₀M((L/2)/√(R² + (L/2)²))πR² magnetization เป็นกี่ ×10⁶ A/m (μ₀ = 4π×10⁻⁷ T m/A, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"M=\frac{\Phi\sqrt{R^2+(L/2)^2}}{\mu_0(L/2)\pi R^2}",
            [measure(bare), measure(full), measure(m / 4)],
        )


RINGS = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)


@_type(22, "ฟลักซ์แม่เหล็กจากการวัดสนามเป็นวงแหวน", MAGNET_TOPIC)
class RingFlux(PhysicsSheet):
    def _variant(self, rng):
        top = rng.randint(30, 50)
        fall = rng.randint(20, 30) / 10
        fields = tuple(round(top / x**fall * (1 + rng.randint(-50, 50) / 1000), 2) for x in RINGS)
        phi = q22.solve(fields=fields)
        disc = sum(b * 1e-3 * pi * (x * 1e-2) ** 2 for x, b in zip(RINGS, fields)) / 1e-5
        table = ", ".join(f"({x:g}, {b:g})" for x, b in zip(RINGS, fields))
        return draw(
            22,
            measure(phi),
            f"วัดสนามแม่เหล็กตั้งฉากกับระนาบผ่านกึ่งกลางแท่งแม่เหล็กยาว เป็นวงแหวนกว้าง 1 cm ที่มีรัศมีกลาง x ได้ (x เป็น cm, B เป็น mT) = {table} ฟลักซ์รวมผ่านระนาบนี้เป็นกี่ ×10⁻⁵ Wb (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Phi=\sum B_i\,2\pi x_i\,\Delta x",
            [measure(disc), measure(2 * phi), measure(phi * 1000)],
        )
