"""Idempotently claim reviewed POSN 2561 chemistry questions."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = "สอวน_chemistry/posn1-61-chemistry.pdf"
UNITS = {
    1: (
        "isoelectronic-ion-count-groups",
        "chem.isoelectronic_ion_count_groups.procedure",
        "ไอออนและอะตอมมีจำนวนอิเล็กตรอนเท่ากันเมื่อ Z−q เท่ากัน โดย q เป็นประจุมีเครื่องหมาย; เลขมวลไม่เปลี่ยนจำนวนอิเล็กตรอน",
        "อ่านเลขอะตอมและประจุของอนุภาคแต่ละตัว แยกเลขมวลออก",
        "คำนวณ Z−q แล้วเลือกกลุ่มที่ทั้งสามค่าเท่ากัน",
    ),
    2: (
        "isotope-ion-nuclear-notation",
        "chem.isotope_ion_nuclear_notation.procedure",
        "", "", "",
    ),
    3: (
        "photon-energy-wavelength-comparison",
        "chem.photon_energy_wavelength_comparison.procedure",
        "พลังงานโฟตอน E=hc/λ และความถี่ f=c/λ จึงแปรผกผันกับความยาวคลื่น",
        "เปรียบเทียบความยาวคลื่นของเส้นที่ระบุ",
        "กลับลำดับเมื่อเปรียบเทียบความถี่หรือพลังงาน และตรวจแต่ละข้อความ",
    ),
}


def main():
    sheet = json.loads((ROOT / "otk/sheets/posn2561_chemistry/sheet.json").read_text())
    destination = ROOT / "otk/knowledge/chemistry"
    for item in sheet["items"]:
        slug, uid, statement, first, second = UNITS[item["number"]]
        path = destination / f"{slug}.json"
        raw = json.loads(path.read_text()) if path.exists() else {
            "subject": "เคมี", "topic": item["topic"], "level": sheet["level"],
            "units": [],
        }
        unit = next((value for value in raw["units"] if value["id"] == uid), None)
        if unit is None:
            unit = {
                "id": uid, "kind": "procedure", "title": item["title"],
                "statement": statement, "steps": [first, second],
                "sources": [], "covered_by": [], "note": item["note"],
            }
            raw["units"].append(unit)
        source = {"sheet": SOURCE, "item": item["number"]}
        if source not in unit["sources"]:
            unit["sources"].append(source)
        if item["generator"] not in unit["covered_by"]:
            unit["covered_by"].append(item["generator"])
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
