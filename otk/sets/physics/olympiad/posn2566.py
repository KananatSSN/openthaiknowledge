"""Seeded variants of the reviewed POSN physics 2566 camp selection paper."""

from fractions import Fraction
from math import isqrt, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.posn2566_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.posn2566_physics import q11, q12, q13, q14, q15, q16, q17, q18, q19, q20

from otk.sheets.posn2566_physics import q21, q22, q23, q24, q25, q26, q27, q28

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
    """value * pi as mantissa pi x 10^n, the mantissa exact."""
    value = Fraction(value)
    power = 0
    while abs(value) >= 10:
        value, power = value / 10, power + 1
    while abs(value) < 1:
        value, power = value * 10, power - 1
    mantissa = _decimal(value) if (value * 10**6).denominator == 1 else tex(value)
    mantissa = "" if mantissa == "1" else mantissa
    return rf"{mantissa}\pi\times10^{{{power}}}"


def signed_root(sign, square):
    """sign * sqrt(square) as exact TeX."""
    if square == 0:
        return "0"
    body = radical(square)
    return body if sign > 0 else "-" + body


# sin(k pi / 6) as (sign, square), exactly.
_SIN_SQUARES = (0, Fraction(1, 4), Fraction(3, 4), 1, Fraction(3, 4), Fraction(1, 4))


def sin_sixth(k):
    k %= 12
    sign = 1 if 0 < k < 6 else (-1 if k > 6 else 0)
    return sign, _SIN_SQUARES[k % 6]


def cos_sixth(k):
    return sin_sixth(k + 3)


SLIPS = {
    1: ("phys.ring_friction_as_ma", "phys.ring_friction_as_weight", "phys.ring_friction_sign"),
    2: ("phys.release_used_static_share", "phys.release_full_weight", "phys.release_end_axis_inertia"),
    3: ("phys.explosion_angle_inverted", "phys.explosion_speeds_swapped", "phys.explosion_alpha_misplaced"),
    4: ("phys.splat_radius_time", "phys.splat_rebound", "phys.splat_rebound_radius"),
    5: ("phys.maxwell_peak_factor_two", "phys.maxwell_peak_no_root", "phys.maxwell_used_rms"),
    6: ("phys.sticking_mass_subtracted", "phys.sticking_original_mass_dropped", "phys.sticking_count_divided"),
    7: ("phys.atmosphere_disc_area", "phys.atmosphere_mass_not_divided", "phys.atmosphere_gravity_ignored"),
    8: ("phys.branch_current_used_total", "phys.branch_current_equal_split", "phys.branch_current_internal_ignored"),
    9: ("phys.standing_single_wave", "phys.standing_amplitude_halved", "phys.standing_sin_cos_swapped"),
    10: ("phys.fold_speed_same", "phys.fold_speed_halved", "phys.fold_speed_tripled"),
    11: ("phys.ice_melt_exposed_volume", "phys.ice_melt_level_drops", "phys.ice_melt_full_volume"),
    12: ("phys.ring_peak_at_radius", "phys.ring_peak_half_radius", "phys.ring_peak_root_two_radius"),
    14: ("phys.paraboloid_no_half", "phys.paraboloid_linear", "phys.paraboloid_quarter"),
    15: ("phys.focal_change_equal_radius", "phys.focal_change_multiplied", "phys.focal_change_index_on_top"),
    16: ("phys.critical_used_cosine", "phys.critical_not_rooted", "phys.critical_inverted"),
    17: ("phys.meniscus_order_ignored", "phys.meniscus_biconvex", "phys.meniscus_biconcave"),
    18: ("phys.binary_radius_swapped", "phys.binary_radius_full", "phys.binary_radius_difference"),
    19: ("phys.network_bridge_dropped", "phys.network_all_parallel", "phys.network_direct_only"),
    20: ("phys.neutrino_one_per_reaction", "phys.neutrino_per_proton", "phys.neutrino_halved"),
    21: ("phys.swept_chain_halved", "phys.swept_chain_speed_not_squared", "phys.swept_chain_doubled"),
    22: ("phys.binary_ke_no_half", "phys.binary_ke_quartered", "phys.binary_ke_one_star"),
    23: ("phys.recoil_same_energy", "phys.recoil_ratio_inverted", "phys.recoil_total_mass"),
    24: ("phys.steam_volume_celsius", "phys.steam_volume_units_omitted", "phys.steam_volume_molar_mass_dropped"),
    25: ("phys.pendulum_merge_no_root", "phys.pendulum_merge_inverted", "phys.pendulum_merge_mass_fraction"),
    26: ("phys.closest_approach_fixed_target", "phys.closest_approach_masses_swapped", "phys.closest_approach_reduced_inverted"),
    27: ("phys.plate_force_full_field", "phys.plate_force_energy_as_force", "phys.plate_force_charge_not_squared"),
    28: ("phys.plate_tilt_plate_weight_ignored", "phys.plate_tilt_cm_at_bottom", "phys.plate_tilt_hanger_depth_ignored"),
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
    sheet_id = "posn2566_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2566)"


def _type(n, title, topic):
    return question_type(
        f"phys.posn2566_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


@_type(1, "แรงเสียดทานบนวงแหวนที่ไถลลงตามเชือก", "กฎข้อสองของนิวตันกับแรงเสียดทาน")
class RingRopeFriction(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 10)
        accel = rng.randint(1, 9)
        answer = agree(q01.solve(mass=mass, accel=accel), mass * (10 - accel))
        return draw(
            1,
            str(answer),
            f"วงแหวนมวล {mass} kg สวมรอบเชือกดิ่งที่ห้อยนิ่ง วงแหวนไถลลงด้วยความเร่ง {accel} m/s² แรงเสียดทานที่เชือกกระทำต่อวงแหวนมีขนาดกี่ N ให้ g=10 m/s²",
            r"mg-f=ma",
            [str(mass * accel), str(10 * mass), str(mass * (accel - 10))],
        )


SUPPORTS = (Fraction(0), Fraction(1, 8), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3))


@_type(2, "แรงที่จุดค้ำทันทีหลังเอาอีกจุดค้ำออก", "การหมุนรอบจุดหมุนคงที่")
class PivotRelease(PhysicsSheet):
    def expr(self, rng):
        fraction = rng.choice(SUPPORTS)
        mass = rng.randint(1, 12)
        d = Fraction(1, 2) - fraction
        exact = 10 * mass * Fraction(1, 12) / (Fraction(1, 12) + d * d)
        answer = agree(q02.solve(mass=mass, fraction=float(fraction)), exact)
        where = "ที่ปลายซ้าย" if fraction == 0 else f"ห่างจากปลายซ้าย {number(fraction)}L"
        return draw(
            2,
            tex(answer),
            f"ท่อนตรงสม่ำเสมอมวล {mass} kg ยาว L วางในแนวระดับบนจุดค้ำ A {where} และจุดค้ำ B ที่ปลายขวา ทันทีที่ดึงจุดค้ำ B ออก จุดค้ำ A รับแรงกี่ N ให้ g=10 m/s²",
            r"I_A\alpha=Mgd,\quad N=M(g-\alpha d)",
            [
                tex(10 * mass * Fraction(1, 2) / (1 - fraction)),
                str(10 * mass),
                tex(10 * mass * (1 - 3 * d * d)),
            ],
        )


@_type(3, "ทิศชิ้นส่วนหลังวัตถุระเบิด", "การอนุรักษ์โมเมนตัมสองมิติ")
class ExplosionDirection(PhysicsSheet):
    def expr(self, rng):
        alpha = rng.choice((Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 5), Fraction(3, 5)))
        speed = rng.randint(2, 12)
        piece = rng.randint(2, 15)
        exact = alpha * piece / speed
        answer = agree(q03.solve(alpha=float(alpha), speed=speed, piece_speed=piece), exact)
        return draw(
            3,
            tex(answer),
            f"วัตถุมวล m เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s ตามทิศ +X แล้วระเบิดออกเป็นสองชิ้น ชิ้นมวล {number(alpha)}m เคลื่อนที่ตามทิศ +Y ด้วยอัตราเร็ว {piece} m/s อีกชิ้นเคลื่อนที่ทำมุม θ ใต้แกน +X tan θ มีค่าเท่าใด",
            r"p_x:\ mu=(1-\alpha)mv_x,\quad p_y:\ 0=\alpha mv-(1-\alpha)mv_y",
            [tex(piece / (alpha * speed)), tex(speed / (alpha * piece)), tex(alpha * speed / piece)],
        )


