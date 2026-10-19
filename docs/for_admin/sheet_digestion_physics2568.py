"""Idempotent source claims for the 25 reviewed 2568 physics questions."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "สอวน_physics/posn1-68-physics.pdf"
UNITS = {
    1: ('projectile-direction-height', 'ความเร็วแนวระดับของโพรเจกไทล์คงที่ ความสูงที่ทิศความเร็วเป็นมุม β หาได้จาก (u_y²−v_y²)/(2g) โดย v_y = u_x tanβ', 'หาองค์ประกอบความเร็วแนวดิ่งที่จุดนั้น', 'ใช้ v²=u²−2gh แนวดิ่ง'),
    2: ('offset-disc-collision-direction', '', '', ''),
    3: ('spring-closest-approach', 'ขณะสปริงระหว่างสองมวลหดมากที่สุด ทั้งสองเคลื่อนที่ด้วยความเร็วเท่ากัน mu/(m+M)', 'ระยะใกล้สุดเกิดเมื่อความเร็วสัมพัทธ์เป็นศูนย์', 'ใช้การอนุรักษ์โมเมนตัม'),
    4: ('charged-ring-axial-field', '', '', ''),
    5: ('rotating-ring-current', 'วงแหวนประจุ Q หมุนด้วย ω ให้กระแส Qω/(2π)', 'หาคาบการหมุน', 'หารประจุด้วยคาบ'),
    6: ('rotating-ring-field', 'วงแหวนประจุที่หมุนให้สนามที่ศูนย์กลาง μ₀Qω/(4πR)', 'หากระแสจากการหมุน', 'ใช้สนามที่ศูนย์กลางวงกระแส μ₀I/(2R)'),
    7: ('split-wire-parallel-maximum', 'ตัดลวด R เป็นสองส่วนแล้วต่อขนาน ความต้านทานสูงสุด R/4 เมื่อตัดครึ่ง', 'เขียน R∥ = R₁(R−R₁)/R', 'หาค่าสูงสุดของพาราโบลา'),
    8: ('self-equal-resistance', 'R₁ อนุกรมกับ R₂∥R เท่ากับ R เมื่อ R² − R₁R − R₁R₂ = 0', 'รวมความต้านทานแล้วตั้งเท่ากับ R', 'เลือกรากบวกของสมการกำลังสอง'),
    9: ('thermal-resistance', 'ความต้านทานความร้อนของแท่งคือ L/(KA) เช่นเดียวกับความต้านทานไฟฟ้า', 'เขียนกฎของฟูริเยร์ Q=KAΔT/L', 'เทียบกับรูป ΔT/ℛ'),
    10: ('thermal-junction-temperature', 'แท่งนำความร้อนต่ออนุกรมมีอัตราไหลเท่ากัน อุณหภูมิรอยต่อแบ่งตามสัดส่วนความต้านทานความร้อน', 'หาความต้านทานความร้อนแต่ละท่อน', 'แบ่งผลต่างอุณหภูมิตามสัดส่วน'),
    11: ('accelerating-tank-pressure', 'ของเหลวในภาชนะที่เร่งขึ้นด้วย a มีความดันเพิ่มตามความลึกเป็น ρ(g+a)h', 'เขียนกฎข้อสองของนิวตันกับลำน้ำ', 'บวกความดันบรรยากาศที่ผิว'),
    12: ('torricelli-jet-range', 'น้ำพุ่งจากรูที่สูง y ใต้ผิวน้ำ h−y ตกไกล x = 2√(y(h−y))', 'ใช้ทอร์ริเชลลี v=√(2g(h−y))', 'ใช้เวลาตกจากความสูง y'),
    13: ('galilean-beam-expander', '', '', ''),
    14: ('longitudinal-image-length', 'ภาพของวัตถุที่วางตามแกนหาได้โดยหาภาพของปลายทั้งสองด้วยสมการเลนส์', 'หาระยะภาพของแต่ละปลาย', 'หารผลต่างระยะภาพด้วยความยาววัตถุ'),
    15: ('stretched-cord-volume', 'V=πr²l ให้ δV/V = δl/l − 2δr/r เมื่อทิ้งพจน์อันดับสอง', 'หาผลต่างอันดับหนึ่งของ πr²l', 'แทนความสัมพันธ์ของ δr กับ δl'),
    16: ('charging-source-power', '', '', ''),
    17: ('series-capacitor-sum', 'ตัวเก็บประจุอนุกรมมีประจุเท่ากัน หาความจุรวมจากผลบวก 1/C_i', 'รวมส่วนกลับความจุเป็นอนุกรม', 'คูณความจุรวมด้วยแรงเคลื่อน'),
    18: ('moving-source-echo-speed', '', '', ''),
    19: ('capacitor-plate-force', '', '', ''),
    20: ('equatorial-apparent-gravity', 'ที่เส้นศูนย์สูตร น้ำหนักปรากฏลดลงด้วยแรงสู่ศูนย์กลาง g = g₀ − 4π²R/T²', 'หาความเร็วเชิงมุมจากคาบดาราคติ', 'ลบ ω²R ออกจาก g ที่ขั้ว'),
    21: ('equatorial-apparent-gravity', '', '', ''),
    22: ('binary-orbit-period', 'ระบบสองวัตถุระยะห่าง D มีคาบ 2π√(D³/(G(M+m))) จึงแปรตาม D^(3/2) และ (M+m)^(−1/2)', 'ใช้ ω² = G(M+m)/D³', 'หาอัตราส่วนคาบเมื่อเปลี่ยน D และมวลรวม'),
    23: ('triangle-three-body-period', 'ดาวสามดวงมวลเท่ากันที่มุมสามเหลี่ยมด้านเท่า D มีคาบ 2π√(D³/(3GM))', 'รวมแรงดึงดูดสองแรงเข้าหาศูนย์กลาง', 'ใช้รัศมีวงโคจร D/√3'),
    24: ('poiseuille-tank-drain', 'น้ำไหลจากถังผ่านท่อหนืดด้วยผลต่างความดัน ρgh ความเร็วเฉลี่ย ρghr²/(8ηl)', 'ใช้กฎของปัวเซยหาอัตราการไหล', 'หารด้วยพื้นที่หน้าตัด'),
    25: ('hairpin-wire-field', 'ลวดกึ่งอนันต์ที่ปลายอยู่บนแนวตั้งฉากผ่านจุดให้สนามครึ่งหนึ่งของลวดยาวอนันต์ รวมกับครึ่งวงกลมได้ (μ₀I/(4R))(1+2/π)', 'ใช้ครึ่งหนึ่งของ μ₀I/(2πR) สำหรับแต่ละลวดกึ่งอนันต์', 'บวกสนามครึ่งวงกลมตามทิศการวน'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/posn2568_physics/sheet.json").read_text("utf-8"))
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
