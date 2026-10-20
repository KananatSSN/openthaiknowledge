"""Idempotent source claims for the 15 reviewed TPhO 3 (2547) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 1)],
    2: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 2)],
    3: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 3), ('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 4), ('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 5), ('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 6)],
    4: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 7)],
    5: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 8)],
    6: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 9)],
    7: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 10)],
    8: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 11)],
    9: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 12), ('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 15)],
    10: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 13)],
    11: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 14)],
    12: [('สอวน_physics/tpho-47-physics/tpho_3_theory_with_solution.pdf', 16)],
    13: [('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 1), ('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 2), ('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 3)],
    14: [('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 4)],
    15: [('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 5), ('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 6), ('สอวน_physics/tpho-47-physics/tpho_3_exp.pdf', 7)],
}
UNITS = {
    1: ('string-over-pulley-kinematics', 'มวลแขวนเชือกยาว 2H คล้องรอกสูง H ที่ปลายเชือกเลื่อนด้วย v₀ คงที่ มีความเร็ว v = v₀²t/√(v₀²t² + H²) และความเร่ง v₀²H²/(v₀²t² + H²)^(3/2)', 'เขียนความยาวเชือกส่วนเอียงด้วยทฤษฎีบทพีทาโกรัส', 'หาอนุพันธ์เทียบเวลาครั้งที่หนึ่งและสอง'),
    2: ('string-over-pulley-kinematics', '', '', ''),
    3: ('pulley-tension-start', 'ขณะเริ่มดึง มวลหยุดนิ่งแต่มีความเร่ง v₀²/H จึงมีแรงตึง T = m(g + v₀²/H) และถ้ารอกมีโมเมนต์ความเฉื่อย I_C แรงตึงอีกฝั่งเป็น T + I_C v₀²/(Hr²)', 'หาความเร่งที่ t = 0 จากเรขาคณิตของเชือก', 'ใช้กฎข้อสองกับมวลและสมการทอร์กกับรอก'),
    4: ('pulley-tension-start', '', '', ''),
    5: ('spring-rod-oscillation', 'แท่งหมุนรอบจุดกึ่งกลางที่มีสปริง k สองข้างที่ปลาย สั่นด้วยความถี่ (1/2π)√(6k/m)', 'เขียนทอร์กคืนตัวจากสปริงทั้งสองที่แขน L/2', 'เทียบกับสมการการเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย'),
    6: ('cue-ball-slide-to-roll', 'ทรงกลมตันที่ไถลโดยไม่หมุนถูกความเสียดทานหน่วงและเร่งการหมุนจนกลิ้งได้ที่ t = 2V₀/(7μg) ระยะไถล 12V₀²/(49μg) และ ω = 5V₀/(7R)', 'เขียน V(t) และ ω(t) จากกฎข้อสองและสมการทอร์ก', 'ตั้งเงื่อนไขการกลิ้ง V = ωR'),
    7: ('cue-ball-slide-to-roll', '', '', ''),
    8: ('sliding-loop-parallel-emf', 'วงลวดสี่เหลี่ยมที่แตะรางที่กึ่งกลางด้านมี emf vBL ในสองด้านที่ขนานกัน เทียบเท่าเซลล์ emf vBL ความต้านทานภายใน r กระแสจึงลดลงแบบเอกซ์โพเนนเชียล', 'ยุบวงจรเป็นเซลล์ขนานเทียบเท่า', 'เขียนสมการแรงแม่เหล็กหน่วงแล้วแก้หา v(t) และ I(t)'),
    9: ('moving-reflector-pulses', 'คลื่นดลห่างกัน τ สะท้อนจากวัตถุที่เข้าหาด้วย v < c กลับมาห่างกัน (c − v)τ/(c + v) และห่างกัน (c + v)τ/(c − v) เมื่อวัตถุหนี', 'หาเวลาที่ลูกคลื่นถัดไปพบวัตถุ', 'หาระยะห่างของคลื่นสะท้อนแล้วหารด้วย c'),
    10: ('moving-reflector-pulses', '', '', ''),
    11: ('moving-reflector-pulses', '', '', ''),
    12: ('moving-reflector-pulses', '', '', ''),
    13: ('physical-pendulum-inertia', 'ลูกตุ้มฟิสิกัลมีคาบ T = 2π√(I/(mgd)) จึงหาโมเมนต์ความเฉื่อยรอบจุดหมุนได้ แล้วใช้ทฤษฎีบทแกนขนานหาโมเมนต์ความเฉื่อยรอบจุดศูนย์กลางมวล', 'หาจุดศูนย์กลางมวลแล้ววัดคาบรอบจุดหมุน', 'คำนวณ I_O แล้วลบ md²'),
    14: ('rl-coil-voltage-ratio', 'ขดลวด L ที่มีความต้านทาน r อนุกรมกับ R มี V_R/V_L = R/√((ωL)² + r²) ดังนั้น (V_L/V_R)² แปรผันตรงกับ 1/R² ด้วยความชัน (ωL)² + r²', 'เขียนอัตราส่วนความต่างศักย์จากกระแสเดียวกัน', 'จัดเป็นเส้นตรงแล้วหา L จากความชัน'),
    15: ('rl-coil-voltage-ratio', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2547_physics/sheet.json").read_text("utf-8"))
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
