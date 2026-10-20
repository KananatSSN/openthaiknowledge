"""Idempotent source claims for the 16 reviewed TPhO 8 (2552) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 1)],
    2: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 2)],
    3: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 3)],
    4: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 4)],
    5: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 5)],
    6: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 6)],
    7: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 7)],
    8: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 7)],
    9: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 8)],
    10: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 9)],
    11: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 10)],
    12: [('สอวน_physics/tpho-52-physics/tpho_8_theory.pdf', 11)],
    13: [('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 3)],
    14: [('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 1), ('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 4)],
    15: [('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 2)],
    16: [('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 5), ('สอวน_physics/tpho-52-physics/tpho_8_exp.pdf', 6)],
}
UNITS = {
    1: ('gas-leak-thrust', 'ถังแก๊สที่เกิดรูรั่วในสุญญากาศได้แรงลัพธ์ PA จากผนังฝั่งตรงข้ามรู โดย P = nRT/V ความเร่งจึงเป็น PA/M', 'หาความดันจากกฎแก๊สอุดมคติ', 'หาแรงลัพธ์จากพื้นที่รูแล้วหารด้วยมวล'),
    2: ('moving-object-image', 'วัตถุที่เคลื่อนที่ตั้งฉากกับแกนเลนส์ ภาพเคลื่อนที่ด้วยความเร็วคูณกำลังขยายตามขวาง −v/u ในทิศกลับกันเมื่อเป็นภาพจริง', 'หาระยะภาพจากสมการเลนส์', 'คูณความเร็วด้วยกำลังขยาย'),
    3: ('electron-triangle-field', 'อิเล็กตรอนที่เข้าสนามแม่เหล็กตั้งฉากเคลื่อนที่เป็นวงกลม r = mv/(eB) การออกจากด้านเอียงของสามเหลี่ยมด้านเท่าในทิศขนานแกน x ต้องเป็นเสี้ยววงกลมรัศมี √3a/(2(1 + √3))', 'หารัศมีจากเรขาคณิตของจุดออก', 'ใช้ evB = mv²/r หาอัตราเร็ว'),
    4: ('charged-ball-two-regions', 'ลูกบอลมีประจุในสนามไฟฟ้าแนวระดับและแรงโน้มถ่วงแนวดิ่ง เคลื่อนที่อิสระสองแนว v_x = v₀ + (qE/m)t, v_y = −gt', 'หาเวลาตกจากความสูงในแนวดิ่ง', 'รวมองค์ประกอบความเร็วทั้งสองแนว'),
    5: ('stacked-ball-bounce', 'ลูกบอลเบาบนลูกบอลหนักที่ตกพร้อมกัน ลูกหนักเด้งจากพื้นแล้วชนลูกเบาแบบยืดหยุ่น ลูกเบาออกด้วย ((3 − m/M)/(1 + m/M))v₀ และชนครั้งต่อไปตามสมการการเคลื่อนที่ของทั้งสองลูก', 'ใช้การชนยืดหยุ่นหนึ่งมิติหาความเร็วหลังชน', 'เขียนตำแหน่งของทั้งสองลูกตามเวลาแล้วหาจุดที่ตรงกัน'),
    6: ('stacked-ball-bounce', '', '', ''),
    7: ('stacked-ball-bounce', '', '', ''),
    8: ('stacked-ball-bounce', '', '', ''),
    9: ('hanging-capacitor-plate', 'แผ่นประจุ ±σ ดึงกันด้วยแรง σ²A/(2ε₀) แผ่นบนที่แขวนสปริงสมดุลเมื่อ kd = ½ε₀A(V₀/(D − d))² และสั่นด้วย ω² = (k/m)(D − 3d)/(D − d) จึงสั่นไม่ได้เมื่อ d ≥ D/3', 'หาแรงระหว่างแผ่นจากสนามของแผ่นเดียว', 'กระจายแรงรอบสมดุลหาค่าคงตัวสปริงยังผล'),
    10: ('hanging-capacitor-plate', '', '', ''),
    11: ('hanging-capacitor-plate', '', '', ''),
    12: ('hanging-capacitor-plate', '', '', ''),
    13: ('hall-sensor-calibration', 'ขดลวดสี่เหลี่ยมให้สนามบนแกน μ₀a²iN/(2π(x² + a²/4)√(x² + a²/2)) ใช้เทียบความไวของเซนเซอร์ฮอลล์ ΔV/B แล้ววัดสนามแม่เหล็กอื่น เช่นสนามที่ผิวแม่เหล็กจานกลม', 'คำนวณสนามของขดลวดที่ตำแหน่งเซนเซอร์', 'หาความไวจากการเปลี่ยนของ V_out แล้วใช้วัดสนามอื่น'),
    14: ('hall-sensor-calibration', '', '', ''),
    15: ('hall-sensor-calibration', '', '', ''),
    16: ('rod-physical-pendulum-g', 'ท่อนทรงกระบอกยาว 2L แกว่งรอบจุดห่างปลาย x มีคาบ (2π/√g)√((L²/3 + R²/4)/(L − x) + (L − x)) จึงหา g จากคาบที่วัดได้', 'หาโมเมนต์ความเฉื่อยรอบจุดหมุนด้วยทฤษฎีบทแกนขนาน', 'แทนในสูตรคาบลูกตุ้มกายภาพแล้วแก้หา g'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2552_physics/sheet.json").read_text("utf-8"))
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
