"""Idempotent complete coverage for two Primary 4 comprehension papers."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-4/4537-4-2565-1-2.pdf'
B='mathematics/level/primary-4/4543-4-2567-2-2.pdf'


def u(key,statement,a,b,covered):
    return dict(id='math.primary4.'+key,kind='procedure',title=statement,statement=statement,
                steps=['อ่านข้อมูล ชื่อจุด หน่วย และคำสั่ง',statement,'ตรวจทุกตัวเลือกกับข้อมูลที่กำหนด'],
                sources=[{'sheet':p,'item':n} for p,items in ((A,a),(B,b)) for n in items],
                covered_by=['math.'+k for k in covered])


def main():
    files={
        ('place-value','ค่าประจำหลัก'):[
            u('million-number-forms','อ่านค่าตามหลักแล้วเชื่อมคำอ่าน ตัวเลขไทย และตัวเลขฮินดูอารบิกถึงหลักสิบล้าน',[1,2],[1,2],['number_reading_p4']),
            u('canonical-million-expansion','เขียนแต่ละพจน์เป็นค่าเลขโดดหลักเดียวและละพจน์ศูนย์ เพื่อแยกรูปกระจายออกจากผลบวกที่เพียงมีค่าเท่ากัน',[3],[3],['canonical_expansion_millions_p4']),
            u('large-number-threshold','เปรียบเทียบจำนวนตามค่าประจำหลักจากซ้ายไปขวาแล้วเลือกค่าที่อยู่ด้านของขอบเขตตามเครื่องหมาย',[4],[4],['compare_large_numbers_p4','number_between_p4']),
        ],
        ('estimation','การประมาณค่า'):[
            u('rounding-statement','ระบุหลักที่จะปัด ตรวจหลักถัดไป แล้วตรวจจำนวนประมาณทั้งค่าและจำนวนศูนย์',[5],[5],['rounding_statement_p4','rounding']),
        ],
        ('addition-subtraction','การบวกและการลบ'):[
            u('large-addsub-sentence','เลือกการรวม การหาส่วนที่ขาดหรือส่วนต่าง และการหาคงเหลือตามความหมายของเรื่องจำนวนมาก',[6,7,8],[6,7],['large_addsub_sentence_p4']),
        ],
        ('multi-step','โจทย์ปัญหาระคน'):[
            u('discount-fee-sentence','หักส่วนลดออกจากราคาเดิมก่อนรวมค่าธรรมเนียมที่ต้องจ่ายเพิ่ม โดยคงเครื่องหมายแต่ละส่วน',[],[8],['discount_fee_sentence_p4']),
        ],
        ('multiplication','การคูณยาว'):[
            u('product-model-statement','ใช้จำนวนกลุ่มคูณปริมาณต่อกลุ่มแล้วตรวจทั้งเครื่องหมายและผลลัพธ์ ไม่เลือกเพียงสมการที่เป็นจริง',[9,10],[9,10],['product_model_statement_p4']),
        ],
        ('lines-angles','เส้นตรงและมุม'):[
            u('line-notation','แยกขีดบน ลูกศรหนึ่งหัว และสองหัวตามส่วนของเส้นตรง รังสี และเส้นตรง พร้อมรักษาจุดเริ่มของรังสี',[11],[11],['line_notation_p4','line_ray_picture_p4']),
            u('plane-surface-model','แยกผิวหน้าแบนที่ใช้เป็นแบบจำลองส่วนของระนาบออกจากผิวทรงกลมตามแบบจำลองเรขาคณิต',[12],[12],['plane_surface_model_p4']),
            u('angle-parts-names','หาจุดยอดร่วมของแขนมุม อ่านชื่อมุมโดยให้จุดยอดอยู่กลาง และแยกจุดยอดออกจากชื่อมุมทั้งมุม',[13,14,15],[13,14,15],['name_angle_p4']),
            u('angle-less-right','ใช้เก้าสิบองศาเป็นเกณฑ์เพื่อจำแนกมุมแหลมออกจากมุมฉาก ป้าน ตรง และกลับ',[16],[16],['classify_angle','angle_kind_picture_p4']),
        ],
        ('rectangles','สี่เหลี่ยมมุมฉาก'):[
            u('rectangle-properties','ตรวจด้าน มุม และเส้นทแยงมุมโดยแยกสมบัติทั่วไปของผืนผ้าออกจากสมบัติของจัตุรัส และระบุเพียงหนึ่งคู่ให้ชัด',[17],[17],['rectangle_property_statement_p4']),
            u('rectangle-opposite-side','ใช้ด้านตรงข้ามยาวเท่ากันเพื่อหาด้านที่ถามเมื่อกำกับจุดเรียงรอบรูป',[18],[],['rectangle_missing_side_p4','construct_rectangle_p4']),
            u('square-summary','ใช้ด้านเท่ากันสี่ด้าน มุมฉากสี่มุม พื้นที่ด้านคูณด้าน และเส้นรอบรูปสี่เท่าของด้านตรวจทุกข้อความ',[],[18],['square_summary_statement_p4']),
        ],
        ('bar-charts','แผนภูมิแท่ง'):[
            u('bar-total','อ่านค่าทุกแท่งตามสเกลแล้วรวม โดยแยกยอดเหตุการณ์รายวันออกจากจำนวนบุคคลไม่ซ้ำ',[19],[],['bar_total_p4']),
            u('three-series-summary','ใช้คำอธิบายชุดข้อมูลและเดือนตรวจค่าสูงสุด ต่ำสุด ความเท่ากัน และการเปรียบเทียบข้ามเดือน',[],[19],['three_series_chart_summary_p4']),
        ],
        ('data-presentation','การนำเสนอข้อมูล'):[
            u('supplied-table-maximum','อ่านทุกค่าจากตารางที่ให้แล้วหาชื่อรายการที่มากที่สุด โดยถือเป็นข้อมูลในโจทย์เท่านั้น',[20],[],['two_way_table_read_p5','bar_chart_compare_p4']),
            u('selected-categories-row-max','รวมเฉพาะสองประเภทที่เข้าเงื่อนไขในแต่ละแถว ไม่รวมประเภทตามเกณฑ์ แล้วเปรียบเทียบผลรวมทุกแถว',[],[20],['selected_columns_row_max_p4']),
        ],
    }
    claims=[(s['sheet'],s['item']) for units in files.values() for unit in units for s in unit['sources']]
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(p,n) for p in (A,B) for n in range(1,21)}
    for (slug,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/primary4-{slug}.json',topic,units,'ป.4')


if __name__=='__main__':
    main()
