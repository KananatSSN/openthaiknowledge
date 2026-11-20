"""Seeded variants of the reviewed POSN physics 2569 camp selection paper."""

from fractions import Fraction
from math import isqrt, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2569_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2569_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2569_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29, q30

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def radical(value):
    """Exact reduced radical of a nonnegative rational."""
    value = Fraction(value)
    square, remainder = 1, value.numerator * value.denominator
    divisor = 2
    while divisor <= isqrt(remainder):
        while remainder % (divisor * divisor) == 0:
            square *= divisor
            remainder //= divisor * divisor
        divisor += 1
    coefficient = Fraction(square, value.denominator)
    if remainder == 1:
        return tex(coefficient)
    numerator = (
        str(coefficient.numerator) if coefficient.numerator != 1 else ""
    ) + rf"\sqrt{{{remainder}}}"
    return (
        numerator
        if coefficient.denominator == 1
        else rf"\frac{{{numerator}}}{{{coefficient.denominator}}}"
    )


def _decimal(value):
    """Plain decimal TeX for a value with at most six decimal places."""
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


def sci(value, force=False):
    """A rational as a plain decimal when it is short and of moderate size,
    otherwise as mantissa × 10^n; a mantissa that does not terminate stays a
    fraction, so nothing is rounded."""
    value = Fraction(value)
    if value == 0:
        return "0"
    if not force and (value * 1000).denominator == 1 and abs(value) < 10**6:
        return _decimal(value) if value.denominator != 1 else str(value)
    if not force and Fraction(1, 1000) <= abs(value) < 10**6 and (value * 10**6).denominator != 1:
        return tex(value)
    power = 0
    while abs(value) >= 10:
        value, power = value / 10, power + 1
    while abs(value) < 1:
        value, power = value * 10, power - 1
    if value == 1:
        return rf"10^{{{power}}}"
    mantissa = _decimal(value) if (value * 10**6).denominator == 1 else tex(value)
    return rf"{mantissa}\times10^{{{power}}}"


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


def pi_sci(value):
    """value * pi as (sign) mantissa pi x 10^n, the mantissa exact."""
    value = Fraction(value)
    sign = "-" if value < 0 else ""
    value = abs(value)
    power = 0
    while value >= 10:
        value, power = value / 10, power + 1
    while value < 1:
        value, power = value * 10, power - 1
    mantissa = _decimal(value) if (value * 10**6).denominator == 1 else tex(value)
    mantissa = "" if mantissa == "1" else mantissa
    return rf"{sign}{mantissa}\pi\times10^{{{power}}}"


def over_pi(value):
    """value / pi as exact TeX."""
    value = Fraction(value)
    bottom = rf"{value.denominator}\pi" if value.denominator != 1 else r"\pi"
    return rf"\frac{{{value.numerator}}}{{{bottom}}}"


def times_pi(value, power=""):
    """value * pi (or pi^2 with power="^2") as exact TeX."""
    value = Fraction(value)
    if value == 0:
        return "0"
    top = "" if abs(value.numerator) == 1 else str(abs(value.numerator))
    sign = "-" if value < 0 else ""
    if value.denominator == 1:
        return rf"{sign}{top}\pi{power}"
    return rf"{sign}\frac{{{top}\pi{power}}}{{{value.denominator}}}"


def pi_radical(square):
    """pi * sqrt(square) as exact TeX."""
    root = radical(square)
    return r"\pi" if root == "1" else rf"{root}\pi"


def three_figures(value):
    """A positive float to three significant figures, as plain text."""
    digits = 3 - len(str(int(value))) if value >= 1 else 3
    return f"{round(value, max(digits, 0)):.{max(digits, 0)}f}"


def pair(first, second):
    return rf"\left({first},\ {second}\right)"


SINES = (Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13), Fraction(7, 25), Fraction(24, 25), Fraction(8, 17), Fraction(15, 17))


def cosine(sine):
    root = Fraction(isqrt(sine.denominator**2 - sine.numerator**2), sine.denominator)
    assert root * root + sine * sine == 1
    return root


