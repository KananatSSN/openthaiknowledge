"""Seeded variants of the reviewed TPhO 3 (2547) national physics olympiad."""

from fractions import Fraction
from math import floor, isqrt, log10, pi

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.answer_choices import exact as number
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, frac_tex
from otk.sheets.tpho2547_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10

from otk.sheets.tpho2547_physics import q11, q12, q13, q14, q15

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


def agree(computed, exact):
    """The solver's float and the generator's exact form must be the same number."""
    assert abs(float(computed) - float(exact)) <= 1e-9 * max(1.0, abs(float(exact)))
    return exact


def over_pi(value):
    """value / pi as exact TeX."""
    value = Fraction(value)
    bottom = rf"{value.denominator}\pi" if value.denominator != 1 else r"\pi"
    return rf"\frac{{{value.numerator}}}{{{bottom}}}"


def figures(value):
    """A nonzero float to three significant figures, as plain text."""
    digits = 2 - floor(log10(abs(value)))
    return f"{round(value, digits):.{digits}f}" if digits > 0 else str(int(round(value, digits)))


SLIPS = {
    1: ("phys.string_speed_equals_end", "phys.string_speed_sine", "phys.string_speed_height_only"),
    2: ("phys.string_accel_initial_value", "phys.string_accel_power_lowered", "phys.string_accel_legs_swapped"),
    3: ("phys.pulley_mass_accel_ignored", "phys.pulley_accel_sign", "phys.pulley_gravity_dropped"),
    4: ("phys.pulley_inertia_ignored", "phys.pulley_inertia_radius_once", "phys.pulley_torque_sign"),
    5: ("phys.rod_springs_one_counted", "phys.rod_springs_full_arm", "phys.rod_springs_point_masses"),
    6: ("phys.cue_ball_sliding_to_stop", "phys.cue_ball_deceleration_dropped", "phys.cue_ball_half_dropped"),
    7: ("phys.cue_ball_initial_speed_used", "phys.cue_ball_speed_loss_used", "phys.cue_ball_ratio_inverted"),
    8: ("phys.loop_emf_doubled", "phys.loop_whole_resistance", "phys.loop_decay_ignored"),
    9: ("phys.echo_doppler_ignored", "phys.echo_one_way_shift", "phys.echo_direction_swapped"),
    10: ("phys.echo_change_sign", "phys.echo_change_half", "phys.echo_change_quotient_rule"),
    11: ("phys.echo_direction_swapped", "phys.echo_one_way_shift", "phys.echo_doppler_ignored"),
    13: ("phys.physical_pendulum_parallel_axis_skipped", "phys.physical_pendulum_parallel_axis_added", "phys.physical_pendulum_pi_not_squared"),
    14: ("phys.coil_resistance_ignored", "phys.coil_impedance_added", "phys.coil_resistance_added_to_r"),
    15: ("phys.coil_line_resistance_ignored", "phys.rc_angular_frequency_as_f", "phys.coil_line_not_rooted"),
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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 3 (2547)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2547_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except _Clash:
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2547_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


TRIPLES = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17))
SCALES = (Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(2))
PULL = "รอกเล็กอยู่สูง H = {height} m เหนือแนวระดับ OX เชือกเบายาว 2H คล้องรอก ปลายหนึ่งผูกมวลที่เริ่มอยู่ที่ O อีกปลาย A เริ่มที่ O แล้วถูกดึงไปตามแนว OX ด้วยความเร็วคงที่ {speed} m/s"


def _pull(rng):
    speed = rng.randint(1, 6)
    across, up, slant = rng.choice(TRIPLES)
    scale = rng.choice(SCALES)
    return speed, across, up, slant, scale, up * scale, across * scale / speed


@_type(1, "ความเร็วของมวลที่ถูกดึงด้วยเชือกคล้องรอก", "จลนศาสตร์ของระบบเชือกคล้องรอก")
class StringSpeed(PhysicsSheet):
    def _variant(self, rng):
        speed, across, up, slant, scale, height, time = _pull(rng)
        exact = Fraction(speed * across, slant)
        agree(q01.solve(speed=speed, height=float(height), time=float(time)), exact)
        return draw(
            1,
            tex(exact),
            PULL.format(height=number(height), speed=speed) + f" ที่เวลา t = {number(time)} s มวลเคลื่อนที่ขึ้นด้วยความเร็วกี่ m/s",
            r"(v_0t)^2+H^2=(H+y)^2\Rightarrow v=\frac{v_0^2t}{H+y}",
            [str(speed), tex(Fraction(speed * up, slant)), tex(Fraction(speed * across, up))],
        )


