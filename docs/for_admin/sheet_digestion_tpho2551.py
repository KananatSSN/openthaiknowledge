"""Idempotent source claims for the 15 reviewed TPhO 7 (2551) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 1), ('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 2)],
    2: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 3), ('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 4)],
    3: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 5)],
    4: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 6), ('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 7)],
    5: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 8)],
    6: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 9)],
    7: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 10)],
    8: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 12)],
    9: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 11)],
    10: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 13)],
    11: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 14)],
    12: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 15), ('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 16), ('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 17)],
    13: [('สอวน_physics/tpho-51-physics/tpho_7_theory.pdf', 18)],
    14: [('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 1), ('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 2), ('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 3)],
    15: [('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 4), ('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 5), ('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 6), ('สอวน_physics/tpho-51-physics/tpho_7_exp.pdf', 7)],
}
UNITS = {
    1: ('liquid-mirror-lens', 'กระจกเว้าบางที่ประกบกับแผ่นแก้วบาง ภาพสลิตกลับมาที่เดิมเมื่อสลิตอยู่ที่จุดศูนย์กลางความโค้ง R = L ถ้าเติมของเหลวดัชนี n ระหว่างแผ่น ระยะใหม่เป็น R/(2n − 1)', 'คิดการหักเห การสะท้อน และการหักเหกลับเป็นกระจกสมมูล', 'ตั้งระยะวัตถุเท่ากับระยะภาพแล้วแก้หาระยะใหม่'),
    2: ('raindrop-deviation', 'แสงที่หักเหเข้าหยดน้ำ สะท้อนภายในหนึ่งครั้งแล้วหักเหออก มีมุมเบี่ยงเบน π − 4α + 2φ เมื่อ sin φ = n sin α และน้อยที่สุดเมื่อ cos φ = √((n² − 1)/3)', 'ใช้กฎของสเนลล์และรูปสามเหลี่ยมในหยดน้ำ', 'หาอนุพันธ์ของมุมเบี่ยงเบนแล้วตั้งเป็นศูนย์'),
    3: ('raindrop-deviation', '', '', ''),
    4: ('charge-through-charged-ball', 'ประจุ −q ที่ผ่านรูของทรงกลมประจุ +Q สม่ำเสมอ: นอกทรงกลมคิดเหมือนจุดประจุ ภายในแรงเป็น kqQx/R³ เข้าหาศูนย์กลาง จึงสั่นแบบฮาร์มอนิกด้วย ω = √(kqQ/(mR³)) งานจากศูนย์กลางถึงผิวคือ −kqQ/(2R)', 'ใช้การอนุรักษ์พลังงานกับศักย์นอกและในทรงกลม', 'ใช้การเคลื่อนที่แบบฮาร์มอนิกภายในหาเวลา'),
    5: ('charge-through-charged-ball', '', '', ''),
    6: ('charge-through-charged-ball', '', '', ''),
    7: ('charge-through-charged-ball', '', '', ''),
    8: ('wedge-block-pulley', 'กล่องบนลิ่มลื่นที่ดึงเชือกพันรอกมวล m_C: เมื่อจับลิ่มไว้ a = m_B g sin θ/(m_B + m_C/2) เมื่อเชือกขาดและลิ่มเลื่อนได้ a_A = mg sin θ cos θ/(M + m sin²θ) และเมื่อเชือกไม่ขาดต้องแก้สมการกล่อง ลิ่มพร้อมรอก และรอกพร้อมกัน', 'เลือกระบบและเขียนสมการตามแนวผิวเอียง ตั้งฉาก และแนวระดับ', 'แก้ระบบสมการเชิงเส้นหาความเร่ง แรงตึง และแรงปฏิกิริยา'),
    9: ('wedge-block-pulley', '', '', ''),
    10: ('wedge-block-pulley', '', '', ''),
    11: ('wedge-block-pulley', '', '', ''),
    12: ('wedge-block-pulley', '', '', ''),
    13: ('wedge-block-pulley', '', '', ''),
    14: ('hose-boyle-pressure', 'ลำอากาศในสายยางที่สูง h เหนือระดับน้ำมีความดัน P_atm − ρgh ตามกฎของบอยล์ 1/L เป็นเส้นตรงกับ h และ P_atm = ρg × จุดตัด/|ความชัน|', 'วัดความยาวลำอากาศที่ความสูงต่าง ๆ', 'เขียนกราฟ 1/L กับ h แล้วอ่านความชันและจุดตัด'),
    15: ('potentiometer-emf', 'โพเทนชิออมิเตอร์เปรียบเทียบแรงเคลื่อนไฟฟ้าที่ไม่ทราบค่ากับเซลล์มาตรฐานด้วยกระแสเดียวกัน E_x = (R_x/R_s)E_s', 'ปรับให้แกลแวนอมิเตอร์ไม่มีกระแสด้วยเซลล์มาตรฐาน', 'เปลี่ยนเป็นเซลล์ที่ไม่ทราบค่าแล้วอ่านความต้านทานที่สมดุล'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2551_physics/sheet.json").read_text("utf-8"))
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
