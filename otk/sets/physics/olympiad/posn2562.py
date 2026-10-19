"""Seeded variants of the reviewed POSN physics 2562 camp selection paper."""

from fractions import Fraction
from math import isqrt, atan, degrees, cos, radians, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import show
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2562_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09

from otk.sheets.posn2562_physics import q10, q11, q12, q13, q14, q15, q16, q17, q18

from otk.sheets.posn2562_physics import q19, q20, q21, q22, q23, q24, q25, q26

LEVEL = {"th": "โอลิมปิก (สอวน.)"}
SLIPS = {}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def radical(value):
    """Exact reduced radical for a nonnegative rational squared answer."""
    value = value if isinstance(value, Fraction) else Fraction(value).limit_denominator(1000000)
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


def draw(number, answer, prompt, hint, slips, expression=""):
    return MathDraw(
        expression,
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number], slips)],
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2562_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2562)"


SLIPS.update(
    {
        1: (
            "phys.resistivity_length_sign",
            "phys.resistivity_as_conductivity",
            "phys.resistivity_as_conductance",
        ),
        2: (
            "phys.lens_deflection_inverted",
            "phys.lens_deflection_square_root",
            "phys.lens_deflection_squared",
        ),
        3: (
            "phys.siphon_pressure_inverted",
            "phys.siphon_gravity_multiplied",
            "phys.siphon_density_omitted",
        ),
        4: (
            "phys.tank_surface_speed_ignored",
            "phys.tank_bernoulli_sign",
            "phys.tank_area_not_squared",
        ),
        5: (
            "phys.em_speed_reciprocal",
            "phys.em_speed_no_square_root",
            "phys.em_permeability_ignored",
        ),
        6: (
            "phys.cone_speed_squared",
            "phys.cone_height_inverted",
            "phys.cone_normal_vertical_only",
        ),
        7: (
            "phys.conduction_drop_as_temperature",
            "phys.conduction_distance_from_cold",
            "phys.conduction_hot_fraction",
        ),
        8: (
            "phys.pendulum_expansion_doubled",
            "phys.pendulum_unity_omitted",
            "phys.pendulum_period_linear_length",
        ),
        9: (
            "phys.arc_potential_full_circle",
            "phys.arc_potential_half_charge",
            "phys.arc_potential_radius_left",
        ),
    }
)