@_type(2, "ความเร่งของมวลที่ถูกดึงด้วยเชือกคล้องรอก", "จลนศาสตร์ของระบบเชือกคล้องรอก")
class StringAcceleration(PhysicsSheet):
    def _variant(self, rng):
        speed, across, up, slant, scale, height, time = _pull(rng)
        exact = speed**2 * up**2 / (slant**3 * scale)
        agree(q02.solve(speed=speed, height=float(height), time=float(time)), exact)
        return draw(
            2,
            tex(exact),
            PULL.format(height=number(height), speed=speed) + f" ที่เวลา t = {number(time)} s มวลมีความเร่งกี่ m/s²",
            r"a=\frac{v_0^2-v^2}{H+y}=\frac{v_0^2H^2}{(v_0^2t^2+H^2)^{3/2}}",
            [
                tex(speed**2 / height),
                tex(speed**2 * up / (slant**2 * scale)),
                tex(speed**2 * across**2 / (slant**3 * scale)),
            ],
        )


def _start(rng):
    mass = Fraction(rng.randint(1, 10), 2)
    speed = rng.randint(1, 6)
    height = Fraction(rng.randint(1, 10), 2)
    return mass, speed, height, speed**2 / height


@_type(3, "ความตึงเชือกขณะเริ่มดึงมวลผ่านรอก", "แรงตึงเชือกและรอกที่มีมวล")
class StartTension(PhysicsSheet):
    def _variant(self, rng):
        mass, speed, height, accel = _start(rng)
        exact = mass * (10 + accel)
        agree(q03.solve(mass=float(mass), speed=speed, height=float(height)), exact)
        return draw(
            3,
            tex(exact),
            PULL.format(height=number(height), speed=speed).replace("ผูกมวล", f"ผูกมวล {number(mass)} kg ") + " ขณะเริ่มดึง (t = 0) ความตึงเชือกที่ดึงมวลเป็นกี่นิวตัน (รอกเบา g = 10 m/s²)",
            r"a(0)=\frac{v_0^2}{H},\quad T-mg=ma(0)",
            [tex(10 * mass), tex(mass * (10 - accel)), tex(mass * accel)],
        )


@_type(4, "ความตึงเชือกเมื่อรอกมีโมเมนต์ความเฉื่อย", "แรงตึงเชือกและรอกที่มีมวล")
class PulleyTension(PhysicsSheet):
    def _variant(self, rng):
        mass, speed, height, accel = _start(rng)
        radius = Fraction(rng.randint(2, 10), 100)
        inertia = Fraction(rng.randint(1, 20), 10000)
        base = mass * (10 + accel)
        exact = base + inertia * accel / radius**2
        agree(q04.solve(mass=float(mass), radius=float(radius), inertia=float(inertia), speed=speed, height=float(height)), exact)
        return draw(
            4,
            tex(exact),
            PULL.format(height=number(height), speed=speed).replace("ผูกมวล", f"ผูกมวล {number(mass)} kg ").replace("รอกเล็ก", f"รอกรัศมี {number(radius)} m โมเมนต์ความเฉื่อย {number(inertia)} kg·m² ", 1)
            + " ขณะเริ่มดึง (t = 0) ความตึงเชือกช่วงที่ต่อไปยังปลาย A เป็นกี่นิวตัน (เชือกไม่ไถลบนรอก g = 10 m/s²)",
            r"(T'-T)r=I_C\frac{a(0)}{r}",
            [tex(base), tex(base + inertia * accel / radius), tex(base - inertia * accel / radius**2)],
        )


