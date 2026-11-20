"""Append complete Primary 4/5 coverage for the eleven-set batch."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
P4 = 'mathematics/level/primary-4/4539-4-2567-2-3.pdf'
P5 = 'mathematics/level/primary-5/4724-5-2567-2-3.pdf'


def u(grade, key, title, statement, numbers, covered):
    source = P4 if grade == 4 else P5
    return dict(id=f'math.primary{grade}.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุข้อมูลและสิ่งที่โจทย์ถาม', statement, 'ตรวจคำตอบและหน่วยกับเรื่องราว'],
                sources=[{'sheet': source, 'item': n} for n in numbers],
                covered_by=['math.' + k for k in covered])


def main():
    files = {
        (4, 'time', 'เวลา'): [
            u(4, 'add-durations', 'รวมเวลาหลายช่วง', 'เปลี่ยนแต่ละช่วงเป็นนาทีก่อนรวม แล้วเปลี่ยนกลับเป็นชั่วโมงและนาที', [1], ['sum_durations_p2']),
            u(4, 'age-year-month-difference', 'ลบอายุที่มีปีและเดือน', 'เปลี่ยนปีและเดือนเป็นเดือนก่อนหาผลต่าง แล้วเปลี่ยนกลับโดยหนึ่งปีมีสิบสองเดือน', [2, 10], ['age_year_month_difference_p4']),
            u(4, 'monthly-reading-duration', 'รวมเวลาของกิจกรรมรายวันตลอดเดือน', 'หาจำนวนวันของเดือนในปีที่กำหนด คูณเวลาต่อวัน แล้วเปลี่ยนหน่วยเวลา', [3], ['monthly_reading_duration_p4']),
            u(4, 'average-task-duration', 'เฉลี่ยระยะเวลาทำงานทีละชิ้น', 'เปลี่ยนเวลารวมเป็นนาที แล้วหารด้วยจำนวนชิ้นที่ทำตามลำดับ', [4], ['average_task_duration_p4']),
            u(4, 'date-after-weeks', 'หาวันที่หลังจำนวนสัปดาห์', 'เปลี่ยนสัปดาห์เป็นวันแล้วเลื่อนวันที่ไปข้างหน้าโดยนับจากวันเริ่มต้น', [5], ['calendar_date_shift_p1', 'calendar_word_problem_p4']),
            u(4, 'elapsed-clock-time', 'หาระยะเวลาจากเวลาเริ่มและสิ้นสุด', 'เปลี่ยนเวลาเป็นนาทีตามนาฬิกาแล้วหาผลต่าง ก่อนแปลงเป็นชั่วโมงและนาที', [6, 21], ['travel_time_p4', 'time_elapsed']),
            u(4, 'repeated-seconds-duration', 'รวมวินาทีของงานหลายข้อ', 'คูณจำนวนข้อกับวินาทีต่อข้อ แล้วหารด้วยหกสิบเพื่อเขียนเป็นนาทีและวินาที', [7], ['repeated_seconds_duration_p4']),
            u(4, 'months-to-years', 'เปลี่ยนเดือนเป็นปีและเดือน', 'จัดสิบสองเดือนเป็นหนึ่งปีและเก็บจำนวนเดือนที่เหลือ', [8], ['time_units_p4']),
            u(4, 'successive-travel-time', 'หาเวลาถึงหลังเดินทางหลายช่วง', 'รวมเวลาของทุกช่วงแล้วบวกกับเวลาเริ่ม โดยทดนาทีเป็นชั่วโมง', [9], ['time_after_p2', 'sum_durations_p2']),
        ],
        (4, 'multi-step', 'โจทย์ปัญหาระคน'): [
            u(4, 'pack-sales', 'บรรจุกลุ่มก่อนคิดรายรับ', 'หารจำนวนทั้งหมดด้วยจำนวนต่อถุง แล้วคูณด้วยราคาขายต่อถุง', [11], ['grouped_sales_p2']),
            u(4, 'regroup-packs', 'รวมของหลายเข่งแล้วแบ่งเป็นถุง', 'คูณจำนวนเข่งด้วยจำนวนต่อเข่ง แล้วหารด้วยจำนวนต่อถุง', [12], ['buy_then_share_p3']),
            u(4, 'balance-two-expenses', 'หายอดคงเหลือหลังจ่ายสองรายการ', 'รวมค่าใช้จ่ายสองรายการแล้วลบจากยอดเริ่มต้น', [13], ['two_step_word_problem_p4']),
            u(4, 'production-remaining', 'หาจำนวนผลิตรวมแล้วลบส่วนที่ขาย', 'คูณจำนวนกลุ่มด้วยปริมาณต่อกลุ่ม แล้วลบส่วนที่ขายไป', [14], ['two_step_word_problem_p4']),
            u(4, 'deposit-plus-balance', 'รวมมัดจำหลายชิ้นกับยอดที่จ่ายเพิ่ม', 'คูณมัดจำต่อชิ้นด้วยจำนวนชิ้น แล้วบวกยอดชำระเพิ่ม', [15], ['two_step_word_problem_p4']),
            u(4, 'annual-multiple-people', 'รวมค่าใช้จ่ายรายเดือนของหลายคนตลอดปี', 'คูณค่าใช้จ่ายต่อเดือนด้วยสิบสองเดือนและจำนวนคน', [16], ['yearly_saving_p4', 'multiplication_word_problem_p3']),
            u(4, 'reserve-half-remaining', 'ขายแล้วสำรองครึ่งหนึ่งของส่วนที่เหลือ', 'ลบส่วนที่ขายจากยอดเริ่มต้นก่อน แล้วแบ่งส่วนที่เหลือครึ่งหนึ่งเป็นสำรองและส่งออก', [17], ['reserve_half_remaining_p4']),
            u(4, 'multiple-and-original-total', 'รวมจำนวนเดิมกับอีกจำนวนที่เป็นหลายเท่า', 'หาจำนวนที่เป็นหลายเท่าก่อน แล้วบวกกับจำนวนเดิม', [18], ['two_step_word_problem_p4']),
            u(4, 'organizer-shared-cost', 'เฉลี่ยค่าใช้จ่ายโดยนับผู้จัดด้วย', 'บวกค่าใช้จ่ายทุกรายการ แล้วหารด้วยจำนวนเพื่อนบวกผู้จัดหนึ่งคน', [19], ['organizer_shared_cost_p4']),
            u(4, 'sum-three-investments', 'รวมเงินลงทุนสามคน', 'บวกเงินลงทุนของทุกคนตามค่าประจำหลักให้ครบ', [20], ['add_three_large_p4']),
            u(4, 'initial-plus-monthly-profit', 'บวกกำไรหลายเดือนกับเงินเดิม', 'คูณกำไรต่อเดือนกับจำนวนเดือน แล้วบวกเงินเดิม พร้อมเขียนประโยคสัญลักษณ์', [22], ['two_step_word_problem_p4', 'two_step_sentence_p4']),
        ],
        (5, 'fraction-stories-batch11', 'โจทย์ปัญหาเศษส่วน'): [
            u(5, 'fraction-batch-count', 'หาจำนวนครั้งจากเศษส่วนของทั้งหมด', 'หารปริมาณทั้งหมดด้วยส่วนที่ใช้ต่อครั้ง หรือหาส่วนกลับของเศษส่วนเมื่อใช้เท่ากันทุกครั้ง', [1, 4], ['fraction_word_muldiv_p5', 'pieces_from_length_p5']),
            u(5, 'fraction-remaining-stories', 'หาปริมาณที่เหลือเมื่อใช้เป็นเศษส่วน', 'หาสัดส่วนที่เหลือแล้วคูณปริมาณเดิม โดยแยกเศษส่วนของทั้งหมดกับปริมาณที่ใช้จริง', [2, 10, 11], ['fraction_remaining_p5', 'fraction_of_amount_p5']),
            u(5, 'fraction-story-addsub', 'บวกและลบปริมาณเศษส่วนหลายจำนวน', 'เปลี่ยนจำนวนคละเป็นเศษเกิน ทำส่วนให้เท่ากัน แล้วบวกลบปริมาณตามเรื่อง', [3, 5, 7, 8], ['fraction_word_addsub_p5', 'mixed_fractions']),
            u(5, 'fraction-story-product', 'คูณอัตราต่อหน่วยกับปริมาณเศษส่วน', 'เปลี่ยนจำนวนคละเป็นเศษเกินแล้วคูณอัตรากับจำนวนหน่วย', [6, 9], ['fraction_word_muldiv_p5']),
            u(5, 'reserve-fraction-daily-budget', 'เก็บเงินเป็นเศษส่วนแล้วแบ่งใช้หลายวัน', 'ลบส่วนที่เก็บจากจำนวนทั้งหมดก่อน แล้วหารเงินที่เหลือด้วยจำนวนวันที่ใช้', [12], ['reserve_fraction_daily_budget_p5']),
        ],
        (5, 'length-weight-batch11', 'ความยาวและน้ำหนัก'): [
            u(5, 'equal-pieces-cm-to-mm', 'แบ่งความยาวแล้วเปลี่ยนเป็นมิลลิเมตร', 'หารความยาวรวมด้วยจำนวนส่วนที่เท่ากัน แล้วเปลี่ยนเซนติเมตรเป็นมิลลิเมตรด้วยอัตราสิบ', [13], ['equal_pieces_cm_to_mm_p5']),
            u(5, 'two-cuts-metres-to-cm', 'ตัดความยาวสองครั้งแล้วเปลี่ยนหน่วย', 'ลบความยาวที่ตัดทั้งสองครั้งจากความยาวเดิม แล้วเปลี่ยนเมตรเป็นเซนติเมตร', [14], ['two_cuts_metres_to_cm_p5']),
            u(5, 'smaller-to-decimal-unit', 'เปลี่ยนหน่วยเล็กเป็นหน่วยใหญ่ในรูปทศนิยม', 'หารด้วยหนึ่งพันเมื่อเปลี่ยนเมตรเป็นกิโลเมตรหรือกรัมเป็นกิโลกรัม', [15, 17], ['length_decimal_p5', 'weight_decimal_p5']),
            u(5, 'decimal-length-sum-smaller-unit', 'รวมความยาวทศนิยมก่อนเปลี่ยนหน่วยเล็ก', 'บวกความยาวในหน่วยเดียวกัน แล้วคูณอัตราเปลี่ยนหน่วยที่ถูกต้อง', [16], ['measure_decimal_word_p5', 'decimal_to_smaller_unit_p5']),
            u(5, 'khit-grams-sum-kg', 'รวมน้ำหนักขีดกับกรัมเป็นกิโลกรัม', 'เปลี่ยนขีดเป็นกรัมก่อนบวกน้ำหนัก แล้วหารหนึ่งพันเพื่อเปลี่ยนเป็นกิโลกรัม', [18], ['convert_weight_p2', 'add_mixed_units_p5', 'weight_decimal_p5']),
            u(5, 'mixed-weight-remaining-kg', 'รวมน้ำหนักสองรายการแล้วลบส่วนที่ให้', 'เปลี่ยนทุกปริมาณเป็นกรัมก่อนบวกลบ แล้วเปลี่ยนน้ำหนักคงเหลือเป็นกิโลกรัม', [19], ['mixed_weight_remaining_kg_p5']),
            u(5, 'price-per-khit-from-grams', 'คิดราคาต่อขีดเมื่อน้ำหนักเป็นกรัม', 'หารน้ำหนักเป็นกรัมด้วยหนึ่งร้อยเพื่อหาจำนวนขีด แล้วคูณด้วยราคาต่อขีด', [20], ['price_per_khit_from_grams_p5']),
        ],
    }
    claims = [(s['sheet'], s['item']) for units in files.values() for item in units for s in item['sources']]
    assert len(claims) == len(set(claims)) == 42
    assert set(claims) == {(P4, n) for n in range(1, 23)} | {(P5, n) for n in range(1, 21)}
    for (grade, slug, topic), units in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary{grade}-{slug}.json', topic, units, f'ป.{grade}')


if __name__ == '__main__':
    main()
