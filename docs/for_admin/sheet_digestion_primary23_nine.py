"""Idempotent preserving coverage map for Primary 2/3 measurement papers."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCES={2:'mathematics/level/primary-2/4152-2-2564-2-2.pdf',3:'mathematics/level/primary-3/4354-3-2565-1-3.pdf'}


def u(grade,key,statement,numbers,covered):
    return dict(id=f'math.primary{grade}.'+key,kind='procedure',title=statement,statement=statement,
                steps=['อ่านข้อมูลและหน่วยที่กำหนด',statement,'ตรวจทุกตัวเลือกและหน่วยของคำตอบ'],
                sources=[{'sheet':SOURCES[grade],'item':n} for n in numbers],covered_by=['math.'+k for k in covered])


def main():
    files={
        ('primary2-measurement','ป.2','การวัด'):[
            u(2,'ruler-endpoints','อ่านขีดตรงปลายสองข้างบนไม้บรรทัดแล้วหาผลต่างเป็นความยาว',[1,2],['ruler_picture_p1']),
            u(2,'cm-compound-metres','หารเซนติเมตรด้วยร้อยเพื่อเขียนเมตรและเศษเซนติเมตร',[3,8],['cm_to_m_cm_p2','convert_length_p2']),
            u(2,'diagram-direct-length','อ่านด้านที่เชื่อมจุดสองจุดที่ถามโดยไม่เลือกเส้นทแยงมุมหรือด้านอื่น',[4],['length_word_problem_p2']),
            u(2,'height-difference-reading','อ่านความสูงจากแกนที่กำหนดแล้วหาส่วนต่าง',[5],['ruler_picture_p1','length_compare_mixed_p2']),
            u(2,'length-relational-statements','แปลงเป็นเซนติเมตรก่อนเปรียบเทียบทิศทางและความเท่ากัน',[6,7,10],['mixed_length_statement_p2']),
            u(2,'round-trip-metres','รวมระยะไปและกลับบนทางเดิมโดยคงหน่วยเมตร',[9],['round_trip_metres_p2']),
            u(2,'volume-statement-truth','เปรียบเทียบปริมาตรด้วยหน่วยหรือภาชนะตวงชนิดขนาดเดียวกันโดยไม่เปรียบเทียบมวล',[11],['volume_comparison_statement_p2']),
            u(2,'container-equivalence','ใช้ความจุที่กำหนดเทียบเท่าจากภาพเพื่อเปรียบเทียบภาชนะหลายใบ',[12],['container_equivalence_p2']),
            u(2,'dry-measure-tool','เลือกภาชนะสำหรับตวงของแห้งตามข้อตกลงของกิจกรรมโดยไม่สมมติความจุที่ไม่ได้ให้',[13],['measuring_tool_p3']),
            u(2,'conventional-container-order','แยกคำตอบตามบริบทภาชนะทั่วไปออกจากการเปรียบเทียบที่มีค่าความจุกำหนด',[14],['capacity_litre_p2']),
            u(2,'dry-measure-method','เลือกการปาดเสมอขอบหรือพูนให้ตรงชนิดของแห้งตามข้อตกลงที่ระบุ',[15],['dry_measure_method_p2']),
        ],
        ('primary2-pictographs','ป.2','แผนภูมิรูปภาพ'):[
            u(2,'chart-value-lookup','คูณจำนวนรูปด้วยค่าประจำรูปเพื่อหาชื่อรายการที่มีค่าตามที่ถาม',[16],['pictograph_matching_rows_p2']),
            u(2,'chart-two-row-operations','อ่านจำนวนสองแถว คูณค่าประจำรูป แล้วรวมหรือหาผลต่างตามคำถาม',[17,18],['pictograph_compare_p2']),
            u(2,'chart-pair-target','หาคู่รายการที่มีจำนวนรวมเท่ากับเป้าหมายโดยตรวจคู่ตัวเลือกทั้งหมด',[19],['pictograph_pair_target_p2']),
            u(2,'chart-extreme-and-value','เปรียบเทียบจำนวนทุกแถวแล้วระบุชื่อรายการมากหรือน้อยที่สุดพร้อมจำนวนจริง',[20],['pictograph_extreme_amount_p2']),
        ],
        ('primary3-addition-subtraction','ป.3','การบวกและการลบ'):[
            u(3,'add-large-stories','รวมจำนวนตามหน่วยเดียวกันโดยแยกกระแสรายรับออกจากยอดสะสมต่างเวลา',[1,2,3,4],['addsub_word_large_p3']),
            u(3,'large-comparison-amount','ใช้จำนวนที่ทราบกับส่วนต่างเพื่อย้อนหาจำนวนที่มากกว่าหรือน้อยกว่าไม่เกินหนึ่งแสน',[5],['comparison_amount_large_p3']),
            u(3,'subtract-large-stories','ลบส่วนที่ใช้หรือส่วนที่ทราบออกจากจำนวนทั้งหมดเพื่อหาคงเหลือ',[6,7,8,9,10],['addsub_word_large_p3']),
            u(3,'large-sequential-expenses','หักค่าใช้จ่ายสองรายการจากเงินเริ่มต้นและตรวจย้อนด้วยผลรวม',[11],['money_left_two_buys_p3','add_sub_large_p3']),
            u(3,'large-sequential-stock','เขียนยอดตั้งต้นบวกของเข้าและลบของออกโดยคงหน่วยและลำดับเหตุการณ์',[12,13,15],['addsub_word_large_p3']),
            u(3,'three-large-revenues','รวมรายรับที่ไม่ทับซ้อนกันสามครั้งเมื่อมีจำนวนห้าหลัก',[14],['three_revenues_large_p3']),
        ],
        ('primary3-measurement','ป.3','การวัด'):[
            u(3,'mixed-length-result','แปลงเป็นหน่วยย่อยก่อนบวกหรือลบแล้วหารกลับเป็นหน่วยผสมโดยทดหรือยืมถูกต้อง',[16,17,18,19,20],['mixed_length_result_p3']),
        ],
    }
    claims=[(source['sheet'],source['item']) for units in files.values() for unit in units for source in unit['sources']]
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(p,n) for p in SOURCES.values() for n in range(1,21)}
    for (slug,level,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/{slug}.json',topic,units,level)


if __name__=='__main__':
    main()
