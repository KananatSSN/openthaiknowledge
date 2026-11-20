"""Idempotent complete coverage for a Secondary 3 inequalities/quadratics paper."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
SOURCE='mathematics/level/secondary-3/5196-3-2564-1.pdf'
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']


def u(key,statement,numbers,covered):
    return dict(id='math.secondary3.'+key,kind='procedure',title=statement,statement=statement,
                steps=['ระบุเงื่อนไขและโดเมนของจำนวน',statement,'แทนคำตอบกลับและตรวจทุกตัวเลือก'],
                sources=[{'sheet':SOURCE,'item':n} for n in numbers],covered_by=['math.'+k for k in covered])


def main():
    files={
        ('inequalities','อสมการเชิงเส้น'):[
            u('numberline-ray','อ่านจุดทึบหรือโปร่งและทิศรังสีบนเส้นจำนวนเป็นขอบเขตอสมการ',[1],['inequality_representation_m3']),
            u('verbal-inequality-grouping','แปลวงเล็บ การหาร และคำไม่เกินหรือไม่น้อยกว่าเป็นข้อความโดยรักษาลำดับดำเนินการ',[2],['inequality_representation_m3']),
            u('expand-solve-inequality','กระจายวงเล็บ รวมตัวแปรทั้งสองข้าง แล้วกลับเครื่องหมายเมื่อหารด้วยจำนวนลบ',[3,4,5,6],['inequality','inequality_negative_coefficient','inequality_both_sides_m3']),
            u('fraction-both-sides-inequality','คูณตัวส่วนบวกร่วมแล้วรวบรวมพจน์เพื่อหาเซตคำตอบอสมการ',[7,8,9],['inequality_fraction_m3','inequality_both_sides_m3']),
            u('compound-negative-inequality','แยกอสมการประกอบ แก้แต่ละด้านโดยกลับเครื่องหมายเมื่อหารด้วยลบ แล้วหาส่วนร่วม',[10],['inequality_compound','inequality_negative_coefficient']),
            u('strict-integer-stock','ตั้งอสมการจากสิ่งของคงเหลือแล้วใช้เงื่อนไขจำนวนเต็มและขอบเขตเข้ม',[11],['inequality_largest_integer_m3','inequality_word_problem_m3']),
            u('age-linear-constraints','เขียนอายุสัมพันธ์และอายุรวมตามเวลาแล้วหาเขตคำตอบที่แน่นที่สุด ก่อนใช้โดเมนอายุที่กำหนด',[12,15],['age_constraint_m3']),
            u('positive-integer-shortfall','เขียนเงื่อนไขส่วนขาดบวกและน้อยกว่าจำนวนที่กำหนด แล้วหาจำนวนเต็มบวกที่เป็นไปได้',[13],['inequality_count_integers_m3']),
            u('rectangle-area-lower-bound','แปลงขอบเขตเส้นรอบรูปเป็นขอบเขตความกว้าง แล้วใช้พื้นที่เพิ่มตามความกว้างบวก',[14],['rectangle_area_bound_m3']),
        ],
        ('factorising','แยกตัวประกอบ'):[
            u('cube-identity-substitution','ระบุพจน์กำลังสามรวมทั้งพจน์เลื่อน แล้วใช้สูตรผลบวกหรือผลต่างกำลังสามพร้อมตรวจด้วยการกระจาย',[16,17,19,20],['factor_cube_identity_m3']),
            u('common-fourth-difference','ดึงตัวร่วมแล้วแยกผลต่างกำลังสี่เป็นผลต่างกำลังสองสองชั้น',[18],['factor_fourth_power_m3']),
        ],
        ('quadratic-equations','สมการกำลังสอง'):[
            u('quadratic-standard-form','ย้ายข้างและรวมพจน์เพื่อจำแนกดีกรีสองและอ่านสัมประสิทธิ์โดยระบุการปรับสเกลชัดเจน',[21,22,24],['quadratic_standard_form_m3']),
            u('verify-root-pair','แทนตัวเลือกทุกค่าในพหุนามเพื่อระบุคู่รากของสมการ',[23],['which_root_m3','quadratic_equation']),
            u('solve-factor-quadratic','แยกตัวประกอบและใช้ผลคูณศูนย์เพื่อหารากทั้งหมดรวมกรณีรากซ้ำ',[25,26,27,29,30],['quadratic_equation','quadratic_formula_roots']),
            u('root-relations','จัดสมการให้อยู่ในรูปกำลังสองแล้วใช้ผลคูณรากหรือแทนหนึ่งรากเพื่อหาผลบวกราก',[28,39],['quadratic_root_relation_m3']),
            u('irrational-quadratic-roots','ใช้สูตรกำลังสองและคงรากที่สองอย่างแน่นอนเพื่อหารากจริงที่ไม่เป็นตรรกยะ',[31,32],['quadratic_equation']),
            u('consecutive-positive-product','ตั้งสมการผลคูณของจำนวนเต็มบวกเรียงติดกันและตัดรากที่ผิดโดเมน',[33],['consecutive_product_m3']),
            u('quadratic-number-relations','ใช้ผลต่างที่กำหนดแทนจำนวนหนึ่งในอีกจำนวนแล้วสร้างสมการจากผลบวกกำลังสองหรือผลคูณสัมพันธ์ผลบวก',[34,38],['quadratic_number_relation_m3']),
            u('quadratic-geometric-dimension','เขียนพื้นที่ด้วยมิติสัมพันธ์ แก้สมการกำลังสอง แล้วเลือกมิติที่เป็นบวก',[35,36],['quadratic_dimension_m3']),
            u('squared-past-age','แทนอายุปัจจุบันในอายุอนาคตและกำลังสองอายุอดีต แล้วตัดคำตอบที่ทำให้อายุอดีตติดลบ',[37],['quadratic_past_age_m3']),
            u('perpendicular-travel-difference','ใช้ผลต่างระยะทางกับพีทาโกรัสสร้างสมการกำลังสองและเลือกความยาวบวก',[40],['perpendicular_travel_m3']),
        ],
    }
    claims=[source['item'] for units in files.values() for unit in units for source in unit['sources']]
    assert len(claims)==len(set(claims))==40 and set(claims)==set(range(1,41))
    for (slug,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/secondary3-{slug}.json',topic,units,'ม.3')


if __name__=='__main__':
    main()
