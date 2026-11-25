"""Knowledge claims for the maths entrance papers, wave 2b (re-runnable, idempotent).

MWIT ม.4 round 1 2567, 2568 and 2569, the MWIT 2563 recollection, KVIS 2566
and 2569, and a KVIS/MWIT exponents compilation. Most are handwritten
recollections. Every question is claimed by its exam tag. A skill already
claimed in waves 1 and 2a gets this wave's tags added to that unit
(``extend``); a new skill gets a unit here. ``covered_by`` names only sets that
practise the skill.
"""
from pathlib import Path
import glob
import json
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']

MWIT63 = 'เข้า ม.4 MWIT 2563/'
MWIT69 = 'เข้า ม.4 MWIT 2569 รอบ 1/'
MWIT67 = 'เข้า ม.4 MWIT 2567 รอบ 1/'
MWIT68 = 'เข้า ม.4 MWIT 2568 รอบ 1/'
KVIS66 = 'เข้า ม.4 KVIS 2566/'
KVIS69 = 'เข้า ม.4 KVIS 2569/'
EXPO = 'รวมข้อสอบ MWIT-KVIS เลขยกกำลัง/'

NUMBER = ('entrance-number-theory', 'จำนวนเต็ม', 'ม.1')
ALGEBRA = ('entrance-algebra', 'นิพจน์พีชคณิต', 'ม.1')
RADICAL = ('entrance-radicals-exponents', 'จัดรูปกรณฑ์', 'ม.4')
COUNT = ('entrance-counting', 'หลักการนับเบื้องต้น', 'ม.4')
PROB = ('entrance-probability', 'ความน่าจะเป็น', 'ม.5')
STATS = ('entrance-primary-statistics', 'สถิติ', 'ม.1')
GEOM = ('entrance-geometry', 'การให้เหตุผลทางเรขาคณิต', 'ม.2')
SOLIDS = ('entrance-solids', 'พื้นที่ผิวและปริมาตร', 'ม.3')
ANALYTIC = ('entrance-analytic-geometry', 'เรขาคณิตวิเคราะห์', 'ม.4')
WORD = ('entrance-word-systems', 'ระบบสมการ', 'ม.3')
SERIES = ('entrance-series', 'อนุกรม', 'ม.6')
FINANCE = ('entrance-finance', 'ดอกเบี้ยและมูลค่าของเงิน', 'ม.5')

FILES = {}
UNITS = {}
EXTEND = {}


def u(file, slug, statement, tags, covered=(), note=''):
    unit = dict(id='math.entrance.' + slug, kind='procedure', title=statement[:60], statement=statement,
                steps=['ระบุสิ่งที่โจทย์กำหนดและสิ่งที่ต้องหา', statement, 'ตรวจคำตอบกับเงื่อนไขของโจทย์'],
                sources=[{'tag': t} for t in tags], covered_by=['math.' + k for k in covered])
    if note:
        unit['note'] = note
    FILES.setdefault(file, []).append(unit)
    UNITS[slug] = unit


def claim(slug, tags):
    UNITS[slug]['sources'] += [{'tag': t} for t in tags if {'tag': t} not in UNITS[slug]['sources']]


def extend(slug, tags):
    """Tags for a unit written by an earlier wave's script."""
    EXTEND.setdefault('math.entrance.' + slug, []).extend(tags)


