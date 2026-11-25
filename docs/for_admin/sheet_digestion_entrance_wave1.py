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

# (file slug, registry topic, level) -> units
FILES = {}


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


def tu65():
    t = lambda *ns: [TU65 + str(n) for n in ns]
    u(TRIG, 'trig-sum-to-product', 'ยกกำลังสอง sin A + cos A เพื่อหา sin A cos A แล้วเขียนนิพจน์ตรีโกณมิติด้วย sin A cos A',
      t(1))
    u(POLY, 'conjugate-irrational-root', 'พหุนามสัมประสิทธิ์ตรรกยะที่มีราก p + √q มีราก p − √q ด้วย จึงมีตัวประกอบกำลังสองตรรกยะ ใช้หาสัมประสิทธิ์และตัวประกอบอื่น',
      t(2))
    u(RATIONAL, 'partial-fractions-cubic', 'แยกเศษส่วนย่อยที่ตัวส่วนเป็นผลต่างกำลังสาม แล้วเทียบสัมประสิทธิ์',
      t(3), ['math.partial_fractions_m4'])
    u(POLY, 'cubic-vieta-squared-roots', 'ใช้ความสัมพันธ์รากกับสัมประสิทธิ์ของพหุนามดีกรีสามสร้างสมการที่มีรากเป็นกำลังสองของรากเดิม',
      t(4), note='ชุดโจทย์ที่มีอยู่ฝึกเฉพาะสมการกำลังสอง')
    u(GEOM, 'rectangle-square-area-split', 'ตั้งตัวแปรความยาวด้าน ใช้พีทาโกรัสและพื้นที่รูปที่แบ่งในสี่เหลี่ยมผืนผ้าสร้างสมการจำนวนเต็ม',
      t(5))
    u(GEOM, 'square-fifteen-degree-point', 'ใช้ความสมมาตรและสามเหลี่ยมหน้าจั่วในสี่เหลี่ยมจัตุรัสที่มีมุม 15° เพื่อพิสูจน์สามเหลี่ยมด้านเท่าและหามุม',
      t(6))
    u(SYSTEMS, 'linear-cost-model', 'ค่าใช้จ่าย = ค่าคงที่ + อัตรา × จำนวน หาค่าคงที่และอัตราจากข้อมูลสองชุดแล้วคำนวณค่าอื่น',
      t(7), ['math.system_word_problem'])
    u(POLY, 'power-remainder-and-expansion-coefficient', 'หาเศษจากการหารผลบวกเลขยกกำลังโดยใช้วัฏจักรเศษ และหาสัมประสิทธิ์จากการกระจายผลคูณทวินาม',
      t(8), ['math.remainder_arithmetic_m4', 'math.binomial_apply_m5'])
    u(RATIONAL, 'work-rate-people', 'แปลงงานเป็นอัตราต่อวันของแต่ละคน ตั้งสมการจากงานที่ทำร่วมกันแล้วหาเวลาของกลุ่มใหม่',
      t(9, 21), ['math.joint_worker_time_m3', 'math.work_together_m4'])
    u(ANALYTIC, 'equilateral-on-parabola', 'จุดยอดสามเหลี่ยมด้านเท่าที่มีจุดยอดอยู่ที่จุดยอดพาราโบลาจะสมมาตรกับแกน ใช้ความชัน tan 60° หาจุดบนพาราโบลา',
      t(10))
    u(SERIES, 'alternating-square-sum', 'จับคู่พจน์ (2k − 1)² − (2k)² = −(4k − 1) แล้วรวมเป็นอนุกรมเลขคณิต หรือใช้ผลบวก Σi',
      t(11))
    u(SYSTEMS, 'train-passing', 'รถไฟพ้นกันเมื่อวิ่งเป็นระยะเท่าความยาวรวม ใช้ความเร็วสัมพัทธ์ (ผลบวกเมื่อสวนกัน ผลต่างเมื่อตามกัน)',
      t(12))
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
      t(19))
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
      t(29))
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


def main():
    tu65()
    for (slug, topic, level), units in FILES.items():
        write_topic(ROOT / f'otk/knowledge/math/{slug}.json', topic, units, level)


if __name__ == '__main__':
    main()