SLIPS = {
    1: ("phys.collision_slower_body", "phys.collision_energy_fraction_as_speed", "phys.collision_assumed_elastic"),
    2: ("phys.pegged_short_length_only", "phys.pegged_length_not_rooted", "phys.pegged_peg_ignored"),
    3: ("phys.terminal_buoyancy_ignored", "phys.terminal_buoyancy_added", "phys.terminal_weight_ignored"),
    4: ("phys.null_point_between_charges", "phys.null_point_not_rooted", "phys.null_point_from_small_charge"),
    5: ("phys.slab_shift_path_ignored", "phys.slab_shift_angle_sum", "phys.slab_shift_used_cosine"),
    6: ("phys.resistor_count_ignored_coincidence", "phys.resistor_count_pairs_only", "phys.resistor_count_no_mixed"),
    7: ("phys.heat_flow_area_length_ignored", "phys.heat_flow_length_ignored", "phys.heat_flow_area_ignored"),
    8: ("phys.explosion_no_change", "phys.explosion_halves_swapped", "phys.explosion_root_missing"),
    9: ("phys.ring_field_odd_ignored", "phys.ring_field_zero_everywhere", "phys.ring_force_point_distance"),
    10: ("phys.loop_field_wrong_power", "phys.loop_axial_linear", "phys.loop_axial_distance_ratio"),
    11: ("phys.split_lens_halved", "phys.split_lens_unchanged", "phys.split_lens_other_half"),
    12: ("phys.real_image_two_focal", "phys.real_image_one_focal", "phys.real_image_three_focal"),
    13: ("phys.pushed_wedge_sine", "phys.pushed_wedge_cosine", "phys.pushed_wedge_cotangent"),
    14: ("phys.rope_lowest_full_weight", "phys.rope_lowest_cotangent", "phys.rope_lowest_sine"),
    15: ("phys.hole_cm_area_not_subtracted", "phys.hole_cm_hole_centre", "phys.hole_cm_area_not_squared"),
    16: ("phys.hose_speed_not_squared", "phys.hose_halved", "phys.hose_doubled"),
    17: ("phys.ring_tension_whole_mass", "phys.ring_tension_half_circumference", "phys.ring_tension_halved"),
    18: ("phys.glancing_ratio_inverted", "phys.glancing_ratio_sine", "phys.glancing_ratio_cosine"),
    19: ("phys.poles_landing_gap_only", "phys.poles_landing_from_launch", "phys.poles_landing_halved"),
    20: ("phys.sound_speed_celsius", "phys.sound_speed_grams", "phys.sound_speed_inverted"),
    21: ("phys.max_power_full", "phys.max_power_halved", "phys.max_power_eighth"),
    22: ("phys.charge_share_capacitors_swapped", "phys.charge_share_half", "phys.charge_share_squared"),
    23: ("phys.charge_split_equally", "phys.charge_split_complement", "phys.charge_split_one_partner"),
    24: ("phys.plate_tilt_hanger_once", "phys.plate_tilt_hanger_depth_ignored", "phys.plate_tilt_doubled"),
    25: ("phys.wall_rebound_speed_unchanged", "phys.wall_rebound_relative_only", "phys.wall_rebound_heavy_limit"),
    26: ("phys.steam_volume_celsius", "phys.steam_volume_units_omitted", "phys.steam_volume_molar_mass_dropped"),
    27: ("phys.parallel_echo_motion_ignored", "phys.parallel_echo_speeds_added", "phys.parallel_echo_speeds_subtracted"),
    28: ("phys.wedge_energy_total_mass", "phys.wedge_energy_momentum_only", "phys.wedge_energy_not_rooted"),
    29: ("phys.receding_sin_cos_swapped", "phys.receding_square_mismatch", "phys.receding_bracket_misread"),
    30: ("phys.lens_pair_virtual_object_ignored", "phys.lens_pair_focal_sign", "phys.lens_pair_focal_sum"),
}


def draw(number_, answer, prompt, hint, slips):
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number_], slips)],
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2569_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2569)"


