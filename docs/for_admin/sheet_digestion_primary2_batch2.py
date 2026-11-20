"""Append Primary 2 division, mixed-operation and pictograph coverage."""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
HELPERS = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary2.py')))
unit, write_topic = HELPERS['unit'], HELPERS['write_topic']
A = 'mathematics/level/primary-2/4163-2-2565-2-3.pdf'
B = 'mathematics/level/primary-2/4175-2-2567-2-3.pdf'


def main():
    division_path = ROOT / 'otk/knowledge/math/primary2-division.json'
    existing = json.loads(division_path.read_text())['units']
    pack = next(u for u in existing if u['id'] == 'math.primary2.pack-count')
    reused = [(A, [3, 4, 6]), (B, [1, 2, 3, 4, 7])]
    claims = []
    for sheet, numbers in reused:
        for n in numbers:
            source = {'sheet': sheet, 'item': n}
            if source not in pack['sources']:
                pack['sources'].append(source)
            claims.append((sheet, n))
    files = {
        'time': ('เวลา', [
            unit('days-to-weeks', 'เปลี่ยนวันเป็นสัปดาห์', 'หนึ่งสัปดาห์มี 7 วัน หารจำนวนวันที่กำหนดด้วย 7 เพื่อหาจำนวนสัปดาห์เต็มเมื่อหารลงตัว',
                 [(A, [1])], ['days_to_weeks_p2']),
        ]),
        'division': ('การหาร', [
            unit('equal-share', 'แบ่งเท่า ๆ กันเพื่อหาจำนวนต่อกลุ่ม', 'หารจำนวนทั้งหมดด้วยจำนวนกลุ่มเพื่อหาจำนวนต่อกลุ่ม แล้วตรวจด้วยการคูณกลับ',
                 [(A, [5]), (B, [5])], ['division_word_problem_p2']),
            unit('unit-price', 'หาราคาต่อชิ้นจากยอดรวม', 'ระบุจำนวนชิ้นที่ซื้อ รวมถึงแปลงครึ่งโหลเป็น 6 ชิ้น แล้วหารยอดเงินรวมด้วยจำนวนชิ้น',
                 [(A, [2, 7, 8]), (B, [6])], ['unit_price_p2']),
            unit('quotient-remainder-story', 'ตอบผลหารและเศษพร้อมกัน', 'แบ่งให้ได้กลุ่มเต็มหรือส่วนแบ่งเต็มมากที่สุด แล้วตอบทั้งผลหารและเศษ โดยเศษต้องน้อยกว่าตัวหาร',
                 [(A, [9, 10, 11, 12, 13, 14, 15]), (B, [9, 10, 11, 13, 14])], ['quotient_remainder_story_p2']),
            unit('least-remainder', 'เปรียบเทียบเศษที่เหลือจากวิธีแบ่ง', 'คำนวณเศษจากการแบ่งแต่ละวิธี แล้วเลือกวิธีที่มีเศษน้อยที่สุด ไม่ใช้ผลหารตัดสินแทนเศษ',
                 [(B, [12])], ['least_remainder_p2']),
            unit('fewest-groups', 'เลือกขนาดกลุ่มที่ทำให้จำนวนกลุ่มน้อย', 'หารจำนวนทั้งหมดด้วยขนาดกลุ่มแต่ละแบบ แล้วเปรียบเทียบจำนวนกลุ่มที่ได้',
                 [(B, [8])], ['largest_quotient_p2', 'division_word_problem_p2']),
            unit('compare-group-results', 'เปรียบเทียบผลของการแบ่งหลายสถานการณ์', 'พิจารณาจำนวนที่แบ่งและตัวหารในแต่ละเรื่อง แล้วเปรียบเทียบผลที่ได้ตามชนิดของหน่วยและคำถาม',
                 [(B, [15])], ['largest_quotient_p2', 'division_remainder_p2']),
        ]),
        'mixed-operations': ('บวก ลบ คูณ หารระคน', [
            unit('remaining-share', 'ลบส่วนที่ใช้แล้วแบ่งส่วนที่เหลือ', 'ลบส่วนที่นำออกจากจำนวนเริ่มต้นก่อน แล้วหารส่วนที่เหลือด้วยจำนวนต่อกลุ่มหรือจำนวนผู้รับ',
                 [(A, [16]), (B, [16])], ['remaining_two_step_p2']),
            unit('remaining-sales', 'หาจำนวนที่เหลือก่อนคิดเงินขาย', 'ลบจำนวนที่ให้ไปก่อน แล้วคูณจำนวนที่เหลือด้วยราคาต่อชิ้น',
                 [(B, [18])], ['remaining_two_step_p2']),
            unit('two-balance-changes', 'เปลี่ยนยอดเงินสองครั้ง', 'เริ่มจากเงินที่มี แล้วบวกเงินที่ได้รับและลบเงินที่จ่ายตามลำดับของเรื่อง',
                 [(A, [17]), (B, [17])], ['two_step_add_sub_p2']),
            unit('multiply-remove', 'หาจำนวนรวมก่อนลบส่วนที่ใช้', 'คูณจำนวนถุงด้วยจำนวนต่อถุง แล้วลบจำนวนที่ขายหรือใช้ไป',
                 [(A, [18])], ['mixed_ops_word_problem_p2']),
            unit('sales-share', 'ขายของแล้วแบ่งรายรับเท่า ๆ กัน', 'คูณจำนวนชิ้นด้วยราคาต่อชิ้นเพื่อหารายรับทั้งหมด แล้วหารด้วยจำนวนผู้รับ',
                 [(A, [19])], ['grouped_sales_p2']),
            unit('pack-sales', 'จัดกลุ่มก่อนคิดรายรับจากการขาย', 'หารจำนวนสิ่งของด้วยจำนวนต่อกล่อง แล้วคูณจำนวนกล่องด้วยราคาขายต่อกล่อง',
                 [(B, [19])], ['grouped_sales_p2']),
            unit('two-purchase-total', 'รวมราคาสองรายการที่ซื้อหลายชิ้น', 'คูณจำนวนชิ้นกับราคาต่อชิ้นของแต่ละรายการก่อน แล้วบวกค่าใช้จ่ายทั้งสองรายการ',
                 [(B, [20])], ['two_purchase_total_p2']),
        ]),
        'money': ('เงิน', [
            unit('three-prices', 'รวมราคาของสามอย่าง', 'บวกราคาของสินค้าทั้งสามอย่างเพื่อหาจำนวนเงินที่ต้องจ่าย',
                 [(A, [20])], ['total_three_items_p2']),
        ]),
        'pictograph': ('แผนภูมิรูปภาพ', [
            unit('pictograph-maximum', 'หารายการที่มีจำนวนมากที่สุด', 'อ่านจำนวนรูปและค่าที่แต่ละรูปแทน แล้วเปรียบเทียบหาวันหรือรายการที่มีจำนวนมากที่สุด',
                 [(A, [21])], ['pictograph_key_picture_p2']),
            unit('pictograph-matching', 'หาทุกรายการที่มีจำนวนตรงเป้าหมาย', 'แปลงจำนวนรูปเป็นจำนวนจริงตามคำอธิบาย แล้วหาทุกแถวที่มีค่าตรงกับจำนวนที่ถาม โดยอาจมีหลายแถวเท่ากัน',
                 [(A, [22])], ['pictograph_matching_rows_p2']),
            unit('pictograph-difference', 'หาส่วนต่างของแผนภูมิรูปภาพ', 'อ่านค่าของแต่ละแถวแล้วลบจำนวนน้อยออกจากจำนวนมาก โดยใช้ค่าที่รูปแทนให้ถูกต้อง',
                 [(A, [23, 24])], ['pictograph_compare_p2']),
            unit('pictograph-total', 'รวมทุกรายการในแผนภูมิรูปภาพ', 'บวกค่าของทุกแถวในแผนภูมิหลังแปลงตามค่าที่หนึ่งรูปแทน',
                 [(A, [25])], ['pictograph_total_p2']),
            unit('pictograph-selected', 'รวมเฉพาะแถวที่โจทย์ถาม', 'เลือกแถวที่โจทย์ระบุแล้วรวมจำนวนจริงของแถวเหล่านั้น โดยไม่รวมแถวอื่นและไม่ลืมคูณค่าต่อรูป',
                 [(B, [21])], ['pictograph_selected_total_p2']),
        ]),
    }
    claims += [(s['sheet'], s['item']) for _, units in files.values() for u in units for s in u['sources']]
    expected = {(p, n) for p, count in ((A, 25), (B, 21)) for n in range(1, count + 1)}
    assert len(claims) == len(set(claims)) == 46 and set(claims) == expected
    for slug, (topic, units) in files.items():
        if slug == 'division':
            units = existing + units
        write_topic(ROOT / f'otk/knowledge/math/primary2-{slug}.json', topic, units, level='ป.2')


if __name__ == '__main__':
    main()
