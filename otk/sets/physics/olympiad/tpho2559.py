"""Seeded variants of the reviewed TPhO 15 (2559) national physics olympiad."""

from math import acos, cos, degrees, exp, floor, log10, pi, radians, sin, sqrt, tan

from otk.core.mistakes import named
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sheets.tpho2559_physics import q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12

from otk.sheets.tpho2559_physics import q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


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
    1: ("phys.venturi_exit_speed_ignored", "phys.venturi_throat_speed_halved", "phys.bernoulli_half_dropped"),
    2: ("phys.stretch_halved", "phys.wire_modulus_inverted", "phys.weight_as_mass"),
    3: ("phys.thermal_growth_dropped", "phys.modulus_change_dropped", "phys.elastic_part_dropped"),
    4: ("phys.elastic_length_growth_ignored", "phys.wire_area_sign", "phys.wire_area_modulus_once"),
    5: ("phys.room_radiation_ignored", "phys.temperature_difference_to_fourth", "phys.radiation_cubed"),
    6: ("phys.resistance_power_ratio_inverted", "phys.ohmic_exponent", "phys.radiation_exponent_halved"),
    7: ("phys.vapour_for_nitrogen", "phys.humidity_not_applied", "phys.saturation_at_warm"),
    8: ("phys.temperature_ratio_inverted", "phys.total_pressure_for_partial", "phys.room_volume_unchanged"),
    9: ("phys.temperature_ratio_inverted", "phys.total_pressure_for_partial", "phys.work_on_room_volume"),
    10: ("phys.vapour_after_only", "phys.room_volume_unchanged", "phys.molar_mass_dropped"),
    11: ("phys.latent_heat_at_room", "phys.room_volume_unchanged", "phys.latent_heat_constant_only"),
    12: ("phys.latent_heat_only", "phys.atmosphere_work_dropped", "phys.cooling_only"),
    13: ("phys.share_inverted", "phys.atmosphere_work_dropped", "phys.latent_heat_only"),
    14: ("phys.drill_friction_ignored", "phys.drill_tangent_inverted", "phys.drill_load_weight_only"),
    15: ("phys.rope_angle_in_degrees", "phys.rope_winding_sign", "phys.rope_angle_unchanged"),
    16: ("phys.drill_friction_ignored", "phys.drill_load_weight_only", "phys.kinetic_half_missing"),
    17: ("phys.drill_spin_down_with_push", "phys.drill_friction_once", "phys.drill_turns_doubled"),
    18: ("phys.drill_half_cycle", "phys.drill_power_not_rooted", "phys.drill_full_cycle_doubled"),
    19: ("phys.blade_whole_length", "phys.blade_torque_at_tip", "phys.blade_half_dropped"),
    20: ("phys.log_slope_not_halved", "phys.log_slope_sign", "phys.log_slope_doubled"),
    21: ("phys.flux_hemisphere", "phys.flux_area_without_4pi", "phys.ldr_exponent_inverted"),
    22: ("phys.grating_cosine", "phys.grating_second_order", "phys.grating_tangent"),
    23: ("phys.response_ratio_inverted", "phys.response_not_corrected", "phys.response_multiplied"),
}


class _Clash(Exception):
    """Two choices came out equal, or the variant is unphysical: the draw is made again."""


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


SHEET = "ฟิสิกส์โอลิมปิกระดับชาติ ครั้งที่ 15 (2559)"


class PhysicsSheet(WordProblem):
    sheet_id = "tpho2559_physics"
    sheet = SHEET

    def expr(self, rng):
        while True:
            try:
                return self._variant(rng)
            except (_Clash, ValueError, ZeroDivisionError):
                continue


def _type(n, title, topic):
    return question_type(
        f"phys.tpho2559_q{n:02d}",
        display_name={"th": title},
        level=LEVEL,
        subject="ฟิสิกส์",
        topic=topic,
    )


STREAM_TOPIC = "เส้นกระแสและสมการแบร์นูลลี"
WIRE_TOPIC = "การยืดของลวดเมื่ออุณหภูมิเปลี่ยน"
LAMP_TOPIC = "หลอดไฟไส้สุญญากาศ"
AIRCON_TOPIC = "เครื่องปรับอากาศและความชื้น"
DRILL_TOPIC = "สว่านปั๊ม (บิดหร่า)"
LDR_TOPIC = "การสอบเทียบตัวต้านทานไวแสง"


