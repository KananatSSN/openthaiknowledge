"""Seeded variants of the reviewed TPhO 5 (2549) national physics olympiad."""

from fractions import Fraction
from math import floor, isqrt, log10, pi, radians, sin, sqrt

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2549_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2549_physics import q11, q12, q13, q14

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
    1: ("phys.lens_pair_separation_not_added", "phys.lens_pair_effective_focal_used", "phys.lens_pair_sign"),
    2: ("phys.rolling_friction_sliding_block", "phys.rolling_friction_inertia_ratio_only", "phys.rolling_friction_ratio_inverted"),
    3: ("phys.loop_rotation_ignored", "phys.loop_top_speed_zero", "phys.loop_cylinder_inertia"),
    4: ("phys.loop_rotation_ignored", "phys.loop_side_weight_added", "phys.loop_height_from_ground"),
    5: ("phys.diving_bell_water_column_ignored", "phys.diving_bell_boyle_inverted", "phys.diving_bell_depth_to_top"),
    6: ("phys.air_added_total_ratio", "phys.air_added_top_pressure", "phys.air_added_inside_level_pressure"),
    7: ("phys.tank_half_volume", "phys.tank_depth_used", "phys.tank_weight_as_mass"),
    8: ("phys.thomson_omega_not_rooted", "phys.thomson_radius_squared", "phys.thomson_field_third_dropped"),
    9: ("phys.thomson_angular_frequency_as_f", "phys.thomson_cube_root_as_square", "phys.thomson_four_pi_dropped"),
    10: ("phys.thomson_pair_distance_not_doubled", "phys.equilibrium_cube_as_square", "phys.thomson_separation_reported"),
    11: ("phys.thomson_pair_repulsion_ignored", "phys.frequency_angular_confused", "phys.thomson_repulsion_stiffness_halved"),
    12: ("phys.prism_halves_dropped", "phys.prism_angles_as_ratio", "phys.prism_apex_not_halved"),
    13: ("phys.steelyard_zero_ignored", "phys.steelyard_lever_inverted", "phys.steelyard_offset_added"),
    14: ("phys.specific_gravity_inverted", "phys.specific_gravity_apparent_ratio", "phys.specific_gravity_air_weight_used"),
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


SHEET = "ฟิสิกส์โอลิมปิก สอวน. ครั้งที่ 5 (2549)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2549_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2549_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


@_type(1, "ตำแหน่งโฟกัสของเลนส์นูนคู่เลนส์เว้า", "เลนส์บางสองอันต่อกัน")
class LensPairFocus(PhysicsSheet):
    def _variant(self, rng):
        focal = rng.randint(10, 40)
        gap = rng.randint(1, focal - 1)
        exact = Fraction(focal * (focal - gap), gap) + gap
        agree(q01.solve(focal=focal, gap=gap), exact)
        return draw(
            1,
            tex(exact),
            f"เลนส์นูนและเลนส์เว้าบางมีความยาวโฟกัส {focal} cm เท่ากัน วางบนแกนเดียวกันห่างกัน {gap} cm แสงขนานเข้าทางเลนส์นูนก่อน จุดโฟกัสของเลนส์ประกอบอยู่ห่างจากเลนส์นูนกี่เซนติเมตร",
            r"v=f,\ u'=L-f,\ \frac1{u'}+\frac1{v'}=-\frac1f",
            [tex(Fraction(focal * (focal - gap), gap)), tex(Fraction(focal * focal, gap)), tex(Fraction(focal * (focal + gap), gap) + gap)],
        )


SHAPES = ((Fraction(1, 2), "ทรงกระบอกตัน"), (Fraction(2, 5), "ทรงกลมตัน"), (Fraction(1), "ห่วงวงกลมบาง"))
SLOPES = (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4), Fraction(1), Fraction(4, 3))


