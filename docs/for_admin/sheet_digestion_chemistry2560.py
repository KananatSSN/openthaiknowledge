"""Idempotently claim the reviewed first batch; leave the other 67 pending."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "สอวน_chemistry/posn1-60-chemistry.pdf"
UNITS = {
    1: (
        "canal-ray-electron-mass",
        "รังสีบวกหลังแคโทดเป็นไอออนของแก๊ส ส่วนรังสีแคโทดหลังแอโนดเป็นอิเล็กตรอน; มวลไอออนมากกว่ามวลอิเล็กตรอนมาก",
        "อ่านตำแหน่งขั้วและฉากเรืองแสงเพื่อระบุอนุภาค",
        "เทียบมวลของไอออนและอิเล็กตรอนโดยคูณจำนวนนิวคลีออน",
    ),
    2: (
        "halogen-predicted-oxidation",
        "ธาตุหมู่ 17 มีเวเลนซ์ ns²np⁵ และ p⁵ มีอิเล็กตรอนเดี่ยวหนึ่งตัว; แบบจำลอง Ts ทำนายเลขออกซิเดชันหลายค่า รวมทั้งค่าบวก",
        "แยกข้อเท็จจริงการจัดอิเล็กตรอนออกจากค่าที่แบบจำลองทำนาย",
        "ตรวจว่าชุดเลขออกซิเดชันที่เป็นไปได้มีค่าอื่นนอกจาก −1",
    ),
    3: (
        "hydrogen-emission-lines",
        "เมื่อกระตุ้นอะตอมไฮโดรเจนจำนวนมากถึงระดับ n เส้นสเปกตรัมจากทุกการเปลี่ยนลงระหว่างระดับ 1 ถึง n มีได้ n(n−1)/2 เส้นในช่วงระดับที่ใช้",
        "ระบุระดับสูงสุดจากแผนภาพ ไม่ใช้ค่าความยาวคลื่นปัดเศษตัดสินการสั่นพ้อง",
        "นับทุกคู่ระดับที่เปลี่ยนลงได้ รวมการคายพลังงานหลายขั้นในกลุ่มอะตอม",
    ),
    4: (
        "isotope-ion-nuclear-notation",
        "ไอโซโทปมีเลขอะตอม Z เท่ากัน; ประจุ q=Z−e และเลขมวล A=Z+N",
        "หาจำนวนโปรตอนจากจำนวนอิเล็กตรอนและประจุของไอออน",
        "ปรับจำนวนนิวตรอนตามเงื่อนไขไอโซโทป แล้วบวก Z เพื่อหาเลขมวล",
    ),
    5: (
        "ionic-radius-occupied-shells",
        "เมื่อไอออนมีจำนวนชั้นอิเล็กตรอนที่ครองอยู่ต่างกัน ไอออนที่มีชั้นนอกสุดต่ำกว่ามีขนาดเล็กกว่าในคู่ที่เลือก",
        "หาจำนวนอิเล็กตรอนของไอออนจากเลขอะตอมและประจุ",
        "เปรียบเทียบชั้นนอกสุดที่ครองอยู่ของไอออนทั้งคู่",
    ),
    6: (
        "oxide-transition-ion-configuration",
        "เมื่อเกิดแคตไอออนของ Mn Fe Co Ni ต้องนำอิเล็กตรอน 4s ออกก่อน 3d; ในออกไซด์ที่กำหนดให้ O=−2 หาเลขออกซิเดชันของโลหะจากความเป็นกลาง",
        "ใช้ผลรวมเลขออกซิเดชันเป็นศูนย์หาเลขออกซิเดชันของโลหะ",
        "นำอิเล็กตรอน 4s ออกก่อน แล้วนำจาก 3d ตามจำนวนที่ยังขาด",
    ),
}


def main():
    sheet = json.loads((ROOT / "otk/sheets/posn2560_chemistry/sheet.json").read_text())
    destination = ROOT / "otk/knowledge/chemistry"
    destination.mkdir(parents=True, exist_ok=True)
    for item in sheet["items"]:
        slug, statement, first, second = UNITS[item["number"]]
        path = destination / f"{slug}.json"
        raw = json.loads(path.read_text()) if path.exists() else {
            "subject": "เคมี", "topic": item["topic"], "level": sheet["level"], "units": [],
        }
        uid = f"chem.{slug.replace('-', '_')}.procedure"
        unit = {
            "id": uid, "kind": "procedure", "title": item["title"],
            "statement": statement, "steps": [first, second],
            "sources": [{"sheet": SOURCE, "item": item["number"]}],
            "covered_by": [item["generator"]], "note": item["note"],
        }
        previous = next((u for u in raw["units"] if u["id"] == uid), None)
        if previous is None:
            raw["units"].append(unit)
        else:
            for field in ("sources", "covered_by"):
                for value in unit[field]:
                    if value not in previous[field]:
                        previous[field].append(value)
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
