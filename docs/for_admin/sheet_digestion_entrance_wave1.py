"""Knowledge claims for the maths entrance papers, wave 1 (re-runnable, idempotent).

Every question of the eight wave-1 papers is claimed by its exam tag. A unit's
``covered_by`` names only sets that practise that skill; a skill no set
practises yet keeps an empty list and shows up in ``sheetpipe plan``.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']

TU65 = 'เข้า ม.4 เตรียมอุดมฯ 2565/'
TU64 = 'เข้า ม.4 เตรียมอุดมฯ 2564/'
TU69 = 'เข้า ม.4 เตรียมอุดมฯ 2569/'
TU69_SHEET = 'mathematics/exam-venue/triam-udom-suksa/3843-2569-TU89-temporary-ver.-6.pdf'
MWIT69 = 'เข้า ม.4 MWIT 2569 รอบ 2/'

# (file slug, registry topic, level) -> units
FILES = {}
UNITS = {}


def u(file, slug, statement, tags, covered=(), steps=None, note=''):
    """One procedure unit claiming ``tags`` (full exam tags)."""
    unit = dict(id='math.entrance.' + slug, kind='procedure', title=statement[:60],
                statement=statement,
                steps=steps or ['ระบุสิ่งที่โจทย์กำหนดและสิ่งที่ต้องหา', statement,
                                'ตรวจคำตอบกับเงื่อนไขของโจทย์'],
                sources=[{'tag': t} for t in tags], covered_by=list(covered))
    if note:
        unit['note'] = note
    FILES.setdefault(file, []).append(unit)
    UNITS[slug] = unit


def claim(slug, tags, covered=()):
    """More questions (and sets) for a unit defined earlier in this script."""
    unit = UNITS[slug]
    unit['sources'] += [{'tag': t} for t in tags if {'tag': t} not in unit['sources']]
    unit['covered_by'] += [k for k in covered if k not in unit['covered_by']]


POLY = ('entrance-polynomials', 'การหารพหุนาม', 'ม.4')
RATIONAL = ('entrance-rational', 'สมการและอสมการเศษส่วน', 'ม.4')
SYSTEMS = ('entrance-word-systems', 'ระบบสมการ', 'ม.3')
TRIG = ('entrance-trigonometry', 'อัตราส่วนตรีโกณมิติ', 'ม.5')
CIRCLE = ('entrance-circles', 'วงกลม', 'ม.3')
GEOM = ('entrance-geometry', 'การให้เหตุผลทางเรขาคณิต', 'ม.2')
SPREAD = ('entrance-statistics', 'การวัดการกระจาย', 'ม.6')
COUNT = ('entrance-counting', 'หลักการนับเบื้องต้น', 'ม.4')
PROB = ('entrance-probability', 'ความน่าจะเป็น', 'ม.5')
RADICAL = ('entrance-radicals-exponents', 'จัดรูปกรณฑ์', 'ม.4')
SERIES = ('entrance-series', 'อนุกรม', 'ม.6')
SOLIDS = ('entrance-solids', 'พื้นที่ผิวและปริมาตร', 'ม.3')
DISC = ('entrance-discriminant', 'ดิสคริมิแนนต์', 'ม.4')
ANALYTIC = ('entrance-analytic-geometry', 'เรขาคณิตวิเคราะห์', 'ม.4')
FUNC = ('entrance-functions', 'ฟังก์ชัน', 'ม.4')
ABS = ('entrance-absolute-value', 'ค่าสัมบูรณ์', 'ม.4')
INEQ = ('entrance-inequalities', 'อสมการเชิงเส้น', 'ม.3')
SIMILAR = ('entrance-similarity', 'ความคล้าย', 'ม.3')


def tu65():
    t = lambda *ns: [TU65 + str(n) for n in ns]
    u(TRIG, 'trig-sum-to-product', 'ยกกำลังสอง sin A + cos A เพื่อหา sin A cos A แล้วเขียนนิพจน์ตรีโกณมิติด้วย sin A cos A',
      t(1))
    u(POLY, 'conjugate-irrational-root', 'พหุนามสัมประสิทธิ์ตรรกยะที่มีราก p + √q มีราก p − √q ด้วย จึงมีตัวประกอบกำลังสองตรรกยะ ใช้หาสัมประสิทธิ์และตัวประกอบอื่น',
      t(2), ['math.conjugate_root_cubic_m4'])
    u(RATIONAL, 'partial-fractions-cubic', 'แยกเศษส่วนย่อยที่ตัวส่วนเป็นผลต่างกำลังสาม แล้วเทียบสัมประสิทธิ์',
      t(3), ['math.partial_fractions_m4'])
    u(POLY, 'cubic-vieta-squared-roots', 'ใช้ความสัมพันธ์รากกับสัมประสิทธิ์ของพหุนามดีกรีสามสร้างสมการที่มีรากเป็นกำลังสองของรากเดิม',
      t(4), note='ชุดโจทย์ที่มีอยู่ฝึกเฉพาะสมการกำลังสอง')
    u(GEOM, 'rectangle-square-area-split', 'ตั้งตัวแปรความยาวด้าน ใช้พีทาโกรัสและพื้นที่รูปที่แบ่งในสี่เหลี่ยมผืนผ้าสร้างสมการจำนวนเต็ม',
      t(5))
    u(GEOM, 'square-fifteen-degree-point', 'ใช้ความสมมาตรและสามเหลี่ยมหน้าจั่วในสี่เหลี่ยมจัตุรัสที่มีมุม 15° เพื่อพิสูจน์สามเหลี่ยมด้านเท่าและหามุม',
      t(6))
    u(SYSTEMS, 'linear-cost-model', 'ค่าใช้จ่าย = ค่าคงที่ + อัตรา × จำนวน หาค่าคงที่และอัตราจากข้อมูลสองชุดแล้วคำนวณค่าอื่น',
      t(7), ['math.system_word_problem', 'math.cost_revenue_function_m4'])
    u(POLY, 'power-remainder-and-expansion-coefficient', 'หาเศษจากการหารผลบวกเลขยกกำลังโดยใช้วัฏจักรเศษ และหาสัมประสิทธิ์จากการกระจายผลคูณทวินาม',
      t(8), ['math.remainder_arithmetic_m4', 'math.binomial_apply_m5'])
    u(RATIONAL, 'work-rate-people', 'แปลงงานเป็นอัตราต่อวันของแต่ละคน ตั้งสมการจากงานที่ทำร่วมกันแล้วหาเวลาของกลุ่มใหม่',
      t(9, 21), ['math.joint_worker_time_m3', 'math.work_together_m4'])
    u(ANALYTIC, 'equilateral-on-parabola', 'จุดยอดสามเหลี่ยมด้านเท่าที่มีจุดยอดอยู่ที่จุดยอดพาราโบลาจะสมมาตรกับแกน ใช้ความชัน tan 60° หาจุดบนพาราโบลา',
      t(10))
    u(SERIES, 'alternating-square-sum', 'จับคู่พจน์ (2k − 1)² − (2k)² = −(4k − 1) แล้วรวมเป็นอนุกรมเลขคณิต หรือใช้ผลบวก Σi',
      t(11))
    u(SYSTEMS, 'train-passing', 'รถไฟพ้นกันเมื่อวิ่งเป็นระยะเท่าความยาวรวม ใช้ความเร็วสัมพัทธ์ (ผลบวกเมื่อสวนกัน ผลต่างเมื่อตามกัน)',
      t(12), ['math.train_passing_m3'])
    u(TRIG, 'two-observer-elevation', 'ใช้ tan ของมุมเงยจากผู้สังเกตสองตำแหน่งหาระยะในแนวราบแล้วรวมหรือลบตามตำแหน่ง',
      t(13), ['math.two_angle_height_m5'], note='โจทย์ไม่บอกตำแหน่ง A และ B ชัดเจน ทรานสคริปต์สมมติว่าอยู่ตรงข้ามกัน')
    u(GEOM, 'trapezoid-special-angles', 'ใช้มุม 30°-60° และพีทาโกรัสในสี่เหลี่ยมคางหมูเพื่อหาด้านและเส้นทแยงมุม แล้วตรวจข้อความ',
      t(14), ['math.special_triangle_picture_m3'])
    u(CIRCLE, 'cyclic-quad-cosine-rule', 'มุมตรงข้ามของสี่เหลี่ยมแนบในวงกลมรวมกันได้ 180° ใช้กฎของโคไซน์กับเส้นทแยงมุมร่วมสองข้าง',
      t(15), ['math.cyclic_quadrilateral', 'math.cosine_rule_side'])
    u(SYSTEMS, 'symmetric-sum-product', 'ให้ s = x + y และ p = xy เปลี่ยนสมการสมมาตรเป็นระบบใน s, p แล้วหา x, y',
      t(16))
    u(RATIONAL, 'rational-substitution', 'แทนส่วนที่ซ้ำกันด้วยตัวแปรใหม่เพื่อลดสมการเศษส่วนเป็นสมการกำลังสอง แล้วตรวจคำตอบที่ใช้ไม่ได้',
      t(17), ['math.rational_equation_m4'])
    u(GEOM, 'angle-bisector-quadrilateral', 'ใช้ผลบวกมุมภายในและเส้นแบ่งครึ่งมุมหามุมของรูปสี่เหลี่ยมที่เกิดจากเส้นแบ่งครึ่งมุม',
      t(18))
    u(GEOM, 'tangential-isosceles-trapezoid', 'สี่เหลี่ยมคางหมูหน้าจั่วที่ผลบวกด้านคู่ขนานเท่ากับผลบวกด้านไม่ขนาน ใช้ cos มุมฐานและพื้นที่หาความยาวด้าน',
      t(19), ['math.tangential_trapezoid_m5'])
    u(SPREAD, 'sd-from-deviations', 'ผลบวกส่วนเบี่ยงจากค่าเฉลี่ยเป็นศูนย์ ใช้หาค่าที่หายไปแล้วคำนวณส่วนเบี่ยงเบนมาตรฐานจากกำลังสองของส่วนเบี่ยง',
      t(20), ['math.standard_deviation'])
    u(SOLIDS, 'box-surface-from-relations', 'แทนความสัมพันธ์ของด้านในสูตรปริมาตรกล่องเพื่อหาด้าน แล้วหาพื้นที่ผิว',
      t(22), ['math.prism_surface_area_m2'])
    u(COUNT, 'digit-condition-casework', 'นับจำนวนที่มีเงื่อนไขของเลขโดดโดยแยกกรณีตามจำนวนครั้งที่เลขปรากฏ หรือใช้ส่วนเติมเต็ม',
      t(23))
    u(DISC, 'vertex-on-axis', 'จุดยอดพาราโบลาอยู่บนแกน X เมื่อดิสคริมิแนนต์เป็นศูนย์ แก้หาพารามิเตอร์',
      t(24), ['math.touch_x_axis_m4'])
    u(SYSTEMS, 'meeting-speed-system', 'ตั้งสมการระยะทาง = อัตราเร็ว × เวลา จากสองสถานการณ์ที่ออกเดินทางไม่พร้อมกัน แล้วแก้ระบบ',
      t(25), ['math.system_word_problem'])
    u(SYSTEMS, 'age-ratio-system', 'ใช้อัตราส่วนอายุในอดีตและอนาคตสร้างระบบสมการเชิงเส้นของอายุปัจจุบัน',
      t(26), ['math.system_ages_m3'])
    u(SOLIDS, 'cone-equal-volume-system', 'ปริมาตรกรวยเท่ากันเมื่อเปลี่ยนพื้นที่ฐานและความสูง ให้สมการผลคูณ (B + p)(h + q) = Bh แล้วแก้ระบบ',
      t(27))
    u(SYSTEMS, 'dilution', 'ปริมาณสารละลายคงที่เมื่อเติมน้ำ: ความเข้มข้น × ปริมาตร ก่อนและหลังเท่ากัน',
      t(28))
    u(PROB, 'transfer-two-stage', 'แยกกรณีตามลูกที่ย้ายจากกล่องแรก คูณความน่าจะเป็นแต่ละขั้นแล้วรวม',
      t(29), ['math.probability_transfer_m5'])
    u(RATIONAL, 'pipe-fill-rates', 'อัตราเติมของท่อรวมกันได้ อัตรา = 1/เวลา หาอัตราท่อที่ไม่รู้แล้วหาเวลาของท่อคู่ใหม่',
      t(30), ['math.work_together_m4'])
    u(CIRCLE, 'tangent-diameter-angles', 'ใช้มุมในครึ่งวงกลม มุมระหว่างเส้นสัมผัสกับคอร์ด และผลบวกมุมในรูปสามเหลี่ยมหามุมที่ต้องการ',
      t(31), ['math.tangent_chord_angle_m3', 'math.angles_same_arc_m3'])
    u(SYSTEMS, 'fraction-change-system', 'ตั้งสมการจากเศษส่วนใหม่เมื่อบวกหรือลบจำนวนเท่ากันที่เศษและส่วน แล้วแก้ระบบเชิงเส้น',
      t(32), ['math.simultaneous_2var'])
    u(RADICAL, 'nested-radical-and-exponential-equations', 'เขียนรากซ้อนเป็นกำลังสองสมบูรณ์เพื่อถอดราก และแทน 7ˣ ด้วยตัวแปรเพื่อลดสมการเลขชี้กำลังเป็นพหุนาม',
      t(33), ['math.radical_denest_m4', 'math.exponential_equation_advanced_m4'])
    u(TRIG, 'exponential-in-sine', 'แทน 2^(sin θ) ด้วยตัวแปร แก้สมการพหุนาม แล้วหามุมจากค่า sin θ ในช่วงที่กำหนด',
      t(34), ['math.sum_of_two_solutions_m5'])
    u(SPREAD, 'variance-linear-transform', 'หาค่าเฉลี่ยและความแปรปรวนจากผลบวกกำลังสองที่กำหนด แล้วใช้ Var(ax + b) = a²Var(x)',
      t(35), ['math.stats_transform_m6'])
    u(RADICAL, 'reciprocal-power-identity', 'จัดรูปนิพจน์เป็น x² ± 1/x² แล้วสร้าง x⁶ − 1/x⁶ จากผลต่างกำลังสาม',
      t(36))
    u(FUNC, 'linear-variation-statements', 'y แปรผันตรงกับนิพจน์เชิงเส้น เขียน y = k(mx + 2) หาค่าคงที่จากข้อมูลแล้วตรวจข้อความ',
      t(37), note='ข้อ 37 ในไฟล์ไม่สมบูรณ์ (ข้อความ ก เป็น "?") จึงไม่มีคำตอบ')


def tu64():
    t = lambda *ns: [TU64 + str(n) for n in ns]
    u(SOLIDS, 'composite-solid-volume', 'แยกทรงประกอบเป็นกรวย ทรงกลม หรือครึ่งทรงกลม รวมปริมาตรแต่ละส่วนเพื่อหาความสูง แล้วใช้พีทาโกรัสหาสูงเอียง',
      t(1), ['math.solid_word_problem_m3', 'math.cone_volume_from_slant_m3'])
    u(SYSTEMS, 'ratio-chain-linear-system', 'เขียนเศษส่วนที่เท่ากับค่าคงที่เป็นสมการเชิงเส้นหลายสมการ แล้วแก้ระบบหาตัวแปรทั้งหมด',
      t(2), ['math.simultaneous_2var', 'math.system_substitution'])
    u(SYSTEMS, 'reciprocal-substitution-system', 'กลับเศษส่วนเป็น 1/x + 1/y และ 1/x − 1/y แล้วแก้ระบบเชิงเส้นของส่วนกลับ',
      t(3, 29), ['math.simultaneous_2var'])
    u(CIRCLE, 'tangent-lengths-area', 'เส้นสัมผัสจากจุดภายนอกยาวเท่ากัน ใช้มุมระหว่างเส้นสัมผัสกับคอร์ดหามุมของสามเหลี่ยม แล้วหาพื้นที่จาก ½ab sin C',
      t(4), ['math.tangent_chord_angle_m3'], note='ข้อความในโจทย์ระบุเส้นสัมผัสคลาดจากรูป (BA และ BC ในรูป)')
    claim('pipe-fill-rates', t(5), ['math.work_together_m4'])
    u(SOLIDS, 'pyramid-lateral-area', 'หาสูงเอียงของหน้าข้างแต่ละคู่จากความสูงตรงและครึ่งด้านฐานด้วยพีทาโกรัส แล้วรวมพื้นที่สามเหลี่ยมหน้าข้าง',
      t(6), ['math.pyramid_surface_from_height_m3'])
    u(SYSTEMS, 'coin-count-system', 'เขียนจำนวนเหรียญแต่ละชนิดด้วยตัวแปรเดียวจากอัตราส่วน แล้วตั้งสมการมูลค่ารวม',
      t(7), ['math.system_coins_m3'])
    u(SPREAD, 'median-of-patterned-list', 'หาว่าข้อมูลตำแหน่งกลางอยู่ในกลุ่มใดของลำดับที่เป็นแบบรูป แล้วเรียงค่านับจำนวนครั้งเพื่อหามัธยฐาน',
      t(8))
    u(CIRCLE, 'overlapping-circle-petals', 'พื้นที่กลีบที่เกิดจากวงกลมสองวงซ้อนกัน = 2 × (พื้นที่เสี้ยววงกลม − พื้นที่สามเหลี่ยม) แล้วคูณจำนวนกลีบ',
      t(9), ['math.circle_petal_area_p6'])
    u(POLY, 'reciprocal-quartic', 'พหุนามสัมประสิทธิ์สมมาตรแบบส่วนกลับ หารด้วย x² แล้วแทน t = x ± 1/x ให้เป็นสมการกำลังสอง',
      t(10))
    claim('work-rate-people', t(11), ['math.joint_worker_time_m3'])
    claim('partial-fractions-cubic', t(12), ['math.partial_fractions_m4'])
    u(PROB, 'two-event-union', 'ใช้ P(A ∪ B) = P(A) + P(B) − P(A ∩ B) และเหตุการณ์ตรงข้ามเพื่อหาความน่าจะเป็นที่ต้องการ',
      t(13), ['math.probability_union_m5'])
    claim('transfer-two-stage', t(14))
    claim('tangential-isosceles-trapezoid', t(15))
    u(SPREAD, 'grouped-mean-unknown-frequency', 'ค่าเฉลี่ยจากตารางอันตรภาคชั้นใช้จุดกึ่งกลางชั้น ตั้งสมการเพื่อหาความถี่ที่ไม่รู้',
      t(16), ['math.mean_from_frequency_m2', 'math.mean_frequency_table_m6'])
    u(CIRCLE, 'semicircle-tangent-circle', 'ใช้ระยะระหว่างจุดศูนย์กลางของวงกลมที่สัมผัสกัน (ผลบวกหรือผลต่างรัศมี) กับพีทาโกรัสหารัศมีวงกลมเล็ก',
      t(17))
    u(SPREAD, 'sd-consecutive-integers', 'ความแปรปรวนของจำนวนเต็มเรียงติดกัน n จำนวนคือ (n² − 1)/12 ใช้หาจำนวนข้อมูลแล้วหาค่ามากที่สุดจากมัธยฐาน',
      t(18), ['math.standard_deviation'])
    u(ANALYTIC, 'perpendicular-lines-intercepts', 'เส้นตั้งฉากผ่านจุดเดียวกันมีความชัน m และ −1/m เขียนจุดตัดแกน Y ด้วย m แล้วใช้พื้นที่สามเหลี่ยมหา m',
      t(19), ['math.perpendicular_through_point_m4'], note='เงื่อนไข 45° < θ < 90° และ y₁, y₂ ≠ 0 ขัดกันในโจทย์ที่พิมพ์')
    u(POLY, 'congruence-arithmetic', 'แทนจำนวนด้วยเศษจากการหาร แล้วคำนวณเศษของผลบวก ผลคูณ และกำลังด้วยเศษนั้น',
      t(20), ['math.remainder_arithmetic_m4'], note='ข้อ 20 คำตอบที่คำนวณได้ (2) ไม่อยู่ในตัวเลือก')
    claim('train-passing', t(21))
    u(POLY, 'factor-theorem-unknowns', 'ใช้ทฤษฎีบทตัวประกอบและทฤษฎีบทเศษเหลือตั้งสมการหาสัมประสิทธิ์ที่ไม่รู้ แล้วคำนวณค่าพหุนาม',
      t(22, 28), ['math.polynomial_unknown_coefficients_m4'])
    claim('conjugate-irrational-root', t(23))
    u(RADICAL, 'cube-root-sum-cubic', 'ให้ x = ∛a + ∛b แล้ว x³ = a + b + 3∛(ab)·x ได้สมการกำลังสามของ x',
      t(24))
    u(TRIG, 'double-angle-telescoping-product', 'เขียน 2cos θ − sec θ = cos 2θ / cos θ แล้วคูณให้ตัดกันเป็นทอด ๆ',
      t(25), ['math.trig_sum_formula_m5'])
    u(ANALYTIC, 'parabola-from-vertex-point', 'เขียนพาราโบลาในรูปจุดยอด y = a(x − h)² + k แทนจุดที่ผ่านเพื่อหา a',
      t(26), ['math.determine_quadratic', 'math.parabola_a_from_point_m4'])
    u(SPREAD, 'sums-of-all-but-one', 'ผลบวกของข้อมูลห้าจำนวนทุกแบบรวมกันได้ 5 เท่าของผลรวมทั้งหมด จึงหาผลรวมและข้อมูลแต่ละตัว',
      t(27))
    claim('linear-cost-model', t(30))
    u(SYSTEMS, 'blend-price-profit', 'ราคาต้นทุนของส่วนผสมคือค่าเฉลี่ยถ่วงน้ำหนักตามอัตราส่วน แล้วบวกกำไรร้อยละ',
      t(31), ['math.mixture_mass_ratio_m3'])
    u(RADICAL, 'factor-exponential-and-nested-radical', 'แยกตัวประกอบสมการเลขชี้กำลังหลายฐาน และเขียนรากซ้อนเป็นค่าสัมบูรณ์เพื่อตัดสินว่ามีคำตอบหรือไม่',
      t(32), ['math.exponential_equation_advanced_m4', 'math.radical_denest_m4'],
      note='สมการของ b ในข้อ 32 ไม่มีคำตอบจริงตามที่พิมพ์')
    u(PROB, 'counts-from-sum-product', 'หาจำนวนสองชนิดจากผลบวกและผลคูณ แล้วคำนวณความน่าจะเป็นของการหยิบหนึ่งชิ้น',
      t(33), ['math.probability_bag_m3'])
    u(RATIONAL, 'rational-division-simplify', 'หารพหุนามในแต่ละเศษส่วนให้เป็นผลหารบวกเศษส่วนอย่างง่าย แล้วรวมพจน์ให้สมการเหลือรูปง่าย',
      t(34), ['math.rational_equation_m4'])
    u(ANALYTIC, 'perpendicular-through-vertex', 'หาจุดยอดพาราโบลาโดยทำกำลังสองสมบูรณ์ แล้วเขียนเส้นตรงที่ตั้งฉากกับเส้นที่กำหนดผ่านจุดนั้น',
      t(35), ['math.perpendicular_through_point_m4'])
    u(TRIG, 'right-triangle-cevian-cosine', 'ใช้ tan หาด้านของสามเหลี่ยมมุมฉาก แล้วใช้พีทาโกรัสกับเส้นตรงจากจุดยอดไปยังด้านตรงข้ามหาค่าโคไซน์',
      t(36), ['math.right_triangle_relations_m5'])
    u(TRIG, 'identity-solve-parameter', 'เขียน tan, cot, sec, cosec ด้วย sin และ cos แล้วใช้ sin² + cos² = 1 หาค่าคงตัวที่ทำให้เป็นเอกลักษณ์',
      t(37), ['math.trig_identity_reduce_m5'])
    claim('trapezoid-special-angles', t(38, 42), ['math.special_triangle_picture_m3'])
    u(DISC, 'parabola-line-tangency', 'เส้นตรงสัมผัสพาราโบลาเมื่อสมการกำลังสองจากการแทนค่ามีดิสคริมิแนนต์ศูนย์ ใช้จุดสัมผัสหาพารามิเตอร์',
      t(39), ['math.tangent_to_parabola_m4'])
    u(SERIES, 'sum-of-squares-formula', 'ใช้ Σk² = n(n + 1)(2n + 1)/6 หา n แล้วคำนวณ Σk = n(n + 1)/2',
      t(40), ['math.sum_of_squares_m6'])
    u(RADICAL, 'two-radical-equation', 'แยกรากหนึ่งไว้ข้างหนึ่ง ยกกำลังสองสองครั้ง แล้วตรวจคำตอบที่ใช้ไม่ได้',
      t(41), ['math.radical_equation_m4'])
    u(POLY, 'power-equals-one-cases', 'aᵇ = 1 เมื่อ a = 1 หรือ b = 0 (a ≠ 0) หรือ a = −1 กับ b เป็นจำนวนคู่ ตรวจแต่ละกรณี',
      t(43))
    u(RADICAL, 'exponential-system-substitution', 'แทน 3ˣ และ 3ʸ ด้วยตัวแปร ใช้ผลต่างและผลคูณสร้างระบบพีชคณิต แล้วหาเลขชี้กำลัง',
      t(44), ['math.exponential_equation_advanced_m4'])


# POSN camp-1 selection 2566-2568 were digested before from another copy of the
# same papers (otk/sheets/posn25xx_math, one set per question), so each question
# is claimed by the unit of its own set. Readings that differ between the copies:
POSN_NOTES = {
    ('2568', 7): 'สำเนานี้พิมพ์ 2(x⁴ − y⁴) ซึ่งให้คำตอบไม่สวย ชุดโจทย์เดิมใช้รูปที่น่าจะตั้งใจ 2(y⁴ − x⁴)',
    ('2568', 10): 'z เป็นเลขชี้กำลังทั้งในสำเนานี้และต้นฉบับ (ได้ 16807) ชุดโจทย์แก้จากการอ่านเดิมที่เป็นผลคูณแล้ว',
    ('2568', 19): 'เงื่อนไขข้อ 3 ถูกตัดในสำเนานี้',
    ('2566', 30): 'สมมติฐาน f¹⁶(P,Q,R) = (F,F,F) เป็นไปไม่ได้ในสำเนานี้',
}


def posn_known():
    from otk.api import REGISTRY
    for year in ('2566', '2567', '2568'):
        for n in range(1, 31):
            key = f'math.posn{year}_q{n:02d}'
            t = REGISTRY[key]
            topic = t.topic
            file = (f'entrance-posn-{year}', topic, 'โอลิมปิก (สอวน.)')
            u(file, f'posn{year}-q{n:02d}', t.display_name_for(), [f'สอวน. ค่าย 1 {year}/{n}'], [key],
              steps=['อ่านเงื่อนไขของโจทย์ ' + t.display_name_for(), 'ใช้วิธีของชุดโจทย์ ' + key,
                     'ตรวจคำตอบกับเงื่อนไขทั้งหมด'],
              note=POSN_NOTES.get((year, n), ''))


# POSN camp-1 2569 was digested before from posn-math/posn1-69-math.pdf, one
# olympiad unit and set per item. This copy's exam tags are added to those units;
# where the two copies read an item differently, the unit's note says so.
POSN69_SHEET = 'mathematics/level/upper-secondary/posn-math/posn1-69-math.pdf'
POSN69_NOTES = {
    5: 'ต้นฉบับ posn1-69 พิมพ์ 2P³ − 5P² − 6P + 9 = 0 สำเนา posn-bangkok ตกเลข 5 (ไม่มีคำตอบจริง)',
    20: 'ต้นฉบับ posn1-69 ระบุ EA = 8 (ได้ 19200) สำเนา posn-bangkok พิมพ์ 18',
    26: 'เงื่อนไข 4 คือ F เข้าหลัง D และ A แต่ก่อน C (ทั้งสองสำเนา) ชุดโจทย์แก้จากการอ่านเดิมแล้ว',
    29: 'ขั้น 1 และ 3 เปิดสวิตช์ที่ปิดอยู่ ขั้น 2 ปิดสวิตช์ที่เปิดอยู่ (ได้ 1182) ชุดโจทย์แก้จากการอ่านเดิมแล้ว',
}


def posn2569():
    import glob
    import json
    for f in sorted(glob.glob(str(ROOT / 'otk/knowledge/math/olympiad_*.json'))):
        raw = json.loads(Path(f).read_text(encoding='utf-8'))
        changed = False
        for unit in raw['units']:
            for source in list(unit['sources']):
                if source.get('sheet') != POSN69_SHEET:
                    continue
                n = source.get('item', source.get('number'))
                tag = {'tag': f'สอวน. ค่าย 1 2569/{n}'}
                if tag not in unit['sources']:
                    unit['sources'].append(tag)
                    changed = True
                note = POSN69_NOTES.get(n, '')
                if note and note not in unit.get('note', ''):
                    unit['note'] = (unit.get('note', '') + ' ' + note).strip()
                    changed = True
        if changed:
            Path(f).write_text(json.dumps(raw, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def tu69():
    t = lambda *ns: [TU69 + str(n) for n in ns]
    INCOMPLETE = 'โจทย์ในไฟล์ (ฉบับชั่วคราว) ไม่ครบ จึงไม่มีคำตอบที่ยืนยันได้'
    u(POLY, 'consecutive-product-plus-one', 'n(n + 1)(n + 2)(n + 3) + 1 = (n² + 3n + 1)² ใช้ถอดรากผลคูณจำนวนเรียงกันสี่จำนวน',
      t(1))
    u(SERIES, 'digit-pattern-sequence', 'หาแบบรูปของหลักในลำดับที่สร้างจากการต่อเลขโดด แล้วระบุเลขโดดในหลักที่ถาม',
      t(2))
    u(CIRCLE, 'chord-angle-chase', 'ใช้มุมในส่วนโค้งเดียวกัน มุมที่จุดศูนย์กลาง และมุมในครึ่งวงกลม ไล่หาขนาดมุมที่ไม่รู้',
      t(3), ['math.angles_same_arc_m3', 'math.central_inscribed_angle'])
    u(COUNT, 'password-positions', 'คูณจำนวนตัวเลือกของแต่ละตำแหน่งในรหัสผ่านตามเงื่อนไขของตำแหน่งนั้น',
      t(4), ['math.codes_with_repeats_m4'])
    u(CIRCLE, 'inscribed-trapezoid-area', 'ใช้ระยะจากจุดศูนย์กลางถึงคอร์ดขนานสองเส้นด้วยพีทาโกรัส หาความสูงของคางหมูแนบในวงกลม (ฝั่งเดียวกันหรือคนละฝั่ง) แล้วหาพื้นที่',
      t(5))
    u(POLY, 'constrained-extremum', 'แทนเงื่อนไขลงในนิพจน์ให้เหลือตัวแปรเดียว แล้วหาค่าสูงสุดหรือต่ำสุดด้วยกำลังสองสมบูรณ์หรืออนุพันธ์',
      t(6))
    u(SERIES, 'reciprocal-power-series-ratio', 'เขียน k/kⁿ⁺¹ = 1/kⁿ แล้วเทียบอนุกรมสลับเครื่องหมายกับอนุกรมเดิม (ผลต่างเป็นพจน์คู่) หา n',
      t(7))
    u(COUNT, 'linear-diophantine-count', 'นับคำตอบจำนวนเต็มบวกของสมการเชิงเส้นหลายตัวแปรโดยไล่ค่าตัวแปรที่มีสัมประสิทธิ์มากที่สุด',
      t(8))
    claim('age-ratio-system', t(9))
    u(SYSTEMS, 'fraction-of-whole-equation', 'เขียนแต่ละช่วงเป็นเศษส่วนของทั้งหมดบวกค่าคงที่ ตั้งสมการผลรวมเท่ากับทั้งหมดแล้วแก้',
      t(10))
    claim('partial-fractions-cubic', t(11))
    u(RADICAL, 'radical-substitution-equation', 'แทนรากที่ซ้ำกันด้วยตัวแปรเดียว ได้สมการกำลังสอง แล้วแปลงกลับและตรวจโดเมน',
      t(12), ['math.radical_equation_m4'])
    u(POLY, 'rational-expression-monomial', 'แยกตัวประกอบและตัดทอนนิพจน์ตรรกยะหลายชั้นให้เหลือเอกนาม แล้วอ่านเลขชี้กำลัง',
      t(13), note=INCOMPLETE)
    u(SYSTEMS, 'two-price-system-discount', 'ตั้งระบบสมการราคาสองชนิดจากใบเสร็จสองใบ โดยปรับราคาตามส่วนลดที่ใช้เฉพาะบางกรณี',
      t(14), ['math.system_two_prices_m3'])
    claim('factor-theorem-unknowns', t(15), ['math.polynomial_unknown_coefficients_m4'])
    u(RADICAL, 'compare-roots-by-powers', 'เปรียบเทียบ a^(1/m) กับ b^(1/n) โดยยกกำลังด้วย ค.ร.น. ของ m, n',
      t(16))
    u(SYSTEMS, 'land-units-percent', 'แปลงหน่วยพื้นที่ไทย (ไร่ ตารางวา ตารางเมตร) แล้วใช้ร้อยละและอัตราต่อพื้นที่',
      t(17))
    u(SPREAD, 'mean-adjust-total', 'ค่าเฉลี่ยคูณจำนวนเป็นผลรวม ใช้ผลรวมก่อนและหลังเปลี่ยนข้อมูลหาค่าที่ต้องเพิ่ม',
      t(18), ['math.mean_word_m6'], note='สมมติคนขาดสอบได้ 0 คะแนน')
    claim('two-observer-elevation', t(19), ['math.two_angle_height_m5'])
    claim('sd-consecutive-integers', t(20), ['math.standard_deviation'])
    u(GEOM, 'isosceles-area-trig', 'ใช้พื้นที่ ½ab sin C ของสามเหลี่ยมหน้าจั่วเพื่อเทียบพื้นที่ของสามเหลี่ยมที่มีด้านเท่ากัน',
      t(21), note='โจทย์และรูปขัดกันเอง')
    u(ABS, 'absolute-value-statements', 'ตรวจข้อความเกี่ยวกับค่าสัมบูรณ์และอสมการด้วยกรณีศูนย์และจำนวนลบ',
      t(22), ['math.absolute_value_properties_m4'])
    u(INEQ, 'integer-bounds-inequalities', 'แก้อสมการเชิงเส้นที่มีเศษส่วน แล้วหาจำนวนเต็มที่มากที่สุดหรือน้อยที่สุดในเซตคำตอบ',
      t(23), ['math.inequality_largest_integer_m3'], note='อ่านเครื่องหมายเป็น ≤ เพราะ ≥ ไม่มีจำนวนเต็มมากที่สุด')
    claim('meeting-speed-system', t(24), ['math.system_word_problem'])
    u(SYSTEMS, 'instalment-schedule', 'คิดราคาหลังส่วนลด หักยอดผ่อนแต่ละปีตามอัตราที่ลดลง แล้วแบ่งยอดคงเหลือ',
      t(25))
    u(ANALYTIC, 'degenerate-conic-factor', 'แยกตัวประกอบสมการกำลังสองสองตัวแปรเป็นผลคูณของเส้นตรงสองเส้น แล้วเทียบความชัน',
      t(26))
    u(CIRCLE, 'nested-tangent-circles', 'วงกลมที่สัมผัสกันภายในที่จุดเดียว ใช้รัศมีและคอร์ดที่สัมผัสวงกลมในหาความยาว',
      t(27), note=INCOMPLETE)
    u(COUNT, 'subset-sum-threshold-count', 'นับเซตย่อยที่ผลรวมเกินเกณฑ์ โดยบังคับสมาชิกที่ต้องมีหรือห้ามมี แล้วนับกรณีที่เหลือ',
      t(28))
    u(RADICAL, 'compare-radicals-infinite-nest', 'ประเมินค่ากรณฑ์ซ้อนและรากซ้อนไม่รู้จบ (c² = 3c) แล้วเรียงลำดับส่วนกลับ',
      t(29), ['math.radical_equation_m4'])
    u(SOLIDS, 'stacked-blocks-volume', 'นับจำนวนก้อนในรูปสามมิติแล้วคูณปริมาตรก้อนเดียว',
      t(30), note='นับก้อนจากรูปไม่ได้แน่นอน จึงไม่มีคำตอบ')
    u(TRIG, 'reciprocal-trig-ratios', 'ใช้ความสัมพันธ์ sec, csc, cot ในสามเหลี่ยมมุมฉากหามุม แล้วคำนวณนิพจน์',
      t(31), ['math.right_triangle_relations_m5'])
    u(ANALYTIC, 'reflection-polygon-area', 'หาพิกัดจุดจากการสะท้อนต่อเนื่อง แล้วหาพื้นที่รูปหลายเหลี่ยมด้วยสูตรเชือกผูกรองเท้า',
      t(32), ['math.reflect_point'], note='ไฟล์พิมพ์ E ซ้ำ อ่านจุดที่สองเป็น D')
    u(POLY, 'integer-part-division', 'เขียนตัวตั้งเป็นผลคูณของตัวหารบวกเศษ แล้วหาส่วนที่เป็นจำนวนเต็มของผลหาร',
      t(33))
    u(FUNC, 'additive-multiplicative-inverse', 'อินเวอร์สการบวกให้ a + b = 0 อินเวอร์สการคูณให้ cd = 1 แทนในนิพจน์',
      t(34), note=INCOMPLETE)
    claim('linear-cost-model', t(35))
    claim('grouped-mean-unknown-frequency', t(36), ['math.mean_from_frequency_m2'])
    u(SIMILAR, 'similar-right-triangles-parallel', 'เส้นขนานตัดเส้นตรงสองเส้นให้สามเหลี่ยมคล้าย ใช้อัตราส่วนด้านและพื้นที่',
      t(37, 38), ['math.similar_triangle_picture_m3', 'math.similar_ratio_area'])
    u(PROB, 'pair-sum-prime-probability', 'นับคู่ที่ผลรวมเป็นจำนวนเฉพาะ แล้วเทียบการหยิบพร้อมกันกับการหยิบทีละใบไม่ใส่คืน',
      t(39), ['math.probability_without_replacement_m5'])
    UNITS['pair-sum-prime-probability']['sources'].append({'sheet': TU69_SHEET, 'item': 39})
    u(CIRCLE, 'intersecting-chords-power', 'คอร์ดตัดกันที่ P: PA·PB = PC·PD = r² − OP²',
      t(40), note=INCOMPLETE)
    claim('tangent-diameter-angles', t(41), ['math.tangent_chord_angle_m3'])
    u(COUNT, 'triple-count-constraint', 'นับสามสิ่งอันดับจำนวนเต็มบวกที่สอดคล้องกับสมการและอสมการเชิงเส้น',
      t(42), note=INCOMPLETE)
    u(ANALYTIC, 'coordinate-region-area', 'หาพื้นที่บริเวณบนระนาบพิกัดจากจุดตัดของเส้นตรง วงกลม หรือพาราโบลา',
      t(43, 45), note=INCOMPLETE)
    u(SOLIDS, 'cone-from-sector', 'ความยาวส่วนโค้งของเซกเตอร์เป็นเส้นรอบวงฐานกรวย รัศมีเซกเตอร์เป็นสูงเอียง ใช้เทียบปริมาตร',
      t(44), ['math.cone_volume_from_slant_m3'])
    u(ANALYTIC, 'point-in-triangle-lines', 'หาจุดตัดของเส้นตรงสามเส้นเป็นจุดยอดสามเหลี่ยม แล้วตรวจว่าจุดอยู่ด้านเดียวกับจุดยอดตรงข้ามของทุกด้านหรือไม่',
      t(46), ['math.lines_meet_m4'])


def mwit69():
    t = lambda *ns: [MWIT69 + str(n) for n in ns]
    claim('linear-cost-model', t(1))
    u(SOLIDS, 'tiling-cost-estimate', 'หาพื้นที่ผิวที่ต้องปู (พื้นเอียงและผนัง) เผื่อร้อยละ แล้วเทียบราคากล่องและส่วนลดของร้านสองร้าน',
      t(4), note='ต้องสมมติว่าปูพื้นเอียงและผนังทั้งสี่ด้าน')
    u(FUNC, 'task-scheduling', 'จัดลำดับงานที่มีเวลาและเงื่อนไขก่อนหลังให้เสร็จภายในเวลาที่กำหนด',
      t(5), note='ข้อเชิงวิจารณญาณ ไม่มีคำตอบตายตัว')


def main():
    tu65()
    tu64()
    tu69()
    mwit69()
    posn_known()
    posn2569()
    for (slug, topic, level), units in FILES.items():
        if slug.startswith('entrance-posn-'):
            # one file per (year, topic): the registry topic is the file's topic
            index = sorted({t for (sl, t, _) in FILES if sl == slug}).index(topic)
            slug = f'{slug}-{index + 1:02d}'
        write_topic(ROOT / f'otk/knowledge/math/{slug}.json', topic, units, level)


if __name__ == '__main__':
    main()