def mwit63():
    t = lambda *ns: [MWIT63 + str(n) for n in ns]
    extend('ratio-chain-parts', t(1, 10))
    u(NUMBER, 'consecutive-product-digits', 'ประมาณรากของผลคูณเพื่อหาจำนวนเรียงกันที่คูณกันได้จำนวนที่มีเงื่อนไขของเลขโดด', t(2), ('consecutive_product_m1',))
    u(NUMBER, 'range-count-multiples', 'แปลงเงื่อนไขจำนวนหลักของพหุคูณเป็นช่วงของ A แล้วนับจำนวนเต็มในช่วงร่วม', t(3))
    u(NUMBER, 'skip-digit-sequence', 'ลำดับจำนวนที่ไม่มีเลขโดด 0 คือการเขียนในฐานเก้าด้วยเลขโดด 1–9 นับตามจำนวนหลัก', t(4),
      note='ข้อ 4 ไม่พิมพ์กฎของลำดับ อ่านเป็นจำนวนที่ไม่มีเลขโดด 0')
    extend('age-ratio-system', t(5))
    extend('linear-cost-model', t(6))
    u(RADICAL, 'radical-simplify-solve', 'ถอดรากให้อยู่ในรูปอย่างง่าย รวมพจน์กรณฑ์ที่คล้ายกัน แล้วแก้สมการหรือหาค่านิพจน์', t(7) + [EXPO + '1', EXPO + '2'],
      ('radical_arithmetic', 'simplify_root_m4', 'radical_denest_m4'))
    u(SERIES, 'block-fraction-sum', 'ผลบวกของ k/n สำหรับ k = 1..n เท่ากับ (n + 1)/2 แล้วรวมทุกกลุ่ม', t(8))
    u(GEOM, 'ladder-pythagoras', 'ใช้พีทาโกรัสหาระยะในแนวราบของบันไดที่พาดสองด้าน แล้วรวมหรือหาผลต่าง', t(9), ('pythagoras_ladder_m2',))
    u(COUNT, 'assign-names-permutation', 'จัดชื่อให้สมาชิกแต่ละกลุ่มด้วยการเรียงสับเปลี่ยนแยกกลุ่มแล้วคูณ', t(11), ('arrange_in_row_m4',))
    u(STATS, 'mean-to-median', 'ใช้ค่าเฉลี่ยตั้งสมการหาข้อมูลที่ไม่รู้ แล้วเรียงข้อมูลหามัธยฐาน', t(12), ('mean_missing_value_m1', 'median_m1'))
    u(NUMBER, 'row-pattern-position', 'แถวที่ n มี 2n − 1 จำนวน หาตำแหน่งสะสมของแถวแล้วหาจำนวนที่ตำแหน่งที่ถาม', t(13))
    u(ALGEBRA, 'real-roots-of-powers', 'หาค่าจริงทุกค่าจากเลขยกกำลังคู่และคี่ แล้วเลือกผลรวมที่มากหรือน้อยที่สุด', t(14), ('real_power_roots_m2',))


