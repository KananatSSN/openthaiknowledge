"""Append coverage for three word papers and one text-layer comprehension paper."""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
HELPERS = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))
unit, write_topic = HELPERS['unit'], HELPERS['write_topic']
BASE = 'mathematics/level/primary-1/'
A, B, C, D = [BASE + name for name in ('3993-1-2564-2-3.pdf', '4005-1-2565-2-3.pdf',
                                     '4011-1-2565-1-3.pdf', '4021-1-2567-2-2.pdf')]


def main():
    path = ROOT / 'otk/knowledge/math/primary1-word-problems.json'
    old = json.loads(path.read_text())
    existing = {u['id'].removeprefix('math.primary1.'): u for u in old['units']}
    additions = {
        'combine': [(A, [1, 3, 4, 5, 6, 7, 8, 9, 10]), (B, [1, 2, 4, 5, 7]), (C, [1, 2, 3, 4, 5, 6, 7, 9, 10, 21])],
        'remaining': [(A, [11, 12, 14, 19]), (B, [11, 13, 14, 15, 16, 18, 20, 21]), (C, [11, 12, 13, 14, 16, 17, 18, 20])],
        'comparison-amount': [(B, [3, 8, 10]), (C, [8])],
        'difference': [(A, [15, 17, 18, 20, 21]), (B, [12])],
        'missing-part': [(A, [13, 16]), (B, [6, 17, 19]), (C, [15, 19])],
    }
    added_claims = []
    for key, sources in additions.items():
        u = existing[key]
        for sheet, numbers in sources:
            for n in numbers:
                source = {'sheet': sheet, 'item': n}
                added_claims.append((sheet, n))
                if source not in u['sources']:
                    u['sources'].append(source)
    # A new written-response comparison also exercises symbolic modelling.
    key = 'math.word_problem_number_sentence'
    for suffix in ('remaining', 'difference'):
        if key not in existing[suffix]['covered_by']:
            existing[suffix]['covered_by'].append(key)
    new_word = [
        unit('multi-dozen', 'รวมของหลายโหลและของที่เพิ่ม', 'แทนแต่ละโหลด้วย 12 แล้วบวกจำนวนของทุกโหลและของที่เพิ่มเข้ามา',
             [(A, [2])], ['multi_dozen_total_p1']),
        unit('dozen-comparison', 'ใช้หนึ่งโหลเป็นผลต่างของสองจำนวน', 'แปลงส่วนต่างหนึ่งโหลเป็น 12 แล้วใช้ความสัมพันธ์จำนวนมากกับจำนวนน้อยหาจำนวนที่ไม่ทราบ',
             [(B, [9])], ['dozen_change_p1', 'compare_word_problem']),
        unit('sentence-to-story', 'เลือกเรื่องราวจากประโยคสัญลักษณ์', 'อ่านจำนวนและเครื่องหมายในประโยคสัญลักษณ์ แล้วเลือกเรื่องที่มีจำนวนและความสัมพันธ์ตรงกัน โดยดูสิ่งที่โจทย์ถามด้วย',
             [(D, [11, 12, 15, 16])], ['story_matches_sentence_p1']),
        unit('story-to-sentence', 'เลือกประโยคสัญลักษณ์จากเรื่องราว', 'ระบุจำนวนที่ทราบและสิ่งที่ต้องการหา แล้วเลือกประโยคสัญลักษณ์ที่แทนความสัมพันธ์นั้นได้',
             [(D, [13, 14, 17, 18])], ['word_problem_number_sentence', 'compare_word_problem']),
    ]
    files = {
        'counting': ('การนับ', [
            unit('ordinal-picture', 'บอกลำดับจากภาพ', 'ระบุจุดเริ่มต้นที่กำหนดแล้วนับลำดับทีละหนึ่งจนถึงตำแหน่งที่ถาม',
                 [(D, [1])], ['ordinal_position_p1']),
            unit('picture-thai-cardinality', 'เทียบจำนวนในภาพกับตัวเลขไทย', 'อ่านตัวเลขไทยแล้วนับจำนวนสิ่งของของแต่ละภาพเพื่อเลือกภาพที่มีจำนวนเท่ากัน',
                 [(D, [5])], ['count_objects_p1', 'equivalent_number_forms_p1']),
            unit('equivalent-forms', 'ตรวจตัวเลขและคำอ่านว่าแทนจำนวนเดียวกัน', 'อ่านค่าของตัวเลขฮินดูอารบิก ตัวเลขไทย และคำอ่าน แล้วตรวจว่าทั้งสามค่าเท่ากัน',
                 [(D, [6])], ['equivalent_number_forms_p1']),
        ]),
        'comparing-numbers': ('การเปรียบเทียบ', [
            unit('rank-by-score', 'จัดอันดับตามจำนวน', 'เรียงค่าจากมากไปน้อยก่อน แล้วหาชื่อหรือตัวเลขที่อยู่ในลำดับที่ถาม',
                 [(D, [2])], ['sorted_position_p1', 'compare_who_most_p1']),
            unit('numeric-comparison', 'ตรวจการเปรียบเทียบจำนวนหลายรูปแบบ', 'แปลงภาพ ตัวเลขไทย หรือคำอ่านเป็นจำนวน แล้วตรวจความสัมพันธ์ มากกว่า น้อยกว่า เท่ากับ หรือไม่เท่ากับ ตามคำถาม',
                 [(D, [3, 7, 8])], ['true_comparison_p1', 'compare_groups_p1', 'equivalent_number_forms_p1']),
            unit('compare-sums', 'เปรียบเทียบผลบวกสองข้าง', 'หาค่าของผลบวกแต่ละข้างก่อน แล้วจึงเปรียบเทียบผลลัพธ์ ไม่เปรียบเทียบเฉพาะจำนวนตัวแรก',
                 [(D, [4])], ['compare_sums_p1']),
            unit('ordering', 'ตรวจลำดับและหาจำนวนระหว่างกลาง', 'เรียงจำนวนตามทิศทางที่โจทย์กำหนด และตรวจว่าจำนวนทุกตำแหน่งอยู่ในลำดับนั้น',
                 [(D, [9, 10])], ['order_numbers', 'number_between_p1']),
        ]),
        'plane-shapes': ('เรขาคณิต 2 มิติ', [
            unit('quadrilateral-picture', 'ระบุรูปสี่เหลี่ยมจากภาพ', 'นับด้านตรงของแต่ละรูป รูปที่มีด้านตรงสี่ด้านเป็นรูปสี่เหลี่ยม แม้จะเอียงก็ตาม',
                 [(D, [19])], ['classify_2d_shape', 'shape_corners_p1']),
        ]),
        'solids': ('เรขาคณิต 3 มิติ', [
            unit('cylinder-object', 'ระบุทรงกระบอกจากสิ่งของ', 'พิจารณารูปทรงหลักของสิ่งของ ฐานวงกลมสองด้านที่ขนานกันและผิวข้างโค้งเป็นลักษณะของทรงกระบอก',
                 [(D, [20])], ['solid_objects_p1']),
        ]),
    }
    claims = added_claims + [(s['sheet'], s['item']) for u in new_word for s in u['sources']]
    claims += [(s['sheet'], s['item']) for _, units in files.values() for u in units for s in u['sources']]
    expected = {(sheet, n) for sheet, count in ((A, 21), (B, 21), (C, 21), (D, 20)) for n in range(1, count + 1)}
    assert len(claims) == len(set(claims)) == 83 and set(claims) == expected
    write_topic(path, 'โจทย์ปัญหา', list(existing.values()) + new_word)
    for slug, (topic, units) in files.items():
        write_topic(ROOT / f'otk/knowledge/math/primary1-{slug}.json', topic, units)


if __name__ == '__main__':
    main()