def _type(n, title, topic):
    return question_type(
        f"phys.posn2569_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


@_type(1, "ความเร็วหลังชนเมื่อพลังงานจลน์เหลือบางส่วน", "การชนกับการสูญเสียพลังงาน")
class FractionCollision(PhysicsSheet):
    def expr(self, rng):
        spread = rng.choice((Fraction(1, 5), Fraction(1, 3), Fraction(1, 2), Fraction(3, 5), Fraction(3, 4)))
        fraction = (1 + spread * spread) / 2
        answer = agree(q01.solve(fraction=float(fraction)), (1 + spread) / 2)
        return draw(
            1,
            tex(answer),
            f"มวล A และ B เท่ากัน A วิ่งด้วยความเร็ว u ชน B ที่หยุดนิ่งตรงๆ หลังชนทั้งสองเคลื่อนที่ไปทางเดิม (A ตามหลัง B) และพลังงานจลน์ของระบบเหลือ {number(fraction)} ของก่อนชน ความเร็ว v₂ ของ B หลังชนเป็นกี่เท่าของ u",
            r"v_1+v_2=u,\quad v_1^2+v_2^2=fu^2",
            [tex((1 - spread) / 2), tex(fraction), "1"],
        )


PEGS = (Fraction(3, 4), Fraction(5, 9), Fraction(8, 9), Fraction(7, 16), Fraction(16, 25), Fraction(9, 25))


@_type(2, "คาบลูกตุ้มที่มีหมุดขวาง", "การแกว่งของลูกตุ้มอย่างง่าย")
class PeggedPendulum(PhysicsSheet):
    def expr(self, rng):
        peg = rng.choice(PEGS)
        rest = 1 - peg
        root = Fraction(isqrt(rest.numerator), isqrt(rest.denominator))
        assert root * root == rest
        answer = agree(q02.solve(peg=float(peg)), (1 + root) / 2)
        return draw(
            2,
            tex(answer),
            f"ลูกตุ้มสายยาว l แกว่งด้วยแอมพลิจูดเล็ก มีหมุดตรึงอยู่ในแนวดิ่งใต้จุดแขวนที่ระยะ {number(peg)}l ขวางสายเมื่อลูกตุ้มแกว่งผ่านไปด้านหนึ่ง คาบการแกว่งครบรอบเป็นกี่เท่าของ 2π√(l/g)",
            r"T=\pi\sqrt{\frac lg}+\pi\sqrt{\frac{l'}g}",
            [tex(root), tex((2 - peg) / 2), "1"],
        )


@_type(3, "ความเร็วปลายเมื่อมีแรงลอยตัวและแรงต้าน", "แรงต้านและความเร็วปลาย")
class TerminalSpeed(PhysicsSheet):
    def expr(self, rng):
        volume = Fraction(rng.randint(1, 8), 2)  # litres
        mass = volume + rng.randint(1, 10)
        beta = rng.randint(1, 10)
        exact = (mass - volume) * 10 / beta
        answer = agree(q03.solve(mass=float(mass), volume=float(volume), beta=beta), exact)
        return draw(
            3,
            tex(answer),
            f"ทรงกลมมวล {number(mass)} kg ปริมาตร {number(volume)} L ตกลงในน้ำนิ่ง (1000 kg/m³) โดยมีแรงต้าน βv เมื่อ β = {beta} kg/s ความเร็วปลายของทรงกลมเป็นกี่ m/s ให้ g=10 m/s²",
            r"Mg-\rho Vg-\beta v=0",
            [tex(Fraction(10) * mass / beta), tex((mass + volume) * 10 / beta), tex(volume * 10 / beta)],
        )


SQUARES = (Fraction(1, 4), Fraction(1, 9), Fraction(4, 9), Fraction(1, 16), Fraction(9, 16), Fraction(4, 25))


@_type(4, "ตำแหน่งที่สนามไฟฟ้าเป็นศูนย์นอกประจุคู่", "การรวมสนามไฟฟ้าแบบเวกเตอร์")
class NullPoint(PhysicsSheet):
    def expr(self, rng):
        beta = rng.choice(SQUARES)
        root = Fraction(isqrt(beta.numerator), isqrt(beta.denominator))
        gap = rng.randint(1, 12)
        answer = agree(q04.solve(beta=float(beta), gap=gap), gap / (1 - root))
        return draw(
            4,
            tex(answer),
            f"ประจุ +Q อยู่ที่ x = 0 และประจุ −{number(beta)}Q อยู่ที่ x = {gap} cm บนแกน x สนามไฟฟ้าลัพธ์เป็นศูนย์ที่ตำแหน่ง x กี่ cm (x > {gap} cm)",
            r"\frac{kQ}{x^2}=\frac{k\beta Q}{(x-a)^2}",
            [tex(gap / (1 + root)), tex(gap / (1 - beta)), tex(gap / root)],
        )


def _slab_pool():
    pool = []
    for inside in SINES:
        for outside in SINES:
            index = outside / inside
            if outside > inside and Fraction(6, 5) <= index <= Fraction(21, 10):
                pool.append((outside, inside))
    return tuple(pool)


SLABS = _slab_pool()


@_type(5, "ระยะเลื่อนขนานของแสงผ่านแผ่นแก้ว", "การเลื่อนขนานของแสงผ่านแผ่นหน้าขนาน")
class SlabShift(PhysicsSheet):
    def expr(self, rng):
        sin_in, sin_glass = rng.choice(SLABS)
        cos_in, cos_glass = cosine(sin_in), cosine(sin_glass)
        thickness = rng.choice((5, 10, 12, 15, 20))
        tilt = sin_in * cos_glass - cos_in * sin_glass
        exact = thickness * tilt / cos_glass
        answer = agree(q05.solve(thickness=thickness, sin_in=float(sin_in), sin_glass=float(sin_glass)), exact)
        return draw(
            5,
            tex(answer),
            f"แสงจากอากาศตกกระทบแผ่นแก้วหน้าขนานหนา {thickness} mm ด้วยมุมตกกระทบ i (sin i = {number(sin_in)}) และหักเหในแก้วเป็นมุม θ (sin θ = {number(sin_glass)}) แนวแสงออกเยื้องจากแนวแสงเข้าเดิมเป็นระยะตั้งฉากกี่ mm",
            r"AB=\frac{L}{\cos\theta},\quad d=AB\sin(i-\theta)",
            [
                tex(thickness * tilt),
                tex(thickness * (sin_in * cos_glass + cos_in * sin_glass) / cos_glass),
                tex(thickness * (cos_in * cos_glass + sin_in * sin_glass) / cos_glass),
            ],
        )


@_type(6, "จำนวนค่าความต้านทานจากตัวต้านทานสามตัว", "การต่อตัวต้านทานแบบอนุกรมและขนาน")
class ResistorCount(PhysicsSheet):
    def expr(self, rng):
        values = tuple(sorted(rng.sample(range(1, 13), 3)))
        answer = q06.solve(values=values)
        generic = 17 if answer != 17 else 16
        listing = ", ".join(f"{v} Ω" for v in values)
        return draw(
            6,
            str(answer),
            f"มีตัวต้านทาน {listing} ใช้ตัวเดียว สองตัว หรือทั้งสามตัวก็ได้ และต่อแบบอนุกรม ขนาน หรือผสมได้ทุกแบบ จะได้ค่าความต้านทานที่แตกต่างกันทั้งหมดกี่ค่า",
            r"3+6+8\text{ arrangements}",
            [str(generic), "9", "11"],
        )


@_type(7, "อัตราการไหลของความร้อนผ่านท่อนโลหะ", "การนำความร้อนคงตัวหนึ่งมิติ")
class HeatFlow(PhysicsSheet):
    def expr(self, rng):
        conductivity = rng.choice((50, 80, 200, 400))
        area = rng.choice((1, 2, 4, 5))
        hot = 10 * rng.randint(5, 15)
        cold = 10 * rng.randint(0, 4)
        length = Fraction(rng.randint(1, 10), 10)
        a = Fraction(area, 10**4)
        exact = a * conductivity * (hot - cold) / length
        answer = agree(q07.solve(conductivity=conductivity, area=area, hot=hot, cold=cold, length=float(length)), exact)
        return draw(
            7,
            tex(answer),
            f"ท่อนโลหะยาว {number(length)} m พื้นที่หน้าตัด {area} cm² สภาพนำความร้อน {conductivity} W/(m °C) ปลายทั้งสองติดกับแหล่งอุณหภูมิ {hot} °C และ {cold} °C ผิวข้างหุ้มฉนวน ในสภาวะคงตัวความร้อนไหลกี่วัตต์",
            r"\frac{Q}{t}=\frac{KA(T_1-T_2)}{L}",
            [str(conductivity * (hot - cold)), tex(a * conductivity * (hot - cold)), tex(conductivity * (hot - cold) / length)],
        )


SPLITS = ((Fraction(2), Fraction(1)), (Fraction(5, 4), Fraction(1, 2)), (Fraction(13, 9), Fraction(2, 3)), (Fraction(10, 9), Fraction(1, 3)), (Fraction(17, 16), Fraction(1, 4)), (Fraction(34, 25), Fraction(3, 5)))


@_type(8, "ความเร็วชิ้นส่วนหลังการระเบิดเพิ่มพลังงาน", "การอนุรักษ์โมเมนตัมในการระเบิด")
class ExplosionSplit(PhysicsSheet):
    def expr(self, rng):
        ratio, spread = rng.choice(SPLITS)
        speed = spread.denominator * rng.randint(1, 5)
        slow, fast = speed * (1 - spread), speed * (1 + spread)
        got = q08.solve(speed=speed, ratio=float(ratio))
        agree(got[0], slow)
        agree(got[1], fast)
        extra = ratio - 1
        return draw(
            8,
            pair(tex(slow), tex(fast)),
            f"วัตถุมวล m เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s แล้วระเบิดออกเป็นสองชิ้นมวลเท่ากันซึ่งยังเคลื่อนที่ไปทางเดิมทั้งคู่ พลังงานจลน์หลังระเบิดเป็น {number(ratio)} เท่าของก่อนระเบิด คู่อัตราเร็ว (v₁, v₂) เป็นกี่ m/s โดย v₁ ≤ v₂",
            r"v_1+v_2=2u,\quad v_1^2+v_2^2=2ku^2",
            [pair(str(speed), str(speed)), pair(tex(fast), tex(slow)), pair(tex(speed * (1 - extra)), tex(speed * (1 + extra)))],
        )


TRIPLES = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10))


