"""Append full coverage for a Primary 2 numbers and geometry paper."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
H = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary2.py')))
unit, write_topic = H['unit'], H['write_topic']
SOURCE = 'mathematics/level/primary-2/4179-2-2567-2-2.pdf'


def u(key, title, statement, numbers, covered):
    return unit(key, title, statement, [(SOURCE, numbers)], covered)


def main():
    files = {
        'numbers': ('จำนวนนับไม่เกิน 1,000', [
            u('abacus-reading', 'อ่านจำนวนจากลูกคิดหลักร้อยสิบหน่วย',
              'นับลูกคิดในแต่ละหลักแล้วรวมค่าหลักร้อย หลักสิบ หลักหน่วย อ่านเป็นตัวเลขหรือคำอ่าน โดยไม่ข้ามตำแหน่งหลักที่ไม่มีลูกคิด',
              [1, 2], ['base_ten_blocks_p2', 'number_reading_p2', 'hundreds_tens_ones_p2']),
            u('expanded-form', 'อ่านและเขียนจำนวนในรูปกระจาย',
              'เขียนจำนวนเป็นผลบวกของค่าประจำหลัก หรือรวมค่าประจำหลักเพื่อกลับเป็นจำนวน โดยหลักที่เป็นศูนย์ไม่ทำให้หลักอื่นเปลี่ยนตำแหน่ง',
              [3, 4, 5], ['expanded_form_p2']),
            u('digit-position-value', 'ระบุหลักและค่าของเลขโดด',
              'ระบุตำแหน่งเลขโดดก่อน แล้วคูณด้วยหนึ่ง สิบ หรือร้อยตามหลักที่อยู่',
              [6], ['place_value_digit', 'hundreds_tens_ones_p2']),
            u('digit-value-difference', 'เปรียบเทียบค่าของเลขโดดต่างหลัก',
              'หาค่าประจำหลักของเลขโดดแต่ละตัวก่อน แล้วลบค่าน้อยออกจากค่ามาก แม้เลขโดดจะเหมือนกันค่าก็อาจต่างกัน',
              [7, 8], ['digit_value_difference_p2']),
            u('compare-expanded', 'เปรียบเทียบจำนวนและรูปกระจาย',
              'รวมค่าของแต่ละข้างก่อน แล้วเปรียบเทียบจากหลักที่สูงที่สุดเพื่อเลือกเครื่องหมายมากกว่าน้อยกว่าหรือเท่ากับ',
              [9, 10, 11], ['compare_sign']),
            u('ordering', 'เรียงลำดับจำนวนสามหลัก',
              'เปรียบเทียบหลักร้อยก่อน ถ้าเท่ากันจึงดูหลักสิบและหลักหน่วย เรียงตามทิศทางที่กำหนด',
              [12, 13], ['order_numbers_p2']),
            u('number-between-bounds', 'หาจำนวนที่อยู่ระหว่างสองขอบเขต',
              'ตรวจทั้งสองเงื่อนไขว่าจำนวนที่เติมมากกว่าขอบล่างและน้อยกว่าขอบบนอย่างเคร่งครัด แล้วเรียงตามทิศทางที่กำหนด',
              [14], ['number_between_bounds_p2']),
        ]),
        'shapes': ('รูปเรขาคณิต', [
            u('polygon-picture', 'จำแนกรูปหลายเหลี่ยมจากจำนวนด้าน',
              'นับด้านตรงและมุมทั้งหมด แม้รูปจะเอียงหรือมีมุมเว้า แล้วจำแนกตามจำนวนด้าน',
              [15, 16, 18], ['shape_sides_picture_p2', 'shape_properties_p2']),
            u('shape-in-object', 'ระบุรูปเรขาคณิตที่เป็นส่วนประกอบของสิ่งของ',
              'พิจารณาเส้นขอบของส่วนที่ถามในสิ่งของจริง แล้วเทียบกับลักษณะของรูปสองมิติ',
              [17], ['shape_objects_p1']),
            u('solid-identification', 'จำแนกรูปทรงสามมิติจากลักษณะ',
              'พิจารณาฐาน ผิวโค้ง หน้าเรียบ และยอดของรูปทรง เพื่อแยกทรงกระบอก กรวย ทรงกลม และทรงเหลี่ยม แม้จะวางเอียง',
              [19, 20], ['solid_shapes_p2', 'solid_picture_p1']),
        ]),
    }
    claims = [s['item'] for _, units in files.values() for item in units for s in item['sources']]
    assert sorted(claims) == list(range(1, 21))
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary2-{slug}.json', topic, units, 'ป.2')


if __name__ == '__main__':
    main()
