"""Preserving coverage map for the first Primary 5 text-layer batch."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A = 'mathematics/level/primary-5/4703-5-2564-1-3.pdf'
B = 'mathematics/level/primary-5/4721-5-2567-2-3.pdf'


def unit(key, title, statement, sources, covered):
    return dict(id='math.primary5.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุข้อมูล หน่วย และสิ่งที่ต้องการหา', statement, 'ตรวจคำตอบด้วยความสัมพันธ์เดิมและหน่วย'],
                sources=[{'sheet': sheet, 'item': n} for sheet, ns in sources for n in ns],
                covered_by=['math.' + k for k in covered])


def main():
    files = {
        'quadrilateral-area': ('พื้นที่รูปสี่เหลี่ยม', [
            unit('side-from-perimeter', 'หาด้านของรูปสี่เหลี่ยมที่ด้านเท่ากัน', 'หารความยาวรอบรูปด้วย 4 เพื่อหาความยาวด้านของสี่เหลี่ยมขนมเปียกปูน',
                 [(A, [1, 4])], ['parallelogram_perimeter_p5']),
            unit('four-equal-sides', 'ความยาวรอบรูปที่มีด้านเท่ากันสี่ด้าน', 'บวกความยาวด้านที่เท่ากันสี่ด้าน หรือคูณความยาวด้านด้วย 4 โดยคงค่าทศนิยมอย่างถูกต้อง',
                 [(A, [2, 6])], ['quadrilateral_repetition_p5']),
            unit('adjacent-side-perimeter', 'ความยาวรอบรูปจากด้านประชิด', 'บวกด้านประชิดสองด้านแล้วคูณ 2 เพื่อรวมด้านตรงข้ามที่เท่ากัน',
                 [(A, [3, 5, 7, 8])], ['parallelogram_perimeter_p5', 'quadrilateral_repetition_p5']),
            unit('base-height-area', 'พื้นที่จากฐานและความสูงตั้งฉาก', 'คูณความยาวฐานด้วยความสูงตั้งฉาก แม้เท้าของเส้นสูงอยู่บนส่วนต่อของฐาน และไม่ใช้ด้านเอียงแทนความสูง',
                 [(A, [9, 10, 11, 12, 21])], ['parallelogram_area', 'quadrilateral_area_figure_p5', 'quadrilateral_repetition_p5']),
            unit('repeated-boundary', 'ระยะทางหลายรอบหรือรั้วหลายชั้น', 'หาความยาวรอบรูปก่อน แล้วคูณจำนวนรอบหรือจำนวนชั้นของรั้ว โดยไม่ปัดทศนิยมระหว่างทาง',
                 [(A, [13, 18, 22])], ['quadrilateral_repetition_p5']),
            unit('repeated-area', 'พื้นที่รวมของหลายแผ่นที่เท่ากัน', 'หาพื้นที่หนึ่งแผ่นจากฐานและความสูง แล้วคูณจำนวนแผ่น',
                 [(A, [14])], ['quadrilateral_repetition_p5']),
            unit('unknown-dimension', 'หาฐานเมื่อทราบพื้นที่และความสูง', 'จากพื้นที่ = ฐาน × สูง หารพื้นที่ด้วยความสูงเพื่อหาฐาน แล้วตรวจด้วยการคูณกลับ',
                 [(A, [15])], ['parallelogram_height_p5', 'decimal_divide_p5']),
            unit('related-dimensions', 'หาความยาวที่บอกเป็นส่วนหรือเท่า', 'คำนวณด้านหรือความสูงที่ยังไม่ทราบจากอัตราที่กำหนดก่อน แล้วใช้สูตรพื้นที่หรือความยาวรอบรูปตามที่ถาม',
                 [(A, [16, 17])], ['related_quad_dimensions_p5']),
            unit('land-area-rai', 'แปลงพื้นที่จากตารางวาเป็นไร่', 'คูณฐานกับความสูงที่มีหน่วยวาเพื่อหาตารางวา แล้วหารด้วย 400 ตามคำอธิบายหน่วยที่โจทย์ให้',
                 [(A, [19])], ['parallelogram_land_area_p5']),
            unit('square-area-from-perimeter', 'หาพื้นที่สี่เหลี่ยมจัตุรัสจากรอบรูป', 'หารความยาวรอบรูปด้วย 4 เพื่อหาด้าน แล้วคูณด้านด้วยตัวเองเพื่อหาพื้นที่',
                 [(A, [20])], ['square_area_from_perimeter_p5']),
        ]),
        'percentages': ('ร้อยละ', [
            unit('percent-of-amount', 'หาจำนวนที่เป็นร้อยละของทั้งหมด', 'คูณจำนวนทั้งหมดด้วยอัตราร้อยละแล้วหารด้วย 100 โดยใช้ค่าทศนิยมของอัตราอย่างถูกต้อง',
                 [(B, [1, 5, 10, 12])], ['percent_of_quantity_p5', 'decimal_multiply_p5']),
            unit('percent-complement', 'หาจำนวนส่วนที่เหลือ', 'ใช้ร้อยละ 100 ลบอัตราของส่วนที่ทราบ แล้วคูณสัดส่วนที่เหลือด้วยจำนวนทั้งหมด',
                 [(B, [2, 8, 9, 22])], ['percent_left_over_p5', 'percent_of_quantity_p5']),
            unit('inclusive-threshold', 'ใช้เกณฑ์ร้อยละแบบไม่ต่ำกว่า', 'คำนวณคะแนนเกณฑ์ แล้วรวมผู้ได้คะแนนเท่ากับเกณฑ์ด้วยเมื่อคำถามใช้คำว่าไม่ต่ำกว่า',
                 [(B, [3])], ['percent_pass_table_p5']),
            unit('year-end-bonus', 'รวมเงินออมก่อนคำนวณเงินเพิ่มปลายปี', 'รวมเงินออมรายเดือนทั้ง 12 เดือนก่อน แล้วคิดเงินเพิ่มตามร้อยละของยอดรวม ตามแบบจำลองการจ่ายปลายปีที่ระบุชัด',
                 [(B, [4])], ['monthly_savings_bonus_p5']),
            unit('percent-share-difference', 'หาส่วนต่างของส่วนแบ่งตามร้อยละ', 'หาจำนวนของทั้งสองส่วนจากฐานเดียวกันแล้วลบกัน หรือคูณทั้งหมดด้วยผลต่างของอัตราร้อยละ',
                 [(B, [6, 21])], ['percent_share_difference_p5']),
            unit('percent-remainder-share', 'แบ่งส่วนที่เหลือหลังกันไว้เป็นร้อยละ', 'หาจำนวนที่เหลือหลังกันส่วนหนึ่งตามร้อยละก่อน แล้วแบ่งให้ผู้รับเท่า ๆ กัน',
                 [(B, [7])], ['percent_remainder_share_p5']),
            unit('discount-loss', 'ราคาหลังลดหรือขายขาดทุน', 'หาจำนวนเงินที่ลดหรือขาดทุนจากร้อยละของฐานเดิม แล้วลบจากราคาเดิม',
                 [(B, [11, 13])], ['discount']),
            unit('principal-plus-percent', 'จำนวนเดิมรวมเงินเพิ่ม', 'หาจำนวนเงินเพิ่มตามร้อยละของฐานเดิม แล้วบวกกับฐานเดิม',
                 [(B, [14])], ['percent_increase_price_p5']),
        ]),
        'unitary-method': ('บัญญัติไตรยางศ์', [
            unit('direct-proportion', 'ปรับจำนวนตามอัตราคงที่', 'ตั้งอัตราส่วนของจำนวนที่สัมพันธ์กัน คำนวณค่าต่อหนึ่งหน่วยหรือคูณสัดส่วน แล้วหาจำนวนใหม่ตามอัตราเดิม',
                 [(B, [15, 16, 18, 19])], ['rate_word_problem_p5', 'recipe_scaling_p5', 'printing_time_p5', 'unit_price_p5']),
            unit('fractional-unit-price', 'คำนวณราคาตามสัดส่วนโดยไม่ปัดก่อน', 'เก็บราคาต่อหน่วยเป็นเศษส่วนที่แน่นอน หรือย่อสัดส่วนก่อนคูณ แปลงเป็นทศนิยมเมื่อได้ราคาสุดท้าย',
                 [(B, [17])], ['fractional_unit_price_p5']),
            unit('proportional-reward-difference', 'หาส่วนต่างหลังปรับตามสัดส่วน', 'หาจำนวนรางวัลที่อีกคนได้รับตามอัตราเดิมก่อน แล้วลบจากจำนวนรางวัลของคนแรก',
                 [(B, [20])], ['proportional_reward_difference_p5']),
        ]),
    }
    claims = [(s['sheet'], s['item']) for _, units in files.values() for u in units for s in u['sources']]
    expected = {(p, n) for p in (A, B) for n in range(1, 23)}
    assert len(claims) == len(set(claims)) == 44 and set(claims) == expected
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary5-{slug}.json', topic, units, level='ป.5')


if __name__ == '__main__':
    main()