@_type(9, "สนามไฟฟ้าบนแกนวงแหวนด้านลบ", "การอินทิเกรตสนามและสมมาตร")
class RingFieldNegativeSide(PhysicsSheet):
    def expr(self, rng):
        radius, distance, hyp = rng.choice(TRIPLES)
        charge = rng.randint(1, 9)
        exact = -Fraction(9 * charge * distance, hyp**3)
        answer = agree(q09.solve(charge=charge, radius=radius, distance=distance), exact)
        return draw(
            9,
            tex(answer),
            f"วงลวดรัศมี {radius} m อยู่ในระนาบ YZ ศูนย์กลางที่ O มีประจุ +{charge} nC กระจายสม่ำเสมอ องค์ประกอบ E_x ของสนามไฟฟ้าที่จุด x = −{distance} m บนแกน X เป็นกี่ V/m (บวกถ้าชี้ไปทาง +X) ให้ k=9×10⁹ N m²/C²",
            r"E_x=\frac{kQx}{(x^2+R^2)^{3/2}}",
            [tex(-exact), "0", tex(-Fraction(9 * charge, hyp * hyp))],
        )


@_type(10, "สนามแม่เหล็กบนแกนวงแหวนประจุหมุนเทียบที่ศูนย์กลาง", "สนามแม่เหล็กบนแกนวงลวด")
class SpinningRingAxial(PhysicsSheet):
    def expr(self, rng):
        radius, distance, hyp = rng.choice(TRIPLES)
        side = rng.choice((1, -1))
        ratio = Fraction(radius, hyp)
        answer = agree(q10.solve(radius=radius, distance=distance), ratio**3)
        return draw(
            10,
            tex(answer),
            f"วงลวดรัศมี {radius} cm มีประจุ Q หมุนรอบแกน X ซึ่งผ่านศูนย์กลางและตั้งฉากกับระนาบวง ทำให้มีสนามแม่เหล็กบนแกน X สนามที่ตำแหน่ง x = {side * distance} cm เป็นกี่เท่าของสนามที่ศูนย์กลาง",
            r"B(x)=\frac{B(0)}{(1+x^2/R^2)^{3/2}}",
            [tex(ratio**2), tex(ratio), tex(Fraction(distance, hyp) ** 3)],
        )


@_type(11, "ความยาวโฟกัสของครึ่งเลนส์นูน", "สูตรผู้สร้างเลนส์")
class SplitLens(PhysicsSheet):
    def expr(self, rng):
        first, second = rng.choice(((1, 1), (1, 2), (2, 1), (1, 3), (2, 3), (3, 2)))
        focal = 5 * rng.randint(2, 8)
        exact = focal * (1 + Fraction(first, second))
        answer = agree(q11.solve(focal=focal, first=first, second=second), exact)
        shape = "สมมาตร" if first == second else f"ที่มีรัศมีความโค้งผิวหน้า R₁ และผิวหลัง R₂ โดย R₁ : R₂ = {first} : {second}"
        return draw(
            11,
            tex(answer),
            f"เลนส์นูนสองหน้าบาง{shape} มีความยาวโฟกัส {focal} cm ผ่าเลนส์ตามระนาบกลางระหว่างผิวทั้งสองได้เลนส์นูนแกมราบสองชิ้น ชิ้นที่มีผิวโค้ง R₁ มีความยาวโฟกัสกี่ cm",
            r"\frac1F=(\mu-1)\left(\frac1{R_1}+\frac1{R_2}\right)",
            [tex(Fraction(focal, 2)), str(focal), tex(focal * (1 + Fraction(second, first)))],
        )