@_type(4, "แรงเฉลี่ยของหยดน้ำกระแทกกำแพง", "การดลและแรงเฉลี่ย")
class SplatForce(PhysicsSheet):
    def expr(self, rng):
        mass = rng.randint(1, 20)
        speed = rng.randint(2, 10)
        radius = rng.randint(1, 5)
        exact = Fraction(mass, 1000) * speed**2 / (2 * Fraction(radius, 100))
        answer = agree(q04.solve(mass=mass, speed=speed, radius=radius), exact)
        return draw(
            4,
            tex(answer),
            f"หยดน้ำทรงกลมมวล {mass} g รัศมี {radius} cm เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s ขนานพื้นเข้ากระทบกำแพงแข็งแล้วแผ่ติดกำแพงไม่กระดอน ถ้าหยดน้ำหยุดภายในเวลาที่ด้านหลังของหยดเคลื่อนมาถึงกำแพง แรงเฉลี่ยที่กำแพงกระทำต่อหยดน้ำมีขนาดกี่ N",
            r"\bar F=\frac{mv}{2r/v}",
            [tex(2 * exact), tex(4 * exact), tex(8 * exact)],
        )


@_type(5, "อัตราเร็วที่มีโมเลกุลมากที่สุด", "การกระจายอัตราเร็วของแมกซ์เวลล์")
class MaxwellPeak(PhysicsSheet):
    def expr(self, rng):
        b = rng.randint(1, 10)
        temperature = 100 * rng.randint(1, 9)
        squared = Fraction(temperature, b)
        agree(q05.solve(temperature=temperature, b=b) ** 2, squared)
        return draw(
            5,
            radical(squared),
            f"จำนวนโมเลกุลของแก๊สอุดมคติที่อุณหภูมิ T = {temperature} K ซึ่งมีอัตราเร็ว v เป็นไปตาม N(v) = Av²e^(−Bv²/T) โดย B = {b} (หน่วย SI) อัตราเร็วที่มีจำนวนโมเลกุลมากที่สุดเป็นกี่ m/s",
            r"\frac{d}{dv}\left(v^2e^{-Bv^2/T}\right)=0",
            [radical(2 * squared), tex(squared), radical(squared * Fraction(3, 2))],
        )


