"""Seeded variants of the reviewed TPhO 16 (2560) national physics olympiad."""

from math import acos, cos, floor, log10, pi, sin, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2560_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2560_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

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
    1: ("phys.planet_frame_speed_reported", "phys.planet_energy_held_fixed", "phys.frame_speed_added"),
    2: ("phys.charles_ratio_inverted", "phys.pressure_scaled_by_volume_ratio", "phys.celsius_difference_ratio"),
    3: ("phys.efficiency_cv_for_cp", "phys.efficiency_isochoric_heat_dropped", "phys.efficiency_as_carnot"),
    4: ("phys.efficiency_as_carnot", "phys.efficiency_factor_five_dropped", "phys.efficiency_cv_for_cp"),
    5: ("phys.rayleigh_factor_dropped", "phys.radius_for_diameter", "phys.rayleigh_factor_doubled"),
    6: ("phys.angle_ratio_inverted", "phys.cone_spacing_doubled", "phys.angle_in_milliradians"),
    7: ("phys.cone_limit_for_diffraction", "phys.eye_depth_for_distance", "phys.rayleigh_factor_dropped"),
    8: ("phys.fringe_half_wavelength", "phys.index_offset_included", "phys.fringe_wavelength_in_medium"),
    9: ("phys.intensity_average_halved", "phys.intensity_phase_not_halved", "phys.intensity_sine_for_cosine"),
    10: ("phys.reference_phase_quarter", "phys.voltage_ratio_linear", "phys.fringe_phase_doubled"),
    11: ("phys.fringe_phase_halved", "phys.voltage_ratio_linear", "phys.fringe_phase_doubled"),
    12: ("phys.kinetic_half_missing", "phys.mev_as_ev", "phys.speed_not_rooted"),
    13: ("phys.dipole_one_wire", "phys.dipole_ring_length_used", "phys.dipole_angle_not_divided"),
    14: ("phys.beam_magnetic_force_ignored", "phys.beam_forces_added", "phys.beam_diameter_for_radius"),
    15: ("phys.beam_spread_half_dropped", "phys.beam_spread_quartered", "phys.beam_magnetic_force_ignored"),
    16: ("phys.quadrupole_one_pair", "phys.quadrupole_radius_not_squared", "phys.quadrupole_factor_two"),
    17: ("phys.kinetic_half_missing", "phys.lens_length_dropped", "phys.lens_half_length_impulse"),
    18: ("phys.doublet_single_lens", "phys.doublet_defocus_first", "phys.doublet_square_over_gap"),
    19: ("phys.log_slope_sign", "phys.log_slope_inverted", "phys.mass_axis_not_logged"),
    20: ("phys.weight_as_mass", "phys.grams_not_converted", "phys.drag_slope_inverted"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 16 (2560)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2560_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2560_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


IMPACT_TOPIC = "การชนของดาวเคราะห์กับก้อนหิน"
ENGINE_TOPIC = "เครื่องจักรความร้อนวัฏจักรสามเหลี่ยม"
EYE_TOPIC = "ขีดจำกัดการแยกภาพของตา"
MZ_TOPIC = "อุปกรณ์แทรกสอดมัคเซนเดอร์"
DIPOLE_TOPIC = "สนามแม่เหล็กในเครื่องเร่งอนุภาค"
QUAD_TOPIC = "การโฟกัสลำอนุภาคด้วย Quadrupole"
MAGNET_TOPIC = "แม่เหล็กนีโอดิเมียม"


@_type(1, "อัตราเร็วก้อนหินที่ถูกดาวเคราะห์พุ่งชน", IMPACT_TOPIC)
class PlanetImpact(PhysicsSheet):
    def _variant(self, rng):
        speed = rng.randint(2, 30)
        gravity, radius = rng.choice(((9.8, 6400), (3.7, 3400), (1.6, 1740), (24.8, 70000)))
        v = q01.solve(speed=speed, gravity=gravity, radius=radius)
        landing = sqrt((speed * 1e3) ** 2 + 2 * gravity * radius * 1e3) / 1e3
        return draw(
            1,
            measure(v),
            f"ก้อนหินลอยนิ่งในอวกาศ ดาวเคราะห์รัศมี {radius} km (ความเร่งโน้มถ่วงที่ผิว {gravity:g} m/s², ไม่มีบรรยากาศ) วิ่งเข้าชนตรง ๆ จากระยะไกลด้วยอัตราเร็ว {speed} km/s "
            "ผู้สังเกตในกรอบเดิมเห็นก้อนหินมีอัตราเร็วกี่กิโลเมตรต่อวินาทีขณะชนพื้นผิว (มวลก้อนหินน้อยมาก, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac12mu^2+\frac{GMm}{R}=\tfrac12mv_{\text{rel}}^2,\quad v=v_{\text{rel}}-u",
            [measure(landing), measure(sqrt(2 * gravity * radius * 1e3) / 1e3), measure(landing + speed)],
        )


ENGINE = "เครื่องจักรความร้อนใช้แก๊สอะตอมเดี่ยว ทำงานเป็นวัฏจักร A → B (ความดันคงที่) → C (เส้นตรง) → A (ปริมาตรคงที่) ที่ A ความดัน {p} atm ปริมาตร {v} L อุณหภูมิ {T} K ปริมาตรสูงสุดต่อต่ำสุด {r}:1 และอุณหภูมิต่ำสุด {Tc} K"


def _engine(rng):
    hot = rng.randint(6, 12) * 50
    cold = rng.randint(4, int(hot / 50) - 1) * 50
    return rng.randint(4, 20), rng.randint(2, 10) / 10, rng.randint(2, 8), hot, cold


@_type(2, "ความดันต่ำสุดของเครื่องจักรความร้อน", ENGINE_TOPIC)
class EngineLowPressure(PhysicsSheet):
    def _variant(self, rng):
        p, v, r, hot, cold = _engine(rng)
        low = q02.solve(pressure=p, hot=hot, cold=cold)
        return draw(
            2,
            measure(low),
            ENGINE.format(p=p, v=f"{v:g}", T=hot, r=r, Tc=cold) + " ความดันต่ำสุดของเครื่องจักรเป็นกี่ atm (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{p_A}{T_A}=\frac{p_C}{T_C}\ (V\ \text{คงที่})",
            [measure(p * hot / cold), measure(p / r), measure(p * (cold - 273.15) / (hot - 273.15))],
        )


@_type(3, "ประสิทธิภาพของเครื่องจักรวัฏจักรสามเหลี่ยม", ENGINE_TOPIC)
class EngineEfficiency(PhysicsSheet):
    def _variant(self, rng):
        p, v, r, hot, cold = _engine(rng)
        e = q03.solve(pressure=p, volume=v, ratio=r, hot=hot, cold=cold)
        drop = p * (1 - cold / hot)
        work = 0.5 * (r - 1) * v * drop
        return draw(
            3,
            measure(e),
            ENGINE.format(p=p, v=f"{v:g}", T=hot, r=r, Tc=cold) + " ประสิทธิภาพของเครื่องจักรเป็นกี่เปอร์เซ็นต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"e=\frac{W}{Q_{AB}+Q_{CA}},\quad Q_{AB}=\tfrac52p\Delta V,\ Q_{CA}=\tfrac32V\Delta p",
            [
                measure(100 * work / (1.5 * p * (r - 1) * v + 1.5 * v * drop)),
                measure(100 * work / (2.5 * p * (r - 1) * v)),
                measure(100 * (1 - cold / (hot * r))),
            ],
        )


@_type(4, "ประสิทธิภาพสูงสุดเมื่อเลื่อนจุด B", ENGINE_TOPIC)
class EngineBest(PhysicsSheet):
    def _variant(self, rng):
        _, _, _, hot, cold = _engine(rng)
        e = q04.solve(hot=hot, cold=cold)
        return draw(
            4,
            measure(e),
            f"เครื่องจักรความร้อนแก๊สอะตอมเดี่ยวทำงานเป็นวัฏจักร A → B (ความดันคงที่) → C (เส้นตรง) → A (ปริมาตรคงที่) อุณหภูมิที่ A เป็น {hot} K และต่ำสุด (ที่ C) {cold} K "
            "ถ้าเลื่อนจุด B ไปทางขวาโดยความดันเท่าเดิม ประสิทธิภาพเข้าใกล้ค่าสูงสุดกี่เปอร์เซ็นต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"e(x)=\frac{(x-1)\Delta p}{5p_A(x-1)+3\Delta p}\to\frac{\Delta p}{5p_A}",
            [measure(100 * (1 - cold / hot)), measure(100 * (1 - cold / hot) / 2), measure(100 * (1 - cold / hot) / 3)],
        )


@_type(5, "ขีดจำกัดการแยกภาพจากการเลี้ยวเบนของรูม่านตา", EYE_TOPIC)
class EyeDiffraction(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.randint(40, 70) * 10
        pupil = rng.randint(15, 60) / 10
        angle = q05.solve(wavelength=wavelength, pupil=pupil)
        return draw(
            5,
            measure(angle),
            f"รูม่านตามีเส้นผ่านศูนย์กลาง {pupil:g} mm มองแสงความยาวคลื่น {wavelength} nm ขนาดเชิงมุมที่เล็กที่สุดที่แยกจุดสองจุดได้ (ขีดจำกัดการเลี้ยวเบน) เป็นกี่ไมโครเรเดียน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\theta=1.22\frac{\lambda}{D}",
            [measure(angle / 1.22), measure(2 * angle), measure(angle * 1.22)],
        )


@_type(6, "ขีดจำกัดการแยกภาพจากระยะห่างเซลรับแสง", EYE_TOPIC)
class EyeCones(PhysicsSheet):
    def _variant(self, rng):
        cone = rng.randint(5, 30) / 10
        depth = rng.randint(18, 26)
        angle = q06.solve(cone=cone, depth=depth)
        return draw(
            6,
            measure(angle),
            f"เซลรับแสงบนเรตินาอยู่ห่างกัน {cone:g} µm และเรตินาอยู่ลึกจากรูม่านตา {depth} mm ถ้าไม่คิดการเลี้ยวเบน ขนาดเชิงมุมที่เล็กที่สุดที่แยกจุดสองจุดได้เป็นกี่ไมโครเรเดียน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\theta=\frac{\text{ระยะระหว่างเซล}}{\text{ระยะรูม่านตาถึงเรตินา}}",
            [measure(depth * 1e-3 / (cone * 1e-6)), measure(2 * angle), measure(angle / 1000)],
        )


@_type(7, "ระยะห่างพิกเซลที่ตาแยกไม่ได้", EYE_TOPIC)
class EyePixels(PhysicsSheet):
    def _variant(self, rng):
        distance = rng.randint(20, 80)
        wavelength = rng.randint(45, 65) * 10
        pupil = rng.randint(15, 40) / 10
        spacing = q07.solve(distance=distance, wavelength=wavelength, pupil=pupil)
        return draw(
            7,
            measure(spacing),
            f"รูม่านตาเส้นผ่านศูนย์กลาง {pupil:g} mm เซลรับแสงห่างกัน 1.0 µm ที่ระยะ 24 mm หลังรูม่านตา มองจอห่าง {distance} cm ด้วยแสง {wavelength} nm "
            "ระยะระหว่างพิกเซลที่อยู่ติดกันต้องน้อยกว่ากี่ไมโครเมตร ตาจึงแยกพิกเซลไม่ออกเมื่อคิดทั้งการเลี้ยวเบนและเซลรับแสง (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{ระยะพิกเซล}=x\,\theta_{\max},\quad \theta_{\max}=\max\left(1.22\frac{\lambda}{D},\frac{1.0\ \mu\text{m}}{24\ \text{mm}}\right)",
            [measure(distance * 1e-2 * 1e-6 / 24e-3 * 1e6), measure(24e-3 * 1.22 * wavelength * 1e-9 / (pupil * 1e-3) * 1e6), measure(spacing / 1.22)],
        )


MZ = "อุปกรณ์แทรกสอดมัคเซนเดอร์มีท่อยาว {L} cm บรรจุน้ำเปล่าในเส้นทางหนึ่งและสารละลายน้ำตาลอีกเส้นทางหนึ่ง ดัชนีหักเห n = 1.33 + {a}h (h = มวลน้ำตาล/มวลน้ำ) แสงในสุญญากาศยาว {lam} nm"


@_type(8, "ความเข้มข้นที่เปลี่ยนต่อหนึ่งริ้วการแทรกสอด", MZ_TOPIC)
class MzFringe(PhysicsSheet):
    def _variant(self, rng):
        length = rng.randint(5, 30) / 10
        alpha = rng.choice((0.12, 0.146, 0.15, 0.18))
        wavelength = rng.choice((450, 532, 550, 633))
        dh = q08.solve(wavelength=wavelength, length=length, alpha=alpha)
        return draw(
            8,
            measure(dh),
            MZ.format(L=f"{length:g}", a=f"{alpha:g}", lam=wavelength) + " ความเข้มข้น h ต้องเปลี่ยนไปกี่ ppm (ส่วนในล้าน) ความสว่างที่ตัวรับแสงจึงเปลี่ยนไปหนึ่งริ้ว (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\alpha\,\Delta h\,L=\lambda_0",
            [measure(dh / 2), measure(dh * 1.33), measure(dh / 1.33)],
        )


@_type(9, "ความเข้มแสงเฉลี่ยที่พอร์ตสว่าง", MZ_TOPIC)
class MzIntensity(PhysicsSheet):
    def _variant(self, rng):
        conc = rng.randint(2, 30) * 10
        intensity = q09.solve(conc=conc)
        phase = 2 * pi * 1e-2 * 0.146 * conc * 1e-6 / 550e-9
        return draw(
            9,
            measure(intensity),
            MZ.format(L="1.0", a="0.146", lam=550) + f" ความเข้มข้น h = {conc} ppm แสงแต่ละเส้นทางมีความเข้มสูงสุด I₀ ที่พอร์ตสว่าง ความเข้มแสงเฉลี่ยรวมเป็นกี่เท่าของ I₀ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\varphi=\frac{2\pi L\alpha h}{\lambda_0},\quad\langle I\rangle=2I_0\cos^2\frac{\varphi}{2}",
            [measure(intensity / 2), measure(2 * cos(phase) ** 2), measure(2 * sin(phase / 2) ** 2)],
        )


@_type(10, "ความเข้มข้นที่เปลี่ยนจากค่าความต่างศักย์ที่อ่านได้", MZ_TOPIC)
class MzReading(PhysicsSheet):
    def _variant(self, rng):
        reading = rng.randint(52, 90) / 100
        dh = q10.solve(reading=reading)
        k = pi * 1e-2 * 0.146 / 550e-9
        quarter = (acos(-sqrt(reading)) - 0.25 * pi) / k * 1e6
        return draw(
            10,
            measure(dh),
            MZ.format(L="1.0", a="0.146", lam=550) + f" ตัวรับแสงที่พอร์ตสว่างให้ V = (1.0 V)cos²(πLαh/λ₀) ค่าอ้างอิง h₀ ให้ 0.50 V บนช่วงที่ V เพิ่มตาม h ถ้าวัดได้ {reading:.2f} V ความเข้มข้นต่างจาก h₀ กี่ ppm (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V=V_{\max}\cos^2\theta,\quad \theta=\frac{\pi L\alpha h}{\lambda_0}",
            [measure(quarter), measure((reading - 0.5) / k * 1e6), measure(2 * dh)],
        )


@_type(11, "ความเข้มข้นที่ตีความผิดเมื่อแสงผันผวน", MZ_TOPIC)
class MzFluctuation(PhysicsSheet):
    def _variant(self, rng):
        bright = rng.randint(102, 140) / 100
        dh = q11.solve(bright=bright)
        k = pi * 1e-2 * 0.146 / 550e-9
        return draw(
            11,
            measure(dh),
            MZ.format(L="1.0", a="0.146", lam=550) + f" ตัวรับแสงเคยให้ค่าสูงสุด 1.0 V และค่าอ้างอิง h₀ ให้ 0.50 V บนช่วงที่ V เพิ่มตาม h ถ้าแหล่งแสงสว่างขึ้นจนค่าสูงสุดเป็น {bright:.2f} V โดยที่ h ยังเท่า h₀ "
            "ผู้ทดลองที่ไม่รู้จะตีความว่า h มากกว่าค่าอ้างอิงกี่ ppm (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"V=V'_{\max}\cos^2\theta_0,\quad 1.0\cos^2\theta'=V",
            [measure(dh / 2), measure((bright * 0.5 - 0.5) / k * 1e6), measure(2 * dh)],
        )


MP, QE = 1.67e-27, 1.6e-19


@_type(12, "อัตราเร็วโปรตอนจากพลังงานจลน์", DIPOLE_TOPIC)
class ProtonSpeed(PhysicsSheet):
    def _variant(self, rng):
        energy = rng.randint(5, 50) / 5
        v = q12.solve(energy=energy)
        return draw(
            12,
            measure(v),
            f"โปรตอน (มวล 1.67×10⁻²⁷ kg) มีพลังงานจลน์ {energy:g} MeV (1 eV = 1.6×10⁻¹⁹ J, ไม่คิดผลสัมพัทธภาพ) มีอัตราเร็วกี่ ×10⁷ m/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E_k=\tfrac12mv^2",
            [measure(v / sqrt(2)), measure(v / 1000), measure(v * v)],
        )


@_type(13, "กระแสในไดโพลแม่เหล็กของเครื่องเร่งอนุภาค", DIPOLE_TOPIC)
class DipoleCurrent(PhysicsSheet):
    def _variant(self, rng):
        energy = rng.randint(2, 10)
        length = rng.randint(10, 40) / 10
        radius = rng.randint(2, 8)
        count = rng.choice((8, 10, 12, 16, 20))
        current = q13.solve(energy=energy, length=length, radius=radius, count=count)
        return draw(
            13,
            measure(current),
            f"เครื่องเร่งอนุภาคจำลองมีไดโพลแม่เหล็ก {count} ชิ้น แต่ละชิ้นเป็นลวดยาว {length:g} m สองเส้นห่างกัน {2 * radius} cm กระแสไหลสวนกัน (สนามที่แกน μ₀I/(πR)) "
            f"ลำโปรตอนพลังงาน {energy} MeV ต้องเลี้ยวครบรอบพอดีเมื่อผ่านไดโพลทั้งหมด กระแสต้องเป็นกี่กิโลแอมแปร์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{mv}{qB}=\frac{ND}{2\pi},\quad B=\frac{\mu_0I}{\pi R}",
            [measure(2 * current), measure(current * 400 / (count * length)), measure(current * 2 * pi)],
        )


BEAM = "ลำโปรตอนทรงกระบอกยาว {l} cm รัศมี {r} mm มีโปรตอน {n}×10⁶ ตัวกระจายสม่ำเสมอ พลังงานจลน์ {E} MeV (ε₀ = 8.85×10⁻¹² และ μ₀ = 4π×10⁻⁷ หน่วย SI)"


def _beam(rng):
    return rng.randint(1, 10), rng.randint(2, 10), rng.randint(5, 20) / 10, rng.randint(10, 40)


@_type(14, "ความเร่งแนวรัศมีที่ขอบลำโปรตอน", DIPOLE_TOPIC)
class BeamPush(PhysicsSheet):
    def _variant(self, rng):
        count, energy, radius, length = _beam(rng)
        a = q14.solve(count=count, energy=energy, radius=radius, length=length)
        v = sqrt(2 * energy * 1e6 * QE / MP)
        gamma = 1 - v * v / 9e16
        return draw(
            14,
            measure(a),
            BEAM.format(l=length, r=f"{radius:g}", n=count, E=energy) + " โปรตอนที่ขอบลำมีความเร่งในแนวรัศมีกี่ ×10⁸ m/s² (คิดทั้งแรงไฟฟ้าและแรงแม่เหล็ก, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=\frac{nq^2}{2\pi\varepsilon_0\ell r_0}\left(1-\frac{v^2}{c^2}\right)",
            [measure(a / gamma), measure(a * (2 - gamma) / gamma), measure(a / 2)],
        )


@_type(15, "อัตราการขยายตัวของรัศมีลำโปรตอน", DIPOLE_TOPIC)
class BeamSpread(PhysicsSheet):
    def _variant(self, rng):
        count, energy, radius, length = _beam(rng)
        beta = q15.solve(count=count, energy=energy, radius=radius, length=length)
        v = sqrt(2 * energy * 1e6 * QE / MP)
        return draw(
            15,
            measure(beta),
            BEAM.format(l=length, r=f"{radius:g}", n=count, E=energy) + " รัศมีลำเปลี่ยนตาม r = r₀ + βz² เมื่อลำเคลื่อนไปตามแกน z ค่า β เป็นกี่ ×10⁻⁷ m⁻¹ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"z=vt,\quad a_0=2\beta v^2",
            [measure(2 * beta), measure(beta / 2), measure(beta / (1 - v * v / 9e16))],
        )


@_type(16, "เกรเดียนต์สนามแม่เหล็กของ Quadrupole", QUAD_TOPIC)
class QuadGradient(PhysicsSheet):
    def _variant(self, rng):
        current = rng.randint(1, 50) * 20
        radius = rng.randint(10, 60) / 10
        b = q16.solve(current=current, radius=radius)
        return draw(
            16,
            measure(b),
            f"Magnetic Quadrupole มีลวดยาวขนานกันสี่เส้นวางที่ระยะ {radius:g} cm จากแกนกลาง กระแส {current} A ในแต่ละเส้น โดยลวดที่อยู่ตรงข้ามกันมีกระแสทิศเดียวกัน "
            "ใกล้แกนกลางสนามเป็น B = ayî + bxĵ ค่า b เป็นกี่เทสลาต่อเมตร (μ₀ = 4π×10⁻⁷, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B_y\approx\frac{2\mu_0Ix}{\pi R^2}",
            [measure(b / 2), measure(b * radius * 1e-2), measure(2 * b)],
        )


@_type(17, "ความยาวโฟกัสของเลนส์แม่เหล็ก", QUAD_TOPIC)
class QuadFocal(PhysicsSheet):
    def _variant(self, rng):
        gradient = rng.randint(2, 30) / 10
        depth = rng.randint(5, 30)
        energy = rng.randint(2, 10)
        f = q17.solve(gradient=gradient, depth=depth, energy=energy)
        return draw(
            17,
            measure(f),
            f"โปรตอนพลังงาน {energy} MeV เคลื่อนที่ขนานแกนผ่าน Quadrupole ยาว {depth} cm ที่มีเกรเดียนต์สนาม b = {gradient:g} T/m ในระนาบที่เป็นเลนส์นูน ความยาวโฟกัสเป็นกี่เมตร (ประมาณเลนส์บาง, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta p_x=qvbx\frac{d}{v},\quad f=\frac{mv}{bqd}",
            [measure(f / sqrt(2)), measure(f * depth * 1e-2), measure(2 * f)],
        )


@_type(18, "ความยาวโฟกัสของ Quadrupole คู่", QUAD_TOPIC)
class QuadDoublet(PhysicsSheet):
    def _variant(self, rng):
        focal = rng.randint(5, 50)
        gap = rng.randint(1, max(2, focal // 3))
        if gap >= focal:
            raise _Clash
        f = q18.solve(focal=focal, gap=gap)
        return draw(
            18,
            measure(f),
            f"Quadrupole สองชิ้นวางห่างกัน {gap} m และกลับทิศกระแส ตัวแรกเป็นเลนส์นูนความยาวโฟกัส {focal} m และตัวที่สองเป็นเลนส์เว้าความยาวโฟกัสขนาดเท่ากันในแกน x ระบบโฟกัสลำขนานที่ระยะกี่เมตรหลังตัวที่สอง (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{1}{f'}=\frac{1}{-f}+\frac{1}{f-L}\Rightarrow f'=\frac{f(f-L)}{L}",
            [measure(focal), measure(focal * (focal + gap) / gap), measure(focal * focal / gap)],
        )


DISTANCES = (26.0, 27.7, 29.8, 31.5, 34.4, 37.6, 41.1)


@_type(19, "เลขชี้กำลังของแรงแม่เหล็กกับระยะห่าง", MAGNET_TOPIC)
class MagnetPower(PhysicsSheet):
    def _variant(self, rng):
        power = -rng.randint(30, 45) / 10
        top = rng.randint(50, 80)
        masses = tuple(round(top * (r / DISTANCES[0]) ** power * (1 + rng.choice((-0.01, 0, 0.01))), 1) for r in DISTANCES)
        n = q19.solve(distances=DISTANCES, masses=masses)
        n_lin = sum((r - sum(DISTANCES) / 7) * (m - sum(masses) / 7) for r, m in zip(DISTANCES, masses)) / sum((r - sum(DISTANCES) / 7) ** 2 for r in DISTANCES)
        table = ", ".join(f"({r:g} mm, {m:g} g)" for r, m in zip(DISTANCES, masses))
        return draw(
            19,
            measure(n),
            f"แม่เหล็กกระดุมสองก้อนดูดกันผ่านแผ่นฐาน เพิ่มแผ่นใต้ฐานจนแม่เหล็กก้อนล่างหลุดพอดี วัด (ระยะระหว่างกึ่งกลางแม่เหล็ก r, มวลที่ห้อยได้ M) ได้ {table} "
            "ถ้าแรงแม่เหล็ก ∝ rⁿ ค่า n จากกราฟ log M กับ log r (วิธีกำลังสองน้อยที่สุด) เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Mg=br^n\Rightarrow\log M=n\log r+\log\frac{b}{g}",
            [measure(-n), measure(1 / n), measure(n_lin)],
        )


@_type(20, "ค่าคงตัวของแรงเบรกแม่เหล็กในท่ออะลูมิเนียม", MAGNET_TOPIC)
class MagnetBraking(PhysicsSheet):
    def _variant(self, rng):
        k = rng.randint(15, 40) / 100
        tube = rng.choice((0.80, 1.00, 1.01, 1.20))
        masses = tuple(round(7.60 + 0.94 * j, 2) for j in range(0, 12, 2))
        times = tuple(round(k * tube / (9.78 * m * 1e-3) * (1 + rng.choice((-0.01, 0, 0.01))), 2) for m in masses)
        got = q20.solve(masses=masses, times=times, tube=tube)
        table = ", ".join(f"({m:g} g, {t:.2f} s)" for m, t in zip(masses, times))
        return draw(
            20,
            measure(got),
            f"แม่เหล็กตกในท่ออะลูมิเนียมยาว {tube:g} m ด้วยอัตราเร็วสุดท้ายตลอดทาง (แรงต้าน kv) เปลี่ยนมวลด้วยลูกปัดแล้วจับเวลาได้ (มวล, เวลา) {table} "
            "จากความชันของกราฟเวลากับ 1/มวล (วิธีกำลังสองน้อยที่สุด) k เป็นกี่ kg/s (g = 9.78 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mg=k\frac{s}{t}\Rightarrow t=\frac{ks}{g}\cdot\frac1m",
            [measure(got / 9.78), measure(got * 1000), measure(1 / got)],
        )
