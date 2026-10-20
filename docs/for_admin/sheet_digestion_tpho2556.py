"""Idempotent source claims for the 21 reviewed TPhO 12 (2556) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 1)],
    2: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 2)],
    3: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 3)],
    4: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 4)],
    5: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 5)],
    6: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 6)],
    7: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 7)],
    8: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 8)],
    9: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 9)],
    10: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 10)],
    11: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 11), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 12)],
    12: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 13)],
    13: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 14)],
    14: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 15)],
    15: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 17), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 18), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 19)],
    16: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 16), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 20), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 21), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 22), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 23)],
    17: [('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 24), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 25), ('สอวน_physics/tpho-56-physics/tpho_12_theory.pdf', 26)],
    18: [('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 1), ('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 2)],
    19: [('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 3)],
    20: [('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 4), ('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 5)],
    21: [('สอวน_physics/tpho-56-physics/tpho_12_exp.pdf', 6)],
}
UNITS = {
    1: ('jerked-hinged-rods', 'ท่อนไม้สามท่อนต่อด้วยจุดหมุนลื่นถูกดีดที่ท่อนกลาง: โมเมนตัมเชิงมุมของท่อนข้างรอบจุดหมุนไม่เปลี่ยนจากการดลที่จุดหมุน จึงได้ ω = 3u cos θ/(2l) ความเร็วศูนย์กลางมวล v_y = u(1 − ¾cos²θ) และการดล (3/2)mu(1 + sin²θ)', 'เขียนโมเมนตัมเชิงมุมของท่อนข้างรอบจุดหมุนให้เป็นศูนย์', 'รวมโมเมนตัมทั้งระบบหาการดลของแรงดีด'),
    2: ('jerked-hinged-rods', '', '', ''),
    3: ('jerked-hinged-rods', '', '', ''),
    4: ('meteor-atmospheric-drag', 'อากาศที่หยุดนิ่งหน้าอุกกาบาตเพิ่มความดัน ½ρv² ให้แรงต้าน C_d½ρv²πr² ในบรรยากาศ ρ₀e^(−αz) อัตราเร็วเป็น v = u·exp(−Ae^(−αz)) กับ A = C_dρ₀πr²/(2mα sin θ) กำลังที่สูญเสียมากที่สุดที่ e^(−αz) = 1/(3A) และความดันหยุดนิ่งที่นั่นต้องไม่เกินความแข็งแรงของวัสดุ', 'หาแรงต้านจากความดันหยุดนิ่งและเขียนสมการการเคลื่อนที่ตามความสูง', 'อินทิเกรตหาอัตราเร็วแล้วหาความสูงที่ ρv³ มากที่สุด'),
    5: ('meteor-atmospheric-drag', '', '', ''),
    6: ('meteor-atmospheric-drag', '', '', ''),
    7: ('meteor-atmospheric-drag', '', '', ''),
    8: ('meteor-atmospheric-drag', '', '', ''),
    9: ('gas-transfer-spring-cylinder', 'ก๊าซไหลช้า ๆ จากกระบอกสูบความดันคงที่ mg/a ไปยังกระบอกสูบที่มีสปริงจนความดันเท่ากัน: V_B = mga/k งานจากน้ำหนัก P V_B T_A/T_B งานต่อสปริง ½P V_B และสมดุลพลังงานให้ T_B/T_A = 2γ/(γ + 1)', 'หาความดันและปริมาตรสุดท้ายจากสมดุลแรงของลูกสูบ', 'เขียนงานเข้าและออกแล้วใช้ U = PV/(γ − 1) หาอุณหภูมิ'),
    10: ('gas-transfer-spring-cylinder', '', '', ''),
    11: ('gas-transfer-spring-cylinder', '', '', ''),
    12: ('gas-transfer-spring-cylinder', '', '', ''),
    13: ('gas-transfer-spring-cylinder', '', '', ''),
    14: ('gas-transfer-spring-cylinder', '', '', ''),
    15: ('rainbow-deviation-angles', 'แสงที่สะท้อนภายในหยดน้ำ N ครั้งเบี่ยง α = 2π − (N + 1)(π − 2φ) − 2θ แสงเข้มที่สุดที่ dα/dθ = 0 คือ cos²θ = (n² − 1)/((N + 1)² − 1) ได้รุ้งปฐมภูมิ 42.5° และรุ้งทุติยภูมิ 50.1° สำหรับ n = 1.33 ระหว่างนั้นเป็นแถบมืดของ Alexander', 'เขียนมุมเบี่ยงเบนจากการหักเหและการสะท้อนแต่ละครั้ง', 'หาจุดที่มุมเบี่ยงเบนคงที่ต่อการเปลี่ยนมุมตกกระทบ'),
    16: ('rainbow-deviation-angles', '', '', ''),
    17: ('rainbow-deviation-angles', '', '', ''),
    18: ('magnet-coupled-oscillation', 'แท่งแม่เหล็กแขวนด้วยเชือกแกว่งแบบบิดด้วย f = (1/2π)√(μB_h/I) จึงหา magnetic moment ได้ เมื่อคาบลูกตุ้มเท่าคาบการบิด พลังงานถ่ายโอนช้าที่สุด τ_max ≅ (B_h/B_v)(1/f)(2ℓ/√(R² + d²/3)) จึงหา B_v และมุมเอียง tan γ = B_v/B_h', 'วัดความถี่การบิดและคาบลูกตุ้มที่ความยาวต่าง ๆ', 'หาความยาวที่คาบเท่ากันและ τ_max แล้วคำนวณ B_v และมุมเอียง'),
    19: ('magnet-coupled-oscillation', '', '', ''),
    20: ('magnet-coupled-oscillation', '', '', ''),
    21: ('magnet-coupled-oscillation', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2556_physics/sheet.json").read_text("utf-8"))
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