@_type(6, "ความเร็วหลังชนติดกันหลายครั้ง", "การชนไม่ยืดหยุ่นและโมเมนตัม")
class SuccessiveSticking(PhysicsSheet):
    def expr(self, rng):
        small = rng.randint(1, 3)
        count = rng.randint(2, 8)
        big = rng.randint(count * small + 1, count * small + 15)
        speed = rng.randint(2, 12)
        exact = Fraction(big * speed, big + count * small)
        answer = agree(q06.solve(big=big, small=small, count=count, speed=speed), exact)
        return draw(
            6,
            tex(answer),
            f"มวล {big} kg เคลื่อนที่ด้วยอัตราเร็ว {speed} m/s บนพื้นลื่น เข้าชนมวล {small} kg ที่วางเรียงอยู่นิ่งทีละลูก แบบชนแล้วติดกันไป ทันทีหลังชนลูกที่ {count} อัตราเร็วเป็นกี่ m/s",
            r"Mu=(M+Nm)v",
            [
                tex(Fraction((big - count * small) * speed, big)),
                tex(Fraction(big * speed, count * small)),
                tex(Fraction(speed, count)),
            ],
        )


@_type(7, "จำนวนโมเลกุลในบรรยากาศโลก", "ความดันบรรยากาศและน้ำหนักอากาศ")
class AtmosphereMolecules(PhysicsSheet):
    def expr(self, rng):
        radius = rng.choice((2, 3, 4, 6))  # x 10^6 m
        pressure = rng.choice((1, 2, 5, 9))  # x 10^5 Pa
        mass = rng.choice((2, 3, 4, 5))  # x 10^-26 kg
        g = rng.choice((4, 5, 10))
        r, p, m = radius * 10**6, pressure * 10**5, Fraction(mass, 10**26)
        exact = 4 * r * r * p / (g * m)  # times pi
        agree(q07.solve(pressure=p, mass=float(m), g=g, radius=r), float(exact) * pi)
        return draw(
            7,
            pi_sci(exact),
            f"ดาวเคราะห์รัศมี {radius}×10⁶ m ความเร่งโน้มถ่วงที่ผิว {g} m/s² ความดันบรรยากาศที่ผิว {pressure}×10⁵ N/m² และมวลโมเลกุลอากาศเฉลี่ย {mass}×10⁻²⁶ kg ถือว่าบรรยากาศบางเมื่อเทียบกับรัศมี จำนวนโมเลกุลในบรรยากาศทั้งหมดเป็นเท่าใด",
            r"Nmg=P\cdot4\pi R^2",
            [pi_sci(exact / 4), pi_sci(exact * m), pi_sci(exact * g)],
        )


@_type(8, "ความต้านทานที่ให้กระแสเท่ากันสองวงจร", "วงจรตัวต้านทานและความต้านทานภายใน")
class EquivalentBranch(PhysicsSheet):
    def expr(self, rng):
        internal = rng.randint(1, 6)
        other = rng.randint(1, 12)
        branch = rng.randint(1, 12)
        exact = branch + Fraction(internal * branch, other)
        answer = agree(q08.solve(internal=internal, other=other, branch=branch), exact)
        return draw(
            8,
            tex(answer),
            f"วงจร ก: แหล่งกำเนิด ℰ ความต้านทานภายใน {internal} Ω ต่อกับตัวต้านทาน {other} Ω และ {branch} Ω ที่ต่อขนานกัน กระแสผ่านตัวต้านทาน {branch} Ω เป็น I วงจร ข: แหล่งกำเนิดเดิมต่อกับตัวต้านทาน x ตัวเดียวแล้วมีกระแส I เท่ากัน x เป็นกี่ Ω",
            r"I=\frac{\mathcal E}{r+R_\parallel}\cdot\frac{R_1}{R_1+R_2}=\frac{\mathcal E}{r+x}",
            [
                tex(internal + Fraction(other * branch, other + branch)),
                str(internal + branch),
                str(branch),
            ],
        )


@_type(9, "ค่าของคลื่นนิ่งจากสองคลื่นสวนกัน", "การซ้อนทับของคลื่นและคลื่นนิ่ง")
class StandingWaveValue(PhysicsSheet):
    def expr(self, rng):
        while True:
            xs, ts = rng.randrange(12), rng.randrange(12)
            (sx, qx), (ct, qt) = sin_sixth(xs), cos_sixth(ts)
            if sx and ct:
                break
        answer = q09.solve(x_sixths=xs, t_sixths=ts)
        sign, square = sx * ct, 4 * qx * qt
        agree(answer * abs(answer), sign * square)
        angle = lambda k: "0" if k == 0 else ("π" if k == 6 else f"{number(Fraction(k, 6))}π")
        single = sin_sixth(xs - ts)
        swapped = cos_sixth(xs)[0] * sin_sixth(ts)[0], 4 * cos_sixth(xs)[1] * sin_sixth(ts)[1]
        return draw(
            9,
            signed_root(sign, square),
            f"คลื่น ψ₁(x, t) = sin(x − t) และ ψ₂(x, t) = sin(x + t) ซ้อนทับกันเป็น ψ = ψ₁ + ψ₂ ค่าของ ψ ที่ x = {angle(xs)} และ t = {angle(ts)} เป็นเท่าใด",
            r"\sin(A\pm B)=\sin A\cos B\pm\cos A\sin B",
            [signed_root(*single), signed_root(sign, square / 4), signed_root(*swapped)],
        )


