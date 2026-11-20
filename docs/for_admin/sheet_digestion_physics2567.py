"""Idempotent source claims for the 16 reviewed 2567 physics questions."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "physics/level/upper-secondary/posn-physics/posn1-67-physics.pdf"
UNITS = {
    1: ('chord-descent-time', '', '', ''),
    2: ('incline-projectile-range', 'ยิง 30° เหนือแนวระดับลงพื้นเอียงลาดลง 30° ระยะตามพื้นเอียงเป็น 2u²/g และความเร็วที่จุดกระทบทำมุม 30° กับพื้นเอียง', 'หาเวลาที่ตำแหน่งตกบนแนวพื้นเอียง', 'หาระยะและทิศความเร็วที่เวลานั้น'),
    3: ('energy-fraction-collision', 'มวลเท่ากันชนกันโดยรู้สัดส่วนพลังงานจลน์ที่เหลือ ใช้โมเมนตัมกับพลังงานแก้สมการกำลังสอง', 'เขียน vA+vB=u และ vA²+vB²=fu²', 'เลือกรากที่ A ไม่แซง B'),
    4: ('rolling-incline-friction', 'ล้อกลิ้งไม่ไถลลงพื้นเอียงรับแรงเสียดทาน MgI sinθ/(I+MR²)', 'เขียนสมการแรงและทอร์กกับเงื่อนไข a=αR', 'แก้หาแรงเสียดทาน'),
    5: ('close-loops-force', 'วงลวดร่วมแกนที่ห่างกัน d≪R ประมาณเป็นลวดตรงยาว 2πR แรงจึงเป็น μ₀I²R/d ดูดกันเมื่อกระแสทางเดียวกัน', 'ใช้แรงต่อความยาวของลวดตรงขนาน', 'คูณด้วยเส้นรอบวงและหาทิศจากทิศกระแส'),
    6: ('charge-pair-axis-field', 'ประจุเท่ากันสองตัวที่ (0,±a) ให้สนามบนแกน x เป็น 2kqx/(x²+a²)³ᐟ² ซึ่งสูงสุด 4kq/(3√3a²)', 'รวมองค์ประกอบแนว x ของสองประจุ', 'หาค่าสูงสุดของ ξ/(1+ξ²)³ᐟ²'),
    7: ('multi-plate-capacitance', 'แผ่นขนานหลายแผ่นมีความจุเท่ากับจำนวนช่องที่สองข้างต่างศักย์คูณ ε₀A/d', 'ระบุศักย์ของแต่ละแผ่นจากการต่อสาย', 'นับช่องที่มีผลต่างศักย์'),
    8: ('steady-rc-network', '', '', ''),
    9: ('concentric-loops-field', 'วงลวดร่วมศูนย์สองวงให้สนามที่ศูนย์กลาง (μ₀I/2)(1/R₁ ± 1/R₂) บวกเมื่อกระแสวนทางเดียวกัน', 'หาทิศการวนของกระแสในแต่ละวง', 'รวมสนามแบบมีเครื่องหมาย'),
    10: ('moving-source-echo-speed', '', '', ''),
    11: ('harmonic-parallel-resistance', 'ตัวต้านทาน 1..N kΩ ขนานกันมี 1/R = H_N ≈ ln N + 0.577 ต่อ kΩ', 'รวมส่วนกลับเป็นอนุกรมฮาร์มอนิก', 'ประมาณด้วย ln N บวกค่าคงที่ออยเลอร์'),
    12: ('raindrop-deviation', 'แสงหักเหเข้าหยดน้ำ สะท้อนภายในหนึ่งครั้งแล้วออก ทำมุมกับแสงเข้า 4θ−2i', 'รวมมุมหมุนจากการหักเหสองครั้งและการสะท้อน', 'หามุมระหว่างแนวแสงออกกับแนวแสงเข้า'),
    13: ('soap-bubble-pressure', 'ฟองสบู่มีสองผิว ความดันภายในสูงกว่าภายนอก 4γ/R', 'สมดุลแรงบนครึ่งทรงกลม', 'นับแรงตึงผิวสองผิว'),
    14: ('lens-index-sensitivity', 'จาก 1/f ∝ (μ−1) การเปลี่ยนเล็กน้อยให้ δf/f = −δμ/(μ−1)', 'เขียน f แปรผกผันกับ μ−1', 'หาผลต่างเล็กแบบสัมพัทธ์'),
    15: ('conduction-radiation-balance', 'ในสภาวะคงตัว ความร้อนที่นำผ่านแผ่น K(T₁−T₂)/l เท่ากับการแผ่รังสีจากผิวดำ σT₂⁴', 'ตั้งสมการสมดุลพลังงาน', 'แก้สมการกำลังสี่เชิงตัวเลข'),
    16: ('self-equal-capacitance', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/posn2567_physics/sheet.json").read_text("utf-8"))
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
        source = {"sheet": SOURCE, "item": item["number"]}
        if source not in unit["sources"]:
            unit["sources"].append(source)
        if item["generator"] not in unit["covered_by"]:
            unit["covered_by"].append(item["generator"])
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", "utf-8")


if __name__ == "__main__":
    main()
