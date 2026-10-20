"""Idempotent source claims for the 18 reviewed TPhO 11 (2555) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 1)],
    2: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 2)],
    3: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 3)],
    4: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 4), ('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 5)],
    5: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 6)],
    6: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 7)],
    7: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 8)],
    8: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 9)],
    9: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 10)],
    10: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 11)],
    11: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 12)],
    12: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 13), ('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 14)],
    13: [('สอวน_physics/tpho-55-physics/tpho_11_theory.pdf', 15)],
    14: [('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 1)],
    15: [('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 2)],
    16: [('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 3)],
    17: [('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 4), ('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 5)],
    18: [('สอวน_physics/tpho-55-physics/tpho_11_exp.pdf', 6)],
}
UNITS = {
    1: ('pinhole-camera-diffraction', 'กล้องรูเข็มรูเส้นผ่านศูนย์กลาง a ห่างฉาก L ให้ภาพวัตถุขนาดเชิงมุม θ ขนาด a + Lθ การเลี้ยวเบนที่รูกลม (มุม 1.22λ/a) เพิ่มขนาดอีก 2.44λL/a ภาพจึงเล็กที่สุดเมื่อ a = √(2.44λL)', 'ลากรังสีจากขอบวัตถุผ่านขอบรูหาขนาดภาพเชิงเรขาคณิต', 'เพิ่มการแผ่ออกจากการเลี้ยวเบนแล้วหาขนาดรูที่ทำให้ผลรวมน้อยที่สุด'),
    2: ('pinhole-camera-diffraction', '', '', ''),
    3: ('pinhole-camera-diffraction', '', '', ''),
    4: ('trapped-air-w-tube', 'ในหลอดรูปตัว W อากาศที่ถูกขังมีความดันเดียวกันตลอด จึงต้องรับผลต่างระดับน้ำทั้งสองด้านเท่ากัน ขณะน้ำเริ่มล้นจากปลายสั้นสูง h ระดับด้านสูงต้องเป็น 2h', 'วาดตำแหน่งของน้ำและช่องอากาศขณะเริ่มล้น', 'เขียนความดันของช่องอากาศจากทั้งสองด้านแล้วจับเท่ากัน'),
    5: ('dust-loaded-oscillator', 'ฝุ่นลอยนิ่ง Δm เกาะมวลติดสปริงที่อัตราเร็ว v ทำให้เสียพลังงานประมาณ ½Δmv² เฉลี่ยต่อรอบ ΔE = −ΔmE₀/(2m) ขณะที่ Δω/ω₀ = −Δm/(2m) จึงได้ ΔE/E₀ = Δω/ω₀ และพลังงานแปรผันตรงกับความถี่เชิงมุม E = E₀ω/ω₀', 'ใช้การอนุรักษ์โมเมนตัมหาพลังงานที่เสียเมื่อฝุ่นเกาะ', 'เฉลี่ยต่อรอบด้วย ⟨v²⟩ = u₀²/2 แล้วเทียบกับการเปลี่ยนความถี่'),
    6: ('dust-loaded-oscillator', '', '', ''),
    7: ('dust-loaded-oscillator', '', '', ''),
    8: ('dust-loaded-oscillator', '', '', ''),
    9: ('dust-loaded-oscillator', '', '', ''),
    10: ('charged-plate-hole-lens', 'แผ่นตัวนำที่มีประจุ σ ทั้งสองผิวให้สนาม σ/ε₀ ในรูของแผ่นหนา d สนามแนวรัศมี E_r = −rE/d จากกฎของเกาส์ ลำโปรตอนความเร็ว u ที่ผ่านรูได้ความเร็วแนวรัศมี erE/(mu) และถูกโฟกัสที่ระยะ 3mu²/(2eE)', 'ใช้กฎของเกาส์กับทรงกระบอกในรูหาสนามแนวรัศมี', 'ใช้การดลหาความเร็วแนวรัศมีแล้วรวมความเร่งตามแกนหาระยะโฟกัส'),
    11: ('charged-plate-hole-lens', '', '', ''),
    12: ('charged-plate-hole-lens', '', '', ''),
    13: ('charged-plate-hole-lens', '', '', ''),
    14: ('capacitor-reference-weighing', 'ตัวเก็บประจุแผ่นคู่ขนานบนท่อพลาสติกที่เป็นสปริงให้ความถี่แปรผันตรงกับระยะห่าง น้ำหนักบนแผ่นลดความถี่เชิงเส้น จึงหามวลโดยเทียบกับมวลอ้างอิง และหาค่าคงตัวสปริงจากความถี่ต่อระยะห่างที่วัดด้วยแผ่นรองที่รู้ความหนา', 'เขียนกราฟความถี่กับจำนวนชิ้นหรือความหนาแล้วหาความชัน', 'เทียบความถี่ที่ลดลงกับมวลอ้างอิงหรือแปลงเป็นระยะยุบเพื่อหาค่าคงตัว'),
    15: ('capacitor-reference-weighing', '', '', ''),
    16: ('spring-effective-mass', 'สปริงมวล m มีมวลยังผล β₁m ในการสั่น ω = √(k/(M + β₁m)) จึงหา β₁ จากจุดตัดแกนต่อความชันของกราฟ T² กับ M ถ้าความหนาแน่นเชิงเส้นเปลี่ยนจาก λ₀ ด้านบนถึง λₙ ด้านล่าง β₂ = (λ₀/6 + λₙ/2)/(λ₀ + λₙ) ซึ่งเป็น 1/3 เมื่อสปริงสม่ำเสมอ', 'หาค่าคงตัวสปริงจากกราฟกฎของฮุก', 'เขียนกราฟ T² กับ M หรือคำนวณ β₂ จากระยะยืดของขดบนและล่าง'),
    17: ('spring-effective-mass', '', '', ''),
    18: ('spring-effective-mass', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2555_physics/sheet.json").read_text("utf-8"))
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
