"""Seeded variants of the reviewed POSN physics 2564 camp selection paper."""

from fractions import Fraction
from math import isqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.posn2564_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2564_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2564_physics import q21, q22, q23, q24, q25, q26, q27, q28, q29, q30

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


def show(value):
    """Exact plain text: a short decimal when one is exact, otherwise a/b."""
    value = Fraction(value)
    if (value * 100).denominator == 1:
        return f"{float(value):g}"
    return f"{value.numerator}/{value.denominator}"


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


def pair(first, second):
    return rf"\left({first},\ {second}\right)"


SLIPS = {
    1: ("phys.slip_relative_as_pull", "phys.slip_ground_acceleration", "phys.slip_friction_sign"),
    2: ("phys.gravity_radius_not_squared", "phys.gravity_radius_inverted", "phys.gravity_radius_cubed"),
    3: ("phys.infall_half_kinetic", "phys.infall_from_infinity", "phys.infall_used_ratio"),
    4: ("phys.restitution_ratio_inverted", "phys.restitution_assumed_elastic", "phys.restitution_ratio_squared"),
    5: ("phys.spring_extension_from_equilibrium", "phys.spring_amplitude_doubled", "phys.spring_released_at_natural_length"),
    6: ("phys.buoyant_rise_wrong_ratio", "phys.buoyant_rise_weight_ignored", "phys.buoyant_rise_inverted"),
    7: ("phys.mixing_simple_average", "phys.mixing_weights_swapped", "phys.mixing_half_difference"),
    8: ("phys.ring_force_point_distance", "phys.ring_force_projection_power", "phys.ring_force_centre_charge"),
    9: ("phys.arc_potential_axis_distance", "phys.arc_potential_added_distances", "phys.arc_potential_radius_only"),
    10: ("phys.charge_share_initial_energy", "phys.charge_share_final_energy", "phys.charge_share_capacitors_swapped"),
    11: ("phys.bridge_charge_one_branch", "phys.bridge_charge_added_branches", "phys.bridge_charge_full_emf"),
    12: ("phys.lens_shift_inverted_squared", "phys.lens_shift_not_squared", "phys.lens_shift_inverted"),
    13: ("phys.focus_intensity_linear", "phys.focus_intensity_screen_ratio", "phys.focus_intensity_wrong_cone"),
    14: ("phys.isothermal_slope_sign", "phys.isothermal_slope_inverted", "phys.isothermal_slope_inverted_negative"),
    15: ("phys.rms_ratio_no_root", "phys.rms_ratio_squared", "phys.rms_ratio_inverted"),
    16: ("phys.charge_ring_pair_ignored", "phys.charge_ring_pair_distance_r", "phys.charge_ring_pair_sign"),
    17: ("phys.conical_used_string_length", "phys.conical_omega_not_rooted", "phys.conical_used_radius"),
    18: ("phys.meeting_one_projectile_closing", "phys.meeting_ignored_angle", "phys.meeting_both_errors"),
    19: ("phys.loop_field_ratio_inverted", "phys.loop_field_wrong_power", "phys.loop_field_radius_ignored"),
    20: ("phys.ladder_answered_last_series", "phys.ladder_answered_first_series", "phys.ladder_answered_total"),
    21: ("phys.prism_snell_inverted", "phys.prism_cos_incidence_scaled", "phys.prism_cos_incidence"),
    22: ("phys.scale_offset_ignored", "phys.scale_span_as_top", "phys.scale_reversed_conversion"),
    23: ("phys.rod_rotation_ignored", "phys.rod_inertia_about_end", "phys.rod_rotation_subtracted"),
    24: ("phys.capillary_exponent_one", "phys.capillary_exponent_half", "phys.capillary_exponent_two"),
    25: ("phys.slab_critical_used_slab", "phys.slab_critical_wrong_interface", "phys.slab_critical_wrong_interface_inverted"),
    26: ("phys.two_source_drop_ignored", "phys.two_source_resistors_swapped", "phys.two_source_polarity_added"),
    27: ("phys.gap_shift_path_ignored", "phys.gap_shift_along_face", "phys.gap_shift_wrong_cosine"),
    28: ("phys.repulsion_single_speed", "phys.repulsion_energy_to_one", "phys.repulsion_energy_doubled"),
    29: ("phys.wedge_recoil_mass_share", "phys.wedge_angle_ignored", "phys.wedge_used_sine"),
    30: ("phys.wall_apex_tan_geometric", "phys.wall_apex_tan_inverted", "phys.wall_apex_vertical_only"),
}

# Sines whose cosines are rational, for angles that keep answers exact.
SINES = tuple(
    Fraction(a, c)
    for a, b, c in ((3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17))
    for a in (a, b)
)
TRIPLES = ((3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17))


def cosine(sine):
    root = Fraction(isqrt((sine.denominator**2 - sine.numerator**2)), sine.denominator)
    assert root * root + sine * sine == 1
    return root


def draw(number, answer, prompt, hint, slips):
    return MathDraw(
        "",
        answer,
        prompt=prompt,
        hint=hint,
        distractors=[named(tag, value) for tag, value in zip(SLIPS[number], slips)],
    )


class PhysicsSheet(WordProblem):
    sheet_id = "posn2564_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2564)"


