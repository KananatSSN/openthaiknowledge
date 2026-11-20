"""Idempotent source claims for the 16 reviewed TPhO 6 (2550) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 2)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 3)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 3)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 4)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 5)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 6)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 7)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 8)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 9)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 10)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 11)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_theory_with_solution.pdf', 12)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 2), ('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 3), ('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 4)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 5)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 6)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 7), ('physics/level/upper-secondary/posn-physics/tpho-50-physics/tpho_6_exp.pdf', 8)],
}
UNITS = {
    1: ('sound-bar-travel-time', 'เสียงในแท่งของแข็งมีอัตราเร็ว √(Y/ρ) เวลาผ่านแท่งต่อกันเป็นผลรวมของ L/v ทุกท่อน ถ้าเวลาและความถี่เท่ากัน เฟสที่ออกมาก็เท่ากัน', 'เขียนเวลาเดินทางของแต่ละเส้นทางเป็น ΣL√(ρ/Y)', 'ตั้งเวลาเท่ากันแล้วแก้หาอัตราส่วนความยาว'),
    2: ('thick-plano-convex-lens', 'เลนส์นูนแกมระนาบที่แสงเข้าทางผิวระนาบหักเหที่ผิวโค้งเท่านั้น R = (n − 1)(D − t) แสงสะท้อนภายในจากผิวโค้งรวมที่ R/2 แล้วหักเหออกที่ผิวระนาบปรากฏที่ (R/2 − t)/n', 'ใช้การหักเหที่ผิวโค้งผิวเดียวหารัศมีความโค้ง', 'ใช้กระจกเว้าและความลึกปรากฏที่ผิวระนาบ'),
    3: ('thick-plano-convex-lens', '', '', ''),
    4: ('adiabatic-piston-drop', 'ลูกสูบที่ตกอัดแก๊สแบบแอเดียแบติกจนหยุดชั่วขณะ: พลังงานศักย์ที่ลดลงเท่ากับพลังงานภายในที่เพิ่ม (5/2)nRΔT และ TV^(γ−1) คงที่', 'เขียนการอนุรักษ์พลังงานจากตำแหน่งเริ่มถึงตำแหน่งต่ำสุด', 'ใช้ความสัมพันธ์แอเดียแบติกหา T แล้วแก้หาอัตราส่วนมวล'),
    5: ('rod-and-wheel-emf', 'แท่งตัวนำที่เคลื่อนที่ให้ vBℓ แท่งที่หมุนรอบปลายให้ ½Bωℓ² ซี่ล้อหลายซี่ต่อขนานกันให้ ½ωBr₀² และวงล้อที่ถูกมวลถ่วงเข้าสู่ ω_f = 4MgR/(B²r₀³)', 'อินทิเกรต vB ตามความยาวแท่ง', 'สมดุลกำลังหรือทอร์กของมวลถ่วงกับแรงแม่เหล็ก'),
    6: ('rod-and-wheel-emf', '', '', ''),
    7: ('rod-and-wheel-emf', '', '', ''),
    8: ('rod-and-wheel-emf', '', '', ''),
    9: ('roller-block-incline', 'ทรงกระบอกแกนลื่นผูกกับกล่องบนพื้นเอียง: เมื่อสถิต แรงเสียดทานอยู่ที่กล่องเท่านั้น F อยู่ระหว่าง (m₁ + m₂)g sin θ ∓ μ_s m₂ g cos θ เมื่อถูกดึงขึ้นด้วยมวลแขวน ทรงกระบอกที่กลิ้งเพิ่มมวลยังผล I/r² และต้องการ μ_s ≥ a/(2g cos θ)', 'เขียนกฎของนิวตันของทรงกระบอก กล่อง และมวลแขวน', 'ใช้สมการทอร์กของทรงกระบอกหาแรงเสียดทานที่ต้องการ'),
    10: ('roller-block-incline', '', '', ''),
    11: ('roller-block-incline', '', '', ''),
    12: ('roller-block-incline', '', '', ''),
    13: ('thermistor-b-constant', 'ความต้านทานเทอร์มิสเตอร์ R = R₀ exp[B(1/T − 1/T₀)] ทำให้ ln R เป็นเส้นตรงกับ 1/T ที่มีความชัน B (T เป็นเคลวิน)', 'วัดความต้านทานที่หลายอุณหภูมิ', 'เขียนกราฟ ln R กับ 1/T แล้วหาความชัน'),
    14: ('spring-and-beam-oscillation', 'คาบของมวลบนสปริง T = 2π√((M + m_s)/k) ทำให้ T² เป็นเส้นตรงกับ M: k = 4π²/ความชัน และ m_s = จุดตัด/ความชัน คานที่ปลายหนึ่งหมุนได้อีกปลายแขวนสปริงมีคาบ 2π√(M/3k)', 'เขียนกราฟ T² กับ M', 'อ่านความชันและจุดตัด หรือใช้คาบของคานหามวล'),
    15: ('spring-and-beam-oscillation', '', '', ''),
    16: ('spring-and-beam-oscillation', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2550_physics/sheet.json").read_text("utf-8"))
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
