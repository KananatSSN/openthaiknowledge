"""Idempotent source claims for the 20 reviewed TPhO 16 (2560) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 1)],
    2: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 3)],
    3: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 2), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 4)],
    4: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 5)],
    5: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 6)],
    6: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 7)],
    7: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 8), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 9)],
    8: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 10), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 11)],
    9: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 12), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 13)],
    10: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 14)],
    11: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 15), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 16)],
    12: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 17)],
    13: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 18), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 19)],
    14: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 20)],
    15: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 21)],
    16: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 22), ('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 23)],
    17: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 24)],
    18: [('สอวน_physics/tpho-60-physics/TPhO2017_Theory.pdf', 25)],
    19: [('สอวน_physics/tpho-60-physics/TPhO2017_Expt___Question.pdf', 1)],
    20: [('สอวน_physics/tpho-60-physics/TPhO2017_Expt___Question.pdf', 2)],
}
UNITS = {
    1: ('planet-rock-impact', 'ดาวเคราะห์มวลมากพุ่งเข้าชนก้อนหินที่นิ่ง: ในกรอบของดาวเคราะห์ก้อนหินตกด้วยอัตราเร็ว √(u² + 2gR) จึงในกรอบเดิมมีอัตราเร็ว √(u² + 2gR) − u ใช้พลังงานคงที่ของดาวเคราะห์ได้เฉพาะในกรอบของดาวเคราะห์', 'แปลงไปกรอบของดาวเคราะห์แล้วใช้การอนุรักษ์พลังงาน', 'แปลงความเร็วกลับมากรอบเดิม'),
    2: ('triangle-cycle-engine', 'วัฏจักรสามเหลี่ยม A → B (ความดันคงที่) → C → A (ปริมาตรคงที่) ของแก๊สอะตอมเดี่ยว: งานเท่าพื้นที่สามเหลี่ยม ความร้อนเข้าในช่วง AB (5/2 pΔV) และ CA (3/2 VΔp) ประสิทธิภาพเข้าใกล้ (1 − T_C/T_A)/5 เมื่อ B ไกลออกไป', 'หาความดันที่ C จากกระบวนการปริมาตรคงที่', 'คำนวณงานและความร้อนเข้าแต่ละช่วงแล้วหาประสิทธิภาพ'),
    3: ('triangle-cycle-engine', '', '', ''),
    4: ('triangle-cycle-engine', '', '', ''),
    5: ('eye-resolution-limits', 'ตามนุษย์แยกจุดได้จำกัดด้วยการเลี้ยวเบน 1.22λ/D ที่รูม่านตาหรือด้วยระยะห่างของเซลรับแสงหารด้วยความลึกของลูกตา ระยะห่างพิกเซลที่ตาแยกไม่ออกที่ระยะ x คือ xθ ของขีดจำกัดที่ใหญ่กว่า', 'คำนวณมุมจากการเลี้ยวเบนและจากเซลรับแสง', 'คูณมุมที่เป็นตัวจำกัดด้วยระยะมองหาขนาดพิกเซล'),
    6: ('eye-resolution-limits', '', '', ''),
    7: ('eye-resolution-limits', '', '', ''),
    8: ('mach-zehnder-sugar', 'อุปกรณ์แทรกสอดมัคเซนเดอร์: สารละลายน้ำตาล n = 1.33 + αh ในท่อยาว L ทำให้เฟสต่างกัน 2πLαh/λ₀ ความเข้มที่พอร์ตสว่าง 2I₀cos²(πLαh/λ₀) จึงวัดความเข้มข้นได้จากความต่างศักย์ และใช้สองพอร์ตเพื่อแก้ผลของแสงผันผวน', 'หาผลต่างทางเดินแสงจากดัชนีหักเหที่ต่างกัน', 'แปลงความเข้มหรือความต่างศักย์ที่วัดได้เป็นเฟสและความเข้มข้น'),
    9: ('mach-zehnder-sugar', '', '', ''),
    10: ('mach-zehnder-sugar', '', '', ''),
    11: ('mach-zehnder-sugar', '', '', ''),
    12: ('accelerator-dipole-beam', 'เครื่องเร่งอนุภาคจำลอง: ไดโพลจากลวดสองเส้นให้สนาม μ₀I/(πR) ที่แกน ซึ่งต้องเลี้ยวโปรตอนรัศมี ND/(2π) ลำอนุภาคกระจายออกด้วยความเร่ง nq²(1 − v²/c²)/(2πε₀mℓr₀) จากแรงไฟฟ้าที่ชนะแรงแม่เหล็ก', 'หาอัตราเร็วจากพลังงานจลน์และรัศมีความโค้งที่ต้องการ', 'ใช้กฎของแอมแปร์และเกาส์หาสนามและแรงในลำอนุภาค'),
    13: ('accelerator-dipole-beam', '', '', ''),
    14: ('accelerator-dipole-beam', '', '', ''),
    15: ('accelerator-dipole-beam', '', '', ''),
    16: ('quadrupole-focusing', 'Magnetic Quadrupole จากลวดสี่เส้นให้สนาม B = ayî + bxĵ โดย a = b = 2μ₀I/(πR²) เป็นเลนส์นูนในระนาบหนึ่งและเลนส์เว้าในอีกระนาบ ความยาวโฟกัส mv/(bqd) และคู่ Quadrupole ที่กลับทิศกระแสโฟกัสได้ทั้งสองระนาบ', 'รวมสนามจากลวดทั้งสี่ใกล้แกนกลาง', 'ใช้การดลหาความยาวโฟกัส แล้วรวมเลนส์บางสองตัว'),
    17: ('quadrupole-focusing', '', '', ''),
    18: ('quadrupole-focusing', '', '', ''),
    19: ('neodymium-magnet-lab', 'แรงระหว่างแม่เหล็กกระดุมแปรตาม rⁿ จึงหา n จากความชันของกราฟ log M กับ log r แม่เหล็กตกในท่ออะลูมิเนียมด้วยอัตราเร็วสุดท้ายเมื่อ mg = ks/t จึงหา k จากความชันของกราฟเวลากับ 1/มวล', 'วัดมวลที่ทำให้แม่เหล็กหลุดหรือเวลาตกที่มวลต่าง ๆ', 'เขียนกราฟเส้นตรงที่เหมาะสมแล้วแปลงความชันเป็น n หรือ k'),
    20: ('neodymium-magnet-lab', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2560_physics/sheet.json").read_text("utf-8"))
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