@_type(2, "สัมประสิทธิ์ความเสียดทานน้อยสุดสำหรับการกลิ้ง", "สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง")
class RollingFriction(PhysicsSheet):
    def _variant(self, rng):
        k, name = rng.choice(SHAPES)
        slope = rng.choice(SLOPES)
        exact = slope * k / (1 + k)
        agree(q02.solve(slope=float(slope), shape=float(k)), exact)
        return draw(
            2,
            tex(exact),
            f"{name} (I = {number(k)}mR²) กลิ้งจากหยุดนิ่งลงตามพื้นเอียงที่ tan θ = {number(slope)} สัมประสิทธิ์ความเสียดทานสถิตต้องมีค่าอย่างน้อยเท่าใดจึงกลิ้งโดยไม่ไถล",
            r"mg\sin\theta-f=ma,\quad fR=I\frac aR,\quad f\le\mu mg\cos\theta",
            [tex(slope), tex(slope * k), tex(slope / (1 + k))],
        )


@_type(3, "ความสูงน้อยสุดที่ทรงกลมกลิ้งผ่านรางวงกลม", "พลังงานการเลื่อนที่ร่วมการหมุน")
class LoopHeight(PhysicsSheet):
    def _variant(self, rng):
        loop = Fraction(rng.randint(2, 30), 10)
        exact = Fraction(27, 10) * loop
        agree(q03.solve(loop=float(loop)), exact)
        return draw(
            3,
            tex(exact),
            f"ทรงกลมตันเล็ก ๆ (รัศมีเล็กมากเทียบกับราง) กลิ้งโดยไม่ไถลจากหยุดนิ่งที่ความสูง h ลงมาตามรางที่ตอนปลายเป็นวงกลมในแนวดิ่งรัศมี {number(loop)} m h ต้องมีค่าน้อยที่สุดกี่เมตรจึงเคลื่อนที่ไปตามรางวงกลมได้ตลอด",
            r"\frac{mv^2}{R}=mg,\quad mgh=\tfrac7{10}mv^2+2mgR",
            [tex(Fraction(5, 2) * loop), tex(2 * loop), tex(Fraction(11, 4) * loop)],
        )


@_type(4, "แรงปฏิกิริยาที่ข้างรางวงกลม", "พลังงานการเลื่อนที่ร่วมการหมุน")
class LoopSideNormal(PhysicsSheet):
    def _variant(self, rng):
        mass = Fraction(rng.randint(1, 10), 10)
        loop = Fraction(rng.randint(2, 20), 10)
        height = Fraction(rng.randint(27, 50), 10) * loop
        exact = Fraction(10, 7) * 10 * mass * (height - loop) / loop
        agree(q04.solve(mass=float(mass), loop=float(loop), height=float(height)), exact)
        return draw(
            4,
            tex(exact),
            f"ทรงกลมตันเล็ก ๆ มวล {number(mass)} kg กลิ้งโดยไม่ไถลจากหยุดนิ่งที่ความสูง {number(height)} m ลงมาตามรางที่ตอนปลายเป็นวงกลมในแนวดิ่งรัศมี {number(loop)} m แรงปฏิกิริยาจากรางที่จุดซึ่งอยู่ระดับเดียวกับศูนย์กลางวงกลมเป็นกี่นิวตัน (g = 10 m/s²)",
            r"N=\frac{mv^2}{R},\quad mg(h-R)=\tfrac7{10}mv^2",
            [tex(2 * 10 * mass * (height - loop) / loop), tex(exact + 10 * mass), tex(Fraction(10, 7) * 10 * mass * height / loop)],
        )


FILLS = (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))
PA, RHO_G = 101300, 10000


def _bell(rng):
    length = rng.randint(4, 12)
    fill = rng.choice(FILLS)
    depth = fill * length + fill * Fraction(PA, RHO_G) / (1 - fill)
    return length, fill, depth


BELL = "ถังเหล็กทรงกระบอกสูง {length} m ถูกคว่ำแล้วหย่อนลงในแม่น้ำจนถึงก้นแม่น้ำ พบว่ามีน้ำเข้าไป {fill} ของถัง (อุณหภูมิคงที่ ความดันบรรยากาศ 1.013×10⁵ Pa, ρg ของน้ำ = 1.0×10⁴ N/m³)"


