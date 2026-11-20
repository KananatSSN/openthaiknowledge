"""Seeded variants of the reviewed POSN physics 2567 camp selection paper."""

from fractions import Fraction
from math import isqrt, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2567_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2567_physics import q11, q12, q13, q14, q15, q16

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


def pair(first, second):
    return rf"\left({first},\ {second}\right)"


def three_figures(value):
    """A positive float to three significant figures, as plain text."""
    digits = 3 - len(str(int(value))) if value >= 1 else 3
    return f"{round(value, max(digits, 0)):.{max(digits, 0)}f}"


SINES = (Fraction(3, 5), Fraction(4, 5), Fraction(5, 13), Fraction(12, 13))

SLIPS = {
    1: ("phys.chord_time_as_radius_fall", "phys.chord_ratio_not_rooted", "phys.chord_ratio_halved_depth"),
    2: ("phys.incline_angle_to_horizontal", "phys.incline_range_halved", "phys.incline_range_doubled"),
    3: ("phys.collision_order_swapped", "phys.collision_assumed_elastic", "phys.collision_assumed_sticking"),
    4: ("phys.rolling_friction_full_component", "phys.rolling_friction_as_ma", "phys.rolling_friction_inertia_only"),
    5: ("phys.loops_force_per_length", "phys.loops_force_sign", "phys.loops_force_halved"),
    6: ("phys.pair_field_no_projection", "phys.pair_field_origin_value", "phys.pair_field_single_charge"),
    7: ("phys.plates_all_gaps", "phys.plates_counted_positive", "phys.plates_series_gaps"),
    8: ("phys.rc_ratio_resistors_ignored", "phys.rc_ratio_capacitors_ignored", "phys.rc_ratio_resistors_swapped"),
    9: ("phys.loops_sense_ignored", "phys.loops_direction_reversed", "phys.loops_half_field"),
    10: ("phys.echo_closing_sign", "phys.echo_boat_motion_ignored", "phys.echo_round_trip_not_halved"),
    11: ("phys.harmonic_euler_omitted", "phys.harmonic_not_inverted", "phys.harmonic_log10_used"),
    12: ("phys.raindrop_half_turn", "phys.raindrop_incidence_once", "phys.raindrop_supplement"),
    13: ("phys.bubble_one_surface", "phys.bubble_tension_over_radius", "phys.bubble_doubled"),
    14: ("phys.lens_index_sign", "phys.lens_index_over_mu", "phys.lens_index_multiplied"),
    15: ("phys.radiating_slab_no_drop", "phys.radiating_slab_conduction_full", "phys.radiating_slab_halved"),
    16: ("phys.ladder_node_off_by_one", "phys.ladder_rest_ignored", "phys.ladder_ratio_complement"),
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
    sheet_id = "posn2567_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2567)"


def _type(n, title, topic):
    return question_type(
        f"phys.posn2567_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


@_type(1, "เวลาไถลตามคอร์ดเทียบการตกอิสระ", "การเคลื่อนที่บนพื้นเอียงลื่น")
class ChordVersusFall(PhysicsSheet):
    def expr(self, rng):
        depth = rng.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(1, 8)))
        squared = 2 / depth
        agree(q01.solve(depth=float(depth)) ** 2, squared)
        return draw(
            1,
            radical(squared),
            f"A เป็นจุดสูงสุดของวงกลมรัศมี R ในระนาบดิ่ง B เป็นจุดหนึ่งบนวงกลม รางตรงลื่น AB ปล่อยมวลจากหยุดนิ่งที่ A ให้ไถลถึง B เวลาที่ใช้เป็นกี่เท่าของเวลาตกอิสระจากหยุดนิ่งเป็นระยะ {number(depth)}R",
            r"t_{AB}=2\sqrt{R/g},\quad t_{fall}=\sqrt{2h/g}",
            [radical(1 / depth), tex(squared), radical(1 / (2 * depth))],
        )