@_type(5, "ความถี่การสั่นของแท่งที่มีสปริงสองข้าง", "การแกว่งของวัตถุแข็งเกร็ง")
class SpringRod(PhysicsSheet):
    def _variant(self, rng):
        mass = Fraction(rng.randint(1, 10), 10)
        j = rng.randint(1, 30)
        spring = mass * j
        length = Fraction(rng.randint(2, 10), 10)
        agree(q05.solve(mass=float(mass), spring=float(spring), length=float(length)) ** 2, Fraction(6 * j) / (4 * 9.869604401089358))
        freq = lambda n: rf"\frac{{1}}{{2\pi}}\sqrt{{{n}}}"  # noqa: E731
        return draw(
            5,
            freq(6 * j),
            f"แท่งบางสม่ำเสมอมวล {number(mass)} kg ยาว {number(length)} m หมุนได้รอบแกนที่จุดกึ่งกลางแท่ง ปลายแต่ละข้างติดสปริงเบาค่าคงตัว {number(spring)} N/m (ข้างหนึ่งต่อขึ้นด้านบน อีกข้างต่อลงด้านล่าง) หมุนแท่งเป็นมุมเล็ก ๆ แล้วปล่อย ความถี่การสั่นเป็นกี่เฮิรตซ์ (I = mL²/12)",
            r"-2k\left(\frac L2\theta\right)\frac L2=\frac{mL^2}{12}\ddot\theta",
            [freq(3 * j), freq(24 * j), freq(2 * j)],
        )


@_type(6, "ระยะไถลของลูกบิลเลียดก่อนกลิ้ง", "สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง")
class CueBallDistance(PhysicsSheet):
    def _variant(self, rng):
        speed = rng.randint(1, 10)
        friction = Fraction(rng.randint(1, 5), 10)
        exact = 12 * speed**2 / (49 * friction * 10)
        agree(q06.solve(speed=speed, friction=float(friction)), exact)
        return draw(
            6,
            tex(exact),
            f"ทรงกลมตันถูกกระแทกในแนวระดับผ่านจุดศูนย์กลางมวล ทำให้ไถลไปบนพื้นระดับด้วยความเร็วต้น {speed} m/s โดยยังไม่หมุน สัมประสิทธิ์ความเสียดทานจลน์ {number(friction)} ทรงกลมเคลื่อนที่ไปได้ไกลกี่เมตรก่อนเริ่มกลิ้งโดยไม่ไถล (I = (2/5)MR², g = 10 m/s²)",
            r"V=V_0-\mu gt,\quad \omega=\frac{5\mu g}{2R}t,\quad V=\omega R",
            [tex(speed**2 / (20 * friction)), tex(2 * speed**2 / (70 * friction)), tex(10 * speed**2 / (490 * friction))],
        )


@_type(7, "อัตราเร็วเชิงมุมของลูกบิลเลียดเมื่อเริ่มกลิ้ง", "สมการนิวตันและออยเลอร์ร่วมเงื่อนไขกลิ้ง")
class CueBallSpin(PhysicsSheet):
    def _variant(self, rng):
        speed = rng.randint(1, 10)
        radius = Fraction(rng.randint(2, 10), 100)
        exact = 5 * speed / (7 * radius)
        agree(q07.solve(speed=speed, radius=float(radius)), exact)
        return draw(
            7,
            tex(exact),
            f"ทรงกลมตันรัศมี {number(radius)} m ถูกกระแทกในแนวระดับผ่านจุดศูนย์กลางมวล ทำให้ไถลไปบนพื้นระดับที่มีความเสียดทานด้วยความเร็วต้น {speed} m/s โดยยังไม่หมุน เมื่อเริ่มกลิ้งโดยไม่ไถล อัตราเร็วเชิงมุมของทรงกลมเป็นกี่ rad/s (I = (2/5)MR²)",
            r"MV_0R=MVR+\tfrac25MR^2\omega,\quad V=\omega R",
            [tex(speed / radius), tex(2 * speed / (7 * radius)), tex(7 * speed / (5 * radius))],
        )