@_type(1, "อัตราเร็วลมต่ำสุดที่ทำให้น้ำพ่นจากท่อเวนทูรี", STREAM_TOPIC)
class VenturiSpray(PhysicsSheet):
    def _variant(self, rng):
        height = rng.randint(1, 20)
        air = rng.choice((1.1, 1.2, 1.25, 1.29))
        v = q01.solve(height=height, air=air)
        base = 1000 * 9.8 * height / 100 / air
        return draw(
            1,
            measure(v),
            f"เป่าลม (ความหนาแน่น {air:g} kg/m³) เข้าท่อที่ช่วงคอดมีพื้นที่หน้าตัดครึ่งหนึ่งและปลายออกมีพื้นที่หน้าตัดสองเท่าของปากท่อ หลอดดูดน้ำ (1000 kg/m³) ต่อจากช่วงคอดลงไปยังผิวน้ำที่อยู่ต่ำกว่า {height} cm "
            "ต้องเป่าลมเข้าปากท่อด้วยอัตราเร็วอย่างน้อยกี่เมตรต่อวินาทีน้ำจึงพ่นออกมาได้ (g = 9.8 m/s², ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_2+\tfrac12\rho_av_2^2=P_a+\tfrac12\rho_av_3^2,\quad P_2=P_a-\rho_wgh",
            [measure(sqrt(2 * base / 4)), measure(sqrt(8 * base / 3)), measure(sqrt(4 * base / 15))],
        )


WIRE = "ลวดยาว {L} m พื้นที่หน้าตัด {A} mm² มอดุลัสของยัง {Y} GPa ที่อุณหภูมิห้อง"


@_type(2, "ระยะยืดของลวดที่ห้อยน้ำหนัก", WIRE_TOPIC)
class WireStretch(PhysicsSheet):
    def _variant(self, rng):
        weight = rng.randint(5, 50) * 10
        length = rng.randint(5, 40) / 10
        area = rng.choice((0.5, 1.0, 2.0, 3.0))
        modulus = rng.choice((70, 110, 120, 200, 210))
        dl = q02.solve(weight=weight, length=length, area=area, modulus=modulus)
        return draw(
            2,
            measure(dl),
            WIRE.format(L=f"{length:g}", A=f"{area:g}", Y=modulus) + f" ห้อยวัตถุน้ำหนัก {weight} N ที่ปลายลวด ลวดยืดออกกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Y\frac{\Delta L}{L}=\frac{F}{A}",
            [measure(dl / 2), measure(1 / dl), measure(dl / 9.8)],
        )


@_type(3, "ระยะยืดของลวดเมื่ออุณหภูมิเพิ่มขึ้น", WIRE_TOPIC)
class WireWarmStretch(PhysicsSheet):
    def _variant(self, rng):
        weight = rng.randint(5, 50) * 10
        length = rng.randint(5, 40) / 10
        area = rng.choice((0.5, 1.0, 2.0))
        modulus = rng.choice((70, 110, 200))
        slope = rng.randint(2, 10) * 10
        expansion = rng.randint(8, 24)
        warming = rng.randint(1, 10) * 10
        dl = q03.solve(weight=weight, length=length, area=area, modulus=modulus, slope=slope, expansion=expansion, warming=warming)
        cold = q02.solve(weight=weight, length=length, area=area, modulus=modulus)
        thermal = expansion * 1e-6 * length * warming * 1e3
        warm_elastic = dl - thermal
        return draw(
            3,
            measure(dl),
            WIRE.format(L=f"{length:g}", A=f"{area:g}", Y=modulus)
            + f" ห้อยวัตถุน้ำหนัก {weight} N แล้วเพิ่มอุณหภูมิขึ้น {warming} K สัมประสิทธิ์การขยายตัว {expansion}×10⁻⁶ K⁻¹ และมอดุลัสเพิ่มขึ้น {slope} MPa ต่อเคลวิน ลวดยืดออกจากความยาวเดิมทั้งหมดกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\Delta L_2=\frac{W}{A}\frac{L_0+\alpha L_0\Delta T}{Y_0+\varepsilon\Delta T}+\alpha L_0\Delta T",
            [measure(warm_elastic), measure(cold + thermal), measure(thermal)],
        )


