"""Idempotent complete coverage for Primary 5 decimal/fraction model papers."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-5/4723-5-2567-2-1.pdf'
B='mathematics/level/primary-5/4725-5-2567-2-2.pdf'


def u(key,statement,sheet,numbers,covered):
    return dict(id='math.primary5.'+key,kind='procedure',title=statement,statement=statement,
                steps=['ระบุข้อมูล หน่วย และสิ่งที่ถาม',statement,'ตรวจทุกตัวเลือกด้วยค่าที่แน่นอน'],
                sources=[{'sheet':sheet,'item':n} for n in numbers],covered_by=['math.'+k for k in covered])


def main():
    files={
        ('decimal-arithmetic','ทศนิยม'):[
            u('three-place-addsub','ตั้งจุดทศนิยมตรงกัน เติมศูนย์ให้จำนวนตำแหน่งเท่ากัน แล้วบวกหรือลบตามค่าประจำหลัก',A,[1,2,3,4],['decimal_three_place_addsub_p5']),
            u('decimal-product','คูณจำนวนเต็มที่ได้จากการเลื่อนจุดแล้วคืนจำนวนตำแหน่งทศนิยมรวม',A,[5,6],['decimal_multiply_p5']),
            u('decimal-power-ten','เลื่อนค่าประจำหลักตามการคูณด้วยหนึ่งพันโดยรักษาค่าของเลขโดด',A,[7],['decimal_times_power_of_ten']),
            u('decimal-division','หารทศนิยมด้วยจำนวนนับและตรวจด้วยผลหารคูณตัวหาร โดยรักษาศูนย์ในผลหาร',A,[8,9,10],['decimal_divide_p5']),
            u('decimal-bracket-calculation','คำนวณตามวงเล็บและลำดับการดำเนินการสองขั้น โดยคงค่าทศนิยมแน่นอนระหว่างคำนวณ',A,list(range(11,19)),['decimal_bracket_calculation_p5']),
            u('decimal-round-final-expression','คำนวณนิพจน์ด้วยค่าแน่นอนแล้วปัดเฉพาะผลสุดท้ายตามจำนวนตำแหน่งที่ระบุ โดยหลักถัดไปห้าขึ้นไปปัดขึ้น',A,[19,20],['decimal_round_expression_p5']),
        ],
        ('fraction-expression-models','เศษส่วน'):[
            u('fraction-mixed-statement','เปลี่ยนจำนวนคละเป็นเศษเกินหรือใช้ผลคูณไขว้เพื่อตรวจข้อความเปรียบเทียบทุกข้อ',B,[1],['fraction_comparison_statement_p5']),
            u('fraction-expression-extreme','คำนวณผลลบจำนวนคละแต่ละนิพจน์เป็นเศษส่วนแน่นอนก่อนเปรียบเทียบมากหรือน้อยที่สุด',B,[2],['fraction_expression_extreme_p5']),
        ],
        ('fraction-story-models','โจทย์ปัญหาเศษส่วน'):[
            u('fraction-story-sentence','เลือกการบวก ลบ คูณ หรือหารจากความหมายส่วนของทั้งหมด การรวม การแบ่งเท่ากัน และความสัมพันธ์น้อยกว่า',B,[3,4,5,6],['fraction_story_sentence_p5']),
            u('fraction-discount-sentence','หาส่วนลดด้วยราคาเต็มคูณหนึ่งลบเศษส่วนของราคาขาย โดยไม่สับสนราคาขายกับส่วนลด',B,[7],['fraction_discount_sentence_p5']),
        ],
        ('length-weight-models','ความยาวและน้ำหนัก'):[
            u('decimal-length-conversion','เปลี่ยนความยาวทศนิยมระหว่างหน่วยโดยใช้ตัวคูณตามมาตรเมตริก',B,[8],['length_decimal_p5','decimal_to_smaller_unit_p5']),
            u('length-equivalence-statement','แปลงความยาวสองข้างของข้อความเป็นหน่วยเดียวกันก่อนตรวจความเท่ากัน',B,[9],['length_equivalence_statement_p5']),
            u('odd-length-equivalence','แปลงความยาวทั้งสี่ตัวเลือกเป็นหน่วยเดียวกันเพื่อหาค่าที่ต่างจากอีกสามค่า',B,[10],['odd_length_equivalence_p5']),
            u('length-rate-sentence','เปลี่ยนกิโลเมตรเป็นเมตรก่อนหารด้วยอัตราเร็วเมตรต่อนาทีเพื่อเลือกรูปคำนวณเวลา',B,[11],['length_rate_sentence_p5']),
            u('decimal-weight-conversion','เปลี่ยนกิโลกรัมทศนิยมเป็นกรัมด้วยหนึ่งพันกรัมต่อกิโลกรัม',B,[12],['weight_decimal_p5']),
            u('khit-cost-sentence','เปลี่ยนกิโลกรัมเป็นขีดด้วยสิบขีดต่อกิโลกรัมแล้วคูณราคาต่อขีด',B,[13],['khit_cost_sentence_p5']),
        ],
        ('parallel-reading','เส้นขนาน'):[
            u('rectangle-perpendicular-sides','ใช้มุมฉากระหว่างด้านประชิดของสี่เหลี่ยมผืนผ้า โดยไม่ถือว่าเส้นทแยงมุมตั้งฉากทั่วไป',B,[14],['construct_rectangle_p4','parallel_concepts_p5']),
            u('parallel-shape-segments','ตรวจคู่ส่วนของเส้นตรงที่มีทิศทางเดียวกันและระยะห่างคงที่ในรูปที่กำหนด',B,[15],['parallel_concepts_p5']),
            u('parallel-grid-construction','เลือกเส้นผ่านจุดที่กำหนดซึ่งรักษาทิศทางของเส้นอ้างอิงบนตาราง โดยตรวจเกณฑ์ความขนาน',B,[16],['parallel_concepts_p5','is_parallel_check_p5']),
            u('transversal-exterior-positions','จำแนกมุมภายนอกจากตำแหน่งนอกบริเวณระหว่างสองเส้น โดยไม่ต้องสมมติว่าเส้นทั้งสองขนาน',B,[17],['parallel_pair_picture_p5']),
            u('alternate-interior-positions','ระบุมุมแย้งภายในจากตำแหน่งคนละข้างของเส้นตัด โดยแยกการตั้งชื่อมุมออกจากเงื่อนไขขนาดเท่ากัน',B,[18],['parallel_pair_picture_p5']),
            u('parallel-angle-supplement','ใช้มุมตรงข้าม มุมสมนัยหรือมุมแย้งร่วมกับมุมเสริมเพื่อหาขนาดมุมเมื่อกำหนดเส้นขนาน',B,[19],['parallel_angle_picture_p5','parallel_angles']),
            u('parallel-angle-identity','ตรวจว่าความสัมพันธ์มุมเป็นสมบัติที่ใช้ได้ทั่วไปของเส้นขนานหรือเป็นเพียงกรณีมุมฉากพิเศษ',B,[20],['parallel_concepts_p5','parallel_angle_picture_p5','vertical_angle_p5']),
        ],
    }
    claims=[(s['sheet'],s['item']) for units in files.values() for unit in units for s in unit['sources']]
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(sheet,n) for sheet in (A,B) for n in range(1,21)}
    for (slug,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/primary5-{slug}.json',topic,units,'ป.5')


if __name__=='__main__':
    main()
