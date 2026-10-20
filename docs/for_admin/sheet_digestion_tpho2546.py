"""Idempotent source claims for the 21 reviewed TPhO 2 (2546) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 1)],
    2: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 1)],
    3: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 2)],
    4: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 3)],
    5: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 4)],
    6: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 5)],
    7: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 6)],
    8: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 7)],
    9: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 8), ('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 9)],
    10: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 10)],
    11: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 11)],
    12: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 12)],
    13: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 13)],
    14: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 14), ('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 15)],
    15: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 16)],
    16: [('สอวน_physics/tpho-46-physics/tpho_2_theory.pdf', 17)],
    17: [('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 1)],
    18: [('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 2), ('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 3), ('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 4)],
    19: [('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 5)],
    20: [('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 5)],
    21: [('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 6), ('สอวน_physics/tpho-46-physics/tpho_2_exp.pdf', 7)],
}
UNITS = {
    1: ('sliding-mass-free-cylinder', 'มวล m ไถลบนทรงกระบอกลื่นมวล M ที่เลื่อนบนพื้นลื่นได้ โมเมนตัมแนวระดับอนุรักษ์ m(v cos θ − V) = MV ร่วมกับพลังงานให้ v² = 2gR(M+m)(1−cos θ)/(M + m sin²θ)', 'เขียนความเร็วของมวลเทียบพื้นจาก v และ V', 'ใช้การอนุรักษ์โมเมนตัมแนวระดับและพลังงานแล้วแก้หา v และ V'),
    2: ('sliding-mass-free-cylinder', '', '', ''),
    3: ('sliding-mass-free-cylinder', '', '', ''),
    4: ('detach-from-free-cylinder', 'ในกรอบของทรงกระบอกที่เร่ง มวลหลุดจากผิวเมื่อแรงปฏิกิริยาเป็นศูนย์ ทรงกระบอกที่เลื่อนได้ทำให้มวลหลุดที่มุมเล็กกว่า cos⁻¹(2/3) ของทรงกระบอกที่ถูกยึด', 'เขียนกฎข้อสองตามแนวรัศมีพร้อมแรงเทียม m dV/dt', 'ตั้ง N = 0 แล้วเทียบกับกรณีทรงกระบอกถูกยึด'),
    5: ('fuse-joule-heating', 'ลวดที่ไม่เสียความร้อนมีอุณหภูมิเพิ่มในอัตรา dT/dt = i²ρ/(π²r⁴cD) ไม่ขึ้นกับความยาวลวด', 'หากำลัง i²R ด้วย R = ρℓ/(πr²)', 'หารด้วยความจุความร้อน cDπr²ℓ'),
    6: ('fuse-joule-heating', '', '', ''),
    7: ('fuse-heat-loss-balance', 'ลวดที่เสียความร้อน α·2πrℓ(T − Tₐ) มี dT/dt = i²ρ/(π²r⁴cD) − 2α(T − Tₐ)/(crD) อุณหภูมิเข้าสู่ Tₐ + i²ρ/(2απ²r³) และละลายเมื่อค่านี้เกินจุดหลอมเหลว', 'เขียนสมดุลพลังงาน กำลังเข้า − กำลังสูญเสีย = mc dT/dt', 'ตั้ง dT/dt = 0 หาอุณหภูมิสุดท้ายแล้วเทียบกับจุดหลอมเหลว'),
    8: ('fuse-heat-loss-balance', '', '', ''),
    9: ('fuse-heat-loss-balance', '', '', ''),
    10: ('uniform-ball-potential', 'ภายในทรงกลมประจุสม่ำเสมอ ชั้นบางให้ศักย์ ρξδξ/ε₀ คงที่ ชั้นนอกรวมกันได้ ρ(R²−r²)/(2ε₀) ประจุภายในให้ ρr²/(3ε₀) ศักย์รวม (ρ/2ε₀)(R² − r²/3)', 'แบ่งทรงกลมเป็นชั้นบางภายนอกและก้อนภายในรัศมี r', 'อินทิเกรตศักย์ของชั้นนอกแล้วบวกศักย์ของก้อนภายใน'),
    11: ('uniform-ball-potential', '', '', ''),
    12: ('uniform-ball-potential', '', '', ''),
    13: ('uniform-ball-potential', '', '', ''),
    14: ('ball-with-point-charges', 'ศักย์และสนามในทรงกลมประจุสม่ำเสมอที่มีจุดประจุ −q′ หาได้จากการซ้อนทับ สนามของทรงกลมภายในคือ ρr/(3ε₀) ประจุ −q′ สองตัวที่ ±r₀ สมดุลเมื่อ r₀³ = 3q′/(16πρ)', 'ซ้อนทับศักย์ของทรงกลมกับศักย์ของจุดประจุ', 'หาสนามจาก E = −dV/dr แล้วตั้งสนามรวมเป็นศูนย์'),
    15: ('ball-with-point-charges', '', '', ''),
    16: ('ball-with-point-charges', '', '', ''),
    17: ('rc-capacitor-rms-line', 'ในวงจร RC อนุกรม ความต่างศักย์ยังผลคร่อมตัวเก็บประจุคือ ℰ₀/(√2·√(1+ω²R²C²)) ดังนั้น 1/V_C² เป็นเส้นตรงกับ R² และ C = √(ความชัน/จุดตัด)/ω', 'เขียนอิมพีแดนซ์และแบ่งแรงดันให้ตัวเก็บประจุ', 'จัดรูปเป็นเส้นตรงของ 1/V_C² กับ R² แล้วอ่านความชันและจุดตัด'),
    18: ('rc-capacitor-rms-line', '', '', ''),
    19: ('bifilar-black-box', 'ลูกบาศก์ที่แขวนด้วยเชือกสองเส้นแกว่งบิดด้วย T² = 16π²Iℓ/(m₀gd²) โพรงทรงกลมให้ I เท่ากันทุกแบบการแขวน ส่วนโพรงทรงกระบอกให้ I ต่างกันและบอกรัศมีโพรงได้', 'หาโมเมนต์ความเฉื่อยจากคาบในแต่ละแบบการแขวน', 'เทียบค่าทั้งสองเพื่อแยกรูปร่างโพรงแล้วแก้สูตร I หารัศมี'),
    20: ('bifilar-black-box', '', '', ''),
    21: ('bifilar-black-box', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2546_physics/sheet.json").read_text("utf-8"))
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
