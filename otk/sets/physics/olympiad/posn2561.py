"""POSN physics camp selection 2561: verified variants of each source item."""

from fractions import Fraction
from math import isqrt, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import show
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2561_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2561_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2561_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29, q30

LEVEL = {"th": "โอลิมปิก (สอวน.)"}

SLIPS = {
    1: ("phys.time_dimension_wrong", "phys.area_dimension_ignored", "phys.dimensions_multiplied"),
    2: (
        "phys.ignored_counterweight_weight",
        "phys.ignored_counterweight",
        "phys.ignored_small_mass",
    ),
    3: ("phys.ignored_launch_delay", "phys.wrong_crossing_time", "phys.used_launch_instant"),
    4: (
        "phys.total_force_as_tension",
        "phys.end_force_difference",
        "phys.assumed_equal_block_masses",
    ),
    5: ("phys.used_table_edge_distance", "phys.ignored_big_mass", "phys.ignored_small_mass"),
    6: (
        "phys.speed_ratio_as_energy",
        "phys.other_particle_velocity",
        "phys.inverted_mass_ratio_energy",
    ),
    7: (
        "phys.friction_assists_motion",
        "phys.ignored_friction_work",
        "phys.used_full_weight_on_incline",
    ),
    8: (
        "phys.ignored_projectile_gravity",
        "phys.half_balloon_acceleration",
        "phys.gravity_sign_wrong",
    ),
    9: ("phys.period_not_squared", "phys.ignored_pendulum_length", "fraction.inverted"),
    10: (
        "phys.subtracted_force_squares",
        "phys.assumed_equal_vertical_hinges",
        "phys.upper_vertical_as_lower",
    ),
}


def tex(value):
    return frac_tex(Fraction(value).limit_denominator(1000000))


def radical(value):
    """Exact reduced radical for a nonnegative rational squared answer."""
    value = Fraction(value).limit_denominator(1000000)
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
    sheet_id = "posn2561_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2561)"


