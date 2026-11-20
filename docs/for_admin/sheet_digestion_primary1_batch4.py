"""Idempotent coverage for a readable Primary 1 arithmetic skills paper."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
H = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))
unit, write_topic = H['unit'], H['write_topic']
SOURCE = 'mathematics/level/primary-1/4019-1-2567-2-1.pdf'


def u(key, title, statement, items, covered):
    return unit(key, title, statement, [(SOURCE, items)], covered)


def main():
    files = {
        'addition': ('การบวก', [
            u('two-digit-addition', 'บวกจำนวนสองหลัก',
              'บวกหลักหน่วยและหลักสิบ ทดหนึ่งสิบเมื่อผลบวกหลักหน่วยถึงสิบ',
              [1, 2, 3], ['two_digit_plus']),
            u('missing-addend', 'หาตัวบวกที่ไม่ทราบ',
              'หาตัวบวกที่ขาดโดยลบตัวบวกที่ทราบออกจากผลบวก แม้เขียนผลบวกไว้ด้านซ้ายของเครื่องหมายเท่ากับ',
              [4, 5, 6], ['missing_addend']),
            u('match-sum-expression', 'เลือกประโยคบวกที่มีผลบวกเท่ากัน',
              'หาผลบวกอ้างอิง แล้วหาผลบวกของตัวเลือกแต่ละข้อเพื่อเลือกประโยคที่มีค่าเท่ากัน',
              [7, 10], ['match_sum_expression_p1']),
            u('equal-sums-missing', 'หาตัวบวกที่ทำให้ผลบวกสองข้างเท่ากัน',
              'หาผลบวกของด้านที่มีข้อมูลครบก่อน แล้วลบตัวบวกที่ทราบอีกด้านออกเพื่อหาตัวที่ขาด ตรวจแทนกลับให้สองข้างเท่ากัน',
              [8, 9], ['equal_sums_missing_p1']),
        ]),
        'subtraction': ('การลบ', [
            u('two-digit-subtraction', 'ลบจำนวนสองหลักโดยกระจายหลักสิบ',
              'ลบตามค่าประจำหลัก ถ้าหลักหน่วยของตัวตั้งน้อยกว่าให้กระจายหนึ่งสิบเป็นสิบหน่วยก่อนลบ',
              [11, 12, 13], ['two_digit_subtraction_with_borrow']),
            u('missing-subtrahend', 'หาตัวลบที่ไม่ทราบ',
              'ลบผลต่างออกจากตัวตั้งเพื่อหาตัวลบที่ทำให้ประโยคเป็นจริง',
              [14, 15], ['missing_subtrahend']),
            u('missing-minuend', 'หาตัวตั้งที่ไม่ทราบ',
              'บวกตัวลบกับผลต่างเพื่อหาตัวตั้ง แม้เขียนผลต่างไว้ด้านซ้ายของเครื่องหมายเท่ากับ',
              [16, 17], ['missing_minuend_p1']),
            u('match-difference-expression', 'เลือกประโยคลบที่มีผลต่างเท่ากัน',
              'หาผลต่างอ้างอิง แล้วลบจำนวนในแต่ละตัวเลือกเพื่อเลือกประโยคที่มีค่าเท่ากัน',
              [18, 19], ['match_difference_expression_p1']),
        ]),
        'add-sub-mixed': ('การบวกลบระคน', [
            u('successive-subtractions', 'ลบสองจำนวนตามลำดับ',
              'ลบจากซ้ายไปขวาหรือรวมจำนวนที่นำออกก่อนแล้วลบจากตัวตั้ง ตรวจว่าลบทั้งสองจำนวนแล้ว',
              [20], ['add_sub_mixed']),
        ]),
    }
    claims = [s['item'] for _, units in files.values() for item in units for s in item['sources']]
    assert sorted(claims) == list(range(1, 21))
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary1-{slug}.json', topic, units)


if __name__ == '__main__':
    main()
