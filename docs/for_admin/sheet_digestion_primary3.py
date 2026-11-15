"""Idempotent coverage of all MC and written items in a Primary 3 word paper."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
H = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))
write_topic = H['write_topic']
SOURCE = 'mathematics/level/primary-3/4357-3-2567-2-3.pdf'


def u(key, title, statement, items, covered):
    return dict(id='math.primary3.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุข้อมูลและสิ่งที่โจทย์ถาม', statement, 'ตรวจคำตอบและหน่วยกับเรื่องราว'],
                sources=[{'sheet': SOURCE, 'item': n} for n in items],
                covered_by=['math.' + key for key in covered])


def main():
    files = {
        'multiplication': ('การคูณ', [
            u('multiplicative-comparison', 'หาจำนวนที่เป็นหลายเท่าของอีกจำนวน',
              'ใช้จำนวนเท่าคูณจำนวนที่ทราบ ไม่ใช้การบวกจำนวนเท่ากับจำนวนเดิม',
              [1, 3], ['multiplication_word_problem_p3']),
            u('equal-group-total', 'รวมจำนวนกลุ่มที่เท่ากัน',
              'คูณจำนวนกลุ่มหรือจำนวนวันด้วยจำนวนต่อกลุ่มหรือต่อวันเพื่อหาจำนวนรวม',
              [2, 4, 5, 6], ['multiplication_word_problem_p3', 'buy_several_p3']),
        ]),
        'division': ('การหาร', [
            u('equal-sharing', 'แบ่งจำนวนทั้งหมดเท่ากัน',
              'ระบุจำนวนผู้รับจากข้อความให้ครบ แล้วหารจำนวนทั้งหมดด้วยจำนวนผู้รับหรือจำนวนกลุ่ม',
              [7, 8, 9], ['division_word_problem_p3', 'share_equally_p3']),
        ]),
        'money': ('เงิน', [
            u('single-change', 'หาเงินทอนจากราคาที่ซื้อ',
              'ลบราคาสินค้าออกจากจำนวนเงินที่จ่ายเพื่อหาเงินทอน',
              [11], ['make_change']),
            u('initial-balance', 'หาเงินเดิมก่อนรับเพิ่ม',
              'เขียนเงินเดิมบวกเงินที่รับเท่ากับเงินปัจจุบัน แล้วลบเงินที่รับออกจากยอดปัจจุบัน',
              [12], ['missing_addsub_large_p3', 'addsub_word_large_p3']),
            u('add-baht-satang', 'รวมราคาที่มีบาทและสตางค์',
              'บวกบาทและสตางค์โดยร้อยสตางค์เป็นหนึ่งบาท แล้วเขียนยอดรวมในหน่วยที่ถูกต้อง',
              [13], ['baht_satang_add_p3']),
            u('half-dozen-unit-price', 'หาราคาต่อชิ้นจากราคาครึ่งโหล',
              'แทนครึ่งโหลด้วยหกชิ้น แล้วหารราคารวมด้วยหกเพื่อหาราคาต่อชิ้น',
              [14], ['unit_price_p2', 'unit_price_p3']),
            u('multiply-baht-satang', 'คิดราคารวมหลายชิ้นที่มีบาทและสตางค์',
              'เปลี่ยนราคาต่อชิ้นเป็นสตางค์ คูณด้วยจำนวนชิ้น แล้วเปลี่ยนกลับเป็นบาทและสตางค์โดยทดให้ครบหนึ่งบาท',
              [15], ['buy_several_satang_p3']),
        ]),
        'multi-step': ('โจทย์ปัญหาระคน', [
            u('half-then-daily-budget', 'แบ่งเงินครึ่งหนึ่งแล้วเฉลี่ยรายวัน',
              'หาเงินครึ่งหนึ่งที่เหลือหลังแบ่งก่อน แล้วหารด้วยจำนวนวันที่ต้องใช้เงิน',
              [10], ['half_then_daily_budget_p3']),
            u('product-plus-purchase', 'คิดราคาที่ซื้อหลายหน่วยแล้วบวกอีกรายการ',
              'คูณจำนวนหน่วยกับราคาต่อหน่วยของรายการแรก แล้วบวกราคาของอีกรายการ',
              [16], ['money_total', 'buy_two_kinds_p3']),
            u('balance-after-several', 'เงินเหลือหลังซื้อสินค้าหลายชิ้น',
              'คูณจำนวนชิ้นด้วยราคาต่อชิ้น แล้วลบค่าใช้จ่ายทั้งหมดออกจากเงินเริ่มต้น',
              [17], ['money_change_left', 'two_step_word_problem_p3']),
            u('resale-profit-unit-price', 'หาราคาขายต่อชิ้นจากกำไรรวมที่ต้องการ',
              'บวกกำไรรวมกับต้นทุนรวมก่อน แล้วหารรายรับที่ต้องการด้วยจำนวนสินค้าที่ขายในราคาเท่ากัน',
              [18], ['resale_profit_unit_price_p3']),
            u('pack-sales', 'จัดกลุ่มก่อนคิดรายรับ',
              'หารจำนวนสิ่งของด้วยจำนวนต่อกล่องเพื่อหาจำนวนกล่อง แล้วคูณด้วยราคาขายต่อกล่อง',
              [19], ['grouped_sales_p2']),
            u('unit-price-from-balance', 'หาราคาต่อชิ้นจากยอดเงินก่อนซื้อและเงินเหลือ',
              'ลบเงินเหลือออกจากเงินเริ่มต้นเพื่อหาค่าใช้จ่ายทั้งหมด แล้วหารด้วยจำนวนชิ้นที่ซื้อ',
              [20], ['unit_price_from_balance_p3']),
            u('two-item-change', 'เงินทอนจากธนบัตรหลายฉบับและของสองรายการ',
              'คูณมูลค่าธนบัตรกับจำนวนฉบับ แล้วลบราคารวมสองรายการ พร้อมเขียนประโยคสัญลักษณ์และวิธีทำ',
              [21], ['money_left_two_buys_p3', 'change_picture_p3', 'two_step_sentence_p3']),
            u('recipients-from-packs', 'หาจำนวนผู้รับจากสิ่งของหลายห่อ',
              'คูณจำนวนห่อด้วยจำนวนต่อห่อ แล้วหารจำนวนรวมด้วยจำนวนที่แต่ละคนได้รับ พร้อมเขียนประโยคสัญลักษณ์และวิธีทำ',
              [22], ['buy_then_share_p3', 'division_word_problem_p3', 'two_step_sentence_p3']),
        ]),
    }
    claims = [s['item'] for _, units in files.values() for item in units for s in item['sources']]
    assert sorted(claims) == list(range(1, 23))
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary3-{slug}.json', topic, units, 'ป.3')


if __name__ == '__main__':
    main()
