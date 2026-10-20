"""Seeded variants of the reviewed TPhO 8 (2552) national physics olympiad."""

from fractions import Fraction
from math import floor, isqrt, log10, pi, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2552_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2552_physics import q11, q12, q13, q14, q15, q16

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


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
    1: ("phys.leak_atmosphere_subtracted", "phys.gas_volume_litres_unconverted", "phys.leak_area_unit"),
    2: ("phys.image_direction_not_inverted", "phys.image_speed_unmagnified", "phys.image_speed_longitudinal"),
    3: ("phys.triangle_exit_radius_half_side", "phys.triangle_exit_radius_half_height", "phys.triangle_tan_cot_swapped"),
    4: ("phys.charged_ball_vertical_ignored", "phys.charged_ball_field_ignored", "phys.charged_ball_full_drop_time"),
    5: ("phys.height_speed_ratio_not_squared", "phys.bounce_partner_motion_ignored", "phys.bounce_relative_speed_only"),
    6: ("phys.bounce_light_limit_used", "phys.bounce_heavy_ball_speed_given", "phys.bounce_mass_ratio_sign"),
    7: ("phys.second_collision_at_ceiling", "phys.ceiling_speed_unreduced", "phys.heavy_ball_assumed_still"),
    8: ("phys.second_collision_at_ceiling", "phys.ceiling_speed_unreduced", "phys.heavy_ball_peak_height"),
    9: ("phys.plate_force_half_dropped", "phys.plate_force_quarter", "phys.plate_force_area_squared"),
    10: ("phys.plate_force_half_dropped", "phys.plate_gap_unstretched", "phys.spring_extension_as_gap"),
    11: ("phys.plate_field_stiffness_ignored", "phys.plate_spring_stiffness_halved", "phys.frequency_angular_confused"),
    12: ("phys.plate_stability_half", "phys.plate_stability_two_thirds", "phys.plate_stability_quarter"),
    13: ("phys.square_coil_as_circle", "phys.coil_turns_omitted", "phys.tesla_gauss_unconverted"),
    14: ("phys.tesla_gauss_unconverted", "phys.sensitivity_inverted", "phys.coil_turns_omitted"),
    15: ("phys.disc_field_surface_as_reading", "phys.disc_shape_root_dropped", "phys.disc_shape_inverted"),
    16: ("phys.physical_pendulum_point_mass", "phys.pendulum_period_not_squared", "phys.rod_half_length_as_length"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 8 (2552)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2552_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2552_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


@_type(1, "ความเร่งของถังแก๊สที่เกิดรูรั่ว", "กฎแก๊สอุดมคติกับแรงดัน")
class LeakingTank(PhysicsSheet):
    def _variant(self, rng):
        moles = rng.randint(5, 30) / 10
        litres = rng.choice((2.0, 4.0, 5.0, 8.0, 10.0))
        temperature = rng.choice((280, 300, 320, 350))
        area = rng.randint(1, 10)
        mass = rng.randint(10, 50) / 10
        a = q01.solve(moles=moles, temperature=temperature, litres=litres, area_mm2=area, mass=mass)
        pressure = moles * 8.31 * temperature / (litres * 1e-3)
        return draw(
            1,
            measure(a),
            f"ถังสี่เหลี่ยมปริมาตรภายใน {litres:g} ลิตร บรรจุแก๊ส {moles:g} โมล อุณหภูมิ {temperature} K มวลรวม {mass:g} kg วางบนพื้นลื่นในสุญญากาศ เกิดรูรั่วพื้นที่ {area} mm² ที่กึ่งกลางผนังด้านหนึ่ง ขณะนั้นถังมีความเร่งกี่ m/s² (R = 8.31 J/mol·K, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P=\frac{nRT}{V},\quad F=PA=Ma",
            [measure((pressure - 101300) * area * 1e-6 / mass), measure(a / 1000), measure(a * 100)],
        )


@_type(2, "ความเร็วของภาพเมื่อวัตถุเคลื่อนที่ตั้งฉากกับแกน", "สมการเลนส์และภาพจริงบนฉาก")
class ImageVelocity(PhysicsSheet):
    def _variant(self, rng):
        focal = rng.randint(5, 30)
        distance = focal + rng.randint(2, 30)
        speed = Fraction(rng.randint(5, 100), 10)
        exact = -speed * focal / (distance - focal)
        agree(q02.solve(focal=focal, distance=distance, speed=float(speed)), exact)
        return draw(
            2,
            tex(exact),
            f"จุดกำเนิดแสงเล็ก ๆ อยู่ห่างเลนส์นูนบาง (ความยาวโฟกัส {focal} cm) {distance} cm และเคลื่อนที่ขึ้นตั้งฉากกับแกนมุขสำคัญด้วยความเร็ว {number(speed)} cm/s ภาพของมันมีความเร็วกี่ cm/s (ทิศขึ้นเป็นบวก)",
            r"\frac1u+\frac1v=\frac1f,\quad m=-\frac vu",
            [tex(-exact), tex(-speed), tex(-speed * Fraction(focal, distance - focal) ** 2)],
        )


@_type(3, "อัตราเร็วอิเล็กตรอนที่ออกจากสนามรูปสามเหลี่ยมขนานแกน x", "การเคลื่อนที่ของประจุในสนามแม่เหล็ก")
class TriangleField(PhysicsSheet):
    def _variant(self, rng):
        field = rng.choice((1, 2, 5)) * 10.0 ** rng.choice((-4, -3))
        side = rng.choice((2, 4, 5, 10, 20)) / 100
        v = q03.solve(field=field, side=side)
        em = 1.76e11
        return draw(
            3,
            measure(v),
            f"อิเล็กตรอนถูกยิงในทิศ +y เข้าที่กึ่งกลางฐานของบริเวณรูปสามเหลี่ยมด้านเท่ายาวด้านละ {side * 100:g} cm ซึ่งมีสนามแม่เหล็กสม่ำเสมอ {field:g} T ทิศพุ่งเข้าหน้ากระดาษ อิเล็กตรอนต้องมีอัตราเร็วกี่ m/s จึงหลุดออกจากสนามที่ด้านเอียงในทิศขนานกับแกน x พอดี (e/m = 1.76×10¹¹ C/kg, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"evB=\frac{mv^2}{r},\quad \frac{r}{a/2-r}=\tan60^\circ",
            [measure(em * field * side / 2), measure(em * field * sqrt(3) * side / 4), measure(em * field * side / (2 * (1 + sqrt(3))))],
        )


@_type(4, "อัตราเร็วของลูกบอลมีประจุที่ครึ่งความสูง", "การเคลื่อนที่ในสนามไฟฟ้าและแรงโน้มถ่วง")
class ChargedBall(PhysicsSheet):
    def _variant(self, rng):
        mass = rng.randint(1, 5) * 1e-3
        charge = rng.randint(1, 20) / 1000
        field = rng.randint(1, 20) / 10
        speed = rng.randint(1, 5)
        height = rng.choice((0.8, 1.0, 1.8, 2.0, 3.2))
        v = q04.solve(mass=mass, charge=charge, field=field, speed=speed, height=height)
        t = sqrt(height / 10)
        vx = speed + charge * field / mass * t
        return draw(
            4,
            measure(v),
            f"ลูกบอลมวล {mass * 1000:g} g ประจุ {charge:g} C ถูกยิงในแนวระดับ (แกน x) ด้วยความเร็ว {speed} m/s ที่ความสูง {height:g} m เหนือพื้น บริเวณที่สูงกว่าครึ่งความสูงนี้มีสนามไฟฟ้า {field:g} N/C ทิศ +x ส่วนบริเวณต่ำกว่าไม่มีสนาม ลูกบอลมีอัตราเร็วกี่ m/s ขณะลงมาถึงครึ่งความสูง (g = 10 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"v_x=v_0+\frac{qE}{m}t,\quad v_y=-gt,\quad \frac h2=\tfrac12gt^2",
            [
                measure(vx),
                measure(sqrt(speed**2 + 10 * height)),
                measure(sqrt((speed + charge * field / mass * sqrt(2 * height / 10)) ** 2 + 10 * height)),
            ],
        )


RATIOS = (Fraction(0), Fraction(1, 9), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2))


