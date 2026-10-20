"""Idempotent source claims for the 22 reviewed TPhO 21 (2565) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 1)],
    2: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 2)],
    3: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 3), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 4)],
    4: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 5), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 6), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 7)],
    5: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 7)],
    6: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 8), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 9), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 11), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 14)],
    7: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 10), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 12), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 14)],
    8: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 13)],
    9: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 16)],
    10: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 15), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 17)],
    11: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 18)],
    12: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 19), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 20)],
    13: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 21), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 22)],
    14: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 23)],
    15: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 24)],
    16: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 25), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 26)],
    17: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Question_Solution.pdf', 25)],
    18: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 1), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 2)],
    19: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 3)],
    20: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 4), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 5)],
    21: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 6), ('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 7)],
    22: [('สอวน_physics/tpho-65-physics/TPhO2022_Theory_Experiment_Solution.pdf', 7)],
}
UNITS = {
    1: ('dipole-point-charge', 'ไดโพลไฟฟ้ากับประจุจุด: สนามระยะไกล E = (2p cos θ r̂ + p sin θ θ̂)/(4πε₀r³) ประจุโคจรเป็นวงกลมรอบแกนได้เมื่อ 3cos²θ = 1 (θ = 125.3°) ด้วย L_z² = (1/4πε₀)(4/3√3)pq₀m₀ และประจุที่ปล่อยจากแนวตั้งฉากเคลื่อนที่บนส่วนโค้งวงกลม เร็วที่สุดที่ θ = π', 'แยกองค์ประกอบของไดโพลหรือรวมศักย์ของสองประจุ', 'ใช้เงื่อนไขแรง พลังงาน และโมเมนตัมเชิงมุมหาวงโคจร อัตราเร็ว และคาบ'),
    2: ('dipole-point-charge', '', '', ''),
    3: ('dipole-point-charge', '', '', ''),
    4: ('dipole-point-charge', '', '', ''),
    5: ('dipole-point-charge', '', '', ''),
    6: ('paramagnetic-demagnetisation', 'การทำความเย็นด้วยสนามแม่เหล็ก: ไดโพลสองระดับกระจายตามโบลต์ซมันน์ M/(Nμ) = tanh(μB/k_BT) เอนโทรปีขึ้นกับ μB/k_BT เท่านั้น จึงลดสนามแบบแอเดียแบติกได้ T_f = (B_L/B_H)T_i โดย B_L มาจากไดโพลเพื่อนบ้าน และความร้อนที่ถ่ายออก T_iΔS', 'เขียนการแจกแจงโบลต์ซมันน์และเอนโทรปีของสองระดับ', 'ใช้เอนโทรปีคงที่และ Q = TΔS หาอุณหภูมิสุดท้ายและความร้อน'),
    7: ('paramagnetic-demagnetisation', '', '', ''),
    8: ('paramagnetic-demagnetisation', '', '', ''),
    9: ('paramagnetic-demagnetisation', '', '', ''),
    10: ('paramagnetic-demagnetisation', '', '', ''),
    11: ('paramagnetic-demagnetisation', '', '', ''),
    12: ('compressible-nozzle-flow', 'การไหลของแก๊สในหัวฉีด: ไม่อัดตัว P₁ = P₀ − Q²/(2ρ₀A²) ส่วนแบบแอเดียแบติก c²/(γ − 1) + v²/2 คงที่ ให้ T₁ = T₀/(1 + (γ − 1)M²/2) และ Q² = P₀ρ₀A²(2γ/(γ − 1))(β^{2/γ} − β^{1+1/γ}) ซึ่งสูงสุดที่ M = 1, P₁* = P₀(2/(γ + 1))^{γ/(γ−1)}', 'เขียนสมการแบร์นูลลีรวมพลังงานภายในและความสัมพันธ์แอเดียแบติก', 'หาอุณหภูมิ ความดัน อัตราการไหล และสภาวะวิกฤติ'),
    13: ('compressible-nozzle-flow', '', '', ''),
    14: ('compressible-nozzle-flow', '', '', ''),
    15: ('compressible-nozzle-flow', '', '', ''),
    16: ('compressible-nozzle-flow', '', '', ''),
    17: ('compressible-nozzle-flow', '', '', ''),
    18: ('permanent-magnet-fields', 'แม่เหล็กถาวร: สนามบนแกนลดลงแบบ x^n (n ≈ −3) จึงหา n และไดโพลโมเมนต์จากกราฟ log B กับ log x และ M = m/V ลูปเหล็กส่งสนาม B_g = 2B₀(1 − d/√(d² + R²)) และฟลักซ์จากครึ่งแท่ง Φ = μ₀M((L/2)/√(R² + (L/2)²))πR²', 'วัดสนามด้วย Hall sensor ที่ระยะ ช่องอากาศ หรือวงแหวนต่าง ๆ', 'เขียนกราฟเส้นตรงหรือรวมฟลักซ์เพื่อหา n, M และ B₀'),
    19: ('permanent-magnet-fields', '', '', ''),
    20: ('permanent-magnet-fields', '', '', ''),
    21: ('permanent-magnet-fields', '', '', ''),
    22: ('permanent-magnet-fields', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2565_physics/sheet.json").read_text("utf-8"))
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
