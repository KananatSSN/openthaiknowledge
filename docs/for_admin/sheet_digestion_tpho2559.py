"""Idempotent source claims for the 23 reviewed TPhO 15 (2559) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 2)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 3)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 4)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 5), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 6)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 7)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 8)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 9), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 10), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 11)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 12), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 13)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 13)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 14)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 14)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 15)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 16)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 17)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 18)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 19)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 20), ('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 21)],
    18: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 22)],
    19: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Theory.pdf', 23)],
    20: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Expt_Question.pdf', 1)],
    21: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Expt_Question.pdf', 2)],
    22: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Expt_Question.pdf', 3)],
    23: [('physics/level/upper-secondary/posn-physics/tpho-59-physics/TPhO2016_Expt_Question.pdf', 4)],
}
UNITS = {
    1: ('venturi-bernoulli-spray', 'ตามเส้นกระแสเดียวกัน P + ρgy + ½ρv² คงที่ ในท่อคอดที่ต่อหลอดดูดน้ำ อากาศที่คอดเร็วขึ้นจนความดันต่ำกว่าบรรยากาศ ρ_wgh จึงดูดน้ำขึ้นได้ ด้านในของท่อโค้งเส้นกระแสชิดกันเพราะความดันด้านนอกต้องให้แรงสู่ศูนย์กลาง', 'ใช้ความต่อเนื่องหาอัตราเร็วที่แต่ละช่วงของท่อ', 'ใช้สมการแบร์นูลลีเทียบความดันที่คอดกับความดันที่ยกน้ำได้'),
    2: ('thermal-wire-stretch', 'ลวดห้อยน้ำหนักยืด WL/(AY) เมื่ออุณหภูมิเพิ่มทั้งความยาวขยาย αLΔT และมอดุลัสเปลี่ยน εΔT ถ้าเลือกพื้นที่หน้าตัด A = (W/Y₀)(ε/(αY₀) − 1) (ต้องมี ε > 0) วัตถุจะอยู่ที่เดิม', 'เขียนระยะยืดรวมจากความร้อนและแรงดึงที่อุณหภูมิใหม่', 'กระจายอันดับหนึ่งแล้วจับให้เท่ากับระยะยืดเดิม'),
    3: ('thermal-wire-stretch', '', '', ''),
    4: ('thermal-wire-stretch', '', '', ''),
    5: ('radiating-filament-lamp', 'ไส้หลอดสุญญากาศรับกำลัง σA(T⁴ − T₀⁴) เมื่อร้อนคงที่ และเมื่อ T ≫ T₀ กับ R ∝ T^p ได้ I ∝ Vⁿ โดย n = (4 − p)/(4 + p) = 0.6 สำหรับ p = 1', 'เขียนสมดุลกำลังไฟฟ้ากับการแผ่รังสีสุทธิ', 'กำจัด T และ R ด้วย R = V/I หาเลขชี้กำลัง'),
    6: ('radiating-filament-lamp', '', '', ''),
    7: ('air-conditioner-humidity', 'เครื่องปรับอากาศ: ความดันไอน้ำ hP_sat/100 ไนโตรเจนรับความดันที่เหลือและมีจำนวนโมลคงที่ จึงหาปริมาตรอากาศเดิม งานของบรรยากาศ มวลน้ำที่ควบแน่น และความร้อนทั้งหมดที่ต้องเอาออกจากกฎข้อที่หนึ่งได้', 'ใช้ความชื้นสัมพัทธ์และความดันย่อยหาโมลของแต่ละก๊าซ', 'รวมพลังงานภายใน งาน และความร้อนแฝงของการควบแน่น'),
    8: ('air-conditioner-humidity', '', '', ''),
    9: ('air-conditioner-humidity', '', '', ''),
    10: ('air-conditioner-humidity', '', '', ''),
    11: ('air-conditioner-humidity', '', '', ''),
    12: ('air-conditioner-humidity', '', '', ''),
    13: ('air-conditioner-humidity', '', '', ''),
    14: ('pump-drill-mechanics', 'สว่านปั๊ม: แรงกด F₁ บนคานเบาให้ทอร์ก F₁r/tan θ ต้านด้วยทอร์กเสียดทาน k(Mg + F₁) งานต่อรอบ F₁L(θ₀ − θₙ) และถ้าล้อตุ้นต้องปั่นเกลียวกลับได้ n รอบพอดี F₁ = 4nπkMg/(L(θ₀ − θₙ) − 2nπk) สำหรับใบมีดยาว 2r ได้ k = μr/2', 'หาแรงตึงเชือกจากสมดุลของคานแล้วหาทอร์กบนแกน', 'ใช้งาน-พลังงานในช่วงคลายเกลียวและปั่นเกลียวหาอัตราเร็วเชิงมุมและแรงกด'),
    15: ('pump-drill-mechanics', '', '', ''),
    16: ('pump-drill-mechanics', '', '', ''),
    17: ('pump-drill-mechanics', '', '', ''),
    18: ('pump-drill-mechanics', '', '', ''),
    19: ('pump-drill-mechanics', '', '', ''),
    20: ('ldr-calibration', 'ตัวต้านทานไวแสง R = c₁E^γ กับแหล่งกำเนิดแบบจุด E ∝ 1/x² ให้ log R = −2γ log x + c₂ จึงหา γ จากความชัน แล้วใช้ R ที่วัดได้หา E และฟลักซ์ E·4πx² สเปกตรัมจากเกรตติง λ = d sin θ ต้องปรับแก้ด้วยกำลังแสงของหลอดในการหาการตอบสนองสัมพัทธ์', 'เขียนกราฟ log R กับ log x หาเลขชี้กำลัง', 'แปลงความต้านทานเป็น illuminance และฟลักซ์ หรือปรับแก้ด้วยกำลังแสง'),
    21: ('ldr-calibration', '', '', ''),
    22: ('ldr-calibration', '', '', ''),
    23: ('ldr-calibration', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2559_physics/sheet.json").read_text("utf-8"))
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