@_type(12, "ระยะห่างน้อยที่สุดระหว่างวัตถุจริงกับภาพจริง", "สมการเลนส์และกำลังขยายภาพเสมือน")
class MinimumSeparation(PhysicsSheet):
    def expr(self, rng):
        focal = rng.randint(2, 30)
        answer = agree(q12.solve(focal=focal), 4 * focal)
        return draw(
            12,
            str(answer),
            f"ใช้เลนส์นูนความยาวโฟกัส {focal} cm สร้างภาพจริงของวัตถุจริง ระยะห่างระหว่างวัตถุกับภาพจริงต้องไม่น้อยกว่ากี่ cm",
            r"x=u+\frac{uf}{u-f}",
            [str(2 * focal), str(focal), str(3 * focal)],
        )


WEDGE_TANS = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5), Fraction(8, 15), Fraction(15, 8))


def _sin_cos(tangent):
    hyp = isqrt(tangent.numerator**2 + tangent.denominator**2)
    return Fraction(tangent.numerator, hyp), Fraction(tangent.denominator, hyp)


@_type(13, "ความเร่งที่ผลักลิ่มให้มวลไม่ไถล", "แรงในกรอบอ้างอิงที่มีความเร่ง")
class PushedWedge(PhysicsSheet):
    def expr(self, rng):
        tangent = rng.choice(WEDGE_TANS)
        sine, cos = _sin_cos(tangent)
        answer = agree(q13.solve(tangent=float(tangent)), 10 * tangent)
        return draw(
            13,
            tex(answer),
            f"มวล m วางบนผิวเอียงลื่นของลิ่มที่ทำมุม β กับพื้น (tan β = {number(tangent)}) ผิวเอียงลาดลงในทิศเดียวกับที่ผลัก ต้องผลักลิ่มบนพื้นระดับด้วยความเร่งกี่ m/s² มวล m จึงอยู่นิ่งเทียบกับลิ่ม ให้ g=10 m/s²",
            r"N\sin\beta=ma,\quad N\cos\beta=mg",
            [tex(10 * sine), tex(10 * cos), tex(10 / tangent)],
        )


@_type(14, "แรงตึงจุดต่ำสุดของเชือกขึงระหว่างเสา", "สมดุลเชือกที่มีน้ำหนัก")
class RopeBetweenPoles(PhysicsSheet):
    def expr(self, rng):
        tangent = rng.choice(WEDGE_TANS)
        sine, _ = _sin_cos(tangent)
        mass = rng.randint(1, 12)
        exact = 5 * mass * tangent
        answer = agree(q14.solve(mass=mass, tangent=float(tangent)), exact)
        return draw(
            14,
            tex(answer),
            f"เชือกมวล {mass} kg ขึงระหว่างยอดเสาสองต้นที่สูงเท่ากัน เชือกที่ยอดเสาทำมุม θ กับแนวดิ่ง (tan θ = {number(tangent)}) แรงตึงในเชือกที่จุดต่ำสุดกึ่งกลางระหว่างเสาเป็นกี่ N ให้ g=10 m/s²",
            r"T_{top}\cos\theta=\tfrac12Mg,\quad T_0=T_{top}\sin\theta",
            [tex(10 * mass * tangent), tex(5 * mass / tangent), tex(5 * mass * sine)],
        )


@_type(15, "ศูนย์กลางมวลของแผ่นกลมที่ถูกเจาะรู", "ศูนย์กลางมวลของวัตถุแผ่น")
class DiscWithHole(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.choice((Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 3)))
        radius = 12 * rng.randint(1, 4)
        exact = ratio * ratio * radius / (1 + ratio)
        answer = agree(q15.solve(radius=radius, ratio=float(ratio)), exact)
        hole = ratio * radius
        return draw(
            15,
            tex(answer),
            f"แผ่นกลมบางสม่ำเสมอรัศมี {radius} cm ศูนย์กลาง O ถูกเจาะรูวงกลมรัศมี {number(hole)} cm โดยขอบรูแตะขอบแผ่นด้านหนึ่ง (ศูนย์กลางรูห่าง O {number(radius - hole)} cm) ศูนย์กลางมวลของแผ่นที่เหลืออยู่ห่างจาก O กี่ cm",
            r"x_{cm}=-\frac{A_{hole}\,d}{A-A_{hole}}",
            [tex(ratio * ratio * (1 - ratio) * radius), tex((1 - ratio) * radius), tex(ratio * radius)],
        )


@_type(16, "แรงปฏิกิริยาของท่อฉีดน้ำ", "การดลจากการไหลของของไหล")
class HoseReaction(PhysicsSheet):
    def expr(self, rng):
        area = rng.randint(2, 20)
        speed = rng.randint(5, 30)
        exact = Fraction(area * speed * speed, 10)
        answer = agree(q16.solve(area=area, speed=speed), exact)
        return draw(
            16,
            tex(answer),
            f"ท่อฉีดน้ำดับเพลิงมีปากท่อพื้นที่หน้าตัด {area} cm² น้ำ (1000 kg/m³) พุ่งออกด้วยอัตราเร็ว {speed} m/s แรงปฏิกิริยาที่น้ำกระทำต่อท่อมีขนาดกี่ N",
            r"F=\dot mv=\rho Av^2",
            [tex(Fraction(area * speed, 10)), tex(exact / 2), tex(exact * 2)],
        )


