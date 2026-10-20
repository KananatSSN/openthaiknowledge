"""Idempotent source claims for the 20 reviewed TPhO 19 (2563) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 1), ('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 2)],
    2: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 2)],
    3: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 3)],
    4: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 4)],
    5: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 5), ('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 6)],
    6: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 7)],
    7: [('สอวน_physics/tpho-63-physics/1_TPhO2020_Theory_Question.pdf', 8)],
    8: [('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 1), ('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 2)],
    9: [('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 3)],
    10: [('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 4), ('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 7)],
    11: [('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 5), ('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 6), ('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 8)],
    12: [('สอวน_physics/tpho-63-physics/2_TPhO2020_Theory_Question.pdf', 9)],
    13: [('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 1), ('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 2), ('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 3), ('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 4), ('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 5)],
    14: [('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 6)],
    15: [('สอวน_physics/tpho-63-physics/3_TPhO2020_Theory_Question.pdf', 7)],
    16: [('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 1)],
    17: [('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 2), ('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 3)],
    18: [('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 3)],
    19: [('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 4), ('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 5)],
    20: [('สอวน_physics/tpho-63-physics/TPhO2020_Experiment_Question.pdf', 5)],
}
UNITS = {
    1: ('strobe-water-drops', 'หยดน้ำใต้ไฟกระพริบ: เมื่อคาบไฟ T₀ + Δt ต่างจากคาบการหยด T₀ หยดถัดไปมาแทนที่ช้าหรือเร็วไป จึงเห็นการเคลื่อนที่ปรากฏด้วย u′ = √(2gh)Δt/(T₀ + Δt) และ a′ = g(Δt/(T₀ + Δt))² ส่วนคาบที่แกว่ง τ sin ωt ทำให้หยดที่ความเร็วสุดท้ายแกว่งขึ้นลงด้วยแอมพลิจูด d₀τ/(T₀²ω)', 'เขียนการกระจัดปรากฏของหยดถัดไปในแต่ละจังหวะไฟสว่าง', 'เทียบกับการเคลื่อนที่ความเร่งคงตัวหรืออินทิเกรตความเร็วปรากฏหาแอมพลิจูด'),
    2: ('strobe-water-drops', '', '', ''),
    3: ('strobe-water-drops', '', '', ''),
    4: ('optical-tweezer', 'แหนบเชิงแสง: ลำแสงที่ผ่านลูกแก้วห่างแกน a − x เบี่ยงเบน δ = 2((n − 1)/n)(a − x)/R โฟตอน Pλ/(hc) ต่อวินาทีพาโมเมนตัม P/c จึงเกิดแรงด้านข้าง (P/c)δ และสองลำแสงให้แรงคืนตัว ω² = 4P(n − 1)/(mcRn)', 'หามุมเบี่ยงเบนจากกฎของสเนลล์ที่มุมเล็ก', 'ใช้อัตราการเปลี่ยนโมเมนตัมของแสงหาแรงและความถี่การสั่น'),
    5: ('optical-tweezer', '', '', ''),
    6: ('optical-tweezer', '', '', ''),
    7: ('optical-tweezer', '', '', ''),
    8: ('adiabatic-lapse-rate', 'อุณหภูมิตามความสูง: อากาศแห้งขยายตัวแบบแอเดียแบติก T ∝ p^(2/7) และ dp/dz = −ρg ให้อัตราลดลง α = 2gμ/(7R) = 9.78 K/km ส่วนอากาศชื้นได้ความร้อนแฝงจากการควบแน่น T₂ − T₁ = −α(z₂ − z₁) − (αL_v/g)Δβ จึงลดลงช้ากว่า', 'ใช้ความสัมพันธ์แอเดียแบติกกับสมดุลความดันหาอุณหภูมิและความสูง', 'เพิ่มความร้อนแฝงจากไอน้ำที่ควบแน่นหาอุณหภูมิของอากาศชื้น'),
    9: ('adiabatic-lapse-rate', '', '', ''),
    10: ('adiabatic-lapse-rate', '', '', ''),
    11: ('adiabatic-lapse-rate', '', '', ''),
    12: ('adiabatic-lapse-rate', '', '', ''),
    13: ('gravitational-lens-fermat', 'เลนส์แรงโน้มถ่วงจากหลักการของแฟร์มาต์: ดัชนีหักเหเสมือน n = 1 + 2GM/(rc²) ทำให้เวลาเดินทาง ℓ₁/c + (2GM/c³) ln(4d₁d₂/y²) น้อยที่สุดที่ y² = (4GM/c²)d₁d₂/(d₁ + d₂) ภาพปรากฏที่มุม β = y/d₂ และวงแหวนของไอน์สไตน์ให้มวลของเลนส์', 'หาเลขชี้กำลังจากมิติแล้วเขียนเวลาเดินทางตามเส้นทางหักมุม', 'หาอนุพันธ์ของเวลาเป็นศูนย์แล้วใช้มุมของวงแหวนหามวล'),
    14: ('gravitational-lens-fermat', '', '', ''),
    15: ('gravitational-lens-fermat', '', '', ''),
    16: ('interleaved-book-friction', 'แรงเสียดทานของสมุดที่สอดสลับกัน: แผ่นกลางมีผิวสัมผัสสองด้าน μ = T/(2W₀) แรงดึงเพิ่มเชิงเส้น T = 2μW₀N + T₀ เมื่อซ้อนน้อย และเสริมกันเอง T ∝ √d exp(k/d) โดย k = 2μδN² เมื่อซ้อนมาก', 'วัดแรงดึงที่จำนวนแผ่นหรือระยะซ้อนต่าง ๆ', 'เขียนกราฟเส้นตรง T กับ N หรือ ln(T/√d) กับ 1/d หาความชันและ μ'),
    17: ('interleaved-book-friction', '', '', ''),
    18: ('interleaved-book-friction', '', '', ''),
    19: ('interleaved-book-friction', '', '', ''),
    20: ('interleaved-book-friction', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2563_physics/sheet.json").read_text("utf-8"))
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