@_type(5, "ความลึกของแม่น้ำจากระดับน้ำในถังคว่ำ", "กฎของบอยล์กับความดันของของเหลว")
class DivingBellDepth(PhysicsSheet):
    def _variant(self, rng):
        length, fill, depth = _bell(rng)
        value = q05.solve(length=length, fraction=float(fill))
        agree(value, depth)
        tail = fill * Fraction(PA, RHO_G) / (1 - fill)
        return draw(
            5,
            measure(value),
            BELL.format(length=length, fill=number(fill)) + " แม่น้ำลึกกี่เมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_aLA=\left(P_a+\rho g(h-kL)\right)(1-k)LA",
            [measure(float(tail)), measure(float(fill * length + (1 - fill) * Fraction(PA, RHO_G) / fill)), measure(float(length + tail))],
        )


@_type(6, "อากาศที่ต้องเติมเพื่อไล่น้ำออกจากถัง", "กฎของบอยล์กับความดันของของเหลว")
class DivingBellAir(PhysicsSheet):
    def _variant(self, rng):
        length, fill, depth = _bell(rng)
        value = q06.solve(length=length, fraction=float(fill))
        agree(value, RHO_G * depth / PA)
        return draw(
            6,
            measure(value),
            BELL.format(length=length, fill=number(fill)) + " ต้องเติมอากาศเพิ่มเป็นมวลอีกกี่เท่าของอากาศเดิมในถัง จึงไล่น้ำออกจากถังได้หมด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{n_3}{n_1}=\frac{P_a+\rho gh}{P_a}",
            [
                measure(float((PA + RHO_G * depth) / PA)),
                measure(float(RHO_G * (depth - length) / PA)),
                measure(float(RHO_G * (depth - fill * length) / PA)),
            ],
        )


@_type(7, "มวลน้อยสุดของถังคว่ำที่ก้นแม่น้ำ", "กฎของบอยล์กับความดันของของเหลว")
class DivingBellMass(PhysicsSheet):
    def _variant(self, rng):
        length, fill, depth = _bell(rng)
        area = Fraction(rng.randint(2, 20), 2)
        exact = 1000 * length * area
        agree(q07.solve(length=length, area=float(area)), exact)
        return draw(
            7,
            measure(float(exact)),
            f"ถังเหล็กทรงกระบอกสูง {length} m พื้นที่หน้าตัด {number(area)} m² คว่ำอยู่ที่ก้นแม่น้ำลึก {measure(float(depth))} m โดยภายในเป็นอากาศทั้งหมด (ไม่มีน้ำ) ถังต้องมีมวลอย่างน้อยกี่กิโลกรัมจึงอยู่ได้โดยไม่ต้องกดไว้ (ไม่คิดปริมาตรเนื้อเหล็ก ρ = 1000 kg/m³, g = 10 m/s²)",
            r"\left[(P_a+\rho gh)-(P_a+\rho g(h-L))\right]A=mg",
            [measure(float(exact / 2)), measure(float(1000 * depth * area)), measure(float(exact * 10))],
        )


E, ME, EPS0, C = 1.6e-19, 9.1e-31, 8.85e-12, 3.0e8
COULOMB = E * E / (4 * pi * EPS0)


@_type(8, "ความถี่เชิงมุมของอิเล็กตรอนในอะตอมทอมสัน", "แบบจำลองอะตอมของทอมสัน")
class ThomsonOmega(PhysicsSheet):
    def _variant(self, rng):
        radius = rng.choice((0.05, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3))
        r = radius * 1e-9
        omega = q08.solve(radius=radius)
        agree(omega, sqrt(COULOMB / (ME * r**3)))
        return draw(
            8,
            measure(omega),
            f"ในแบบจำลองอะตอมไฮโดรเจนของทอมสัน ประจุบวก e กระจายสม่ำเสมอในทรงกลมรัศมี {radius} nm อิเล็กตรอนถูกปล่อยจากหยุดนิ่งภายในทรงกลม มันสั่นแบบฮาร์มอนิกอย่างง่ายด้วยความถี่เชิงมุมกี่ rad/s (e = 1.6×10⁻¹⁹ C, mₑ = 9.1×10⁻³¹ kg, ε₀ = 8.85×10⁻¹² C²/N·m²)",
            r"E=\frac{\rho x}{3\varepsilon_0},\quad m\ddot x=-\frac{Qe}{4\pi\varepsilon_0R^3}x",
            [measure(omega**2), measure(sqrt(COULOMB / (ME * r**2))), measure(sqrt(3) * omega)],
        )


