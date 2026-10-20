"""Idempotent source claims for the 22 reviewed TPhO 17 (2561) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 1)],
    2: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 2)],
    3: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 3)],
    4: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 4), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 5)],
    5: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 6)],
    6: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 7), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 8)],
    7: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 9), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 10)],
    8: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 11), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 12), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 13)],
    9: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 14)],
    10: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 15)],
    11: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 16)],
    12: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 17)],
    13: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 18), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 19)],
    14: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 20), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 21), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 22)],
    15: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 23)],
    16: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 24)],
    17: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 25)],
    18: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 26)],
    19: [('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 27), ('สอวน_physics/tpho-61-physics/tpho_17_theory.pdf', 28)],
    20: [('สอวน_physics/tpho-61-physics/tpho_17_exp.pdf', 1), ('สอวน_physics/tpho-61-physics/tpho_17_exp.pdf', 2)],
    21: [('สอวน_physics/tpho-61-physics/tpho_17_exp.pdf', 3)],
    22: [('สอวน_physics/tpho-61-physics/tpho_17_exp.pdf', 4)],
}
UNITS = {
    1: ('rotating-beam-bounce', 'มวลที่กระดอนซ้ำรอยบนคานหมุน: ต้องกระทบตั้งฉากกับคาน จึงได้ L = 2v² sin θ₀/g การชนยืดหยุ่นกลับทิศทั้งมวลและคาน MLω = 6mv และคานต้องหมุน 2θ₀ ระหว่างการกระทบ ได้ m/M = θ₀ tan θ₀/3', 'ใช้การเคลื่อนที่แบบโพรเจกไทล์หาความยาวคาน', 'ใช้การดลเชิงมุมและเวลาบินหาอัตราเร็วเชิงมุมและอัตราส่วนมวล'),
    2: ('rotating-beam-bounce', '', '', ''),
    3: ('rotating-beam-bounce', '', '', ''),
    4: ('vacuum-flask-radiation', 'ภาชนะผนังสองชั้นสุญญากาศ: รวมการสะท้อนไปมาเป็นอนุกรมเรขาคณิต ได้ความร้อนสุทธิ ε₁ε₂σ(T₁⁴ − T₂⁴)/(ε₁ + ε₂ − ε₁ε₂) ต่อพื้นที่ และเวลาที่น้ำแข็งละลายหมดเท่ากับ mL_f หารด้วยกำลังผ่านผนังด้านข้าง', 'รวมรังสีที่ผนังในดูดกลืนจากการสะท้อนทุกรอบ', 'หักการแผ่รังสีของผนังในแล้วคูณพื้นที่หาเวลาละลาย'),
    5: ('vacuum-flask-radiation', '', '', ''),
    6: ('falling-rod-smooth-floor', 'ท่อนไม้ที่ปลายหนึ่งแตะพื้นลื่นเริ่มล้มจากหยุดนิ่ง: แรงตั้งฉากและสมการหมุนให้จุดกึ่งกลางตกด้วย 3g cos²θ/(1 + 3cos²θ) และปลายบนด้วยสองเท่า เชือกที่แขวนมวลจะหย่อนทั้งหมดเมื่อ θ ≥ 54.7°', 'เขียนสมการแรงและทอร์กพร้อมเงื่อนไขที่ปลายแตะพื้น', 'เทียบความเร่งของแต่ละจุดกับ g หาเงื่อนไขเชือกหย่อน'),
    7: ('falling-rod-smooth-floor', '', '', ''),
    8: ('watt-balance', 'ตาชั่งแม่เหล็กไฟฟ้า: ขดลวดในสนามแนวรัศมีให้แรง IN2πrB_r และอีเอ็มเอฟ 2πrNB_r u ขณะเคลื่อนที่ หารกันได้ m = VI/(ug) โดยไม่ต้องรู้สนามหรือรัศมี', 'หา B_r จากอีเอ็มเอฟและอัตราเร็วของขดลวด', 'ใช้สมดุลแรงหรือ VI = mgu หามวล'),
    9: ('watt-balance', '', '', ''),
    10: ('watt-balance', '', '', ''),
    11: ('quantum-electrical-standards', 'มาตรฐานทางไฟฟ้าเชิงควอนตัม: แรงดันโจเซฟสัน V = Afh/e จากการวิเคราะห์มิติ ความต้านทานฮอลล์ h/(νe²) จึงได้ m ∝ f₁f₂h/(ug) โดย e ตัดกัน และความคลาดเคลื่อนสัมพัทธ์ของมวลเป็นผลรวมของ h, u, g และความถี่', 'ใช้การวิเคราะห์มิติหาเลขชี้กำลัง', 'แทนแรงดันและกระแสด้วยความถี่และค่าคงที่มูลฐานแล้วรวมความคลาดเคลื่อน'),
    12: ('quantum-electrical-standards', '', '', ''),
    13: ('quantum-electrical-standards', '', '', ''),
    14: ('acoustic-radiation-pressure', 'คลื่นเสียง: P_m = ρ₀cv_m, ρ_m = ρ₀v_m/c, c = √(γPₐ/ρ₀) พลังงานจลน์เฉลี่ย ρ₀v_m²/4 โมเมนตัมเฉลี่ย ρ₀v_m²/(2c) พจน์อันดับสองเพิ่มความดันเฉลี่ย P_m²/(4ρ₀c²) จึงเกิดแรงยก P₀²a/(ρ₀c²) เมื่อคลื่นสะท้อน', 'หาความสัมพันธ์ของแอมพลิจูดจากกฎของนิวตันและการอนุรักษ์มวล', 'เฉลี่ยพจน์อันดับสองตามเวลาหาความดันส่วนเกินและแรง'),
    15: ('acoustic-radiation-pressure', '', '', ''),
    16: ('acoustic-radiation-pressure', '', '', ''),
    17: ('acoustic-radiation-pressure', '', '', ''),
    18: ('acoustic-radiation-pressure', '', '', ''),
    19: ('acoustic-radiation-pressure', '', '', ''),
    20: ('rice-angle-of-repose', 'มุมทรงตัวของข้าว: วัดจากกองข้าวโดยตรง tan α = h/r หรือจากทรงกระบอกที่เริ่มกลิ้งบนพื้นเอียง sin θ_c = (x_cm/R) sin α₁ ซึ่งประมาณเป็นเส้นตรงในปริมาณข้าว และความหนาแน่นการอัดหาจากปริมาตรน้ำที่เติมเต็มช่องว่าง', 'วัดความสูงและรัศมีกองหรือมุมวิกฤติที่ปริมาณข้าวต่าง ๆ', 'เขียนกราฟเส้นตรงหรือใช้ปริมาตรน้ำหามุมและความหนาแน่นการอัด'),
    21: ('rice-angle-of-repose', '', '', ''),
    22: ('rice-angle-of-repose', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2561_physics/sheet.json").read_text("utf-8"))
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
