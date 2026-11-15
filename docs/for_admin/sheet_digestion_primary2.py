"""Idempotent knowledge mapping for the first Primary 2 text-layer batch.

Run from the repository root with python docs/for_admin/sheet_digestion_primary2.py.
Private source text and answer checks stay in the separate sheet bank.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
S1 = 'mathematics/level/primary-2/4157-2-2564-1-3.pdf'
S2 = 'mathematics/level/primary-2/4178-2-2567-2-3.pdf'


def unit(key, title, statement, sources, covered):
    return dict(id='math.primary2.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุสิ่งที่ทราบและสิ่งที่ต้องการหา', statement, 'ตรวจคำตอบกับข้อมูลและหน่วยในโจทย์'],
                sources=[{'sheet': sheet, 'item': n} for sheet, ns in sources for n in ns],
                covered_by=['math.' + k for k in covered])


def main():
    files = {
        'addition-subtraction': ('การบวกและการลบ', [
            unit('combine', 'รวมจำนวนหรือเพิ่มจำนวน', 'รวมจำนวนที่โจทย์ถามด้วยการบวก ไม่รวมข้อมูลที่ไม่เกี่ยวข้อง',
                 [(S1, [1, 2, 3, 4]), (S2, [1, 2, 9])], ['add_word_three_digit_p2']),
            unit('comparison-amount', 'หาจำนวนที่มากกว่าหรือน้อยกว่าอีกจำนวน',
                 'ระบุว่ารู้จำนวนมากหรือจำนวนน้อย แล้วใช้ จำนวนมาก = จำนวนน้อย + ส่วนต่าง หาจำนวนที่ไม่ทราบ',
                 [(S1, [5, 6, 9]), (S2, [3, 7, 13, 17])], ['comparison_amount_p2']),
            unit('remaining', 'หาส่วนที่เหลือหรือส่วนที่ขาด',
                 'เขียนจำนวนทั้งหมด ส่วนที่ทราบ และส่วนที่ไม่ทราบ แล้วลบส่วนที่ทราบจากทั้งหมด พร้อมบอกข้อมูล คำถาม วิธีทำ ประโยคสัญลักษณ์ และคำตอบ',
                 [(S1, [7, 21]), (S2, [11, 12, 15, 18])], ['sub_word_three_digit_p2', 'missing_addsub_p2']),
            unit('difference', 'เปรียบเทียบส่วนต่าง', 'หาจำนวนที่มากกว่าและน้อยกว่า แล้วลบจำนวนมากด้วยจำนวนน้อยเพื่อหาส่วนต่าง',
                 [(S1, [8, 10]), (S2, [14])], ['how_many_more_p2', 'length_word_problem_p2']),
            unit('known-offset', 'ใช้ผลต่างที่กำหนดแปลงจำนวน', 'เมื่อโจทย์กำหนดว่าจำนวนปลายทางมากกว่าเดิมอยู่เท่าใด ให้บวกผลต่างนั้นกับจำนวนเริ่มต้น',
                 [(S2, [5])], ['add_columns']),
        ]),
        'multiplication': ('การคูณ', [
            unit('equal-groups', 'หาจำนวนรวมของกลุ่มเท่า ๆ กัน', 'คูณจำนวนกลุ่มด้วยจำนวนสิ่งของในแต่ละกลุ่ม',
                 [(S1, [11, 12, 13, 15])], ['multiplication_word_problem_p2']),
            unit('half-dozen', 'แปลครึ่งโหลเป็นจำนวนชิ้น', 'ครึ่งโหลมี 6 ชิ้น จึงคูณจำนวนกล่องด้วย 6',
                 [(S1, [14])], ['half_dozen_packs_p2']),
            unit('daily-week', 'สะสมรายวันครบสัปดาห์', 'หนึ่งสัปดาห์มี 7 วัน คูณจำนวนต่อวันด้วย 7 เมื่อทำทุกวัน',
                 [(S1, [16])], ['daily_total_weeks_p2']),
            unit('pack-price', 'คิดราคาแพ็คโดยตัดข้อมูลที่ไม่เกี่ยวข้อง', 'คูณราคาต่อแพ็คด้วยจำนวนแพ็ค ไม่ใช้จำนวนสีซึ่งไม่ใช่ราคา',
                 [(S2, [4])], ['pack_price_irrelevant_p2']),
        ]),
        'division': ('การหาร', [
            unit('pack-count', 'หาจำนวนแพ็คที่ได้จำนวนพอดี', 'หารจำนวนสิ่งของทั้งหมดด้วยจำนวนต่อแพ็ค แล้วตรวจด้วยการคูณกลับ',
                 [(S2, [6])], ['equal_packs_p2']),
        ]),
        'mixed-operations': ('บวก ลบ คูณ หารระคน', [
            unit('purchase-groups', 'รวมราคาของหนึ่งชิ้นและหลายชิ้น', 'คูณราคาต่อชิ้นด้วยจำนวนชิ้น แล้วบวกกับราคาของอีกอย่าง',
                 [(S2, [10])], ['two_step_word_problem']),
        ]),
        'money': ('เงิน', [
            unit('payment', 'หาเงินที่จ่ายจากราคาและเงินทอน', 'เงินที่จ่ายเท่ากับราคาสินค้าบวกเงินทอน',
                 [(S2, [8])], ['payment_from_change_p2']),
            unit('change', 'หาเงินทอน', 'ลบราคาสินค้าออกจากเงินที่จ่าย',
                 [(S2, [16])], ['change_from_note_p2']),
            unit('purchase-from-balance', 'ระบุสินค้าที่ซื้อจากยอดคงเหลือ', 'หาจำนวนเงินที่ใช้จากเงินเดิมลบเงินที่เหลือ แล้วเทียบราคาสินค้าแต่ละอย่าง',
                 [(S2, [19])], ['purchase_from_change_p2']),
            unit('sale-comparison', 'เปรียบเทียบราคาสุทธิหลังลด', 'ลบส่วนลดออกจากราคาตั้งของแต่ละร้านก่อน แล้วจึงเปรียบเทียบราคาสุทธิ',
                 [(S2, [20])], ['compare_sale_prices_p2']),
        ]),
        'time': ('เวลา', [
            unit('elapsed', 'ระยะเวลาระหว่างเวลาเต็มชั่วโมง', 'ลบเวลาเริ่มออกจากเวลาจบของวันเดียวกัน และแปลงหน่วยคำตอบให้ตรงคำถาม',
                 [(S1, [17, 20])], ['time_elapsed', 'hours_minutes_p2']),
            unit('duration-difference', 'เวลาที่ใช้ต่างกัน', 'เมื่อหน่วยเป็นนาทีเหมือนกัน ลบเวลาที่น้อยกว่าออกจากเวลาที่มากกว่า',
                 [(S1, [18])], ['how_many_more_p2']),
            unit('duration-sum', 'รวมระยะเวลาแล้วแปลงเป็นชั่วโมงและนาที', 'บวกระยะเวลาเป็นนาทีก่อน แล้วแยกทุก 60 นาทีเป็น 1 ชั่วโมง และเก็บนาทีที่เหลือ',
                 [(S1, [19])], ['sum_durations_p2']),
        ]),
    }
    for slug, (topic, units) in files.items():
        path = ROOT / f'otk/knowledge/math/primary2-{slug}.json'
        path.write_text(json.dumps(dict(subject='คณิตศาสตร์', topic=topic, level='ป.2', units=units), ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
