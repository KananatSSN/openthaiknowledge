"""Idempotent source claims for the 17 reviewed TPhO 1 (2545) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 1),
    2: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 2),
    3: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 3),
    4: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 4),
    5: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 5),
    6: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 6),
    7: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 7),
    8: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 8),
    9: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 9),
    10: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 10),
    11: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 11),
    12: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 12),
    13: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 13),
    14: ('สอวน_physics/tpho-45-physics/tpho_1_theory_eng.pdf', 14),
    15: ('สอวน_physics/tpho-45-physics/tpho_1_expt.pdf', 1),
    16: ('สอวน_physics/tpho-45-physics/tpho_1_expt.pdf', 2),
    17: ('สอวน_physics/tpho-45-physics/tpho_1_expt.pdf', 3),
}
UNITS = {
    1: ('released-spring-centre', 'ระบบที่ปล่อยจากหยุดนิ่งบนพื้นลื่นมีศูนย์กลางมวลอยู่กับที่ ระยะของแต่ละมวลจากศูนย์กลางมวลแบ่งตามส่วนกลับของมวล', 'หาตำแหน่งศูนย์กลางมวลเริ่มต้น', 'แบ่งความยาวสปริงใหม่ตามสัดส่วนมวล'),
    2: ('sliding-rod-emf', 'แท่งตัวนำเลื่อนบนรางห่าง L ด้วยความเร็ว v ในสนาม B ให้ emf = vLB ไม่ขึ้นกับมุมเอียงของแท่ง', 'หาอัตราการเปลี่ยนพื้นที่ของวงจร', 'คูณด้วยสนามแม่เหล็ก'),
    3: ('magnetic-drag-decay', 'แท่งเลื่อนบนรางที่มีตัวต้านทานถูกหน่วงด้วยแรง L²B²v/R ความเร็วลดแบบเอกซ์โพเนนเชียล v₀e^(−L²B²t/(MR))', 'เขียนสมการ M dv/dt = −L²B²v/R', 'แก้สมการเชิงอนุพันธ์แยกตัวแปร'),
    4: ('equal-image-focal', 'ภาพเสมือนจากวัตถุที่ระยะ a เท่ากับภาพจริงจากวัตถุที่ระยะ b เมื่อ f = (a+b)/2', 'เขียนกำลังขยาย f/(f−a) และ f/(b−f)', 'ตั้งเท่ากันแล้วแก้หา f'),
    5: ('rolling-ball-bowl', 'ทรงกลมกลิ้งไม่ไถลในชามรัศมี R มีพลังงานจลน์ (7/10)M(R−r)²θ̇² อัตราเร็วเชิงมุมสูงสุดที่ก้นชาม', 'เขียนพลังงานจลน์การเลื่อนและการหมุนด้วยเงื่อนไขการกลิ้ง', 'ใช้การอนุรักษ์พลังงานจากมุมเริ่มต้นถึงก้นชาม'),
    6: ('ionosphere-limiting-wavelength', 'คลื่นวิทยุสะท้อนกลับหมดที่ไอโอโนสเฟียร์เมื่อ sinθ₁ = R sinα/(R+h) ไม่น้อยกว่าดรรชนี √(1−λ²/A)', 'ใช้กฎไซน์หามุมตกกระทบที่ขอบไอโอโนสเฟียร์', 'ตั้งเงื่อนไขการสะท้อนกลับหมดแล้วแก้หา λ'),
    7: ('hoop-on-rod-oscillation', 'ห่วงรัศมี R กลิ้งไม่ไถลรอบแกนรัศมี r แกว่งเหมือนลูกตุ้มที่มีพลังงานจลน์ M(R−r)²θ̇² และความถี่ (1/2π)√(g/(2(R−r)))', 'หาตำแหน่งศูนย์กลางห่วงและอัตราหมุนจากเงื่อนไขการกลิ้ง', 'เขียนพลังงานแล้วหาความถี่การสั่นมุมเล็ก'),
    8: ('hoop-on-rod-oscillation', '', '', ''),
    9: ('hoop-on-rod-oscillation', '', '', ''),
    10: ('hoop-on-rod-oscillation', '', '', ''),
    11: ('hoop-on-rod-oscillation', '', '', ''),
    12: ('liquid-magnetic-pump', 'กระแส I ผ่านของเหลวในสนาม B ทำให้เกิดแรง IaB ดันของเหลว ระดับต่างกัน h = IB/(Dgb) และความร้อน I²a/(σbL)', 'หาทิศแรงจากกฎมือขวา', 'สมดุลแรงกับผลต่างความดันของคอลัมน์ของเหลว'),
    13: ('liquid-magnetic-pump', '', '', ''),
    14: ('liquid-magnetic-pump', '', '', ''),
    15: ('newton-cooling-law', 'กฎการเย็นตัวของนิวตันให้ T = Tₐ + (T₀−Tₐ)e^(−t/β) และ ln(T−Tₐ) ลดเป็นเส้นตรงตามเวลาด้วยความชัน −1/β', 'แก้สมการเชิงอนุพันธ์แยกตัวแปร', 'ใช้ล็อกเพื่อหาค่าคงตัว β จากข้อมูล'),
    16: ('newton-cooling-law', '', '', ''),
    17: ('airy-ring-wavelength', 'วงแหวนมืดวงในสุดของการเลี้ยวเบนรอบวัตถุทึบกลมเส้นผ่านศูนย์กลาง D อยู่ที่ D sinθ = 1.22λ', 'หามุมจากระยะเลื่อนและระยะห่างรู', 'แทนในเงื่อนไขวงแหวนมืดหา λ'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2545_physics/sheet.json").read_text("utf-8"))
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
        sheet_path, digest_item = SOURCES[item["number"]]
        source = {"sheet": sheet_path, "item": digest_item}
        if source not in unit["sources"]:
            unit["sources"].append(source)
        if item["generator"] not in unit["covered_by"]:
            unit["covered_by"].append(item["generator"])
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", "utf-8")


if __name__ == "__main__":
    main()