@_type(10, "ความเร็วปลายเชือกที่พับซ้อน", "การเคลื่อนที่สัมพัทธ์ของเชือก")
class FoldedChain(PhysicsSheet):
    def expr(self, rng):
        fold = Fraction(rng.randint(1, 20), rng.choice((1, 2)))
        answer = agree(q10.solve(fold_speed=float(fold)), 2 * fold)
        return draw(
            10,
            tex(answer),
            f"เชือกอ่อน ABC วางบนพื้นระดับ ช่วง AB วางนิ่ง ส่วนช่วง BC พับกลับซ้อนอยู่ข้างช่วง AB โดย B เป็นจุดพับ ดึงปลาย C ไปทางขวาจนจุดพับ B เคลื่อนไปทางขวาด้วยอัตราเร็ว {number(fold)} m/s ปลาย C เคลื่อนที่ด้วยอัตราเร็วกี่ m/s",
            r"L=AB+BC=2x_B-x_C",
            [tex(fold), tex(fold / 2), tex(3 * fold)],
        )


@_type(11, "ระดับน้ำเมื่อน้ำแข็งลอยละลาย", "หลักของอาร์คิมีดีสกับการละลาย")
class FloatingIceMelt(PhysicsSheet):
    def expr(self, rng):
        liquid = rng.choice((Fraction(1), Fraction(23, 20), Fraction(6, 5), Fraction(5, 4)))
        ice = rng.choice((Fraction(9, 10), Fraction(23, 25)))
        volume = 100 * rng.randint(1, 5)
        area = rng.choice((50, 100, 200))
        mass = ice * volume
        exact = mass * (1 - 1 / liquid) / area
        answer = agree(q11.solve(ice_density=float(ice), volume=volume, area=area, liquid=float(liquid)), exact)
        exposed = volume * (1 - ice / liquid) / area
        kind = "น้ำ (1 g/cm³)" if liquid == 1 else f"น้ำเกลือความหนาแน่น {number(liquid)} g/cm³"
        return draw(
            11,
            tex(answer),
            f"น้ำแข็งความหนาแน่น {number(ice)} g/cm³ ปริมาตร {volume} cm³ ลอยนิ่งใน{kind} ในถ้วยทรงกระบอกพื้นที่หน้าตัด {area} cm² เมื่อน้ำแข็งละลายเป็นน้ำจืด (1 g/cm³) หมดและไม่คิดการเปลี่ยนปริมาตรจากการผสม ระดับของเหลวในถ้วยสูงขึ้นกี่ cm (ตอบเป็นลบถ้าลดลง)",
            r"V_{sub}=\frac{m}{\rho_l},\quad V_{melt}=\frac{m}{\rho_w}",
            [tex(exposed), tex(-exposed), tex(Fraction(volume, area))],
        )


@_type(12, "ตำแหน่งที่สนามบนแกนวงแหวนสูงสุด", "การอินทิเกรตสนามและสมมาตร")
class RingFieldPeak(PhysicsSheet):
    def expr(self, rng):
        radius = rng.randint(1, 30)
        squared = Fraction(radius * radius, 2)
        agree(q12.solve(radius=radius) ** 2, squared)
        return draw(
            12,
            radical(squared),
            f"วงแหวนรัศมี {radius} cm อยู่ในระนาบ YZ มีศูนย์กลางที่ O และมีประจุบวกกระจายสม่ำเสมอ บนแกน X ขนาดสนามไฟฟ้ามีค่ามากที่สุดที่ระยะห่างจาก O กี่ cm",
            r"E(x)\propto\frac{x}{(x^2+R^2)^{3/2}}",
            [str(radius), tex(Fraction(radius, 2)), radical(2 * radius * radius)],
        )


SHAPES = {
    "rise_to_constant": "เพิ่มจากศูนย์แล้วเข้าหาค่าคงที่ค่าหนึ่ง",
    "rise_then_decay": "เพิ่มจากศูนย์ถึงค่าสูงสุดแล้วลดลงเข้าหาศูนย์",
    "damped": "ขึ้นแล้วลงต่ำกว่าศูนย์แบบแกว่งหน่วงก่อนเข้าหาศูนย์",
    "sustained": "แกว่งขึ้นลงรอบศูนย์ด้วยแอมพลิจูดคงที่",
}
WHICH = {
    "starred": "ตัวเก็บประจุ C* ที่ต่อขนานกับตัวต้านทานตัวล่าง",
    "series": "ตัวเก็บประจุ C ที่ต่ออนุกรมกับแหล่งกำเนิด",
}