def mwit69():
    t = lambda *ns: [MWIT69 + str(n) for n in ns]
    u(COUNT, 'adjacent-colour-sequences', 'นับลำดับสีด้วยเงื่อนไขของลูกที่ติดกันโดยนับทีละตำแหน่ง', t(1),
      note='ข้อ 1 ถ้อยคำอ่านได้สองแบบ (12420 หรือ 2916) จึงไม่มีคำตอบ')
    extend('gcd-lcm-statements', t(2))
    u(WORD, 'ratio-after-removal', 'เขียนจำนวนเดิมด้วยอัตราส่วน หักจำนวนที่นำออกแล้วตั้งสมการจากอัตราส่วนใหม่', t(3))
    u(NUMBER, 'recurrence-remainder', 'คำนวณลำดับเวียนเกิดด้วยเศษจากการหารทีละพจน์', t(4))
    extend('box-surface-from-relations', t(5))
    u(NUMBER, 'radical-prime-count', 'ให้ค่ารากเป็นจำนวนเฉพาะ p ย้อนหา x จาก p² แล้วนับค่าที่เป็นจำนวนเต็ม', t(6))
    u(GEOM, 'rectangle-diagonal-in-triangle', 'สี่เหลี่ยมผืนผ้าในสามเหลี่ยมมุมฉากมีเส้นทแยงมุมยาวเท่ากัน ใช้พีทาโกรัสหาความยาว', t(7))
    u(RADICAL, 'rationalize-surds', 'คูณด้วยสังยุคเพื่อจัดรูปส่วนแล้วเทียบสัมประสิทธิ์ของ √2, √3, √6', t(8), ('rationalize_binomial',))
    u(COUNT, 'board-move-count', 'นับช่องบนกระดานที่การเดินทุกแบบยังอยู่บนกระดาน ด้วยการตัดแถวและหลักขอบ', t(9))
    extend('compare-discounts', t(10))
    extend('mean-correction', t(11))
    u(STATS, 'data-conditions-statistics', 'ใช้เงื่อนไขของพิสัย ค่าเฉลี่ย มัธยฐาน และฐานนิยมตั้งสมการหาข้อมูลที่ไม่รู้', t(12),
      ('mean_median_mode_m2',))
    u(NUMBER, 'digit-position-sequence', 'นับจำนวนเลขโดดสะสมของแต่ละกลุ่มในทศนิยมที่ต่อจำนวนกัน แล้วหาเลขโดดที่ตำแหน่งที่ถาม', t(13), ('digit_position_m1',))
    extend('square-sector-shaded', t(14))
    u(COUNT, 'coin-change-count', 'นับวิธีแลกเงินด้วยเหรียญหลายชนิดโดยไล่จำนวนเหรียญมูลค่าสูงก่อน', t(15))
    u(COUNT, 'round-robin-points', 'แข่งพบกันหมดมี n(n − 1)/2 นัด แต้มรวมขึ้นกับจำนวนนัดเสมอ ใช้หาจำนวนนัดเสมอ', t(16))
    u(NUMBER, 'toggle-divisor-cards', 'การ์ดถูกพลิกครั้งละหนึ่งต่อตัวหารที่กำหนด นับการ์ดที่ถูกพลิกจำนวนครั้งคี่', t(17),
      ('conditional_switch_passes_olympiad',))
    u(SOLIDS, 'prism-pyramid-volume', 'ปริมาตรรูปประกอบ = ปริมาตรปริซึม + ปริมาตรพีระมิด (หนึ่งในสามของฐานคูณสูง)', t(18), ('pyramid_volume_m3',))
    u(GEOM, 'congruent-triangles-area', 'ใช้ความเท่ากันทุกประการและจุดกึ่งกลางหาความยาว แล้วหาพื้นที่รูปที่ทับกัน', t(19))
    u(NUMBER, 'arithmetic-table-entry', 'แต่ละแถวและหลักของตารางเป็นลำดับเลขคณิต เขียนพจน์ทั่วไปแล้วหาค่าหรือผลรวมตามตำแหน่ง', t(20, 22))
    u(NUMBER, 'difference-of-squares-count', 'a² − b² = (a − b)(a + b) นับคู่ตัวประกอบที่มีภาวะคู่คี่เดียวกัน', t(21))
    u(ANALYTIC, 'taxicab-distance', 'ระยะแท็กซี่ |x₁ − x₂| + |y₁ − y₂| ใช้หาระยะ จุดที่ระยะเท่ากัน และค่าต่ำสุด', t(23, 24, 25, 26, 27))