@_type(8, "กระแสในวงลวดสี่เหลี่ยมที่เลื่อนบนราง", "แรงเคลื่อนไฟฟ้าเหนี่ยวนำ")
class SlidingLoopCurrent(PhysicsSheet):
    def _variant(self, rng):
        field = Fraction(rng.randint(1, 10), 10)
        side = Fraction(rng.randint(5, 30), 100)
        speed = rng.randint(1, 10)
        wire = Fraction(rng.randint(1, 10), 10)
        resistor = rng.randint(1, 10)
        mass = Fraction(rng.randint(1, 50), 1000)
        n = rng.randint(1, 3)
        time = n * mass * (wire + resistor) / (field * side) ** 2
        start = field * side * speed / (wire + resistor)
        agree(
            q08.solve(field=float(field), side=float(side), speed=speed, mass=float(mass), wire=float(wire), resistor=resistor, time=float(time)),
            float(start) * 2.718281828459045 ** (-n),
        )
        decay = lambda i: rf"{tex(i)}e^{{-{n}}}"  # noqa: E731
        return draw(
            8,
            decay(start),
            f"วงลวดสี่เหลี่ยมจัตุรัสมวล {number(mass)} kg ด้านยาว {number(side)} m แต่ละด้านมีความต้านทาน {number(wire)} Ω มีลวดสั้น ๆ ที่กึ่งกลางด้านบนและด้านล่างพาดบนรางขนานลื่นในแนวระดับ ปลายรางต่อตัวต้านทาน {resistor} Ω ทั้งหมดอยู่ในสนามแม่เหล็ก {number(field)} T ตั้งฉากกับระนาบ ดีดวงลวดให้มีความเร็วต้น {speed} m/s ไปตามราง ที่เวลา t = {number(time)} s กระแสผ่านตัวต้านทานเป็นกี่แอมแปร์",
            r"\mathcal E=vBL,\ r_{\text{in}}=\frac{2r}{2}=r,\quad m\frac{dv}{dt}=-\frac{B^2L^2v}{r+R}",
            [decay(2 * start), decay(field * side * speed / (4 * wire + resistor)), tex(start)],
        )


