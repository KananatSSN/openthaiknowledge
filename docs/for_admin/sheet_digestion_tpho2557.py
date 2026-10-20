"""Idempotent source claims for the 17 reviewed TPhO 13 (2557) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 1), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 2)],
    2: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 3), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 4)],
    3: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 5)],
    4: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 6)],
    5: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 7)],
    6: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 8)],
    7: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 9)],
    8: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 10), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 11), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 12), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 13), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 14)],
    9: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 15)],
    10: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 16), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 17)],
    11: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 18), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 19), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 20), ('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 21)],
    12: [('สอวน_physics/tpho-57-physics/tpho_13_theory.pdf', 22)],
    13: [('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 1)],
    14: [('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 2), ('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 3)],
    15: [('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 3)],
    16: [('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 4)],
    17: [('สอวน_physics/tpho-57-physics/tpho_13_exp.pdf', 4)],
}
UNITS = {
    1: ('wedge-film-fringes', 'แสงสะท้อนจากผิวบนและผิวล่างของลิ่มใสแทรกสอดเสริมกันเมื่อ 2ny = (N + ½)λ ริ้วห่างกัน λ/(2n tan θ) เมื่อลิ่มขยายตัว ริ้วเลื่อนไปทางด้านบาง จำนวนริ้วที่เลื่อนให้สัมประสิทธิ์การขยายตัว α = λΔN/(2nL₀ΔT tan θ)', 'เขียนผลต่างทางเดินแสงพร้อมการกลับเฟสที่ผิวหนึ่ง', 'แปลงความหนาเป็นตำแหน่งตามลิ่มแล้วนับริ้วที่เลื่อน'),
    2: ('wedge-film-fringes', '', '', ''),
    3: ('passing-source-doppler', 'แหล่งกำเนิดเสียงที่วิ่งผ่านผู้สังเกต: เสียงที่ได้ยินขณะแหล่งกำเนิดอยู่ใกล้ที่สุดถูกปล่อยมาจากตำแหน่งที่ cos θ = u/v ได้ f = f₀v²/(v² − u²) และได้ยิน f₀ เมื่อแหล่งกำเนิดเลยไปแล้ว uL/v ห่าง L√(u² + v²)/v', 'หาตำแหน่งที่ปล่อยเสียงจากเวลาที่เสียงเดินทาง', 'ใช้องค์ประกอบความเร็วตามแนวเส้นสายตาในสูตรดอปเพลอร์'),
    4: ('passing-source-doppler', '', '', ''),
    5: ('one-wheeled-table', 'โต๊ะที่มีล้อเพียงขาเดียวไถลบนพื้น: สมดุลทอร์กรอบศูนย์กลางมวลกระจายแรงกดให้ขาที่ลากต่างกันตามทิศ ความหน่วง wgμ/(2(w ∓ μh)) จึงต่างกันเมื่อกลับทิศ และโต๊ะไม่ล้มเมื่อ μ < w/(2h)', 'เขียนสมดุลแรงแนวดิ่งและทอร์กรอบศูนย์กลางมวล', 'หาความหน่วงและระยะหยุด หรือเงื่อนไขแรงกดที่ล้อเป็นศูนย์'),
    6: ('one-wheeled-table', '', '', ''),
    7: ('one-wheeled-table', '', '', ''),
    8: ('water-hammer-ram', 'ตะบันน้ำ: น้ำไหลด้วย u = √(2gh₀) แล้วถูกหยุดกะทันหัน รอยต่อเคลื่อนย้อนด้วยอัตราเร็วเสียง v = √(B/ρ) ความดันเพิ่ม ρvu + ρu² ≈ ρvu และดันน้ำขึ้นได้สูง vu/g + u²/g', 'หาปริมาตรที่หยุดและโมเมนตัมที่เปลี่ยนในเวลา Δt', 'แปลงการดลเป็นความดันแล้วเทียบกับมอดุลัสเชิงปริมาตรและความดันของลำน้ำ'),
    9: ('water-hammer-ram', '', '', ''),
    10: ('water-hammer-ram', '', '', ''),
    11: ('moving-dielectric-emf', 'ไดอิเล็กทริกที่เคลื่อนที่ด้วย v ในสนามแม่เหล็ก B รู้สึกสนามยังผล vB สนามภายในเหลือ vB/εᵣ ประจุโพลาไรเซชันให้สนาม vB(1 − 1/εᵣ) ในทิศตรงข้าม และอีเอ็มเอฟคร่อมแผ่นขนาน vBd(1 − 1/εᵣ)', 'หาสนามยังผลจากแรงลอเรนซ์ต่อประจุ', 'แยกสนามโพลาไรเซชันออกจากสนามรวมในไดอิเล็กทริก'),
    12: ('moving-dielectric-emf', '', '', ''),
    13: ('eddy-current-brake', 'ล้อแม่เหล็กที่กลิ้งบนแถบตัวนำเป็นจานฟาราเดย์ V = vB(R² − R₀²)/R แม่เหล็กที่ไถลบนแผ่นตัวนำถูกหน่วงด้วย −bv ความเร็วปลายให้ v_T/cos θ = (mg/b)(tan θ − μ) และ b = σΛ กับ Λ = kdD²B²', 'เขียนกราฟเส้นตรง V² กับ a หรือ v_T/cos θ กับ tan θ', 'อ่านความชันและจุดตัดแกนหาสนามแม่เหล็ก b, μ, σ และ k'),
    14: ('eddy-current-brake', '', '', ''),
    15: ('eddy-current-brake', '', '', ''),
    16: ('eddy-current-brake', '', '', ''),
    17: ('eddy-current-brake', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2557_physics/sheet.json").read_text("utf-8"))
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