def mwit67():
    t = lambda *ns: [MWIT67 + str(n) for n in ns]
    extend('defined-operation', t(1))
    extend('legs-count-equation', t(2))
    u(NUMBER, 'distinct-prime-factors', 'แยกตัวประกอบเฉพาะแล้วนับจำนวนตัวประกอบเฉพาะที่แตกต่างกัน', t(3), ('prime_factorization',))
    u(GEOM, 'heading-turns', 'รวมมุมที่หันหัวตามและทวนเข็มนาฬิกาเพื่อหาทิศหรือมุมที่ต้องหันต่อ', t(4))
    u(STATS, 'median-frequency-table', 'หาตำแหน่งมัธยฐานจากความถี่สะสมในตารางแจกแจงความถี่', t(5))
    u(SOLIDS, 'volume-units-trips', 'แปลงหน่วยปริมาตร หาความจุหนึ่งเที่ยว แล้วหารและปัดขึ้นหาจำนวนเที่ยว', t(6), ('rectangular_prism_volume',))
    u(GEOM, 'hexagon-midpoint-triangle', 'สามเหลี่ยมที่จุดยอดเป็นจุดกึ่งกลางด้านเว้นด้านของหกเหลี่ยมด้านเท่าเป็นสามเหลี่ยมด้านเท่า หาด้านแล้วหาพื้นที่', t(7))
    u(GEOM, 'square-circle-radius', 'วงกลมผ่านจุดยอดสองจุดและสัมผัสด้านตรงข้ามของสี่เหลี่ยมจัตุรัส ใช้พีทาโกรัสหารัศมี', t(8), ('square_circle_radius_m3',))
    extend('parallel-angle-chase', t(9))
    u(ALGEBRA, 'exponent-laws-compare', 'ใช้สมบัติเลขยกกำลังจัดนิพจน์ให้เหลือฐานเดียวแล้วเทียบเลขชี้กำลัง', t(10), ('power_laws_rational_m5',))
    u(NUMBER, 'cyclic-counting-game', 'คำพูดในเกมซ้ำเป็นรอบ หาความยาวรอบแล้วใช้เศษจากการหารหาตำแหน่ง', t(11),
      note='ข้อ 11 ที่จำมาไม่ระบุว่าเกมยาวเท่าไร จึงไม่มีคำตอบ')
    extend('percent-categories', t(12))
    extend('compare-discounts', t(13))
    extend('figure-pattern-count', t(14))
    u(NUMBER, 'number-triple-conditions', 'ไล่คู่ตัวประกอบของผลคูณที่กำหนดแล้วใช้ผลบวกและการหารลงตัวคัดชุดจำนวน', t(15))
    u(GEOM, 'isosceles-trapezoid-area', 'ใช้สามเหลี่ยมหน้าจั่วและสามเหลี่ยมคล้ายหาความสูง แล้วหาพื้นที่ส่วนที่เหลือ', t(16),
      note='ข้อ 16 คำตอบที่ได้ไม่อยู่ในตัวเลือกที่จำมา')
    extend('gcd-with-remainders', t(17))
    u(COUNT, 'sign-grid-count', 'ใส่ ±2 ในตาราง 3 × 3 ให้ผลคูณแต่ละแถวและหลักเป็นบวก: กำหนดตาราง 2 × 2 แล้วช่องที่เหลือถูกบังคับ', t(18))
    extend('data-conditions-statistics', t(19))
    extend('chase-catch-up-time', t(20))
    u(GEOM, 'fence-area-partition', 'เขียนด้านของสี่เหลี่ยมที่แบ่งด้วยตัวแปรจากอัตราส่วนพื้นที่ แล้วใช้ความยาวรั้วรวมแก้สมการ', t(21))
    u(SERIES, 'reciprocal-arithmetic-sum', 'ส่วนกลับเป็นลำดับเลขคณิต ผลบวก = จำนวนพจน์ × (พจน์แรก + พจน์สุดท้าย) ÷ 2', t(22))
    u(NUMBER, 'integer-mean-order', 'ค่าเฉลี่ยของการ์ดที่หยิบเป็นจำนวนเต็มทุกครั้ง ใช้การหารลงตัวกำหนดลำดับการหยิบ', t(23),
      note='ข้อ 23 ที่จำมาเป็นไปไม่ได้ (ผลรวมการ์ดทั้งห้าไม่หารด้วย 5 ลงตัว)')
    u(NUMBER, 'number-base-codes', 'แปลงระหว่างฐานสิบ ฐานสอง และฐานสิบหก (RGB/HEX/ASCII) แล้วคำนวณตามที่ถาม', t(24, 25, 26, 27, 28), ('number_base_m1',))