@_type(13, "ประจุในตัวเก็บประจุของวงจร RC สองชั้น", "วงจร RC ในสภาวะชั่วครู่")
class RcLadderShape(ChoiceType):
    sheet_id = "posn2566_physics"
    sheet = "สอวน. ค่าย 1 ฟิสิกส์ (2566)"

    def compose(self, rng):
        which = rng.choice(sorted(WHICH))
        shape = q13.solve(capacitor=which)
        wrongs = tuple(named(f"phys.rc_shape_{other}", SHAPES[other]) for other in SHAPES if other != shape)
        return (
            "แหล่งกำเนิด ℰ ต่ออนุกรมกับตัวต้านทาน R และตัวเก็บประจุ C ไปยังจุด P จากจุด P มีตัวต้านทาน R และตัวเก็บประจุ C* ต่อขนานกันลงสายล่าง "
            "และมีสวิตช์บนสายล่าง เริ่มต้นไม่มีประจุในตัวเก็บประจุใดเลย สับสวิตช์ที่ t = 0 "
            f"ประจุใน{WHICH[which]} เปลี่ยนตามเวลาอย่างไร",
            SHAPES[shape],
            wrongs,
        )


@_type(14, "ผิวน้ำในภาชนะที่หมุน", "ของไหลในกรอบหมุน")
class RotatingSurface(PhysicsSheet):
    def expr(self, rng):
        omega = rng.randint(2, 20)
        cup = rng.randint(5, 15)
        x = rng.randint(1, cup - 1)
        exact = Fraction(omega * omega * x * x, 2000)
        answer = agree(q14.solve(omega=omega, radius=x), exact)
        return draw(
            14,
            tex(answer),
            f"ถ้วยทรงกระบอกรัศมี {cup} cm บรรจุน้ำหมุนรอบแกนกลางพร้อมกับน้ำด้วยอัตราเร็วเชิงมุม {omega} rad/s จนผิวน้ำคงรูป ที่ระยะ {x} cm จากแกน ผิวน้ำสูงกว่าผิวน้ำที่แกนกี่ cm ให้ g=10 m/s²",
            r"\frac{dy}{dx}=\frac{\omega^2x}{g}",
            [tex(2 * exact), tex(Fraction(omega * omega * cup * x, 2000)), tex(exact / 2)],
        )


@_type(15, "การเปลี่ยนโฟกัสเมื่อรัศมีความโค้งเปลี่ยน", "สูตรผู้สร้างเลนส์")
class FocalSensitivity(PhysicsSheet):
    def expr(self, rng):
        index = rng.choice((Fraction(3, 2), Fraction(8, 5), Fraction(5, 4), Fraction(7, 4), Fraction(2)))
        radius = 5 * rng.randint(2, 8)
        change = Fraction(rng.randint(1, 9), 10)
        exact = change / (index - 1)
        answer = agree(q15.solve(index=float(index), radius=radius, change=float(change)), exact)
        return draw(
            15,
            tex(answer),
            f"เลนส์นูนแกมราบดรรชนีหักเห {number(index)} ผิวโค้งรัศมี {radius} cm มี 1/f = (μ − 1)/R ถ้ารัศมีความโค้งเพิ่มขึ้นเล็กน้อย {number(change)} cm ความยาวโฟกัสเพิ่มขึ้นประมาณกี่ cm",
            r"f=\frac{R}{\mu-1},\quad\Delta f=\frac{\Delta R}{\mu-1}",
            [tex(change), tex(change * (index - 1)), tex(change * index / (index - 1))],
        )


INCIDENCE = {30: (Fraction(1, 4), Fraction(3, 4)), 45: (Fraction(1, 2), Fraction(1, 2)), 60: (Fraction(3, 4), Fraction(1, 4))}


@_type(16, "ดรรชนีต่ำสุดของปริซึมสะท้อนกลับหมด", "การสะท้อนกลับหมด")
class MinimumIndex(PhysicsSheet):
    def expr(self, rng):
        angle = rng.choice(sorted(INCIDENCE))
        sin2, cos2 = INCIDENCE[angle]
        agree(q16.solve(angle=angle) ** 2, 1 / sin2)
        return draw(
            16,
            radical(1 / sin2),
            f"แสงในปริซึมใสตกกระทบผิวสะท้อนด้านในด้วยมุมตกกระทบ {angle}° (วัดจากเส้นปกติ) ต้องการให้แสงสะท้อนกลับหมดที่ผิวนี้ (อากาศอยู่ด้านนอก) ดรรชนีหักเหของปริซึมต้องมีค่าอย่างน้อยเท่าใด",
            r"\sin\theta_c=\frac1\mu\le\sin\varphi",
            [radical(1 / cos2), tex(1 / sin2), radical(sin2)],
        )