@_type(9, "รัศมีอะตอมทอมสันจากความยาวคลื่นสเปกตรัม", "แบบจำลองอะตอมของทอมสัน")
class ThomsonRadius(PhysicsSheet):
    def _variant(self, rng):
        wavelength = rng.choice((410, 434, 486, 589, 656, 700))
        radius = q09.solve(wavelength=wavelength)
        omega = 2 * pi * C / (wavelength * 1e-9)
        agree(radius, (COULOMB / (ME * omega**2)) ** (1 / 3) * 1e9)
        return draw(
            9,
            measure(radius),
            f"ถ้าแสงความยาวคลื่น {wavelength} nm ของไฮโดรเจนเกิดจากการสั่นของอิเล็กตรอนในอะตอมแบบทอมสัน (ประจุ e กระจายสม่ำเสมอในทรงกลม) ทรงกลมประจุบวกต้องมีรัศมีกี่นาโนเมตร (e = 1.6×10⁻¹⁹ C, mₑ = 9.1×10⁻³¹ kg, ε₀ = 8.85×10⁻¹² C²/N·m², c = 3.0×10⁸ m/s)",
            r"\omega=\frac{2\pi c}{\lambda},\quad R^3=\frac{e^2}{4\pi\varepsilon_0m_e\omega^2}",
            [
                measure(radius * (2 * pi) ** (2 / 3)),
                measure(sqrt(COULOMB / (ME * omega**2)) * 1e9),
                measure((E * E / (EPS0 * ME * omega**2)) ** (1 / 3) * 1e9),
            ],
        )


def _cube_over(numerator, n):
    """numerator/cbrt(n) as TeX, exact when n is a cube."""
    root = round(n ** (1 / 3))
    if root**3 == n:
        return tex(Fraction(numerator, root))
    return rf"\frac{{{numerator}}}{{\sqrt[3]{{{n}}}}}"


def _square_over(numerator, n):
    root = isqrt(n)
    if root * root == n:
        return tex(Fraction(numerator, root))
    return rf"\frac{{{numerator}}}{{\sqrt{{{n}}}}}"


@_type(10, "ตำแหน่งสมดุลของอิเล็กตรอนสองตัวในอะตอมทอมสัน", "แบบจำลองอะตอมของทอมสัน")
class ThomsonPairSpacing(PhysicsSheet):
    def _variant(self, rng):
        charge = rng.randint(1, 6)
        radius = 10 * rng.randint(5, 30)  # pm
        agree(q10.solve(radius=radius, charge=charge), radius / (4 * charge) ** (1 / 3))
        return draw(
            10,
            _cube_over(radius, 4 * charge),
            f"อะตอมแบบทอมสันมีประจุบวก {charge}e กระจายสม่ำเสมอในทรงกลมรัศมี {radius} pm และมีอิเล็กตรอน 2 ตัว ที่สมดุลอิเล็กตรอนแต่ละตัวอยู่ห่างจากศูนย์กลางกี่พิโกเมตร",
            r"\frac{eQx}{4\pi\varepsilon_0R^3}=\frac{e^2}{4\pi\varepsilon_0(2x)^2}",
            [_cube_over(radius, charge), _square_over(radius, 4 * charge), _cube_over(2 * radius, 4 * charge)],
        )


@_type(11, "ความถี่การสั่นของอิเล็กตรอนสองตัวในอะตอมทอมสัน", "แบบจำลองอะตอมของทอมสัน")
class ThomsonPairFrequency(PhysicsSheet):
    def _variant(self, rng):
        charge = rng.randint(1, 6)
        radius = 10 * rng.randint(5, 30)  # pm
        r = radius * 1e-12
        freq = q11.solve(radius=radius / 1000, charge=charge)
        base = charge * COULOMB / (ME * r**3)
        agree(freq, sqrt(3 * base) / (2 * pi))
        return draw(
            11,
            measure(freq),
            f"อะตอมแบบทอมสันมีประจุบวก {charge}e กระจายสม่ำเสมอในทรงกลมรัศมี {radius} pm มีอิเล็กตรอน 2 ตัวอยู่ที่สมดุล ขยับอิเล็กตรอนทั้งสองออกจากสมดุลในทิศตรงข้ามกันเท่า ๆ กันเล็กน้อยแล้วปล่อย อิเล็กตรอนสั่นด้วยความถี่กี่เฮิรตซ์ (e = 1.6×10⁻¹⁹ C, mₑ = 9.1×10⁻³¹ kg, ε₀ = 8.85×10⁻¹² C²/N·m²)",
            r"\frac{1}{(x_0+x)^2}\approx\frac1{x_0^2}-\frac{2x}{x_0^3}",
            [measure(sqrt(base) / (2 * pi)), measure(sqrt(3 * base)), measure(sqrt(2 * base) / (2 * pi))],
        )


