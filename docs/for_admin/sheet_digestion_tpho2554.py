"""Idempotent source claims for the 20 reviewed TPhO 10 (2554) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 2)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 3)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 4)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 5)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 6)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 7)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 8)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 9)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 10)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 11)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 12)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 13)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 14)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 15), ('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 16), ('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 17)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 18)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_theory_with_solution.pdf', 19)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_exp.pdf', 1)],
    18: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_exp.pdf', 2)],
    19: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_exp.pdf', 3)],
    20: [('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_exp.pdf', 4), ('physics/level/upper-secondary/posn-physics/tpho-54-physics/tpho_10_exp.pdf', 5)],
}
UNITS = {
    1: ('superconducting-ring-levitation', 'วงแหวนตัวนำยวดยิ่งรักษาฟลักซ์รวม πR²B_z + LI ให้คงที่ เมื่อตกลงในสนาม B_z = B₀(1 + αz), B_r = B₀βr กระแส πR²αB₀z/L ทำให้เกิดแรงยก kz กับ k = 2B₀²αβπ²R⁴/L วงแหวนสมดุลที่ z₀ = mg/k สั่นแบบฮาร์มอนิกด้วย ω = √(k/m) แอมพลิจูด z₀ และกระแสสูงสุดที่ 2z₀', 'ใช้ฟลักซ์คงที่หากระแสที่ตำแหน่ง z', 'หาแรงจากสนามแนวรัศมีแล้วเขียนสมการการเคลื่อนที่แบบฮาร์มอนิก'),
    2: ('superconducting-ring-levitation', '', '', ''),
    3: ('superconducting-ring-levitation', '', '', ''),
    4: ('superconducting-ring-levitation', '', '', ''),
    5: ('superconducting-ring-levitation', '', '', ''),
    6: ('two-mass-rotating-string', 'มวลสองก้อนบนเชือกเส้นเดียวหมุนรอบแกนดิ่ง: แรงตึงแนวดิ่งรับน้ำหนัก T₂cos α = (m₁ + m₂)g, T₁cos β = m₁g แรงแนวระดับให้แรงสู่ศูนย์กลาง เมื่อผูกมวลกลางที่กึ่งกลาง (m₁/(m₁ + m₂))sin²β/cos β = sin α tan β − tan α sin β + tan α sin α และเมื่อมวลกลางไถลได้แรงตึงเท่ากันทั้งเส้น cos β = m₁cos α/(m₁ + m₂)', 'เขียนสมดุลแรงแนวดิ่งและแรงสู่ศูนย์กลางของแต่ละมวล', 'กำจัดอัตราเร็วเชิงมุมเพื่อหาความสัมพันธ์ของมุมหรือความยาว'),
    7: ('two-mass-rotating-string', '', '', ''),
    8: ('two-mass-rotating-string', '', '', ''),
    9: ('two-mass-rotating-string', '', '', ''),
    10: ('two-mass-rotating-string', '', '', ''),
    11: ('two-mass-rotating-string', '', '', ''),
    12: ('falling-jet-surface-tension', 'ลำน้ำที่ตกจากท่อเล็กลงตามแบร์นูลลีและความต่อเนื่อง R = R₀(1 + 2gh/v₀²)^(−1/4) แรงตึงผิวเพิ่มความดันในลำน้ำ γ/R ทำให้รัศมีเปลี่ยนเล็กน้อย ΔR หาได้จากการประมาณอันดับหนึ่ง ลำน้ำแตกเป็นหยดหลังเวลาประมาณ 2.91√(ρR₀³/γ) และการคงปริมาตรกับพื้นที่ผิวให้หยดรัศมี 3R/2', 'ใช้แบร์นูลลีกับความต่อเนื่องหารัศมีลำน้ำ', 'เพิ่มความดันจากแรงตึงผิวแล้วประมาณอันดับหนึ่งหรือใช้การอนุรักษ์ปริมาตรและพื้นที่ผิว'),
    13: ('falling-jet-surface-tension', '', '', ''),
    14: ('falling-jet-surface-tension', '', '', ''),
    15: ('falling-jet-surface-tension', '', '', ''),
    16: ('falling-jet-surface-tension', '', '', ''),
    17: ('diode-black-box', 'กล่องดำที่มีไดโอดชนิดเดียวกันต่อเป็นสองเส้นขนานทิศตรงข้ามกับตัวต้านทาน R: ความต่างศักย์ขีดเริ่มแต่ละทิศเท่ากับจำนวนไดโอดในเส้นที่นำไฟฟ้าคูณขีดเริ่มของไดโอดหนึ่งตัว และช่วงที่นำไฟฟ้าเต็มที่ความชันของกราฟ V กับ I คือ R', 'อ่านความต่างศักย์ขีดเริ่มของทั้งสองทิศจากกราฟ I-V', 'หากระแสจากตัวต้านทานอ้างอิงแล้วหาความชันของช่วงเส้นตรง'),
    18: ('diode-black-box', '', '', ''),
    19: ('pencil-roller-friction', 'ความเสียดทานสถิตวัดจากความชันของกราฟแรงที่ทำให้เริ่มเลื่อนกับแรงกด F_s = μ_sN ไม้บรรทัดบนดินสอสองแท่งเริ่มเลื่อนเมื่อ μ_kN_B = μ_sN_A ซึ่ง N_B/N_A = x_A/x_B จึงได้ μ_s/μ_k เป็นความชันของกราฟ x_A กับ x_B', 'วัดแรงที่ทำให้เริ่มเลื่อนที่แรงกดต่าง ๆ แล้วหาความชัน', 'ใช้สมดุลโมเมนต์หาอัตราส่วนแรงกดจากระยะถึงศูนย์กลางมวล'),
    20: ('pencil-roller-friction', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2554_physics/sheet.json").read_text("utf-8"))
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
