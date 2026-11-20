"""Seeded variants of the reviewed TPhO 11 (2555) national physics olympiad."""

from math import floor, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2555_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2555_physics import q11, q12, q13, q14, q15, q16, q17, q18

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
    1: ("phys.pinhole_hole_size_dropped", "phys.pinhole_half_angle", "phys.pinhole_angle_doubled"),
    2: ("phys.diffraction_one_edge_only", "phys.diffraction_slit_factor", "phys.diffraction_ignored"),
    3: ("phys.diffraction_one_edge_only", "phys.diffraction_slit_factor", "phys.diffraction_edges_doubled"),
    4: ("phys.pocket_ignored_equal_levels", "phys.pocket_initial_level_added", "phys.pocket_pressure_doubled"),
    5: ("phys.kinetic_half_missing", "phys.speed_not_rooted", "phys.grams_not_converted"),
    6: ("phys.kinetic_half_missing", "phys.cycle_average_applied_early", "phys.speed_not_squared"),
    7: ("phys.cycle_average_dropped", "phys.average_applied_to_energy", "phys.kinetic_half_missing"),
    8: ("phys.frequency_change_half_dropped", "phys.frequency_change_halved", "phys.frequency_change_rooted"),
    9: ("phys.energy_frequency_squared", "phys.energy_frequency_inverted", "phys.energy_frequency_rooted"),
    10: ("phys.conductor_as_charged_sheet", "phys.both_faces_counted_twice", "phys.coulomb_constant_for_sheet"),
    11: ("phys.hole_one_end_only", "phys.hole_ends_doubled", "phys.hole_ratio_inverted"),
    12: ("phys.conductor_as_charged_sheet", "phys.radial_field_as_axial", "phys.hole_ends_doubled"),
    13: ("phys.focus_exit_acceleration_ignored", "phys.focus_shift_only", "phys.conductor_as_charged_sheet"),
    14: ("phys.reference_shift_not_taken", "phys.first_reading_as_empty", "phys.slope_per_reading_not_per_nut"),
    15: ("phys.parallel_springs_not_shared", "phys.millimetres_not_converted", "phys.weight_as_mass"),
    16: ("phys.weight_as_mass", "phys.centimetres_not_converted", "phys.grams_not_converted"),
    17: ("phys.uniform_spring_third", "phys.effective_mass_for_coefficient", "phys.effective_mass_ratio_inverted"),
    18: ("phys.density_proportional_to_spacing", "phys.uniform_spring_third", "phys.effective_mass_half_spring"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 11 (2555)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2555_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2555_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


PINHOLE_TOPIC = "กล้องรูเข็มและการเลี้ยวเบน"
W_TOPIC = "ความดันอากาศในหลอดรูปตัว W"
DUST_TOPIC = "การสั่นของมวลติดสปริงที่ฝุ่นเกาะ"
HOLE_TOPIC = "สนามไฟฟ้าในรูของแผ่นประจุ"
CAPACITOR_TOPIC = "การวัดมวลแบบเทียบอ้างอิงด้วยตัวเก็บประจุ"
SPRING_TOPIC = "มวลยังผลของสปริง"

SUN = 0.0093
PINHOLE = "กล้องรูเข็มมีรูกลมเส้นผ่านศูนย์กลาง {a} mm อยู่หน้าฉากที่ห่างออกไป {L} cm ใช้ถ่ายภาพดวงอาทิตย์ซึ่งมีขนาดเชิงมุม 0.0093 rad"


@_type(1, "ขนาดภาพดวงอาทิตย์ในกล้องรูเข็ม", PINHOLE_TOPIC)
class PinholeImage(PhysicsSheet):
    def _variant(self, rng):
        hole = rng.randint(2, 10) / 10
        depth = rng.randint(2, 10) * 5
        size = q01.solve(hole=hole, depth=depth, angle=SUN)
        spread = depth * 10 * SUN
        return draw(
            1,
            measure(size),
            PINHOLE.format(a=f"{hole:g}", L=depth) + " ถ้าไม่คิดการเลี้ยวเบนของแสง ภาพดวงอาทิตย์บนฉากมีเส้นผ่านศูนย์กลางกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{a}{x}=\frac{A}{L+x},\quad \theta\approx\frac{a}{x}\Rightarrow A=a+L\theta",
            [measure(spread), measure(hole + spread / 2), measure(hole + 2 * spread)],
        )


@_type(2, "ขนาดภาพในกล้องรูเข็มเมื่อคิดการเลี้ยวเบน", PINHOLE_TOPIC)
class PinholeDiffraction(PhysicsSheet):
    def _variant(self, rng):
        hole = rng.randint(2, 8) / 10
        depth = rng.randint(2, 10) * 5
        wavelength = rng.randint(9, 13) * 50
        size = q02.solve(hole=hole, depth=depth, wavelength=wavelength, angle=SUN)
        base = hole + depth * 10 * SUN
        bend = wavelength * 1e-9 * depth * 1e-2 / (hole * 1e-3) * 1e3     # lambda L/a in mm
        return draw(
            2,
            measure(size),
            PINHOLE.format(a=f"{hole:g}", L=depth) + f" ผ่านแผ่นกรองแสงความยาวคลื่น {wavelength} nm เมื่อคิดการเลี้ยวเบนที่รู ภาพบนฉากมีเส้นผ่านศูนย์กลางประมาณกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\theta_{\text{diff}}=1.22\frac{\lambda}{a},\quad A=a+L\theta+2L\theta_{\text{diff}}",
            [measure(base + 1.22 * bend), measure(base + 2 * bend), measure(base)],
        )


@_type(3, "ขนาดรูเข็มที่ให้ภาพเล็กที่สุด", PINHOLE_TOPIC)
class PinholeBest(PhysicsSheet):
    def _variant(self, rng):
        depth = rng.randint(2, 10) * 5
        wavelength = rng.randint(9, 13) * 50
        a = q03.solve(wavelength=wavelength, depth=depth)
        lam_l = wavelength * 1e-9 * depth * 1e-2
        return draw(
            3,
            measure(a),
            f"กล้องรูเข็มมีฉากห่างจากรู {depth} cm ใช้แผ่นกรองแสงความยาวคลื่น {wavelength} nm ถ่ายภาพดวงอาทิตย์ เมื่อคิดทั้งขนาดรูและการเลี้ยวเบน (มุม 1.22λ/a ที่ขอบทั้งสองข้าง) รูควรมีเส้นผ่านศูนย์กลางกี่มิลลิเมตรภาพจึงเล็กที่สุด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"A=a+L\theta+\frac{2.44\lambda L}{a}\text{ น้อยที่สุดเมื่อ }a=\sqrt{2.44\lambda L}",
            [measure(sqrt(1.22 * lam_l) * 1e3), measure(sqrt(2 * lam_l) * 1e3), measure(sqrt(4.88 * lam_l) * 1e3)],
        )


@_type(4, "ระดับน้ำในหลอดรูปตัว W ขณะน้ำเริ่มล้น", W_TOPIC)
class WTubeLevel(PhysicsSheet):
    def _variant(self, rng):
        height = rng.randint(3, 20) * 2
        tall = q04.solve(height=height)
        return draw(
            4,
            str(int(tall)),
            f"หลอดแก้วเล็กรูปตัว W ปลายด้านสั้นสูง {height} cm ยอดตรงกลางของ W สูงเท่ากับปลายด้านสั้น เดิมมีน้ำสูง {height // 2} cm ทั้งสองข้าง "
            "แล้วเติมน้ำที่ปลายด้านที่สูงกว่าอย่างช้า ๆ อากาศที่ถูกขังเป็นของไหลที่อัดไม่ได้ ไม่คิดแรงตึงผิว "
            "ขณะน้ำเริ่มล้นจากปลายด้านสั้น ระดับน้ำด้านปลายที่สูงกว่าอยู่สูงกี่เซนติเมตร",
            r"P=P_a+\rho g h=P_a+\rho g(H-h)",
            [str(height), str(height * 3 // 2), str(height * 3)],
        )


SPRING_BLOCK = "ก้อนวัตถุมวล {m} g ติดสปริงเบาสั่นบนพื้นลื่นด้วยพลังงาน {E} mJ"


@_type(5, "อัตราเร็วสูงสุดของมวลติดสปริง", DUST_TOPIC)
class BlockTopSpeed(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(1, 20) * 25
        energy = rng.randint(1, 20) * 5
        u = q05.solve(mass=mass, energy=energy)
        return draw(
            5,
            measure(u),
            SPRING_BLOCK.format(m=mass, E=energy) + " ขณะผ่านจุดสมดุลมีอัตราเร็วกี่เมตรต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E_0=\tfrac12mu_0^2",
            [measure(u / sqrt(2)), measure(u * u), measure(u / sqrt(1000))],
        )


@_type(6, "พลังงานที่เสียไปเมื่อฝุ่นเกาะมวลที่เคลื่อนที่", DUST_TOPIC)
class DustLoss(PhysicsSheet):
    def _variant(self, rng):
        dust = rng.randint(1, 20) / 2
        speed = rng.randint(2, 20) / 10
        loss = q06.solve(dust=dust, speed=speed)
        return draw(
            6,
            measure(loss),
            f"ก้อนวัตถุติดสปริงเคลื่อนที่ด้วยอัตราเร็ว {speed:g} m/s ขณะนั้นฝุ่นที่ลอยนิ่งมวล {dust:g} mg มาเกาะ (มวลฝุ่นน้อยมากเทียบกับก้อนวัตถุ) พลังงานกลของระบบลดลงประมาณกี่ไมโครจูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"mv=(m+\Delta m)v',\quad \Delta E\approx-\tfrac12\Delta m\,v^2",
            [measure(2 * loss), measure(loss / 2), measure(0.5 * dust * speed)],
        )


@_type(7, "พลังงานที่เสียไปต่อรอบเมื่อฝุ่นเกาะ", DUST_TOPIC)
class DustCycleLoss(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(2, 20) * 25
        energy = rng.randint(1, 20) * 5
        dust = rng.randint(1, 20) / 2
        loss = q07.solve(mass=mass, energy=energy, dust=dust)
        return draw(
            7,
            measure(loss),
            SPRING_BLOCK.format(m=mass, E=energy) + f" ฝุ่นลอยนิ่งเกาะอย่างต่อเนื่องสม่ำเสมอ รวม {dust:g} mg ในหนึ่งรอบการสั่น (⟨v²⟩ = u₀²/2) พลังงานกลลดลงกี่ไมโครจูลในรอบนั้น (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta E=-\tfrac12\Delta m\langle v^2\rangle=-\frac{\Delta m}{2m}E_0",
            [measure(2 * loss), measure(loss / 2), measure(4 * loss)],
        )


@_type(8, "ความถี่เชิงมุมที่ลดลงเมื่อฝุ่นเกาะ", DUST_TOPIC)
class DustFrequencyDrop(PhysicsSheet):
    def _variant(self, rng):
        omega = rng.randint(4, 40)
        energy = rng.randint(2, 20) * 5
        loss = rng.randint(1, 50)
        drop = q08.solve(omega=omega, energy=energy, loss=loss) * 1000      # mrad/s
        return draw(
            8,
            measure(drop),
            f"ก้อนวัตถุติดสปริงสั่นด้วยความถี่เชิงมุม {omega} rad/s และพลังงาน {energy} mJ ฝุ่นลอยนิ่งเกาะทีละน้อยจนพลังงานกลลดลง {loss} µJ ความถี่เชิงมุมลดลงประมาณกี่มิลลิเรเดียนต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\omega^2=\frac{k}{m}\Rightarrow\frac{2\Delta\omega}{\omega_0}=-\frac{\Delta m}{m},\quad \Delta E=-\frac{\Delta m}{2m}E_0",
            [measure(2 * drop), measure(drop / 2), measure(omega * sqrt(loss * 1e-6 / (energy * 1e-3)) * 1000)],
        )


@_type(9, "พลังงานของมวลติดสปริงเมื่อความถี่เปลี่ยน", DUST_TOPIC)
class DustEnergyLater(PhysicsSheet):
    def _variant(self, rng):
        energy = rng.randint(2, 20) * 5
        omega = rng.randint(10, 40)
        later = rng.randint(omega // 3, omega - 2)
        e1 = q09.solve(energy=energy, omega=omega, later=later)
        ratio = later / omega
        return draw(
            9,
            measure(e1),
            f"ก้อนวัตถุติดสปริงสั่นด้วยพลังงาน {energy} mJ ความถี่เชิงมุม {omega} rad/s ฝุ่นลอยนิ่งเกาะอย่างต่อเนื่องจนความถี่เชิงมุมลดเหลือ {later} rad/s ระบบเหลือพลังงานกลกี่มิลลิจูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{\Delta E}{E}=y\frac{\Delta\omega}{\omega},\ \frac{\Delta E}{E_0}=\frac{\Delta\omega}{\omega_0}\Rightarrow y=1",
            [measure(energy * ratio**2), measure(energy / ratio), measure(energy * sqrt(ratio))],
        )


EPS0, E_CHARGE, M_PROTON = 8.85e-12, 1.6e-19, 1.67e-27
PLATE = "แผ่นตัวนำบางขนาดใหญ่มากหนา {d} mm มีประจุบวกกระจายสม่ำเสมอ {s} µC/m² ที่ผิวแต่ละด้าน (ε₀ = 8.85×10⁻¹² C²/N·m²)"


@_type(10, "สนามไฟฟ้านอกแผ่นตัวนำที่มีประจุ", HOLE_TOPIC)
class PlateField(PhysicsSheet):
    def _variant(self, rng):
        density = rng.randint(1, 40) / 4
        e = q10.solve(density=density)
        return draw(
            10,
            measure(e),
            PLATE.format(d="1.0", s=f"{density:g}") + " สนามไฟฟ้าที่แผ่ออกมาจากแผ่นตัวนำมีขนาดกี่กิโลโวลต์ต่อเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\oint\vec E\cdot d\vec A=\frac{Q}{\varepsilon_0},\quad Q=2\sigma A",
            [measure(e / 2), measure(2 * e), measure(e / (4 * pi))],
        )


@_type(11, "สนามไฟฟ้าแนวรัศมีในรูของแผ่นประจุ", HOLE_TOPIC)
class HoleRadialField(PhysicsSheet):
    def _variant(self, rng):
        thickness = rng.randint(2, 12) / 4
        radius = rng.randint(1, 16) / 4
        ratio = q11.solve(radius=radius, thickness=thickness)
        return draw(
            11,
            measure(ratio),
            PLATE.format(d=f"{thickness:g}", s="2") + f" แผ่นถูกเจาะเป็นรูกลมเส้นผ่านศูนย์กลาง {4 * radius + 2:g} mm (สนามนอกรูยังเหมือนเดิม และในรูสนามแนวรัศมีสม่ำเสมอตามแนวแกน) ที่ระยะ {radius:g} mm จากแกนของรู สนามไฟฟ้าแนวรัศมีมีขนาดเป็นกี่เท่าของสนามภายนอก (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2\pi r d\,E_r+2\pi r^2E=0",
            [measure(ratio / 2), measure(2 * ratio), measure(1 / ratio)],
        )


@_type(12, "ความเร็วแนวรัศมีของโปรตอนที่ผ่านรู", HOLE_TOPIC)
class HoleKick(PhysicsSheet):
    def _variant(self, rng):
        density = rng.randint(2, 8) / 4
        speed = rng.randint(4, 10) * 50
        radius = rng.randint(1, 8) / 8
        thickness = rng.choice((0.5, 1.0, 1.5, 2.0))
        if radius == thickness:
            raise _Clash
        v = q12.solve(density=density, speed=speed, radius=radius) / 1e3
        return draw(
            12,
            measure(v),
            PLATE.format(d=f"{thickness:g}", s=f"{density:g}")
            + f" มีรูกลมขนาดใหญ่กว่าความหนา ลำโปรตอน (m = 1.67×10⁻²⁷ kg, e = 1.6×10⁻¹⁹ C) ความเร็ว {speed} km/s วิ่งขนานแกนเข้าไปในรู โปรตอนที่อยู่ห่างแกน {radius:g} mm ผ่านออกจากรูด้วยความเร็วแนวรัศมีกี่กิโลเมตรต่อวินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F_r\Delta t=\frac{erE}{d}\cdot\frac{d}{u},\quad E=\frac{\sigma}{\varepsilon_0}",
            [measure(v / 2), measure(v * thickness / radius), measure(2 * v)],
        )


@_type(13, "ระยะโฟกัสของลำโปรตอนที่ผ่านรูของแผ่นประจุ", HOLE_TOPIC)
class HoleFocus(PhysicsSheet):
    def _variant(self, rng):
        density = rng.randint(2, 20) / 4
        speed = rng.randint(2, 10) * 50
        s = q13.solve(density=density, speed=speed)
        return draw(
            13,
            measure(s),
            PLATE.format(d="1.0", s=f"{density:g}")
            + f" มีรูกลม ลำโปรตอนความหนาแน่นต่ำ (m = 1.67×10⁻²⁷ kg, e = 1.6×10⁻¹⁹ C) ความเร็ว {speed} km/s วิ่งขนานแกนผ่านรู ลำโปรตอนถูกโฟกัสรวมกันที่ระยะกี่มิลลิเมตรจากแผ่น ไม่คิดแรงผลักระหว่างโปรตอน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta t'=\frac{r}{v_r}=\frac{mu}{eE},\quad s=u\Delta t'+\tfrac12\frac{eE}{m}\Delta t'^2",
            [measure(s * 2 / 3), measure(s / 3), measure(2 * s)],
        )


@_type(14, "มวลน็อตจากการเทียบความถี่กับแบตเตอรี่", CAPACITOR_TOPIC)
class NutMass(PhysicsSheet):
    def _variant(self, rng):
        battery = rng.randint(40, 50)
        nut = rng.randint(20, 50) / 10
        per_gram = rng.randint(5, 12) / 100             # kHz per gram
        empty = rng.randint(95, 110) / 10
        step = rng.choice((2, 3))
        counts = tuple(step * k for k in range(1, 6))
        freqs = tuple(round(empty - per_gram * nut * n + rng.choice((-0.01, 0, 0.01)), 2) for n in counts)
        loaded = round(empty - per_gram * battery, 2)
        if loaded <= 1:
            raise _Clash
        m = q14.solve(battery=battery, counts=counts, freqs=freqs, loaded=loaded)
        slope = -m * (empty - loaded) / battery
        table = ", ".join(f"({n} ตัว, {f:.2f} kHz)" for n, f in zip(counts, freqs))
        return draw(
            14,
            measure(m),
            "แผ่นทองแดงคู่ขนานคั่นด้วยท่อพลาสติกที่ทำหน้าที่เหมือนสปริง ต่อกับกล่องที่ให้ความถี่แปรผันตรงกับระยะห่างระหว่างแผ่น "
            f"วางหัวน็อตบนแผ่นบนแล้วอ่านความถี่ได้ (จำนวนน็อต, ความถี่) {table} เมื่อวางแบตเตอรี่มวล {battery} g อย่างเดียวอ่านได้ {loaded:.2f} kHz "
            "หาความชันและจุดตัดแกนด้วยวิธีกำลังสองน้อยที่สุด น็อตหนึ่งตัวมีมวลกี่กรัม (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"m_{\text{nut}}=m_{\text{batt}}\frac{|\Delta f/\Delta n|}{f_0-f_{\text{batt}}}",
            [
                measure(battery * -slope / loaded),
                measure(battery * -slope / (freqs[0] - loaded)),
                measure(m * step),
            ],
        )


@_type(15, "ค่าคงตัวสปริงของท่อพลาสติกจากความถี่", CAPACITOR_TOPIC)
class TubeStiffness(PhysicsSheet):
    def _variant(self, rng):
        per_mm = rng.randint(80, 120) / 100             # kHz per mm
        base = rng.randint(80, 110) / 10
        thickness = tuple(float(k) for k in range(5))
        freqs = tuple(round(base + per_mm * t + rng.choice((-0.01, 0, 0.01)), 2) for t in thickness)
        drop = rng.randint(20, 120) / 100                # kHz per 100 g
        k = q15.solve(thickness=thickness, freqs=freqs, drop=drop)
        table = ", ".join(f"({t:g} mm, {f:.2f} kHz)" for t, f in zip(thickness, freqs))
        return draw(
            15,
            measure(k),
            "แผ่นทองแดงคู่ขนานคั่นด้วยท่อพลาสติก 2 ท่อที่ทำหน้าที่เหมือนสปริง ต่อกับกล่องที่ให้ความถี่แปรผันตรงกับระยะห่างระหว่างแผ่น "
            f"สอดแผ่นพลาสติกหนา 1.0 mm เพิ่มระยะห่างแล้วอ่านความถี่ได้ (ความหนาที่เพิ่ม, ความถี่) {table} "
            f"และจากตอนที่ 1 มวล 100 g ที่วางบนแผ่นทำให้ความถี่ลดลง {drop:.2f} kHz ท่อพลาสติกหนึ่งท่อมีค่าคงตัวสปริงกี่นิวตันต่อเมตร (g = 9.81 m/s², ใช้วิธีกำลังสองน้อยที่สุด, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"k_{\text{รวม}}=\frac{mg}{\Delta x}=2k",
            [measure(2 * k), measure(k / 1000), measure(k / 9.81)],
        )


@_type(16, "ค่าคงตัวสปริงจากกราฟกฎของฮุก", SPRING_TOPIC)
class HookeSpring(PhysicsSheet):
    def _variant(self, rng):
        k = rng.randint(15, 60) / 10
        rest = rng.randint(150, 300) / 10
        clips = rng.choice((5, 10))
        masses = tuple(round(1.55 * clips * j, 2) for j in range(1, 6))
        lengths = tuple(round(rest + m * 1e-3 * 9.81 / k * 100 + rng.choice((-0.1, 0, 0.1)), 1) for m in masses)
        got = q16.solve(masses=masses, lengths=lengths)
        table = ", ".join(f"({m:g} g, {x:g} cm)" for m, x in zip(masses, lengths))
        return draw(
            16,
            measure(got),
            f"แขวนคลิป (ตัวละ 1.55 g) ที่ปลายสปริงในแนวดิ่ง วัดความยาวสปริงได้ (มวลที่แขวน, ความยาว) {table} "
            "จากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) สปริงมีค่าคงตัวกี่นิวตันต่อเมตร (g = 9.81 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"x=x_0+\frac{g}{k}M",
            [measure(got / 9.81), measure(got / 100), measure(got * 1000)],
        )


@_type(17, "สัมประสิทธิ์มวลยังผลของสปริงจากกราฟคาบ", SPRING_TOPIC)
class EffectiveMassFit(PhysicsSheet):
    def _variant(self, rng):
        k = rng.randint(20, 60) / 10
        spring = rng.randint(4, 12) * 5
        beta = rng.randint(26, 42) / 100
        masses = tuple(float(20 * j) for j in range(1, 6))
        periods = tuple(round(2 * pi * sqrt((m + beta * spring) * 1e-3 / k), 3) for m in masses)
        b = q17.solve(spring=spring, masses=masses, periods=periods)
        if abs(b - 1 / 3) < 0.01:
            raise _Clash
        table = ", ".join(f"({m:g} g, {t:.3f} s)" for m, t in zip(masses, periods))
        return draw(
            17,
            measure(b),
            f"สปริงมวล {spring} g แขวนมวล M แล้ววัดคาบการสั่นได้ (M, คาบ) {table} "
            "ใช้ ω = 2π/T = √(k/(M + β₁m)) เขียนกราฟเส้นตรงที่เหมาะสม (วิธีกำลังสองน้อยที่สุด) สัมประสิทธิ์มวลยังผล β₁ เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"T^2=\frac{4\pi^2}{k}M+\frac{4\pi^2\beta_1m}{k}",
            [measure(1 / 3), measure(b * spring), measure(1 / b)],
        )


@_type(18, "สัมประสิทธิ์มวลยังผลจากระยะยืดบนและล่าง", SPRING_TOPIC)
class EffectiveMassTurns(PhysicsSheet):
    def _variant(self, rng):
        bottom = rng.randint(3, 10)
        top = bottom + rng.randint(2, 15)
        b = q18.solve(top=top, bottom=bottom)
        return draw(
            18,
            measure(b),
            f"สปริงแขวนในแนวดิ่งมีมวลแขวนที่ปลาย ขดสปริงแต่ละขดมีมวลเท่ากัน ขดบนสุดยืดยาว {top} mm และขดล่างสุดยืดยาว {bottom} mm "
            "ความหนาแน่นเชิงเส้นจึงแปรผกผันกับความยาวขด ใช้ β₂ = (λ₀/6 + λₙ/2)/(λ₀ + λₙ) (λ₀ ด้านบน λₙ ด้านล่าง) สัมประสิทธิ์มวลยังผล β₂ เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\lambda\propto\frac{1}{\ell},\quad \beta_2=\frac{\lambda_0/6+\lambda_n/2}{\lambda_0+\lambda_n}",
            [measure((top / 6 + bottom / 2) / (top + bottom)), measure(1 / 3), measure(0.5)],
        )
