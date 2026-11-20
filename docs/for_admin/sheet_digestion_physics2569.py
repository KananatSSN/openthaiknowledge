"""Idempotent source claims for the 30 reviewed 2569 physics questions."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "physics/level/upper-secondary/posn-physics/posn1-69-physics.pdf"
UNITS = {
    1: ('energy-fraction-collision', '', '', ''),
    2: ('pegged-pendulum-period', 'ลูกตุ้มที่มีหมุดขวางแกว่งครึ่งรอบด้วยความยาวเต็มและครึ่งรอบด้วยความยาวที่เหลือ คาบรวมเป็นผลบวกครึ่งคาบทั้งสอง', 'หาครึ่งคาบของแต่ละความยาว', 'รวมเป็นคาบเต็มแล้วเทียบกับคาบเดิม'),
    3: ('upward-terminal-speed', '', '', ''),
    4: ('collinear-charge-equilibrium', '', '', ''),
    5: ('air-gap-lateral-shift', '', '', ''),
    6: ('resistor-combination-count', 'ตัวต้านทานสามตัวใช้ทีละหนึ่ง สอง หรือสามตัวแบบอนุกรมขนานได้ 3+6+8 = 17 แบบ ค่าที่ซ้ำกันลดจำนวนค่าที่ต่างกัน', 'แจกแจงทุกแบบของแต่ละกลุ่มย่อย', 'นับเฉพาะค่าที่ไม่ซ้ำกัน'),
    7: ('thermal-resistance', '', '', ''),
    8: ('explosion-energy-split', 'เมื่อวัตถุแยกเป็นสองส่วนเท่ากันตามแนวเดิม โมเมนตัมคงที่และพลังงานที่เพิ่มกำหนดผลต่างความเร็ว', 'เขียน v₁+v₂ = 2u', 'ใช้พลังงานหาผลต่างของความเร็ว'),
    9: ('charged-ring-axial-field', '', '', ''),
    10: ('loop-axial-field-ratio', '', '', ''),
    11: ('split-lens-focal', 'ผ่าเลนส์นูนสองหน้าตามระนาบกลางได้เลนส์แกมราบ 1/f = (μ−1)/R ของผิวที่เหลือ', 'เขียน 1/F เป็นผลรวมของสองผิว', 'เก็บเฉพาะผิวของครึ่งที่สนใจ'),
    12: ('real-image-minimum-separation', 'เลนส์นูนให้ภาพจริงของวัตถุจริงได้เมื่อระยะวัตถุถึงภาพไม่น้อยกว่า 4f', 'เขียน x = u + uf/(u−f)', 'หาค่าต่ำสุดที่ u = 2f'),
    13: ('pushed-wedge-rest', 'มวลบนผิวลื่นของลิ่มที่ถูกผลักไม่ไถลเมื่อ a = g tanβ', 'ให้แรงปกติให้ทั้งความเร่งแนวระดับและรับน้ำหนัก', 'หารสองสมการหา a'),
    14: ('heavy-rope-lowest-tension', '', '', ''),
    15: ('disc-with-hole-centre', 'ศูนย์กลางมวลของแผ่นที่เจาะรูหาได้โดยคิดรูเป็นมวลลบ', 'หาพื้นที่และตำแหน่งของรู', 'ใช้โมเมนต์ของแผ่นเต็มลบโมเมนต์ของรู'),
    16: ('hose-reaction-force', 'ลำน้ำที่พุ่งออกจากท่อด้วยความเร็ว v ทำให้ท่อรับแรงปฏิกิริยา ρAv²', 'หาอัตราการไหลของมวล ρAv', 'คูณด้วยความเร็ว'),
    17: ('spinning-ring-tension', 'วงลวดมวล M ที่หมุนด้วยอัตราเร็ว v มีแรงตึง Mv²/(2πR)', 'แรงตึงสองข้างของส่วนโค้งเล็กให้แรงสู่ศูนย์กลาง Tθ', 'ตั้งเท่ากับมวลส่วนโค้งคูณ v²/R'),
    18: ('offset-disc-collision-direction', '', '', ''),
    19: ('symmetric-pole-projectile', 'จุดที่สูงเท่ากันบนวิถีโพรเจกไทล์อยู่สมมาตรรอบจุดสูงสุด ระยะตกจึงห่างเสาแรก L₁ + L₂', 'ใช้ความสมมาตรของพาราโบลา', 'หาตำแหน่งตกจากระยะยิงทั้งหมด'),
    20: ('sound-speed-gas', 'ในแก๊สอุดมคติ P/ρ = RT/M ดังนั้น v² = γRT/M โดย T เป็นเคลวิน', 'แทน P/ρ ด้วยกฎแก๊สอุดมคติ', 'แปลงอุณหภูมิเป็นเคลวิน'),
    21: ('maximum-load-power', '', '', ''),
    22: ('charge-sharing-heat', '', '', ''),
    23: ('parallel-charge-sharing', 'ตัวเก็บประจุที่มีประจุต่อขนานกับตัวที่ว่าง แรงดันสุดท้ายเท่ากัน ประจุแบ่งตามความจุ', 'ประจุรวมคงที่', 'แบ่งตามสัดส่วนความจุ'),
    24: ('hanging-plate-tilt', '', '', ''),
    25: ('wall-rebound-collision', 'มวลใหญ่ที่สะท้อนกำแพงแล้วชนมวลเล็กแบบยืดหยุ่น ส่งมวลเล็กออกไปด้วยความเร็วเกือบ 3u', 'หาความเร็วมวลใหญ่หลังสะท้อน', 'ใช้สูตรชนยืดหยุ่นหนึ่งมิติ'),
    26: ('steam-volume-ratio', '', '', ''),
    27: ('parallel-echo-distance', 'เรือแล่นขนานหน้าผา เสียงเดินทางตามสามเหลี่ยมหน้าจั่ว (vT/2)² = L² + (uT/2)²', 'เขียนระยะทางเสียงและระยะทางเรือในเวลา T', 'ใช้พีทาโกรัสในครึ่งสามเหลี่ยม'),
    28: ('wedge-energy-recoil', 'มวลไถลลงลิ่มบนพื้นลื่นถึงพื้น ใช้โมเมนตัมแนวระดับและพลังงานได้ V = m√(2gh/(M(M+m)))', 'โมเมนตัมแนวระดับรวมเป็นศูนย์', 'พลังงานศักย์เปลี่ยนเป็นพลังงานจลน์ของทั้งสอง'),
    29: ('projectile-receding-condition', 'ระยะจากจุดยิงถึงโพรเจกไทล์เพิ่มตลอดเมื่อ cos²θ ≤ 8/9 (θ จากแนวดิ่ง) คือ sinθ ≥ 1/3', 'ให้พจน์คงที่ในวงเล็บไม่เป็นลบ', 'แปลงเป็นเงื่อนไขของ sinθ'),
    30: ('diverging-converging-pair', 'ภาพเสมือนจากเลนส์ตัวแรกเป็นวัตถุของเลนส์ตัวที่สอง หาระยะวัตถุจากสมการเลนส์แล้วลบระยะโฟกัสของเลนส์แรก', 'หาระยะวัตถุของเลนส์ตัวที่สองจากตำแหน่งภาพ', 'ลบระยะภาพเสมือนของเลนส์แรก'),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/posn2569_physics/sheet.json").read_text("utf-8"))
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