def mwit68():
    t = lambda *ns: [MWIT68 + str(n) for n in ns]
    u(NUMBER, 'remainder-conditions', 'เขียนจำนวนจากเงื่อนไขเศษจากการหารหลายตัว แล้วไล่หาค่าที่สอดคล้องทั้งหมด', t(1))
    claim('real-roots-of-powers', t(2))
    extend('two-price-system-discount', t(3))
    u(WORD, 'sales-relations', 'เขียนยอดขายแต่ละร้านด้วยตัวแปรเดียวจากความสัมพันธ์ แล้วใช้ยอดรวมแก้สมการ', t(4, 5, 10),
      note='ข้อ 4, 5 และ 10 ที่จำมาไม่ครบ จึงไม่มีคำตอบ')
    extend('tank-volume-fraction', t(6))
    u(NUMBER, 'periodic-schedule-total', 'กิจกรรมซ้ำเป็นรอบ หาจำนวนรอบเต็มและส่วนที่เหลือในช่วงเวลา แล้วรวม', t(7))
    u(GEOM, 'quadrilateral-region-ratio', 'แบ่งรูปสี่เหลี่ยมด้วยจุดกึ่งกลางและเส้นตรง หาอัตราส่วนพื้นที่ของส่วนย่อย', t(8))
    u(GEOM, 'rotation-point-triangle', 'หมุนจุดภายในสามเหลี่ยมมุมฉากหน้าจั่ว 90° รอบจุดยอดมุมฉาก แล้วใช้พีทาโกรัสหามุม', t(9))
    claim('digit-position-sequence', t(11))
    u(GEOM, 'trapezoid-reflection', 'สะท้อนรูปสี่เหลี่ยมคางหมูข้ามเส้นตรงแล้วหาพื้นที่รูปรวม', t(12),
      note='ข้อ 12 ไม่ระบุแกนสะท้อน และความยาวที่จำมาทำให้ความสูงเป็นศูนย์')
    u(ALGEBRA, 'exponent-expression-square', 'จัดนิพจน์เลขยกกำลังให้อยู่ในรูปกำลังสองสมบูรณ์เพื่อหาค่าที่ทำให้รากเป็นจำนวนเต็ม', t(13),
      note='ข้อ 13 ไม่มี k ที่สอดคล้องตามที่อ่าน')
    extend('mean-correction', t(14))
    u(PROB, 'probability-without-replacement', 'ความน่าจะเป็นเมื่อหยิบไม่ใส่คืน: นับวิธีที่ต้องการ ÷ วิธีทั้งหมด หรือคูณความน่าจะเป็นทีละครั้ง', t(15),
      ('probability_without_replacement_m5',))
    u(STATS, 'weighted-average', 'ค่าเฉลี่ยรวม = ผลรวมของ (จำนวนคน × ค่าเฉลี่ยกลุ่ม) ÷ จำนวนคนทั้งหมด', t(16), ('weighted_mean_m6',))
    u(ALGEBRA, 'sum-of-squares-zero', 'ผลบวกกำลังสองเป็นศูนย์เมื่อแต่ละวงเล็บเป็นศูนย์ แก้ระบบสมการเชิงเส้น', t(17))
    claim('number-base-codes', t('18.1', '18.2', '18.3', '18.4'))
    u(PROB, 'dice-sum-probability', 'นับคู่ผลลัพธ์จากลูกเต๋าสองลูกที่ผลบวกเข้าเงื่อนไข ÷ จำนวนคู่ทั้งหมด', t(19), ('two_dice_sum_m3',))
    claim('square-circle-radius', t(20))