@_type(4, "พื้นที่หน้าตัดลวดที่ทำให้วัตถุอยู่ที่เดิม", WIRE_TOPIC)
class WireCompensated(PhysicsSheet):
    def _variant(self, rng):
        weight = rng.randint(5, 50) * 100
        modulus = rng.choice((70, 110, 120, 200))
        slope = rng.randint(5, 20) * 10
        expansion = rng.randint(4, 20)
        ratio = slope * 1e6 / (expansion * 1e-6 * modulus * 1e9)
        if ratio < 2:
            raise _Clash
        a = q04.solve(weight=weight, modulus=modulus, slope=slope, expansion=expansion)
        base = weight / (modulus * 1e9) * 1e6
        return draw(
            4,
            measure(a),
            f"ลวดมอดุลัสของยัง {modulus} GPa ที่ T₀ สัมประสิทธิ์การขยายตัว {expansion}×10⁻⁶ K⁻¹ และมอดุลัสเพิ่มขึ้น {slope} MPa ต่อเคลวิน ห้อยวัตถุน้ำหนัก {weight} N "
            "ลวดต้องมีพื้นที่หน้าตัดกี่ตารางมิลลิเมตรเพื่อให้วัตถุอยู่ที่ตำแหน่งเดิมเมื่ออุณหภูมิเพิ่มขึ้นเล็กน้อย (ประมาณอันดับหนึ่ง, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{W}{AY_0}\left(\alpha-\frac{\varepsilon}{Y_0}\right)+\alpha=0",
            [measure(base * ratio), measure(base * (ratio + 1)), measure(ratio - 1)],
        )


SIGMA = 5.67e-8


@_type(5, "กำลังไฟฟ้าที่ไส้หลอดได้รับ", LAMP_TOPIC)
class LampPower(PhysicsSheet):
    def _variant(self, rng):
        area = rng.randint(5, 50) * 2
        hot = rng.randint(15, 30) * 100
        room = rng.choice((290, 300, 310))
        p = q05.solve(area=area, hot=hot, room=room)
        A = area * 1e-6
        return draw(
            5,
            measure(p),
            f"ไส้หลอดไฟสุญญากาศพื้นที่ผิว {area} mm² ร้อนคงที่ที่ {hot} K ในห้องอุณหภูมิ {room} K ถ้าความร้อนถ่ายเทด้วยการแผ่รังสีอย่างเดียว (σ = 5.67×10⁻⁸ W/m²·K⁴) ไส้หลอดได้รับกำลังไฟฟ้ากี่วัตต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P+\sigma AT_0^4=\sigma AT^4",
            [measure(SIGMA * A * hot**4), measure(SIGMA * A * (hot - room) ** 4), measure(SIGMA * A * (hot**3 - room**3))],
        )


@_type(6, "เลขชี้กำลังของความสัมพันธ์กระแสกับความต่างศักย์ของหลอดไฟ", LAMP_TOPIC)
class LampExponent(PhysicsSheet):
    def _variant(self, rng):
        power = rng.choice((0.8, 1.0, 1.2, 1.25, 1.5))
        n = q06.solve(power=power)
        return draw(
            6,
            measure(n),
            f"ไส้หลอดไฟสุญญากาศมีความต้านทาน R = λT^{power:g} และสูญเสียความร้อนด้วยการแผ่รังสี σAT⁴ เมื่ออุณหภูมิไส้หลอดสูงกว่าอุณหภูมิห้องมาก กระแส I = βVⁿ ค่า n เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"I^2R=\sigma AT^4,\quad R=\lambda T^p,\quad R=\frac{V}{I}",
            [measure((4 + power) / (4 - power)), measure(1.0), measure((4 - power) / (2 * (4 + power)))],
        )


AIR = 101325.0
ROOM = "ห้องปริมาตร {V} m³ เดิมมีอากาศ 30 °C ความชื้นสัมพัทธ์ {h}% (ไนโตรเจนกับไอน้ำ) เปิดเครื่องปรับอากาศจนเหลือ 25 °C ความชื้นสัมพัทธ์ {h2}% ความดันรวมคงที่ 1.01325×10⁵ Pa (ความดันไอน้ำอิ่มตัว 4.244 kPa ที่ 30 °C และ 3.169 kPa ที่ 25 °C, R = 8.31 J/(mol·K))"


