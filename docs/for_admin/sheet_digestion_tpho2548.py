"""Idempotent source claims for the 19 reviewed TPhO 4 (2548) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 1)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 1)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 2)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 3)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 3)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 4)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 5)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 6)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 7)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 8)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 9)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 10)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 11)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 12)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 13)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/tpho_4_theory_with_solution.pdf', 14)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/thpo_4_exp.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-48-physics/thpo_4_exp.pdf', 2), ('physics/level/upper-secondary/posn-physics/tpho-48-physics/thpo_4_exp.pdf', 3)],
    18: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/thpo_4_exp.pdf', 4)],
    19: [('physics/level/upper-secondary/posn-physics/tpho-48-physics/thpo_4_exp.pdf', 5)],
}
UNITS = {
    1: ('elastic-collision-1d', 'การชนยืดหยุ่นหนึ่งมิติอนุรักษ์โมเมนตัมและพลังงานจลน์ ให้ v_B = (2M_Au_A + (M_B − M_A)u_B)/(M_A + M_B) และ v_A = (2M_Bu_B + (M_A − M_B)u_A)/(M_A + M_B)', 'เขียนการอนุรักษ์โมเมนตัมและพลังงานจลน์', 'ใช้ u_A − u_B = v_B − v_A แล้วแก้หาความเร็วหลังชน'),
    2: ('elastic-collision-1d', '', '', ''),
    3: ('elastic-energy-transfer', 'มวลที่หยุดนิ่งรับพลังงาน 4M_AM_B/(M_A + M_B)² ของพลังงานมวลที่ชน การส่งผ่านมวลตัวกลางได้มากที่สุดเมื่อ m = √(M_AM_B) และการชนซ้ำกับมวลใหญ่ลดพลังงานลงตัวประกอบ ((M − m)/(M + m))² ต่อครั้ง', 'หาสัดส่วนพลังงานต่อการชนหนึ่งครั้ง', 'คูณสัดส่วนของการชนต่อเนื่องแล้วหาค่าสูงสุดหรือจำนวนครั้ง'),
    4: ('elastic-energy-transfer', '', '', ''),
    5: ('elastic-energy-transfer', '', '', ''),
    6: ('elastic-energy-transfer', '', '', ''),
    7: ('proton-square-potential', 'งานที่ใช้จัดประจุคือผลรวม kq²/r ของทุกคู่ ศักย์ภายในสี่เหลี่ยมโปรตอนต่ำสุดที่จุดกลาง และพลังงานศักย์ของโพสิตรอนบนแกนผ่านกลางมีสองยอดใกล้ ±0.39a', 'รวมพลังงานศักย์หรือศักย์ไฟฟ้าจากประจุแต่ละตัว', 'หาค่าสูงสุดหรือต่ำสุดตามเส้นทางแล้วใช้การอนุรักษ์พลังงาน'),
    8: ('proton-square-potential', '', '', ''),
    9: ('proton-square-potential', '', '', ''),
    10: ('proton-square-potential', '', '', ''),
    11: ('proton-square-oscillation', 'ใกล้จุดกลางของสี่เหลี่ยมโปรตอน แรงต่อโพสิตรอนเป็น −(4√2ke²/a³)x ทุกทิศทาง จึงสั่นด้วย ω = √(4√2ke²/(a³mₑ))', 'กระจายแรงหรือพลังงานศักย์รอบจุดสมดุลถึงอันดับหนึ่ง', 'เทียบกับสมการการสั่นแบบฮาร์มอนิกอย่างง่าย'),
    12: ('radial-flow-between-discs', 'อากาศจากท่อรัศมี a ที่แผ่ออกระหว่างแผ่นกลมห่าง t มีความเร็ว v = a²v₀/(2tr) ความดันต่ำกว่าบรรยากาศตามแบร์นูลลี ทำให้เกิดแรงยก πρK²[ln(R/a) − 1/2 + a²/(2R²)] หักแรงจากโมเมนตัมของลม ρπa²v₀²', 'ใช้สมการความต่อเนื่องและแบร์นูลลีหาความเร็วและความดัน', 'อินทิเกรตความดันบนวงแหวนแล้วหักแรงจากการเปลี่ยนโมเมนตัม'),
    13: ('radial-flow-between-discs', '', '', ''),
    14: ('radial-flow-between-discs', '', '', ''),
    15: ('radial-flow-between-discs', '', '', ''),
    16: ('radial-flow-between-discs', '', '', ''),
    17: ('foil-capacitor-dielectric', 'ตัวเก็บประจุแผ่นขนานบนไฟฟ้ากระแสสลับมี I = VωC เมื่อ X_C ≫ R และ C = (κε₀/d)A จึงหา κε₀/d จากความชันของ C กับพื้นที่ และหา κ เมื่อรู้ความหนา', 'วัดกระแสและแรงดันที่พื้นที่ต่าง ๆ แล้วคำนวณ C', 'หาความชันของ C กับ A แล้วคูณด้วย d/ε₀'),
    18: ('foil-capacitor-dielectric', '', '', ''),
    19: ('reflection-grating-ruler', 'แสงเลเซอร์ที่สะท้อนจากขีดสเกลห่าง d ที่มุมเฉียด ให้จุดสว่างเมื่อ d cos θ − d cos φ = nλ', 'หามุมของจุดสว่างจากความสูงบนฉากและระยะฉาก', 'แทนในเงื่อนไขการแทรกสอดหา λ'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2548_physics/sheet.json").read_text("utf-8"))
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