def kvis66():
    t = lambda *ns: [KVIS66 + str(n) for n in ns]
    u(SOLIDS, 'views-surface-area', 'สร้างรูปทรงจากภาพด้านหน้า ด้านข้าง และด้านบน แล้วหาพื้นที่ผิวที่มากที่สุด', t('I.1'))
    u(PROB, 'draw-percent-condition', 'ตั้งอสมการร้อยละของผลที่ได้จากการสุ่มเทียบกับจำนวนผู้เข้าร่วม', t('I.2'))
    u(ALGEBRA, 'quadratic-profit-max', 'เขียนกำไรเป็นฟังก์ชันกำลังสองของจำนวนที่ขาย แล้วหาค่าสูงสุดจากจุดยอด', t('I.3'), ('best_output_m5',))
    u(FINANCE, 'compound-deposits', 'เงินฝากต้นปีทุกปีทบต้น: รวม P(1 + r)ᵏ ของแต่ละงวด', t('I.4'), ('regular_saving_m5', 'compound_interest_m5'))
    u(GEOM, 'british-flag-theorem', 'จุด P ในสี่เหลี่ยมผืนผ้า ABCD: PA² + PC² = PB² + PD²', t('I.5'))
    extend('chord-angle-chase', t('I.6'))
    u(WORD, 'coincident-lines', 'เส้นตรงสองเส้นมีจุดตัดมากกว่าหนึ่งจุดเมื่อเป็นเส้นเดียวกัน สัมประสิทธิ์เป็นสัดส่วนกัน', t('I.7', 'II.4'),
      ('system_solution_count_m3',))
    u(STATS, 'box-plot-quartiles', 'ควอร์ไทล์ พิสัยระหว่างควอร์ไทล์ และค่านอกเกณฑ์จากแผนภาพกล่อง', t('I.8', 'III.4'), ('iqr_from_data_m6',),
      note='I.8 และ III.4 เป็นสไลด์หัวข้อที่ไม่มีโจทย์')
    u(COUNT, 'digit-triple-count', 'นับสามสิ่งอันดับหรือจำนวนจากเลขโดดตามเงื่อนไข ด้วยการแยกกรณีหรือไล่ทุกค่า', t('II.1'))
    u(NUMBER, 'clock-hands', 'เข็มยาวเดิน 6° ต่อนาที เข็มสั้น 0.5° ต่อนาที ตั้งสมการตำแหน่งเข็ม', t('II.2'))
    u(GEOM, 'equilateral-triangle-area', 'พื้นที่สามเหลี่ยมด้านเท่า (√3/4)a² และมุม 60° ใช้หาพื้นที่รูปประกอบ', t('II.3'))
    claim('consecutive-product-digits', t('II.5'))
    extend('overlapping-circle-petals', t('II.6'))
    claim('probability-without-replacement', t('II.7'))
    claim('digit-position-sequence', t('II.8'))
    u(NUMBER, 'integer-fraction-pairs', 'ให้ผลบวกเศษส่วนเป็นจำนวนเต็ม ใช้การหารลงตัวกับ ห.ร.ม. = 1 จำกัดค่าของตัวแปร', t('III.1'))
    u(GEOM, 'pentagon-area-parallel', 'เส้นขนานทำให้สามเหลี่ยมที่มีฐานร่วมกันมีพื้นที่เท่ากัน ใช้แปลงพื้นที่รูปห้าเหลี่ยมเป็นสามเหลี่ยม', t('III.2'))
    u(NUMBER, 'board-invariant', 'การดำเนินการ a, b → a + b + ab รักษาผลคูณของ (จำนวน + 1) ไว้ ใช้หาค่าสุดท้าย', t('III.3'),
      note='III.3 ที่จำมาเป็นไปไม่ได้ (79 เป็นจำนวนเฉพาะ)')


