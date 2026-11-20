"""Seeded variants of the reviewed POSN physics 2565 camp selection paper."""

from fractions import Fraction
from math import isqrt, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2565_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2565_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2565_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29, q30

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


def over_pi(value):
    """value / pi as exact TeX."""
    value = Fraction(value)
    top = "" if value.numerator == 1 else str(value.numerator)
    return rf"\frac{{{top or 1}}}{{{value.denominator if value.denominator != 1 else ''}\pi}}"


def times_pi(value):
    """value * pi as exact TeX."""
    value = Fraction(value)
    top = "" if value.numerator == 1 else str(value.numerator)
    if value.denominator == 1:
        return rf"{top}\pi"
    return rf"\frac{{{top}\pi}}{{{value.denominator}}}"


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


SLIPS = {
    1: ("phys.exponent_units_inverted", "phys.exponent_speed_unit_inverted", "phys.exponent_mass_omitted"),
    2: ("phys.parallel_source_alone", "phys.parallel_source_rail_voltage", "phys.parallel_source_shared_equally"),
    3: ("phys.field_angle_negative_reversed", "phys.field_angle_one_charge", "phys.field_angle_charge_ratio"),
    4: ("phys.shell_potential_sign", "phys.shell_inner_only", "phys.shell_outer_only"),
    5: ("phys.sling_one_strap", "phys.sling_sine_multiplied", "phys.sling_weight_as_tension"),
    6: ("phys.charging_power_heat_ignored", "phys.charging_power_storage_ignored", "phys.charging_power_heat_subtracted"),
    7: ("phys.orbit_pair_radius_full", "phys.orbit_pair_coulomb_half", "phys.orbit_pair_reduced_twice"),
    8: ("phys.rope_horizontal_used_tan", "phys.rope_horizontal_used_sine", "phys.rope_horizontal_used_cosine"),
    9: ("phys.offset_impact_head_on", "phys.offset_impact_used_sine", "phys.offset_impact_projected_twice"),
    10: ("phys.retro_mirror_lens_ignored", "phys.retro_mirror_focal_length", "phys.retro_mirror_halved"),
    11: ("phys.half_loop_full_circle", "phys.half_loop_opposed", "phys.half_loop_full_and_opposed"),
    12: ("phys.chord_time_times_cosine", "phys.chord_time_over_cosine", "phys.chord_time_root_cosine"),
    14: ("phys.steam_volume_units_omitted", "phys.steam_volume_celsius", "phys.steam_volume_freezing_point"),
    15: ("phys.spring_pair_one_side", "phys.spring_pair_halved", "phys.spring_pair_half_spring_doubled"),
    16: ("phys.tilt_slide_no_normal_factor", "phys.tilt_slide_friction_added", "phys.tilt_slide_sin_cos_swapped"),
    17: ("phys.coaxial_end_area", "phys.coaxial_no_circumference", "phys.coaxial_wrong_geometry"),
    18: ("phys.push_limit_inverted", "phys.push_limit_squared", "phys.push_limit_difference"),
    19: ("phys.release_weight_ignored", "phys.release_weight_added", "phys.release_ratio_inverted"),
    20: ("phys.wire_fields_added_scalar", "phys.wire_field_one_wire", "phys.wire_fields_opposed"),
    21: ("phys.angular_momentum_sines_ignored", "phys.angular_momentum_used_cosine", "phys.angular_momentum_inverted"),
    22: ("phys.gamma_diatomic_only", "phys.gamma_monatomic_only", "phys.gamma_averaged"),
    23: ("phys.em_field_divided_by_c", "phys.em_field_times_c_squared", "phys.em_field_divided_by_c_squared"),
    24: ("phys.wire_field_area_multiplied", "phys.wire_field_inverted", "phys.wire_field_conductivity_on_top"),
    25: ("phys.jet_reversal_one_way", "phys.jet_reversal_half_dynamic", "phys.jet_reversal_speed_not_squared"),
    26: ("phys.thermal_stress_area_omitted", "phys.thermal_force_halved", "phys.thermal_strain_alpha_omitted"),
    27: ("phys.aim_drop_doubled", "phys.aim_drop_as_angle", "phys.aim_drop_halved"),
    28: ("phys.echo_speed_returns_ignored", "phys.echo_speed_sign", "phys.echo_speed_one_way"),
    29: ("phys.spoke_gap_halved", "phys.spoke_tip_speed", "phys.spoke_single_gap"),
    30: ("phys.cone_period_cosine", "phys.cone_period_inverted", "phys.cone_period_inverse_cosine"),
}

# Sines whose cosines are rational, for angles that keep answers exact.
SINES = tuple(
    Fraction(a, c)
    for a, b, c in ((3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17))
    for a in (a, b)
)


def cosine(sine):
    root = Fraction(isqrt(sine.denominator**2 - sine.numerator**2), sine.denominator)
    assert root * root + sine * sine == 1
    return root


def draw(number_, answer, prompt, hint, slips):
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number_], slips)],
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2565_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2565)"


def _unit(kg, m, s):
    parts = []
    for name, power in (("kg", kg), ("m", m), ("s", s)):
        if power:
            parts.append(rf"\mathrm{{{name}}}" + ("" if power == 1 else f"^{{{power}}}"))
    return r"\,".join(parts) or "1"


EXPONENTS = {(1, 1): "mv", (1, 2): "mv²", (1, 3): "mv³", (2, 2): "m²v²", (1, 4): "mv⁴"}