@_type(17, "ความยาวโฟกัสของเลนส์ที่กลับผิว", "สูตรผู้สร้างเลนส์")
class SwappedMeniscus(PhysicsSheet):
    def expr(self, rng):
        index = rng.choice((Fraction(3, 2), Fraction(8, 5), Fraction(5, 4)))
        first = 5 * rng.randint(1, 4)
        second = first * rng.randint(2, 4)
        diff, total = Fraction(1, first) - Fraction(1, second), Fraction(1, first) + Fraction(1, second)
        exact = 1 / ((1 - index) * diff)
        answer = agree(q17.solve(index=float(index), first=first, second=second), exact)
        return draw(
            17,
            tex(answer),
            f"เลนส์ A เป็นเลนส์นูนแบบเมนิสคัสดรรชนี {number(index)} ผิวซ้ายรัศมี R₁ = {first} cm ผิวขวารัศมี R₂ = {second} cm (ศูนย์กลางความโค้งทั้งสองอยู่ทางขวา) มี 1/f_A = (μ − 1)(1/R₁ − 1/R₂) "
            "เลนส์ B ใช้ผิวทั้งสองเดิมแต่สลับลำดับ ผิวซ้ายรัศมี R₂ ผิวขวารัศมี R₁ โดยยังโค้งไปทางเดียวกัน (หนาที่ขอบ) ความยาวโฟกัส f_B เป็นกี่ cm (ค่าลบหมายถึงเลนส์เว้า)",
            r"\frac1f=(\mu-1)\left(\frac1{r_1}-\frac1{r_2}\right)",
            [tex(-exact), tex(1 / ((index - 1) * total)), tex(1 / ((1 - index) * total))],
        )


@_type(18, "รัศมีวงโคจรในระบบดาวคู่", "ศูนย์กลางมวลของระบบสองวัตถุ")
class BinaryRadius(PhysicsSheet):
    def expr(self, rng):
        small = rng.randint(1, 5)
        big = rng.randint(small + 1, 12)
        separation = rng.randint(2, 20)
        exact = Fraction(big * separation, big + small)
        answer = agree(q18.solve(big=big, small=small, separation=separation), exact)
        return draw(
            18,
            tex(answer),
            f"ดาวมวล {big} และ {small} เท่าของมวลดวงอาทิตย์อยู่ห่างกัน {separation} AU คงที่ และโคจรรอบศูนย์กลางมวลร่วม รัศมีวงโคจรของดาวมวล {small} เท่าเป็นกี่ AU",
            r"r_m=\frac{M}{M+m}R",
            [tex(Fraction(small * separation, big + small)), str(separation), tex(Fraction((big - small) * separation, big + small))],
        )


def _network(aq, qs, sb, qb, as_, ab):
    g = [Fraction(1, v) if v else Fraction(0) for v in (aq, qs, sb, qb, as_, ab)]
    gaq, gqs, gsb, gqb, gas, gab = g
    a11, a12, b1 = gaq + gqs + gqb, -gqs, gaq
    a21, a22, b2 = -gqs, gas + gqs + gsb, gas
    det = a11 * a22 - a12 * a21
    q = (b1 * a22 - a12 * b2) / det
    s = (a11 * b2 - b1 * a21) / det
    return 1 / ((1 - q) * gaq + (1 - s) * gas + gab)


@_type(19, "ความต้านทานรวมของวงจรสี่จุดต่อครบ", "วงจรตัวต้านทานที่ไม่ใช่อนุกรมขนาน")
class CompleteNetwork(PhysicsSheet):
    def expr(self, rng):
        values = [rng.choice((1, 2, 3, 4, 6, 12)) for _ in range(6)]
        aq, qs, sb, qb, as_, ab = values
        answer = q19.solve(aq=aq, qs=qs, sb=sb, qb=qb, as_=as_, ab=ab)
        dropped = _network(aq, 0, sb, qb, as_, ab)
        everything = 1 / sum(Fraction(1, v) for v in values)
        return draw(
            19,
            tex(answer),
            f"จุด A, Q, S, B ต่อถึงกันด้วยตัวต้านทานครบทุกคู่: A–Q {aq} Ω, Q–S {qs} Ω, S–B {sb} Ω, Q–B {qb} Ω, A–S {as_} Ω และ A–B {ab} Ω ความต้านทานรวมระหว่าง A กับ B เป็นกี่ Ω",
            r"\text{node equations at Q and S}",
            [tex(dropped), tex(everything), str(ab)],
        )


@_type(20, "จำนวนนิวตริโนจากดวงอาทิตย์ต่อวินาที", "พลังงานนิวเคลียร์และฟิวชัน")
class NeutrinoRate(PhysicsSheet):
    def expr(self, rng):
        power = rng.choice((2, 3, 4, 5, 6, 8))  # x 10^26 W
        energy = rng.choice((2, 4, 5))  # x 10^-12 J per chain
        exact = 2 * Fraction(power * 10**26) / Fraction(energy, 10**12)
        answer = agree(q20.solve(power=power * 1e26, energy=energy * 1e-12), exact)
        return draw(
            20,
            sci(answer, force=True),
            f"ดาวฤกษ์ดวงหนึ่งปล่อยพลังงาน {power}×10²⁶ J ต่อวินาทีจากปฏิกิริยา 4 ¹H → ⁴He + 2e⁺ + 2γ + 2ν ซึ่งแต่ละครั้งปล่อยพลังงาน {energy}×10⁻¹² J ดาวดวงนี้ปล่อยนิวตริโนกี่อนุภาคต่อวินาที",
            r"\frac{P}{E}\times2",
            [sci(exact / 2, force=True), sci(exact * 2, force=True), sci(exact / 4, force=True)],
        )


