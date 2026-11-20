"""Idempotent source claims for the 24 reviewed TPhO 18 (2562) items."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    1: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 2)],
    2: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 3)],
    3: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 4)],
    4: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 5)],
    5: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 6), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 7)],
    6: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 8), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 9)],
    7: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 10)],
    8: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 11), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 12), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 13)],
    9: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 14), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 15), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 16)],
    10: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 17), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 18)],
    11: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 19)],
    12: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 20), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 21), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 22)],
    13: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 23)],
    14: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 24)],
    15: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 25), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 26)],
    16: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 27)],
    17: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 28)],
    18: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Theory (1).pdf', 29)],
    19: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 1), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 2)],
    20: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 2)],
    21: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 3)],
    22: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 4), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 5)],
    23: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 6), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 7)],
    24: [('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 8), ('physics/level/upper-secondary/posn-physics/tpho-62-physics/TPhO2019_Experiment (1).pdf', 9)],
}
UNITS = {
    1: ('hydraulic-jump', 'ไฮดรอลิกจัมพ์: โมเมนตัมต่อเวลา ρAv² ต่างกันเท่ากับแรงดันของของไหลหยุดนิ่ง ½ρgL(h₂² − h₁²) ร่วมกับความต่อเนื่อง h₁v₁ = h₂v₂ ได้ h₂ = (h₁/2)[√(1 + 8v₁²/(gh₁)) − 1] พลังงานที่หายไปต่อปริมาตร ρg(h₂ − h₁)(h₂² + h₁²)/(4h₁h₂) และจัมพ์วงกลมรัศมี R = 4Q²/(π²d²gH²)', 'เขียนสมดุลโมเมนตัมกับแรงดันของของไหลหยุดนิ่งและความต่อเนื่อง', 'แก้หาความสูงหลังจัมพ์ พลังงานที่หาย หรือรัศมีจัมพ์วงกลม'),
    2: ('hydraulic-jump', '', '', ''),
    3: ('hydraulic-jump', '', '', ''),
    4: ('hydraulic-jump', '', '', ''),
    5: ('hydraulic-jump', '', '', ''),
    6: ('ac-power-transmission', 'การส่งไฟฟ้า: กำลังสูญเสียในสายเทียบกับโหลดคือ P_LR_w/V_L² ความเหนี่ยวนำของโซเลนอยด์ μ₀n²πr²ℓ และความเหนี่ยวนำร่วม M = √(L₁L₂) ทำให้หม้อแปลงขึ้นแรงดัน V_S/V_L = M/L_L และลดอัตราส่วนกำลังสูญเสียลงด้วยกำลังสองของอัตราส่วนแรงดัน', 'หาความเหนี่ยวนำจากฟลักซ์ที่คล้องขดลวดต่อกระแส', 'เขียนสมการวงจรหม้อแปลงหากระแสปฐมภูมิและอัตราส่วนกำลังสูญเสีย'),
    7: ('ac-power-transmission', '', '', ''),
    8: ('ac-power-transmission', '', '', ''),
    9: ('ac-power-transmission', '', '', ''),
    10: ('ac-power-transmission', '', '', ''),
    11: ('protostar-ignition', 'กลุ่มแก๊สที่ยึดด้วยแรงโน้มถ่วง: ทฤษฎีบทไวเรียล P.E. = −2 K.E. กับพลังงานศักย์ทรงกลม −(3/5)GM²/R ให้อุณหภูมิเฉลี่ย GMm_p/(5Rk_B) และ dE/dT < 0 ความดันใจกลาง ½GMρ/R ต้านด้วยความดันแก๊สและ degeneracy ทำให้มีมวลน้อยที่สุดราว 0.1 มวลดวงอาทิตย์ที่ร้อนถึง 10⁷ K', 'ใช้กฎสเตฟาน-โบลซ์มันน์และทฤษฎีบทไวเรียลหาอุณหภูมิ', 'สมดุลความดันใจกลางกับความดันแก๊สและ degeneracy หาความหนาแน่นและมวลน้อยที่สุด'),
    12: ('protostar-ignition', '', '', ''),
    13: ('protostar-ignition', '', '', ''),
    14: ('protostar-ignition', '', '', ''),
    15: ('protostar-ignition', '', '', ''),
    16: ('protostar-ignition', '', '', ''),
    17: ('protostar-ignition', '', '', ''),
    18: ('protostar-ignition', '', '', ''),
    19: ('led-diode-characteristics', 'หลอด LED: ที่กระแสน้อย ln I เป็นเส้นตรงกับ V ความชัน e/(nkT) และจุดตัด ln I₀ ส่วนที่กระแสสูงเบี่ยงด้วย IR_s ความต่างศักย์ขีดเริ่ม eV_t = hc/λ − E₀ เป็นเส้นตรงกับ 1/λ จึงหาความยาวคลื่นของ LED อินฟราเรดได้', 'เขียนกราฟเส้นตรงจากสมการของชอกลีย์หรือจาก V_t กับ 1/λ', 'อ่านความชันและจุดตัดหาแฟกเตอร์อุดมคติ กระแสอิ่มตัว ความต้านทานอนุกรม หรือความยาวคลื่น'),
    20: ('led-diode-characteristics', '', '', ''),
    21: ('led-diode-characteristics', '', '', ''),
    22: ('led-diode-characteristics', '', '', ''),
    23: ('led-photovoltaic-cell', 'LED เป็นเซลล์โฟโตวอลเทอิก: ฟิลแฟกเตอร์ FF = P_max/(V_OCI_SC) ความชันใกล้ V_OC ให้ −1/R_S และความชันช่วงความต่างศักย์น้อยให้ −1/(R_SH + R_S)', 'วัดกราฟ I-V ของเซลล์และจุดกำลังสูงสุด', 'คำนวณฟิลแฟกเตอร์และความต้านทานอนุกรมหรือขนานจากความชัน'),
    24: ('led-photovoltaic-cell', '', '', ''),
}

def main():
    sheet = json.loads((ROOT / "otk/sheets/tpho2562_physics/sheet.json").read_text("utf-8"))
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