def kvis69():
    t = lambda *ns: [KVIS69 + str(n) for n in ns]
    u(WORD, 'pouring-shares', 'ติดตามปริมาณของแต่ละคนทีละขั้นเมื่อแบ่งเป็นส่วนของที่มี หรือย้อนจากผลสุดท้าย', t('1.1'))
    claim('digit-triple-count', t('1.2'))
    u(GEOM, 'moving-points-distance', 'เขียนตำแหน่งของจุดที่เคลื่อนที่ด้วยเวลาแล้วหาระยะห่างด้วยพีทาโกรัส', t('1.3', '3.3'))
    u(STATS, 'stem-leaf-median', 'อ่านข้อมูลจากแผนภาพต้นใบ แล้วหาค่าที่ทำให้มัธยฐานหรือค่าเฉลี่ยเปลี่ยนตามเงื่อนไข', t('1.4'),
      ('median_m1',))
    extend('parabola-from-vertex-point', t('1.5'))
    u(ANALYTIC, 'coordinate-triangle-area', 'พื้นที่สามเหลี่ยมบนระนาบพิกัด = ½ × ฐาน × ความสูงจากพิกัด', t('2.1'))
    u(COUNT, 'cube-colourings', 'ระบายสีหน้าลูกบาศก์ให้หน้าติดกันต่างสี นับแบบที่ไม่ซ้ำกันเมื่อหมุน', t('2.2'))
    u(SOLIDS, 'hollow-cylinder', 'ทรงกระบอกกลวง: ปริมาตร = π(R² − r²)h และพื้นที่ผิวรวมผิวในผิวนอกและวงแหวนปลาย', t('2.3'),
      ('hollow_cylinder_m2',))
    u(NUMBER, 'folded-sheet-pages', 'กระดาษที่พับเป็นเล่มหนึ่งแผ่นมีเลขหน้าสี่หน้า ผลบวกคู่หน้าคงที่ตามจำนวนหน้าทั้งหมด', t('2.4'))
    claim('quadratic-profit-max', t('2.5'))
    extend('mean-correction', t('2.6'))
    u(GEOM, 'star-polygon-angles', 'มุมของดาวที่เกิดจากรูปหลายเหลี่ยมซ้อนหมุน ใช้ผลบวกมุมภายในและมุมภายนอก', t('2.7'), ('polygon_angle_sum',))
    u(NUMBER, 'powerful-numbers', 'จำนวนทรงพลังมีกำลังของจำนวนเฉพาะทุกตัวอย่างน้อย 2 นับจากการแยกตัวประกอบเฉพาะ', t('3.1'),
      ('prime_factorization',))
    u(GEOM, 'square-points-angle', 'ใช้เงื่อนไขความยาวบนด้านของสี่เหลี่ยมจัตุรัสหามุมจากสามเหลี่ยมมุมฉาก', t('3.2'),
      note='3.2 ขาดเงื่อนไข มุมไม่คงที่')
    u(PROB, 'guessing-binomial', 'เดาข้อสอบ n ข้อ ความน่าจะเป็นถูก k ข้อ = C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ', t('4.1', '4.2', '4.3', '4.4', '4.5'),
      ('exactly_k_heads_m4',))
    u(COUNT, 'answer-design-count', 'นับลำดับคำตอบที่ต้องมีค่าทุกแบบอย่างน้อยหนึ่งครั้งด้วยหลักการรวมและแยก', t('4.6'))


def apply_extend():
    pending = {k: list(v) for k, v in EXTEND.items()}
    for f in sorted(glob.glob(str(ROOT / 'otk/knowledge/math/entrance-*.json'))):
        raw = json.loads(Path(f).read_text(encoding='utf-8'))
        changed = False
        for unit in raw['units']:
            for tag in pending.pop(unit['id'], []):
                if {'tag': tag} not in unit['sources']:
                    unit['sources'].append({'tag': tag})
                    changed = True
        if changed:
            Path(f).write_text(json.dumps(raw, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    assert not pending, f'no such unit: {sorted(pending)}'


def main():
    mwit63()
    mwit69()
    mwit67()
    mwit68()
    kvis66()
    kvis69()
    for (slug, topic, level), units in FILES.items():
        write_topic(ROOT / f'otk/knowledge/math/{slug}.json', topic, units, level)
    apply_extend()


if __name__ == '__main__':
    main()