@_type(21, "แรงที่ใช้กวาดโซ่ด้วยความเร็วคงที่", "ระบบมวลแปรเปลี่ยน")
class SweptChain(PhysicsSheet):
    def expr(self, rng):
        density = Fraction(rng.randint(1, 20), 10)
        speed = rng.randint(1, 10)
        exact = density * speed**2
        answer = agree(q21.solve(density=float(density), speed=speed), exact)
        return draw(
            21,
            tex(answer),
            f"โซ่มวลต่อหน่วยความยาว {number(density)} kg/m วางเป็นแนวตรงบนพื้นระดับลื่น มือกวาดโซ่ไปตามแนวโซ่ด้วยความเร็วคงที่ {speed} m/s โดยข้อโซ่ที่ถูกกวาดเปลี่ยนจากหยุดนิ่งมาเคลื่อนพร้อมมือ แรงที่โซ่กระทำต่อมือมีขนาดกี่ N",
            r"F=\frac{dp}{dt}=\lambda v\cdot v",
            [tex(exact / 2), tex(density * speed), tex(2 * exact)],
        )


@_type(22, "พลังงานจลน์ของระบบดาวคู่", "กฎความโน้มถ่วงสากลและวงโคจร")
class BinaryEnergy(PhysicsSheet):
    def expr(self, rng):
        big = rng.randint(2, 12)
        small = rng.randint(1, big)
        separation = rng.randint(1, 10)
        exact = Fraction(big * small, 2 * separation)
        answer = agree(q22.solve(big=big, small=small, separation=separation), exact)
        return draw(
            22,
            tex(answer),
            f"วัตถุทรงกลมเล็กมวล {big} kg และ {small} kg อยู่ห่างกัน {separation} m คงที่ และโคจรรอบศูนย์กลางมวลร่วมด้วยอัตราเร็วเชิงมุมคงที่ภายใต้แรงโน้มถ่วงระหว่างกันเท่านั้น พลังงานจลน์รวมเป็นกี่เท่าของ G (หน่วย SI)",
            r"\omega^2=\frac{G(M+m)}{R^3}",
            [tex(2 * exact), tex(exact / 2), tex(exact * big / (big + small))],
        )


DAUGHTERS = (206, 210, 222, 226, 230, 234)


@_type(23, "พลังงานจลน์ของนิวเคลียสที่สะท้อนกลับ", "โมเมนตัมในการสลายตัว")
class AlphaRecoil(PhysicsSheet):
    def expr(self, rng):
        daughter = rng.choice(DAUGHTERS)
        energy = Fraction(rng.randint(40, 80), 10)
        exact = 4 * energy / daughter
        answer = agree(q23.solve(daughter=daughter, energy=float(energy)), exact)
        return draw(
            23,
            tex(answer),
            f"นิวเคลียสกัมมันตรังสีที่อยู่นิ่งปล่อยอนุภาคแอลฟามวล 4 u ด้วยพลังงานจลน์ {number(energy)} MeV แล้วเหลือนิวเคลียสใหม่มวล {daughter} u ซึ่งเด้งถอยกลับ พลังงานจลน์ของนิวเคลียสใหม่เป็นกี่ MeV (ใช้กลศาสตร์แบบดั้งเดิม)",
            r"p_\alpha=p_M,\quad K=\frac{p^2}{2m}",
            [tex(energy), tex(energy * daughter / 4), tex(4 * energy / (daughter + 4))],
        )


@_type(24, "ปริมาตรไอน้ำจากน้ำเหลว", "กฎแก๊สอุดมคติกับการเปลี่ยนสถานะ")
class SteamFromWater(PhysicsSheet):
    def expr(self, rng):
        volume = rng.randint(1, 5)
        celsius = rng.choice((87, 177, 267, 357, 447, 627))
        pressure = rng.choice((1, 2))
        exact = Fraction(volume, 18) * Fraction(83, 10) * (celsius + 273) / (pressure * 10**5) * 10**6
        answer = agree(q24.solve(volume=volume, celsius=celsius, pressure=pressure * 1e5), exact)
        celsius_form = Fraction(volume, 18) * Fraction(83, 10) * celsius / (pressure * 10**5) * 10**6
        return draw(
            24,
            sci(answer),
            f"น้ำเหลว {volume} cm³ (1 g/cm³ มวลโมเลกุล 18 g/mol) กลายเป็นไอน้ำทั้งหมดที่อุณหภูมิ {celsius} °C ภายใต้ความดัน {pressure}×10⁵ N/m² ถือว่าไอน้ำเป็นแก๊สอุดมคติ ปริมาตรไอน้ำเป็นประมาณกี่ cm³ ใช้ R = 8.3 J K⁻¹ mol⁻¹",
            r"V=\frac{nRT}{P},\quad n=\frac{m}{18}",
            [sci(celsius_form), sci(exact / 10**6), sci(exact * 18)],
        )


DROP_COSINES = (Fraction(3, 4), Fraction(8, 9), Fraction(5, 9), Fraction(7, 16), Fraction(24, 25), Fraction(16, 25))