@_type(2, "ระยะและมุมกระทบของโพรเจกไทล์บนพื้นเอียง", "การเคลื่อนที่แบบโพรเจกไทล์บนพื้นเอียง")
class InclineProjectile(PhysicsSheet):
    def expr(self, rng):
        speed = 5 * rng.randint(1, 8)
        distance, angle = q02.solve(speed=speed)
        exact = Fraction(speed * speed, 5)
        agree(distance, exact)
        assert angle == 30
        return draw(
            2,
            pair(tex(exact), "30^\\circ"),
            f"ยิงโพรเจกไทล์จากจุด O ด้วยอัตราเร็ว {speed} m/s ทำมุม 30° เหนือแนวระดับ ลงบนพื้นเอียง OA ที่ลาดลงทำมุม 30° ใต้แนวระดับ ตกกระทบพื้นเอียงที่จุด P ให้ g=10 m/s² คู่ค่า (OP, φ) เป็นเท่าใด โดย OP มีหน่วย m และ φ เป็นมุมระหว่างแนวความเร็วที่ P กับพื้นเอียง",
            r"x=u\cos30^\circ t,\quad y=u\sin30^\circ t-\tfrac12gt^2=-x\tan30^\circ",
            [pair(tex(exact), "60^\\circ"), pair(tex(exact / 2), "30^\\circ"), pair(tex(exact * 2), "30^\\circ")],
        )


@_type(3, "ความเร็วหลังชนเมื่อพลังงานจลน์ลดลง", "การชนกับการสูญเสียพลังงาน")
class EnergyFractionCollision(PhysicsSheet):
    def expr(self, rng):
        spread = rng.choice((Fraction(1, 5), Fraction(1, 3), Fraction(1, 2), Fraction(3, 5)))
        speed = 2 * spread.denominator * rng.randint(1, 3)
        fraction = (1 + spread * spread) / 2
        slow, fast = speed * (1 - spread) / 2, speed * (1 + spread) / 2
        got = q03.solve(speed=speed, fraction=float(fraction))
        agree(got[0], slow)
        agree(got[1], fast)
        return draw(
            3,
            pair(tex(slow), tex(fast)),
            f"A และ B มีมวลเท่ากัน A เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s เข้าชน B ที่อยู่นิ่งในหนึ่งมิติ หลังชนพลังงานจลน์ของระบบเหลือ {number(fraction)} ของก่อนชน และทั้งสองเคลื่อนที่ไปในทิศเดิม (A ไม่แซง B) คู่ความเร็ว (v_A, v_B) หลังชนเป็นกี่ m/s",
            r"v_A+v_B=u,\quad v_A^2+v_B^2=fu^2",
            [pair(tex(fast), tex(slow)), pair("0", str(speed)), pair(tex(Fraction(speed, 2)), tex(Fraction(speed, 2)))],
        )


ROLLERS = {
    Fraction(1, 2): "ทรงกระบอกตัน",
    Fraction(2, 5): "ทรงกลมตัน",
    Fraction(1): "วงแหวนบาง",
    Fraction(2, 3): "ทรงกลมกลวงบาง",
}


@_type(4, "แรงเสียดทานบนล้อที่กลิ้งลงพื้นเอียง", "การกลิ้งโดยไม่ไถล")
class RollingFriction(PhysicsSheet):
    def expr(self, rng):
        factor = rng.choice(sorted(ROLLERS))
        sine = rng.choice(SINES)
        mass = rng.randint(1, 12)
        component = 10 * mass * sine
        exact = component * factor / (factor + 1)
        answer = agree(q04.solve(mass=mass, inertia_factor=float(factor), sine=float(sine)), exact)
        return draw(
            4,
            tex(answer),
            f"{ROLLERS[factor]}มวล {mass} kg (โมเมนต์ความเฉื่อยรอบศูนย์กลาง {number(factor)}MR²) กลิ้งโดยไม่ไถลลงพื้นเอียงที่ทำมุม θ กับแนวระดับ โดย sin θ = {number(sine)} แรงเสียดทานที่พื้นเอียงกระทำต่อวัตถุมีขนาดกี่ N ให้ g=10 m/s²",
            r"Mg\sin\theta-f=Ma,\quad fR=I\frac aR",
            [tex(component), tex(component / (factor + 1)), tex(component * factor)],
        )