@question_type(
    "phys.posn2562_q01",
    display_name={"th": "หน่วยของสภาพต้านทานและความยาว"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="หน่วยและมิติของสภาพต้านทาน",
)
class ResistivityUnits(PhysicsSheet):
    def expr(self, rng):
        n = rng.randint(0, 4)
        ohm, meter = q01.solve(n=n)
        fmt = lambda a, b: rf"\Omega^{{{a}}}\,\mathrm{{m}}^{{{b}}}"
        return draw(
            1,
            fmt(ohm, meter),
            "ลวดสม่ำเสมอมีความต้านทาน R ความยาว L และพื้นที่หน้าตัด A โดย R=ρL/A ให้ ρ เป็นสภาพต้านทานไฟฟ้า หน่วย SI ของปริมาณ X ในสมการเป็นข้อใด",
            r"[\rho]=[R][A]/[L]=\Omega\,\mathrm{m}",
            [fmt(1, -1 - n), fmt(-1, -1 - n), fmt(-1, 1 - n)],
            rf"X=\rho/L^{{{n}}}",
        )


@question_type(
    "phys.posn2562_q02",
    display_name={"th": "มุมเบี่ยงเบนผ่านเลนส์เว้า"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การหักเหพาราเซียลของเลนส์บาง",
)
class DivergingRayDeflection(PhysicsSheet):
    def expr(self, rng):
        h = rng.randint(1, 4)
        f = 100 * rng.randint(1, 5)
        answer = q02.solve(height=h, focal=f, object_distance=3 * f)
        return draw(
            2,
            tex(answer),
            f"รังสีจากวัตถุจริงผ่านเลนส์เว้าบาง fเลนส์=−{f} cm ที่ความสูง {h} cm เหนือแกนหลัก ในการประมาณพาราเซียล มุมทิศทางของรังสีหลังผ่านเลนส์เปลี่ยนจากก่อนผ่านเลนส์เป็นขนาดกี่เรเดียน (ใช้มุมเล็ก ไม่คิดความคลาด)",
            r"\Delta\theta=\left|h/f_{lens}\right|",
            [tex(1 / answer), radical(answer), tex(answer**2)],
        )


@question_type(
    "phys.posn2562_q03",
    display_name={"th": "ขอบเขตจำเป็นของความสูงกาลักน้ำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความดันและหัวความดันของของเหลว",
)
class SiphonNecessaryHeight(PhysicsSheet):
    def expr(self, rng):
        p = 10000 * rng.randint(8, 12)
        density = rng.choice((800, 1000, 1200))
        g = 10
        answer = q03.solve(atmosphere=p, density=density, g=g)
        return draw(
            3,
            tex(answer),
            f"กาลักน้ำดูดของเหลวความหนาแน่น {density} kg/m³ จากถังเปิด บรรยากาศ {p} Pa ยอดท่อสูง h จากผิวถัง ให้ g=10 m/s² จากเงื่อนไขความดันที่ยอดต้องเป็นบวก h ต้องน้อยกว่าขอบเขตจำเป็นค่าใดในหน่วย m โดยละหัวความเร็วและความดันไอในการหาขอบเขตนี้",
            r"P_{crest}=P_a-\rho gh-\tfrac12\rho v^2>0",
            [tex(1 / answer), tex(Fraction(p * g, density)), tex(Fraction(p, g))],
        )


@question_type(
    "phys.posn2562_q04",
    display_name={"th": "ความเร็วลำน้ำจากถังหน้าตัดจำกัด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แบร์นูลลีและสมการความต่อเนื่อง",
)
class FiniteTankJet(PhysicsSheet):
    def expr(self, rng):
        height = rng.randint(1, 10)
        ratio = Fraction(1, rng.randint(3, 8))
        answer = q04.solve(height=height, g=10, area_ratio=float(ratio))
        return draw(
            4,
            radical(answer**2),
            f"ถังเปิดหน้าตัด A มีรูที่ก้นให้ลำน้ำหน้าตัด a ผิวน้ำสูงเหนือรู {height} m ณ ขณะพิจารณา ให้ a/A={show(ratio)} ใช้การไหลอุดมคติแบบกึ่งคงตัว ผิวน้ำและลำน้ำมีความดันบรรยากาศ และ g=10 m/s² อัตราเร็วลำน้ำที่รูเป็นกี่ m/s โดยต้องคิดการลดระดับผิวน้ำด้วย",
            r"Av_s=av,\quad gh+v_s^2/2=v^2/2",
            [
                radical(20 * height),
                radical(Fraction(20 * height, 1 + ratio**2)),
                radical(Fraction(20 * height, 1 - ratio)),
            ],
        )


@question_type(
    "phys.posn2562_q05",
    display_name={"th": "อัตราส่วนสนามไฟฟ้าต่อสนามแม่เหล็ก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานของคลื่นแม่เหล็กไฟฟ้า",
)
class EMFieldRatio(PhysicsSheet):
    def expr(self, rng):
        er = rng.choice((2, 3, 4, 5, 9))
        mr = rng.choice((1, 2, 3, 4))
        answer = q05.solve(epsilon_r=er, mu_r=mr)
        return draw(
            5,
            radical(answer**2),
            f"คลื่นแม่เหล็กไฟฟ้าระนาบในตัวกลางอุดมคติไม่มีการสูญเสียมี ε={er}ε₀ และ μ={mr}μ₀ ความหนาแน่นพลังงานไฟฟ้าเท่ากับแม่เหล็ก อัตราส่วน E/B เป็นกี่เท่าของ c₀=1/√(ε₀μ₀) โดย E และ B เป็นขนาดสนาม",
            r"\tfrac12\epsilon E^2=B^2/(2\mu)",
            [radical(er * mr), tex(Fraction(1, er * mr)), radical(Fraction(1, er))],
        )


@question_type(
    "phys.posn2562_q06",
    display_name={"th": "อัตราเร็ววงกลมด้านในกรวยลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเข้าสู่ศูนย์กลางบนผิวกรวย",
)
class SmoothConeSpeed(PhysicsSheet):
    def expr(self, rng):
        height = rng.randint(1, 12)
        beta = rng.choice((30, 45, 60))
        answer = q06.solve(height=height, g=10, beta=beta)
        return draw(
            6,
            radical(answer**2),
            f"อนุภาคเคลื่อนเป็นวงกลมแนวระดับบนผิวด้านในของกรวยลื่น แกนกรวยตั้งฉากกับพื้นและยอดกรวยอยู่บนพื้น วงโคจรสูงจากยอด {height} m มุมผิวกรวยกับแกนดิ่ง {beta}° อัตราเร็วเป็นกี่ m/s ให้ g=10 m/s²",
            r"N\sin\beta=mg,\quad N\cos\beta=mv^2/r,\quad r=h\tan\beta",
            [str(10 * height), radical(Fraction(10, height)), radical(20 * height)],
        )


@question_type(
    "phys.posn2562_q07",
    display_name={"th": "อุณหภูมิตามแท่งนำความร้อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การนำความร้อนคงตัวหนึ่งมิติ",
)
class SteadyRodTemperature(PhysicsSheet):
    def expr(self, rng):
        hot = 10 * rng.randint(8, 16)
        cold = 10 * rng.randint(1, 5)
        fraction = rng.choice((Fraction(1, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 4)))
        answer = q07.solve(hot=hot, cold=cold, fraction=float(fraction))
        return draw(
            7,
            tex(answer),
            f"แท่งโลหะสม่ำเสมอยาว L ผิวด้านข้างหุ้มฉนวน ปลาย A คงที่ {hot} °C ปลาย B คงที่ {cold} °C เมื่อการนำความร้อนอยู่ในสถานะคงตัวแล้ว ที่ระยะ {show(fraction)}L จาก A มีอุณหภูมิกี่ °C ไม่มีแหล่งความร้อนภายใน",
            r"T(x)=T_A-(T_A-T_B)x/L",
            [
                tex(fraction * (hot - cold)),
                tex(cold + fraction * (hot - cold)),
                tex(fraction * hot),
            ],
        )


@question_type(
    "phys.posn2562_q08",
    display_name={"th": "คาบลูกตุ้มเมื่อสายแขวนขยายตัว"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การขยายตัวและคาบลูกตุ้มอย่างง่าย",
)
class HeatedPendulumPeriod(PhysicsSheet):
    def expr(self, rng):
        alpha = Fraction(rng.randint(1, 5), 100000)
        dt = rng.choice((20, 40, 60, 80, 100))
        answer = q08.solve(alpha=float(alpha), delta_t=dt)
        x = alpha * dt
        return draw(
            8,
            radical(answer**2),
            f"ลูกตุ้มอย่างง่ายแกว่งมุมเล็ก สายแขวนมีสัมประสิทธิ์ขยายตัวเชิงเส้น {show(alpha)} K⁻¹ เมื่อเพิ่มอุณหภูมิ {dt} K คาบใหม่เป็นกี่เท่าของเดิม ให้ความยาวเป็นไปตามกฎขยายตัวเชิงเส้น ใช้ค่า g เดิมและไม่ตัดพจน์รากที่สองทิ้ง",
            r"P=2\pi\sqrt{\ell/g},\quad \ell'=\ell(1+\alpha\Delta T)",
            [radical(1 + 2 * x), radical(x), tex(1 + x)],
        )


@question_type(
    "phys.posn2562_q09",
    display_name={"th": "ศักย์ไฟฟ้าที่ศูนย์กลางส่วนโค้งมีประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ศักย์ไฟฟ้าของประจุกระจายตามเส้น",
)
class ChargedArcPotential(PhysicsSheet):
    def expr(self, rng):
        angle = rng.choice((60, 90, 120, 180, 240, 270))
        radius = rng.randint(1, 8)
        answer = q09.solve(angle=angle, radius=radius)
        return draw(
            9,
            tex(answer),
            f"ลวดฉนวนเป็นส่วนโค้งวงกลมรัศมี {radius} m รองรับมุม {angle}° ที่ศูนย์กลาง O มีประจุบวกกระจายสม่ำเสมอด้วยความหนาแน่นเชิงเส้น λ ค่าศักย์ที่ O เทียบอนันต์เป็นศูนย์ เป็นกี่เท่าของ λ/ε₀ ให้ k=1/(4πε₀)",
            r"V=kQ/R,\quad Q=\lambda R\phi",
            [tex(2 * answer), tex(answer / 2), tex(answer / radius)],
        )


SLIPS.update(
    {
        10: (
            "phys.virtual_magnification_no_unity",
            "phys.virtual_image_sign_wrong",
            "phys.near_point_substituted",
        ),
        11: (
            "phys.semicircle_fields_added",
            "phys.semicircle_full_loop",
            "phys.semicircle_outer_ignored",
        ),
        12: (
            "phys.rope_total_weight_one_side",
            "phys.rope_end_tension_as_bottom",
            "phys.rope_angle_from_horizontal",
        ),
        13: (
            "phys.opposed_batteries_added",
            "phys.middle_resistance_only",
            "phys.middle_current_outer_only",
        ),
        14: (
            "phys.capacitor_divider_wrong_resistor",
            "phys.capacitor_full_source_voltage",
            "phys.capacitor_current_continuity",
        ),
        15: (
            "phys.collision_used_one_radius",
            "phys.collision_tangent_instead_sine",
            "phys.collision_sine_as_tangent",
        ),
        16: (
            "phys.isobaric_heat_as_internal",
            "phys.monatomic_cp_as_seven_halves",
            "phys.isobaric_heat_as_work",
        ),
        17: (
            "phys.maximum_power_missing_four",
            "phys.maximum_power_emf_unsquared",
            "phys.maximum_power_missing_internal",
        ),
        18: (
            "phys.inductor_node_voltage_sign",
            "phys.inductor_voltage_equals_source",
            "phys.inductor_current_reset_zero",
        ),
    }
)


@question_type(
    "phys.posn2562_q10",
    display_name={"th": "กำลังขยายเลนส์นูนที่ให้ภาพเสมือน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมการเลนส์และกำลังขยายภาพเสมือน",
)
class VirtualLensMagnification(PhysicsSheet):
    def expr(self, rng):
        d = rng.randint(12, 30)
        f = rng.randint(4, 15)
        answer = q10.solve(distance=d, focal=f)
        return draw(
            10,
            tex(answer),
            f"เลนส์นูนบางความยาวโฟกัส {f} cm ให้วัตถุจริงเกิดภาพเสมือนหัวตั้งห่างจากเลนส์ {d} cm ทางด้านวัตถุ ขนาดกำลังขยายของเลนส์เป็นกี่เท่า",
            r"v=-d,\quad 1/f=1/u+1/v,\quad |M|=d/u",
            [tex(Fraction(d, f)), tex(Fraction(d, f) - 1), tex(1 + Fraction(25, f))],
        )


@question_type(
    "phys.posn2562_q11",
    display_name={"th": "สนามแม่เหล็กจากส่วนโค้งครึ่งวงกลมร่วมศูนย์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎบีโอต์ซาวาร์ตสำหรับลวดโค้ง",
)
class OpposedSemicircleField(PhysicsSheet):
    def expr(self, rng):
        inner = rng.randint(1, 5)
        outer = inner + rng.randint(1, 6)
        answer = q11.solve(inner=inner, outer=outer)
        return draw(
            11,
            tex(answer),
            f"ลวดเป็นส่วนโค้งครึ่งวงกลมร่วมศูนย์ O รัศมี {inner} m และ {outer} m เชื่อมปลายด้วยเส้นตรงตามแนวรัศมี มีกระแส I ไหลทวนเข็มบนโค้งนอกและตามเข็มบนโค้งใน ขนาดสนามแม่เหล็กที่ O เป็นกี่เท่าของ μ₀I ในหน่วย m⁻¹",
            r"B_{arc}=\mu_0 I\phi/(4\pi R),\quad B_{radial}=0",
            [
                tex(Fraction(1, 4 * inner) + Fraction(1, 4 * outer)),
                tex(2 * answer),
                tex(Fraction(1, 4 * inner)),
            ],
        )


@question_type(
    "phys.posn2562_q12",
    display_name={"th": "แรงตึงจุดต่ำสุดของเชือกห้อยท้องช้าง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลเชือกที่มีน้ำหนัก",
)
class LowestRopeTension(PhysicsSheet):
    def expr(self, rng):
        w = 20 * rng.randint(2, 15)
        tangent = rng.choice((Fraction(1, 2), Fraction(3, 4), Fraction(4, 3), 2))
        theta = degrees(atan(float(tangent)))
        answer = q12.solve(weight=w, theta=theta)
        return draw(
            12,
            tex(answer),
            f"เชือกอ่อนหนักรวม {w} N แขวนสมมาตรจากสองจุดระดับเดียวกัน ที่จุดแขวนแต่ละข้างแนวสัมผัสเชือกทำมุม θ กับแนวดิ่ง แรงตึงที่จุดต่ำสุดเป็นกี่ N ให้ค่ามุมตามสมการ",
            r"V_{support}=W/2,\quad T_{bottom}=H=V_{support}\tan\theta",
            [
                tex(w * tangent),
                radical(Fraction(w * w, 4) * (1 + tangent**2)),
                tex(Fraction(w, 2) / tangent),
            ],
            rf"\tan\theta={tex(tangent)}",
        )


@question_type(
    "phys.posn2562_q13",
    display_name={"th": "กระแสแขนงกลางของสองแหล่งจ่ายขั้วตรงข้าม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎเคอร์ชอฟฟ์และขั้วแหล่งจ่าย",
)
class OpposedSourceMiddleCurrent(PhysicsSheet):
    def expr(self, rng):
        left = rng.randint(6, 20)
        right = rng.randint(6, 20)
        outer = rng.randint(2, 9)
        middle = rng.randint(2, 9)
        answer = q13.solve(left_emf=left, right_emf=right, outer=outer, middle=middle)
        return draw(
            13,
            tex(answer),
            f"วงจรมีสามแขนงระหว่างจุดบนกับจุดล่าง แขนงกลางมี r={middle} Ω แขนงซ้ายมีตัวต้านทาน {outer} Ω อนุกรมแบตเตอรี่อุดมคติ {left} V ขั้วบวกอยู่ด้านบน แขนงขวามีตัวต้านทาน {outer} Ω อนุกรมแบตเตอรี่ {right} V ขั้วบวกอยู่ด้านล่าง กระแสผ่าน r เป็นกี่ A กำหนดทิศลงจากจุดบนเป็นบวก",
            r"(E_L-V)/R+(-E_R-V)/R=V/r",
            [
                tex(Fraction(left + right, outer + 2 * middle)),
                tex(Fraction(left - right, middle)),
                tex(Fraction(left - right, outer)),
            ],
        )


@question_type(
    "phys.posn2562_q14",
    display_name={"th": "กระแสเริ่มต้นหลังสลับตัวเก็บประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความต่อเนื่องแรงดันตัวเก็บประจุ",
)
class SwitchedCapacitorInitialCurrent(PhysicsSheet):
    def expr(self, rng):
        emf = 6 * rng.randint(2, 8)
        r1 = rng.randint(1, 8)
        r2 = rng.randint(1, 8)
        load = rng.randint(2, 12)
        cap = rng.randint(1, 9)
        answer = q14.solve(emf=emf, r1=r1, r2=r2, load=load, cap=cap)
        return draw(
            14,
            tex(answer),
            f"แบตเตอรี่อุดมคติ {emf} V ต่ออนุกรม R₁={r1} Ω กับ R₂={r2} Ω ตัวเก็บประจุ {cap} μF ต่อคร่อม R₂ จนเป็นสถานะคงตัว จากนั้นสวิตช์ตัดตัวเก็บประจุออกจากวงจรเดิมแล้วต่อเข้ากับ R={load} Ω เพียงตัวเดียว ทันทีหลังสับ กระแสคายประจุผ่าน R มีขนาดกี่ A",
            r"V_C(0^+)=V_C(0^-)=E R_2/(R_1+R_2),\quad I=V_C/R",
            [tex(Fraction(emf * r1, load * (r1 + r2))), tex(Fraction(emf, load)), "0"],
        )


@question_type(
    "phys.posn2562_q15",
    display_name={"th": "ทิศเหรียญหลังชนเยื้องศูนย์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงดลตามแนวศูนย์กลางของผิวเกลี้ยง",
)
class OffsetDiscCollision(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(1, 8)
        ratio = Fraction(rng.randint(1, 8), 10)
        offset = radius * ratio
        angle = q15.solve(offset=float(offset), radius=radius)
        assert 0 < angle < 30
        fmt = lambda kind, value: rf"\{kind}\!\left({tex(value)}\right)"
        return draw(
            15,
            fmt("arcsin", ratio / 2),
            f"เหรียญกลมเกลี้ยง A และ B รัศมีเท่ากัน {radius} cm A เคลื่อนแนวตรงชน B ซึ่งหยุดนิ่งก่อนชน ศูนย์กลาง B เยื้องจากเส้นทางศูนย์กลาง A ในแนวตั้งฉากเป็น {show(offset)} cm หลังชน B เคลื่อนทำมุม θ กับทิศเดิมของ A ตามข้อใด ไม่คิดแรงเสียดทาน",
            r"2R\sin\theta=a",
            [fmt("arcsin", ratio), fmt("arctan", ratio), fmt("arctan", ratio / 2)],
        )


@question_type(
    "phys.posn2562_q16",
    display_name={"th": "อุณหภูมิแก๊สอะตอมเดี่ยวที่รับความร้อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎข้อหนึ่งในกระบวนการความดันคงตัว",
)
class MonatomicIsobaricHeating(PhysicsSheet):
    def expr(self, rng):
        heat = 100 * rng.randint(1, 12)
        moles = rng.randint(1, 5)
        gas = Fraction(83, 10)
        answer = q16.solve(heat=heat, moles=moles, gas_constant=gas)
        return draw(
            16,
            tex(answer),
            f"แก๊สอุดมคติอะตอมเดี่ยว {moles} mol อยู่ในกระบอกกับลูกสูบเบาลื่น รับความร้อนช้า ๆ {heat} J และขยายตัวต้านความดันภายนอกคงที่ อุณหภูมิเพิ่มขึ้นกี่ K ให้ R=8.3 J/(mol K) และไม่มีงานชนิดอื่น",
            r"Q=\Delta U+P\Delta V=\tfrac32nR\Delta T+nR\Delta T",
            [
                tex(Fraction(2 * heat, 3 * moles * gas)),
                tex(Fraction(2 * heat, 7 * moles * gas)),
                tex(Fraction(heat, moles * gas)),
            ],
        )


@question_type(
    "phys.posn2562_q17",
    display_name={"th": "กำลังสูงสุดที่จ่ายให้ตัวต้านทานโหลด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="เงื่อนไขรากจริงและการถ่ายโอนกำลังสูงสุด",
)
class MaximumLoadPower(PhysicsSheet):
    def expr(self, rng):
        emf = rng.randint(6, 30)
        internal = rng.randint(2, 10)
        answer = q17.solve(emf=emf, internal=internal)
        return draw(
            17,
            tex(answer),
            f"แบตเตอรี่แรงเคลื่อนไฟฟ้า {emf} V มีความต้านทานภายใน r={internal} Ω ต่อโหลด x>0 Ω ให้กำลังบนโหลด β=i²x สมการของ x แสดงในบรรทัดคณิตศาสตร์ กำลัง β ที่มากที่สุดซึ่งเกิดได้จริงเป็นกี่ W",
            r"\Delta=(2r-E^2/\beta)^2-4r^2\ge0,\quad x>0",
            [
                tex(Fraction(emf * emf, internal)),
                tex(Fraction(emf, 4 * internal)),
                tex(Fraction(emf * emf, 4)),
            ],
            r"x^2+(2r-E^2/\beta)x+r^2=0",
        )


@question_type(
    "phys.posn2562_q18",
    display_name={"th": "ศักย์จุดต่อหลังตัดแหล่งจ่ายของตัวเหนี่ยวนำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความต่อเนื่องกระแสตัวเหนี่ยวนำและเครื่องหมายศักย์",
)
class InductorTopNodeVoltage(PhysicsSheet):
    def expr(self, rng):
        emf = rng.randint(6, 24)
        load = rng.randint(2, 12)
        r = rng.randint(2, 10)
        answer = q18.solve(emf=emf, resistor=load, internal=r)
        return draw(
            18,
            tex(answer),
            f"ก่อนสับสวิตช์ แบตเตอรี่ {emf} V จ่ายกระแสคงตัวลงผ่านตัวเหนี่ยวนำอุดมคติ L อนุกรม r={r} Ω สู่กราวด์ จากนั้นตัดแบตเตอรี่ออกแล้วต่อปลายบน A ของ L กับ R={load} Ω ที่มีอีกปลายต่อกราวด์ โดย r ยังอยู่ใต้ L ทันทีหลังสับ ศักย์ Vₐ เทียบกราวด์เป็นกี่ V",
            r"I_L(0^+)=E/r,\quad V_A/R+I_L=0",
            [tex(-answer), str(-emf), "0"],
        )


SLIPS.update(
    {
        19: (
            "phys.falling_rod_ignored_rotation",
            "phys.falling_rod_ignored_translation",
            "phys.falling_rod_half_available_energy",
        ),
        20: (
            "phys.minimum_pull_horizontal_only",
            "phys.minimum_pull_unnormalized_components",
            "phys.minimum_pull_mu_omitted",
        ),
        21: (
            "phys.capacitor_negative_quadratic_root",
            "phys.capacitor_quadratic_missing_half",
            "phys.capacitor_quadratic_missing_subtraction",
        ),
        22: (
            "phys.spool_sine_threshold",
            "phys.spool_tangent_threshold",
            "phys.spool_complement_radius",
        ),
        23: (
            "phys.rolling_point_speed_relative_center",
            "phys.rolling_point_wrong_angle_origin",
            "phys.rolling_point_full_angle_cosine",
        ),
        24: (
            "phys.pendulum_collision_quarter_period",
            "phys.pendulum_collision_full_period",
            "phys.pendulum_collision_mass_ratio",
        ),
        25: (
            "phys.ring_field_point_charge",
            "phys.ring_field_missing_projection",
            "phys.ring_field_half_ring",
        ),
        26: (
            "phys.symmetric_collision_one_target",
            "phys.symmetric_collision_no_rebound",
            "phys.symmetric_collision_mass_lumped",
        ),
    }
)


@question_type(
    "phys.posn2562_q19",
    display_name={"th": "อัตราเร็วศูนย์กลางแท่งที่ล้มบนพื้นลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานการเลื่อนที่ร่วมการหมุน",
)
class FallingRodCenterSpeed(PhysicsSheet):
    def expr(self, rng):
        half = rng.randint(1, 12)
        answer = q19.solve(half_length=half, g=10, initial_angle=0)
        return draw(
            19,
            radical(answer**2),
            f"แท่งบางสม่ำเสมอยาว {2 * half} m เริ่มจากหยุดนิ่งเกือบตั้งดิ่งโดยปลายล่างแตะพื้นราบลื่น แล้วล้มลง ปลายล่างเลื่อนได้ อัตราเร็วศูนย์กลางมวลก่อนแท่งราบแตะพื้นเป็นกี่ m/s ใช้ขีดจำกัดมุมเริ่มจากแนวดิ่งเข้าใกล้ศูนย์ ให้ g=10 m/s² และ Iศูนย์กลาง=mL²/12",
            r"mgl=\tfrac12mv_G^2+\tfrac12I_G\omega^2,\quad v_G=l\omega\ \text{at contact}",
            [radical(20 * half), radical(60 * half), radical(Fraction(15 * half, 2))],
        )


@question_type(
    "phys.posn2562_q20",
    display_name={"th": "แรงดึงน้อยสุดที่ทำให้ก้อนเริ่มเคลื่อน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเสียดทานสถิตและการหาค่าน้อยสุด",
)
class MinimumAngledPull(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(2, 15)
        mu = rng.choice((Fraction(3, 4), Fraction(4, 3), Fraction(5, 12), Fraction(12, 5)))
        answer = q20.solve(mass=mass, g=10, mu=float(mu))
        return draw(
            20,
            tex(answer),
            f"ก้อนมวล {mass} kg วางบนพื้นราบมีสัมประสิทธิ์เสียดทานสถิต {show(mu)} ดึงด้วยแรง F ที่ปรับมุมขึ้นจากแนวระดับได้ 0° ถึง 90° แรง F น้อยที่สุดที่ทำให้เริ่มเคลื่อนมีขนาดกี่ N ให้ g=10 m/s² และก้อนยังสัมผัสพื้น",
            r"F(\cos\theta+\mu_s\sin\theta)=\mu_s mg",
            [
                tex(10 * mass * mu),
                tex(10 * mass * mu / (1 + mu)),
                radical(Fraction(100 * mass * mass, 1 + mu**2)),
            ],
        )


@question_type(
    "phys.posn2562_q21",
    display_name={"th": "ความจุที่ทำให้ความจุรวมเท่ากับตัวมันเอง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="วงจรตัวเก็บประจุและสมการกำลังสอง",
)
class SelfEqualCapacitance(PhysicsSheet):
    def expr(self, rng):
        r = rng.randint(1, 9)
        k = rng.randint(1, 4)
        c = r * k
        c1 = r * k * (k + 1)
        c2 = r
        answer = q21.solve(c1=c1, c2=c2)
        return draw(
            21,
            tex(answer),
            f"ตัวเก็บประจุ C₁={c1} μF ต่ออนุกรมกับกลุ่มขนาน C₂={c2} μF และ C โดย C>0 ต้องเลือก C กี่ μF จึงทำให้ความจุสมมูลของวงจรสองขั้วนี้เท่ากับ C พอดี",
            r"C=C_1(C_2+C)/(C_1+C_2+C)",
            [tex(-c - c2), tex(2 * c), tex(c + c2)],
        )


@question_type(
    "phys.posn2562_q22",
    display_name={"th": "มุมวิกฤตของล้อม้วนเชือกที่กลิ้งเข้าหาผู้ดึง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง",
)
class SpoolPullCriticalAngle(PhysicsSheet):
    def expr(self, rng):
        inner = rng.randint(1, 5)
        outer = inner + rng.randint(1, 6)
        ratio = Fraction(inner, outer)
        critical = q22.solve(inner=inner, outer=outer)
        assert abs(cos(radians(critical)) - float(ratio)) < 1e-12
        fmt = lambda kind, x: rf"\{kind}\!\left({tex(x)}\right)"
        return draw(
            22,
            fmt("arccos", ratio),
            f"ล้อม้วนเชือกรัศมีนอก R₂={outer} cm มีเพลารัศมี R₁={inner} cm เชือกคลายจากด้านล่างของเพลาแล้วถูกดึงไปทางขวาเฉียงขึ้นมุม θ กับแนวระดับ ให้กลิ้งไม่ไถลและใช้สมการที่กำหนด มุม θ ต้องน้อยกว่าค่าใดจึงมีความเร่งไปทางขวา ให้ 0°≤θ≤90°",
            r"a=\frac{FR_2(R_2\cos\theta-R_1)}{I+MR_2^2}",
            [fmt("arcsin", ratio), fmt("arctan", ratio), fmt("arccos", 1 - ratio)],
            r"a=\Omega R_2,\quad Ma=F\cos\theta-f,\quad I\Omega=fR_2-FR_1",
        )


@question_type(
    "phys.posn2562_q23",
    display_name={"th": "อัตราเร็วจุดบนขอบล้อเทียบพื้น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความเร็วจากการเลื่อนที่ร่วมการหมุน",
)
class RollingRimPointSpeed(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(1, 8)
        omega = rng.randint(1, 9)
        theta = rng.choice((30, 60, 150))
        answer = q23.solve(radius=radius, omega=omega, theta=theta)
        assert abs(answer**2 - radius**2 * omega**2 * (2 + 2 * cos(radians(theta)))) < 1e-8
        fmt = lambda expression: rf"{radius * omega}\sqrt{{{expression}}}"
        return draw(
            23,
            fmt(rf"2+2\cos {theta}^\circ"),
            f"ล้อรัศมี {radius} m กลิ้งไปทางขวาบนพื้นโดยไม่ไถล มีอัตราเร็วเชิงมุม {omega} rad/s ตามเข็มนาฬิกา จุดบนขอบล้ออยู่ที่มุม θ={theta}° วัดตามเข็มจากรัศมีชี้ขึ้นในแนวดิ่ง อัตราเร็วของจุดนี้เทียบจุด O ที่ตรึงกับพื้นเป็นกี่ m/s",
            r"v_x=R\omega(1+\cos\theta),\quad v_y=-R\omega\sin\theta",
            [
                str(radius * omega),
                fmt(rf"2-2\cos {theta}^\circ"),
                rf"{2 * radius * omega}\left|\cos {theta}^\circ\right|",
            ],
        )


@question_type(
    "phys.posn2562_q24",
    display_name={"th": "ช่วงเวลาระหว่างการชนสองครั้งของลูกตุ้ม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การแกว่งความถี่เท่ากันและการชน",
)
class PendulumSecondCollision(PhysicsSheet):
    def expr(self, rng):
        length = rng.randint(1, 12)
        light = rng.randint(1, 4)
        heavy = light + rng.randint(1, 6)
        answer = q24.solve(length=length, g=10, light=light, heavy=heavy)
        assert abs(answer**2 - pi * pi * length / 10) < 1e-10
        fmt = lambda squared: rf"\pi\left({radical(squared)}\right)"
        return draw(
            24,
            fmt(Fraction(length, 10)),
            f"ลูกตุ้มอย่างง่ายสองลูกยาวเท่ากัน {length} m มวล {light} kg และ {heavy} kg แขวนแตะกันที่ตำแหน่งสมดุล ยกลูกเบาไปด้านซ้ายเล็กน้อยแล้วปล่อย ชนแบบยืดหยุ่นในหนึ่งมิติและไม่มีการชนติดกัน ใช้แบบจำลองมุมเล็กตลอดการแกว่ง ช่วงระหว่างเสียงชนครั้งแรกกับครั้งที่สองเป็นกี่ s ให้ g=10 m/s² ไม่คิดแรงต้าน",
            r"x_1,x_2\propto\sin(\omega t),\quad\omega=\sqrt{g/l}",
            [
                fmt(Fraction(length, 40)),
                fmt(Fraction(2 * length, 5)),
                fmt(Fraction(length * heavy, 10 * light)),
            ],
        )


@question_type(
    "phys.posn2562_q25",
    display_name={"th": "สนามไฟฟ้าบนแกนวงแหวนมีประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การอินทิเกรตสนามและสมมาตร",
)
class RingAxialElectricField(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(1, 6)
        distance = rng.randint(1, 8)
        answer = q25.solve(radius=radius, distance=distance)
        squared = Fraction(
            (radius * distance) ** 2, 4 * (radius * radius + distance * distance) ** 3
        )
        assert abs(answer**2 - float(squared)) < 1e-12
        correct = radical(squared)
        return draw(
            25,
            correct,
            f"วงแหวนฉนวนรัศมี {radius} m อยู่ในระนาบ YZ ศูนย์กลางที่ O มีประจุบวกสม่ำเสมอหนาแน่นเชิงเส้น λ สนามไฟฟ้าที่จุดบนแกน X ห่าง O ทางบวก {distance} m มีขนาดเป็นกี่เท่าของ λ/ε₀ ในหน่วย m⁻¹ ให้ k=1/(4πε₀)",
            r"dE_x=k\,dq\,x/(R^2+x^2)^{3/2},\quad Q=2\pi R\lambda",
            [
                tex(Fraction(radius, 2 * distance * distance)),
                tex(Fraction(radius, 2 * (radius * radius + distance * distance))),
                radical(squared / 4),
            ],
        )


@question_type(
    "phys.posn2562_q26",
    display_name={"th": "ความเร็วหลังชนเหรียญสามเหรียญสมมาตร"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การชนยืดหยุ่นพร้อมกันหลายจุดสัมผัส",
)
class SymmetricThreeDiscCollision(PhysicsSheet):
    def expr(self, rng):
        speed = 5 * rng.randint(1, 10)
        rebound, target = q26.solve(speed=speed)
        pair = lambda first, second: rf"\left({first},\ {second}\right)"
        answer = pair(tex(rebound), radical(target**2))
        prompt = f"เหรียญกลมเกลี้ยง A,B,C รัศมีและมวลเท่ากันอยู่บนโต๊ะลื่น B กับ C หยุดนิ่งแตะกัน A วิ่งด้วย {speed} m/s ตามแนวแบ่งครึ่งตั้งฉากของเส้นศูนย์กลาง B–C จนชนทั้งสองพร้อมกันอย่างสมมาตรและยืดหยุ่น หลังชน B,C แยกไปตามแนวศูนย์กลางที่ทำมุม ±30° กับทิศเดิมของ A "
        prompt += "อัตราเร็วคู่ (v,w) เป็นเท่าใดในหน่วย m/s โดย v คืออัตราเร็วที่ A กระดอนกลับ และ w คืออัตราเร็วของ B ซึ่งเท่ากับ C"
        slips = [
            pair("0", tex(speed)),
            pair("0", radical(Fraction(speed * speed, 2))),
            pair(tex(Fraction(speed, 3)), tex(Fraction(2 * speed, 3))),
        ]
        return draw(26, answer, prompt, r"u=-v+2w\cos30^\circ,\quad u^2=v^2+2w^2", slips)