@question_type(
    "phys.posn2564_q01",
    display_name={"th": "ความเร่งสัมพัทธ์ของแผ่นที่ไถล"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงเสียดทานและความเร่งสัมพัทธ์",
)
class PlankSlip(PhysicsSheet):
    def expr(self, rng):
        mu = Fraction(rng.randint(1, 5), 10)
        limit = mu * 10
        accel = int(limit) + rng.randint(1, 6)
        answer = agree(q01.solve(mu=float(mu), accel=accel, g=10), accel - limit)
        return draw(
            1,
            tex(answer),
            f"แผ่น B วางบนแผ่น A ซึ่งวางบนพื้นระดับ สัมประสิทธิ์ความเสียดทานระหว่าง A กับ B เท่ากับ {show(mu)} (ใช้ค่าเดียวกันทั้งสถิตและจลน์) ดึง A ไปทางขวาด้วยความเร่งคงตัว {accel} m/s² ให้ g=10 m/s² B จะไถลบน A หรือไม่ ถ้าไถล ความเร่งของ B เทียบกับ A มีขนาดกี่ m/s²",
            r"a_B\le\mu g,\quad a_{B/A}=a-\mu g",
            [str(accel), tex(limit), tex(accel + limit)],
        )


@question_type(
    "phys.posn2564_q02",
    display_name={"th": "ความเร่งโน้มถ่วงเมื่อเปลี่ยนมวลและรัศมีดาว"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎความโน้มถ่วงสากลและค่า g",
)
class SurfaceGravityScale(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 4)
        radius = rng.choice((Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 2), Fraction(2)))
        answer = agree(q02.solve(mass_factor=mass, radius_factor=float(radius)), mass / radius**2)
        return draw(
            2,
            tex(answer),
            f"ดาวเคราะห์ทรงกลมดวงหนึ่ง ถ้ามวลเป็น {mass} เท่าของเดิมและรัศมีเป็น {show(radius)} เท่าของเดิม ความเร่งโน้มถ่วงที่ผิวดาวใหม่เป็นกี่เท่าของค่าเดิม",
            r"g=GM/R^2",
            [tex(mass / radius), tex(mass * radius**2), tex(mass / radius**3)],
        )


@question_type(
    "phys.posn2564_q03",
    display_name={"th": "อัตราเร็วเมื่อตกจากระยะไกลสู่ผิวโลก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานศักย์โน้มถ่วงระยะไกล",
)
class RadialInfall(PhysicsSheet):
    def expr(self, rng):
        n = rng.choice((2, 3, 4, 5, 6, 9, 10))
        squared = Fraction(2 * (n - 1), n)
        agree(q03.solve(n=n) ** 2, squared)
        return draw(
            3,
            radical(squared),
            f"ปล่อยวัตถุจากหยุดนิ่งที่ระยะ {n}R จากศูนย์กลางโลก (R เป็นรัศมีโลก) ให้ตกตามแนวรัศมีเข้าสู่โลกโดยไม่มีแรงต้านจนถึงบรรยากาศบางๆ ที่ผิวโลก อัตราเร็วขณะนั้นเป็นกี่เท่าของ √(gR) โดย g เป็นความเร่งโน้มถ่วงที่ผิวโลก",
            r"\tfrac12v^2=GM\left(\tfrac1R-\tfrac1x\right),\quad GM=gR^2",
            [radical(squared / 2), radical(2), radical(Fraction(2, n))],
        )


@question_type(
    "phys.posn2564_q04",
    display_name={"th": "สัมประสิทธิ์การคืนตัวที่ทำให้ลูกชนหยุด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สัมประสิทธิ์การคืนตัวและโมเมนตัม",
)
class RestitutionStop(PhysicsSheet):
    def expr(self, rng):
        heavy = rng.randint(3, 9)
        light = rng.randint(1, heavy - 1)
        ratio = Fraction(light, heavy)
        answer = agree(q04.solve(e=float(ratio)), ratio)
        return draw(
            4,
            tex(answer),
            f"มวล {light} kg วิ่งชนตรงกับมวล {heavy} kg ที่หยุดนิ่งบนพื้นลื่นในหนึ่งมิติ สัมประสิทธิ์การคืนตัว e=(V−v)/u ต้องมีค่าเท่าใด มวล {light} kg จึงหยุดนิ่งทันทีหลังชน (u เป็นอัตราเร็วก่อนชน v และ V เป็นความเร็วหลังชนของมวลเบาและมวลหนัก)",
            r"mu=mv+MV,\quad V-v=eu",
            [tex(1 / ratio), "1", tex(ratio**2)],
        )


@question_type(
    "phys.posn2564_q05",
    display_name={"th": "ระยะยืดมากสุดของสปริงหลังปล่อย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แบบซิมเปิลฮาร์มอนิกของสปริงแขวน",
)
class SpringRelease(PhysicsSheet):
    def expr(self, rng):
        mass, k = rng.choice(((Fraction(1, 5), 20), (Fraction(1, 2), 50), (Fraction(1, 2), 25), (1, 50), (1, 100), (2, 100), (2, 50)))
        static = Fraction(100 * 10) * mass / k
        lift = rng.randint(1, int(static) - 1)
        answer = agree(q05.solve(mass=float(mass), k=k, lift=lift, g=10), static + lift)
        return draw(
            5,
            tex(answer),
            f"มวล {show(Fraction(mass))} kg แขวนกับสปริงเบาค่าคงตัว {k} N/m อยู่นิ่งที่ตำแหน่งสมดุล ยกมวลขึ้นตรงๆ {lift} cm จากตำแหน่งสมดุล จับนิ่งแล้วปล่อย ขณะมวลอยู่ต่ำสุด สปริงยืดออกจากความยาวธรรมชาติกี่ cm ให้ g=10 m/s² ไม่คิดแรงต้าน",
            r"x_{eq}=mg/k,\quad\text{amplitude}=a",
            [str(lift), tex(static + 2 * lift), tex(2 * static)],
        )


@question_type(
    "phys.posn2564_q06",
    display_name={"th": "ความสูงที่ลูกเบาพุ่งพ้นผิวน้ำ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="แรงลอยตัวและงานพลังงาน",
)
class BuoyantRise(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 6)
        volume = mass * rng.randint(2, 4) + rng.choice((0, mass // 2))
        depth = 5 * rng.randint(1, 6)
        ratio = Fraction(volume, mass)
        answer = agree(q06.solve(mass=mass, volume=volume, depth=depth), (ratio - 1) * depth)
        return draw(
            6,
            tex(answer),
            f"ลูกบอลเบามวล {mass} g ปริมาตร {volume} cm³ ถูกปล่อยจากหยุดนิ่งที่ก้นถังน้ำลึก {depth} cm (น้ำหนาแน่น 1 g/cm³) คิดลูกบอลเป็นจุดที่รับแรงลอยตัวเต็มจนถึงผิวน้ำ และไม่คิดแรงต้านของน้ำและอากาศ ลูกบอลพุ่งขึ้นพ้นผิวน้ำได้สูงสุดกี่ cm",
            r"(\rho Vg-mg)h=mgH",
            [tex((1 - 1 / ratio) * depth), tex(ratio * depth), tex(depth / ratio)],
        )


@question_type(
    "phys.posn2564_q07",
    display_name={"th": "อุณหภูมิสุดท้ายเมื่อผสมของเหลว"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมดุลความร้อนของการผสม",
)
class LiquidMixing(PhysicsSheet):
    def expr(self, rng):
        hot = 10 * rng.randint(5, 9)
        cold = 10 * rng.randint(1, 4)
        ratio = rng.choice((Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3), Fraction(3, 2), Fraction(2, 3)))
        exact = (ratio * hot + cold) / (ratio + 1)
        answer = agree(q07.solve(hot=hot, cold=cold, ratio=float(ratio)), exact)
        return draw(
            7,
            tex(answer),
            f"ของเหลว A อุณหภูมิ {hot} °C ผสมกับของเหลว B อุณหภูมิ {cold} °C ในภาชนะฉนวนจนเป็นเนื้อเดียว ไม่มีปฏิกิริยาเคมีหรือการเปลี่ยนสถานะ และไม่คิดความจุความร้อนของภาชนะ กำหนดให้ m_A S_A = {show(ratio)} m_B S_B อุณหภูมิสุดท้ายเป็นกี่ °C",
            r"m_AS_A(\theta_A-T)=m_BS_B(T-\theta_B)",
            [
                tex(Fraction(hot + cold, 2)),
                tex((hot + ratio * cold) / (ratio + 1)),
                tex(Fraction(hot - cold, 2)),
            ],
        )


@question_type(
    "phys.posn2564_q08",
    display_name={"th": "แรงบนประจุบนแกนวงแหวนมีประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การอินทิเกรตสนามและสมมาตร",
)
class RingAxialForce(PhysicsSheet):
    def expr(self, rng):
        a, b, c = rng.choice(TRIPLES)
        radius, distance = (a, b) if rng.random() < 0.5 else (b, a)
        exact = Fraction(distance, c**3)
        answer = agree(q08.solve(radius=radius, distance=distance), exact)
        return draw(
            8,
            tex(answer),
            f"วงแหวนรัศมี {radius} m มีประจุ q กระจายสม่ำเสมอ ประจุ Q อยู่บนแกนของวงแหวนห่างจากศูนย์กลาง {distance} m ขนาดแรงไฟฟ้าบน Q เป็นกี่เท่าของ kqQ ในหน่วย m⁻² โดย k=1/(4πε₀)",
            r"F=\frac{kqQx}{(x^2+R^2)^{3/2}}",
            [tex(Fraction(1, c * c)), tex(Fraction(distance, c * c)), tex(Fraction(1, distance**2))],
        )


@question_type(
    "phys.posn2564_q09",
    display_name={"th": "ศักย์บนแกนของครึ่งวงกลมมีประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ศักย์ไฟฟ้าของประจุกระจายตามเส้น",
)
class OffPlaneArcPotential(PhysicsSheet):
    def expr(self, rng):
        a, b, c = rng.choice(TRIPLES)
        radius, distance = (a, b) if rng.random() < 0.5 else (b, a)
        answer = agree(q09.solve(radius=radius, distance=distance), Fraction(1, c))
        return draw(
            9,
            tex(answer),
            f"เส้นลวดครึ่งวงกลมรัศมี {radius} m อยู่ในระนาบ YZ มีศูนย์กลางที่ O และมีประจุรวม q กระจายสม่ำเสมอ จุด P อยู่บนแกน X ห่างจาก O {distance} m ศักย์ไฟฟ้าที่ P (ให้ศักย์ที่ระยะอนันต์เป็นศูนย์) เป็นกี่เท่าของ kq ในหน่วย m⁻¹",
            r"V=\frac{kq}{\sqrt{x^2+R^2}}",
            [tex(Fraction(1, distance)), tex(Fraction(1, distance + radius)), tex(Fraction(1, radius))],
        )


@question_type(
    "phys.posn2564_q10",
    display_name={"th": "ความร้อนเมื่อแบ่งประจุระหว่างตัวเก็บประจุ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานตัวเก็บประจุและการแบ่งประจุ",
)
class ChargeSharingHeat(PhysicsSheet):
    def expr(self, rng):
        c1, c2 = rng.sample(range(1, 7), 2)
        charge = 6 * rng.randint(1, 4)
        exact = Fraction(charge * charge * c2, 2 * c1 * (c1 + c2))
        answer = agree(q10.solve(c1=c1, c2=c2, q0=charge), exact)
        return draw(
            10,
            tex(answer),
            f"ตัวเก็บประจุ C₁={c1} μF มีประจุ {charge} μC ต่อเป็นวงเดียวกับสวิตช์ ตัวต้านทาน และตัวเก็บประจุ C₂={c2} μF ที่ไม่มีประจุ หลังปิดสวิตช์นานพอ พลังงานไฟฟ้าที่เปลี่ยนเป็นความร้อนในตัวต้านทานเป็นกี่ μJ",
            r"\frac{q_0^2}{2C_1}-\frac{q_0^2}{2(C_1+C_2)}",
            [
                tex(Fraction(charge * charge, 2 * c1)),
                tex(Fraction(charge * charge, 2 * (c1 + c2))),
                tex(Fraction(charge * charge * c1, 2 * c2 * (c1 + c2))),
            ],
        )


@question_type(
    "phys.posn2564_q11",
    display_name={"th": "ประจุบนตัวเก็บประจุในวงจรบริดจ์"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="วงจรตัวเก็บประจุในสถานะคงตัว",
)
class BridgeCapacitorCharge(PhysicsSheet):
    def expr(self, rng):
        while True:
            r1, r2, r3, r4 = (rng.randint(1, 6) for _ in range(4))
            if r1 * r4 != r2 * r3:
                break
        emf = rng.choice((6, 12, 21, 24, 42))
        cap = rng.randint(1, 5)
        top, bottom = Fraction(r2, r1 + r2), Fraction(r4, r3 + r4)
        exact = cap * emf * abs(top - bottom)
        agree(q11.solve(r1=r1, r2=r2, r3=r3, r4=r4) * cap * emf, exact)
        return draw(
            11,
            tex(exact),
            f"แขนงบนมีตัวต้านทาน {r1}R และ {r2}R ต่ออนุกรม แขนงล่างมี {r3}R และ {r4}R ต่ออนุกรม ทั้งสองแขนงต่อขนานคร่อมแบตเตอรี่อุดมคติ {emf} V โดย {r1}R ของแขนงบนและ {r3}R ของแขนงล่างต่อกับขั้วเดียวกัน ตัวเก็บประจุ {cap} μF ต่อระหว่างจุดต่อกลางของสองแขนง เมื่อกระแสคงตัวแล้ว ประจุบนตัวเก็บประจุมีขนาดกี่ μC",
            r"Q=C\left|V_{top}-V_{bottom}\right|",
            [tex(cap * emf * top), tex(cap * emf * (top + bottom)), str(cap * emf)],
        )


@question_type(
    "phys.posn2564_q12",
    display_name={"th": "การเปลี่ยนระยะภาพเมื่อโฟกัสเปลี่ยนเล็กน้อย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สมการเลนส์และการเปลี่ยนแปลงเล็ก",
)
class ImageShift(PhysicsSheet):
    def expr(self, rng):
        focal = rng.choice((5, 10, 12, 15, 20))
        ratio = rng.choice((Fraction(3, 2), Fraction(2), Fraction(3), Fraction(4), Fraction(5, 2), Fraction(5)))
        if (ratio * focal).denominator != 1:
            ratio = Fraction(2)
        distance = int(ratio * focal)
        exact = (ratio / (ratio - 1)) ** 2
        answer = agree(q12.solve(focal=focal, object_distance=distance), exact)
        return draw(
            12,
            tex(answer),
            f"วัตถุอยู่ห่างเลนส์บาง {distance} cm คงที่ เลนส์มีความยาวโฟกัส {focal} cm และให้ภาพจริงตามสูตร 1/v+1/u=1/f ถ้าความยาวโฟกัสเพิ่มขึ้นเล็กน้อย Δf (Δf ≪ f) ระยะภาพจะเพิ่มขึ้นประมาณกี่เท่าของ Δf",
            r"v=\frac{uf}{u-f},\quad\frac{dv}{df}",
            [tex(1 / exact), tex(ratio / (ratio - 1)), tex((ratio - 1) / ratio)],
        )


@question_type(
    "phys.posn2564_q13",
    display_name={"th": "ความเข้มแสงบนฉากก่อนจุดโฟกัส"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="เลนส์นูนและความเข้มแสง",
)
class ConvergingIntensity(PhysicsSheet):
    def expr(self, rng):
        fraction = rng.choice((Fraction(1, 4), Fraction(1, 3), Fraction(3, 5), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5)))
        focal = 60 * rng.randint(1, 2)
        screen = fraction * focal
        exact = 1 / (1 - fraction) ** 2
        answer = agree(q13.solve(fraction=float(fraction)), exact)
        return draw(
            13,
            tex(answer),
            f"แสงอาทิตย์ขนานกับแกนมุขสำคัญตกกระทบเลนส์นูนบางความยาวโฟกัส {focal} cm ผ่านเลนส์โดยไม่สะท้อนหรือถูกดูดกลืน ไปตกบนฉากที่ตั้งฉากกับแกนห่างจากเลนส์ {screen} cm ความเข้มแสงบนฉากเป็นกี่เท่าของความเข้มแสงที่ตกกระทบเลนส์",
            r"\frac{r}{r_0}=\frac{f-d}{f},\quad I\propto\frac1{r^2}",
            [tex(1 / (1 - fraction)), tex(1 / fraction), tex((fraction / (1 - fraction)) ** 2)],
        )


@question_type(
    "phys.posn2564_q14",
    display_name={"th": "อัตราส่วน ΔP/ΔV ของแก๊สอุณหภูมิคงที่"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎของบอยล์และการเปลี่ยนแปลงเล็ก",
)
class IsothermalSlope(PhysicsSheet):
    def expr(self, rng):
        pressure = rng.choice((80, 100, 120, 150, 200, 300))
        volume = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4), Fraction(5)))
        exact = -pressure / volume
        answer = agree(q14.solve(pressure=pressure, volume=float(volume)), exact)
        return draw(
            14,
            tex(answer),
            f"แก๊สอุดมคติมีความดัน {pressure} kPa ปริมาตร {show(volume)} L ถ้าเปลี่ยนสถานะเพียงเล็กน้อยโดยอุณหภูมิคงที่ ค่า ΔP/ΔV เป็นกี่ kPa/L โดยประมาณ",
            r"PV=\text{const}\Rightarrow\frac{dP}{dV}=-\frac PV",
            [tex(-exact), tex(volume / pressure), tex(-volume / pressure)],
        )


GASES = {"H₂": 2, "He": 4, "CH₄": 16, "Ne": 20, "N₂": 28, "O₂": 32, "Ar": 40, "CO₂": 44}


@question_type(
    "phys.posn2564_q15",
    display_name={"th": "อัตราส่วนอัตราเร็ว rms ของแก๊สสองชนิด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="ทฤษฎีจลน์ของแก๊ส",
)
class RmsSpeedRatio(PhysicsSheet):
    def expr(self, rng):
        asked, other = rng.sample(sorted(GASES), 2)
        ratio = Fraction(GASES[other], GASES[asked])
        agree(q15.solve(asked=GASES[asked], other=GASES[other]) ** 2, ratio)
        return draw(
            15,
            radical(ratio),
            f"แก๊สอุดมคติ {asked} (มวลโมเลกุล {GASES[asked]} g/mol) และ {other} (มวลโมเลกุล {GASES[other]} g/mol) อยู่ที่อุณหภูมิเดียวกัน อัตราเร็วรากที่สองของกำลังสองเฉลี่ย (v_rms) ของโมเลกุล {asked} เป็นกี่เท่าของโมเลกุล {other}",
            r"v_{rms}=\sqrt{3RT/M}",
            [tex(ratio), tex(ratio**2), radical(1 / ratio)],
        )


@question_type(
    "phys.posn2564_q16",
    display_name={"th": "พลังงานต่ำสุดของประจุบนวงกลม"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานศักย์ของระบบประจุ",
)
class RingChargeEnergy(PhysicsSheet):
    def expr(self, rng):
        centre = rng.randint(1, 6)
        exact = Fraction(-4 * centre + 1, 2)
        answer = agree(q16.solve(centre=centre), exact)
        label = "+e" if centre == 1 else f"+{centre}e"
        return draw(
            16,
            tex(answer),
            f"ประจุ {label} ตรึงอยู่ที่ศูนย์กลางวงกลมรัศมี r ประจุ −e สองตัวอยู่บนวงกลมนี้และเลื่อนไปตามวงได้ เมื่อจัดมุมระหว่างประจุลบให้ระบบมีพลังงานศักย์ไฟฟ้าต่ำสุด พลังงานศักย์ของทั้งระบบเป็นกี่เท่าของ ke²/r (ศักย์ที่ระยะอนันต์เป็นศูนย์)",
            r"U=\sum_{i<j}\frac{kq_iq_j}{r_{ij}}",
            [str(-2 * centre), str(-2 * centre + 1), tex(Fraction(-4 * centre - 1, 2))],
        )


CONES = ((5, 3, 4), (5, 4, 3), (13, 5, 12), (13, 12, 5), (10, 6, 8), (10, 8, 6), (17, 8, 15), (17, 15, 8))


@question_type(
    "phys.posn2564_q17",
    display_name={"th": "อัตราเร็วเชิงมุมของลูกตุ้มกรวย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แบบวงกลมของลูกตุ้มกรวย",
)
class ConicalOmega(PhysicsSheet):
    def expr(self, rng):
        length, radius, height = rng.choice(CONES)
        squared = Fraction(10, height)
        agree(q17.solve(length=length, radius=radius, g=10) ** 2, squared)
        return draw(
            17,
            radical(squared),
            f"ลูกตุ้มมวล m แขวนด้วยเชือกเบายาว {length} m เคลื่อนที่เป็นวงกลมรัศมี {radius} m ในระนาบระดับ (ลูกตุ้มกรวย) ให้ g=10 m/s² อัตราเร็วเชิงมุมของ m เป็นกี่ rad/s",
            r"T\cos\alpha=mg,\quad T\sin\alpha=m\omega^2R",
            [radical(Fraction(10, length)), tex(squared), radical(Fraction(10, radius))],
        )


@question_type(
    "phys.posn2564_q18",
    display_name={"th": "เวลาพบกันของโพรเจกไทล์ที่ยิงเข้าหากัน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเคลื่อนที่แบบโพรเจกไทล์และความเร็วสัมพัทธ์",
)
class ProjectileMeeting(PhysicsSheet):
    def expr(self, rng):
        while True:
            sine = rng.choice(SINES)
            cos = cosine(sine)
            speed = 5 * rng.randint(2, 6)
            time = Fraction(rng.randint(1, 4), 2)
            distance = 2 * speed * cos * time
            if distance.denominator == 1 and time < 2 * speed * sine / 10:
                break
        answer = agree(q18.solve(distance=int(distance), speed=speed, cosine=float(cos)), time)
        return draw(
            18,
            tex(answer),
            f"จุด A และ B อยู่บนพื้นระดับห่างกัน {distance} m ยิงโพรเจกไทล์จาก A และ B เข้าหากันพร้อมกันในระนาบดิ่งเดียวกัน ด้วยอัตราเร็วต้น {speed} m/s และมุมเงย θ₀ เท่ากัน โดย cos θ₀ = {show(cos)} ทั้งสองชนกันกลางอากาศก่อนถึงพื้น เวลาที่ชนกันหลังยิงเป็นกี่ s ให้ g=10 m/s²",
            r"y_A=y_B,\quad 2u\cos\theta_0\,t=D",
            [tex(time * 2), tex(time * cos), tex(time * 2 * cos)],
        )


LOOPS = {12: (5, 9, 16, 35), 24: (7, 10, 18, 32)}


@question_type(
    "phys.posn2564_q19",
    display_name={"th": "อัตราส่วนสนามแม่เหล็กบนแกนวงลวด"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สนามแม่เหล็กบนแกนวงลวด",
)
class LoopFieldRatio(PhysicsSheet):
    def expr(self, rng):
        radius = rng.choice(sorted(LOOPS))
        a, b = rng.sample(LOOPS[radius], 2)
        far_a, far_b = isqrt(radius * radius + a * a), isqrt(radius * radius + b * b)
        exact = Fraction(far_a, far_b) ** 3
        answer = agree(q19.solve(radius=radius, a=a, b=b), exact)
        return draw(
            19,
            tex(answer),
            f"วงลวดวงกลมรัศมี {radius} cm มีกระแส i จุด M และ N อยู่บนแกนของวงลวดคนละด้าน ห่างจากศูนย์กลาง {a} cm และ {b} cm ตามลำดับ ขนาดสนามแม่เหล็กที่จุด N เป็นกี่เท่าของที่จุด M",
            r"B=\frac{\mu_0iR^2}{2(R^2+z^2)^{3/2}}",
            [tex(1 / exact), tex(Fraction(far_a, far_b) ** 2), tex(Fraction(a, b) ** 3)],
        )


@question_type(
    "phys.posn2564_q20",
    display_name={"th": "ตัวต้านทานปลายวงจรขั้นบันได"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="วงจรตัวต้านทานแบบขั้นบันได",
)
class LadderTail(PhysicsSheet):
    def expr(self, rng):
        total = 20 * rng.randint(2, 7)
        while True:
            last = rng.randint(5, total - 5)
            if 2 * last != total:
                break
        answer = agree(q20.solve(total=total, last=last), total - last)
        half = total // 2
        return draw(
            20,
            str(answer),
            f"วงจรขั้นบันได: จากปลาย A ต่ออนุกรมตัวต้านทาน {half} Ω แล้วมีตัวต้านทาน {total} Ω ต่อลงสาย B จากนั้นต่ออนุกรม {half} Ω อีกตัวแล้วมี {total} Ω ต่อลงสาย B อีกตัว สุดท้ายต่ออนุกรม {last} Ω กับตัวต้านทาน R ลงสาย B ตัวต้านทาน R ต้องมีค่ากี่ Ω ความต้านทานรวมระหว่าง A กับ B จึงเท่ากับ {total} Ω พอดี",
            r"s+(2s\parallel 2s)=2s",
            [str(last), str(half), str(total)],
        )


@question_type(
    "phys.posn2564_q21",
    display_name={"th": "มุมตกกระทบผิวที่สองของปริซึมมุมฉาก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การหักเหและการสะท้อนกลับหมดในปริซึม",
)
class RightPrism(PhysicsSheet):
    def expr(self, rng):
        while True:
            index = rng.choice((Fraction(3, 2), Fraction(4, 3), Fraction(5, 3), Fraction(2), Fraction(8, 5)))
            sine = rng.choice(SINES[:4])
            if index**2 - sine**2 >= 1:
                break
        cos = cosine(sine)
        answer = agree(q21.solve(index=float(index), sine=float(sine)), sine / index)
        return draw(
            21,
            tex(answer),
            f"ปริซึมแก้วมุมยอด 90° มีดรรชนีหักเห {show(index)} ลำแสงตกกระทบผิวแรกด้วยมุมตกกระทบ i โดย sin i = {show(sine)} หักเหเข้าไปกระทบผิวที่สองด้วยมุม θ จากเส้นปกติแล้วสะท้อนกลับหมด cos θ มีค่าเท่าใด",
            r"\sin i=\mu\sin r,\quad r+\theta=90^\circ",
            [tex(index * sine), tex(index * cos), tex(cos / index)],
        )


@question_type(
    "phys.posn2564_q22",
    display_name={"th": "การแปลงสเกลอุณหภูมิที่สร้างเอง"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="สเกลอุณหภูมิ",
)
class CustomScale(PhysicsSheet):
    def expr(self, rng):
        ice = rng.choice((-20, -10, 10, 20))
        steam = 10 * rng.randint(10, 25)
        celsius = rng.choice((10, 20, 25, 30, 40, 50, 60, 75))
        exact = ice + Fraction((steam - ice) * celsius, 100)
        answer = agree(q22.solve(ice=ice, steam=steam, celsius=celsius), exact)
        return draw(
            22,
            tex(answer),
            f"เทอร์มอมิเตอร์สเกล °A ที่แบ่งเชิงเส้น กำหนดจุดน้ำแข็งเป็น {ice}°A และจุดน้ำเดือดเป็น {steam}°A อุณหภูมิ {celsius}°C จะอ่านได้กี่ °A",
            r"\frac{A-A_{ice}}{A_{steam}-A_{ice}}=\frac{C}{100}",
            [
                tex(Fraction((steam - ice) * celsius, 100)),
                tex(ice + Fraction(steam * celsius, 100)),
                tex(Fraction(100 * (celsius - ice), steam - ice)),
            ],
        )


@question_type(
    "phys.posn2564_q23",
    display_name={"th": "พลังงานจลน์ของแท่งที่เลื่อนและหมุน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="พลังงานจลน์การหมุน",
)
class RodKineticEnergy(PhysicsSheet):
    def expr(self, rng):
        mass = rng.choice((1, 2, 3, 4, 6))
        length = rng.randint(1, 3)
        speed = rng.randint(1, 3)
        omega = rng.randint(1, 4)
        moving = Fraction(mass * speed**2, 2)
        spin = Fraction(mass * length**2 * omega**2, 24)
        answer = agree(q23.solve(mass=mass, length=length, speed=speed, omega=omega), moving + spin)
        return draw(
            23,
            tex(answer),
            f"ท่อนโลหะผอมตรงสม่ำเสมอยาว {length} m มวล {mass} kg ถูกขว้างให้ศูนย์กลางมวลเคลื่อนที่ด้วยอัตราเร็ว {speed} m/s และหมุนรอบศูนย์กลางมวลด้วยอัตราเร็วเชิงมุม {omega} rad/s รอบแกนที่ตั้งฉากกับท่อน พลังงานจลน์รวมเป็นกี่ J",
            r"K=\tfrac12Mv^2+\tfrac12\cdot\tfrac1{12}ML^2\omega^2",
            [tex(moving), tex(moving + 4 * spin), tex(moving - spin)],
        )


@question_type(
    "phys.posn2564_q24",
    display_name={"th": "ความถี่ของคลื่นผิวความยาวคลื่นสั้น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การวิเคราะห์สมการคลื่นผิว",
)
class CapillaryScaling(PhysicsSheet):
    def expr(self, rng):
        root = rng.choice((Fraction(2), Fraction(3), Fraction(4), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 2)))
        ratio = root**2
        answer = agree(q24.solve(ratio=float(ratio)), root**3)
        return draw(
            24,
            tex(answer),
            f"อัตราเร็วคลื่นผิวน้ำเป็นไปตาม v² = λg/(2π) + 2πS/(λρ) สำหรับคลื่นที่ความยาวคลื่นสั้นมากจนตัดพจน์ λg/(2π) ได้ คลื่นที่ 1 และ 2 มีความยาวคลื่น λ₁ และ λ₂ โดย λ₁/λ₂ = {show(ratio)} ความถี่ f₂ เป็นกี่เท่าของ f₁",
            r"v^2\approx\frac{2\pi S}{\lambda\rho},\quad f=\frac v\lambda",
            [tex(ratio), tex(root), tex(ratio**2)],
        )


@question_type(
    "phys.posn2564_q25",
    display_name={"th": "มุมวิกฤตผ่านแผ่นตัวกลางหน้าขนาน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การสะท้อนกลับหมดผ่านหลายชั้น",
)
class SlabCriticalAngle(PhysicsSheet):
    def expr(self, rng):
        first, slab = rng.sample(
            (Fraction(5, 4), Fraction(4, 3), Fraction(3, 2), Fraction(5, 3), Fraction(2), Fraction(6, 5), Fraction(7, 4)), 2
        )
        answer = agree(q25.solve(mu1=float(first), mu2=float(slab)), 1 / first)
        return draw(
            25,
            tex(answer),
            f"แผ่นตัวกลางหน้าขนานดรรชนีหักเห {show(slab)} กั้นระหว่างตัวกลางดรรชนี {show(first)} กับสุญญากาศ แสงจากตัวกลางดรรชนี {show(first)} ตกกระทบแผ่นด้วยมุม θ₁ จากเส้นปกติ ผ่านแผ่นแล้วสะท้อนกลับหมดพอดีที่ผิวแผ่นด้านสุญญากาศ sin θ₁ มีค่าเท่าใด",
            r"\mu_1\sin\theta_1=\mu_2\sin\theta_2=1\cdot\sin90^\circ",
            [tex(1 / slab), tex(first / slab), tex(slab / first)],
        )


@question_type(
    "phys.posn2564_q26",
    display_name={"th": "อัตราส่วนกระแสในวงจรสองแหล่งจ่าย"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="กฎเคอร์ชอฟฟ์และขั้วแหล่งจ่าย",
)
class TwoSourceRatio(PhysicsSheet):
    def expr(self, rng):
        e2 = rng.randint(2, 12)
        e1 = e2 + rng.randint(1, 12)
        r1, r2 = rng.sample(range(1, 9), 2)
        exact = Fraction(r2 * (e1 - e2), r1 * e2)
        answer = agree(q26.solve(e1=e1, e2=e2, r1=r1, r2=r2), exact)
        return draw(
            26,
            tex(answer),
            f"แบตเตอรี่อุดมคติ ℰ₁={e1} V ต่ออนุกรมกับ R₁={r1} Ω ไปยังจุด P ส่วนแบตเตอรี่อุดมคติ ℰ₂={e2} V และตัวต้านทาน R₂={r2} Ω ต่างต่อคร่อมระหว่างจุด P กับสายร่วม ขั้วบวกของแบตเตอรี่ทั้งสองหันไปทางจุด P (ขั้วลบของ ℰ₁ ต่อกับสายร่วม) ให้ i₁ เป็นกระแสผ่าน R₁ ไปยัง P และ i₂ เป็นกระแสผ่าน R₂ จาก P ลงสายร่วม i₁/i₂ มีค่าเท่าใด",
            r"i_1=\frac{\mathcal E_1-\mathcal E_2}{R_1},\quad i_2=\frac{\mathcal E_2}{R_2}",
            [
                tex(Fraction(r2 * e1, r1 * e2)),
                tex(Fraction(r1 * (e1 - e2), r2 * e2)),
                tex(Fraction(r2 * (e1 + e2), r1 * e2)),
            ],
        )


def _gap_pool():
    pool = []
    for inside in SINES:
        for outside in SINES:
            index = outside / inside
            if outside > inside and Fraction(11, 10) <= index <= 2:
                pool.append((inside, outside, index))
    return tuple(pool)


GAPS = _gap_pool()


@question_type(
    "phys.posn2564_q27",
    display_name={"th": "ระยะเลื่อนขนานของแสงผ่านช่องอากาศ"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การเลื่อนขนานของแสงผ่านแผ่นหน้าขนาน",
)
class AirGapShift(PhysicsSheet):
    def expr(self, rng):
        sine, out_sine, index = rng.choice(GAPS)
        width = rng.choice((6, 10, 12, 15, 30))
        cos, out_cos = cosine(sine), cosine(out_sine)
        tilt = out_sine * cos - out_cos * sine
        exact = width * tilt / out_cos
        answer = agree(q27.solve(width=width, index=float(index), sine=float(sine)), exact)
        return draw(
            27,
            tex(answer),
            f"ลำแสงในก้อนน้ำแข็งดรรชนีหักเห {show(index)} ตกกระทบโพรงอากาศที่มีผิวขนานกันกว้าง {width} cm ด้วยมุม θ จากเส้นปกติ โดย sin θ = {show(sine)} ผ่านโพรงแล้วกลับเข้าน้ำแข็ง ลำแสงออกขนานกับลำแสงเข้า ระยะห่างตั้งฉากระหว่างแนวลำแสงออกกับแนวต่อของลำแสงเข้าเป็นกี่ cm (ดรรชนีอากาศเท่ากับ 1)",
            r"\sin\phi=\mu\sin\theta,\quad x=\frac{D\sin(\phi-\theta)}{\cos\phi}",
            [
                tex(width * tilt),
                tex(width * (out_sine / out_cos - sine / cos)),
                tex(width * tilt / cos),
            ],
        )


DISTANCES = {Fraction(1, 10): "0.1", Fraction(1, 5): "0.2", Fraction(2, 5): "0.4", Fraction(1, 2): "0.5", Fraction(9, 10): "0.9", Fraction(1): "1"}


@question_type(
    "phys.posn2564_q28",
    display_name={"th": "อัตราเร็วสัมพัทธ์ของประจุที่ผลักกัน"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="การอนุรักษ์พลังงานและโมเมนตัมของประจุ",
)
class RepellingCharges(PhysicsSheet):
    def expr(self, rng):
        charge = rng.randint(1, 6)
        mass = rng.choice((1, 2, 4, 5, 9, 10, 20))
        distance = rng.choice(sorted(DISTANCES))
        # k q^2 / (m D) in SI with q in uC and m in g: 9 q^2 / (m D).
        each = 9 * charge * charge / (mass * distance)
        agree(q28.solve(charge=charge, mass=mass, distance=float(distance)) ** 2, 4 * each)
        return draw(
            28,
            radical(4 * each),
            f"ทรงกลมเล็ก A และ B มีมวลเท่ากันลูกละ {mass} g และมีประจุเท่ากันลูกละ {charge} μC ปล่อยจากหยุดนิ่งที่ระยะห่าง {DISTANCES[distance]} m ให้ผลักกันโดยไม่มีแรงอื่น เมื่ออยู่ห่างกันมากๆ ขนาดความเร็วสัมพัทธ์ระหว่าง A กับ B เป็นกี่ m/s ให้ k=9×10⁹ N m²/C²",
            r"\frac{kq^2}{D}=2\cdot\tfrac12mv^2,\quad v_{rel}=2v",
            [radical(each), radical(2 * each), radical(8 * each)],
        )


@question_type(
    "phys.posn2564_q29",
    display_name={"th": "อัตราเร็วถอยของลิ่มบนพื้นลื่น"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="โมเมนตัมแนวระดับของลิ่มและมวล",
)
class WedgeRecoil(PhysicsSheet):
    def expr(self, rng):
        sine = rng.choice(SINES[:4])
        cos = cosine(sine)
        small = rng.randint(1, 3)
        big = rng.randint(small + 1, 9)
        speed = 5 * rng.randint(1, 4)
        exact = small * speed * cos / (small + big)
        answer = agree(q29.solve(small=small, big=big, speed=speed, cosine=float(cos)), exact)
        return draw(
            29,
            tex(answer),
            f"ลิ่มมวล {big} kg วางบนพื้นระดับลื่น ผิวเอียงของลิ่มลื่นและทำมุม θ กับพื้นโดย cos θ = {show(cos)} ก้อนมวล {small} kg ถูกปล่อยจากหยุดนิ่งให้ไถลลงตามผิวเอียงขณะลิ่มก็เริ่มจากหยุดนิ่ง ขณะที่ก้อนมีอัตราเร็ว {speed} m/s เทียบกับลิ่ม ลิ่มถอยหนีด้วยอัตราเร็วกี่ m/s",
            r"m(v\cos\theta-V)=MV",
            [
                tex(small * speed * cos / big),
                tex(Fraction(small * speed, small + big)),
                tex(small * speed * sine / (small + big)),
            ],
        )


@question_type(
    "phys.posn2564_q30",
    display_name={"th": "มุมยิงและอัตราเร็วต้นเมื่อชนกำแพงตั้งฉาก"},
    level=LEVEL,
    subject="ฟิสิกส์",
    topic="จุดสูงสุดของโพรเจกไทล์",
)
class WallApex(PhysicsSheet):
    def expr(self, rng):
        while True:
            width = 2 * rng.randint(5, 30)
            height = rng.randint(2, 30)
            if width != 2 * height:
                break
        slope = Fraction(2 * height, width)
        speed2 = Fraction(10 * (width**2 + 4 * height**2), 2 * height)
        # u² = u_y²(1 + 1/tan²θ) with u_y² = 2gH at the apex.
        apex = lambda tan: 20 * height * (1 + 1 / tan**2)
        assert apex(slope) == speed2
        got = q30.solve(width=width, height=height, g=10)
        agree(got[0], slope)
        agree(got[1], speed2)
        return draw(
            30,
            pair(tex(slope), tex(speed2)),
            f"ยิงโพรเจกไทล์จากจุด A บนพื้นระดับด้วยอัตราเร็วต้น u ทำมุม θ กับพื้น ไปชนกำแพงดิ่งที่อยู่ห่างจาก A ตามแนวระดับ {width} m โดยชนตั้งฉากกับกำแพงพอดีที่ความสูง {height} m จากพื้น ให้ g=10 m/s² คู่ค่า (tan θ, u²) เป็นเท่าใด โดย u² มีหน่วย m²/s²",
            r"v_y=0\text{ at the wall},\quad H=\frac{u_y^2}{2g},\quad L=\frac{u_xu_y}{g}",
            # Each slip keeps the apex height and carries its wrong angle into u².
            [
                pair(tex(slope / 2), tex(apex(slope / 2))),
                pair(tex(1 / slope), tex(apex(1 / slope))),
                pair(tex(slope), str(20 * height)),
            ],
        )
