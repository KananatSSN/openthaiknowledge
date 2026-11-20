"""Idempotent source claims for the 29 reviewed TPhO 20 (2564) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 3)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 2), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 4)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 5)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 5)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 6), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 7)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 8)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 9)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 10)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 11)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 12), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 13), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 15)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 14)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 16)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 17)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 18)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 19), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 20)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 21), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 22)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 23)],
    18: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 24)],
    19: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 25)],
    20: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 26), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 27)],
    21: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 28)],
    22: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 29)],
    23: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 30)],
    24: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_theory.pdf', 31)],
    25: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 2), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 3)],
    26: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 4)],
    27: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 5), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 6)],
    28: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 7), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 8), ('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 9)],
    29: [('physics/level/upper-secondary/posn-physics/tpho-64-physics/tpho2021_experiment.pdf', 9)],
}
UNITS = {
    1: ('rolling-tube-half-cylinder', 'ท่อกลวงกลิ้งบนพื้นเอียง: a = ½g sin θ cos φ และต้องการ μ ≥ ½tan θ √(1 + 3 sin²φ) ครึ่งทรงกระบอกหลวมภายในไม่หมุนจึงได้ a = ((m′ + m)/(2m′ + m))g sin θ ส่วนเมื่อเชื่อมติดกัน จุดศูนย์กลางมวล k′R ทำให้ต้องเอียงอย่างน้อย sin⁻¹(k′ sin θ₀) และพลังงาน ความเร็วเชิงมุม และแรงตั้งฉากหาได้จากโมเมนต์ความเฉื่อยรอบจุดสัมผัส', 'เขียนกฎของนิวตันกับทอร์กหรือพลังงานรอบจุดสัมผัส', 'ใช้เงื่อนไขกลิ้งไม่ไถลหาความเร่ง แรงเสียดทาน มุม หรือแรงตั้งฉาก'),
    2: ('rolling-tube-half-cylinder', '', '', ''),
    3: ('rolling-tube-half-cylinder', '', '', ''),
    4: ('rolling-tube-half-cylinder', '', '', ''),
    5: ('rolling-tube-half-cylinder', '', '', ''),
    6: ('rolling-tube-half-cylinder', '', '', ''),
    7: ('rolling-tube-half-cylinder', '', '', ''),
    8: ('rolling-tube-half-cylinder', '', '', ''),
    9: ('child-langmuir-diode', 'ไดโอดสุญญากาศ: อิเล็กตรอนเดี่ยวได้พลังงาน exV_d/d ส่วนที่สภาวะคงตัว I = ρva² กับสมการปัวซองให้ V = kx^(4/3) กระแสจำกัดด้วยประจุสเปซ I = (4ε₀a²/9d²)√(2e/m)V_d^(3/2) ประจุสเปซรวม −(4/3)ε₀a²V_d/d และแอโนดมีประจุ +(4/3)ε₀V_d/d ต่อพื้นที่', 'รวมสมการกระแส การอนุรักษ์พลังงาน และสมการปัวซอง', 'แก้หากระแส ศักย์ ประจุสเปซ และประจุที่ขั้ว'),
    10: ('child-langmuir-diode', '', '', ''),
    11: ('child-langmuir-diode', '', '', ''),
    12: ('child-langmuir-diode', '', '', ''),
    13: ('child-langmuir-diode', '', '', ''),
    14: ('breathing-lung-work', 'กลไกการหายใจ: ปอดเป็นไปตาม p_D = (1/k)ln(α/(α − V)) งานขยายเนื้อเยื่อ ∫p_D dV = (α/k)[1 − e^(−kp)(1 + kp)] กะบังลมใช้พลังงานราว 2% ของอัตราการเผาผลาญ และอากาศในปอดได้ความร้อน (5/2)p_DV + w', 'หาผลต่างความดันจากปริมาตรแล้วอินทิเกรตหางาน', 'ใช้กฎข้อหนึ่งของเทอร์โมไดนามิกส์หาพลังงานภายในและความร้อน'),
    15: ('breathing-lung-work', '', '', ''),
    16: ('breathing-lung-work', '', '', ''),
    17: ('breathing-lung-work', '', '', ''),
    18: ('breathing-lung-work', '', '', ''),
    19: ('breathing-lung-work', '', '', ''),
    20: ('bilens-interference', 'ไบเลนส์: สองส่วนของเลนส์ที่ตัดกลางออกมีศูนย์กลางเลื่อน ±a/2 ให้ภาพเสมือนสองภาพที่ |v| = uf/(f − u) ห่างกัน au/(f − u) เมื่อแหล่งกำเนิดอยู่ที่โฟกัส ลำแสงขนานตัดกันที่มุม a/f ริ้วห่าง λf/a หายไปที่ f(D − a)/a และมีมากที่สุด (D − a)a/(2λf) ริ้ว', 'ใช้สมการเลนส์บางกับศูนย์กลางที่เลื่อนหาภาพสองภาพ', 'ใช้การแทรกสอดของสองแหล่งหรือสองลำแสงขนานหาระยะริ้วและจำนวนริ้ว'),
    21: ('bilens-interference', '', '', ''),
    22: ('bilens-interference', '', '', ''),
    23: ('bilens-interference', '', '', ''),
    24: ('bilens-interference', '', '', ''),
    25: ('cantilever-beam', 'คานยื่น: การโก่งเชิงเส้น Δy = L³(3μLg + 8mg)/(2Ebh³) ให้ E จากคานเปล่าหรือความชันของกราฟ Δy กับ m ความชันเฉลี่ยที่เปลี่ยนเกิน 10% บอกช่วงไม่เชิงเส้น และคาบการสั่น T² = 16π²L³(aμL + m)/(Ebh³) ให้ E และมวลสมมูล aμL', 'วัดการโก่งหรือคาบการสั่นที่มวลปลายคานต่าง ๆ', 'เขียนกราฟเส้นตรงหา E จากความชันและมวลสมมูลจากจุดตัดแกน'),
    26: ('cantilever-beam', '', '', ''),
    27: ('cantilever-beam', '', '', ''),
    28: ('cantilever-beam', '', '', ''),
    29: ('cantilever-beam', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2564_physics/sheet.json").read_text("utf-8"))
    for item in sheet["items"]:
        slug, statement, first, second = UNITS[item["number"]]
        path = ROOT / "otk/knowledge/physics" / f"{slug}.json"
        raw = (
            json.loads(path.read_text("utf-8"))
            if path.exists()
            else {
                "subject": sheet["subject"],
                "topic": item["topic"],
                "level": sheet["level"],
                "units": [],
            }
        )
        uid = f"phys.{slug.replace('-', '_')}.procedure"
        unit = next((u for u in raw["units"] if u["id"] == uid), None)
        if unit is None:
            assert statement and first and second
            unit = {
                "id": uid,
                "kind": "procedure",
                "title": item["title"],
                "statement": statement,
                "steps": [first, second],
                "sources": [],
                "covered_by": [],
                "note": item["note"],
            }
            raw["units"].append(unit)
        for sheet_path, digest_item in SOURCES[item["number"]]:
            source = {"sheet": sheet_path, "item": digest_item}
            if source not in unit["sources"]:
                unit["sources"].append(source)
        if item["generator"] not in unit["covered_by"]:
            unit["covered_by"].append(item["generator"])
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", "utf-8")


if __name__ == "__main__":
    main()
