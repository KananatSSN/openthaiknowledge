"""Idempotent source claims for the 17 reviewed TPhO 14 (2558) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 1)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 2)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 3)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 4)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 5)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 6)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 7)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 8)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 9), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 10)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 11)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 12)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 13), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 14), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 15)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 16), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO14_theory.pdf', 17)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 2)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 3), ('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 4)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 5)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-58-physics/TPhO2015_Lab_Problem.pdf', 6)],
}
UNITS = {
    1: ('charged-pendulum-field', 'ลูกตุ้มประจุในสนามไฟฟ้าแนวราบ: ปล่อยจากแนวดิ่งแกว่งได้ถึง θ_m = 2 tan⁻¹(qE/mg) สมดุลที่ tan θ₀ = qE/mg และสั่นรอบ θ₀ ด้วย ω² = √(g² + (qE/m)²)/ℓ', 'ใช้งานของสนามไฟฟ้าเท่ากับพลังงานศักย์โน้มถ่วงที่เพิ่มขึ้น', 'กระจายแรงในแนวสัมผัสรอบมุมสมดุลหาค่าคงที่ของแรงคืนตัว'),
    2: ('charged-pendulum-field', '', '', ''),
    3: ('charged-pendulum-field', '', '', ''),
    4: ('railway-barrier-counterweight', 'คานกั้นรถไฟที่มีตุ้มถ่วง: ความเร่งเชิงมุม (τ + mgℓ − MgL/2)/(ML²/3 + mℓ²) มากที่สุดเมื่อ mℓ² + 2(τ/g − ML/2)ℓ − ML²/3 = 0 และถ้า τ ≈ MgL/2 ได้ ℓ ≈ L√(M/(3m))', 'เขียนทอร์กลัพธ์และโมเมนต์ความเฉื่อยรอบจุดหมุน', 'หาอนุพันธ์ของความเร่งเชิงมุมเทียบกับ ℓ ให้เป็นศูนย์'),
    5: ('railway-barrier-counterweight', '', '', ''),
    6: ('sealed-vessel-water-film', 'ภาชนะปิดปริมาตรคงตัว: ก๊าซมีความดัน P₀T₁/T₀ ความดันส่วนที่เกินมาจากไอน้ำที่ระเหยจากฟิล์ม จึงหาโมลน้ำและความหนาฟิล์มได้ และเวลาให้ความร้อนเพิ่มตามความร้อนของไอน้ำและความร้อนแฝง', 'ใช้กฎของก๊าซแยกความดันย่อยของก๊าซและไอน้ำ', 'แปลงโมลน้ำเป็นปริมาตรของเหลวหรือความร้อนที่ต้องใช้'),
    7: ('sealed-vessel-water-film', '', '', ''),
    8: ('sealed-vessel-water-film', '', '', ''),
    9: ('pop-gun-adiabatic', 'ฉับโผง: อากาศในกระบอกถูกอัดแบบแอเดียแบติกจนแรงดันชนะแรงเสียดทานสถิต L = L₀(PₐA/(F + PₐA))^(1/γ) แล้วขยายตัวดันลูกปอ งานที่ได้ให้อัตราเร็ว และกระบอกยาวที่สุดที่ยังเร่งได้คือ D = L[((F + PₐA)/(f + PₐA))^(1/γ) − 1]', 'ใช้ PV^γ คงที่หาความยาวอากาศเมื่อลูกเริ่มเคลื่อน', 'อินทิเกรตแรงลัพธ์ตามระยะหาอัตราเร็วและระยะที่แรงลัพธ์เป็นศูนย์'),
    10: ('pop-gun-adiabatic', '', '', ''),
    11: ('pop-gun-adiabatic', '', '', ''),
    12: ('eddy-heating-disc', 'แผ่นทองแดงในสนาม B₀ cos ωt: อีเอ็มเอฟรอบวงรัศมี r เป็น πr²B₀ω sin ωt วงแหวนแต่ละวงสูญเสียกำลัง ε²zΔr/(2πρr) รวมทั้งแผ่นได้กำลังเฉลี่ย zπa⁴B₀²ω²/(16ρ)', 'หาอีเอ็มเอฟจากอัตราการเปลี่ยนฟลักซ์', 'รวมกำลังของวงแหวนทุกวงแล้วเฉลี่ยตามเวลา'),
    13: ('eddy-heating-disc', '', '', ''),
    14: ('saline-viscosity-tension', 'น้ำเกลือพุ่งจากเข็มแนวนอนให้ Q = √(g/2y)πr²x จึงหารัศมีรูเข็ม การไหลผ่านเข็มตามกฎปัวซอย Q = πr⁴ρg(h − y)/(8ηℓ) ให้ความหนืด เมื่อคิดสายน้ำเกลืออนุกรมใช้ ℓ/r⁴ + L/R⁴ และหยดน้ำ mg = 1.4πr_oγ ให้ความตึงผิว', 'เขียนกราฟเส้นตรงของอัตราการไหลกับระยะตกหรือความสูง', 'แปลงความชันเป็นรัศมี ความหนืด หรือใช้น้ำหนักหยดหาความตึงผิว'),
    15: ('saline-viscosity-tension', '', '', ''),
    16: ('saline-viscosity-tension', '', '', ''),
    17: ('saline-viscosity-tension', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2558_physics/sheet.json").read_text("utf-8"))
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
