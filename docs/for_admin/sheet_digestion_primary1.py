"""Idempotent Primary 1 coverage map for the second text-layer-first batch."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S1 = 'mathematics/level/primary-1/3999-1-2564-1-3.pdf'
S2 = 'mathematics/level/primary-1/4017-1-2567-2-3.pdf'
S3 = 'mathematics/level/primary-1/4020-1-2567-2-3.pdf'


def unit(key, title, statement, sources, covered):
    return dict(id='math.primary1.' + key, kind='procedure', title=title, statement=statement,
                steps=['ระบุข้อมูลและสิ่งที่โจทย์ถาม', statement, 'ตรวจคำตอบและหน่วยกับเรื่องราว'],
                sources=[{'sheet': sheet, 'item': n} for sheet, ns in sources for n in ns],
                covered_by=['math.' + k for k in covered])



def write_topic(path, topic, units, level='ป.1'):
    """Upsert this batch while preserving later units and additional coverage."""
    raw = json.loads(path.read_text()) if path.exists() else {}
    if raw and (raw['subject'], raw['topic'], raw['level']) != ('คณิตศาสตร์', topic, level):
        raise ValueError(f'Conflicting topic metadata: {path}')
    known = {u['id']: u for u in raw.get('units', [])}
    for u in units:
        previous = known.get(u['id'], {})
        merged = {**previous, **u}
        for field in ('sources', 'covered_by'):
            values = list(previous.get(field, []))
            for value in u[field]:
                if value not in values:
                    values.append(value)
            merged[field] = values
        known[u['id']] = merged
    raw.update(subject='คณิตศาสตร์', topic=topic, level=level, units=list(known.values()))
    path.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + '\n')


def main():
    files = {
        'word-problems': ('โจทย์ปัญหา', [
            unit('combine', 'รวมจำนวนหรือเพิ่มจำนวน',
                 'บวกจำนวนที่นำมารวมกันหรือจำนวนที่เพิ่มมา เขียนประโยคสัญลักษณ์และวิธีทำเมื่อโจทย์ต้องการ',
                 [(S1, [1, 3, 5, 6, 7, 8, 9, 10, 21]), (S2, [1, 2, 3]), (S3, [1, 2, 4])],
                 ['add_word_problem', 'word_problem_number_sentence']),
            unit('dozen-change', 'ใช้จำนวนหนึ่งโหลก่อนเพิ่มหรือลด',
                 'หนึ่งโหลมี 12 ชิ้น แทนจำนวนด้วย 12 ก่อนบวกจำนวนที่ได้เพิ่มหรือลบจำนวนที่ใช้ไป',
                 [(S1, [2, 15])], ['dozen_change_p1']),
            unit('equal-total', 'รวมสองกลุ่มที่มีจำนวนเท่ากัน',
                 'เมื่อสองกลุ่มมีเท่ากัน ใช้จำนวนที่ทราบแทนอีกกลุ่มแล้วบวกสองจำนวนนั้น',
                 [(S1, [4]), (S2, [7]), (S3, [8])], ['equal_amount_total_p1']),
            unit('comparison-amount', 'หาจำนวนจากความสัมพันธ์มากกว่าน้อยกว่า',
                 'ระบุจำนวนมากและจำนวนน้อยก่อน ใช้ จำนวนมาก = จำนวนน้อย + ส่วนต่าง หาจำนวนที่โจทย์ถาม',
                 [(S2, [4, 6, 8, 9, 15]), (S3, [3, 5, 15, 16])], ['compare_word_problem', 'age_word_p1']),
            unit('remaining', 'จำนวนที่เหลือหลังใช้ไป', 'ลบจำนวนที่ใช้ แจก ขาย หรือหายไปออกจากจำนวนเริ่มต้น',
                 [(S1, [11, 12, 16, 17, 18, 19, 20]), (S2, [11, 18]), (S3, [11, 12])], ['sub_word_problem']),
            unit('missing-part', 'หาจำนวนเริ่มต้นหรือส่วนที่ไม่ทราบ',
                 'เขียนความสัมพันธ์ระหว่างจำนวนทั้งหมดกับส่วนต่าง ๆ แล้วใช้การบวกหรือลบหาจำนวนที่ขาด พร้อมเขียนประโยคสัญลักษณ์เมื่อโจทย์ต้องการ',
                 [(S1, [14]), (S2, [5, 10, 13, 17, 21]), (S3, [6, 7, 13, 19])],
                 ['missing_part_word_problem', 'word_problem_number_sentence']),
            unit('difference', 'หาส่วนต่างของสองจำนวน', 'ลบจำนวนน้อยออกจากจำนวนมากเพื่อหาผลต่างหรือจำนวนที่ยังต้องเพิ่ม',
                 [(S1, [13]), (S2, [12, 16]), (S3, [14, 18])], ['compare_word_problem']),
            unit('more-needed', 'หาเงินที่ยังขาด', 'ลบเงินที่มีออกจากราคาของที่ต้องการซื้อ',
                 [(S2, [14]), (S3, [17])], ['more_needed_p1', 'missing_part_word_problem']),
            unit('purchase-balance', 'หาสินค้าจากเงินที่เหลือ', 'ลบเงินที่เหลือออกจากเงินเริ่มต้น แล้วเทียบกับราคาสินค้าเพื่อหาของที่ซื้อ',
                 [(S3, [20])], ['purchase_from_balance_p1']),
            unit('budget-conclusion', 'สรุปเงินพอ ขาด หรือเหลือ', 'เปรียบเทียบเงินที่มีกับราคา แล้วเลือกข้อความที่บอกว่าเงินพอดี ขาด หรือเหลือ พร้อมจำนวนเงินที่ถูกต้อง',
                 [(S2, [20])], ['budget_conclusion_p1']),
            unit('spending-comparison', 'เปรียบเทียบค่าใช้จ่ายรวม', 'บวกราคาของสองอย่างที่แต่ละคนซื้อก่อน แล้วเปรียบเทียบผลรวมของทุกคน',
                 [(S3, [10])], ['compare_spending_totals_p1']),
            unit('calendar-date', 'นับวันที่ภายในเดือนเดียวกัน', 'หาว่าต้องนับวันไปข้างหน้าหรือย้อนกลับ แล้วบวกหรือลบจำนวนวันที่ผ่านไป โดยไม่รวมวันเริ่มต้นเป็นวันที่ผ่านไป',
                 [(S3, [9])], ['calendar_date_shift_p1']),
        ]),
        'measurement': ('การวัด', [
            unit('length-statement', 'แปลผลต่างความยาวเป็นข้อความ', 'เปรียบเทียบความยาว หาผลต่าง และระบุให้ถูกว่าสิ่งใดยาวกว่าหรือสั้นกว่าอีกสิ่ง',
                 [(S2, [19])], ['length_comparison_statement_p1']),
        ]),
    }
    claims = [(s['sheet'], s['item']) for _, units in files.values() for u in units for s in u['sources']]
    expected = [(sheet, n) for sheet, count in ((S1, 21), (S2, 21), (S3, 20)) for n in range(1, count + 1)]
    assert len(claims) == len(set(claims)) == 62
    assert set(claims) == set(expected)
    for slug, (topic, units) in files.items():
        p = ROOT / f'otk/knowledge/math/primary1-{slug}.json'
        write_topic(p, topic, units)


if __name__ == '__main__':
    main()