@_type(17, "แรงตึงในวงลวดที่หมุน", "การเคลื่อนที่แบบวงกลมของวัตถุต่อเนื่อง")
class SpinningRingTension(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 6)
        speed = rng.randint(2, 12)
        radius = rng.choice((Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)))
        top = mass * speed * speed / (2 * radius)
        agree(q17.solve(mass=mass, speed=speed, radius=float(radius)), float(top) / pi)
        return draw(
            17,
            over_pi(top),
            f"วงลวดวงกลมมวล {mass} kg รัศมี {number(radius)} m หมุนรอบแกนที่ผ่านศูนย์กลางและตั้งฉากกับระนาบวงด้วยอัตราเร็วตามแนววง {speed} m/s แรงตึงในลวดเนื่องจากการหมุนมีขนาดกี่ N",
            r"T\theta=\left(\frac{M\theta}{2\pi}\right)\frac{v^2}{R}",
            [tex(2 * top), over_pi(2 * top), over_pi(top / 2)],
        )


@_type(18, "อัตราส่วนอัตราเร็วหลังชนเยื้องแบบยืดหยุ่น", "แรงดลตามแนวศูนย์กลางของผิวเกลี้ยง")
class GlancingRatio(PhysicsSheet):
    def expr(self, rng):
        sine = rng.choice(SINES)
        cos = cosine(sine)
        answer = agree(q18.solve(sine=float(sine)), sine / cos)
        return draw(
            18,
            tex(answer),
            f"ทรงกลมเกลี้ยง M₁ และ M₂ มวลเท่ากัน M₁ เคลื่อนที่ชน M₂ ที่อยู่นิ่งแบบยืดหยุ่นเยื้องศูนย์กลาง ขณะชนความเร็วของ M₁ ทำมุม θ กับแนวเส้นต่อศูนย์กลาง (sin θ = {number(sine)}) อัตราส่วนอัตราเร็วหลังชนของ M₁ ต่อของ M₂ เป็นเท่าใด",
            r"v_2=u\cos\theta,\quad v_1=u\sin\theta",
            [tex(cos / sine), tex(sine), tex(cos)],
        )


@_type(19, "ระยะตกของโพรเจกไทล์ที่เฉียดยอดเสาสองต้น", "การเคลื่อนที่แบบโพรเจกไทล์")
class PoleGrazing(PhysicsSheet):
    def expr(self, rng):
        first, second = rng.randint(2, 20), rng.randint(2, 30)
        answer = agree(q19.solve(first=first, second=second), first + second)
        return draw(
            19,
            str(answer),
            f"ยิงโพรเจกไทล์จากจุด O บนพื้นระดับให้เฉียดยอดเสาดิ่ง A และ B ที่สูงเท่ากันพอดี เสา A ห่างจาก O {first} m และเสา B อยู่ถัดไปอีก {second} m (ทางเดียวกัน) โพรเจกไทล์ตกถึงพื้นห่างจากเสา A กี่ m",
            r"\text{equal heights are symmetric about the apex}",
            [str(second), str(2 * first + second), tex(Fraction(2 * first + second, 2))],
        )


GASES = {"ไฮโดรเจน": 2, "ฮีเลียม": 4, "ไนโตรเจน": 28, "อากาศ": 29, "ออกซิเจน": 32, "คาร์บอนไดออกไซด์": 44}


@_type(20, "อัตราเร็วเสียงในรูปอุณหภูมิและมวลโมเลกุล", "อัตราเร็วเสียงในแก๊ส")
class SoundSpeedGas(PhysicsSheet):
    def expr(self, rng):
        name = rng.choice(sorted(GASES))
        molar = GASES[name]
        celsius = rng.choice((-73, 0, 27, 127, 227))
        exact = Fraction(83, 10) * (celsius + 273) * 1000 / molar
        answer = agree(q20.solve(celsius=celsius, molar=molar), exact)
        return draw(
            20,
            tex(answer),
            f"อัตราเร็วเสียงในแก๊สเป็นไปตาม v² = γP/ρ สำหรับ{name} (มวลโมเลกุล {molar} g/mol) ซึ่งถือเป็นแก๊สอุดมคติที่อุณหภูมิ {celsius} °C ค่า v²/γ เป็นกี่ m²/s² ใช้ R = 8.3 J mol⁻¹ K⁻¹ และ K = °C + 273",
            r"\frac P\rho=\frac{RT}{M}",
            [
                tex(Fraction(83, 10) * celsius * 1000 / molar) if celsius else "0",
                tex(Fraction(83, 10) * (celsius + 273) / molar),
                tex(Fraction(molar, 1000) / (Fraction(83, 10) * (celsius + 273))),
            ],
        )


@_type(21, "กำลังสูงสุดที่โหลดจากเงื่อนไขรากจริง", "เงื่อนไขรากจริงและการถ่ายโอนกำลังสูงสุด")
class MaxLoadPower(PhysicsSheet):
    def expr(self, rng):
        emf = rng.randint(2, 24)
        internal = Fraction(rng.randint(1, 10), 2)
        exact = emf * emf / (4 * internal)
        answer = agree(q21.solve(emf=emf, internal=float(internal)), exact)
        return draw(
            21,
            tex(answer),
            f"แหล่งกำเนิดแรงเคลื่อน {emf} V ความต้านทานภายใน {number(internal)} Ω จ่ายไฟให้ตัวต้านทาน R กำลังที่ R เป็นไปตาม R² − (ε²/P − 2r)R + r² = 0 ซึ่ง R ต้องเป็นจำนวนจริง กำลังมากที่สุดที่ R เป็นกี่ W",
            r"\left(\frac{\varepsilon^2}P-2r\right)^2\ge4r^2",
            [tex(4 * exact), tex(2 * exact), tex(exact / 2)],
        )


