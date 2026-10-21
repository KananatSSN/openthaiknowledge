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
    4: (
        "period-two-proton-offset-shells",
        "chem.period_two_proton_offset_shells.procedure",
        "เมื่อ X อยู่คาบ 2 และ Z มีโปรตอนเพิ่มตามที่กำหนด ต้องตรวจทุกค่า X ที่เป็นไปได้; เลขมวลยังขึ้นกับนิวตรอนที่โจทย์ไม่ระบุ",
        "ไล่เลขอะตอมของ X ทุกค่าที่โจทย์อนุญาต แล้วหาเลขอะตอม Z",
        "ตรวจคาบ ชั้นอิเล็กตรอนที่สอง และเวเลนซ์ทุกกรณี แยกโปรตอนจากเลขมวล",
    ),
    5: (
        "halogen-reactivity-from-configuration",
        "chem.halogen_reactivity_from_configuration.procedure",
        "แฮโลเจนมีการจัดอิเล็กตรอนชั้นนอก ns²np⁵; ในตัวเลือกที่กำหนด ความไวต่อปฏิกิริยาของแฮโลเจนลดลงเมื่อเลื่อนลงหมู่ F > Cl > Br",
        "ระบุธาตุจากจำนวนอิเล็กตรอนในแต่ละการจัดเรียง",
        "คัดอโลหะและเปรียบเทียบตำแหน่งแฮโลเจนในหมู่ 17",
    ),
    6: (
        "second-ionization-energy-comparison",
        "chem.second_ionization_energy_comparison.procedure",
        "IE₂ เป็นพลังงานดึงอิเล็กตรอนออกจากไอออน +1; K⁺ และ Rb⁺ มีชั้นปิดทำให้ IE₂ สูง และค่าคู่ Se–Br ต้องตรวจข้อมูลจริง",
        "แปลงเลขอะตอมเป็นธาตุและระบุไอออน +1 ที่ถูกดึงอิเล็กตรอน",
        "เทียบค่า IE₂ ของธาตุแต่ละคู่ตามลำดับที่โจทย์ให้",
    ),
    7: (
        "atomic-ionic-radius-comparison",
        "chem.atomic_ionic_radius_comparison.procedure",
        "รัศมีอะตอมและไอออนเป็นคนละนิยาม; เมื่อต้องเปรียบเทียบข้ามชนิดควรใช้ข้อมูลรัศมีชุดเดียวกันที่กำหนดไว้ชัดเจน",
        "อ่านตารางรัศมีของ Na, Na⁺, Cl, Ca, Br และ Br⁻ ในโจทย์",
        "ตรวจอสมการทีละคู่ในแต่ละตัวเลือก แล้วเลือกสายที่จริงทั้งหมด",
    ),
    8: (
        "periodic-property-order-p-ca-as",
        "chem.periodic_property_order_p_ca_as.procedure",
        "P และ As อยู่หมู่ 15 โดย P มี IE₁ และ EN สูงกว่า As; Ca มีรัศมีมากกว่าและจุดหลอมเหลวของ Ca สูงกว่า As สีเทา",
        "แปลงสัญลักษณ์สมมติกลับเป็น P, Ca และ As",
        "ตรวจแต่ละสมบัติแยกกัน โดยระบุรูปของ As และเงื่อนไขจุดหลอมเหลว",
    ),
    9: (
        "oxide-acid-base-water-reactions",
        "chem.oxide_acid_base_water_reactions.procedure",
        "SO₃ ทำปฏิกิริยากับน้ำให้ H₂SO₄ และ Na₂O ให้ NaOH; SiO₂ กับ Al₂O₃ ไม่ให้สารละลายตามเงื่อนไข",
        "พิจารณาว่าออกไซด์แต่ละตัวทำปฏิกิริยากับน้ำได้หรือไม่",
        "จำแนกผลิตภัณฑ์ที่ละลายน้ำว่าเป็นกรดหรือเบส แล้วจับคู่ X กับ Y",
    ),
    10: (
        "halogen-extraction-metal-water-identification",
        "chem.halogen_extraction_metal_water_identification.procedure",
        "คลอรีนออกซิไดซ์ I⁻ เป็น I₂ ซึ่งมีสีม่วงใน CCl₄; Mg ทำปฏิกิริยากับน้ำร้อนให้ Mg(OH)₂ และ H₂ จึงได้เกลือ MgI₂",
        "ใช้สีในชั้นตัวทำละลายอินทรีย์ระบุไอโอดีน แล้วใช้ปฏิกิริยากับน้ำร้อนระบุแมกนีเซียม",
        "เขียนสูตรเกลือจาก Mg²⁺ และ I⁻ แล้วตรวจสี IE₃ และการละลายของซัลเฟต",
    ),
    11: (
        "phosphorus-oxidation-oxide-chloride",
        "chem.phosphorus_oxidation_oxide_chloride.procedure",
        "ธาตุคาบ 3 ที่มีเลขออกซิเดชัน −3 ถึง +5 คือ P; ออกไซด์ของ P มี P เป็นบวก และ PCl₅ มีรูปทรงสมมาตรไม่เป็นขั้วในสถานะแก๊ส",
        "ระบุ P จากคาบและช่วงเลขออกซิเดชัน",
        "เทียบสถานะและโมเลกุลของ P กับเลขออกซิเดชันในออกไซด์และขั้วของคลอไรด์",
    ),
    12: (
        "colored-aqueous-ion-pairs",
        "chem.colored_aqueous_ion_pairs.procedure",
        "ไดโครเมตในน้ำสีส้มและ Fe³⁺ สีเหลือง; เกลือ Na⁺, K⁺ และ Rb⁺ กับแอนไอออนทั่วไปไม่มีสีในสารละลายเจือจาง",
        "ระบุไอออนที่อยู่ในสารละลายของสารแต่ละชนิด",
        "ตรวจทั้งสองสารในแต่ละคู่ ไม่ตัดสินจากตัวที่มีสีเพียงตัวเดียว",
    ),
    13: (
        "carbonate-sulfate-precipitation-identification",
        "chem.carbonate_sulfate_precipitation_identification.procedure",
        "Mg²⁺ ให้ตะกอนคาร์บอเนตแต่ซัลเฟตละลายได้; K⁺ ไม่ให้ตะกอนในชุดทดสอบ; Ba²⁺ ให้ตะกอนทั้งคาร์บอเนตและซัลเฟต",
        "แปลงผลตะกอนของ A, B, C เป็นรูปแบบสำหรับ Cl⁻, CO₃²⁻ และ SO₄²⁻",
        "จับคู่รูปแบบกับ Mg²⁺, K⁺, Ba²⁺ แล้วตรวจสูตรเกลือในตัวเลือก",
    ),
    14: (
        "coordination-complex-oxidation-ranking",
        "chem.coordination_complex_oxidation_ranking.procedure",
        "เมื่อต้องหาเลขออกซิเดชันสูงที่สุดในสารเชิงซ้อน ต้องคัดสารที่มีไอออนเชิงซ้อนก่อน; [Fe(CN)₆]⁴⁻ มี Fe(II) ส่วน [Cr(NH₃)₆]³⁺ มี Cr(III)",
        "แยกสารเชิงซ้อนออกจากออกไซด์และเกลือธรรมดา",
        "ใช้ประจุของลิแกนด์และประจุไอออนเชิงซ้อนแก้เลขออกซิเดชันของโลหะ",
    ),
    15: (
        "beta-minus-atomic-number-increase",
        "chem.beta_minus_atomic_number_increase.procedure",
        "การแผ่ β⁻ เปลี่ยนนิวตรอนเป็นโปรตอน ทำให้เลขอะตอมเพิ่ม 1 แต่เลขมวลคงเดิม; β⁺ ทำให้เลขอะตอมลด 1",
        "เขียนการเปลี่ยนจำนวนโปรตอนและนิวตรอนของการแผ่แต่ละชนิด",
        "เลือกชนิดที่ให้เลขอะตอมของธาตุใหม่เพิ่มหนึ่งหน่วยและเลขมวลคงเดิม",
    ),
    16: (
        "parent-mass-exponential-half-life-graph",
        "chem.parent_mass_exponential_half_life_graph.procedure",
        "มวลของสารกัมมันตรังสีตั้งต้นลดแบบยกกำลัง m(t)=m₀2^(−t/t½); ที่หนึ่งครึ่งชีวิตเหลือครึ่ง และสองครึ่งชีวิตเหลือหนึ่งในสี่",
        "ดูว่ากราฟเริ่มจากมวลสารตั้งต้น ไม่ใช่เริ่มจากศูนย์เหมือนผลิตภัณฑ์",
        "ตรวจมวลที่เวลา t½ และ 2t½ เพื่อตัดกราฟที่ชันผิด",
    ),
    17: (
        "identify-light-nuclei-fusion-reaction",
        "chem.identify_light_nuclei_fusion_reaction.procedure",
        "ฟิวชันคือนิวเคลียสเบาสองตัวรวมเป็นนิวเคลียสหนักกว่า; ³He กับ ²H ให้ ⁴He และโปรตอน ส่วนการสลายบีตาและฟิชชันไม่ใช่ฟิวชัน",
        "แยกชนิดอนุภาคตั้งต้นของแต่ละสมการนิวเคลียร์",
        "เลือกสมการที่นิวเคลียสเบาสองตัวเข้าร่วมและได้นิวเคลียสหนักกว่า",
    ),
    18: (
        "calcium-rubidium-basic-oxides",
        "chem.calcium_rubidium_basic_oxides.procedure",
        "เลขอะตอม 7, 16, 20, 37 คือ N, S, Ca, Rb; CaO และ Rb₂O ทำปฏิกิริยากับน้ำให้ไฮดรอกไซด์ซึ่งทำให้ฟีนอลฟ์ทาลีนสีชมพู",
        "ระบุธาตุจากเลขอะตอม แล้วแยกโลหะจากอโลหะ",
        "พิจารณาผลิตภัณฑ์เมื่อออกไซด์ทำปฏิกิริยากับน้ำ และเลือกคู่ที่ให้เบสทั้งสอง",
    ),
    19: (
        "gallium-period-group-reaction-inference",
        "chem.gallium_period_group_reaction_inference.procedure",
        "Ga มีเลขอะตอม 31 อยู่คาบ 4 หมู่ 13; 2Ga+3Cl₂ ให้ 2GaCl₃ และปฏิกิริยากับกรดให้ H₂ กับสารละลาย Ga³⁺ ไม่มีสี",
        "ใช้อัตราส่วน X:Cl₂ = 2:3 อนุมานคลอไรด์ XCl₃ แล้วใช้ช่วงเลขอะตอมกับสมบัติน้ำและกรด",
        "ระบุ Ga และตรวจข้อความเรื่องคาบ หมู่ และแก๊สจากกรด",
    ),
    20: (
        "rubidium-water-halogen-sulfate-reactions",
        "chem.rubidium_water_halogen_sulfate_reactions.procedure",
        "Rb เป็นโลหะหมู่ 1 เลขอะตอม 37; 2Rb+2H₂O→2RbOH+H₂, I₂ ไม่แทนที่ Br⁻ และ Ba²⁺ กับ SO₄²⁻ ให้ BaSO₄ ตกตะกอน",
        "ระบุ M ว่าเป็น Rb และตรวจประจุ +1 เพื่อเขียนสูตรเกลือ",
        "ดุลปฏิกิริยาน้ำ ตรวจลำดับการแทนที่แฮโลเจนและการตกตะกอนของซัลเฟต",
    ),
    21: (
        "cyanogen-octet-bond-lone-pair-count",
        "chem.cyanogen_octet_bond_lone_pair_count.procedure",
        "C₂N₂ ที่เป็นกลางและครบออกเตตมีโครง N≡C–C≡N จึงมีพันธะเดี่ยว 1 พันธะสาม 2 และอิเล็กตรอนคู่โดดเดี่ยวบน N อย่างละ 1",
        "วางโครง N–C–C–N และเติมพันธะให้ C แต่ละตัวมีพันธะรวม 4 ส่วน N มีพันธะรวม 3",
        "นับจำนวนพันธะแต่ละอันดับและคู่โดดเดี่ยวทั้งโมเลกุล",
    ),
    22: (
        "molecular-versus-network-covalent-properties",
        "chem.molecular_versus_network_covalent_properties.procedure",
        "CS₂ เป็นโมเลกุลเส้นตรงไม่มีขั้ว ส่วน SiO₂ เป็นผลึกโคเวเลนต์ร่างตาข่ายที่มีจุดหลอมเหลวสูงและไม่ละลายน้ำ",
        "ระบุธาตุจากเลขอะตอมแล้วสร้างสูตร CS₂ และ SiO₂",
        "เปรียบเทียบแรงระหว่างโมเลกุลกับพันธะในผลึกร่างตาข่าย รวมทั้งการละลาย",
    ),
    23: (
        "vsepr-symmetric-molecule-polarity",
        "chem.vsepr_symmetric_molecule_polarity.procedure",
        "SbCl₅ แบบโมเลกุลแก๊สมีรูปทรงพีระมิดคู่ฐานสามเหลี่ยมและไม่มีขั้ว; SiH₄ ทรงสี่หน้าไม่มีขั้ว; TeF₆ ทรงแปดหน้าไม่มีคู่โดดเดี่ยวบน Te",
        "นับโดเมนอิเล็กตรอนรอบอะตอมกลางของสารแต่ละตัว",
        "วาดรูปทรง VSEPR แล้วพิจารณาการหักล้างของขั้วพันธะ",
    ),
    24: (
        "covalent-compound-water-solubility-screen",
        "chem.covalent_compound_water_solubility_screen.procedure",
        "เอทานอล HF และกรดแอซีติกละลายน้ำได้ดี ขณะที่เบนซีน CCl₄ และ CS₂ ละลายได้น้อย และ NH₄Cl เป็นสารไอออนิก",
        "ตรวจชนิดพันธะและสมบัติการละลายน้ำของสารทุกตัวในแต่ละกลุ่ม",
        "ตัดกลุ่มที่มีสารไม่ละลายน้ำหรือไม่ใช่สารโคเวเลนต์ แล้วเลือกกลุ่มที่เหลือ",
    ),
    25: (
        "solvent-extraction-polarity-inference",
        "chem.solvent_extraction_polarity_inference.procedure",
        "ตัวทำละลายที่ใช้สกัดเรียงจากขั้วน้อยไปมากช่วยบอกแนวโน้มความมีขั้วของสาร แต่ไม่ยืนยันโครงสร้างหรือจัดสารเป็นมีขั้ว/ไม่มีขั้วแบบเด็ดขาด",
        "อ่านสารเด่นในส่วนสกัดเฮกเซน คลอโรฟอร์ม และเอทานอลตามลำดับ",
        "อนุมาน C มีแนวโน้มขั้วมากกว่า B แล้วแยกข้อสรุปที่เป็นไปได้ออกจากข้อสรุปที่ยืนยันเกินข้อมูล",
    ),
    26: (
        "fractional-distillation-boiling-order",
        "chem.fractional_distillation_boiling_order.procedure",
        "การกลั่นลำดับส่วนให้สารที่มีจุดเดือดต่ำออกก่อน: บิวเทนประมาณ −0.5°C ไดเอทิลอีเทอร์ 34.6°C และเอทานอล 78.4°C",
        "เปรียบเทียบแรงลอนดอน ขั้วโมเลกุล และพันธะไฮโดรเจนของสารทั้งสาม",
        "เรียงจุดเดือดจากน้อยไปมากเป็นลำดับการกลั่นออก",
    ),
    27: (
        "central-atom-octet-exceptions",
        "chem.central_atom_octet_exceptions.procedure",
        "NO₂ มีอิเล็กตรอนคี่และ N ไม่ครบออกเตต; XeF₄ มี 12 อิเล็กตรอนรอบ Xe; B ใน BF₄⁻ และ C ใน CO₃²⁻ มีแปดอิเล็กตรอน",
        "นับอิเล็กตรอนเวเลนซ์รวมและวาดโครงสร้างลิวอิสของแต่ละอนุภาค",
        "นับอิเล็กตรอนรอบอะตอมกลางแล้วเลือกคู่ที่มีแปดตัวทั้งคู่",
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