PRISMS = ((60, 20, 50), (45, 15, 35), (30, 10, 20))


@_type(12, "ดัชนีหักเหจากมุมเบี่ยงเบนน้อยสุดของปริซึม", "การหักเหผ่านปริซึม")
class PrismIndex(PhysicsSheet):
    def _variant(self, rng):
        apex, low, high = rng.choice(PRISMS)
        deviation = rng.randint(low, high)
        n = q12.solve(apex=apex, deviation=deviation)
        a, d = radians(apex), radians(deviation)
        return draw(
            12,
            measure(n),
            f"ปริซึมมีมุมยอด {apex}° วัดมุมเบี่ยงเบนน้อยที่สุดได้ {deviation}° ดัชนีหักเหของปริซึมเป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"n=\frac{\sin\frac{A+D_m}{2}}{\sin\frac A2}",
            [measure(sin(a + d) / sin(a)), measure((apex + deviation) / apex), measure(sin((a + d) / 2) / sin(a))],
        )


@_type(13, "มวลที่อ่านจากตาชั่งจีน", "สมดุลโมเมนต์ของคาน")
class Steelyard(PhysicsSheet):
    def _variant(self, rng):
        slider = rng.choice((10, 20, 25, 50))
        hook = rng.choice((Fraction(2), Fraction(5, 2), Fraction(4), Fraction(5)))
        zero = rng.randint(1, 5)
        mark = zero + rng.randint(2, 30)
        exact = slider * (mark - zero) / hook
        agree(q13.solve(slider=slider, hook=float(hook), zero=zero, mark=mark), exact)
        return draw(
            13,
            tex(exact),
            f"ตาชั่งจีนมีตะขอแขวนวัตถุห่างจุดหมุน {number(hook)} cm ตุ้มเลื่อนมวล {slider} g เมื่อไม่มีวัตถุ คานสมดุลขณะตุ้มเลื่อนอยู่ห่างจุดหมุน {zero} cm (ขีดศูนย์) เมื่อแขวนวัตถุ คานสมดุลขณะตุ้มเลื่อนอยู่ห่างจุดหมุน {mark} cm วัตถุมีมวลกี่กรัม",
            r"m\,d=M(x-x_0)",
            [tex(slider * mark / hook), tex(slider * hook / (mark - zero)), tex(slider * (mark + zero) / hook)],
        )


@_type(14, "ความถ่วงจำเพาะของของเหลวด้วยหลักอาร์คิมีดีส", "หลักของอาร์คิมีดีสกับความถ่วงจำเพาะ")
class SpecificGravity(PhysicsSheet):
    def _variant(self, rng):
        air = rng.randint(60, 150)
        loss = rng.randint(15, air // 2)
        water = air - loss
        liquid = air - rng.randint(loss // 2, 2 * loss)
        exact = Fraction(air - liquid, air - water)
        agree(q14.solve(air=air, water=water, liquid=liquid), exact)
        return draw(
            14,
            tex(exact),
            f"ชั่งก้อนหินในอากาศได้ {air} g ชั่งขณะจมอยู่ในน้ำทั้งก้อนได้ {water} g และขณะจมอยู่ในของเหลวทั้งก้อนได้ {liquid} g ความถ่วงจำเพาะของของเหลวเป็นเท่าใด",
            r"\text{SG}=\frac{W-W_l}{W-W_w}",
            [tex(Fraction(air - water, air - liquid)), tex(Fraction(liquid, water)), tex(Fraction(air - liquid, air))],
        )
