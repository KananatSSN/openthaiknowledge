"""Append all twenty items of the Primary 1 measurement comprehension paper."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
HELPERS = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))
unit, write_topic = HELPERS['unit'], HELPERS['write_topic']
SOURCE = 'mathematics/level/primary-1/4018-1-2567-2-2.pdf'


def u(key, title, statement, numbers, covered):
    return unit(key, title, statement, [(SOURCE, numbers)], covered)


def main():
    files = {
        'measurement': ('การวัด', [
            u('count-length-units', 'นับหน่วยที่วางเทียบความยาว',
              'นับหน่วยที่มีขนาดเท่ากันซึ่งวางต่อกันตั้งแต่ต้นจนถึงปลายของสิ่งที่วัด โดยไม่เว้นช่องหรือซ้อนทับ',
              [1, 2], ['count_objects_p1', 'count_objects_20_p1', 'count_units_nonstandard']),
            u('order-measured-lengths', 'เรียงลำดับความยาวจากภาพ',
              'พิจารณาจุดเริ่มต้นร่วมกันแล้วเปรียบเทียบปลายของสิ่งของ เรียงตามทิศทางที่โจทย์กำหนด',
              [3, 4], ['order_numbers', 'length_comparison_statement_p1']),
            u('measuring-tool', 'เลือกเครื่องมือให้เหมาะกับงานวัด',
              'เลือกเครื่องมือที่วัดปริมาณถูกชนิด มีความยาวพอ และมีความแข็งหรือโค้งงอเหมาะกับสิ่งที่วัด',
              [5, 6], ['measuring_tool_p1']),
            u('read-scale-kg-khit', 'อ่านหน้าปัดเครื่องชั่งเป็นกิโลกรัมและขีด',
              'ระบุเลขกิโลกรัมก่อนตำแหน่งเข็ม แล้วนับช่วงย่อยโดยสิบขีดเท่ากับหนึ่งกิโลกรัม',
              [7, 12], ['scale_picture_p2', 'scale_kg_khit_p1']),
            u('balance-unit-weight', 'อ่านน้ำหนักจากหน่วยบนตาชั่งสมดุล',
              'เมื่อตาชั่งสมดุล น้ำหนักของวัตถุเท่ากับจำนวนหน่วยน้ำหนักที่เท่ากันบนอีกข้าง',
              [8], ['count_objects_p1', 'compare_nonstandard_weight']),
            u('balance-weight-comparison', 'เปรียบเทียบน้ำหนักจากตาชั่ง',
              'ข้างที่ต่ำกว่าหนักกว่า หรือถ้าตาชั่งสมดุลให้นับหน่วยน้ำหนักของแต่ละวัตถุแล้วเปรียบเทียบ',
              [9, 10], ['compare_nonstandard_weight', 'weight_compare_kg_p1']),
            u('weight-pair-gap', 'เปรียบเทียบผลต่างน้ำหนักต่างหน่วย',
              'แปลงกิโลกรัมและขีดให้เป็นหน่วยเดียวกันก่อนหาผลต่างของแต่ละคู่ แล้วเลือกคู่ที่มีผลต่างมากที่สุด',
              [11], ['weight_difference_pairs_p1']),
        ]),
        'comparing-numbers': ('การเปรียบเทียบ', [
            u('ordering', 'ตรวจลำดับและหาจำนวนระหว่างกลาง',
              'เรียงจำนวนตามทิศทางที่โจทย์กำหนด และตรวจว่าจำนวนทุกตำแหน่งอยู่ในลำดับนั้น',
              [13, 14], ['order_numbers', 'number_between_p1']),
            u('numeric-comparison', 'ตรวจการเปรียบเทียบจำนวนหลายรูปแบบ',
              'แปลงภาพ ตัวเลขไทย หรือคำอ่านเป็นจำนวน แล้วตรวจความสัมพันธ์ มากกว่า น้อยกว่า เท่ากับ หรือไม่เท่ากับ ตามคำถาม',
              [17, 18], ['true_comparison_p1', 'compare_sums_p1']),
        ]),
        'counting': ('การนับ', [
            u('digit-place-value', 'ระบุหลักและค่าของเลขโดด',
              'ค่าของเลขโดดขึ้นกับตำแหน่ง หลักสิบมีค่าสิบเท่าของเลขโดด ส่วนหลักหน่วยมีค่าเท่ากับเลขโดด',
              [15], ['tens_and_ones_p1', 'place_value_digit']),
            u('expanded-form', 'เขียนจำนวนเป็นผลบวกของค่าประจำหลัก',
              'แยกจำนวนเป็นค่าของหลักร้อย หลักสิบ และหลักหน่วย แล้วเขียนเป็นผลบวก โดยละพจน์ศูนย์ได้',
              [16], ['expanded_form_p2']),
        ]),
        'pictograph': ('แผนภูมิรูปภาพ', [
            u('pictograph-maximum', 'หารายการที่มากที่สุดจากแผนภูมิรูปภาพ',
              'อ่านค่าของแต่ละสัญลักษณ์แล้วเปรียบเทียบจำนวนของแต่ละแถวเพื่อหารายการที่มีค่ามากที่สุด',
              [19], ['pictograph_most_p1']),
            u('pictograph-difference', 'หาผลต่างสองแถวจากแผนภูมิรูปภาพ',
              'นับจำนวนสัญลักษณ์ของสองแถว คูณค่าประจำสัญลักษณ์ แล้วหาผลต่าง',
              [20], ['pictograph_compare_p1']),
        ]),
    }
    claims = [s['item'] for _, units in files.values() for item in units for s in item['sources']]
    assert sorted(claims) == list(range(1, 21))
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary1-{slug}.json', topic, units)


if __name__ == '__main__':
    main()