@question_type(
    "phys.posn2561_q01",
    display_name={"th": "มิติของค่าคงที่ในสมการพลังงานกับความถี่"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การวิเคราะห์มิติ",
)
class EnergyFrequencyDimensions(PhysicsSheet):
    def expr(self, rng):
        power = rng.randint(1, 5)
        mass, length, time = q01.solve(power=power)
        fmt = lambda m, le, t: rf"M^{{{m}}}L^{{{le}}}T^{{{t}}}"
        return draw(
            1,
            fmt(mass, length, time),
            "แบบจำลองให้พลังงาน E ขึ้นกับความถี่ f ตามสมการ มิติของ k เป็นเท่าใด "
            "(M แทนมวล L แทนความยาว T แทนเวลา)",
            r"[E]=ML^2T^{-2},\quad [f]=T^{-1}",
            [fmt(1, 2, -2 - power), fmt(1, 0, time), fmt(1, -2, -time)],
            rf"E=kf^{{{power}}}",
        )


@question_type(
    "phys.posn2561_q02",
    display_name={"th": "อัตราเร็วของลิงกับตุ้มถ่วงผ่านรอก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานของระบบรอกสองมวล",
)
class MonkeyCounterweight(PhysicsSheet):
    def expr(self, rng):
        light, ratio = rng.randint(2, 12), rng.choice((2, 3, 5))
        heavy, speed = light * ratio, rng.choice((4, 6, 8, 10))
        height = Fraction(speed**2 * (heavy + light), 20 * (heavy - light))
        v = q02.solve(heavy=heavy, light=light, height=float(height), g=10)
        return draw(
            2,
            tex(v),
            f"เชือกเบาคล้องผ่านรอกเบาลื่น ปลายหนึ่งมีลิงมวล {heavy} kg อีกปลายมีตุ้มมวล {light} kg "
            f"ลิงจับปลายเชือกโดยไม่ไถล เริ่มจากหยุดนิ่งและลงมา {show(height)} m "
            "ลิงมีอัตราเร็วเท่าใดในหน่วย m/s (g = 10 m/s² ตุ้มไม่ติดสิ่งกีดขวาง)",
            r"(M-m)gh=\frac12(M+m)v^2",
            [
                radical(Fraction(20 * heavy, heavy + light) * height),
                radical(20 * height),
                radical(Fraction(20 * (heavy - light), heavy) * height),
            ],
        )


@question_type(
    "phys.posn2561_q03",
    display_name={"th": "ความสูงที่ลูกบอลซึ่งโยนห่างเวลากันสวนทาง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แนวดิ่งของวัตถุที่ปล่อยต่างเวลา",
)
class SuccessiveThrows(PhysicsSheet):
    def expr(self, rng):
        speed, delay = rng.choice((10, 15, 20, 25)), rng.choice((Fraction(1, 2), 1, Fraction(3, 2)))
        height = q03.solve(speed=speed, delay=float(delay), g=10)
        return draw(
            3,
            tex(height),
            f"โยนลูกบอลสามลูกขึ้นในแนวดิ่งจากจุดเดียวกันด้วยอัตราเร็วต้น {speed} m/s "
            f"เว้นช่วงการโยนลูกถัดไป {show(delay)} s ลูกที่สองกับลูกที่สามสวนทางที่ความสูงเท่าใด "
            "เหนือจุดโยนในหน่วย m (g = 10 m/s² ไม่คิดแรงต้าน)",
            r"y_2(t+\Delta t)=y_3(t),\quad y(t)=ut-\frac12gt^2",
            [
                tex(Fraction(speed**2, 20)),
                tex(Fraction(speed**2, 20) - 5 * delay**2),
                tex(speed * delay - 5 * delay**2),
            ],
        )


@question_type(
    "phys.posn2561_q04",
    display_name={"th": "ตาชั่งสปริงระหว่างก้อนที่ถูกผลักไปทิศเดียวกัน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงตึงระหว่างวัตถุที่เร่งร่วมกัน",
)
class SpringScaleBetweenBlocks(PhysicsSheet):
    def expr(self, rng):
        ml, mr, acceleration = rng.randint(5, 9), rng.randint(1, 4), rng.randint(3, 7)
        tension = rng.randint(1, ml * acceleration - 1)
        fl, fr = ml * acceleration - tension, mr * acceleration + tension
        answer = q04.solve(left_mass=ml, right_mass=mr, left_force=fl, right_force=fr)
        return draw(
            4,
            tex(answer),
            f"ก้อนซ้ายมวล {ml} kg และก้อนขวามวล {mr} kg อยู่บนพื้นลื่น "
            f"เชื่อมกันด้วยเชือกและตาชั่งสปริงเบา ออกแรง {fl} N ที่ก้อนซ้ายไปทางขวา "
            f"และ {fr} N ที่ก้อนขวาไปทางขวา ตาชั่งอ่านค่าเท่าใดในหน่วย N",
            r"a=(F_L+F_R)/(m_L+m_R),\quad T=m_La-F_L",
            [str(fl + fr), str(abs(fr - fl)), tex(Fraction(fr - fl, 2))],
        )


@question_type(
    "phys.posn2561_q05",
    display_name={"th": "อัตราเร็วสูงสุดก่อนมวลแขวนถึงพื้น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="รอกที่หยุดเร่งเมื่อมวลแขวนถึงพื้น",
)
class HangingMassHitsFloor(PhysicsSheet):
    def expr(self, rng):
        mt, mh, height = rng.randint(5, 10), rng.randint(1, 4), rng.randint(1, 4)
        distance = height + rng.randint(1, 3)
        speed = q05.solve(
            table_mass=mt, hanging_mass=mh, height=height, edge_distance=distance, g=10
        )
        return draw(
            5,
            radical(speed**2),
            f"มวล {mt} kg บนโต๊ะลื่นห่างขอบ {distance} m ผูกกับมวลแขวน {mh} kg "
            f"ด้วยเชือกเบาผ่านรอกเบาลื่น มวลแขวนสูงจากพื้น {height} m "
            "ปล่อยระบบจากหยุดนิ่ง เมื่อมวลแขวนถึงพื้นเชือกหย่อน มวลบนโต๊ะมีอัตราเร็วสูงสุด "
            "ขณะยังอยู่บนผิวโต๊ะเท่าใดในหน่วย m/s (g = 10 m/s²)",
            r"m_hgh=\frac12(m_t+m_h)v^2",
            [
                radical(Fraction(20 * mh * distance, mt + mh)),
                radical(20 * height),
                radical(Fraction(20 * mh * height, mt)),
            ],
        )


@question_type(
    "phys.posn2561_q06",
    display_name={"th": "พลังงานที่นิวตรอนเหลือหลังชนยืดหยุ่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สัดส่วนพลังงานในการชนยืดหยุ่นหนึ่งมิติ",
)
class NeutronElasticEnergy(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.randint(2, 9)
        energy = q06.solve(ratio=ratio)
        return draw(
            6,
            tex(energy),
            f"อนุภาคมวล m พุ่งชนตรงแบบยืดหยุ่นกับอนุภาคที่อยู่นิ่งมวล {ratio}m "
            "ภายหลังชน อนุภาคแรกมีพลังงานจลน์เป็นกี่เท่าของก่อนชน (การชนหนึ่งมิติ)",
            r"v_1/u_1=(m_1-m_2)/(m_1+m_2),\quad K'_1/K_1=(v_1/u_1)^2",
            [
                tex(Fraction(ratio - 1, ratio + 1)),
                tex(Fraction(4, (ratio + 1) ** 2)),
                tex(Fraction(1, ratio**2)),
            ],
        )


@question_type(
    "phys.posn2561_q07",
    display_name={"th": "กำลังมอเตอร์ดึงวัตถุขึ้นพื้นเอียงฝืด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กำลังต้านน้ำหนักและแรงเสียดทาน",
)
class InclineMotorPower(PhysicsSheet):
    def expr(self, rng):
        weight, length, time = (
            100 * rng.randint(3, 30),
            5 * rng.randint(2, 10),
            10 * rng.randint(2, 12),
        )
        sine, cosine = rng.choice(
            ((Fraction(3, 5), Fraction(4, 5)), (Fraction(4, 5), Fraction(3, 5)))
        )
        mu = rng.choice((Fraction(1, 5), Fraction(1, 4), Fraction(1, 10)))
        power = q07.solve(weight=weight, length=length, time=time, sine=float(sine), mu=float(mu))
        return draw(
            7,
            tex(power),
            f"มอเตอร์ดึงวัตถุหนัก {weight} N ขึ้นพื้นเอียงยาว {length} m ด้วยความเร็วคงตัว "
            f"ใช้เวลา {time} s สัมประสิทธิ์เสียดทานจลน์ {show(mu)} "
            "กำลังของมอเตอร์เท่าใดในหน่วย W ใช้ค่าตรีโกณมิติตามสมการ",
            r"P=W(\sin\theta+\mu\cos\theta)L/t",
            [
                tex(weight * (sine - mu * cosine) * length / time),
                tex(weight * sine * length / time),
                tex(Fraction(weight * length, time)),
            ],
            rf"\sin\theta={tex(sine)},\quad\cos\theta={tex(cosine)}",
        )


@question_type(
    "phys.posn2561_q08",
    display_name={"th": "ความเร่งลูกโป่งเพื่อชนโพรเจกไทล์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การพบกันของโพรเจกไทล์กับวัตถุเร่งขึ้น",
)
class ProjectileBalloon(PhysicsSheet):
    def expr(self, rng):
        speed, target_acceleration = rng.choice((20, 30, 40, 50)), rng.choice((2, 5, 10))
        distance = Fraction(speed**2, 2 * (10 + target_acceleration))
        acceleration = q08.solve(speed=speed, distance_coeff=float(distance), g=10)
        return draw(
            8,
            tex(acceleration),
            f"ขว้างวัตถุจากพื้นด้วยอัตราเร็ว {speed} m/s ทำมุม 30° กับแนวระดับ "
            "พร้อมปล่อยลูกโป่งจากหยุดนิ่งขึ้นในแนวดิ่งจากพื้นซึ่งห่างจุดขว้างในแนวระดับ d "
            "ลูกโป่งต้องมีความเร่งขึ้นคงตัวเท่าใดในหน่วย m/s² เพื่อให้ชนวัตถุ "
            "(g = 10 m/s² ไม่คิดแรงต้านที่กระทำต่อวัตถุ)",
            r"t=d/(u\cos30^\circ),\quad \frac12at^2=u\sin30^\circ t-\frac12gt^2",
            [tex(acceleration + 10), tex(acceleration / 2), tex(acceleration + 20)],
            rf"d={tex(distance)}\sqrt{{3}}\ \mathrm{{m}}",
        )


@question_type(
    "phys.posn2561_q09",
    display_name={"th": "แรงตึงเชือกของลูกตุ้มกรวยสองชุด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="เปรียบเทียบลูกตุ้มกรวยที่คาบต่างกัน",
)
class ConicalPendulumRatio(PhysicsSheet):
    def expr(self, rng):
        mass, la, period = rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 4)
        lb = la + rng.randint(1, 5)
        ratio = q09.solve(mass_ratio=mass, len_a=la, len_b=lb, period_ratio=period)
        return draw(
            9,
            tex(ratio),
            f"ลูกตุ้มกรวย A และ B แขวนจากจุดเดียวกัน มวล A เป็น {mass} เท่าของ B "
            f"เชือก A ยาว {la}L เชือก B ยาว {lb}L ทั้งสองเคลื่อนที่เป็นวงกลมแนวระดับ "
            f"โดยคาบ A เป็น {period} เท่าของคาบ B อัตราส่วนขนาดแรงตึง Tₐ/Tᵦ เท่าใด",
            r"T=m(2\pi/P)^2\ell",
            [tex(Fraction(mass * la, lb * period)), tex(Fraction(mass, period**2)), tex(1 / ratio)],
        )


@question_type(
    "phys.posn2561_q10",
    display_name={"th": "แรงบานพับล่างของประตูในสมดุล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงบานพับประตูและสมดุลโมเมนต์",
)
class DoorHingeForces(PhysicsSheet):
    def expr(self, rng):
        scale = rng.randint(2, 15)
        weight, upper, horizontal = 9 * scale, 5 * scale, 3 * scale
        lower = q10.solve(weight=weight, width=1, separation=1.5, upper=upper)
        return draw(
            10,
            radical(lower**2),
            f"ประตูสม่ำเสมอหนัก {weight} N กว้าง 1 m บานพับบนและล่างอยู่ห่างกัน 1.5 m "
            f"แรงที่บานพับบนกระทำต่อประตูมีขนาด {upper} N "
            "โดยองค์ประกอบแนวดิ่งของแรงจากบานพับทั้งสองชี้ขึ้น "
            "แรงจากบานพับล่างมีขนาดเท่าใดในหน่วย N",
            r"Hh=Wb/2,\quad V_U=\sqrt{F_U^2-H^2},\quad F_L=\sqrt{H^2+(W-V_U)^2}",
            [
                radical(weight**2 - upper**2),
                radical(horizontal**2 + Fraction(weight**2, 4)),
                str(4 * scale),
            ],
        )


SLIPS.update(
    {
        11: ("phys.edge_charge_sign", "phys.diagonal_charge_sign", "phys.pair_energy_doubled"),
        12: (
            "phys.charge_linear_mass",
            "phys.charge_inverse_root_mass",
            "phys.charge_inverse_mass",
        ),
        13: (
            "phys.assumed_equal_resistors",
            "phys.series_over_smallest",
            "phys.inverse_resistance_range",
        ),
        14: (
            "phys.full_voltage_on_series_cap",
            "phys.ignored_parallel_capacitors",
            "phys.added_series_capacitances",
        ),
        15: (
            "phys.wire_diameter_as_radius",
            "phys.wire_area_as_radius",
            "phys.wire_centimeter_as_meter",
        ),
        16: (
            "phys.inverse_pressure_difference",
            "phys.ignored_heavy_liquid",
            "phys.same_liquid_depths",
        ),
        17: (
            "phys.gauge_in_gas_law",
            "phys.reported_absolute_pressure",
            "phys.ambient_pressure_added",
        ),
        18: (
            "phys.radius_gap_as_diameter",
            "phys.millimeter_centimeter_mix",
            "phys.ignored_temperature_interval",
        ),
        19: ("phys.lid_pressure_sign", "phys.lift_pressure_as_inside", "phys.ignored_lid_lift"),
        20: (
            "phys.demagnified_lens_position",
            "phys.focal_length_as_object_distance",
            "phys.midpoint_lens_position",
        ),
    }
)


@question_type(
    "phys.posn2561_q11",
    display_name={"th": "พลังงานศักย์ของประจุที่มุมสี่เหลี่ยม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานศักย์ไฟฟ้าของระบบประจุ",
)
class SquareChargeEnergy(PhysicsSheet):
    def expr(self, rng):
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        energy = q11.solve(a=a, b=b)
        assert abs(energy - (-4 * a * b + (a * a + b * b) / sqrt(2))) < 1e-9
        term = tex(Fraction(a * a + b * b, 2)) + r"\sqrt{2}"
        return draw(
            11,
            rf"{-4 * a * b}+{term}",
            f"ประจุที่มุมสี่เหลี่ยมจัตุรัสด้าน L เรียงตามเข็มนาฬิกาเป็น +{a}Q, −{b}Q, +{a}Q, −{b}Q พลังงานศักย์ไฟฟ้ารวมเทียบกับเมื่อแยกทุกประจุไปอนันต์ เป็นกี่เท่าของ kQ²/L",
            r"U=\sum_{i<j}kq_iq_j/r_{ij}",
            [
                rf"{4 * a * b}+{term}",
                rf"{-4 * a * b}-{term}",
                rf"{-8 * a * b}+{tex(a * a + b * b)}\sqrt{{2}}",
            ],
        )


@question_type(
    "phys.posn2561_q12",
    display_name={"th": "ปรับประจุเมื่อเพิ่มมวลลูกทรงกลม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลแรงไฟฟ้าและน้ำหนัก",
)
class ChargeMassScaling(PhysicsSheet):
    def expr(self, rng):
        factor = rng.choice((2, 3, 4, 5, 8, 9))
        ratio = q12.solve(factor=factor)
        return draw(
            12,
            radical(ratio**2),
            f"ลูกทรงกลมเหมือนกันสองลูกแขวนด้วยเชือกเบายาวเท่ากันจากจุดเดียว มีประจุบวกเท่ากัน q และผลักกันจนสมดุล ต่อมาเพิ่มมวลแต่ละลูกเป็น {factor} เท่า ต้องปรับประจุแต่ละลูกเป็นกี่เท่าของ q เพื่อให้เชือกเอียงมุมเดิมและระยะห่างเท่าเดิม",
            r"F_e\propto q^2,\quad F_e/(mg)=\tan\theta",
            [str(factor), radical(Fraction(1, factor)), tex(Fraction(1, factor))],
        )


@question_type(
    "phys.posn2561_q13",
    display_name={"th": "อัตราส่วนความต้านทานมากสุดต่อน้อยสุด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="วงจรตัวต้านทานอนุกรมและขนาน",
)
class ResistorRange(PhysicsSheet):
    def expr(self, rng):
        rs = (rng.randint(1, 4), rng.randint(5, 8), rng.randint(9, 12))
        answer = q13.solve(resistors=rs)
        return draw(
            13,
            tex(answer),
            f"มีตัวต้านทาน {rs[0]} Ω, {rs[1]} Ω และ {rs[2]} Ω อย่างละตัว ใช้ครบทั้งสามตัวต่อเป็นวงจรสองขั้วด้วยการต่ออนุกรมหรือขนาน โดยไม่ลัดวงจร อัตราส่วนความต้านทานรวมมากที่สุดต่อน้อยที่สุดเป็นเท่าใด",
            r"R_{max}=\sum R_i,\quad R_{min}^{-1}=\sum R_i^{-1}",
            ["9", tex(Fraction(sum(rs), min(rs))), tex(1 / answer)],
        )


@question_type(
    "phys.posn2561_q14",
    display_name={"th": "ประจุบนตัวเก็บประจุในแขนงผสม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ตัวเก็บประจุอนุกรมและขนาน",
)
class BranchCapacitorCharge(PhysicsSheet):
    def expr(self, rng):
        c = rng.randint(2, 9)
        parallel = (rng.randint(1, 4), rng.randint(2, 5), rng.randint(5, 9))
        v = 12 * rng.randint(2, 8)
        answer = q14.solve(voltage=v, cap=c, parallel=parallel)
        total = sum(parallel)
        return draw(
            14,
            tex(answer),
            f"แหล่งจ่ายอุดมคติ {v} V ต่อคร่อมสองแขนงขนาน แขนงบนมีตัวเก็บประจุ 5 μF ขนาน 4 μF แล้วอนุกรม 3 μF แขนงล่างมี {c} μF อนุกรมกับกลุ่มขนาน {parallel[0]}, {parallel[1]}, {parallel[2]} μF ตัวเก็บประจุเริ่มไม่มีประจุ ประจุบนตัว {c} μF เป็นกี่ μC",
            r"Q=C_{eq}V,\quad C_{eq}=C\,C_p/(C+C_p)",
            [str(c * v), tex(Fraction(v * c * parallel[0], c + parallel[0])), str((c + total) * v)],
        )


@question_type(
    "phys.posn2561_q15",
    display_name={"th": "รัศมีลวดจากกราฟกระแสและความต่างศักย์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สภาพนำไฟฟ้าและรูปทรงลวด",
)
class WireRadiusFromGraph(PhysicsSheet):
    def expr(self, rng):
        radius = Fraction(rng.randint(2, 9), 10)
        length = rng.choice((20, 40))
        sigma = rng.choice((1000000, 2500000))
        voltage = rng.choice((20, 40))
        current = Fraction(sigma) * radius**2 * voltage / Fraction(length * 10000)
        answer = q15.solve(length_cm=length, current=current, voltage=voltage, sigma_pi=sigma)
        return draw(
            15,
            tex(answer),
            f"ลวดทรงกระบอกสม่ำเสมอยาว {length} cm กราฟ I กับ V เป็นเส้นตรงผ่านจุดกำเนิดและจุด (V={voltage} V, I={show(current)} A) สภาพนำไฟฟ้า σ={sigma}/π (Ω m)⁻¹ รัศมีหน้าตัดลวดเป็นกี่ mm",
            r"I/V=\sigma\pi r^2/L",
            [tex(2 * radius), tex(radius**2), tex(10 * radius)],
        )


@question_type(
    "phys.posn2561_q16",
    display_name={"th": "ความลึกของของเหลวสามชนิดในหลอดรูปตัวยู"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลความดันของของเหลวหลายชั้น",
)
class ThreeLiquidDepth(PhysicsSheet):
    def expr(self, rng):
        heavy = 100 * rng.randint(12, 16)
        left = heavy - 200
        right = heavy - rng.choice((300, 400, 500))
        b = rng.randint(6, 24)
        answer = q16.solve(left=left, right=right, heavy=heavy, height_b=b)
        return draw(
            16,
            tex(answer),
            f"หลอดรูปตัวยูเปิดสู่บรรยากาศทั้งสองข้าง มีของเหลวหนักความหนาแน่น {heavy} kg/m³ เชื่อมด้านล่าง ด้านซ้ายมีของเหลว {left} kg/m³ หนา {b} cm ด้านขวามีของเหลว {right} kg/m³ หนา A ผิวบนสุดทั้งสองด้านอยู่ระดับเดียวกัน ของเหลวไม่ผสมกัน A เป็นกี่ cm",
            r"\rho_L B+\rho_H(D-B)=\rho_R A+\rho_H(D-A)",
            [
                tex(Fraction(b * (heavy - right), heavy - left)),
                tex(Fraction(b * left, right)),
                str(b),
            ],
        )


@question_type(
    "phys.posn2561_q17",
    display_name={"th": "ความดันเกจของแก๊สเมื่ออุณหภูมิเปลี่ยน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แก๊สอุดมคติและความดันเกจ",
)
class GaugeGasPressure(PhysicsSheet):
    def expr(self, rng):
        gauge = 20 * rng.randint(8, 20)
        start = 100
        end = rng.choice((40, 60, 80))
        t1 = rng.choice((27, 47))
        t2 = rng.choice((-23, -3, 7))
        answer = q17.solve(
            gauge=gauge, ambient_start=start, ambient_end=end, temp_start=t1, temp_end=t2
        )
        ratio = Fraction(t2 + 273, t1 + 273)
        return draw(
            17,
            tex(answer),
            f"แก๊สในภาชนะปิดแข็งปริมาตรคงตัวมีความดันเกจ {gauge} kPa เมื่อบรรยากาศภายนอก {start} kPa และอุณหภูมิ {t1} °C ต่อมาย้ายไปที่บรรยากาศ {end} kPa และอุณหภูมิแก๊ส {t2} °C ความดันเกจใหม่เป็นกี่ kPa ให้ T(K)=t(°C)+273 และไม่มีแก๊สรั่ว",
            r"(P_g+P_{atm})/T=\text{constant}",
            [tex(gauge * ratio - end), tex(answer + end), tex(answer + 2 * end)],
        )


@question_type(
    "phys.posn2561_q18",
    display_name={"th": "ผลต่างสัมประสิทธิ์ขยายตัวของวงแหวน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การขยายตัวเชิงเส้นด้วยความร้อน",
)
class ThermalCircleGap(PhysicsSheet):
    def expr(self, rng):
        length = rng.choice((10, 20, 30))
        gap = rng.choice((0.1, 0.2, 0.3, 0.4))
        dt = rng.choice((40, 60, 80))
        answer = q18.solve(length_pi_cm=length, gap_mm=gap, delta_t=dt) * 100000
        return draw(
            18,
            tex(answer),
            f"แถบโลหะสองชนิดมีความยาวเริ่มต้นเท่ากัน {length}π cm เมื่ออุณหภูมิเพิ่ม {dt} K นำแต่ละแถบมาดัดเป็นวงกลมครบหนึ่งรอบโดยไม่ยืดเพิ่ม วางร่วมศูนย์กลางแล้วรัศมีต่างกัน {gap} mm ผลต่างสัมประสิทธิ์ขยายตัวเชิงเส้นเป็นกี่หน่วยของ 10⁻⁵ K⁻¹ ใช้แบบจำลองการขยายตัวเชิงเส้นอิสระ",
            r"L_0(\alpha_2-\alpha_1)\Delta T=2\pi\Delta r",
            [tex(answer / 2), tex(answer * 10), tex(answer * dt)],
        )


@question_type(
    "phys.posn2561_q19",
    display_name={"th": "อุณหภูมิแก๊สจากแรงเปิดฝาภาชนะ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ความดัน แรงบนฝา และแก๊สอุดมคติ",
)
class GasUnderLid(PhysicsSheet):
    def expr(self, rng):
        height = rng.choice((10, 20, 30))
        area = rng.choice((20, 40, 60))
        force = area * rng.choice((4, 6, 8))
        answer = q19.solve(height_cm=height, area_cm2=area, force=force)
        base = q19.solve(height_cm=height, area_cm2=area, force=0)
        return draw(
            19,
            tex(answer),
            f"กระบอกสูง {height} cm หน้าตัด {area} cm² ปิดด้วยฝาเบามากและไม่ติดขอบ บรรจุแก๊สอุดมคติ 1/83 mol ภายนอกมีความดัน 100 kPa ต้องออกแรงดึงฝาขึ้น {force} N จึงเริ่มเปิด อุณหภูมิแก๊สเป็นกี่ K ให้ R=8.3 J/(mol K)",
            r"P_{in}A+F=P_{atm}A,\quad P_{in}Ah=nRT",
            [tex(2 * base - answer), tex(base - answer), tex(base)],
        )


@question_type(
    "phys.posn2561_q20",
    display_name={"th": "ตำแหน่งเลนส์ที่ให้ภาพจริงขยาย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมการเลนส์และภาพจริงบนฉาก",
)
class MagnifiedLensPosition(PhysicsSheet):
    def expr(self, rng):
        a, b = rng.choice(((2, 3), (1, 2), (1, 3), (2, 5)))
        scale = rng.randint(1, 8)
        distance = (a + b) ** 2 * scale
        focal = a * b * scale
        answer = q20.solve(distance=distance, focal=focal)
        return draw(
            20,
            tex(answer),
            f"วัตถุกับฉากห่างกัน {distance} cm วางเลนส์นูนบางความยาวโฟกัส {focal} cm ระหว่างทั้งสองให้เกิดภาพจริงคมชัดที่ขยายใหญ่กว่าวัตถุ เลนส์ต้องอยู่ห่างจากวัตถุกี่ cm",
            r"u+v=D,\quad 1/u+1/v=1/f,\quad v>u",
            [tex(distance - answer), str(focal), tex(Fraction(distance, 2))],
        )


SLIPS.update(
    {
        21: (
            "phys.rocket_ignored_coast",
            "phys.rocket_ignored_powered_height",
            "phys.rocket_thrust_as_net",
        ),
        22: (
            "phys.wedge_ignored_acceleration",
            "phys.wedge_acceleration_sign",
            "phys.wedge_wrong_component",
        ),
        23: (
            "phys.cylinder_ignored_torque",
            "phys.cylinder_ignored_friction",
            "phys.cylinder_wrong_rope_direction",
        ),
        24: (
            "phys.incline_relative_speed_halved",
            "phys.incline_ignored_gravity",
            "phys.incline_full_height",
        ),
        25: (
            "phys.impulse_initial_momentum_sign",
            "phys.impulse_peak_rectangle",
            "phys.impulse_ignored_first_trapezoid",
        ),
        26: ("phys.work_ignored_weight", "phys.work_added_weight", "phys.work_weight_only"),
        27: (
            "phys.switch_total_current_as_branch",
            "phys.switch_ignored_voltage_drop",
            "phys.switch_change_sign",
        ),
        28: (
            "phys.buoyancy_ignored_torque",
            "phys.buoyancy_wrong_centroid",
            "phys.buoyancy_ratio_inverted",
        ),
        29: (
            "phys.heat_ignored_melting",
            "phys.heat_ignored_meltwater",
            "phys.heat_ignored_final_metal_temperature",
        ),
        30: (
            "phys.beam_added_focal_magnitudes",
            "phys.beam_used_convex_focus",
            "phys.beam_reversed_gap",
        ),
    }
)


@question_type(
    "phys.posn2561_q21",
    display_name={"th": "ความสูงสูงสุดของจรวดหลังดับเครื่อง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่สองช่วงของจรวด",
)
class RocketApex(PhysicsSheet):
    def expr(self, rng):
        a = rng.choice((5, 10, 15, 20))
        time = rng.randint(2, 12)
        answer = q21.solve(acceleration=a, time=time, g=10)
        return draw(
            21,
            tex(answer),
            f"จรวดเริ่มจากหยุดนิ่งที่พื้น เคลื่อนขึ้นด้วยความเร่งสุทธิ {a} m/s² นาน {time} s แล้วเครื่องยนต์ดับ จากนั้นมีเพียงแรงโน้มถ่วง g=10 m/s² ความสูงสูงสุดเหนือพื้นเป็นกี่ m ไม่คิดแรงต้าน",
            r"h=\tfrac12at^2+v^2/(2g),\quad v=at",
            [
                tex(a * time * time / 2),
                tex((a * time) ** 2 / 20),
                tex((a + 10) * time * time / 2 + ((a + 10) * time) ** 2 / 20),
            ],
        )


@question_type(
    "phys.posn2561_q22",
    display_name={"th": "แรงผนังที่ลูกบอลบนพื้นเอียงเร่ง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลสัมพัทธ์ในระบบเร่ง",
)
class AcceleratingWedgeWall(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 8)
        a = rng.randint(1, 8)
        tangent = rng.choice((Fraction(3, 4), Fraction(4, 3), 1))
        theta = {Fraction(3, 4): 36.86989764584402, Fraction(4, 3): 53.13010235415598, 1: 45}[
            tangent
        ]
        answer = q22.solve(mass=mass, acceleration=a, theta=theta, g=10)
        return draw(
            22,
            tex(answer),
            f"ลูกบอลมวล {mass} kg อยู่ระหว่างพื้นเอียงลาดลงทางขวากับผนังแนวดิ่งทางขวา ผิวสัมผัสทุกจุดลื่น ทั้งพื้นเอียงและผนังเคลื่อนไปทางซ้ายด้วยความเร่ง {a} m/s² โดยลูกบอลอยู่นิ่งเทียบกับทั้งสอง แรงที่ผนังกระทำต่อลูกบอลมีขนาดกี่ N ให้ g=10 m/s² และมุมพื้นเอียง θ ตามสมการ",
            r"N\cos\theta=mg,\quad N\sin\theta-R=-ma",
            [
                tex(10 * mass * tangent),
                tex(mass * abs(10 * tangent - a)),
                tex(mass * (a + 10 / tangent)),
            ],
            rf"\tan\theta={tex(tangent)}",
        )


@question_type(
    "phys.posn2561_q23",
    display_name={"th": "แรงเชือกแนวระดับที่พยุงทรงกระบอก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลแรงและโมเมนต์ของทรงกระบอก",
)
class CylinderTangentRope(PhysicsSheet):
    def expr(self, rng):
        ratio = rng.choice((Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)))
        # tan(theta/2)=ratio; theta from atan is only a way to pass this geometry to the solver.
        from math import atan, degrees

        theta = degrees(2 * atan(float(ratio)))
        answer = q23.solve(theta=theta)
        return draw(
            23,
            tex(answer),
            "ทรงกระบอกหนัก W วางนิ่งบนพื้นเอียงสูงขึ้นทางขวา เชือกเบาดึงไปทางขวาในแนวระดับและสัมผัสทรงกระบอกที่จุดบนสุด มีแรงเสียดทานสถิตเพียงพอ แรงตึงเชือกเป็นกี่เท่าของ W ให้ค่าตรีโกณมิติตามสมการ",
            r"f=T,\quad T\cos\theta+f=W\sin\theta",
            [tex(2 * ratio / (1 - ratio**2)), tex(2 * ratio), tex(1 / ratio)],
            rf"\sin\theta={tex(2 * ratio / (1 + ratio**2))},\quad\cos\theta={tex((1 - ratio**2) / (1 + ratio**2))}",
        )


@question_type(
    "phys.posn2561_q24",
    display_name={"th": "ความเร็วต้นเพื่อพบกันกลางพื้นเอียง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่พร้อมกันบนพื้นเอียง",
)
class InclineMeetingMidpoint(PhysicsSheet):
    def expr(self, rng):
        length = rng.randint(2, 15)
        sine = rng.choice((Fraction(1, 2), Fraction(3, 5), Fraction(4, 5)))
        answer = q24.solve(length=length, sine=float(sine), g=10)
        return draw(
            24,
            radical(answer**2),
            f"พื้นเอียงลื่นยาว {length} m ตามแนวลาด ปล่อยก้อน A จากหยุดนิ่งที่ปลายบน พร้อมยิงก้อน B จากปลายล่างขึ้นตามแนวลาด ทั้งสองพบกันตรงกึ่งกลางพื้นเอียง ต้องยิง B ด้วยอัตราเร็วต้นกี่ m/s ให้ g=10 m/s² และใช้ค่ามุมตามสมการ",
            r"L/2=\tfrac12g\sin\theta\,t^2,\quad L/2=ut-\tfrac12g\sin\theta\,t^2",
            [radical(answer**2 / 4), radical(10 * length), radical(2 * answer**2)],
            rf"\sin\theta={tex(sine)}",
        )


@question_type(
    "phys.posn2561_q25",
    display_name={"th": "ความเร็วหลังตีจากกราฟแรงกับเวลา"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การดลจากกราฟแรงเป็นช่วง",
)
class BatForceImpulse(PhysicsSheet):
    def expr(self, rng):
        mass = rng.choice((50, 100))
        incoming = rng.randint(2, 8)
        first = 50 * rng.randint(1, 3)
        peak = first + 100
        rise = rng.choice((10, 20))
        fall = 5
        answer = q25.solve(
            mass_g=mass, incoming=incoming, first_force=first, peak=peak, rise_ms=rise, fall_ms=fall
        )
        return draw(
            25,
            tex(answer),
            f"ลูกบอลมวล {mass} g วิ่งเข้าหาไม้ด้วยอัตราเร็ว {incoming} m/s แรงจากไม้สวนทิศความเร็วเดิมตลอดช่วงสัมผัส กราฟแรงกับเวลาเป็นเส้นตรงเชื่อม (0 ms,{first} N), ({rise} ms,{peak} N), ({rise + fall} ms,0 N) ลูกบอลกระดอนออกด้วยอัตราเร็วกี่ m/s ไม่คิดแรงดลอื่น",
            r"J=\int Fdt=m(v_{out}+v_{in})",
            [
                tex(answer + 2 * incoming),
                tex(Fraction(peak * (rise + fall), mass) - incoming),
                tex(Fraction(peak * fall, 2 * mass) - incoming),
            ],
        )


@question_type(
    "phys.posn2561_q26",
    display_name={"th": "พลังงานจลน์ที่เพิ่มเมื่อดึงวัตถุขึ้น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="งานสุทธิและพลังงานจลน์",
)
class NetVerticalWork(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 8)
        force = mass * 10 + rng.randint(5, 30)
        distance = rng.randint(2, 10)
        answer = q26.solve(mass=mass, force=force, distance=distance, g=10)
        return draw(
            26,
            tex(answer),
            f"ออกแรงคงตัว {force} N ดึงวัตถุมวล {mass} kg ขึ้นในแนวดิ่งเป็นระยะ {distance} m พลังงานจลน์เพิ่มขึ้นกี่ J ให้ g=10 m/s² และไม่มีแรงต้าน",
            r"\Delta K=W_{net}=Fd-mgd",
            [str(force * distance), str((force + mass * 10) * distance), str(mass * 10 * distance)],
        )


@question_type(
    "phys.posn2561_q27",
    display_name={"th": "กระแสแขนงเปลี่ยนเมื่อปิดสวิตช์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การแบ่งกระแสในวงจรที่มีตัวต้านทานร่วม",
)
class SwitchedBranchCurrent(PhysicsSheet):
    def expr(self, rng):
        voltage = 10 * rng.randint(2, 10)
        series = rng.choice((10, 15, 20))
        branch = 10
        added = (20, 20)
        answer = q27.solve(voltage=voltage, series=series, branch=branch, added=added)
        before = Fraction(voltage, series + branch)
        after = answer + before
        return draw(
            27,
            tex(answer),
            f"แหล่งจ่ายอุดมคติ {voltage} V ต่ออนุกรมกับ {series} Ω แล้วต่อกับแขนง 10 Ω ที่มีแอมมิเตอร์อุดมคติต่ออนุกรมอยู่ ปิดสวิตช์เพื่อเพิ่มแขนง 20 Ω สองแขนงขนานกับ 10 Ω กระแสที่แอมมิเตอร์เปลี่ยนเป็นกี่ A โดยนิยามการเปลี่ยนเท่ากับค่าหลังปิดลบค่าก่อนปิด",
            r"V_{branch}=V R_p/(R_s+R_p),\quad I_A=V_{branch}/10",
            [tex(2 * after - before), tex(Fraction(voltage, branch) - before), tex(-answer)],
        )


@question_type(
    "phys.posn2561_q28",
    display_name={"th": "อัตราส่วนความหนาแน่นของแท่งลอยมีจุดหมุน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงลอยตัวและสมดุลโมเมนต์",
)
class PivotedFloatingRod(PhysicsSheet):
    def expr(self, rng):
        length = 10 * rng.randint(4, 10)
        submerged = rng.choice((10, 20, 30))
        answer = q28.solve(length=length, submerged=submerged)
        return draw(
            28,
            tex(answer),
            f"แท่งไม้บางสม่ำเสมอยาว {length} cm มีจุดหมุนไร้โมเมนต์ที่ปลายบนซึ่งแห้ง แท่งอยู่สมดุลเอียงทำมุมที่ไม่เป็นแนวดิ่ง ส่วนปลายล่างจมน้ำยาว {submerged} cm ตามแนวแท่ง อัตราส่วนความหนาแน่นน้ำต่อไม้เป็นเท่าใด ไม่คิดแรงตึงผิว",
            r"\rho_{wood}ALg(L/2)=\rho_{water}Asg(L-s/2)",
            [
                tex(Fraction(length, submerged)),
                tex(Fraction(length**2, submerged * (length - submerged))),
                tex(1 / answer),
            ],
        )


@question_type(
    "phys.posn2561_q29",
    display_name={"th": "อุณหภูมิเริ่มต้นของโลหะที่ทำให้น้ำแข็งละลาย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลความร้อนและการเปลี่ยนสถานะ",
)
class IceWaterMetalHeat(PhysicsSheet):
    def expr(self, rng):
        water = 100 * rng.randint(2, 5)
        ice = 100 * rng.randint(1, 3)
        metal = 500 * rng.randint(1, 4)
        final = rng.choice((5, 10, 20))
        specific = 2
        answer = q29.solve(water_g=water, ice_g=ice, metal_g=metal, metal_c=specific, final=final)
        return draw(
            29,
            tex(answer),
            f"ภาชนะฉนวนมีน้ำ {water} g และน้ำแข็ง {ice} g ที่ 0 °C ใส่โลหะ {metal} g ความร้อนจำเพาะ 2 J/(g K) แล้วสมดุลที่ {final} °C น้ำแข็งละลายหมด โลหะเริ่มต้นที่กี่ °C ให้ความร้อนจำเพาะน้ำ 4.2 J/(g K) ความร้อนแฝงหลอมเหลวน้ำแข็ง 335 J/g ไม่คิดความร้อนภาชนะ",
            r"m_mc_m(T_i-T_f)=m_iL+(m_w+m_i)c_wT_f",
            [
                tex(final + Fraction((water + ice) * 42 * final, 10 * metal * specific)),
                tex(
                    final
                    + Fraction(ice * 335, metal * specific)
                    + Fraction(water * 42 * final, 10 * metal * specific)
                ),
                tex(answer - final),
            ],
        )


@question_type(
    "phys.posn2561_q30",
    display_name={"th": "ระยะเลนส์ของชุดขยายลำแสงขนาน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ระบบเลนส์เว้าร่วมเลนส์นูนแบบไร้โฟกัส",
)
class AfocalBeamExpander(PhysicsSheet):
    def expr(self, rng):
        diverging = rng.randint(2, 10)
        ratio = rng.randint(2, 5)
        converging = diverging * ratio
        answer = q30.solve(diverging=diverging, converging=converging)
        return draw(
            30,
            tex(answer),
            f"ลำแสงขนานแกนผ่านเลนส์เว้าบาง f₁=−{diverging} cm แล้วผ่านเลนส์นูนบาง f₂=+{converging} cm ที่วางร่วมแกน ต้องวางเลนส์ห่างกันกี่ cm เพื่อให้ลำแสงออกขนานและมีเส้นผ่านศูนย์กลางขยาย {ratio} เท่า",
            r"d=f_2+f_1=f_2-|f_1|",
            [str(converging + diverging), str(converging), tex(-answer)],
        )
