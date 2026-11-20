"""Idempotent procedure coverage for the Secondary3 5198 text-layer paper."""
from pathlib import Path
import json
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCE='mathematics/level/secondary-3/5198-3-2565-2.pdf'


def main():
    files,claims={},[]
    def add(slug,topic,key,numbers,covered=(),statement=None):
        path=ROOT/f'otk/knowledge/math/secondary3-{slug}.json'
        if path not in files:
            raw=json.loads(path.read_text()) if path.exists() else {'units':[]}
            files[path]=(raw.get('topic',topic),raw['units'],raw.get('level','ม.3'))
        units=files[path][1];uid='math.secondary3.'+key
        unit=next((u for u in units if u['id']==uid),None)
        if unit is None:
            assert statement,uid
            unit=dict(id=uid,kind='procedure',title=statement,statement=statement,
                      steps=['ระบุข้อมูลและเงื่อนไขที่จำเป็น',statement,'ตรวจหน่วย สมมติฐาน และทุกตัวเลือก'],sources=[],covered_by=[])
            units.append(unit)
        for n in numbers:
            source={'sheet':SOURCE,'item':n};claims.append(n)
            if source not in unit['sources']:unit['sources'].append(source)
        for key in covered:
            if 'math.'+key not in unit['covered_by']:unit['covered_by'].append('math.'+key)

    add('systems','ระบบสมการ','system-solution-count',[1,2,7,8])
    add('systems','ระบบสมการ','exact-linear-system',[3,4,5,9])
    add('systems','ระบบสมการ','system-sum',[6])
    add('systems','ระบบสมการ','system-parameter-difference',[10],['system_parameter_difference_m3'],
        'แทนคู่อันดับที่ทราบลงในสมการทั้งสองเพื่อหาสัมประสิทธิ์ไม่ทราบค่า แล้วคำนวณผลต่างที่ถาม')
    add('systems','ระบบสมการ','past-ratio-age-sum',[11],['system_ages_m3','system_setup_m3'],
        'กำหนดอายุปัจจุบัน ใช้อายุย้อนหลังทั้งสองคนในอัตราส่วน แล้วใช้ผลรวมอายุแก้ระบบ')
    add('systems','ระบบสมการ','two-item-prices',[12],['system_two_prices_m3'],
        'ตั้งสมการราคาจากการซื้อสองชุดแล้วแก้หาราคาต่อชิ้นของแต่ละชนิด')
    add('systems','ระบบสมการ','mixture-mass-ratio',[13],['mixture_mass_ratio_m3'],
        'รักษามวลและมูลค่ารวมของส่วนผสม เพื่อหาอัตราส่วนมวลชนิดราคาต่ำต่อชนิดราคาสูงที่ให้ราคาเฉลี่ยตามกำหนด')
    add('systems','ระบบสมการ','joint-worker-time',[14],['joint_worker_time_m3'],
        'ใช้ส่วนของงานต่อวันตั้งระบบจากทีมสองแบบ แก้อัตรางานรายคนแล้วกลับเศษส่วนเป็นเวลา โดยไม่ปัดเป็นวันเต็มเอง')
    add('systems','ระบบสมการ','reversed-digit-system',[15],['reversed_digit_system_m3'],
        'เขียนจำนวนเดิมและจำนวนสลับหลักจากเลขหลักสิบหน่วย ใช้ผลรวมเลขโดดและผลต่างของจำนวนแก้ระบบ')
    add('circle-theorems','วงกลม','circle-tangent-chord-facts',[16,17,19,20])
    add('circle-theorems','วงกลม','radius-chord-equilateral',[18],['triangle_facts_p6','circle_parts'],
        'เมื่อคอร์ดยาวเท่ารัศมี สามด้านของสามเหลี่ยมที่เชื่อมศูนย์กลางกับปลายคอร์ดเท่ากัน จึงใช้มุมสามเหลี่ยมด้านเท่า')
    add('circle-theorems','วงกลม','circle-triangle-angle-chain',[21,22,25],['circle_angle_picture_m3','angles_same_arc_m3','isosceles_base_angle_p6','triangle_missing_angle'],
        'เชื่อมมุมในส่วนโค้งกับสามเหลี่ยมหน้าจั่วจากรัศมี เส้นผ่านศูนย์กลาง และผลรวมมุม โดยอ่านจุดยอดมุมที่ถามให้ถูก')
    add('circle-theorems','วงกลม','central-to-inscribed',[23,24])
    add('solid-inverses','พื้นที่ผิวและปริมาตร','cone-total-area',[26,29])
    add('solid-inverses','พื้นที่ผิวและปริมาตร','pyramid-surface-from-height',[27],['pyramid_surface_from_height_m3'],
        'หาสูงเอียงของหน้าพีระมิดตรงจากสูงตั้งฉากกับครึ่งด้านฐาน แล้วรวมพื้นที่หน้าทั้งสี่กับฐาน')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','sphere-surface',[28])
    add('solid-inverses','พื้นที่ผิวและปริมาตร','pyramid-roof-tile-count',[30],['pyramid_roof_tile_count_m3'],
        'ตรวจว่ามิติพีระมิดเป็นไปได้ รวมพื้นที่สามเหลี่ยมหลังคาทุกหน้า หารพื้นที่ต่อแผ่นแล้วปัดขึ้นภายใต้กฎคิดจากพื้นที่อย่างเดียว')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','sphere-area-from-volume',[31],['sphere_area_from_volume_m3'],
        'ย้อนสูตรปริมาตรทรงกลมหารัศมีด้วยรากที่สาม แล้วคำนวณพื้นที่ผิวด้วยค่าพายที่กำหนด')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','hemisphere-on-cone-area',[32],['hemisphere_on_cone_area_m3'],
        'ใช้พีทาโกรัสหารัศมีจากสูงเอียงและสูงกรวยที่มีฐานร่วม แล้วหาผิวโค้งครึ่งทรงกลมโดยไม่รวมฐานที่ซ่อน')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','sphere-volume-from-circumference',[33],['sphere_volume_from_circumference_m3'],
        'ต้องทราบว่าเป็นวงใหญ่ผ่านศูนย์กลาง ย้อนเส้นรอบวงหารัศมีแล้วคำนวณปริมาตร โดยไม่ปัดรัศมีก่อนกำลังสาม')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','cone-radius-height-volume',[34],['cone_volume'],
        'หารเส้นผ่านศูนย์กลางด้วยสองแล้วใช้หนึ่งในสามพายรัศมีกำลังสองคูณสูงตั้งฉาก')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','rectangular-pyramid-volume',[35])
    add('solid-inverses','พื้นที่ผิวและปริมาตร','cone-cup-count',[36],['cone_cup_count_m3'],
        'แปลงลิตรเป็นลูกบาศก์เซนติเมตร หารด้วยปริมาตรกรวยต่อถ้วย แล้วแยกเต็มถ้วยกับบรรจุหมดโดยถ้วยสุดท้ายไม่เต็ม')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','pyramid-cast-mass',[37],['pyramid_cast_mass_m3'],
        'หาปริมาตรพีระมิดหนึ่งอัน คูณจำนวนอันและมวลต่อหน่วยปริมาตร แล้วแปลงกรัมเป็นกิโลกรัม')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','cylinder-sphere-recast-count',[38],['cylinder_volume_m3','sphere_volume','solid_word_problem_m3'],
        'ภายใต้การหลอมไม่สูญเสียเนื้อวัสดุ หารปริมาตรทรงกระบอกเดิมด้วยปริมาตรทรงกลมหนึ่งลูกเพื่อหาจำนวนลูก')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','pyramid-recipe-litres',[39],['pyramid_volume_m3','part_of_part_p6','volume_capacity_p5'],
        'รวมปริมาตรขนมพีระมิดทุกชิ้น คูณสัดส่วนวัตถุดิบโดยปริมาตร แล้วแปลงลูกบาศก์เซนติเมตรเป็นลิตร')
    add('solid-inverses','พื้นที่ผิวและปริมาตร','hemisphere-sphere-recast-radius',[40],['hemisphere_volume_m3','sphere_area_from_volume_m3','solid_word_problem_m3'],
        'รวมปริมาตรครึ่งทรงกลมทุกชิ้นเป็นปริมาตรทรงกลมใหม่ แล้วจัดสูตรและถอดรากที่สามหารัศมีภายใต้การอนุรักษ์ปริมาตร')
    assert len(claims)==len(set(claims))==40 and set(claims)==set(range(1,41))
    for path,(topic,units,level) in files.items():write_topic(path,topic,units,level)


if __name__=='__main__':
    main()
