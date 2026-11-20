"""Complete preserving claims for two Primary 6 model papers."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-6/4898-6-2565-1-2.pdf'
B='mathematics/level/primary-6/4901-6-2565-1-2.pdf'


def main():
    files,claims={},[]
    def add(grade,slug,topic,key,sheet,numbers,covered=(),statement=None):
        path=ROOT/f'otk/knowledge/math/primary{grade}-{slug}.json'
        if path not in files:
            raw=json.loads(path.read_text()) if path.exists() else {'units':[]}
            files[path]=(raw.get('topic',topic),raw['units'],raw.get('level',f'ป.{grade}'))
        units=files[path][1]
        uid=f'math.primary{grade}.{key}'
        target=next((u for u in units if u['id']==uid),None)
        if target is None:
            assert statement,uid
            target=dict(id=uid,kind='procedure',title=statement,statement=statement,
                        steps=['อ่านข้อมูลและเงื่อนไขที่กำหนด',statement,'ตรวจทุกตัวเลือกและหน่วย'],sources=[],covered_by=[])
            units.append(target)
        for n in numbers:
            source={'sheet':sheet,'item':n}
            claims.append((sheet,n))
            if source not in target['sources']:
                target['sources'].append(source)
        for k in covered:
            if 'math.'+k not in target['covered_by']:
                target['covered_by'].append('math.'+k)

    add(5,'fraction-expression-models','เศษส่วน','fraction-mixed-statement',A,[1,2,3,4])
    add(6,'fractions-mixed-models','เศษส่วนและจำนวนคละ','mixed-order',A,[5,6,8],['order_mixed_numbers_p6'],
        'เปลี่ยนเศษส่วนและจำนวนคละเป็นค่าเดียวกันแล้วตรวจลำดับทุกคู่ตามทิศที่ถาม')
    add(6,'fractions-mixed-models','เศษส่วนและจำนวนคละ','fraction-order-statement',A,[7],['fraction_order_statement_p6'],
        'ตรวจแต่ละแถวแยกกันเมื่อแต่ละตัวเลือกอาจมีจำนวนต่างชุดกัน และต้องเรียงถูกตลอดทุกคู่')
    add(6,'fractions-mixed-models','เศษส่วนและจำนวนคละ','mixed-remaining-model',A,[9,11],['mixed_remaining_model_p6'],
        'รวมส่วนที่ใช้ไปหรือส่วนที่มีแล้วทั้งสองก่อนหักจากยอดทั้งหมดหรือยอดที่ต้องการ โดยรักษาข้อมูลจำนวนคละทุกตัว')
    add(5,'fraction-story-models','โจทย์ปัญหาเศษส่วน','fraction-story-sentence',A,[10,13,14])
    add(6,'fractions-mixed-models','เศษส่วนและจำนวนคละ','two-fraction-purchases-model',A,[12],['two_fraction_purchases_model_p6'],
        'คูณน้ำหนักเศษส่วนหรือจำนวนคละของสินค้าแต่ละชนิดด้วยราคาต่อกิโลกรัมของชนิดนั้น แล้วรวมราคาทั้งสอง')
    add(6,'decimals','ทศนิยม','ribbon-sale-model',A,[15],['ribbon_sale_model_p6'],
        'จับหน่วยราคาต่อเส้นกับจำนวนเส้น หรือต่อเมตรกับความยาวรวม ไม่ใช้ความยาวต่อเส้นแทนยอดขายรวม')
    add(6,'decimals','ทศนิยม','decimal-bag-count',A,[16],['decimal_bag_count_p6','decimal_operation_model_p6'],
        'หารน้ำหนักรวมด้วยความจุต่อถุง แล้วแยกผลหารเชิงจำนวนออกจากจำนวนถุงเต็มหรือจำนวนถุงที่ใช้บรรจุหมดตามข้อกำหนด')
    add(6,'decimals','ทศนิยม','decimal-division-story',A,[17],['decimal_division_story_p6'],
        'เลือกเรื่องราวที่ถามค่าต่อคนหรือต่อชิ้นจากยอดรวมทศนิยมหารจำนวนส่วนเท่ากัน โดยรักษาบทบาทของตัวตั้งและตัวหาร')
    add(6,'decimals','ทศนิยม','decimal-operation-model',A,[18,19,20],['decimal_operation_model_p6'],
        'เลือกบวกหาผลรวม ลบหาผลต่าง คูณหาค่ารวมจากอัตรา หรือหารหาค่าต่อหน่วยตามบทบาทข้อมูลทศนิยม')

    add(6,'gcd-and-lcm','ห.ร.ม. และ ค.ร.น.','factor-product-gcd',B,[1,2])
    add(6,'gcd-and-lcm','ห.ร.ม. และ ค.ร.น.','factor-product-lcm',B,[3,4])
    add(2,'patterns','แบบรูป','changing-attribute',B,[5])
    add(6,'patterns','แบบรูป','square-grid-perimeter',B,[6],['square_grid_perimeter_p6'],
        'หาจำนวนแผ่นต่อด้านตามลำดับรูปแล้วนับเฉพาะขอบภายนอกของตารางจัตุรัส ไม่ใช้พื้นที่หรือรวมขอบแผ่นด้านใน')
    add(6,'patterns','แบบรูป','constant-difference',B,[7])
    add(6,'solids','รูปเรขาคณิต 3 มิติ','pyramid-lateral',B,[8,10])
    add(6,'solids','รูปเรขาคณิต 3 มิติ','solid-apex-feature',B,[9],['solid_from_description_p6','pyramid_counts_p6'],
        'แยกยอดแหลมตามความหมายแบบเรียนออกจากจุดยอดของทรงหลายหน้า แล้วจำแนกปริซึม กรวย และพีระมิด')
    add(6,'solids','รูปเรขาคณิต 3 มิติ','net-solid',B,[11,12,13,14,15])
    add(6,'volume-and-surface-area','ปริมาตรและพื้นที่ผิว','multiple-cube-volume',B,[16],['multiple_cube_volume_p6'],
        'คูณสันสามครั้งหาปริมาตรลูกบาศก์หนึ่งกล่อง แล้วคูณจำนวนกล่องขนาดเท่ากัน')
    add(6,'volume-and-surface-area','ปริมาตรและพื้นที่ผิว','cuboid-capacity-extreme',B,[17],['cuboid_capacity_extreme_p6'],
        'คูณมิติภายในทั้งสามของแต่ละภาชนะในหน่วยเดียวกัน รวมทศนิยมครึ่งหน่วย แล้วเปรียบเทียบความจุครบทุกใบ')
    add(6,'volume-and-surface-area','ปริมาตรและพื้นที่ผิว','mixed-volume-model',B,[18],['box_volume_sentence_p6','mixed_box_cost_sentence_p6'],
        'แปลงเซนติเมตรเป็นเมตรทุกมิติก่อนคูณหาปริมาตรลูกบาศก์เมตร ไม่แปลงเฉพาะบางด้าน')
    add(6,'volume-and-surface-area','ปริมาตรและพื้นที่ผิว','inverse-box-model',B,[19])
    add(6,'volume-and-surface-area','ปริมาตรและพื้นที่ผิว','mixed-volume-cost',B,[20])
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(p,n) for p in (A,B) for n in range(1,21)}
    for path,(topic,units,level) in files.items():
        write_topic(path,topic,units,level)


if __name__=='__main__':
    main()