@_type(22, "ร้อยละของพลังงานที่เหลือหลังแบ่งประจุ", "พลังงานตัวเก็บประจุและการแบ่งประจุ")
class EnergyRetained(PhysicsSheet):
    def expr(self, rng):
        first, second = rng.sample(range(1, 10), 2)
        exact = Fraction(100 * first, first + second)
        answer = agree(q22.solve(first=first, second=second), exact)
        return draw(
            22,
            tex(answer),
            f"ตัวเก็บประจุ C₁ = {first} μF มีประจุ ต่อผ่านสวิตช์กับตัวเก็บประจุ C₂ = {second} μF ที่ไม่มีประจุ หลังสับสวิตช์ พลังงานไฟฟ้าของระบบเหลือกี่เปอร์เซ็นต์ของก่อนสับ",
            r"U\propto\frac{Q^2}{C_{total}}",
            [tex(Fraction(100 * second, first + second)), "50", tex(Fraction(100 * first * first, (first + second) ** 2))],
        )


@_type(23, "ประจุที่เหลือหลังต่อกับตัวเก็บประจุหลายตัว", "พลังงานตัวเก็บประจุและการแบ่งประจุ")
class ChargeSplit(PhysicsSheet):
    def expr(self, rng):
        caps = [rng.randint(1, 6) for _ in range(4)]
        total = sum(caps)
        charge = total * rng.randint(1, 10)
        exact = Fraction(charge * caps[0], total)
        answer = agree(q23.solve(charge=charge, c1=caps[0], c2=caps[1], c3=caps[2], c4=caps[3]), exact)
        return draw(
            23,
            tex(answer),
            f"ตัวเก็บประจุ C₁ = {caps[0]} μF มีประจุ {charge} μC ต่อผ่านสวิตช์กับตัวเก็บประจุ C₂ = {caps[1]} μF, C₃ = {caps[2]} μF และ C₄ = {caps[3]} μF ที่ต่อขนานกันและไม่มีประจุ หลังสับสวิตช์ครู่หนึ่ง C₁ มีประจุกี่ μC",
            r"V=\frac{q}{\sum C_i},\quad q_1=C_1V",
            [tex(Fraction(charge, 4)), tex(Fraction(charge * (total - caps[0]), total)), tex(Fraction(charge * caps[0], caps[0] + caps[1]))],
        )


@_type(24, "มุมเอียงของแผ่นที่ห้อยมวลที่มุมล่าง", "สมดุลโมเมนต์ของวัตถุแข็งเกร็ง")
class PlateTiltRatio(PhysicsSheet):
    def expr(self, rng):
        plate, hung = rng.randint(1, 12), rng.randint(1, 6)
        exact = Fraction(hung, plate + 2 * hung)
        answer = agree(q24.solve(plate=plate, hung=hung), exact)
        return draw(
            24,
            tex(answer),
            f"แผ่นสี่เหลี่ยมผืนผ้าสม่ำเสมอมวล {plate} kg กว้าง a (ด้านตั้ง) ยาว b (ด้านบน) แขวนด้วยเชือกที่จุดกึ่งกลางด้านบน แล้วห้อยมวล {hung} kg ที่มุมล่างด้านหนึ่ง แผ่นเอียงทำมุม θ กับแนวระดับ ค่า (tan θ)·(a/b) เป็นเท่าใด",
            r"M\frac a2\sin\theta=m\left(\frac b2\cos\theta-a\sin\theta\right)",
            [tex(Fraction(hung, plate + hung)), tex(Fraction(hung, plate)), tex(Fraction(2 * hung, plate + 2 * hung))],
        )