@_type(5, "แรงระหว่างวงลวดร่วมแกนที่อยู่ใกล้กัน", "แรงแม่เหล็กระหว่างกระแส")
class CloseLoopsForce(PhysicsSheet):
    def expr(self, rng):
        current = rng.randint(1, 20)
        radius = rng.choice((5, 10, 20, 25))
        gap = rng.choice((1, 2, 4, 5))
        same = rng.random() < 0.5
        magnitude = Fraction(4, 10**7) * current**2 * Fraction(radius, 100) / Fraction(gap, 1000)
        exact = magnitude if same else -magnitude
        agree(q05.solve(current=current, radius=radius, gap=gap, same=same), float(exact) * pi)
        sense = "ไหลวนทางเดียวกัน" if same else "ไหลวนสวนทางกัน"
        per_length = Fraction(2, 10**7) * current**2 / Fraction(gap, 1000)
        return draw(
            5,
            pi_sci(exact),
            f"วงลวดวงกลมสองวงรัศมี {radius} cm วางร่วมแกนห่างกัน {gap} mm (น้อยมากเทียบกับรัศมี) แต่ละวงมีกระแส {current} A {sense} ใช้แรงต่อความยาวระหว่างลวดตรงยาว μ₀I²/(2πd) ประมาณแรงระหว่างวงลวดในหน่วย N โดยตอบเป็นบวกถ้าดูดกันและลบถ้าผลักกัน ให้ μ₀=4π×10⁻⁷ T m/A",
            r"F\approx\frac{\mu_0I^2}{2\pi d}\cdot2\pi R",
            [sci(per_length if same else -per_length, force=True), pi_sci(-exact), pi_sci(exact / 2)],
        )


HALVES = (Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(1, 2), Fraction(1))


@_type(6, "สนามไฟฟ้าสูงสุดบนแกนของประจุคู่", "การรวมสนามไฟฟ้าแบบเวกเตอร์")
class PairAxisField(PhysicsSheet):
    def expr(self, rng):
        charge = rng.randint(1, 9)
        half = rng.choice(HALVES)
        squared = Fraction(48 * charge * charge) / half**4
        agree(q06.solve(charge=charge, half=float(half)) ** 2, squared)
        return draw(
            6,
            radical(squared),
            f"ประจุ +{charge} nC สองประจุอยู่ที่ (0, +{number(half)} m) และ (0, −{number(half)} m) สนามไฟฟ้าบนแกน X มีขนาดมากที่สุดกี่ V/m ให้ k=9×10⁹ N m²/C² และฟังก์ชัน ξ/(1+ξ²)^(3/2) มีค่าสูงสุด 2/(3√3)",
            r"E(x)=\frac{2kqx}{(x^2+a^2)^{3/2}}",
            [tex(Fraction(18 * charge) / half**2), "0", radical(squared / 4)],
        )


@_type(7, "ความจุของตัวเก็บประจุหลายแผ่น", "ตัวเก็บประจุแผ่นขนานหลายแผ่น")
class MultiPlate(PhysicsSheet):
    def expr(self, rng):
        while True:
            count = rng.randint(3, 6)
            pattern = "".join(rng.choice("+-") for _ in range(count))
            if "+" in pattern and "-" in pattern:
                break
        answer = q07.solve(pattern=pattern)
        listing = ", ".join(f"แผ่นที่ {k + 1} ขั้ว{'บวก' if s == '+' else 'ลบ'}" for k, s in enumerate(pattern))
        return draw(
            7,
            str(answer),
            f"แผ่นโลหะขนาน {count} แผ่น พื้นที่ A วางซ้อนห่างกันแผ่นละ d (d ≪ √A) ต่อกับแบตเตอรี่ V ดังนี้: {listing} ประจุที่แบตเตอรี่จ่ายออกไปทั้งหมดเป็นกี่เท่าของ ε₀AV/d",
            r"Q=\varepsilon_0\frac Ad\,V\times(\text{gaps across }V)",
            [str(count - 1), str(pattern.count("+")), tex(Fraction(1, count - 1))],
        )


