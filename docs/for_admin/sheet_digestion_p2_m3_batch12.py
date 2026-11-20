"""Preserve prior claims while mapping two complete Primary 2 / Secondary 3 papers."""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
P2 = 'mathematics/level/primary-2/4176-2-2567-2-2.pdf'
M3 = 'mathematics/level/secondary-3/5202-3-2567-2.pdf'


def u(grade, key, title, statement, numbers, covered):
    source = P2 if grade == 'primary2' else M3
    return dict(id=f'math.{grade}.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุข้อมูลและสิ่งที่โจทย์ถาม', statement, 'ตรวจคำตอบและเงื่อนไขของโจทย์'],
                sources=[{'sheet': source, 'item': n} for n in numbers],
                covered_by=['math.' + k for k in covered])


def main():
    files = {
        ('primary2-measurement', 'ป.2', 'การวัด'): [
            u('primary2','convert-length','เปลี่ยนเมตรและเซนติเมตรเป็นเซนติเมตร','คูณจำนวนเมตรด้วยหนึ่งร้อยแล้วบวกจำนวนเซนติเมตร',[1,6],['convert_length_p2']),
            u('primary2','mixed-length-statement','เลือกข้อความเปรียบเทียบความยาวต่างหน่วย','เปลี่ยนความยาวเป็นหน่วยเดียวกัน หาผลต่าง แล้วระบุทิศทางยาวกว่าสั้นกว่าให้ถูกต้อง',[2,4,7,10],['mixed_length_statement_p2']),
            u('primary2','repeated-length','รวมความยาวชิ้นที่เท่ากันและเขียนสองหน่วย','คูณความยาวต่อชิ้นด้วยจำนวนชิ้น แล้วเปลี่ยนเซนติเมตรเป็นเมตรและเซนติเมตร',[3],['length_word_problem_p2','cm_to_m_cm_p2']),
            u('primary2','length-cut','หาความยาวหลังตัดส่วนหนึ่งออก','เปลี่ยนเป็นหน่วยเดียวกันก่อนลบส่วนที่ตัดจากความยาวทั้งหมด',[5],['length_word_problem_p2']),
            u('primary2','out-and-back-length','หาระยะทางไปและกลับ','ระยะทางไปและกลับรวมสองเที่ยว คูณความยาวหนึ่งเที่ยวด้วยสอง',[8],['length_word_problem_p2','daily_total_weeks_p2']),
            u('primary2','mixed-length-difference','หาผลต่างความยาวแล้วเขียนสองหน่วย','หาผลต่างหลังแปลงเป็นเซนติเมตร แล้วแบ่งหนึ่งร้อยเซนติเมตรเป็นหนึ่งเมตร',[9],['length_compare_mixed_p2','cm_to_m_cm_p2']),
            u('primary2','capacity-tool','เลือกหน่วยและภาชนะตวงตามขนาด','เลือกหน่วยและเครื่องตวงให้เหมาะกับปริมาณและลักษณะของสิ่งที่ตวง โดยไม่สับสนเครื่องมือกับหน่วย',[11,12],['kitchen_measures_p3','capacity_unit_p3']),
            u('primary2','capacity-difference','หาผลต่างความจุหน่วยเดียวกัน','ลบความจุน้อยจากความจุมากแล้วแปลเป็นข้อความเปรียบเทียบ',[13],['capacity_litre_p2']),
            u('primary2','capacity-unit-picture','นับหน่วยตวงจากภาพ','เมื่อปริมาณในเหยือกเท่ากับแก้วขนาดเดียวกันที่แสดง ให้นับจำนวนแก้วครบทุกใบ',[14],['count_objects_p1','capacity_litre_p2']),
            u('primary2','capacity-litre-ml-comparison','เปรียบเทียบลิตรกับมิลลิลิตร','เปลี่ยนลิตรเป็นมิลลิลิตรด้วยอัตราหนึ่งพันก่อนเลือกมากกว่าน้อยกว่าหรือเท่ากับ',[15],['capacity_litre_ml_comparison_p2']),
        ],
        ('secondary3-systems','ม.3','ระบบสมการ'): [
            u('secondary3','graph-system-solution','อ่านคำตอบระบบสมการจากกราฟ','คำตอบร่วมคือจุดตัดของเส้นตรง อ่านพิกัดหรือใช้สมการตรวจจุดตัดและจำนวนคำตอบ',[1,2],['simultaneous_2var','system_solution_count_m3']),
            u('secondary3','exact-linear-system','แก้ระบบสมการโดยคงค่าแน่นอน','จัดรูปและกำจัดตัวแปร โดยเคลียร์ตัวส่วนและทศนิยมก่อนคำนวณเมื่อจำเป็น แล้วตรวจแทนกลับทั้งสองสมการ',[3,4,5,6,7],['simultaneous_2var','system_substitution','system_which_pair_m3']),
            u('secondary3','system-solution-count','จำแนกจำนวนคำตอบจากความสัมพันธ์สมการ','ตรวจว่าสองเส้นตัดกัน ขนานกัน หรือเป็นเส้นเดียวกัน โดยเทียบอันดับเมทริกซ์หรืออัตราส่วนสัมประสิทธิ์และค่าคงตัว',[8,10],['system_solution_count_m3']),
            u('secondary3','system-sum','หาผลรวมของพิกัดคำตอบ','แก้ระบบสมการหรือรวมสมการให้ได้ผลรวมที่ต้องการ แล้วแทนกลับตรวจคำตอบ',[9],['system_x_plus_y_m3']),
            u('secondary3','number-story-system','ตั้งระบบสมการจากความสัมพันธ์จำนวนสองจำนวน','กำหนดตัวแปรแทนจำนวนน้อยและจำนวนมาก แปลผลบวกและพหุคูณตามเรื่อง แล้วคำนวณนิพจน์ที่ถาม',[11,13],['system_setup_m3','system_word_problem','system_sum_difference_m3']),
            u('secondary3','basket-target','ใช้ระบบสมการคิดราคาตะกร้าใหม่','หาราคาต่อหน่วยจากการซื้อสองแบบที่เป็นอิสระกัน แล้วคูณจำนวนสินค้าของตะกร้าใหม่',[12],['system_basket_target_m3']),
            u('secondary3','two-rate-allocation','แบ่งเงินตามผลตอบแทนสองอัตรา','ใช้สมการเงินรวมและสมการผลตอบแทนรวมจากสองอัตราเพื่อหาเงินลงทุนแต่ละส่วน',[14],['two_rate_allocation_m3']),
            u('secondary3','rectangle-perimeter-gap-area','หาพื้นที่สี่เหลี่ยมจากเส้นรอบรูปและผลต่างด้าน','ใช้ผลบวกและผลต่างของความยาวด้านหาด้านทั้งสอง แล้วคูณเพื่อหาพื้นที่',[15],['rectangle_equation_m1','rectangle_area_perimeter']),
        ],
        ('secondary3-circle-theorems','ม.3','วงกลม'): [
            u('secondary3','circle-tangent-chord-facts','ใช้เงื่อนไขทฤษฎีรัศมี คอร์ด และเส้นสัมผัส','ตรวจสมมติฐานให้ครบก่อนใช้การตั้งฉากของรัศมีกับเส้นสัมผัสและเส้นแบ่งครึ่งคอร์ด อย่าสรุปจำนวนจุดตัดจากรัศมีอย่างเดียว',[16,17],['tangent_length_m3','chord_from_distance_m3','perpendicular_bisector_m2']),
            u('secondary3','named-circle-theorem','แยกชื่อทฤษฎีมุมที่จุดศูนย์กลางกับมุมในส่วนโค้ง','มุมที่จุดศูนย์กลางเป็นสองเท่าของมุมในส่วนโค้งเดียวกัน และมุมในส่วนโค้งเท่ากันรองรับส่วนโค้งเท่ากัน โดยระบุทฤษฎีที่โจทย์ถามให้ตรง',[18,20],['inscribed_from_central_m3','angles_same_arc_m3']),
            u('secondary3','tangent-chord-angles','ใช้มุมระหว่างเส้นสัมผัสกับคอร์ด','มุมเส้นสัมผัสกับคอร์ดเท่ากับมุมในส่วนโค้งตรงข้าม ใช้ร่วมกับมุมเส้นตรงและผลรวมมุมสามเหลี่ยมเมื่อจำเป็น',[19,21,25],['tangent_chord_angle_m3','triangle_angle_algebra_m2']),
            u('secondary3','central-to-inscribed','เปลี่ยนมุมที่จุดศูนย์กลางเป็นมุมในส่วนโค้ง','มุมในส่วนโค้งที่รองรับด้วยส่วนโค้งเดียวกันมีขนาดครึ่งหนึ่งของมุมที่จุดศูนย์กลาง',[22],['inscribed_from_central_m3']),
            u('secondary3','equal-chords-arcs','เชื่อมคอร์ดยาวเท่ากันกับส่วนโค้งและมุม','คอร์ดเท่ากันรองรับส่วนโค้งเท่ากัน แล้วใช้มุมในส่วนโค้งร่วมกับส่วนโค้งรอบวงรวมสามร้อยหกสิบองศา',[23],['angles_same_arc_m3','central_inscribed_angle']),
            u('secondary3','semicircle-angle','ใช้มุมในครึ่งวงกลมหามุมสามเหลี่ยม','มุมที่รองรับเส้นผ่านศูนย์กลางเป็นมุมฉาก แล้วใช้ผลรวมมุมสามเหลี่ยมหามุมที่เหลือ',[24],['inscribed_angle_semicircle']),
        ],
        ('secondary3-solid-inverses','ม.3','พื้นที่ผิวและปริมาตร'): [
            u('secondary3','pyramid-lateral-area','รวมพื้นที่หน้าด้านข้างพีระมิด','หาพื้นที่สามเหลี่ยมหน้าด้านข้างแล้วรวมทุกหน้า โดยระบุสมมติฐานฐานและความเท่ากันของหน้าตามรูปให้ครบ',[26],['pyramid_surface_from_edge_m3']),
            u('secondary3','cone-total-area','หาพื้นที่ผิวรวมกรวย','รวมพื้นที่ฐานวงกลมกับพื้นที่ผิวข้าง และใช้พีทาโกรัสหาสูงเอียงเมื่อให้ความสูงตั้งฉาก',[27,32],['cone_sphere_surface_area_m3','cone_curved_from_height_m3']),
            u('secondary3','sphere-surface','หาพื้นที่ผิวทรงกลมและรวมหลายลูก','เปลี่ยนเส้นผ่านศูนย์กลางเป็นรัศมีก่อนใช้สี่พายอาร์กำลังสอง แล้วรวมทุกลูกและระบุค่าพายที่ใช้',[28,31],['cone_sphere_surface_area_m3']),
            u('secondary3','pyramid-surface-from-edge','หาพื้นที่ผิวพีระมิดจากสันถึงจุดยอดฐาน','ใช้พีทาโกรัสในหน้าสามเหลี่ยมหาสูงเอียงจากสันและครึ่งด้านฐาน รวมพื้นที่หน้าด้านข้างและฐานตามที่โจทย์ถาม',[29,30],['pyramid_surface_from_edge_m3']),
            u('secondary3','hemisphere-litres','แปลงปริมาตรครึ่งทรงกลมเป็นลิตร','ใช้รัศมีคำนวณสองในสามพายอาร์กำลังสาม แล้วเปลี่ยนลูกบาศก์เซนติเมตรเป็นลิตรและปัดตามโจทย์',[33],['hemisphere_volume_m3','volume_capacity_p5']),
            u('secondary3','rectangular-pyramid-volume','หาปริมาตรพีระมิดฐานสี่เหลี่ยมผืนผ้า','คูณพื้นที่ฐานกับความสูงตั้งฉาก แล้วหารสาม',[34],['pyramid_volume_m3','rectangle_area_perimeter']),
            u('secondary3','cone-from-base-area','หาปริมาตรกรวยจากพื้นที่ฐานโดยตรง','คูณพื้นที่ฐานที่กำหนดกับความสูงตั้งฉากแล้วหารสาม ไม่ต้องหารัศมีซ้ำ',[35],['cone_volume']),
            u('secondary3','cone-volume-from-slant','หาปริมาตรกรวยจากสูงเอียง','หารเส้นผ่านศูนย์กลางด้วยสอง หาความสูงตั้งฉากด้วยพีทาโกรัส แล้วคำนวณปริมาตรกรวย',[36],['cone_volume_from_slant_m3']),
            u('secondary3','hemisphere-from-sphere-area','หาความจุครึ่งทรงกลมจากพื้นที่ผิวเดิม','ใช้พื้นที่ผิวทรงกลมหารัศมี แล้วคำนวณปริมาตรครึ่งทรงกลมพร้อมค่าพายและการปัดเศษที่กำหนด',[37],['hemisphere_from_sphere_area_m3']),
            u('secondary3','hemisphere-radius','หารัศมีจากปริมาตรครึ่งทรงกลม','จัดสูตรให้ได้รัศมียกกำลังสาม แล้วหารากที่สามบวก',[38],['hemisphere_radius_from_volume_m3']),
            u('secondary3','square-pyramid-slant-volume','หาปริมาตรพีระมิดสี่เหลี่ยมจากสูงเอียง','ใช้สูงเอียงกับครึ่งด้านฐานหาความสูงตั้งฉาก แล้วคูณพื้นที่ฐานและหารสาม',[39],['square_pyramid_volume_from_slant_m3']),
            u('secondary3','equilateral-pyramid-base','หาด้านฐานสามเหลี่ยมด้านเท่าจากปริมาตร','ย้อนจากปริมาตรและความสูงเพื่อหาพื้นที่ฐาน ใช้สูตรพื้นที่สามเหลี่ยมด้านเท่าแล้วถอดรากบวก',[40],['equilateral_pyramid_base_from_volume_m3']),
        ],
    }
    path = ROOT / 'otk/knowledge/math/primary2-pictograph.json'
    old = json.loads(path.read_text())['units']
    additions = {'pictograph-maximum':[16], 'pictograph-difference':[19]}
    claims=[]
    for key,numbers in additions.items():
        target=next(item for item in old if item['id']=='math.primary2.'+key)
        for n in numbers:
            source={'sheet':P2,'item':n}
            if source not in target['sources']:
                target['sources'].append(source)
            claims.append((P2,n))
    chart = [
        u('primary2','pictograph-read','อ่านจำนวนจริงจากแผนภูมิรูปภาพ','นับจำนวนรูปแล้วคูณค่าของรูปตามคำอธิบาย',[17],['pictograph']),
        u('primary2','pictograph-truth','ตรวจข้อความจากแผนภูมิรูปภาพ','แปลงจำนวนรูปเป็นค่าจริงก่อนตรวจความเท่ากันและการเปรียบเทียบทุกข้อความ',[18],['pictograph_true_statement_p2']),
        u('primary2','pictograph-minimum-value','หาค่าของรายการที่น้อยที่สุด','เปรียบเทียบทุกแถวเพื่อหารายการน้อยที่สุด แล้วคูณจำนวนรูปกับค่าต่อรูป',[20],['pictograph_order_p2','pictograph']),
    ]
    claims += [(s['sheet'],s['item']) for units in files.values() for item in units for s in item['sources']]
    claims += [(s['sheet'],s['item']) for item in chart for s in item['sources']]
    assert len(claims)==len(set(claims))==60
    assert set(claims)=={(P2,n) for n in range(1,21)}|{(M3,n) for n in range(1,41)}
    write_topic(path,'แผนภูมิรูปภาพ',old+chart,'ป.2')
    for (slug,level,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/{slug}.json',topic,units,level)


if __name__=='__main__':
    main()