def _room(rng):
    return rng.choice((45, 60, 75, 90, 120)), rng.randint(60, 90), rng.randint(40, 55)


def _parts(room, humid, dry, coil=10.0):
    T, Tp, Tc = 303.15, 298.15, coil + 273.15
    R = 8.31447
    pv, pv2 = humid / 100 * 4244, dry / 100 * 3169
    pn, pn2 = AIR - pv, AIR - pv2
    volume = pn2 * T * room / (pn * Tp)
    nv, nv2 = pv * volume / (R * T), pv2 * room / (R * Tp)
    nn = pn * volume / (8.31 * T)
    condensed = nv - nv2
    latent = condensed * (57.075e3 - 43.9 * Tc)
    cooling = (3 * nv + 2.5 * nn) * 8.31 * 5 + 3 * condensed * 8.31 * (Tp - Tc)
    work = AIR * (volume - room)
    return {"pv": pv, "pv2": pv2, "pn": pn, "pn2": pn2, "volume": volume, "nv": nv, "nv2": nv2,
            "condensed": condensed, "latent": latent, "cooling": cooling, "work": work}


@_type(7, "ความดันย่อยของไนโตรเจนหลังเปิดเครื่องปรับอากาศ", AIRCON_TOPIC)
class AirconNitrogen(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        p = q07.solve(dry=dry)
        return draw(
            7,
            measure(p),
            ROOM.format(V=room, h=humid, h2=dry) + " หลังเปิดเครื่อง ความดันย่อยของไนโตรเจนในห้องเป็นกี่กิโลพาสคัล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"P_{\text{vapor}}=\frac{h}{100}P_{\text{sat}},\quad P_{N_2}=P_{\text{mixture}}-P_{\text{vapor}}",
            [measure(dry / 100 * 3.169), measure((AIR - 3169) / 1e3), measure((AIR - dry / 100 * 4244) / 1e3)],
        )


@_type(8, "ปริมาตรอากาศทั้งหมดก่อนเปิดเครื่องปรับอากาศ", AIRCON_TOPIC)
class AirconVolume(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        v = q08.solve(room=room, humid=humid, dry=dry)
        p = _parts(room, humid, dry)
        return draw(
            8,
            measure(v),
            ROOM.format(V=room, h=humid, h2=dry) + " อากาศทั้งหมดที่สุดท้ายอยู่ในห้อง เดิม (ที่ 30 °C) มีปริมาตรรวมกี่ลูกบาศก์เมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{P_{N_2}V}{T}=\frac{P'_{N_2}V'}{T'}",
            [measure(p["pn2"] * 298.15 * room / (p["pn"] * 303.15)), measure(303.15 * room / 298.15), measure(p["pn2"] * room / p["pn"])],
        )


@_type(9, "งานของความดันบรรยากาศเมื่อเปิดเครื่องปรับอากาศ", AIRCON_TOPIC)
class AirconWork(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        w = q09.solve(room=room, humid=humid, dry=dry)
        p = _parts(room, humid, dry)
        flipped = p["pn2"] * 298.15 * room / (p["pn"] * 303.15)
        return draw(
            9,
            measure(w),
            ROOM.format(V=room, h=humid, h2=dry) + " ความดันบรรยากาศภายนอกดันอากาศเข้าห้อง ทำงานกี่กิโลจูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"W=P_{\text{atm}}(V-V')",
            [measure(AIR * abs(flipped - room) / 1e3), measure(AIR * (303.15 / 298.15 - 1) * room / 1e3), measure(AIR * p["volume"] / 1e3)],
        )


@_type(10, "มวลไอน้ำที่ควบแน่นในเครื่องปรับอากาศ", AIRCON_TOPIC)
class AirconCondensed(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        m = q10.solve(room=room, humid=humid, dry=dry)
        p = _parts(room, humid, dry)
        unchanged = (p["pv"] * room / (8.31447 * 303.15) - p["nv2"]) * 18
        return draw(
            10,
            measure(m),
            ROOM.format(V=room, h=humid, h2=dry) + " ไอน้ำกลายเป็นหยดน้ำทั้งหมดกี่กรัม (น้ำ 18 g/mol, ตอบเลขนัยสำคัญ 3 ตัว)",
            r"n=\frac{P_{\text{vapor}}V}{RT}-\frac{P'_{\text{vapor}}V'}{RT'}",
            [measure(p["nv2"] * 18), measure(unchanged), measure(p["condensed"])],
        )


@_type(11, "ความร้อนจากการควบแน่นของไอน้ำ", AIRCON_TOPIC)
class AirconLatent(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        coil = rng.randint(5, 15)
        q = q11.solve(room=room, humid=humid, dry=dry, coil=coil)
        p = _parts(room, humid, dry, coil)
        unchanged = p["pv"] * room / (8.31447 * 303.15) - p["nv2"]
        return draw(
            11,
            measure(q),
            ROOM.format(V=room, h=humid, h2=dry) + f" ไอน้ำควบแน่นที่ขดลวดเย็น {coil} °C โดยความร้อนแฝง H(T) = 57.075 − 0.0439T kJ/mol (T ในเคลวิน) ความร้อนที่คายออกจากการควบแน่นเป็นกี่กิโลจูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=n\,H(T_{\text{coil}})",
            [measure(p["condensed"] * (57.075 - 0.0439 * 298.15)), measure(unchanged * (57.075 - 0.0439 * (coil + 273.15))), measure(p["condensed"] * 57.075)],
        )


@_type(12, "ความร้อนทั้งหมดที่เครื่องปรับอากาศต้องเอาออก", AIRCON_TOPIC)
class AirconTotal(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        q = q12.solve(room=room, humid=humid, dry=dry)
        p = _parts(room, humid, dry)
        return draw(
            12,
            measure(q),
            ROOM.format(V=room, h=humid, h2=dry) + " ไอน้ำควบแน่นที่ขดลวด 10 °C (H = 57.075 − 0.0439T kJ/mol) พลังงานภายในของไนโตรเจน 5PV/2 และของไอน้ำ 3PV ความร้อนทั้งหมดที่ต้องเอาออกจากห้องเป็นกี่กิโลจูล (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"Q=\Delta U_{30\to25}+\Delta U_{25\to10}+W+Q_{\text{condense}}",
            [measure(p["latent"] / 1e3), measure((p["cooling"] + p["latent"]) / 1e3), measure(p["cooling"] / 1e3)],
        )


@_type(13, "สัดส่วนความร้อนที่ใช้ในการควบแน่น", AIRCON_TOPIC)
class AirconShare(PhysicsSheet):
    def _variant(self, rng):
        room, humid, dry = _room(rng)
        share = q13.solve(room=room, humid=humid, dry=dry)
        p = _parts(room, humid, dry)
        return draw(
            13,
            measure(share),
            ROOM.format(V=room, h=humid, h2=dry) + " (ควบแน่นที่ 10 °C, H = 57.075 − 0.0439T kJ/mol, U ของไนโตรเจน 5PV/2 และของไอน้ำ 3PV) ความร้อนจากการควบแน่นคิดเป็นกี่เปอร์เซ็นต์ของความร้อนทั้งหมดที่ต้องเอาออก (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\frac{Q_{\text{condense}}}{Q_{\text{total}}}\times100",
            [measure(10000 / share), measure(100 * p["latent"] / (p["cooling"] + p["latent"])), measure(100 * p["cooling"] / (p["cooling"] + p["work"] + p["latent"]))],
        )


DRILL = "สว่านปั๊มมีล้อตุ้นมวล {M} kg โมเมนต์ความเฉื่อย {I} kg·cm² ทอร์กเสียดทานที่หัวสว่านเท่ากับ k = {k} mm คูณแรงปฏิกิริยาที่พื้น (g = 9.8 m/s²)"


@_type(14, "ความเร่งเชิงมุมของสว่านปั๊มขณะกดคาน", DRILL_TOPIC)
class DrillAcceleration(PhysicsSheet):
    def _variant(self, rng):
        force = rng.randint(10, 50)
        angle = rng.randint(10, 40)
        radius = rng.randint(3, 8)
        mass = rng.randint(5, 30) / 10
        k = rng.randint(1, 5) / 10
        inertia = rng.randint(5, 30)
        a = q14.solve(force=force, angle=angle, radius=radius, mass=mass, k=k, inertia=inertia)
        if a <= 0:
            raise _Clash
        t = radians(angle)
        drive = force * radius * 1e-3 / tan(t)
        inverted = force * radius * 1e-3 * tan(t) - k * 1e-3 * (mass * 9.8 + force)
        if inverted <= 0:
            raise _Clash
        moment = inertia * 1e-4
        return draw(
            14,
            measure(a),
            DRILL.format(M=f"{mass:g}", I=inertia, k=f"{k:g}") + f" แกนรัศมี {radius} mm กดคานด้วยแรงรวม {force} N ขณะเชือกทำมุม {angle}° กับคาน แกนสว่านมีความเร่งเชิงมุมกี่ rad/s² (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"2T\sin\theta=F_1,\quad \tau=2T\cos\theta\,r-k(Mg+F_1)",
            [measure(drive / moment), measure(inverted / moment), measure((drive - k * 1e-3 * mass * 9.8) / moment)],
        )


@_type(15, "ค่า b ของงานในช่วงคลายเกลียว", DRILL_TOPIC)
class DrillReach(PhysicsSheet):
    def _variant(self, rng):
        arm = rng.randint(20, 35)
        radius = rng.randint(2, 5)
        angle = rng.randint(65, 80)
        turns = rng.randint(2, 6)
        b = q15.solve(arm=arm, radius=radius, angle=angle, turns=turns)
        t0 = radians(angle)
        tn = acos(cos(t0) * exp(2 * turns * pi * radius / (arm * 10)))
        return draw(
            15,
            measure(b),
            f"สว่านปั๊มมีคานยาวข้างละ L = {arm} cm แกนรัศมี {radius} mm เมื่อเชือกคลายหมดทำมุม θ₀ = {angle}° กับคาน พันเกลียวไว้ {turns} รอบ (cos θₙ = cos θ₀ e^(2nπr/L)) "
            "งานของแรงกด F₁ ตลอดช่วงคลายเกลียวเท่ากับ b·F₁ ค่า b เป็นกี่เซนติเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"W_1=F_1L(\theta_0-\theta_n)",
            [measure(arm * (angle - degrees(tn))), measure(arm * (tan(t0) - tan(tn))), measure(arm * t0)],
        )


@_type(16, "อัตราเร็วเชิงมุมของสว่านเมื่อคลายเกลียวหมด", DRILL_TOPIC)
class DrillSpin(PhysicsSheet):
    def _variant(self, rng):
        force = rng.randint(20, 50)
        turns = rng.randint(2, 4)
        mass = rng.randint(5, 20) / 10
        k = rng.randint(1, 4) / 10
        inertia = rng.randint(5, 30)
        w = q16.solve(force=force, turns=turns, mass=mass, k=k, inertia=inertia)
        b = q15.solve(turns=turns) * 1e-2
        moment = inertia * 1e-4
        friction = 2 * turns * pi * k * 1e-3 * (mass * 9.8 + force)
        return draw(
            16,
            measure(w),
            DRILL.format(M=f"{mass:g}", I=inertia, k=f"{k:g}") + f" คานยาวข้างละ 25 cm แกนรัศมี 3 mm θ₀ = 70° พันเกลียว {turns} รอบ กดคานด้วยแรงคงที่ {force} N จนเกลียวคลายหมด หัวสว่านหมุนด้วยอัตราเร็วเชิงมุมกี่ rad/s (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tfrac12I\omega^2=F_1L(\theta_0-\theta_n)-2n\pi k(Mg+F_1)",
            [measure(sqrt(2 * force * b / moment)), measure(sqrt(2 * (force * b - 2 * turns * pi * k * 1e-3 * mass * 9.8) / moment)), measure(sqrt((force * b - friction) / moment))],
        )


@_type(17, "แรงกดที่ทำให้สว่านปั่นเกลียวกลับได้พอดี", DRILL_TOPIC)
class DrillBalancedPush(PhysicsSheet):
    def _variant(self, rng):
        turns = rng.randint(2, 6)
        mass = rng.randint(5, 20) / 10
        k = rng.randint(1, 4) / 10
        reach = rng.randint(20, 50) / 10
        kk, b = k * 1e-3, reach * 1e-2
        if b <= 4 * turns * pi * kk:
            raise _Clash
        f = q17.solve(turns=turns, mass=mass, k=k, reach=reach)
        return draw(
            17,
            measure(f),
            DRILL.format(M=f"{mass:g}", I=10, k=f"{k:g}") + f" พันเกลียว {turns} รอบ งานของแรงกดในช่วงคลายเกลียวเท่ากับ F₁ × {reach:g} cm ต้องกดด้วยแรงกี่นิวตัน ล้อตุ้นจึงปั่นเกลียวกลับได้ {turns} รอบเท่าเดิมแล้วหยุดพอดีโดยไม่ต้องกดชะลอ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"F_1b-2n\pi k(Mg+F_1)=2n\pi kMg",
            [
                measure(4 * turns * pi * kk * mass * 9.8 / b),
                measure(2 * turns * pi * kk * mass * 9.8 / (b - 2 * turns * pi * kk)),
                measure(8 * turns * pi * kk * mass * 9.8 / (b - 4 * turns * pi * kk)),
            ],
        )


@_type(18, "กำลังเฉลี่ยของผู้ใช้สว่านปั๊ม", DRILL_TOPIC)
class DrillPower(PhysicsSheet):
    def _variant(self, rng):
        force = rng.randint(5, 20)
        reach = rng.randint(20, 50) / 10
        turns = rng.randint(2, 6)
        mass = rng.randint(5, 20) / 10
        k = rng.randint(1, 4) / 10
        inertia = rng.randint(5, 30)
        p = q18.solve(force=force, reach=reach, turns=turns, mass=mass, k=k, inertia=inertia)
        return draw(
            18,
            measure(p),
            DRILL.format(M=f"{mass:g}", I=inertia, k=f"{k:g}") + f" พันเกลียว {turns} รอบ กดด้วยแรง {force} N ซึ่งทำงาน F₁ × {reach:g} cm ต่อรอบการทำงาน ความเร่งและความหน่วงเชิงมุมมีขนาดคงตัวเท่ากัน (kMg/I) กำลังเฉลี่ยของผู้ใช้เป็นกี่วัตต์ (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"t=4\sqrt{\frac{n\pi I}{kMg}},\quad P=\frac{F_1b}{t}",
            [measure(2 * p), measure(p * p * 1000), measure(p / 2)],
        )


@_type(19, "ค่าคงตัวทอร์กเสียดทานของใบสว่าน", DRILL_TOPIC)
class DrillBlade(PhysicsSheet):
    def _variant(self, rng):
        mu = rng.randint(15, 80) / 100
        radius = rng.randint(10, 60) / 10
        k = q19.solve(mu=mu, radius=radius)
        return draw(
            19,
            measure(k),
            f"หัวสว่านเป็นใบมีดบางยาว {2 * radius:g} mm หมุนรอบกึ่งกลาง แรงปฏิกิริยาจากเนื้อไม้กระจายสม่ำเสมอตามความยาว สัมประสิทธิ์ความเสียดทาน {mu:g} "
            "ถ้าทอร์กเสียดทานเท่ากับ k คูณแรงปฏิกิริยา ค่า k เป็นกี่มิลลิเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\tau=2\int_0^r\frac{\mu N}{2r}x\,dx",
            [measure(2 * mu * radius), measure(mu * radius), measure(mu * radius / 4)],
        )


DISTANCES = (21, 25, 31, 41, 55, 73)


@_type(20, "เลขชี้กำลังของตัวต้านทานไวแสงจากกราฟ log-log", LDR_TOPIC)
class LdrExponent(PhysicsSheet):
    def _variant(self, rng):
        gamma = -rng.randint(50, 80) / 100
        base = rng.randint(60, 120) * 10
        resistances = tuple(round(base * (x / 21) ** (-2 * gamma) * (1 + rng.choice((-0.01, 0, 0.01)))) for x in DISTANCES)
        g = q20.solve(distances=DISTANCES, resistances=resistances)
        table = ", ".join(f"({x} cm, {r} Ω)" for x, r in zip(DISTANCES, resistances))
        return draw(
            20,
            measure(g),
            f"วัดความต้านทาน LDR (R = c₁E^γ) ที่ระยะ x ต่าง ๆ จากหลอดไฟที่ประมาณเป็นแหล่งกำเนิดแบบจุด ได้ (x, R) {table} "
            "จากความชันของกราฟ log R กับ log x (วิธีกำลังสองน้อยที่สุด) ค่า γ เป็นเท่าใด (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E\propto\frac{1}{x^2}\Rightarrow\log R=-2\gamma\log x+c_2",
            [measure(-2 * g), measure(-g), measure(-4 * g)],
        )


@_type(21, "ฟลักซ์การส่องสว่างของหลอดไฟจาก LDR", LDR_TOPIC)
class LdrFlux(PhysicsSheet):
    def _variant(self, rng):
        gamma = -rng.randint(55, 75) / 100
        resistance = rng.randint(80, 300) * 10
        distance = rng.choice((25, 30, 35, 40))
        flux = q21.solve(gamma=gamma, resistance=resistance, distance=distance)
        c1 = 1e4 / 10**gamma
        E = flux / (4 * pi * (distance / 100) ** 2)
        return draw(
            21,
            measure(flux),
            f"LDR มี R = c₁E^γ โดย γ = {gamma:g} และ R = 1.0×10⁴ Ω เมื่อ E = 10 lux ที่ระยะ {distance} cm จากหลอดไฟ (แหล่งกำเนิดแบบจุด) วัด R ได้ {resistance} Ω "
            "ฟลักซ์การส่องสว่างของหลอดไฟเป็นกี่ลูเมน (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"E=\left(\frac{R}{c_1}\right)^{1/\gamma},\quad \Phi=E\cdot4\pi x^2",
            [measure(flux / 2), measure(E * (distance / 100) ** 2), measure((resistance / c1) ** gamma * 4 * pi * (distance / 100) ** 2)],
        )


@_type(22, "ความยาวคลื่นจากมุมของสเปกตรัมเกรตติง", LDR_TOPIC)
class GratingWavelength(PhysicsSheet):
    def _variant(self, rng):
        angle = rng.randint(15, 30)
        spacing = rng.choice((1.5, 1.6, 1.67))
        lam = q22.solve(angle=angle, spacing=spacing)
        t = radians(angle)
        return draw(
            22,
            measure(lam),
            f"แสงจากหลอดไฟผ่านเกรตติงจากแผ่น CD ที่มีระยะห่างร่อง {spacing:g} µm แถบสีหนึ่งในสเปกตรัมลำดับที่ 1 ทำมุม {angle}° กับแถบสว่างกลาง แสงนั้นมีความยาวคลื่นกี่นาโนเมตร (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"d\sin\theta=n\lambda",
            [measure(spacing * 1e3 * cos(t)), measure(spacing * 1e3 * sin(t) / 2), measure(spacing * 1e3 * tan(t))],
        )


@_type(23, "การตอบสนองสัมพัทธ์ของ LDR หลังปรับแก้กำลังแสง", LDR_TOPIC)
class LdrResponse(PhysicsSheet):
    def _variant(self, rng):
        first = rng.randint(180, 260) / 10000
        second = rng.randint(250, 400) / 10000
        power1 = rng.randint(50, 90)
        power2 = rng.randint(120, 200)
        ratio = q23.solve(first=first, power1=power1, second=second, power2=power2)
        return draw(
            23,
            measure(ratio),
            f"LDR วัด illuminance สัมพัทธ์ได้ {first:g} ที่ 494 nm และ {second:g} ที่ 651 nm ขณะที่กำลังแสงสัมพัทธ์ของหลอดไฟที่สองความยาวคลื่นเป็น {power1} และ {power2} "
            "หลังปรับแก้ให้เป็นค่าที่กำลังแสงเท่ากัน การตอบสนองของ LDR ที่ 651 nm เป็นกี่เท่าของที่ 494 nm (ตอบเลขนัยสำคัญ 3 ตัว)",
            r"\text{การตอบสนอง}\propto\frac{E_\lambda}{P_\lambda}",
            [measure(1 / ratio), measure(second / first), measure(second * power2 / (first * power1))],
        )