@question_type(
    "phys.posn2565_q01",
    display_name={"th": "หน่วยของค่าคงตัวในเลขชี้กำลัง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="มิติและหน่วยในเลขชี้กำลัง",
)
class ExponentUnits(PhysicsSheet):
    def expr(self, rng):
        (a, b), quantity = rng.choice(sorted(EXPONENTS.items()))
        kg, m, s = q01.solve(mass_power=a, speed_power=b)
        return draw(
            1,
            _unit(kg, m, s),
            f"สมการ A = B·2^(−X/C) โดย X = {quantity} เมื่อ m เป็นมวลในหน่วย kg และ v เป็นอัตราเร็วในหน่วย m/s หน่วย SI ของค่าคงตัว C เป็นข้อใด",
            r"[X/C]=1\Rightarrow[C]=[X]",
            [_unit(-kg, -m, -s), _unit(kg, m, -s), _unit(0, m, s)],
        )


@question_type(
    "phys.posn2565_q02",
    display_name={"th": "กระแสในแขนงแบตเตอรี่ขนาน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎเคอร์ชอฟฟ์ของแหล่งจ่ายขนาน",
)
class ParallelSources(PhysicsSheet):
    def expr(self, rng):
        while True:
            count = rng.randint(3, 5)
            emfs = [rng.randint(2, 12) for _ in range(count)]
            branch = rng.randrange(count)
            rail = Fraction(sum(emfs), count)
            if rail != emfs[branch]:
                break
        resistance = rng.choice((1, 2, 4))
        exact = abs(emfs[branch] - rail) / resistance
        answer = agree(q02.solve(emfs=tuple(emfs), resistance=resistance, branch=branch), exact)
        listing = ", ".join(f"{e} V" for e in emfs)
        return draw(
            2,
            tex(answer),
            f"แบตเตอรี่อุดมคติ {count} ก้อนมีแรงเคลื่อน {listing} ตามลำดับ แต่ละก้อนต่ออนุกรมกับตัวต้านทาน {resistance} Ω เป็นหนึ่งแขนง แล้วต่อทุกแขนงขนานกันระหว่างสายสองเส้น โดยขั้วบวกของทุกก้อนหันไปทางสายเดียวกัน กระแสในแขนงที่ {branch + 1} (แบตเตอรี่ {emfs[branch]} V) มีขนาดกี่ A",
            r"\sum_i\frac{\mathcal E_i-V}{R}=0",
            [tex(Fraction(emfs[branch], resistance)), tex(rail / resistance), tex(Fraction(emfs[branch], count * resistance))],
        )


def _charge(n, sign):
    return f"{sign}Q" if n == 1 else f"{sign}{n}Q"


@question_type(
    "phys.posn2565_q03",
    display_name={"th": "ทิศสนามไฟฟ้าลัพธ์จากสองประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การรวมสนามไฟฟ้าแบบเวกเตอร์",
)
class FieldDirection(PhysicsSheet):
    def expr(self, rng):
        positive = rng.randint(2, 6)
        negative = rng.randint(1, positive - 1)
        exact = Fraction(positive - negative, positive + negative)
        answer = agree(q03.solve(positive=positive, negative=negative), exact)
        return draw(
            3,
            tex(answer),
            f"ประจุ {_charge(positive, '+')} อยู่ที่ (0, 0) และประจุ {_charge(negative, '−')} อยู่ที่ (2a, 0) สนามไฟฟ้าลัพธ์ที่จุด (a, a) ทำมุม θ กับแกน +X (วัดทวนเข็มนาฬิกา) tan θ มีค่าเท่าใด",
            r"\vec E=\sum\frac{kq\,\vec r}{r^3}",
            [tex(1 / exact), "1", tex(Fraction(negative, positive))],
        )


@question_type(
    "phys.posn2565_q04",
    display_name={"th": "ผลต่างศักย์ระหว่างทรงกลมร่วมศูนย์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ศักย์ไฟฟ้าของตัวนำทรงกลม",
)
class GroundedShell(PhysicsSheet):
    def expr(self, rng):
        inner, outer = sorted(rng.sample((1, 2, 3, 4, 5, 6, 8, 9, 10), 2))
        charge = rng.randint(1, 9)
        exact = 900 * charge * (Fraction(1, inner) - Fraction(1, outer))
        answer = agree(q04.solve(charge=charge, inner=inner, outer=outer), exact)
        return draw(
            4,
            tex(answer),
            f"ทรงกลมโลหะอันในรัศมี {inner} cm มีประจุ −{charge} nC อยู่ภายในทรงกลมโลหะบางอันนอกรัศมี {outer} cm ซึ่งมีศูนย์กลางร่วมกันและต่อลงดิน ทรงกลมอันนอกมีศักย์ไฟฟ้าสูงกว่าอันในกี่ V ให้ k=9×10⁹ N m²/C²",
            r"V_{out}-V_{in}=kQ\left(\frac1{R_1}-\frac1{R_2}\right)",
            [tex(-exact), tex(Fraction(900 * charge, inner)), tex(Fraction(900 * charge, outer))],
        )


@question_type(
    "phys.posn2565_q05",
    display_name={"th": "แรงตึงแถบเชือกที่รองรับทรงกระบอก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลของแรงบนวัตถุทรงกลม",
)
class SlingTension(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 20)
        sine = rng.choice(SINES)
        exact = Fraction(10 * mass) / (2 * sine)
        answer = agree(q05.solve(mass=mass, sine=float(sine)), exact)
        return draw(
            5,
            tex(answer),
            f"ทรงกระบอกผิวลื่นมวล {mass} kg วางสมดุลบนแถบเชือกเบาที่แขวนจากจุดตรึงสองจุด แถบเชือกทั้งสองข้างทำมุม θ กับแนวระดับ โดย sin θ = {number(sine)} แรงตึงในแถบเชือกมีขนาดกี่ N ให้ g=10 m/s²",
            r"2T\sin\theta=Mg",
            [tex(10 * mass / sine), tex(10 * mass * sine), str(10 * mass)],
        )


@question_type(
    "phys.posn2565_q06",
    display_name={"th": "กำลังของแหล่งจ่ายขณะอัดประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานในวงจร RC",
)
class ChargingPower(PhysicsSheet):
    def expr(self, rng):
        cap = rng.randint(1, 5)
        charge = cap * rng.randint(1, 6)
        current = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2)))
        resistance = rng.randint(1, 10)
        store = Fraction(charge, cap) * current
        heat = resistance * current**2
        answer = agree(
            q06.solve(charge=charge * 1e-6, capacitance=cap * 1e-6, current=float(current), resistance=resistance),
            store + heat,
        )
        return draw(
            6,
            tex(answer),
            f"แหล่งจ่ายแรงเคลื่อน ℰ อัดประจุตัวเก็บประจุ {cap} μF ผ่านตัวต้านทาน {resistance} Ω ขณะที่ตัวเก็บประจุมีประจุ {charge} μC และกระแส {number(current)} A แหล่งจ่ายทำงานด้วยอัตรากี่ W",
            r"\mathcal E=IR+\frac qC,\quad P=\mathcal EI",
            [tex(store), tex(heat), tex(store - heat)],
        )


@question_type(
    "phys.posn2565_q07",
    display_name={"th": "อัตราเร็วของคู่ประจุที่โคจรรอบกัน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แบบวงกลมด้วยแรงไฟฟ้า",
)
class OrbitingPair(PhysicsSheet):
    def expr(self, rng):
        charge = rng.randint(1, 6)
        mass = rng.choice((1, 2, 4, 5, 9, 10))
        distance = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(9, 10), Fraction(1)))
        squared = Fraction(9 * charge * charge, 2 * mass) / distance
        agree(q07.solve(charge=charge, mass=mass, distance=float(distance)) ** 2, squared)
        return draw(
            7,
            radical(squared),
            f"อนุภาคมีประจุ +{charge} μC กับ −{charge} μC มีมวลเท่ากันอนุภาคละ {mass} g โคจรรอบกันและกันที่ระยะห่าง {number(distance)} m คงที่ ไม่คิดแรงโน้มถ่วง อัตราเร็วของแต่ละอนุภาคเป็นกี่ m/s ให้ k=9×10⁹ N m²/C²",
            r"\frac{mv^2}{D/2}=\frac{kQ^2}{D^2}",
            [radical(2 * squared), radical(4 * squared), radical(squared / 2)],
        )


@question_type(
    "phys.posn2565_q08",
    display_name={"th": "แรงตึงแนวระดับของเชือกหนัก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลเชือกที่มีน้ำหนัก",
)
class HeavyRopeHorizontal(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 12)
        sine = rng.choice(SINES)
        cos = cosine(sine)
        exact = 10 * mass * cos / sine
        answer = agree(q08.solve(mass=mass, sine=float(sine)), exact)
        return draw(
            8,
            tex(answer),
            f"เชือกสม่ำเสมอมวล {mass} kg แขวนสมดุลระหว่างจุด O กับ A โดยเชือกที่ O อยู่ในแนวระดับ และที่ A ทำมุม θ กับแนวระดับ (sin θ = {number(sine)}) แรงแนวระดับ H ที่ O มีขนาดกี่ N ให้ g=10 m/s²",
            r"T_A\sin\theta=Mg,\quad H=T_A\cos\theta",
            [tex(10 * mass * sine / cos), tex(10 * mass * sine), tex(10 * mass * cos)],
        )


@question_type(
    "phys.posn2565_q09",
    display_name={"th": "อัตราเร็วของทรงกลมเป้าหลังชนเยื้อง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงดลตามแนวศูนย์กลางของผิวเกลี้ยง",
)
class OffsetImpactSpeed(PhysicsSheet):
    def expr(self, rng):
        sine = rng.choice((Fraction(1, 2), Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13)))
        radius = sine.denominator * rng.randint(1, 2)
        offset = 2 * radius * sine
        speed = rng.randint(2, 12)
        squared = speed * speed * (1 - sine * sine)
        agree(q09.solve(offset=float(offset), radius=radius, speed=speed) ** 2, squared)
        return draw(
            9,
            radical(squared),
            f"ทรงกลมตันผิวเกลี้ยง A และ B มีมวลและรัศมีเท่ากัน ({radius} cm) A เคลื่อนที่เร็ว {speed} m/s เข้าชน B ที่อยู่นิ่ง ศูนย์กลาง B เยื้องจากแนวการเคลื่อนที่ของศูนย์กลาง A ในแนวตั้งฉากเป็น {number(offset)} cm การชนยืดหยุ่น หลังชน B มีอัตราเร็วกี่ m/s",
            r"\sin\alpha=\frac b{2R},\quad v_B=u\cos\alpha",
            [str(speed), tex(speed * sine), tex(speed * (1 - sine * sine))],
        )


LENS_PAIRS = ((10, 10), (20, 30), (30, 60), (12, 24), (15, 10), (60, 30), (40, 10), (20, 20))


@question_type(
    "phys.posn2565_q10",
    display_name={"th": "รัศมีความโค้งกระจกเว้าที่ภาพตรงวัตถุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ระบบเลนส์และกระจก",
)
class RetroMirror(PhysicsSheet):
    def expr(self, rng):
        distance, focal = rng.choice(LENS_PAIRS)
        gap = 5 * rng.randint(2, 12)
        image = Fraction(distance * focal, distance + focal)
        answer = agree(q10.solve(object_distance=distance, focal=focal, gap=gap), gap + image)
        return draw(
            10,
            tex(answer),
            f"วัตถุอยู่หน้าเลนส์เว้าบางความยาวโฟกัส {focal} cm (ค่า f เป็นลบ) ห่างเลนส์ {distance} cm หลังเลนส์มีกระจกเว้าห่างจากเลนส์ {gap} cm บนแกนเดียวกัน แสงจากวัตถุผ่านเลนส์ สะท้อนกระจก แล้วผ่านเลนส์กลับมาเกิดภาพที่ตำแหน่งวัตถุพอดี รัศมีความโค้งของกระจกเว้าเป็นกี่ cm",
            r"R=D+\frac{u|f|}{u+|f|}",
            [str(gap + distance), tex(Fraction(gap + distance, 2)), tex((gap + image) / 2)],
        )


@question_type(
    "phys.posn2565_q11",
    display_name={"th": "สนามแม่เหล็กจากครึ่งวงกลมสองรัศมี"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎบีโอต์ซาวาร์ตสำหรับลวดโค้ง",
)
class HalfLoopPair(PhysicsSheet):
    def expr(self, rng):
        inner, outer = sorted(rng.sample((1, 2, 4, 5, 10, 20, 25), 2))
        total, gap = Fraction(100, inner) + Fraction(100, outer), Fraction(100, inner) - Fraction(100, outer)
        answer = agree(q11.solve(inner=inner, outer=outer), total / 4)
        return draw(
            11,
            tex(answer),
            f"ลวดประกอบด้วยครึ่งวงกลมรัศมี {inner} cm และครึ่งวงกลมรัศมี {outer} cm ซึ่งมีศูนย์กลางร่วมกันที่ O ต่อถึงกันด้วยสายตรงแนวรัศมี กระแส I วนรอบ O ทางเดียวกันในทั้งสองครึ่งวงกลม และสายนำเข้าออกอยู่ในแนวรัศมี สนามแม่เหล็กที่ O มีขนาดเป็นกี่เท่าของ μ₀I ในหน่วย m⁻¹",
            r"B_{half}=\frac{\mu_0I}{4R}",
            [tex(total / 2), tex(gap / 4), tex(gap / 2)],
        )


@question_type(
    "phys.posn2565_q12",
    display_name={"th": "เวลาไถลตามคอร์ดถึงจุดต่ำสุด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่บนพื้นเอียงลื่น",
)
class ChordTime(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(1, 30)
        squared = Fraction(2 * radius, 5)  # (2 sqrt(R/g))^2 with g = 10
        cos = rng.choice((Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13), Fraction(1, 2)))
        agree(q12.solve(radius=radius, cosine=float(cos)) ** 2, squared)
        return draw(
            12,
            radical(squared),
            f"จุด A และ C เป็นจุดสูงสุดและต่ำสุดของวงกลมรัศมี {radius} m ในระนาบดิ่ง B เป็นอีกจุดบนวงกลม รางลื่นตรง BC ทำมุม θ กับแนวดิ่ง โดย cos θ = {number(cos)} ปล่อยมวลจากหยุดนิ่งที่ B ให้ไถลถึง C ใช้เวลากี่ s ให้ g=10 m/s²",
            r"BC=2R\cos\theta,\quad a=g\cos\theta",
            [radical(squared * cos * cos), radical(squared / cos**2), radical(squared * cos)],
        )


PROCESSES = {
    "solid_warming": "ของแข็งมีอุณหภูมิสูงขึ้นก่อนหลอมเหลว",
    "melting": "การเปลี่ยนสถานะจากของแข็งเป็นของเหลว",
    "liquid_warming": "ของเหลวมีอุณหภูมิสูงขึ้น",
    "boiling": "การเปลี่ยนสถานะจากของเหลวเป็นแก๊ส",
    "vapour_warming": "แก๊สมีอุณหภูมิสูงขึ้นหลังเดือดหมดแล้ว",
}
# The other segments, most diagnostic first, and the process each one is.
CONFUSIONS = {
    "solid_warming": ("melting", "liquid_warming", "vapour_warming"),
    "melting": ("boiling", "liquid_warming", "solid_warming"),
    "liquid_warming": ("solid_warming", "vapour_warming", "melting"),
    "boiling": ("melting", "vapour_warming", "liquid_warming"),
    "vapour_warming": ("liquid_warming", "boiling", "solid_warming"),
}


@question_type(
    "phys.posn2565_q13",
    display_name={"th": "ช่วงการเปลี่ยนสถานะบนกราฟการให้ความร้อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเปลี่ยนสถานะและกราฟอุณหภูมิ",
)
class HeatingCurve(PhysicsSheet):
    def expr(self, rng):
        process = rng.choice(sorted(PROCESSES))
        segment = lambda name: rf"\mathrm{{{q13.solve(process=name)}}}"
        return MathDraw(
            "",
            segment(process),
            prompt=(
                "สารชนิดหนึ่งได้รับความร้อนในอัตราคงที่ภายใต้ความดันคงที่ กราฟอุณหภูมิกับเวลาเป็นดังนี้: "
                "A→B อุณหภูมิเพิ่ม, B→C อุณหภูมิคงที่, C→D อุณหภูมิเพิ่ม, D→E อุณหภูมิคงที่ที่ค่าสูงกว่าช่วง B→C, E→F อุณหภูมิเพิ่ม "
                f"ช่วงใดแสดง{PROCESSES[process]}"
            ),
            hint=r"\text{flat: phase change; rising: one phase warming}",
            distractors=[named(f"phys.heating_curve_picked_{other}", segment(other)) for other in CONFUSIONS[process]],
        )


@question_type(
    "phys.posn2565_q14",
    display_name={"th": "อัตราส่วนปริมาตรไอน้ำต่อน้ำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎแก๊สอุดมคติกับการเปลี่ยนสถานะ",
)
class SteamVolume(PhysicsSheet):
    def expr(self, rng):
        celsius = 10 * rng.randint(10, 20)
        kelvin = celsius + 273
        agree(q14.solve(celsius=celsius), Fraction(kelvin, 18) * Fraction(8314, 1000) / Fraction(101325) * 10**6)
        form = lambda t, scale: rf"\left(\frac{{{t}}}{{18}}\right)\left(\frac RP\right)" + scale
        million = r"\times10^{6}"
        return draw(
            14,
            form(kelvin, million),
            f"น้ำ 1 g (ปริมาตร 1 cm³) กลายเป็นไอน้ำทั้งหมดที่อุณหภูมิ {celsius} °C และความดัน P ถือว่าไอน้ำเป็นแก๊สอุดมคติ (มวลโมเลกุล 18 g/mol) ปริมาตรไอน้ำเป็นประมาณกี่เท่าของปริมาตรน้ำ 1 g เมื่อ R ในหน่วย J K⁻¹ mol⁻¹ และ P ในหน่วย N m⁻²",
            r"PV=nRT,\quad n=\tfrac1{18}",
            [form(kelvin, ""), form(celsius, million), form(273, million)],
        )


@question_type(
    "phys.posn2565_q15",
    display_name={"th": "แรงสปริงในระบบสองมวลสั่นสมมาตร"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎของฮุกกับระบบสองมวล",
)
class SpringPair(PhysicsSheet):
    def expr(self, rng):
        k = 10 * rng.randint(2, 20)
        x = rng.randint(1, 10)
        exact = Fraction(2 * k * x, 100)
        answer = agree(q15.solve(k=k, x=x), exact)
        return draw(
            15,
            tex(answer),
            f"มวล A และ B ต่อที่ปลายสปริงเบาค่าคงตัว {k} N/m บนพื้นลื่น ทั้งสองสั่นอย่างสมมาตรรอบจุดกึ่งกลาง O ขณะหนึ่งแต่ละมวลอยู่ห่างจากตำแหน่งที่สปริงยาวตามธรรมชาติออกไปข้างละ {x} cm แรงที่สปริงกระทำต่อ B มีขนาดกี่ N",
            r"\Delta l=2x,\quad F=k\Delta l",
            [tex(exact / 2), tex(exact / 4), tex(exact * 2)],
        )


SLIDE_STATIC = (Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5), Fraction(7, 24))


@question_type(
    "phys.posn2565_q16",
    display_name={"th": "ความเร่งบนพื้นเอียงที่มุมเริ่มไถล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเสียดทานสถิตและจลน์บนพื้นเอียง",
)
class TiltSlide(PhysicsSheet):
    def expr(self, rng):
        static = rng.choice(SLIDE_STATIC)
        kinetic = static * rng.choice((Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)))
        norm = Fraction(isqrt((static.numerator**2 + static.denominator**2)), static.denominator)
        assert norm * norm == 1 + static * static
        exact = 10 * (static - kinetic) / norm
        answer = agree(q16.solve(static=float(static), kinetic=float(kinetic)), exact)
        return draw(
            16,
            tex(answer),
            f"ก้อนมวล m วางบนพื้นเอียงที่มีสัมประสิทธิ์ความเสียดทานสถิต {number(static)} และจลน์ {number(kinetic)} ค่อยๆ ยกพื้นเอียงให้ชันขึ้นจนก้อนเริ่มไถล แล้วคงมุมนั้นไว้ ก้อนไถลลงด้วยความเร่งกี่ m/s² ให้ g=10 m/s²",
            r"\tan\theta=\mu_s,\quad a=g(\sin\theta-\mu_k\cos\theta)",
            [tex(10 * (static - kinetic)), tex(10 * (static + kinetic) / norm), tex(10 * (1 - kinetic * static) / norm)],
        )


@question_type(
    "phys.posn2565_q17",
    display_name={"th": "ความจุตัวเก็บประจุทรงกระบอกช่องแคบ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความจุไฟฟ้าของตัวเก็บประจุ",
)
class ThinCoaxial(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(2, 10)
        length = 10 * rng.randint(1, 5)
        gap = rng.choice((1, 2, 5))
        r, span, d = Fraction(radius, 100), Fraction(length, 100), Fraction(gap, 1000)
        exact = 2 * r * span / d
        agree(q17.solve(radius=radius, length=length, gap=gap), float(exact) * pi)
        return draw(
            17,
            times_pi(exact),
            f"ตัวเก็บประจุทรงกระบอกซ้อนกันยาว {length} cm ทรงกระบอกในรัศมี {radius} cm และช่องว่างอากาศระหว่างทรงกระบอกกว้าง {gap} mm (แคบมากเทียบกับรัศมี) ความจุไฟฟ้าเป็นกี่เท่าของ ε₀ ในหน่วย m (ประมาณเป็นตัวเก็บประจุแผ่นขนาน C = ε₀A/d)",
            r"A=2\pi rl,\quad C=\frac{\epsilon_0A}d",
            [times_pi(r * r / d), tex(r * span / d), times_pi((r + d) ** 2 / span)],
        )


@question_type(
    "phys.posn2565_q18",
    display_name={"th": "มุมกดสูงสุดที่ยังลากวัตถุได้"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเสียดทานกับแรงกดเฉียง",
)
class PushLimit(PhysicsSheet):
    def expr(self, rng):
        mu = rng.choice((Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 3), Fraction(3, 4), Fraction(2, 5)))
        answer = agree(q18.solve(mu=float(mu)), 1 / mu)
        return draw(
            18,
            tex(answer),
            f"ก้อนมวล M วางบนพื้นระดับที่มีสัมประสิทธิ์ความเสียดทาน {number(mu)} ออกแรง F ดันก้อนไปทางขวาโดยแนวแรงชี้ลงทำมุม θ ใต้แนวระดับ ถ้า F มีขนาดเท่าใดก็ได้ tan θ ต้องไม่เกินค่าเท่าใดจึงจะลากก้อนไปทางขวาได้",
            r"F\cos\theta>\mu(Mg+F\sin\theta)",
            [tex(mu), tex(1 / mu**2), tex(1 - mu)],
        )


@question_type(
    "phys.posn2565_q19",
    display_name={"th": "ความเร่งลูกลอยเมื่อเชือกขาด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงลอยตัวและกฎข้อสองของนิวตัน",
)
class TetheredRelease(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 6)
        volume = mass * rng.randint(2, 5) + rng.choice((0, 1))
        ratio = Fraction(volume, mass)
        exact = (ratio - 1) * 10
        answer = agree(q19.solve(mass=mass, volume=volume), exact)
        return draw(
            19,
            tex(answer),
            f"ลูกบอลเบามวล {mass} g ปริมาตร {volume} cm³ ถูกผูกด้วยเชือกเบาไว้กับก้นถังน้ำ (น้ำหนาแน่น 1 g/cm³) ลูกบอลจมอยู่ทั้งลูก ถ้าเชือกขาดทันที ลูกบอลเริ่มเคลื่อนขึ้นด้วยความเร่งกี่ m/s² ไม่คิดแรงต้านของน้ำและมวลน้ำที่เคลื่อนตาม ให้ g=10 m/s²",
            r"ma=\rho Vg-mg",
            [tex(ratio * 10), tex((ratio + 1) * 10), tex((1 / ratio - 1) * 10)],
        )


WIRES = ((3, 4), (4, 3), (5, 12), (12, 5), (8, 15), (6, 8))


@question_type(
    "phys.posn2565_q20",
    display_name={"th": "สนามแม่เหล็กจากลวดตรงสองเส้นตั้งฉาก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สนามแม่เหล็กจากลวดตรงยาว",
)
class PerpendicularWires(PhysicsSheet):
    def expr(self, rng):
        along_x, along_y = rng.choice(WIRES)
        height = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(2)))
        hyp = isqrt(along_x**2 + along_y**2)
        unit = Fraction(1, 5) / height
        answer = agree(q20.solve(along_x=along_x, along_y=along_y, height=float(height)), unit * hyp)
        return draw(
            20,
            tex(answer),
            f"ลวดตรงยาวมากสองเส้นวางตามแกน OX และแกน OY ซึ่งตั้งฉากกันที่ O มีกระแส {along_x} A ตามทิศ +X และ {along_y} A ตามทิศ +Y ตามลำดับ สนามแม่เหล็กที่จุด (0, 0, {number(height)} m) มีขนาดกี่ μT ให้ μ₀=4π×10⁻⁷ T m/A",
            r"B=\frac{\mu_0I}{2\pi z}\text{ each, perpendicular}",
            [tex(unit * (along_x + along_y)), tex(unit * along_x), tex(unit * abs(along_x - along_y))],
        )


@question_type(
    "phys.posn2565_q21",
    display_name={"th": "การอนุรักษ์โมเมนตัมเชิงมุมของดาวเคราะห์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="โมเมนตัมเชิงมุมในวงโคจร",
)
class OrbitalAngularMomentum(PhysicsSheet):
    def expr(self, rng):
        while True:
            sine, other_sine = rng.sample(SINES[:4], 2)
            distance, other = rng.sample((1, 2, 3, 4, 5), 2)
            speed = 10 * rng.randint(1, 6)
            exact = speed * distance * sine / (other * other_sine)
            if exact.denominator <= 100:
                break
        answer = agree(
            q21.solve(speed=speed, distance=distance, sine=float(sine), other_distance=other, other_sine=float(other_sine)),
            exact,
        )
        cos, other_cos = cosine(sine), cosine(other_sine)
        return draw(
            21,
            tex(answer),
            f"ดาวเคราะห์โคจรรอบดวงอาทิตย์ (M ≫ m) ที่ตำแหน่งหนึ่งห่างดวงอาทิตย์ {distance} AU มีอัตราเร็ว {speed} km/s โดยความเร็วทำมุม θ₁ กับแนวรัศมีซึ่ง sin θ₁ = {number(sine)} อีกตำแหน่งหนึ่งห่าง {other} AU ความเร็วทำมุม θ₂ กับแนวรัศมีซึ่ง sin θ₂ = {number(other_sine)} อัตราเร็วที่ตำแหน่งหลังเป็นกี่ km/s",
            r"mvr\sin\theta=\text{const}",
            [
                tex(Fraction(speed * distance, other)),
                tex(speed * distance * cos / (other * other_cos)),
                tex(speed * other * other_sine / (distance * sine)),
            ],
        )


@question_type(
    "phys.posn2565_q22",
    display_name={"th": "อัตราส่วนความจุความร้อน γ ของแก๊สผสม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความจุความร้อนของแก๊สอุดมคติ",
)
class MixtureGamma(PhysicsSheet):
    def expr(self, rng):
        mono, di = rng.randint(1, 4), rng.randint(1, 4)
        answer = q22.solve(monatomic=mono, diatomic=di)
        averaged = (mono * Fraction(5, 3) + di * Fraction(7, 5)) / (mono + di)
        return draw(
            22,
            tex(answer),
            f"แก๊สอุดมคติผสมประกอบด้วยแก๊สอะตอมเดี่ยว {mono} mol และแก๊สไดอะตอมิก {di} mol ที่อุณหภูมิไม่สูงมาก (ไม่คิดการสั่นของโมเลกุล) ในกระบวนการแอเดียแบติก PV^γ คงที่ γ ของแก๊สผสมมีค่าเท่าใด",
            r"\gamma=\frac{C_P}{C_V},\quad C_P=C_V+nR",
            [tex(Fraction(7, 5)), tex(Fraction(5, 3)), tex(averaged)],
        )


@question_type(
    "phys.posn2565_q23",
    display_name={"th": "สนามไฟฟ้าจากสนามแม่เหล็กในคลื่นแม่เหล็กไฟฟ้า"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานของคลื่นแม่เหล็กไฟฟ้า",
)
class WaveFieldRatio(PhysicsSheet):
    def expr(self, rng):
        micro = rng.randint(1, 50)
        field = Fraction(micro, 10**6)
        light = 3 * 10**8
        answer = agree(q23.solve(field_nt=micro * 1000), field * light)
        return draw(
            23,
            sci(answer, force=True),
            f"คลื่นแม่เหล็กไฟฟ้าในสุญญากาศมีขนาดสนามแม่เหล็ก {micro} μT ณ จุดหนึ่ง ความหนาแน่นพลังงานในสนามไฟฟ้าเท่ากับในสนามแม่เหล็ก ขนาดสนามไฟฟ้า ณ จุดนั้นเป็นกี่ V/m ให้ c=3×10⁸ m/s",
            r"\tfrac12\epsilon_0E^2=\frac{B^2}{2\mu_0}",
            [sci(field / light, force=True), sci(field * light**2, force=True), sci(field / light**2, force=True)],
        )


@question_type(
    "phys.posn2565_q24",
    display_name={"th": "สนามไฟฟ้าในลวดที่มีกระแส"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎของโอห์มรูปความหนาแน่นกระแส",
)
class WireField(PhysicsSheet):
    def expr(self, rng):
        current = rng.randint(1, 10)
        sigma = rng.choice((1, 2, 5, 6)) * 10**7
        area = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2), Fraction(5, 2)))
        a = area / 10**6
        exact = current / (sigma * a)
        answer = agree(q24.solve(current=current, conductivity=sigma, area=float(area)), exact)
        return draw(
            24,
            sci(answer),
            f"ลวดพื้นที่หน้าตัด {number(area)} mm² สภาพนำไฟฟ้า {sigma // 10**7}×10⁷ S/m มีกระแส {current} A ไหลผ่าน สนามไฟฟ้าในเนื้อลวดมีขนาดกี่ V/m",
            r"J=\frac Ia=\sigma E",
            [sci(a * current / sigma), sci(sigma * a / current), sci(sigma / (a * current))],
        )


@question_type(
    "phys.posn2565_q25",
    display_name={"th": "แรงจากลำน้ำที่ถูกเบนกลับ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การดลจากการไหลของของไหล",
)
class ReversedJet(PhysicsSheet):
    def expr(self, rng):
        area = rng.randint(1, 10)
        speed = rng.randint(2, 10)
        exact = Fraction(2 * 1000 * area * speed * speed, 10**4)
        answer = agree(q25.solve(area=area, speed=speed), exact)
        return draw(
            25,
            tex(answer),
            f"ลำน้ำ (ความหนาแน่น 1000 kg/m³) พุ่งเข้าท่อรูปตัว U พื้นที่หน้าตัด {area} cm² ด้วยอัตราเร็ว {speed} m/s แล้วถูกเบนกลับออกมาในทิศตรงข้ามด้วยอัตราเร็วเท่าเดิม ท่อยึดกับกำแพง แรงที่ท่อดันกำแพงมีขนาดกี่ N",
            r"F=\dot m\,\Delta v=\rho Av\cdot2v",
            [tex(exact / 2), tex(exact / 4), tex(exact / speed)],
        )


@question_type(
    "phys.posn2565_q26",
    display_name={"th": "แรงจากการขยายตัวที่ถูกจำกัด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความเค้นจากความร้อน",
)
class ThermalStress(PhysicsSheet):
    def expr(self, rng):
        modulus = rng.choice((70, 110, 200))
        area = rng.randint(1, 5)
        alpha = rng.choice((12, 17, 23))
        rise = 10 * rng.randint(2, 10)
        exact = Fraction(modulus * area * alpha * rise, 10)
        answer = agree(q26.solve(modulus=modulus, area=area, alpha=alpha, rise=rise), exact)
        return draw(
            26,
            sci(answer),
            f"ท่อนโลหะตรงพื้นที่หน้าตัด {area} cm² วางพอดีระหว่างกำแพงแข็งสองข้าง มอดุลัสของยัง {modulus} GPa สัมประสิทธิ์การขยายตัวเชิงเส้น {alpha}×10⁻⁶ K⁻¹ เมื่ออุณหภูมิของท่อนเพิ่มขึ้น {rise} K กำแพงต้องออกแรงดันท่อนกี่ N เพื่อไม่ให้ท่อนยืด",
            r"F=YA\alpha\Delta T",
            [sci(exact * 10**4 / area), sci(exact / 2), sci(exact * 10**6 / alpha)],
        )


@question_type(
    "phys.posn2565_q27",
    display_name={"th": "มุมเล็งชดเชยการตกของโพรเจกไทล์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การประมาณอันดับแรกของโพรเจกไทล์",
)
class AimCorrection(PhysicsSheet):
    def expr(self, rng):
        distance = rng.choice((10, 20, 50, 100))
        speed = rng.choice((100, 200, 250, 500))
        exact = Fraction(10 * distance, 2 * speed * speed)
        answer = q27.solve(distance=distance, speed=speed)
        agree(answer, exact)
        return draw(
            27,
            tex(exact),
            f"ยิงโพรเจกไทล์ด้วยอัตราเร็ว {speed} m/s ไปยังเป้า B บนกำแพงดิ่งที่อยู่ห่าง {distance} m และสูงระดับเดียวกับจุดยิง ต้องเล็งสูงกว่าแนวตรงไปยัง B เป็นมุมประมาณกี่ rad ให้ g=10 m/s² (ใช้การประมาณมุมเล็ก)",
            r"t\approx\frac D{v_0},\quad\delta\theta\approx\frac{gt^2/2}D",
            [tex(exact * 2), tex(exact * distance), tex(exact / 2)],
        )


@question_type(
    "phys.posn2565_q28",
    display_name={"th": "อัตราเร็วเรือจากเวลาเสียงสะท้อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="เสียงสะท้อนจากผู้สังเกตที่เคลื่อนที่",
)
class EchoBoat(PhysicsSheet):
    def expr(self, rng):
        sound = 340
        while True:
            drop = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2)))
            tau = rng.randint(5, 20)
            speed = sound * drop / (2 * tau - drop)
            if speed < sound / 5:
                break
        second = rng.randint(4, 10)
        first = second + drop
        answer = agree(q28.solve(t1=float(first), t2=second, tau=tau, sound=sound), speed)
        return draw(
            28,
            tex(answer),
            f"เรือแล่นเข้าหาหน้าผาด้วยความเร็วคงที่ ที่ตำแหน่งแรกเรือเปิดหวูดสั้นๆ คนบนเรือได้ยินเสียงสะท้อนหลังเปิดหวูด {number(first)} s อีก {tau} s ต่อมาเรือเปิดหวูดอีกครั้งและได้ยินเสียงสะท้อนหลังเปิดหวูด {second} s อัตราเร็วเสียงในอากาศนิ่ง {sound} m/s เรือแล่นเร็วกี่ m/s",
            r"(c+u)t=2L,\quad L_2=L_1-u\tau",
            [
                tex(sound * drop / (2 * tau)),
                tex(sound * drop / (2 * tau + drop)),
                tex(sound * drop / tau),
            ],
        )


@question_type(
    "phys.posn2565_q29",
    display_name={"th": "อัตราเร็วต่ำสุดที่ลูกธนูผ่านซี่ล้อ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่สัมพัทธ์กับการหมุน",
)
class SpokeGap(PhysicsSheet):
    def expr(self, rng):
        spokes = rng.choice((3, 4, 6, 8))
        omega = rng.randint(2, 12)
        length = rng.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)))
        top = Fraction(spokes * omega) * length / 2
        agree(q29.solve(spokes=spokes, omega=omega, length=float(length)), float(top) / pi)
        return draw(
            29,
            over_pi(top),
            f"ล้อจักรยานมีซี่ลวดบางๆ {spokes} ซี่ทำมุมเท่ากัน หมุนด้วยอัตราเร็วเชิงมุม {omega} rad/s ลูกธนูยาว {number(length)} m พุ่งตั้งฉากกับระนาบล้อผ่านช่องระหว่างซี่ ลูกธนูต้องมีอัตราเร็วอย่างน้อยกี่ m/s จึงมีโอกาสผ่านไปได้โดยไม่ถูกซี่กระทบ",
            r"t_{gap}=\frac{2\pi}{n\omega},\quad v\ge\frac l{t_{gap}}",
            [over_pi(2 * top), tex(omega * length), over_pi(Fraction(omega) * length / 2)],
        )


CONE_COSINES = (Fraction(16, 25), Fraction(9, 25), Fraction(144, 169), Fraction(25, 169), Fraction(1, 4), Fraction(9, 16), Fraction(64, 289))


@question_type(
    "phys.posn2565_q30",
    display_name={"th": "อัตราส่วนคาบลูกตุ้มกรวยต่อลูกตุ้มอย่างง่าย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แบบวงกลมของลูกตุ้มกรวย",
)
class ConeSimpleRatio(PhysicsSheet):
    def expr(self, rng):
        cos = rng.choice(CONE_COSINES)
        root = Fraction(isqrt(cos.numerator), isqrt(cos.denominator))
        answer = agree(q30.solve(cosine=float(cos)), root)
        return draw(
            30,
            tex(answer),
            f"มวล m แขวนด้วยเชือกยาว l เคลื่อนที่เป็นวงกลมในระนาบระดับโดยเชือกทำมุม θ คงที่กับแนวดิ่ง (cos θ = {number(cos)}) คาบของการเคลื่อนที่นี้เป็นกี่เท่าของคาบการแกว่งมุมเล็กของลูกตุ้มอย่างง่ายที่ใช้เชือกยาว l เท่ากัน",
            r"T_{cone}=2\pi\sqrt{\frac{l\cos\theta}g}",
            [tex(cos), tex(1 / root), tex(1 / cos)],
        )
