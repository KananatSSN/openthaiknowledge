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
    28: (
        "ammonium-equivalent-nh-bonds",
        "chem.ammonium_equivalent_nh_bonds.procedure",
        "NH₄⁺ มีพันธะ N–H สมมูลกันสี่พันธะในรูปทรงสี่หน้า แม้พันธะหนึ่งจะอธิบายการเกิดด้วยการบริจาคคู่โดดเดี่ยวจาก NH₃ ให้ H⁺",
        "สร้างโครงสร้างลิวอิส NH₄⁺ แล้วนับคู่พันธะและคู่โดดเดี่ยวบน N",
        "ใช้สมมาตรของทรงสี่หน้าเปรียบเทียบพันธะ N–H ทั้งสี่หลังเกิดไอออน",
    ),
    29: (
        "bent-versus-linear-vsepr-shapes",
        "chem.bent_versus_linear_vsepr_shapes.procedure",
        "SO₂ มีรูปทรงงอเพราะ S มีคู่โดดเดี่ยว ส่วน CO₂, XeF₂ และ BeCl₂ โมเลกุลเดี่ยวในสถานะแก๊สมีรูปทรงเส้นตรง",
        "นับโดเมนพันธะและคู่โดดเดี่ยวรอบอะตอมกลาง",
        "เปรียบเทียบรูปทรงโมเลกุลตาม VSEPR แล้วเลือกชนิดที่ต่างจากอีกสาม",
    ),
    30: (
        "smallest-bond-angle-comparison",
        "chem.smallest_bond_angle_comparison.procedure",
        "PCl₅ แบบโมเลกุลแก๊สมีมุมระหว่างพันธะแกนกับพันธะระนาบ 90° ซึ่งน้อยกว่ามุมต่ำสุดของ NCl₃, SOCl₂ และ CH₂Cl₂",
        "หารูปทรง VSEPR ของโมเลกุลแต่ละตัวและมุมที่เป็นไปได้ทั้งหมด",
        "นำมุมที่เล็กที่สุดของแต่ละโมเลกุลมาเปรียบเทียบ โดยตรวจ SOCl₂ กับข้อมูลการวัด",
    ),
    31: (
        "permanent-dipole-intermolecular-pairs",
        "chem.permanent_dipole_intermolecular_pairs.procedure",
        "PH₃ และ H₂S เป็นโมเลกุลมีขั้วอ่อนจึงมีแรงระหว่างขั้วทั้งคู่; CO₂, O₂, CH₄ และ SiH₄ ไม่มีขั้วถาวร",
        "พิจารณารูปร่างและสมมาตรของโมเลกุลทุกตัวในแต่ละคู่",
        "ตรวจว่าทั้งสองตัวมีโมเมนต์ขั้วถาวรหรือไม่ โดยแยกแรงลอนดอนที่มีในทุกสาร",
    ),
    32: (
        "carbonate-bond-bf3-polarity-fluoromethane-boiling",
        "chem.carbonate_bond_bf3_polarity_fluoromethane_boiling.procedure",
        "C–O ใน CO₃²⁻ มีอันดับพันธะเฉลี่ย 4/3 จึงยาวกว่า C=O ใน CO₂; BF₃ และ F₂ ไม่มีขั้ว; CF₄ เดือดต่ำกว่า CHF₃",
        "นับอันดับพันธะจากโครงสร้างเรโซแนนซ์คาร์บอเนตและตรวจรูปทรง BF₃",
        "เทียบข้อมูลจุดเดือด CF₄ กับ CHF₃ แล้วเลือกข้อความที่ถูกทั้งหมด",
    ),
    33: (
        "hydrogen-chlorine-photoreaction-gas-fraction",
        "chem.hydrogen_chlorine_photoreaction_gas_fraction.procedure",
        "H₂ + Cl₂ → 2HCl รักษาจำนวนโมลแก๊สรวม; ปริมาณ H₂ เริ่มต้นเท่ากับ H₂ ที่เหลือบวกครึ่งหนึ่งของ HCl ที่เกิด",
        "ใช้เศษส่วนปริมาตรแทนเศษส่วนโมลที่อุณหภูมิและความดันเดียวกัน",
        "ทำบัญชี H₂, Cl₂ และ HCl ก่อนหลัง แล้วตรวจร้อยละ Cl₂ ที่ลดลง",
    ),
    34: (
        "sulfate-metal-from-barium-precipitate",
        "chem.sulfate_metal_from_barium_precipitate.procedure",
        "ASO₄ และ BaSO₄ มีอัตราส่วนโมล 1:1; จากมวลตะกอนหาโมลซัลเฟตและมวลโมล ASO₄ แล้วลบมวล SO₄ เพื่อระบุ A",
        "คำนวณโมล BaSO₄ จากมวลตะกอนและมวลโมล 233 g/mol",
        "เทียบโมล ASO₄ เท่ากัน หามวลโมลของโลหะ และตรวจย้อนกับตัวเลือก",
    ),
    35: (
        "combustion-air-demand-gas-mixture",
        "chem.combustion_air_demand_gas_mixture.procedure",
        "แก๊ส CO และ H₂ ใช้ O₂ อย่างละ 1/2 ปริมาตร, CH₄ ใช้ 2 และ C₂H₄ ใช้ 3; CO₂ กับ Ar ไม่ใช้ O₂; ปริมาตรอากาศขึ้นกับเศษส่วน O₂ ในอากาศ",
        "คูณสัดส่วนปริมาตรของแก๊สที่เผาไหม้ได้ด้วยสัมประสิทธิ์ O₂ ของแต่ละชนิด",
        "รวมความต้องการ O₂ แล้วหารด้วยเศษส่วน O₂ ในอากาศ",
    ),
    36: (
        "magnesium-nitride-ammonia-yield",
        "chem.magnesium_nitride_ammonia_yield.procedure",
        "แมกนีเซียม 3 mol ให้ Mg₃N₂ 1 mol ซึ่งไฮโดรไลซ์ให้ NH₃ 2 mol; คำนวณย้อนหลังและหารด้วยเศษส่วนผลได้ของไนไตรด์",
        "เปลี่ยนปริมาตร NH₃ ที่ 0°C และ 1 atm เป็นโมลด้วย 22.4 L/mol",
        "ใช้อัตราส่วน Mg:NH₃ = 3:2 และปรับด้วยร้อยละผลได้ก่อนแปลงเป็นกรัม",
    ),
    37: (
        "carbonate-left-after-silver-precipitation",
        "chem.carbonate_left_after_silver_precipitation.procedure",
        "Ag₂CO₃ ใช้ Ag⁺ สองโมลต่อ CO₃²⁻ หนึ่งโมล; หักคาร์บอเนตที่ตกตะกอนแล้วหารด้วยปริมาตรรวม",
        "หาจำนวนโมลเริ่มต้นของ CO₃²⁻ และ Ag⁺ เพื่อระบุ Ag⁺ เป็นสารกำหนดปริมาณ",
        "หัก CO₃²⁻ ครึ่งหนึ่งของโมล Ag⁺ แล้วหารด้วยปริมาตรสารละลายผสม",
    ),
    38: (
        "aluminium-zinc-alloy-hydrogen-balance",
        "chem.aluminium_zinc_alloy_hydrogen_balance.procedure",
        "Al และ Zn ในโลหะผสมให้ H₂ ตามอัตราส่วน 3/2 และ 1 mol ต่อ mol โลหะตามลำดับ; ใช้มวลที่ละลายและปริมาตรแก๊สตั้งสมการคู่",
        "ลบมวล Si กับ Cu ที่เหลือออกจากมวลโลหะผสมและแปลงปริมาตร H₂ เป็นโมล",
        "แก้สมการมวล 27a+65z และโมล H₂=1.5a+z เพื่อหาร้อยละมวล Al",
    ),
    39: (
        "ferric-after-acidic-permanganate",
        "chem.ferric_after_acidic_permanganate.procedure",
        "Fe₂(SO₄)₃ เริ่มต้นให้ Fe³⁺ สองโมลต่อโมล; MnO₄⁻ ในกรดออกซิไดซ์ Fe²⁺ ห้าโมลต่อโมล แล้วหาร Fe³⁺ รวมด้วยปริมาตรหลังผสม",
        "นับ Fe³⁺ เริ่มต้นจากเกลือเฟอร์ริกและโมล Fe²⁺ จากเกลือของมอร์",
        "ใช้สมการรีดอกซ์หาปริมาณ Fe³⁺ ที่เกิดและหารด้วยปริมาตรรวม",
    ),
    40: (
        "diborane-borohydride-percent-yield",
        "chem.diborane_borohydride_percent_yield.procedure",
        "ดุลสมการ 3NaBH₄+4BF₃→3NaBF₄+2B₂H₆ แล้วคำนวณย้อนจากผลได้จริงด้วยอัตราส่วน NaBH₄:B₂H₆ = 3:2",
        "หารโมล B₂H₆ ที่ต้องการด้วยเศษส่วนผลได้เพื่อหาโมลตามทฤษฎี",
        "คูณด้วย 3/2 เพื่อหาโมล NaBH₄ ที่ต้องใช้",
    ),
    41: (
        "azide-nitrogen-two-reaction-gas-law",
        "chem.azide_nitrogen_two_reaction_gas_law.procedure",
        "NaN₃ หนึ่งโมลให้ N₂ รวม 8/5 โมลจากการสลายตัวและปฏิกิริยา Na กับ KNO₃; ใช้ PV=nRT ที่อุณหภูมิและความดันกำหนด",
        "รวม N₂ จากสมการทั้งสองต่อโมล NaN₃ และหาโมล N₂ ด้วยกฎแก๊สอุดมคติ",
        "ใช้สัดส่วน 5/8 หาโมล NaN₃ แล้วคูณมวลโมล 65 g/mol",
    ),
    42: (
        "trona-carbonate-bicarbonate-acid-equivalents",
        "chem.trona_carbonate_bicarbonate_acid_equivalents.procedure",
        "โทรนาหนึ่งสูตรมีคาร์บอเนตหนึ่งตัวและไบคาร์บอเนตหนึ่งตัว จึงใช้ H⁺ สามโมลต่อโมลสูตรเมื่อเปลี่ยนเป็น CO₂",
        "แปลงมวลแร่เป็นโมลโดยหารด้วยมวลสูตร 226 g/mol",
        "คูณโมลแร่ด้วยสามและหารด้วยความเข้มข้น HCl เพื่อหาปริมาตร",
    ),
    43: (
        "potassium-superoxide-carbon-dioxide-oxygen-limit",
        "chem.potassium_superoxide_carbon_dioxide_oxygen_limit.procedure",
        "ดุล 4KO₂+2CO₂→2K₂CO₃+3O₂ แล้วเทียบปริมาณ O₂ ที่สารตั้งต้นแต่ละชนิดให้ได้เพื่อเลือกสารกำหนดปริมาณ",
        "แปลงมวล KO₂ และปริมาตร CO₂ ที่ STP เป็นจำนวนโมล",
        "ใช้ปริมาณ O₂ ต่ำกว่าจากสองสารตั้งต้นแล้วแปลงกลับเป็นปริมาตร",
    ),
    44: (
        "acid-identity-from-molarity-density-mass-fraction",
        "chem.acid_identity_from_molarity_density_mass_fraction.procedure",
        "ความหนาแน่นกับร้อยละมวลให้มวลกรดต่อลิตร; หารด้วยโมลาริตีเพื่อหามวลโมลแล้วเทียบสูตรกรด",
        "คูณความหนาแน่นด้วย 1000 mL และเศษส่วนมวลกรดเพื่อหากรัมกรดต่อลิตร",
        "หารกรัมกรดด้วยโมลต่อลิตรและเปรียบเทียบมวลโมลของตัวเลือก",
    ),
    45: (
        "sodium-ion-after-mixing-sulfate-phosphate",
        "chem.sodium_ion_after_mixing_sulfate_phosphate.procedure",
        "Na₂SO₄ ให้ Na⁺ สองโมล และ Na₃PO₄ ให้ Na⁺ สามโมลต่อโมลเกลือ; ความเข้มข้นหลังผสมคือโมล Na⁺ รวมต่อปริมาตรรวม",
        "คำนวณโมล Na⁺ แยกจากเกลือซัลเฟตและฟอสเฟตตามสัมประสิทธิ์ในสูตร",
        "บวกโมล Na⁺ แล้วหารด้วยผลบวกปริมาตรสารละลาย",
    ),
    46: (
        "chlorine-hcl-solution-mass-yield",
        "chem.chlorine_hcl_solution_mass_yield.procedure",
        "MnO₂ หนึ่งโมลให้ Cl₂ หนึ่งโมลโดยใช้ HCl สี่โมล; มวลสารละลายกรดเท่ากับมวล HCl บริสุทธิ์หารด้วยเศษส่วนมวล",
        "ดุลสมการและแปลงมวล Cl₂ เป็นโมลเพื่อหามวล HCl ที่ทำปฏิกิริยา",
        "หารมวล HCl บริสุทธิ์ด้วยความเข้มข้นร้อยละโดยมวล",
    ),
    47: (
        "acetic-acid-left-after-bicarbonate",
        "chem.acetic_acid_left_after_bicarbonate.procedure",
        "กรดแอซีติกกับ NaHCO₃ ทำปฏิกิริยา 1:1; ความเข้มข้นกรดที่เหลือหาได้จากโมลเริ่มต้นลบโมลไบคาร์บอเนตแล้วหารด้วยปริมาตร",
        "ใช้ความหนาแน่นและร้อยละมวลหาโมลกรดแอซีติกในน้ำส้มสายชู",
        "หักโมล NaHCO₃ จากโมลกรดแล้วหารด้วยปริมาตรสารละลายที่กำหนดให้คงที่",
    ),
    48: (
        "hydroxide-target-barium-ppm-naoh-stock",
        "chem.hydroxide_target_barium_ppm_naoh_stock.procedure",
        "แปลง ppm โดยมวลของ Ba(OH)₂ เป็นโมล OH⁻ สองเท่า แล้วเติมโมล OH⁻ ที่ขาดด้วย NaOH ร้อยละมวลและความหนาแน่นที่กำหนด",
        "หามวลสารละลาย Ba(OH)₂ จากปริมาตรและความหนาแน่น แล้วแปลง ppm เป็นโมล OH⁻",
        "หัก OH⁻ เดิมจากเป้าหมายและแปลงโมล NaOH เป็นปริมาตรสารละลายสต็อก",
    ),
    49: (
        "benzene-boiling-elevation-molar-mass",
        "chem.benzene_boiling_elevation_molar_mass.procedure",
        "สารไม่ระเหยและไม่แตกตัวทำให้จุดเดือดเพิ่มตาม ΔTb=Kb·m; โมแลลิตีใช้กิโลกรัมของเบนซีนเป็นตัวหาร",
        "หารการเพิ่มจุดเดือดด้วย Kb เพื่อหาโมแลลิตีของ X",
        "คูณโมแลลิตีด้วยกิโลกรัมเบนซีนเพื่อหาโมล X แล้วหารมวล X ด้วยโมล",
    ),
    50: (
        "equal-molality-freezing-to-boiling-transfer",
        "chem.equal_molality_freezing_to_boiling_transfer.procedure",
        "ตัวละลายมวลเท่ากันและตัวทำละลายมวลเท่ากันให้โมแลลิตีเท่ากัน; ใช้ ΔTf(A)/Kf(A) หา m แล้วบวก Kb(B)·m ที่จุดเดือด B",
        "หาการลดจุดเยือกแข็งของ A จากผลต่างระหว่างตัวทำละลายบริสุทธิ์กับสารละลาย",
        "นำโมแลลิตีเดียวกันไปหาการเพิ่มจุดเดือดใน B",
    ),
    51: (
        "solute-mass-from-boiling-freezing-gap",
        "chem.solute_mass_from_boiling_freezing_gap.procedure",
        "ช่วงห่างจุดเดือดกับจุดเยือกแข็งของน้ำที่มีตัวละลายไม่แตกตัวเท่ากับ 100+(Kb+Kf)m; จาก m หาโมลและมวลตัวละลาย",
        "ลบช่วงห่าง 100°C ของน้ำบริสุทธิ์แล้วหารด้วย Kb+Kf เพื่อหาโมแลลิตี",
        "แปลงปริมาตรน้ำเป็นกิโลกรัมและคูณมวลโมลของ X",
    ),
    52: (
        "solid-crystal-bonding-types",
        "chem.solid_crystal_bonding_types.procedure",
        "แรงยึดเหนี่ยวในผลึกขึ้นกับชนิดอนุภาค: CO₂ ไม่มีขั้วจึงมีแรงลอนดอน, LiF เป็นไอออนิก, Kr มีแรงลอนดอน และ Au เป็นโลหะ",
        "จำแนกอนุภาคในผลึกแต่ละชนิด",
        "ตรวจว่าคำอธิบายแรงยึดเหนี่ยวตรงกับขั้วโมเลกุลและชนิดผลึกหรือไม่",
    ),
    53: (
        "covalent-network-melting-explanation",
        "chem.covalent_network_melting_explanation.procedure",
        "SiO₂ และโครงผลึกร่างตาข่ายอื่นมีพันธะโคเวเลนต์ต่อเนื่อง ไม่ใช่โมเลกุลแยกที่ยึดด้วยแรงระหว่างขั้ว",
        "จำแนกสารเป็นโลหะ โมเลกุล ไอออนิก หรือโครงผลึกร่างตาข่าย",
        "เทียบชนิดพันธะกับสมบัติและหาข้อความที่ให้เหตุผลผิด",
    ),
    54: (
        "vapor-pressure-boiling-force-ranking",
        "chem.vapor_pressure_boiling_force_ranking.procedure",
        "เมื่อเปรียบเทียบของเหลวที่อุณหภูมิเดียวกัน ความดันไอสูงหมายถึงระเหยง่ายและแรงยึดเหนี่ยวอ่อน จึงมีจุดเดือดต่ำกว่า",
        "เรียงความดันไอที่อุณหภูมิเดียวกัน",
        "กลับลำดับเพื่อเรียงจุดเดือด และใช้ลำดับเดิมหาแรงยึดเหนี่ยวอ่อนสุด",
    ),
    55: (
        "phase-from-melting-boiling-thresholds",
        "chem.phase_from_melting_boiling_thresholds.procedure",
        "ที่ความดันคงที่ สารเป็นของแข็งเมื่อ T ต่ำกว่าจุดหลอมเหลว เป็นของเหลวระหว่างจุดหลอมเหลวกับจุดเดือด และเป็นแก๊สเมื่อ T สูงกว่าจุดเดือด",
        "อ่านค่า T และจุดหลอมเหลวกับจุดเดือดของสารแต่ละตัว",
        "ตรวจเงื่อนไขสถานะทั้งสามตัวในแต่ละแถว",
    ),
    56: (
        "water-wetting-cohesion-adhesion",
        "chem.water_wetting_cohesion_adhesion.procedure",
        "พื้นผิวไม่ชอบน้ำอย่างใบบัวทำให้น้ำเป็นหยดกลม ในขณะที่กระดาษดูดน้ำและกระจกสะอาดเปียกน้ำ",
        "สังเกตว่าหยดน้ำแผ่ซึมหรือเป็นหยดกลมบนพื้นผิว",
        "เทียบการยึดเกาะของน้ำกับพื้นผิวกับการยึดกันเองของน้ำ",
    ),
    57: (
        "gas-mean-kinetic-energy-temperature",
        "chem.gas_mean_kinetic_energy_temperature.procedure",
        "พลังงานจลน์เฉลี่ยของการเคลื่อนที่ของอนุภาคแก๊สอุดมคติเท่ากับ 3kT/2 และขึ้นกับอุณหภูมิเคลวิน ไม่ขึ้นกับมวลหรือชนิดแก๊ส",
        "แยกข้อสมมติว่าปริมาตรอนุภาคน้อยจากการมีมวลเป็นศูนย์",
        "ใช้ T(K) ตรวจพลังงานจลน์เฉลี่ยและความดันเมื่อปริมาตรคงที่",
    ),
    58: (
        "gas-density-identity-and-diffusion",
        "chem.gas_density_identity_and_diffusion.procedure",
        "จาก d=PM/RT หา M ของแก๊ส แล้วใช้กฎของเกรแฮมว่าอัตราการแพร่แปรผกผันกับรากที่สองของมวลโมล",
        "คำนวณมวลโมลจากความหนาแน่น ความดัน และอุณหภูมิเคลวิน",
        "เทียบมวลโมลของสูตรผู้สมัคร แล้วเลือกแก๊สเบาสุดเป็นผู้แพร่เร็วสุด",
    ),
    59: (
        "boyle-old-new-volume-ratio",
        "chem.boyle_old_new_volume_ratio.procedure",
        "เมื่ออุณหภูมิและจำนวนโมลคงที่ P₁V₁=P₂V₂ จึงมี V₁/V₂=P₂/P₁; อัตราส่วนที่เขียนต่างรูปอาจเท่ากัน",
        "อ่านลำดับปริมาตรเดิมต่อใหม่แล้วกลับลำดับความดัน",
        "ลดเศษส่วนและเขียนตัวเลือกทั้งหมดในรูปฐานเดียวกันเพื่อตรวจคำตอบซ้ำ",
    ),
    60: (
        "rising-bubble-combined-gas-law",
        "chem.rising_bubble_combined_gas_law.procedure",
        "ฟองแก๊สจำนวนโมลคงที่ทำตาม P₁V₁/T₁=P₂V₂/T₂; ต้องแปลงอุณหภูมิเซลเซียสเป็นเคลวิน",
        "แปลง T ทั้งสองตำแหน่งด้วย T(K)=t(°C)+273",
        "จัดรูปหา V₂=V₁(P₁/P₂)(T₂/T₁)",
    ),
    61: (
        "zirconium-ground-state-subshells",
        "chem.zirconium_ground_state_subshells.procedure",
        "Zr มีเลขอะตอม 40 จัดอิเล็กตรอนสถานะพื้นเป็น [Kr]4d²5s²; การเขียนแกนแก๊สมีตระกูลเทียบเท่าการขยายออร์บิทัลชั้นในทั้งหมด",
        "เริ่มจากแกน [Kr] ที่มี 36 อิเล็กตรอน",
        "กระจายสี่อิเล็กตรอนที่เหลือใน 5s² และ 4d² แล้วตรวจผลรวมเป็น 40",
    ),
    62: (
        "outer-configuration-atomic-size-and-formula",
        "chem.outer_configuration_atomic_size_and_formula.procedure",
        "เมื่อ n=3, A=Na, D=Fe, E=Ca และ G=Cl; G เล็กสุด และไอออน E²⁺ กับ G⁻ ให้สูตร EG₂",
        "แปลงรูปการจัดอิเล็กตรอนชั้นนอกเป็นคาบและหมู่",
        "เทียบขนาดอะตอมและดุลประจุไอออนเพื่อเขียนสูตรอย่างง่าย",
    ),
    63: (
        "bromochloromethane-isotopologue-fraction",
        "chem.bromochloromethane_isotopologue_fraction.procedure",
        "มวลโมเลกุล CH₂BrCl เท่ากับ 128 เมื่อใช้ ⁷⁹Br และ ³⁵Cl; ร้อยละไอโซโทโปล็อกเท่ากับผลคูณของความน่าจะเป็นสองไอโซโทป",
        "แจกแจงมวลจาก C,H และไอโซโทป Cl,Br ที่เป็นไปได้",
        "เลือกคู่ที่รวมเป็น 128 แล้วคูณสัดส่วนไอโซโทปก่อนแปลงเป็นร้อยละ",
    ),
    64: (
        "consecutive-chromium-manganese-iron",
        "chem.consecutive_chromium_manganese_iron.procedure",
        "เลขอะตอม Cr,Mn,Fe เท่ากับ 24,25,26; Cr มีออกไซด์ +6 เป็น CrO₃ และ Mn สถานะพื้น [Ar]3d⁵4s²",
        "ระบุ Fe จากฮีมแล้วถอยหา Mn และ Cr",
        "ดุล Cr(+6) กับ O(−2) และนับอิเล็กตรอนของ Mn",
    ),
    65: (
        "einsteinium-synthesis-neutrons-half-life",
        "chem.einsteinium_synthesis_neutrons_half_life.procedure",
        "อนุรักษ์เลขมวลและเลขอะตอมในปฏิกิริยา ²³⁸U+¹⁴N→²⁴⁸Es+4n; มวลที่เหลือเท่ากับมวลเริ่มต้นคูณ (1/2) ยกกำลังจำนวนครึ่งชีวิต",
        "ลบเลขมวลผลิตภัณฑ์จากเลขมวลสารตั้งต้นเพื่อหานิวตรอน",
        "หารเวลาเก็บด้วย 25 นาทีแล้วคำนวณมวลที่เหลือ",
    ),
    66: (
        "born-haber-first-ionization-energy",
        "chem.born_haber_first_ionization_energy.procedure",
        "ผลรวมขั้นในวัฏจักรบอร์น–ฮาเบอร์เท่ากับเอนทัลปีเกิด MX โดยใช้ครึ่งหนึ่งของพลังงานสลาย X₂ และใส่เครื่องหมายพลังงานรับอิเล็กตรอนกับเกิดผลึกตามที่กำหนด",
        "รวมการระเหิดโลหะและครึ่งหนึ่งของการสลาย X₂",
        "จัดสมการ ΔHf=ΔHsub+½D+IE+EA+ΔHlattice เพื่อหา IE",
    ),
    67: (
        "carbonyl-dihalide-lewis-and-polarity",
        "chem.carbonyl_dihalide_lewis_and_polarity.procedure",
        "C ที่ผูกกับธาตุหมู่ 16 หนึ่งตัวและฮาโลเจนสองตัวมีโครง Y–C(=X)–Y; X มีคู่โดดเดี่ยวสองคู่ Y แต่ละตัวสามคู่ และโมเลกุลมีขั้ว",
        "ใช้เวเลนซ์ C=4, X=6, Y=7 เพื่อดุลจำนวนพันธะและเขียนสูตร CXY₂",
        "วาดพันธะคู่ C=X กับพันธะเดี่ยว C–Y สองเส้น แล้วระบุแรงระหว่างขั้ว",
    ),
    68: (
        "aluminum-per-pancake-nested-mass-fractions",
        "chem.aluminum_per_pancake_nested_mass_fractions.procedure",
        "มวล Al ต่อชิ้นเท่ากับมวลแป้งคูณเศษส่วนสารเติมแต่งคูณเศษส่วน Al₂O₃ คูณ 54/102 แล้วหารจำนวนชิ้น",
        "คำนวณมวลสารเติมแต่งและ Al₂O₃ จากร้อยละมวลซ้อน",
        "แปลง Al₂O₃ เป็น Al และหารจำนวนแพนเค้กก่อนแปลงเป็นมิลลิกรัม",
    ),
    69: (
        "phosphate-silver-back-titration-p2o5",
        "chem.phosphate_silver_back_titration_p2o5.procedure",
        "SCN⁻ วัด Ag⁺ เหลือแบบ 1:1; Ag₃PO₄ ใช้ Ag⁺ สามโมลต่อฟอสเฟต และ P₂O₅ หนึ่งโมลให้ฟอสเฟตสองโมล จึงใช้ Ag⁺ หกโมลต่อ P₂O₅",
        "หาโมล Ag⁺ เริ่มต้นและที่เหลือจากการไทเทรต SCN⁻",
        "หัก Ag⁺ เหลือ แปลง Ag⁺ ที่ใช้เป็น P₂O₅ และหารมวลตัวอย่างเพื่อหาร้อยละ",
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
