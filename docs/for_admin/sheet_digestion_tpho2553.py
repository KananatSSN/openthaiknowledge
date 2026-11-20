"""Idempotent source claims for the 14 reviewed TPhO 9 (2553) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 1)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 2)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 3)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 4)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 5)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 6)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 7)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 8)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 9)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 10), ('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 11), ('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 12)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_theory_with_solution.pdf', 12)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_exp.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_exp.pdf', 2), ('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_exp.pdf', 3)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_exp.pdf', 4)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-53-physics/tpho_9_exp.pdf', 5)],
}
UNITS = {
    1: ('wall-shuttle-collisions', 'มวลหนักชนมวลเบาที่ไป-กลับระหว่างมวลหนักกับผนังแบบยืดหยุ่น: ระยะการชนแต่ละครั้งสัมพันธ์กันด้วย ℓₙ(vₙ + Vₙ) = ℓ₀V₀ และเมื่อ M ≫ m มวลหนักเข้าใกล้ผนังที่สุดประมาณ ℓ₀√(m/M)', 'หาความเร็วหลังชนแต่ละครั้งจากการชนยืดหยุ่น', 'ใช้ระยะทางรวมที่ทั้งสองไถลหาตำแหน่งการชนครั้งถัดไป'),
    2: ('wall-shuttle-collisions', '', '', ''),
    3: ('wall-shuttle-collisions', '', '', ''),
    4: ('wall-shuttle-collisions', '', '', ''),
    5: ('double-piston-gas', 'ลูกสูบคู่พื้นที่ A และ a ที่เชื่อมกัน สมดุลเมื่อ (P₀ − Pₐ)(A − a) = Mg เมื่อร้อนขึ้นช้า ๆ ความดันคงที่ ลูกสูบเลื่อน RΔT/(Pₐ(A − a) + Mg) เมื่อเป็นฉนวน การกดลงเล็กน้อยให้แรงคืนตัว P₀γ(A − a)²y/V₀ และสั่นแบบฮาร์มอนิก', 'เขียนสมดุลแรงบนลูกสูบทั้งคู่', 'ใช้กระบวนการความดันคงที่หรือแอเดียแบติกหาการเลื่อนหรือแรงคืนตัว'),
    6: ('double-piston-gas', '', '', ''),
    7: ('double-piston-gas', '', '', ''),
    8: ('double-piston-gas', '', '', ''),
    9: ('voltage-doubler', 'วงจรทวีแรงดันจากตัวเก็บประจุสองตัวและไดโอดสองตัว: ไดโอดล่างตรึงศักย์จุด b ไม่ให้ต่ำกว่าศูนย์ ไดโอดบนแบ่งประจุระหว่างตัวเก็บประจุทั้งสองเมื่อศักย์ b สูงกว่า d จนในที่สุด V_d = 2V₀', 'พิจารณาสถานะไดโอดจากศักย์ที่ปลายทั้งสอง', 'ใช้การอนุรักษ์ประจุที่จุดต่อและกฎของเคอร์ชอฟฟ์หาประจุใหม่'),
    10: ('double-star-interferometer', 'แสงจากดาวที่มุม ±α ผ่านสลิตคู่ให้ริ้วเลื่อนสวนกัน ริ้วหายเมื่อ 2d sin α = (n + ½)λ ระยะสลิตสองค่าที่ริ้วหายต่อเนื่องกันให้ 2α ≈ λ/(d₁ − d₀)', 'เขียนผลต่างเส้นทางแสง d sin α + d sin β ของดาวแต่ละดวง', 'ตั้งแถบสว่างของดวงหนึ่งทับแถบมืดของอีกดวงแล้วแก้หา α'),
    11: ('double-star-interferometer', '', '', ''),
    12: ('brewster-polarisation', 'ที่มุมบริวสเตอร์แสงสะท้อนและแสงหักเหตั้งฉากกัน tan θ_B = n แสงสะท้อนโพลาไรซ์ตั้งฉากกับระนาบตกกระทบ จึงใช้หาดัชนีหักเหของของเหลวได้', 'ใช้กฎของสเนลล์กับเงื่อนไขมุม 90°', 'วัดมุมที่แสงโพลาไรซ์ขนานสะท้อนน้อยที่สุดแล้วหา n = tan θ_B'),
    13: ('brewster-polarisation', '', '', ''),
    14: ('seiche-models', 'การกระเพื่อมของน้ำในอ่างลึก H ยาว L ตามแบบจำลองศูนย์กลางมวลเลื่อนซ้ายขวามีคาบ 2π√(L²/(12gH)) เทียบกับแบบจำลองลูกตุ้มและกระดานกระดก', 'เขียนคาบของแต่ละแบบจำลอง', 'เปรียบเทียบกับคาบที่วัดได้ด้วยกราฟเส้นตรง'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2553_physics/sheet.json").read_text("utf-8"))
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