@_type(25, "อัตราส่วนมวลลูกตุ้มที่ชนแล้วติดกัน", "การชนไม่ยืดหยุ่นร่วมกับพลังงาน")
class PendulumMerge(PhysicsSheet):
    def expr(self, rng):
        cos = rng.choice(DROP_COSINES)
        drop = 1 - cos
        share = Fraction(isqrt(drop.numerator), isqrt(drop.denominator))
        assert share * share == drop
        exact = share / (1 - share)
        answer = agree(q25.solve(cosine=float(cos)), exact)
        return draw(
            25,
            tex(answer),
            f"ปล่อยลูกตุ้มมวล M จากหยุดนิ่งโดยเชือกอยู่ในแนวระดับระดับเดียวกับจุดแขวน ให้แกว่งลงมาชนมวล m ที่วางนิ่งบนพื้นลื่นใต้จุดแขวน ชนแล้วติดกันไปและแกว่งขึ้นได้สูงสุดเมื่อเชือกทำมุม θ กับแนวดิ่ง โดย cos θ = {number(cos)} อัตราส่วน M/m เป็นเท่าใด",
            r"v_0^2=2gL,\quad V=\frac{Mv_0}{M+m},\quad V^2=2gL(1-\cos\theta)",
            [tex(drop / (1 - drop)), tex((1 - share) / share), tex(share)],
        )


@_type(26, "พลังงานจลน์ที่ต้องใช้เข้าใกล้ประจุที่เคลื่อนได้", "การอนุรักษ์พลังงานและโมเมนตัมของประจุ")
class FreeTargetApproach(PhysicsSheet):
    def expr(self, rng):
        q, big_q = rng.randint(1, 5), rng.randint(1, 10)
        distance = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1)))
        small, big = rng.randint(1, 4), rng.randint(1, 8)
        base = Fraction(9 * q * big_q, 1000) / distance
        exact = base * (1 + Fraction(small, big))
        answer = agree(
            q26.solve(small_charge=q, big_charge=big_q, distance=float(distance), small=small, big=big), exact
        )
        return draw(
            26,
            tex(answer),
            f"ยิงประจุ +{q} μC มวล {small} kg จากระยะไกลมากเข้าหาประจุ +{big_q} μC มวล {big} kg ซึ่งเริ่มอยู่นิ่งและเคลื่อนที่ได้อิสระ ไม่มีแรงอื่น ต้องการให้เข้าใกล้กันที่สุดเป็นระยะ {number(distance)} m ประจุที่ยิงต้องมีพลังงานจลน์เริ่มต้นกี่ J ให้ k=9×10⁹ N m²/C²",
            r"mu=(m+M)V,\quad\tfrac12mu^2-\tfrac12(m+M)V^2=\frac{kqQ}D",
            [tex(base), tex(base * (1 + Fraction(big, small))), tex(base * Fraction(big, small + big))],
        )


@_type(27, "แรงดึงดูดระหว่างแผ่นตัวเก็บประจุ", "แรงในตัวเก็บประจุแผ่นขนาน")
class PlateForce(PhysicsSheet):
    def expr(self, rng):
        cap = rng.choice((10, 20, 50, 100, 200))  # pF
        emf = 100 * rng.randint(1, 30)
        gap = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2)))  # mm
        c, d = Fraction(cap, 10**12), gap / 1000
        exact = c * emf**2 / (2 * d)
        answer = agree(q27.solve(capacitance=cap, emf=emf, gap=float(gap)), exact)
        return draw(
            27,
            sci(answer, force=True),
            f"ตัวเก็บประจุแผ่นขนานความจุ {cap} pF แผ่นห่างกัน {number(gap)} mm ต่อกับแหล่งกำเนิดแรงเคลื่อน {emf} V แผ่นทั้งสองดึงดูดกันด้วยแรงกี่ N",
            r"F=Q\cdot\frac{E}{2},\quad Q=C\varepsilon,\quad E=\frac{\varepsilon}{d}",
            [sci(2 * exact, force=True), sci(c * emf**2 / 2, force=True), sci(c * emf / (2 * d), force=True)],
        )


@_type(28, "มุมเอียงของแผ่นที่ห้อยมวลที่มุม", "สมดุลโมเมนต์ของวัตถุแข็งเกร็ง")
class HangingPlateTilt(PhysicsSheet):
    def expr(self, rng):
        plate = rng.randint(1, 10)
        hung = rng.randint(1, 5)
        length = 10 * rng.randint(2, 8)
        width = 5 * rng.randint(1, 6)
        exact = Fraction(hung * length, width * (plate + 2 * hung))
        answer = agree(q28.solve(plate=plate, hung=hung, length=length, width=width), exact)
        return draw(
            28,
            tex(answer),
            f"แผ่นสี่เหลี่ยมมุมฉากสม่ำเสมอมวล {plate} kg ยาว {length} cm กว้าง {width} cm แขวนด้วยเชือกที่จุด A กึ่งกลางขอบบน แล้วห้อยมวล {hung} kg ที่มุมล่าง B ปลายด้านหนึ่ง แผ่นจึงเอียงทำมุม θ กับแนวระดับ (ด้าน B ต่ำลง) tan θ มีค่าเท่าใด",
            r"Mg\frac b2\sin\theta=mg\left(\frac L2\cos\theta-b\sin\theta\right)",
            [
                tex(Fraction(length, 2 * width)),
                tex(Fraction(hung * length, 2 * width * (plate + hung))),
                tex(Fraction(hung * length, width * plate)),
            ],
        )