@_type(5, "ความสูงที่ลูกบอลเบาเด้งขึ้นหลังชนลูกบอลหนัก", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class DoubleBallHeight(PhysicsSheet):
    def _variant(self, rng):
        r = rng.choice(RATIOS)
        speed = (3 - r) / (1 + r)
        agree(q05.solve(ratio=float(r)), speed**2)
        setting = "มวล M ≫ m" if r == 0 else f"m = M/{int(1 / r)}" if r.numerator == 1 else f"m/M = {number(r)}"
        return draw(
            5,
            tex(speed**2),
            f"ลูกบอลมวล m วางบนลูกบอลมวล M ({setting}) ร้อยในลวดตรงแนวดิ่งลื่น ปล่อยพร้อมกันจากความสูง h ลูกล่างกระทบพื้นแล้วเด้งขึ้นชนลูกบนทันที การชนทั้งหมดยืดหยุ่นสมบูรณ์ ลูกบอลมวล m ขึ้นได้สูงสุดกี่เท่าของ h (เพดานสูงมาก)",
            r"v=\frac{3-m/M}{1+m/M}v_0,\quad\frac{H_{\max}}{h}=\left(\frac{v}{v_0}\right)^2",
            [tex(speed), "1", "4"],
        )


DROPS = (Fraction(9, 5), Fraction(16, 5), Fraction(5), Fraction(36, 5), Fraction(64, 5))


def _share(r):
    """m as a fraction of M, written M/6 rather than 1/6M."""
    return f"M/{r.denominator}" if r.numerator == 1 else f"{number(r)}M"


@_type(6, "อัตราเร็วลูกบอลเบาหลังการชนครั้งแรก", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class DoubleBallSpeed(PhysicsSheet):
    def _variant(self, rng):
        r = rng.choice(RATIOS[1:])
        drop = rng.choice(DROPS)
        v0 = isqrt(int(20 * drop))
        exact = (3 - r) / (1 + r) * v0
        agree(q06.solve(ratio=float(r), drop=float(drop)), exact)
        heavy = (1 - r) * v0 - r * exact
        return draw(
            6,
            tex(exact),
            f"ลูกบอลมวล m = {_share(r)} วางบนลูกบอลมวล M ร้อยในลวดตรงแนวดิ่งลื่น ปล่อยพร้อมกันจากความสูง {number(drop)} m ลูกล่างกระทบพื้นแล้วเด้งขึ้นชนลูกบนทันที (ชนยืดหยุ่นสมบูรณ์) หลังการชนครั้งแรกลูกบอลมวล m มีอัตราเร็วขึ้นกี่ m/s (g = 10 m/s²)",
            r"Mv_0-mv_0=MV+mv,\quad v_0^2(M+m)=MV^2+mv^2",
            [str(3 * v0), tex(heavy), tex((3 + r) / (1 + r) * v0)],
        )


def _second(rng):
    r = rng.choice((Fraction(1, 9), Fraction(1, 8), Fraction(1, 6), Fraction(1, 5)))
    drop = rng.choice((Fraction(16, 5), Fraction(5), Fraction(36, 5)))
    ceiling = drop + rng.randint(1, 6)
    g = 10.0
    v0 = sqrt(2 * g * float(drop))
    v = float((3 - r) / (1 + r)) * v0
    big = float(1 - r) * v0 - float(r) * v
    if v * v <= 2 * g * float(ceiling):
        raise _Clash
    top = sqrt(v * v - 2 * g * float(ceiling))
    t_top = (v - top) / g
    tau = q07.solve(ratio=float(r), drop=float(drop), ceiling=float(ceiling))
    height = q08.solve(ratio=float(r), drop=float(drop), ceiling=float(ceiling))
    if tau <= t_top or height <= 0.05 or tau >= 2 * big / g:
        raise _Clash
    return r, drop, ceiling, v, big, top, t_top, tau, height


PAIR = "ลูกบอลมวล m = {r} วางบนลูกบอลมวล M ร้อยในลวดตรงแนวดิ่งลื่นระหว่างพื้นกับเพดานที่สูง {ceiling} m ปล่อยพร้อมกันจากความสูง {drop} m การชนทั้งหมด (กับพื้น เพดาน และกันเอง) ยืดหยุ่นสมบูรณ์ (g = 10 m/s²)"


def _slips(v, big, top, t_top, ceiling):
    g = 10.0
    fast = (ceiling + v * t_top - g * t_top**2 / 2) / (big + v - g * t_top)
    s = (-top + sqrt(top * top + 2 * g * ceiling)) / g
    return fast, s


@_type(7, "เวลาระหว่างการชนครั้งแรกและครั้งที่สอง", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class SecondCollisionTime(PhysicsSheet):
    def _variant(self, rng):
        r, drop, ceiling, v, big, top, t_top, tau, height = _second(rng)
        fast, fall = _slips(v, big, top, t_top, float(ceiling))
        return draw(
            7,
            measure(tau),
            PAIR.format(r=_share(r), ceiling=ceiling, drop=number(drop)) + " ลูกบอลชนกันครั้งที่สองหลังการชนครั้งแรกกี่วินาที (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"y_M=V\tau-\tfrac12g\tau^2,\quad y_m=H-v_H(\tau-t_H)-\tfrac12g(\tau-t_H)^2",
            [measure(t_top), measure(fast), measure(t_top + fall)],
        )


@_type(8, "ความสูงที่ลูกบอลชนกันครั้งที่สอง", "การชนแบบยืดหยุ่นหนึ่งมิติ")
class SecondCollisionHeight(PhysicsSheet):
    def _variant(self, rng):
        r, drop, ceiling, v, big, top, t_top, tau, height = _second(rng)
        fast, _ = _slips(v, big, top, t_top, float(ceiling))
        at_top = big * t_top - 5 * t_top**2
        fast_height = big * fast - 5 * fast**2
        if min(at_top, fast_height) <= 0:
            raise _Clash
        return draw(
            8,
            measure(height),
            PAIR.format(r=_share(r), ceiling=ceiling, drop=number(drop)) + " ลูกบอลชนกันครั้งที่สองที่ความสูงกี่เมตรจากพื้น (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"y_M=V\tau-\tfrac12g\tau^2,\quad y_m=H-v_H(\tau-t_H)-\tfrac12g(\tau-t_H)^2",
            [measure(at_top), measure(fast_height), measure(big * big / 20)],
        )


EPS0 = 8.85e-12


@_type(9, "แรงระหว่างแผ่นประจุขนาน", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateForce(PhysicsSheet):
    def _variant(self, rng):
        sigma = rng.randint(2, 60)
        area = rng.randint(1, 40) / 100
        force = q09.solve(sigma=sigma, area=area)
        return draw(
            9,
            measure(force),
            f"แผ่นโลหะขนานพื้นที่ {area:g} m² สองแผ่นมีความหนาแน่นประจุ +{sigma} μC/m² และ −{sigma} μC/m² อยู่ใกล้กันมาก แรงที่แผ่นหนึ่งกระทำต่ออีกแผ่นเป็นกี่นิวตัน (ε₀ = 8.85×10⁻¹² C²/N·m², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F=(\sigma A)\frac{\sigma}{2\varepsilon_0}",
            [measure(2 * force), measure(force / 2), measure(force * area)],
        )


def _hung(rng):
    gap = rng.randint(5, 30) / 1000
    stretch = gap * rng.randint(5, 30) / 100
    return gap, stretch


@_type(10, "ค่าคงตัวสปริงจากการยืดของแผ่นตัวเก็บประจุ", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateSpring(PhysicsSheet):
    def _variant(self, rng):
        gap, stretch = _hung(rng)
        volts = rng.randint(1, 20) * 100
        area = rng.randint(1, 40) / 100
        k = q10.solve(volts=volts, area=area, gap=gap, stretch=stretch)
        return draw(
            10,
            measure(k),
            f"แผ่นโลหะบนของตัวเก็บประจุแผ่นขนาน (พื้นที่ {area:g} m²) แขวนกับสปริงนำไฟฟ้า ห่างแผ่นล่างที่ตรึงไว้ {gap * 1000:g} mm เมื่อไม่มีความต่างศักย์ เมื่อต่อความต่างศักย์ {volts} V สปริงยืดเพิ่ม {stretch * 1000:g} mm ค่าคงตัวสปริงเป็นกี่ N/m (ε₀ = 8.85×10⁻¹² C²/N·m², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"kd=\tfrac12\varepsilon_0A\left(\frac{V_0}{D-d}\right)^2",
            [measure(2 * k), measure(k * ((gap - stretch) / gap) ** 2), measure(k * stretch / gap)],
        )


@_type(11, "ความถี่เชิงมุมของแผ่นตัวเก็บประจุที่แขวนสปริง", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateOscillation(PhysicsSheet):
    def _variant(self, rng):
        gap, stretch = _hung(rng)
        spring = rng.randint(5, 80)
        mass = rng.randint(10, 200) / 1000
        omega = q11.solve(spring=spring, mass=mass, gap=gap, stretch=stretch)
        return draw(
            11,
            measure(omega),
            f"แผ่นโลหะบนมวล {mass * 1000:g} g ของตัวเก็บประจุแผ่นขนานแขวนกับสปริงค่าคงตัว {spring} N/m เดิมห่างแผ่นล่าง {gap * 1000:g} mm เมื่อต่อความต่างศักย์คงที่ สปริงยืดเพิ่ม {stretch * 1000:g} mm และสมดุล เคาะแผ่นบนให้สั่นเล็กน้อย ความถี่เชิงมุมเป็นกี่ rad/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\omega^2=\frac1m\left(k-\frac{V_0^2A\varepsilon_0}{(D-d)^3}\right)",
            [measure(sqrt(spring / mass)), measure(sqrt(spring / mass * (gap - 2 * stretch) / (gap - stretch))), measure(omega / (2 * pi))],
        )


@_type(12, "เงื่อนไขที่แผ่นตัวเก็บประจุสั่นไม่ได้", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateStability(PhysicsSheet):
    def _variant(self, rng):
        gap = Fraction(rng.randint(3, 60), 2)
        agree(q12.solve(gap=float(gap)), gap / 3)
        return draw(
            12,
            tex(gap / 3),
            f"แผ่นบนของตัวเก็บประจุแผ่นขนานแขวนกับสปริง เดิมห่างแผ่นล่าง {number(gap)} mm เมื่อเพิ่มความต่างศักย์ สปริงยืดเพิ่มเป็นระยะ d แผ่นบนจะสั่นแบบฮาร์มอนิกรอบสมดุลไม่ได้เมื่อ d มีค่าอย่างน้อยกี่มิลลิเมตร",
            r"\omega^2=\frac km\cdot\frac{D-3d}{D-d}",
            [tex(gap / 2), tex(2 * gap / 3), tex(gap / 4)],
        )


MU0 = 4e-7 * pi
COIL = 4.8 / 5.2


def _coil_field(side, distance, turns=130):
    a, x = side / 100, distance / 100
    return MU0 * a * a * COIL * turns / (2 * pi) / ((x * x + a * a / 4) * sqrt(x * x + a * a / 2)) * 1e4


@_type(13, "สนามแม่เหล็กบนแกนของขดลวดสี่เหลี่ยมจัตุรัส", "สนามแม่เหล็กและเซนเซอร์ฮอลล์")
class SquareCoilField(PhysicsSheet):
    def _variant(self, rng):
        side = rng.choice((4, 6, 8, 10, 12))
        distance = rng.randint(0, 20)
        b = q13.solve(side=side, distance=distance)
        agree(b, _coil_field(side, distance))
        radius = side / 200
        circle = MU0 * 130 * COIL * radius**2 / (2 * ((distance / 100) ** 2 + radius**2) ** 1.5) * 1e4
        return draw(
            13,
            measure(b),
            f"ขดลวดสี่เหลี่ยมจัตุรัส 130 รอบ ยาวด้านละ {side} cm มีความต้านทาน 5.2 Ω ต่อกับความต่างศักย์ 4.8 V สนามแม่เหล็กบนแกนของขดลวดที่ห่างจากศูนย์กลาง {distance} cm มีค่ากี่เกาส์ (μ₀ = 4π×10⁻⁷ H/m, 1 G = 10⁻⁴ T, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B=\frac{\mu_0a^2iN}{2\pi}\cdot\frac{1}{(x^2+a^2/4)\sqrt{x^2+a^2/2}}",
            [measure(circle), measure(b / 130), measure(b * 1e-4)],
        )


@_type(14, "ความไวของเซนเซอร์ฮอลล์", "สนามแม่เหล็กและเซนเซอร์ฮอลล์")
class HallSensitivity(PhysicsSheet):
    def _variant(self, rng):
        side = rng.choice((4, 6, 8, 10, 12))
        distance = rng.randint(0, 10)
        change = rng.randint(5, 80) / 10
        sens = q14.solve(change=change, side=side, distance=distance)
        b = _coil_field(side, distance)
        return draw(
            14,
            measure(sens),
            f"วาง Hall effect sensor บนแกนของขดลวดสี่เหลี่ยมจัตุรัส 130 รอบ ยาวด้านละ {side} cm (5.2 Ω ต่อกับ 4.8 V) ห่างจากศูนย์กลาง {distance} cm เมื่อเปิดกระแส V_out เปลี่ยนไป {change:g} mV ความไวของเซนเซอร์เป็นกี่ mV ต่อเกาส์ (μ₀ = 4π×10⁻⁷ H/m, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{ความไว}=\frac{\Delta V_{out}}{B}",
            [measure(sens * 1e4), measure(b / change), measure(sens * 130)],
        )


@_type(15, "สนามที่ผิวแม่เหล็กแผ่นกลมจากค่าที่วัดได้", "สนามแม่เหล็กและเซนเซอร์ฮอลล์")
class DiscMagnet(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.randint(5, 25) / 10
        thickness = rng.randint(2, 10) / 10
        distance = rng.randint(2, 30) / 10
        reading = rng.randint(20, 500)
        b0 = q15.solve(radius=radius, thickness=thickness, distance=distance, reading=reading)
        bracket = (distance + thickness) / sqrt((distance + thickness) ** 2 + radius**2) - distance / sqrt(distance**2 + radius**2)
        root = sqrt(1 + (radius / thickness) ** 2)
        return draw(
            15,
            measure(b0),
            f"แม่เหล็กแผ่นจานกลมรัศมี {radius:g} cm หนา {thickness:g} cm วัดสนามบนแกนที่ห่างจากผิว {distance:g} cm ได้ {reading} G ถ้า B(y) = B₀√(1 + (r/t)²)[(y + t)/√((y + t)² + r²) − y/√(y² + r²)] สนามที่ผิว B₀ เป็นกี่เกาส์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"B_0=\frac{B(y)}{\sqrt{1+(r/t)^2}\,\{\cdots\}}",
            [str(reading), measure(reading / bracket), measure(reading * root * bracket)],
        )


@_type(16, "ค่า g จากลูกตุ้มกายภาพทรงกระบอก", "การแกว่งของวัตถุแข็งเกร็ง")
class RodPendulumG(PhysicsSheet):
    def _variant(self, rng):
        half = rng.choice((30, 40, 50))
        radius = rng.randint(3, 10) / 10
        pivot = rng.randint(2, half - 10)
        arm = (half - pivot) / 100
        inertia = (half / 100) ** 2 / 3 + (radius / 100) ** 2 / 4 + arm * arm
        period = round(2 * pi * sqrt(inertia / (9.78 * arm)), 3)
        g = q16.solve(half=half, radius=radius, pivot=pivot, period=period)
        return draw(
            16,
            measure(g),
            f"ท่อนทรงกระบอกตันยาว {2 * half} cm รัศมี {radius:g} cm แกว่งรอบแกนระดับที่ห่างจากปลายข้างหนึ่ง {pivot} cm ด้วยแอมพลิจูดเล็ก ๆ วัดคาบได้ {period:.3f} s ค่า g เป็นกี่ m/s² (I_CM = M(L²/3 + R²/4) เมื่อท่อนยาว 2L, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"g=\frac{4\pi^2}{T^2}\left[\frac{L^2/3+R^2/4}{L-x}+(L-x)\right]",
            [
                measure(4 * pi**2 * arm / period**2),
                measure(g * period),
                measure(4 * pi**2 * (((2 * half / 100) ** 2 / 3 + (radius / 100) ** 2 / 4) / arm + arm) / period**2),
            ],
        )
