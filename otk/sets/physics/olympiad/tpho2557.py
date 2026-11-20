"""Seeded variants of the reviewed TPhO 13 (2557) national physics olympiad."""

from math import floor, log10, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2557_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2557_physics import q11, q12, q13, q14, q15, q16, q17
from otk.sheets.tpho2557_physics.q14 import _points

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
    1: ("phys.wedge_round_trip_dropped", "phys.wedge_index_dropped", "phys.wedge_index_inverted"),
    2: ("phys.wedge_round_trip_dropped", "phys.wedge_index_dropped", "phys.wedge_index_inverted"),
    3: ("phys.doppler_full_speed_at_closest", "phys.doppler_receding_formula", "phys.doppler_source_as_observer"),
    4: ("phys.doppler_retardation_ignored", "phys.doppler_offset_for_distance", "phys.doppler_retardation_sign"),
    5: ("phys.table_tipping_ignored", "phys.table_torque_sign", "phys.stopping_distance_half"),
    6: ("phys.tipping_half_dropped", "phys.tipping_ratio_inverted", "phys.tipping_height_doubled"),
    7: ("phys.reversed_table_half", "phys.table_dims_swapped", "phys.ratio_denominator_dropped"),
    8: ("phys.water_hammer_as_bernoulli", "phys.water_hammer_speed_squared", "phys.water_hammer_half"),
    9: ("phys.bulk_speed_factor_two", "phys.gigapascal_not_converted", "phys.density_in_grams"),
    10: ("phys.water_hammer_as_bernoulli", "phys.water_hammer_half", "phys.torricelli_factor_two_dropped"),
    11: ("phys.dielectric_total_for_polarisation", "phys.dielectric_external_for_polarisation", "phys.dielectric_factor_inverted"),
    12: ("phys.dielectric_total_for_polarisation", "phys.dielectric_external_for_polarisation", "phys.dielectric_factor_inverted"),
    13: ("phys.wheel_axle_radius_dropped", "phys.two_wheels_counted_once", "phys.field_not_rooted"),
    14: ("phys.damping_slope_inverted", "phys.weight_as_mass", "phys.terminal_speed_cos_dropped"),
    15: ("phys.intercept_as_coefficient", "phys.friction_intercept_ratio_inverted", "phys.terminal_speed_cos_dropped"),
    16: ("phys.conductivity_ratio_inverted", "phys.conductivity_product", "phys.time_constant_for_damping"),
    17: ("phys.radius_for_diameter", "phys.field_not_squared", "phys.magnet_thickness_for_plate"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 13 (2557)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2557_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2557_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


WEDGE_TOPIC = "การแทรกสอดในลิ่มใส"
DOPPLER_TOPIC = "ปรากฏการณ์ดอปเพลอร์ของแหล่งกำเนิดที่ผ่านหน้า"
TABLE_TOPIC = "โต๊ะมีล้อด้านเดียว"
RAM_TOPIC = "ตะบันน้ำ"
DIELECTRIC_TOPIC = "ไดอิเล็กทริกเคลื่อนที่ในสนามแม่เหล็ก"
BRAKE_TOPIC = "กระแสไหลวนและเบรกแม่เหล็ก"

INDICES = (1.45, 1.50, 1.52, 1.60)


@_type(1, "ระยะห่างริ้วการแทรกสอดในลิ่มใส", WEDGE_TOPIC)
class WedgeSpacing(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.randint(40, 70) * 10
        n = rng.choice(INDICES)
        angle = rng.randint(1, 10)
        dx = q01.solve(wavelength=wavelength, index=n, angle=angle)
        return draw(
            1,
            measure(dx),
            f"แสงความยาวคลื่น {wavelength} nm ตกกระทบตั้งฉากลงบนลิ่มแก้วใสดัชนีหักเห {n} ซึ่งเอียงทำมุม {angle} mrad แสงที่สะท้อนจากผิวบนและผิวล่างแทรกสอดกัน ริ้วสว่างที่อยู่ติดกันห่างกันในแนวราบกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2ny=\left(N+\tfrac12\right)\lambda,\quad y=x\tan\theta",
            [measure(2 * dx), measure(dx * n), measure(dx * n * n)],
        )


@_type(2, "สัมประสิทธิ์การขยายตัวจากริ้วที่เลื่อน", WEDGE_TOPIC)
class WedgeExpansion(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.randint(50, 65) * 10
        n = 1.5
        length = rng.randint(5, 12)
        angle = rng.randint(20, 50)
        warming = rng.randint(2, 10) * 10
        fringes = rng.randint(5, 30)
        alpha = q02.solve(wavelength=wavelength, index=n, length=length, angle=angle, warming=warming, fringes=fringes)
        if not 2 <= alpha <= 30:
            raise _Clash
        return draw(
            2,
            measure(alpha),
            f"ลิ่มแก้วใสยาว {length} cm ดัชนีหักเห 1.5 เอียงทำมุม {angle} mrad ปลายด้านหนาถูกตรึงไว้ ส่องด้วยแสงความยาวคลื่น {wavelength} nm "
            f"เมื่อให้ความร้อนจนอุณหภูมิเพิ่มขึ้น {warming} K เห็นริ้วการแทรกสอดเลื่อนผ่านไป {fringes} ริ้ว (ดัชนีหักเหไม่เปลี่ยน) สัมประสิทธิ์การขยายตัวเชิงเส้นเป็นกี่ ×10⁻⁶ K⁻¹ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta N=\frac{2n\,\alpha L_0\Delta T\tan\theta}{\lambda}",
            [measure(2 * alpha), measure(alpha * n), measure(alpha * n * n)],
        )


SOUND = 340


@_type(3, "ความถี่ที่ได้ยินเมื่อแหล่งกำเนิดอยู่ใกล้ที่สุด", DOPPLER_TOPIC)
class DopplerClosest(PhysicsSheet):
    def _variant(self, rng):
        base = rng.randint(30, 100) * 10
        speed = rng.randint(6, 16) * 10
        shift = q03.solve(base=base, speed=speed, sound=SOUND)
        return draw(
            3,
            measure(shift),
            f"แหล่งกำเนิดเสียงความถี่ {base} Hz เคลื่อนที่เป็นเส้นตรงด้วยอัตราเร็ว {speed} m/s ผ่านผู้สังเกตที่อยู่ห่างจากแนวเส้นตรงระยะหนึ่ง (อัตราเร็วเสียง {SOUND} m/s) "
            "ขณะที่แหล่งกำเนิดอยู่ใกล้ผู้สังเกตมากที่สุด ผู้สังเกตได้ยินเสียงความถี่สูงกว่า f₀ กี่เฮิรตซ์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\cos\theta=\frac{u}{v},\quad f=\frac{v}{v-u\cos\theta}f_0",
            [
                measure(base * speed / (SOUND - speed)),
                measure(base * speed / (SOUND + speed)),
                measure(base * speed**2 / SOUND**2),
            ],
        )


@_type(4, "ระยะแหล่งกำเนิดเมื่อได้ยินความถี่เดิม", DOPPLER_TOPIC)
class DopplerUnshifted(PhysicsSheet):
    def _variant(self, rng):
        distance = rng.randint(2, 20) * 10
        speed = rng.randint(6, 16) * 10
        d = q04.solve(distance=distance, speed=speed, sound=SOUND)
        return draw(
            4,
            measure(d),
            f"แหล่งกำเนิดเสียงความถี่ f₀ เคลื่อนที่เป็นเส้นตรงด้วยอัตราเร็ว {speed} m/s ผู้สังเกตอยู่ห่างจากแนวเส้นตรงเป็นระยะตั้งฉาก {distance} m (อัตราเร็วเสียง {SOUND} m/s) "
            "ขณะที่ผู้สังเกตได้ยินเสียงความถี่ f₀ พอดี แหล่งกำเนิดอยู่ห่างจากผู้สังเกตกี่เมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"t=\frac{L}{v},\quad x=ut",
            [measure(distance), measure(distance * speed / SOUND), measure(distance * sqrt(SOUND**2 - speed**2) / SOUND)],
        )


TABLE = "โต๊ะกว้าง {w} m จุดศูนย์กลางมวลอยู่กึ่งกลางสูง {h} m ขาหลังมีล้อเบาหมุนได้ไม่มีฝืด ขาหน้าไม่มีล้อ สัมประสิทธิ์ความเสียดทานกับพื้น {mu} (g = 9.8 m/s²)"


def _table(rng):
    while True:
        width = rng.randint(6, 15) / 10
        height = rng.randint(4, 12) / 10
        mu = rng.randint(10, 60) / 100
        if mu < 0.9 * width / (2 * height):
            return width, height, mu


@_type(5, "ระยะไถลของโต๊ะมีล้อด้านเดียว", TABLE_TOPIC)
class TableSlide(PhysicsSheet):
    def _variant(self, rng):
        width, height, mu = _table(rng)
        speed = rng.randint(10, 40) / 10
        s = q05.solve(speed=speed, width=width, height=height, mu=mu)
        return draw(
            5,
            measure(s),
            TABLE.format(w=f"{width:g}", h=f"{height:g}", mu=f"{mu:g}") + f" โต๊ะเคลื่อนที่ไปข้างหน้าด้วยอัตราเร็วต้น {speed:g} m/s โต๊ะเคลื่อนที่ได้ไกลกี่เมตรจึงหยุด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"N_1\left(\tfrac w2-\mu h\right)=N_2\tfrac w2,\quad a=\frac{wg\mu}{2(w-\mu h)}",
            [
                measure(speed**2 / (2 * mu * 9.8)),
                measure(speed**2 * (width + mu * height) / (width * 9.8 * mu)),
                measure(s / 2),
            ],
        )


@_type(6, "ค่าสัมประสิทธิ์ความเสียดทานที่โต๊ะไม่ล้ม", TABLE_TOPIC)
class TableTipping(PhysicsSheet):
    def _variant(self, rng):
        width = rng.randint(6, 15) / 10
        height = rng.randint(4, 12) / 10
        mu = q06.solve(width=width, height=height)
        return draw(
            6,
            measure(mu),
            f"โต๊ะกว้าง {width:g} m จุดศูนย์กลางมวลอยู่กึ่งกลางสูง {height:g} m ขาหลังมีล้อเบา ขาหน้าไม่มีล้อ ไถลไปข้างหน้าบนพื้นที่มีความเสียดทาน สัมประสิทธิ์ความเสียดทานต้องน้อยกว่าเท่าใดโต๊ะจึงไม่ล้มคว่ำ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"N_2>0\Rightarrow a<\frac{wg}{2h}",
            [measure(width / height), measure(height / (2 * width)), measure(width / (4 * height))],
        )


@_type(7, "สัมประสิทธิ์ความเสียดทานจากอัตราส่วนระยะไถล", TABLE_TOPIC)
class TableReverse(PhysicsSheet):
    def _variant(self, rng):
        width = rng.randint(6, 15) / 10
        height = rng.randint(4, 12) / 10
        ratio = rng.randint(12, 28) / 10
        mu = q07.solve(ratio=ratio, width=width, height=height)
        return draw(
            7,
            measure(mu),
            f"โต๊ะกว้าง {width:g} m จุดศูนย์กลางมวลอยู่กึ่งกลางสูง {height:g} m ขาข้างหนึ่งมีล้อเบา อีกข้างไม่มีล้อ ไถลด้วยอัตราเร็วต้นเท่ากัน "
            f"เมื่อล้ออยู่ด้านหน้าโต๊ะไถลได้ไกลเป็น {ratio:g} เท่าของเมื่อล้ออยู่ด้านหลัง สัมประสิทธิ์ความเสียดทานเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"n=\frac{a_1}{a_2}=\frac{w+\mu h}{w-\mu h}",
            [
                measure(mu / 2),
                measure(height * (ratio - 1) / (width * (ratio + 1))),
                measure(width * (ratio - 1) / height),
            ],
        )


RAM = "ตะบันน้ำต่อกับแหล่งน้ำสูง {h} m น้ำไหลออกที่ปลายท่อโดยแทบไม่สูญเสียพลังงาน แล้ววาล์วปิดทันที รอยต่อระหว่างน้ำที่หยุดกับน้ำที่ยังไหลเคลื่อนย้อนด้วยอัตราเร็วเสียงในน้ำ {v} m/s (ρ = 1000 kg/m³, g = 9.8 m/s²)"


def _ram(rng):
    return rng.randint(1, 10) / 2, rng.randint(140, 150) * 10


@_type(8, "ความดันที่เพิ่มขึ้นในตะบันน้ำ", RAM_TOPIC)
class RamPressure(PhysicsSheet):
    def _variant(self, rng):
        head, sound = _ram(rng)
        p = q08.solve(head=head, sound=sound)
        u2 = 2 * 9.8 * head
        return draw(
            8,
            measure(p),
            RAM.format(h=f"{head:g}", v=sound) + " ความดันของน้ำที่หยุดนิ่งเพิ่มขึ้นประมาณกี่เมกะพาสคัล (v ≫ u, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta P=\frac{1}{A}\frac{\Delta q}{\Delta t}\approx\rho vu,\quad u=\sqrt{2gh_0}",
            [measure(500 * u2 / 1e6), measure(1000 * sound**2 / 1e6), measure(p / 2)],
        )


@_type(9, "อัตราเร็วเสียงในน้ำจากมอดุลัสเชิงปริมาตร", RAM_TOPIC)
class RamSoundSpeed(PhysicsSheet):
    def _variant(self, rng):
        bulk = rng.randint(15, 25) / 10
        v = q09.solve(bulk=bulk)
        return draw(
            9,
            measure(v),
            f"น้ำมีมอดุลัสเชิงปริมาตร {bulk:g} GPa และความหนาแน่น 1000 kg/m³ รอยต่อระหว่างน้ำที่หยุดกับน้ำที่ไหลในตะบันน้ำ (ΔP = BΔV/V₀) เคลื่อนด้วยอัตราเร็วกี่เมตรต่อวินาที (v ≫ u, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B=\frac{V_0}{\Delta V}\Delta P\approx\rho v^2",
            [measure(v * sqrt(2)), measure(v / sqrt(1e9)), measure(sqrt(bulk * 1e9))],
        )


@_type(10, "ความสูงที่ตะบันน้ำส่งน้ำขึ้นไปได้", RAM_TOPIC)
class RamLift(PhysicsSheet):
    def _variant(self, rng):
        head, sound = _ram(rng)
        h = q10.solve(head=head, sound=sound)
        u = sqrt(2 * 9.8 * head)
        return draw(
            10,
            measure(h),
            RAM.format(h=f"{head:g}", v=sound) + " น้ำที่หยุดนิ่งดันวาล์วด้านบนเปิดให้น้ำขึ้นไปในท่อตั้ง น้ำขึ้นไปได้สูงที่สุดกี่เมตร (ใช้ ΔP = ρvu + ρu², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_a+\rho gh'=P_a+\rho vu+\rho u^2",
            [measure(head), measure(sound * u / (2 * 9.8)), measure(sound * u / (9.8 * sqrt(2)))],
        )


PLATES = "ตัวเก็บประจุแผ่นขนานห่างกัน {d} mm มีแผ่นไดอิเล็กทริก (εᵣ = {e}) สอดเต็มช่อง อยู่ในสนามแม่เหล็ก {B} T ขนานกับแผ่น ดึงแผ่นไดอิเล็กทริกออกด้วยอัตราเร็ว {v} m/s ขนานกับแผ่นและตั้งฉากกับสนามแม่เหล็ก"


def _plates(rng):
    return rng.randint(1, 10) / 2, rng.randint(1, 10) / 10, rng.randint(4, 20) / 2


@_type(11, "สนามไฟฟ้าจากการแยกขั้วในไดอิเล็กทริก", DIELECTRIC_TOPIC)
class DielectricField(PhysicsSheet):
    def _variant(self, rng):
        speed, field, eps = _plates(rng)
        e2 = q11.solve(speed=speed, field=field, permittivity=eps)
        e0 = speed * field
        return draw(
            11,
            measure(e2),
            PLATES.format(d="2", e=f"{eps:g}", B=f"{field:g}", v=f"{speed:g}") + " สนามไฟฟ้าที่เกิดจากการแยกขั้วประจุในแผ่นไดอิเล็กทริกมีขนาดกี่โวลต์ต่อเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E_0=vB,\quad E_1=\frac{E_0}{\varepsilon_r},\quad E_2=E_1-E_0",
            [measure(e0 / eps), measure(e0), measure(e0 * (eps - 1))],
        )


@_type(12, "อีเอ็มเอฟเหนี่ยวนำคร่อมตัวเก็บประจุ", DIELECTRIC_TOPIC)
class DielectricEmf(PhysicsSheet):
    def _variant(self, rng):
        speed, field, eps = _plates(rng)
        gap = rng.randint(1, 10) / 2
        emf = q12.solve(speed=speed, field=field, gap=gap, permittivity=eps)
        base = speed * field * gap
        return draw(
            12,
            measure(emf),
            PLATES.format(d=f"{gap:g}", e=f"{eps:g}", B=f"{field:g}", v=f"{speed:g}") + " ความต่างศักย์เหนี่ยวนำคร่อมตัวเก็บประจุเป็นกี่มิลลิโวลต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mathcal E=E_2d=vBd\left(1-\frac{1}{\varepsilon_r}\right)",
            [measure(base / eps), measure(base), measure(base * (eps - 1))],
        )


WHEEL, AXLE, RUN = 9.50, 2.60, 0.70
SPAN = (WHEEL**2 - AXLE**2) / WHEEL * 1e-3      # (R^2 - R0^2)/R in metres


@_type(13, "สนามแม่เหล็กของล้อแม่เหล็กจากกราฟ V² กับ a", BRAKE_TOPIC)
class BrakeWheelField(PhysicsSheet):
    def _variant(self, rng):
        field = rng.randint(20, 40) / 100
        accels = [0.20 + 0.13 * k + rng.randint(-2, 2) / 100 for k in range(7)]
        times = tuple(round(sqrt(2 * RUN / a), 2) for a in accels)
        volts = tuple(round(field * sqrt(2 * a * RUN) * SPAN * 1e3 + rng.choice((-0.01, 0, 0.01)), 2) for a in accels)
        b = q13.solve(times=times, volts=volts)
        table = ", ".join(f"({t:.2f} s, {v:.2f} mV)" for t, v in zip(times, volts))
        return draw(
            13,
            measure(b),
            "ล้อแม่เหล็กสองล้อ (รัศมีล้อ 9.50 mm รัศมีเพลา 2.60 mm) กลิ้งลงพื้นเอียงบนแถบอะลูมิเนียมสองแถบเป็นระยะ 70 cm จากหยุดนิ่ง "
            f"ที่มุมเอียงต่าง ๆ วัด (เวลา, ความต่างศักย์ระหว่างแถบที่ปลายทาง) ได้ {table} "
            "ใช้ V² = 2asB²(R² − R₀²)²/R² เขียนกราฟ V² กับ a (วิธีกำลังสองน้อยที่สุด) สนามแม่เหล็กของล้อเป็นกี่เทสลา (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"a=\frac{2s}{t^2},\quad \text{ความชัน}=2sB^2\left(\frac{R^2-R_0^2}{R}\right)^2",
            [measure(b * SPAN / (WHEEL * 1e-3)), measure(2 * b), measure(b * b)],
        )


HEIGHTS = (22.0, 23.5, 25.0, 26.5, 28.0, 29.5, 31.0)


def _brake_data(rng):
    while True:
        damping = rng.randint(30, 60) / 100
        mu = rng.randint(10, 25) / 100
        times = []
        for h in HEIGHTS:
            s = h / 70
            c = sqrt(1 - s * s)
            vt = 0.0174 * 9.8 * (s - mu * c) / damping
            if vt <= 0.02:
                break
            times.append(round(0.20 / vt, 2))
        else:
            return damping, mu, tuple(times)


def _fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return slope, my - slope * mx


BRAKE = (
    "แม่เหล็กมวล 17.4 g ไถลลงพื้นเอียงยาว 70 cm ที่ปูด้วยแผ่นอะลูมิเนียม เมื่อถึงความเร็วปลายแล้วจับเวลาไถลระยะ 20 cm "
    "ที่ความสูงปลายพื้นเอียงต่าง ๆ ได้ (h, เวลา) {table} แรงต้านจากกระแสไหลวนเป็น −bv และสมการ v_T/cos θ = (mg/b)(tan θ − μ) (g = 9.8 m/s²)"
)


@_type(14, "สัมประสิทธิ์การหน่วงจากความเร็วปลาย", BRAKE_TOPIC)
class BrakeDamping(PhysicsSheet):
    def _variant(self, rng):
        _, _, times = _brake_data(rng)
        b = q14.solve(heights=HEIGHTS, times=times)
        xs, ys = _points(HEIGHTS, times, 0.70, 0.20)
        slope, _ = _fit(xs, ys)
        raw_slope, _ = _fit(xs, [0.20 / t for t in times])
        table = ", ".join(f"({h:g} cm, {t:.2f} s)" for h, t in zip(HEIGHTS, times))
        return draw(
            14,
            measure(b),
            BRAKE.format(table=table) + " จากความชันของกราฟ (วิธีกำลังสองน้อยที่สุด) damping coefficient b เป็นกี่ kg/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{ความชัน}=\frac{mg}{b}",
            [measure(slope / (0.0174 * 9.8)), measure(0.0174 / slope), measure(0.0174 * 9.8 / raw_slope)],
        )


@_type(15, "สัมประสิทธิ์ความเสียดทานจลน์จากความเร็วปลาย", BRAKE_TOPIC)
class BrakeFriction(PhysicsSheet):
    def _variant(self, rng):
        _, _, times = _brake_data(rng)
        mu = q15.solve(heights=HEIGHTS, times=times)
        xs, ys = _points(HEIGHTS, times, 0.70, 0.20)
        slope, intercept = _fit(xs, ys)
        raw_slope, raw_intercept = _fit(xs, [0.20 / t for t in times])
        table = ", ".join(f"({h:g} cm, {t:.2f} s)" for h, t in zip(HEIGHTS, times))
        return draw(
            15,
            measure(mu),
            BRAKE.format(table=table) + " จากกราฟเส้นตรง (วิธีกำลังสองน้อยที่สุด) สัมประสิทธิ์ความเสียดทานจลน์ μ เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\mu=-\frac{\text{จุดตัดแกน}}{\text{ความชัน}}",
            [measure(abs(intercept)), measure(slope / abs(intercept)), measure(-raw_intercept / raw_slope)],
        )


@_type(16, "สภาพนำไฟฟ้าของอะลูมิเนียมจากการหน่วง", BRAKE_TOPIC)
class BrakeConductivity(PhysicsSheet):
    def _variant(self, rng):
        damping = rng.randint(30, 60) / 100
        shape = rng.randint(10, 25) / 10
        sigma = q16.solve(damping=damping, shape=shape) * 1e7
        lam = shape * 1e-8
        return draw(
            16,
            measure(sigma),
            f"แม่เหล็กมวล 17.4 g ไถลบนแผ่นอะลูมิเนียมมี damping coefficient b = {damping:.2f} kg/s ถ้าแรงต้าน bv = σΛv โดย Λ = {shape:g}×10⁻⁸ (หน่วย SI) สภาพนำไฟฟ้าของอะลูมิเนียมเป็นกี่ซีเมนส์ต่อเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"b=\sigma\Lambda",
            [measure(lam / damping), measure(damping * lam), measure(0.0174 / damping / lam)],
        )


@_type(17, "ค่า k ในแฟกเตอร์การกระจายสนามแม่เหล็ก", BRAKE_TOPIC)
class BrakeShapeFactor(PhysicsSheet):
    def _variant(self, rng):
        shape = rng.randint(10, 25) / 10
        field = rng.randint(20, 40) / 100
        k = q17.solve(shape=shape, field=field)
        return draw(
            17,
            measure(k),
            f"แม่เหล็กจานเส้นผ่านศูนย์กลาง 19.0 mm หนา 5.0 mm สนามแม่เหล็ก {field:g} T ไถลบนแผ่นอะลูมิเนียมหนา 1.0 mm วัดได้ Λ = {shape:g}×10⁻⁸ (หน่วย SI) ถ้า Λ = kdD²B² ค่า k เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"k=\frac{\Lambda}{dD^2B^2}",
            [measure(k * 4), measure(k * field), measure(k / 5)],
        )