@_type(8, "อัตราส่วนประจุของตัวเก็บประจุคร่อมตัวต้านทาน", "วงจรตัวเก็บประจุในสถานะคงตัว")
class SteadyRcRatio(PhysicsSheet):
    def expr(self, rng):
        r1, r2 = rng.sample(range(1, 10), 2)
        c1, c2 = rng.sample(range(1, 10), 2)
        exact = Fraction(c1 * r1, c2 * r2)
        answer = agree(q08.solve(r1=r1, c1=c1, r2=r2, c2=c2), exact)
        return draw(
            8,
            tex(answer),
            f"แบตเตอรี่ต่ออนุกรมกับตัวต้านทาน R₁ = {r1} Ω และ R₂ = {r2} Ω ตัวเก็บประจุ C₁ = {c1} μF ต่อคร่อม R₁ และ C₂ = {c2} μF ต่อคร่อม R₂ เมื่อกระแสคงตัวแล้ว อัตราส่วนประจุใน C₁ ต่อใน C₂ เป็นเท่าใด",
            r"Q_k=C_kV_k=C_kIR_k",
            [tex(Fraction(c1, c2)), tex(Fraction(r1, r2)), tex(Fraction(c1 * r2, c2 * r1))],
        )


@_type(9, "สนามแม่เหล็กจากวงลวดสองวงร่วมศูนย์", "กฎบีโอต์ซาวาร์ตสำหรับลวดโค้ง")
class ConcentricLoops(PhysicsSheet):
    def expr(self, rng):
        inner, outer = sorted(rng.sample((1, 2, 4, 5, 10, 20, 25), 2))
        opposed = rng.random() < 0.6
        a, b = Fraction(50, inner), Fraction(50, outer)
        exact = a - b if opposed else a + b
        answer = agree(q09.solve(inner=inner, outer=outer, opposed=opposed), exact)
        other = a + b if opposed else a - b
        sense = "ตามเข็มนาฬิกา" if opposed else "ทวนเข็มนาฬิกา"
        return draw(
            9,
            tex(answer),
            f"ลวดในระนาบกระดาษเป็นวงกลมรัศมี {inner} cm และ {outer} cm ศูนย์กลางร่วมที่ O ต่อกันด้วยสายแนวรัศมี กระแส I วนรอบวงในทวนเข็มนาฬิกาหนึ่งรอบ แล้ววนรอบวงนอก{sense}หนึ่งรอบ สายนำเข้าออกอยู่ในแนวรัศมี สนามแม่เหล็กที่ O เป็นกี่เท่าของ μ₀I ในหน่วย m⁻¹ (บวกเมื่อชี้ออกจากกระดาษ)",
            r"B=\frac{\mu_0I}{2R}\text{ per loop}",
            [tex(other), tex(-exact), tex(exact / 2)],
        )