def _echo(rng):
    wave = rng.choice((330, 340, 1500))
    speed = rng.randint(1, wave // 3)
    gap = Fraction(rng.randint(1, 20), 100)
    return wave, speed, gap


ECHO = "แหล่งกำเนิดส่งคลื่นดลออกไปเป็นขบวนด้วยความเร็ว {wave} m/s ห่างกันทุก ๆ {gap} s ลูกคลื่นสะท้อนจากวัตถุที่เคลื่อนที่{way}แหล่งกำเนิดด้วยความเร็ว {speed} m/s"


@_type(9, "ช่วงเวลาระหว่างคลื่นดลที่สะท้อนจากวัตถุที่เข้าหา", "คลื่นดลสะท้อนจากวัตถุเคลื่อนที่")
class EchoApproaching(PhysicsSheet):
    def _variant(self, rng):
        wave, speed, gap = _echo(rng)
        exact = (wave - speed) * gap / (wave + speed)
        agree(q09.solve(wave=wave, speed=speed, gap=float(gap)), exact)
        return draw(
            9,
            tex(exact),
            ECHO.format(wave=wave, gap=number(gap), way="เข้าหา", speed=speed) + " คลื่นดลที่สะท้อนกลับมาห่างกันกี่วินาที",
            r"t'c+t'v=c\tau,\quad \Delta t=\frac{(c-v)t'}{c}",
            [tex(gap), tex((wave - speed) * gap / wave), tex((wave + speed) * gap / (wave - speed))],
        )


@_type(10, "การเปลี่ยนช่วงเวลาสะท้อนเมื่อความเร็วเพิ่มเล็กน้อย", "คลื่นดลสะท้อนจากวัตถุเคลื่อนที่")
class EchoChange(PhysicsSheet):
    def _variant(self, rng):
        wave, speed, gap = _echo(rng)
        step = Fraction(rng.randint(1, 10), 10)
        exact = -2 * wave * gap * step / (wave + speed) ** 2
        agree(q10.solve(wave=wave, speed=speed, gap=float(gap), step=float(step)), exact)
        return draw(
            10,
            tex(exact),
            ECHO.format(wave=wave, gap=number(gap), way="เข้าหา", speed=speed) + f" ถ้าวัตถุเร็วขึ้นอีก {number(step)} m/s ช่วงเวลาระหว่างคลื่นที่สะท้อนเปลี่ยนไปประมาณกี่วินาที (ประมาณอันดับหนึ่ง)",
            r"\delta t=\frac{d}{dv}\left[\frac{c-v}{c+v}\tau\right]\delta v",
            [tex(-exact), tex(exact / 2), tex(-2 * gap * step / (wave + speed))],
        )


@_type(11, "ช่วงเวลาระหว่างคลื่นดลที่สะท้อนจากวัตถุที่หนี", "คลื่นดลสะท้อนจากวัตถุเคลื่อนที่")
class EchoReceding(PhysicsSheet):
    def _variant(self, rng):
        wave, speed, gap = _echo(rng)
        exact = (wave + speed) * gap / (wave - speed)
        agree(q11.solve(wave=wave, speed=speed, gap=float(gap)), exact)
        return draw(
            11,
            tex(exact),
            ECHO.format(wave=wave, gap=number(gap), way="หนีจาก", speed=speed) + " คลื่นดลที่สะท้อนกลับมาห่างกันกี่วินาที",
            r"t'c-t'v=c\tau,\quad \Delta t=\frac{(c+v)t'}{c}",
            [tex((wave - speed) * gap / (wave + speed)), tex((wave + speed) * gap / wave), tex(gap)],
        )


ECHO_FATE = {
    "overlap": "คลื่นสะท้อนซ้อนทับกัน เพราะวัตถุวิ่งนำหน้าคลื่นที่สะท้อนออกมา",
    "none": "ไม่มีคลื่นสะท้อน เพราะลูกคลื่นวิ่งตามวัตถุไม่ทัน",
    "ordered": "คลื่นสะท้อนกลับมาตามลำดับเดิม โดยห่างกันด้วยช่วงเวลาคงที่ค่าหนึ่ง",
    "same": "คลื่นสะท้อนกลับมาห่างกันเท่าเดิมทุกกรณี เพราะคลื่นเร็ว c เสมอ",
}


@_type(12, "คลื่นดลสะท้อนเมื่อวัตถุเร็วกว่าคลื่น", "คลื่นดลสะท้อนจากวัตถุเคลื่อนที่")
class EchoSupersonic(ChoiceType):
    sheet_id = "tpho2547_physics"
    sheet = SHEET

    def compose(self, rng):
        wave = rng.choice((330, 340, 1500))
        approaching = rng.random() < 0.5
        speed = rng.randint(wave + 10, 3 * wave) if rng.random() < 0.7 else rng.randint(1, wave - 10)
        answer = q12.solve(wave=wave, speed=speed, approaching=approaching)
        if answer == "ordered":
            tags = {"overlap": "phys.echo_subsonic_overlap", "none": "phys.echo_subsonic_no_reflection"}
        else:
            tags = {"overlap": "phys.echo_supersonic_direction_swapped", "none": "phys.echo_supersonic_direction_swapped",
                    "ordered": "phys.echo_supersonic_formula_extended"}
        tags["same"] = "phys.echo_doppler_ignored"
        return (
            f"แหล่งกำเนิดส่งคลื่นดลออกไปเป็นขบวนด้วยความเร็ว {wave} m/s ห่างกันด้วยช่วงเวลาเท่ากัน วัตถุเคลื่อนที่{'เข้าหา' if approaching else 'หนีจาก'}แหล่งกำเนิดด้วยความเร็ว {speed} m/s (ไม่คิดทฤษฎีสัมพัทธภาพ) ข้อใดบรรยายคลื่นสะท้อนได้ถูกต้อง",
            ECHO_FATE[answer],
            tuple(named(tags[k], ECHO_FATE[k]) for k in ECHO_FATE if k != answer),
        )


@_type(13, "โมเมนต์ความเฉื่อยรอบจุดศูนย์กลางมวลจากลูกตุ้มฟิสิกัล", "การแกว่งของวัตถุแข็งเกร็ง")
class HangerInertia(PhysicsSheet):
    def _variant(self, rng):
        mass = 26
        while True:
            distance = rng.randint(3, 15)
            period = Fraction(rng.randint(70, 130), 100)
            pivot = mass * 980 * distance * period**2
            if float(pivot) / (4 * pi**2) > 1.2 * mass * distance**2:
                break
        inertia = q13.solve(mass=mass, distance=distance, period=float(period))
        agree(inertia, float(pivot) / (4 * pi**2) - mass * distance**2)
        return draw(
            13,
            figures(inertia),
            f"ไม้แขวนเสื้อมวล 26.0 g แกว่งด้วยแอมพลิจูดเล็ก ๆ รอบจุดหมุน O ที่อยู่ห่างจุดศูนย์กลางมวล {distance} cm ได้คาบ {number(period)} s โดย T = 2π√(I/(mgd)) โมเมนต์ความเฉื่อยรอบแกนที่ผ่านจุดศูนย์กลางมวล (ขนานกับแกนผ่าน O) เป็นกี่ g·cm² (g = 980 cm/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"I_O=\frac{mgdT^2}{4\pi^2},\quad I_{cm}=I_O-md^2",
            [
                figures(float(pivot) / (4 * pi**2)),
                figures(float(pivot) / (4 * pi**2) + mass * distance**2),
                figures(float(pivot) / (4 * pi) - mass * distance**2),
            ],
        )


@_type(14, "อัตราส่วนความต่างศักย์คร่อมตัวต้านทานต่อขดลวด", "วงจรไฟฟ้ากระแสสลับ RL")
class CoilVoltageRatio(PhysicsSheet):
    def _variant(self, rng):
        coil, reactance, impedance = rng.choice(TRIPLES)
        k = rng.choice((2, 5, 10))
        coil, reactance, impedance = coil * k, reactance * k, impedance * k
        resistor = 50 * rng.randint(1, 40)
        inductance = Fraction(reactance, 1000)
        exact = Fraction(resistor, impedance)
        agree(q14.solve(resistor=resistor, coil=coil, omega=1000, inductance=float(inductance)), exact)
        return draw(
            14,
            tex(exact),
            f"ขดลวดเหนี่ยวนำ {number(inductance)} H ที่มีความต้านทานในตัว {coil} Ω ต่ออนุกรมกับตัวต้านทาน {resistor} Ω และแหล่งจ่ายไฟฟ้ากระแสสลับที่มี ω = 1000 rad/s อัตราส่วน V_R/V_L ของความต่างศักย์ยังผลคร่อมตัวต้านทานต่อคร่อมขดลวดเป็นเท่าใด",
            r"\frac{V_R}{V_L}=\frac{R}{\sqrt{(\omega L)^2+r^2}}",
            [tex(Fraction(resistor, reactance)), tex(Fraction(resistor, reactance + coil)), tex(Fraction(resistor + coil, impedance))],
        )


def _root_over_pi(square, scale):
    """sqrt(square)/(scale pi) for a whole square, reduced, as TeX."""
    outside, inside = 1, square
    for k in range(isqrt(square), 1, -1):
        if square % (k * k) == 0:
            outside, inside = k, square // (k * k)
            break
    coefficient = Fraction(outside, scale)
    top = (str(coefficient.numerator) if coefficient.numerator != 1 else "") + rf"\sqrt{{{inside}}}"
    bottom = rf"{coefficient.denominator}\pi" if coefficient.denominator != 1 else r"\pi"
    return rf"\frac{{{top}}}{{{bottom}}}"


@_type(15, "ความเหนี่ยวนำจากกราฟเส้นตรง", "วงจรไฟฟ้ากระแสสลับ RL")
class InductanceFromLine(PhysicsSheet):
    def _variant(self, rng):
        reactance = 10 * rng.randint(5, 60)
        slope = reactance**2 + 38**2
        agree(q15.solve(slope=slope), reactance / (100 * pi))
        return draw(
            15,
            over_pi(Fraction(reactance, 100)),
            f"บัลลาสต์ (ขดลวดเหนี่ยวนำ) ความต้านทานในตัว 38 Ω ต่ออนุกรมกับตัวต้านทาน R และหม้อแปลงไฟฟ้ากระแสสลับความถี่ 50 Hz วัด V_L และ V_R ที่ R หลายค่า แล้วเขียนกราฟ (V_L/V_R)² กับ 1/R² ได้เส้นตรงผ่านจุดกำเนิดที่มีความชัน {slope} Ω² ความเหนี่ยวนำ L เป็นกี่เฮนรี",
            r"\left(\frac{V_L}{V_R}\right)^2=\frac{(\omega L)^2+r^2}{R^2}",
            [_root_over_pi(slope, 100), tex(Fraction(reactance, 50)), over_pi(Fraction(reactance**2, 100))],
        )