@_type(25, "ความเร็วของมวลเล็กหลังชนกับมวลใหญ่ที่สะท้อนกำแพง", "การชนยืดหยุ่นหนึ่งมิติ")
class WallRebound(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.choice((2, 3, 4, 9, 19, 99))
        speed = rng.randint(1, 10)
        exact = Fraction(speed * (3 * ratio - 1), ratio + 1)
        answer = agree(q25.solve(ratio=ratio, speed=speed), exact)
        return draw(
            25,
            tex(answer),
            f"มวล m และ M = {ratio}m เคลื่อนที่ไปทางกำแพงแข็งบนพื้นลื่นด้วยอัตราเร็ว {speed} m/s เท่ากัน โดย M นำหน้า M ชนกำแพงแบบยืดหยุ่นแล้วชนกับ m แบบยืดหยุ่น หลังจากนั้น m มีอัตราเร็วกี่ m/s เทียบกับกำแพง",
            r"v_m=\frac{(m-M)u+2M(-u)}{m+M}",
            [str(speed), str(2 * speed), str(3 * speed)],
        )


@_type(26, "ปริมาตรไอน้ำจากน้ำ 1.8 กรัม", "กฎแก๊สอุดมคติกับการเปลี่ยนสถานะ")
class SteamGrams(PhysicsSheet):
    def expr(self, rng):
        mass = rng.choice((Fraction(9, 10), Fraction(9, 5), Fraction(18, 5), Fraction(9)))
        celsius = rng.choice((107, 127, 227, 327))
        pressure = rng.choice((1, 2))
        exact = mass / 18 * Fraction(83, 10) * (celsius + 273) / (pressure * 10**5) * 10**6
        answer = agree(q26.solve(mass=float(mass), celsius=celsius, pressure=pressure * 1e5), exact)
        celsius_form = mass / 18 * Fraction(83, 10) * celsius / (pressure * 10**5) * 10**6
        return draw(
            26,
            sci(answer),
            f"น้ำ {number(mass)} g (มวลโมเลกุล 18 g/mol) กลายเป็นไอน้ำที่ความดัน {pressure}×10⁵ N/m² อุณหภูมิ {celsius} °C ถือว่าไอน้ำเป็นแก๊สอุดมคติ ปริมาตรไอน้ำเป็นประมาณกี่ cm³ ใช้ R = 8.3 J mol⁻¹ K⁻¹",
            r"V=\frac{nRT}{P}",
            [sci(celsius_form), sci(exact / 10**6), sci(exact * 18)],
        )


@_type(27, "ระยะหน้าผาจากเสียงสะท้อนของเรือที่แล่นขนาน", "เสียงสะท้อนจากผู้สังเกตที่เคลื่อนที่")
class ParallelEcho(PhysicsSheet):
    def expr(self, rng):
        sound = 340
        boat = rng.choice((10, 20, 30, 40, 50))
        time = rng.randint(1, 8)
        squared = Fraction(time * time * (sound * sound - boat * boat), 4)
        agree(q27.solve(time=time, sound=sound, boat=boat) ** 2, squared)
        return draw(
            27,
            radical(squared),
            f"เรือแล่นขนานกับหน้าผาด้วยอัตราเร็ว {boat} m/s เปิดหวูดสั้นๆ และได้ยินเสียงสะท้อนจากหน้าผาหลังจากนั้น {time} s อัตราเร็วเสียงในอากาศนิ่ง {sound} m/s หน้าผาอยู่ห่างแนวการแล่นของเรือกี่ m",
            r"\left(\frac{vT}2\right)^2=L^2+\left(\frac{uT}2\right)^2",
            [
                tex(Fraction(sound * time, 2)),
                radical(Fraction(time * time * (sound * sound + boat * boat), 4)),
                tex(Fraction((sound - boat) * time, 2)),
            ],
        )


@_type(28, "ความเร็วสุดท้ายของลิ่มเมื่อมวลไถลถึงพื้น", "โมเมนตัมแนวระดับของลิ่มและมวล")
class WedgeEnergyRecoil(PhysicsSheet):
    def expr(self, rng):
        small, big = rng.randint(1, 6), rng.randint(1, 12)
        squared = Fraction(small * small, big * (big + small))
        agree(q28.solve(small=small, big=big) ** 2, squared)
        return draw(
            28,
            radical(squared),
            f"ลิ่มมวล {big} kg สูง h วางบนพื้นระดับลื่น ปล่อยมวล {small} kg จากหยุดนิ่งที่ยอดลิ่มให้ไถลลงผิวลื่นจนถึงพื้นแล้วเคลื่อนที่ไปตามพื้น ความเร็วสุดท้ายของลิ่มเป็นกี่เท่าของ √(2gh)",
            r"mv=MV,\quad\tfrac12mv^2+\tfrac12MV^2=mgh",
            [tex(Fraction(small, big + small)), tex(Fraction(small, big)), radical(Fraction(small, big + small))],
        )


RECEDING = {
    "sin θ ต่ำสุด": (Fraction(1, 9), Fraction(8, 9), "sin"),
    "cos θ สูงสุด": (Fraction(8, 9), Fraction(1, 9), "cos"),
    "tan² θ ต่ำสุด": (Fraction(1, 8), Fraction(8), "tan2"),
}


@_type(29, "มุมยิงที่ระยะจากจุดยิงเพิ่มขึ้นตลอด", "การเคลื่อนที่แบบโพรเจกไทล์")
class RecedingProjectile(PhysicsSheet):
    def expr(self, rng):
        asked = rng.choice(sorted(RECEDING))
        square, other, kind = RECEDING[asked]
        sin_min = q29.solve()
        agree(sin_min**2, Fraction(1, 9))
        answer = tex(square) if kind == "tan2" else radical(square)
        swapped = tex(other) if kind == "tan2" else radical(other)
        unsquared = radical(square) if kind == "tan2" else tex(square)
        return draw(
            29,
            answer,
            f"ยิงโพรเจกไทล์จากจุด O ด้วยอัตราเร็ว u ทำมุม θ กับแนวดิ่ง อัตราการเปลี่ยนของ r² (r คือระยะจาก O) เป็น g²t[(t − 3u cosθ/(2g))² + (2u²/g²)(1 − (9/8)cos²θ)] ต้องการให้ r เพิ่มขึ้นตลอดเวลา ค่า{asked}ที่ยอมให้เป็นเท่าใด",
            r"1-\tfrac98\cos^2\theta\ge0",
            [swapped, unsquared, "1"],
        )


def _lens_pairs():
    pool = []
    for a in (5, 10, 15, 20):
        for b in (10, 15, 20, 30):
            for d in range(b + 5, 6 * b + 1, 5):
                u = Fraction(b * d, d - b)
                if u.denominator == 1 and u > a:
                    pool.append((a, b, d))
    return tuple(pool)


LENS_PAIRS = _lens_pairs()


@_type(30, "ระยะระหว่างเลนส์เว้าและเลนส์นูนให้แสงรวมที่จุดกำหนด", "ระบบเลนส์หลายตัว")
class DivergingConverging(PhysicsSheet):
    def expr(self, rng):
        a, b, d = rng.choice(LENS_PAIRS)
        u = Fraction(b * d, d - b)
        answer = agree(q30.solve(diverging=a, converging=b, focus=d), u - a)
        return draw(
            30,
            tex(answer),
            f"ลำแสงขนานผ่านเลนส์เว้าความยาวโฟกัส −{a} cm แล้วผ่านเลนส์นูนความยาวโฟกัส {b} cm ที่อยู่ห่างออกไป x ลำแสงไปรวมกันที่ระยะ {d} cm หลังเลนส์นูน x เป็นกี่ cm",
            r"\frac1u+\frac1d=\frac1{f_B},\quad x=u-|f_A|",
            [tex(u), tex(u + a), str(a + b)],
        )