@_type(10, "เวลาที่เรือชนหน้าผาจากเสียงสะท้อน", "เสียงสะท้อนจากผู้สังเกตที่เคลื่อนที่")
class EchoCliffTime(PhysicsSheet):
    def expr(self, rng):
        speed = rng.choice((5, 10, 20, 40))
        echo = rng.randint(2, 12)
        sound = 340
        exact = Fraction((sound + speed) * echo, 2 * speed)
        answer = agree(q10.solve(speed=speed, echo=echo, sound=sound), exact)
        return draw(
            10,
            tex(answer),
            f"เรือแล่นด้วยความเร็วคงที่ {speed} m/s ตรงเข้าหาหน้าผา ที่จุด A เรือเปิดหวูดสั้นๆ และคนบนเรือได้ยินเสียงสะท้อนหลังเปิดหวูด {echo} s อัตราเร็วเสียง {sound} m/s เรือจะชนหน้าผาหลังเปิดหวูดกี่ s",
            r"(c+v)t=2L,\quad t_{hit}=\frac Lv",
            [
                tex(Fraction((sound - speed) * echo, 2 * speed)),
                tex(Fraction(sound * echo, 2 * speed)),
                tex(Fraction((sound + speed) * echo, speed)),
            ],
        )


@_type(11, "ความต้านทานขนานจากอนุกรมฮาร์มอนิก", "ตัวต้านทานขนานและการประมาณผลรวม")
class HarmonicParallel(PhysicsSheet):
    def expr(self, rng):
        power = rng.randint(2, 6)
        answer = q11.solve(power=power)
        return draw(
            11,
            three_figures(answer),
            f"ตัวต้านทาน 10^{power} ตัวมีค่า 1, 2, 3, ..., 10^{power} kΩ นำมาต่อขนานกันทั้งหมด ความต้านทานลัพธ์เป็นประมาณกี่ Ω (ตอบเลขนัยสำคัญสามตัว) ใช้ 1 + 1/2 + ... + 1/n − ln n ≈ 0.577 และ ln 10 ≈ 2.303",
            r"\frac1R=\sum_{k=1}^{N}\frac1{k\,\mathrm{k}\Omega}\approx\frac{\ln N+0.577}{\mathrm{k}\Omega}",
            [
                three_figures(1000 / (power * 2.303)),
                three_figures(1000 * (power * 2.303 + 0.577)),
                three_figures(1000 / (power + 0.577)),
            ],
        )


