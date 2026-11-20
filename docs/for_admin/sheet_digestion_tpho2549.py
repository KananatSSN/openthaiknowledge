"""Idempotent source claims for the 14 reviewed TPhO 5 (2549) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 1)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 2)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 3)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 4)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 5)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 6)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 7)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 8)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 9)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 10)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 11)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 12), ('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 13), ('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 14), ('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 15)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 16), ('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 17)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-49-physics/tpho_5_theory_with_solution_and_exp.pdf', 18)],
}
UNITS = {
    1: ('convex-concave-lens-pair', 'เลนส์นูนกับเลนส์เว้าความยาวโฟกัส f เท่ากันห่างกัน L < f รวมแสงขนานที่ระยะ f(f − L)/L หลังเลนส์เว้า', 'หาภาพจากเลนส์นูนแล้วใช้เป็นวัตถุของเลนส์เว้า', 'บวกระยะห่าง L เพื่อวัดจากเลนส์นูน'),
    2: ('rolling-without-slipping-friction', 'วัตถุกลมที่ I = kmR² กลิ้งลงพื้นเอียงโดยไม่ไถลเมื่อ μ ≥ tan θ · k/(1 + k) (ทรงกระบอกตัน 1/3 tan θ)', 'เขียนสมการการเลื่อนที่และการหมุนพร้อมเงื่อนไขกลิ้ง', 'หาแรงเสียดทานที่ต้องการแล้วเทียบกับ μN'),
    3: ('rolling-ball-loop', 'ทรงกลมตันเล็กที่กลิ้งผ่านรางวงกลมรัศมี R ต้องเริ่มสูงอย่างน้อย 2.7R และที่ระดับศูนย์กลางรางแรงปฏิกิริยาเป็น (10/7)mg(h − R)/R', 'ใช้เงื่อนไขแรงสู่ศูนย์กลางที่จุดสูงสุดหรือที่ข้างราง', 'ใช้การอนุรักษ์พลังงานรวมพลังงานจลน์การหมุน (7/10)mv²'),
    4: ('rolling-ball-loop', '', '', ''),
    5: ('diving-bell-caisson', 'ถังคว่ำที่หย่อนลงน้ำบีบอากาศตามกฎของบอยล์ ระดับน้ำในถังบอกความลึก ไล่น้ำออกหมดต้องเพิ่มอากาศเป็น ρgh/P_a เท่าของเดิม และถังต้องมีมวลอย่างน้อย ρLA', 'สมดุลความดันอากาศในถังกับความดันน้ำที่ระดับผิวน้ำในถัง', 'ใช้ PV = nRT ที่อุณหภูมิคงที่และสมดุลแรงบนถัง'),
    6: ('diving-bell-caisson', '', '', ''),
    7: ('diving-bell-caisson', '', '', ''),
    8: ('thomson-atom-oscillator', 'ในอะตอมแบบทอมสัน อิเล็กตรอนในทรงกลมประจุสม่ำเสมอสั่นแบบฮาร์มอนิกด้วย ω² = Qe/(4πε₀mR³) อิเล็กตรอนสองตัวสมดุลที่ x = (e/4Q)^(1/3)R และสั่นสวนกันด้วย ω² = 3Qe/(4πε₀mR³)', 'ใช้กฎของเกาส์หาสนามภายในทรงกลม', 'ตั้งสมการการเคลื่อนที่หรือสมดุลรวมแรงผลักระหว่างอิเล็กตรอน'),
    9: ('thomson-atom-oscillator', '', '', ''),
    10: ('thomson-atom-oscillator', '', '', ''),
    11: ('thomson-atom-oscillator', '', '', ''),
    12: ('prism-minimum-deviation', 'ที่มุมเบี่ยงเบนน้อยที่สุด ดัชนีหักเหของปริซึมคือ n = sin((A + D_m)/2)/sin(A/2)', 'วัดมุมเบี่ยงเบนที่มุมตกกระทบต่าง ๆ หาค่าน้อยสุด', 'แทนมุมยอดและมุมเบี่ยงเบนน้อยสุดในสูตร'),
    13: ('steelyard-archimedes', 'ตาชั่งจีนอ่านมวลจากสมดุลโมเมนต์ m = M(x − x₀)/d และใช้ชั่งน้ำหนักที่หายไปในน้ำและของเหลวเพื่อหาความถ่วงจำเพาะ (W − W_l)/(W − W_w)', 'เทียบขีดศูนย์แล้วอ่านตำแหน่งตุ้มเลื่อน', 'ใช้หลักอาร์คิมีดีสเทียบน้ำหนักที่หายไป'),
    14: ('steelyard-archimedes', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2549_physics/sheet.json").read_text("utf-8"))
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
