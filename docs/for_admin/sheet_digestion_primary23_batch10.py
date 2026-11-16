"""Preserving map for complete Primary 2 arithmetic and Primary 3 measurement papers."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCES={2:'mathematics/level/primary-2/4180-2-2567-2-1.pdf',3:'mathematics/level/primary-3/4352-3-2565-1-2.pdf'}


def u(grade,key,title,statement,numbers,covered):
    return dict(id=f'math.primary{grade}.'+key,kind='procedure',title=title,statement=statement,
                steps=['ระบุข้อมูลและสิ่งที่ถาม',statement,'ตรวจความสัมพันธ์และหน่วยของคำตอบ'],
                sources=[{'sheet':SOURCES[grade],'item':n} for n in numbers],
                covered_by=['math.'+k for k in covered])


def main():
    files={
        ('primary2-addition-subtraction','ป.2','การบวกและการลบ'):[
            u(2,'add-three-digits','บวกจำนวนสามหลักตามค่าประจำหลัก','บวกหน่วย สิบ ร้อยตามหลักและทดเมื่อครบสิบ โดยคงค่าหลักที่มีศูนย์',[1,2,3,6,7,8],['add_columns']),
            u(2,'missing-add-sub','หาจำนวนที่ขาดในประโยคบวกลบ','ใช้การดำเนินการย้อนกลับตามตำแหน่งตัวไม่ทราบค่า แล้วแทนกลับตรวจทั้งประโยค',[4,14,19],['missing_addsub_p2']),
            u(2,'match-three-digit-sum','เลือกนิพจน์สามหลักที่มีผลบวกตามเป้าหมาย','คำนวณผลบวกแต่ละตัวเลือกโดยรวมค่าหลักและการทด แล้วเทียบกับเป้าหมาย',[5,9],['match_three_digit_sum_p2']),
            u(2,'balance-three-digit-sums','รักษาผลบวกสองข้างให้เท่ากัน','รวมค่าของด้านที่ทราบ แล้วลบพจน์ที่ทราบของอีกข้างเพื่อหาพจน์ที่ขาด',[10],['balance_three_digit_sums_p2']),
            u(2,'subtract-three-digits','ลบจำนวนสามหลักและกระจายหลักเมื่อจำเป็น','ลบตามหลักจากหน่วยไปหาร้อย กระจายหนึ่งหน่วยจากหลักที่สูงกว่าเมื่อค่าหลักนั้นไม่พอ',[11,12,13,16,17,18],['sub_columns']),
            u(2,'match-three-digit-difference','เลือกนิพจน์สามหลักที่มีผลลบตามเป้าหมาย','หาผลต่างของแต่ละคู่แล้วเปรียบเทียบกับจำนวนเป้าหมาย โดยระวังหลักสิบและหลักร้อย',[15],['match_three_digit_difference_p2']),
            u(2,'balance-three-digit-differences','รักษาผลลบสองข้างให้เท่ากัน','หาผลต่างด้านที่ทราบแล้วลบผลต่างนี้จากตัวตั้งอีกด้านเพื่อหาตัวลบที่ขาด',[20],['balance_three_digit_differences_p2']),
        ],
        ('primary3-one-way-tables','ป.3','ตารางทางเดียว'):[
            u(3,'pictograph-context-and-key','อ่านหัวเรื่องและค่าประจำรูปของแผนภูมิ','อ่านหัวเรื่องเพื่อระบุสิ่งที่นับ อ่านรายการและค่าของหนึ่งรูปก่อนหาจำนวนหรือผลต่าง โดยไม่สับสนจำนวนสัตว์กับจำนวนคนที่ชอบสัตว์',[1,2,3],['pictograph','pictograph_compare_p2']),
            u(3,'raw-data-to-table','นับข้อมูลรายคนหรือรูปแล้วสร้างตารางทางเดียว','นับแต่ละประเภทแยกกันจากข้อมูลเดิม ตรวจผลรวมและทุกรายการของตารางตัวเลือก',[4,5],['tally_to_table_p3']),
        ],
        ('primary3-time','ป.3','เวลา'):[
            u(3,'activity-time-lookup','อ่านเวลาเริ่มกิจกรรมจากบันทึก','หารายการกิจกรรมที่ถามในบันทึก แล้วอ่านเวลาแถวเดียวกันโดยคงชั่วโมงและนาที',[6,7,8],['activity_time_lookup_p3']),
        ],
        ('primary3-measurement','ป.3','การวัด'):[
            u(3,'scale-reading','อ่านน้ำหนักจากหน้าปัดเครื่องชั่ง','อ่านหน่วยและค่าช่วงย่อยของหน้าปัดก่อนเปลี่ยนกิโลกรัมเป็นขีด โดยไม่เปลี่ยนจำนวนวัตถุให้เป็นน้ำหนักต่อชิ้น',[9],['scale_picture_p2','scale_kg_khit_p1']),
            u(3,'weight-instrument','เลือกเครื่องชั่งตามลักษณะงาน','แยกเครื่องชั่งน้ำหนักออกจากเครื่องมือชนิดอื่น และเลือกแบบรองรับสิ่งของตามบริบท โดยไม่สมมติพิกัดน้ำหนักที่โจทย์ไม่ได้ให้',[10],['measuring_tool_p3']),
            u(3,'normalize-and-add-weight','แปลงกิโลกรัมขีดกรัมก่อนรวม','ใช้หนึ่งกิโลกรัมเป็นหนึ่งพันกรัมและหนึ่งขีดเป็นหนึ่งร้อยกรัม แล้วรวมเมื่อโจทย์ถามน้ำหนักทั้งหมด',[11,13],['convert_weight_p3','weight_word_problem_p3','weight_comparison_statement_p3']),
            u(3,'weight-comparison-statement','เปรียบเทียบน้ำหนักต่างหน่วยเป็นข้อความ','เปลี่ยนเป็นกรัม หาผลต่าง และระบุว่าสิ่งใดหนักกว่าสิ่งใดตามข้อมูลจริง',[12],['weight_comparison_statement_p3']),
            u(3,'weight-estimation-error','หาความคลาดเคลื่อนของน้ำหนักที่คาดคะเน','เปลี่ยนน้ำหนักคาดคะเนและน้ำหนักจริงเป็นหน่วยเดียวกัน หาผลต่างบวกแล้วเขียนหน่วยตามที่ถาม',[14,15],['weight_estimation_error_p3']),
        ],
        ('primary3-volume-capacity','ป.3','ปริมาตรและความจุ'):[
            u(3,'litres-to-ml','แปลงลิตรเป็นมิลลิลิตร','คูณจำนวนลิตรด้วยหนึ่งพันเพื่อเขียนปริมาตรเดิมเป็นมิลลิลิตร',[16],['convert_volume_p3']),
            u(3,'share-decimal-litres','แบ่งปริมาตรลิตรทศนิยมแล้วตอบมิลลิลิตร','เปลี่ยนลิตรทศนิยมเป็นมิลลิลิตรก่อนหารจำนวนแก้วที่แบ่งเท่ากัน',[17],['share_decimal_litres_p3']),
            u(3,'dry-volume-measure','เลือกภาชนะตวงของแห้งตามขนาด','เลือกภาชนะตวงตามลักษณะและขนาดของสิ่งที่ตวง โดยแยกหน่วยปริมาตรออกจากเครื่องตวง',[18],['capacity_unit_p3','kitchen_measures_p3','measuring_tool_p3']),
            u(3,'capacity-comparison-statement','เปรียบเทียบความจุทศนิยมและส่วนต่าง','เปลี่ยนเป็นหน่วยเดียวกัน หาผลต่างอย่างแน่นอน แล้วระบุภาชนะที่จุมากกว่าและส่วนต่างให้ถูก',[19],['capacity_comparison_statement_p3']),
            u(3,'capacity-estimation-error','หาความคลาดเคลื่อนความจุเป็นมิลลิลิตร','หาผลต่างบวกระหว่างความจุที่คาดคะเนกับที่ตวงจริง แล้วเปลี่ยนลิตรเป็นมิลลิลิตรโดยไม่ปัดทศนิยม',[20],['capacity_estimation_error_p3']),
        ],
    }
    claims=[(source['sheet'],source['item']) for units in files.values() for unit in units for source in unit['sources']]
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(source,n) for source in SOURCES.values() for n in range(1,21)}
    for (slug,level,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/{slug}.json',topic,units,level)


if __name__=='__main__':
    main()