@_type(12, "มุมระหว่างแสงเข้าและแสงออกจากหยดน้ำ", "การหักเหและการสะท้อนในหยดน้ำ")
class RaindropAngle(PhysicsSheet):
    def expr(self, rng):
        incidence = rng.randint(30, 80)
        refraction = rng.randint(incidence // 2 + 1, incidence - 1)
        answer = q12.solve(incidence=incidence, refraction=refraction)
        return draw(
            12,
            f"{answer}^\\circ",
            f"แสงตกกระทบหยดน้ำทรงกลมด้วยมุมตกกระทบ {incidence}° หักเหเข้าไปเป็นมุม {refraction}° สะท้อนภายในหนึ่งครั้งแล้วหักเหออก แนวแสงออกทำมุมกับแนวแสงเข้ากี่องศา",
            r"\phi=4\theta-2i",
            [f"{2 * refraction - incidence}^\\circ", f"{4 * refraction - incidence}^\\circ", f"{180 - answer}^\\circ"],
        )


@_type(13, "ผลต่างความดันในฟองสบู่", "ความตึงผิว")
class SoapBubble(PhysicsSheet):
    def expr(self, rng):
        tension = 5 * rng.randint(4, 16)  # mN/m
        radius = rng.randint(1, 10)  # cm
        exact = Fraction(4 * tension, 10 * radius)
        answer = agree(q13.solve(tension=tension / 1000, radius=radius), exact)
        return draw(
            13,
            tex(answer),
            f"ฟองสบู่รัศมี {radius} cm น้ำสบู่มีความตึงผิว {tension}×10⁻³ N/m ความดันภายในฟองสบู่สูงกว่าความดันภายนอกกี่ Pa",
            r"\Delta P\cdot\pi R^2=2\cdot2\pi R\gamma",
            [tex(exact / 2), tex(exact / 4), tex(exact * 2)],
        )


@_type(14, "การเปลี่ยนโฟกัสเมื่อดรรชนีหักเหเปลี่ยน", "สูตรผู้สร้างเลนส์")
class LensIndexChange(PhysicsSheet):
    def expr(self, rng):
        index = rng.choice((Fraction(3, 2), Fraction(8, 5), Fraction(5, 4), Fraction(7, 5), Fraction(2)))
        change = Fraction(rng.randint(1, 9), 100)
        exact = -change / (index - 1)
        answer = agree(q14.solve(index=float(index), change=float(change)), exact)
        return draw(
            14,
            tex(answer),
            f"เลนส์บางทำด้วยแก้วดรรชนีหักเห {number(index)} มี 1/f = (μ − 1)(1/R₁ + 1/R₂) ถ้าดรรชนีหักเหเพิ่มขึ้นเล็กน้อย {number(change)} โดยรัศมีความโค้งเท่าเดิม δf/f มีค่าประมาณเท่าใด",
            r"f\propto\frac1{\mu-1}",
            [tex(-exact), tex(-change / index), tex(-change * (index - 1))],
        )


@_type(15, "อุณหภูมิผิวแผ่นที่นำและแผ่รังสีความร้อน", "การนำความร้อนกับการแผ่รังสี")
class ConductionRadiation(PhysicsSheet):
    def expr(self, rng):
        hot = 100 * rng.randint(4, 15)
        ratio = rng.choice((2, 5, 10, 20, 50))  # K / l
        answer = round(q15.solve(hot=hot, conductivity=ratio / 10, thickness=0.1))
        conduction_only = round((ratio * hot / 5.7e-8) ** 0.25)
        return draw(
            15,
            str(answer),
            f"แผ่นกันความร้อนมี K/l = {ratio} W/(m² K) ด้านหนึ่งติดแหล่งความร้อนอุณหภูมิ {hot} K อีกด้านเป็นผิวดำแผ่รังสีสู่ความว่างเปล่า (σ = 5.7×10⁻⁸ W m⁻² K⁻⁴) ในสภาวะคงตัว อุณหภูมิผิวดำ T₂ เป็นประมาณกี่ K (ปัดเป็นจำนวนเต็ม)",
            r"\frac Kl(T_1-T_2)=\sigma T_2^4",
            [str(hot), str(conduction_only), str(hot // 2)],
        )


LADDERS = ((4, 2, 2), (6, 1, 2), (2, 1, 1), (6, 3, 3), (10, 5, 5), (12, 1, 3), (12, 6, 6))


@_type(16, "ศักย์ที่ปลายวงจรขั้นบันไดตัวเก็บประจุ", "วงจรตัวเก็บประจุและสมการกำลังสอง")
class CapacitorLadder(PhysicsSheet):
    def expr(self, rng):
        series, shunt, tail = rng.choice(LADDERS)
        node = rng.randint(2, 5)
        emf = rng.choice((16, 32, 64, 81, 100, 243))
        ratio = Fraction(series, series + shunt + tail)
        exact = emf * ratio**node
        agree(q16.solve(series=series, shunt=shunt, node=node) * emf, exact)
        return draw(
            16,
            tex(exact),
            f"แหล่งกำเนิด {emf} V (ขั้วลบต่อดิน) ต่อกับวงจรขั้นบันได: ตัวเก็บประจุอนุกรม {series} μF ต่อเรียงกัน {node} ตัวไปยังจุด 1 ถึง {node} ที่จุด 1 ถึง {node - 1} มีตัวเก็บประจุ {shunt} μF ต่อลงดิน และที่จุด {node} มีตัวเก็บประจุ {shunt + tail} μF ต่อลงดิน เริ่มต้นไม่มีประจุ ศักย์ไฟฟ้าที่จุด {node} เป็นกี่ V",
            r"C=\frac{\sqrt{C_2^2+4C_1C_2}-C_2}{2},\quad\frac{V_{k+1}}{V_k}=\frac{C_1}{C_1+C_2+C}",
            [
                tex(emf * ratio ** (node - 1)),
                tex(emf * Fraction(series, series + shunt) ** node),
                tex(emf * (1 - ratio) ** node),
            ],
        )
