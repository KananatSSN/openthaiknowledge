"""Idempotently claim three complete Primary 1–3 comprehension papers."""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCES = {1: 'mathematics/level/primary-1/3994-1-2564-2-2.pdf',
           2: 'mathematics/level/primary-2/4158-2-2564-1-2.pdf',
           3: 'mathematics/level/primary-3/4358-3-2567-2-2.pdf'}


def main():
    files, claims = {}, []

    def topic(grade, slug, name):
        path = ROOT / f'otk/knowledge/math/primary{grade}-{slug}.json'
        if path not in files:
            raw = json.loads(path.read_text()) if path.exists() else {'units': []}
            files[path] = (name, raw['units'], f'ป.{grade}')
        return files[path][1]

    def add(grade, slug, name, key, numbers, covered=(), title=None, statement=None):
        units = topic(grade, slug, name)
        uid = f'math.primary{grade}.{key}'
        target = next((u for u in units if u['id'] == uid), None)
        if target is None:
            assert title and statement, uid
            target = dict(id=uid, kind='procedure', title=title, statement=statement,
                          steps=['ระบุข้อมูลและสิ่งที่โจทย์ถาม', statement, 'ตรวจคำตอบกับข้อมูลทั้งหมด'],
                          sources=[], covered_by=[])
            units.append(target)
        for n in numbers:
            source = {'sheet': SOURCES[grade], 'item': n}
            claims.append((SOURCES[grade], n))
            if source not in target['sources']:
                target['sources'].append(source)
        for key in covered:
            if 'math.' + key not in target['covered_by']:
                target['covered_by'].append('math.' + key)

    add(1,'measurement','การวัด','length-statement',[1,2],['length_order_names_p1','min_max_of_four'])
    add(1,'measurement','การวัด','order-measured-lengths',[3,4],['length_order_names_p1'])
    add(1,'measurement','การวัด','measuring-tool',[5,6])
    add(1,'measurement','การวัด','balance-unit-weight',[7,8])
    add(1,'measurement','การวัด','balance-weight-comparison',[9,10])
    add(1,'measurement','การวัด','read-scale-kg-khit',[11,12])
    add(1,'comparing-numbers','การเปรียบเทียบ','ordering',[13,14])
    add(1,'counting','การนับ','expanded-form-judgement',[15],['expanded_form_judgement_p1'],
        'ตรวจรูปกระจายตามหลักสิบและหลักหน่วย','ตรวจว่าพจน์แรกเป็นค่าหลักสิบและพจน์ที่สองเป็นค่าหลักหน่วย แม้การแยกผลบวกแบบอื่นจะให้จำนวนเดียวกัน')
    add(1,'counting','การนับ','digit-place-value',[16],['place_value_statement_p1'])
    add(1,'comparing-numbers','การเปรียบเทียบ','false-sum-comparison',[17])
    add(1,'comparing-numbers','การเปรียบเทียบ','numeric-comparison',[18])
    add(1,'pictograph','แผนภูมิรูปภาพ','pictograph-read',[19,20],['pictograph','count_objects_p1'],
        'อ่านจำนวนรายการจากแผนภูมิรูปภาพ','นับรูปในรายการที่ถามแล้วคูณค่าต่อรูปที่กำหนด โดยนับเฉพาะรายการนั้น')

    add(2,'time','เวลา','clock-period-24h',[1,7],['clock_period_to_24h_p2','clock_read_p2'],
        'ใช้ช่วงวันอ่านเวลาแบบยี่สิบสี่ชั่วโมง','อ่านเข็มชั่วโมงและนาที แล้วใช้ช่วงก่อนหรือหลังเที่ยงวันกำหนดชั่วโมงในระบบยี่สิบสี่ชั่วโมง')
    add(2,'time','เวลา','colloquial-clock',[2,6,8],['colloquial_clock_p2'],
        'บอกเวลาเป็นภาษาพูด','อ่านตำแหน่งเข็มและช่วงวัน แปลงชั่วโมงเป็นคำบอกเวลาตี โมง หรือทุ่ม แล้วอ่านนาทีให้ถูกต้อง')
    add(2,'time','เวลา','clock-hands-from-hour',[3,4,5],['clock_hands_from_hour_p2'],
        'ระบุตำแหน่งเข็มจากชั่วโมงตรง','เมื่อเป็นชั่วโมงตรงเข็มยาวชี้สิบสอง เข็มสั้นชี้ชั่วโมงบนหน้าปัดสิบสองชั่วโมง')
    add(2,'time','เวลา','calendar-event-month',[9,11],['calendar_event_month_p2'],
        'ระบุเดือนของกิจกรรมในปฏิทิน','หาวันที่ของกิจกรรมแล้วแปลงเลขเดือนเป็นชื่อเดือน')
    add(2,'time','เวลา','daily-schedule-activity',[10],['daily_schedule_activity_p2'],
        'เลือกกิจกรรมตามช่วงเวลาในวัน','อ่านเวลาและเลือกกิจกรรมที่สอดคล้องกับเวลาตามตารางหรือบริบทชีวิตประจำวัน')
    add(2,'time','เวลา','calendar-month-order',[12,13,14],['months_p2'],
        'อ่านลำดับเดือนในหนึ่งปี','เรียงเดือนตั้งแต่มกราคมถึงธันวาคม ระบุลำดับหรือเดือนที่อยู่ระหว่างเดือนที่กำหนด')
    add(2,'shapes','รูปเรขาคณิต','polygon-picture',[15,16])
    add(2,'patterns','แบบรูป','changing-attribute',[17],['pattern_changing_attribute_p2'],
        'จำแนกลักษณะที่เปลี่ยนในแบบรูป','เปรียบเทียบขนาด สี และรูปร่างแยกกัน เพื่อหาลักษณะที่ใช้สร้างแบบรูปซ้ำโดยลักษณะอื่นคงเดิม')
    add(2,'patterns','แบบรูป','repeating-shape-next',[18],['repeating_pattern_p2'],
        'หารูปถัดไปในแบบรูปซ้ำ','หาหน่วยการซ้ำแล้วต่อรูปตามตำแหน่งในหน่วยนั้น')
    add(2,'shapes','รูปเรขาคณิต','solid-identification',[19,20])

    add(3,'money','เงิน','denomination-total',[1,2],['money_purse_comparison_p3','baht_satang_p3'],
        'รวมเงินจากธนบัตรและเหรียญ','คูณมูลค่าต่อใบหรือเหรียญด้วยจำนวน แล้วรวมเป็นบาทและสตางค์โดยร้อยสตางค์เท่ากับหนึ่งบาท')
    add(3,'money','เงิน','odd-purse',[3],['money_odd_purse_p3'],
        'หากลุ่มเงินที่มีค่าต่างจากกลุ่มอื่น','คำนวณค่าเงินทุกกลุ่มเป็นหน่วยเดียวกัน แล้วหากลุ่มที่ไม่เท่ากับอีกสามกลุ่ม')
    add(3,'money','เงิน','purse-comparison',[4,5],['money_purse_comparison_p3'],
        'เปรียบเทียบจำนวนเงินหลายรูปแบบ','รวมมูลค่าธนบัตรและเหรียญให้ครบทุกชนิดก่อนเรียงลำดับหรือเลือกเงินมากที่สุดหรือน้อยที่สุด')
    add(3,'money','เงิน','satang-ledger-query',[6,7,8,9],['satang_ledger_query_p3'],
        'วิเคราะห์รายรับรายจ่ายที่มีสตางค์','จำแนกรายรับรายจ่ายตามวันและผู้ให้เงิน รวมเฉพาะแถวที่ถาม แล้วหาผลต่างหรือเงินคงเหลือตามโจทย์')
    add(3,'patterns','แบบรูป','constant-step-next',[10,14],['pattern_next_p3'],
        'หาจำนวนถัดไปเมื่อเพิ่มหรือลดเท่ากัน','หาผลต่างระหว่างพจน์ติดกัน แล้วบวกผลต่างนั้นกับพจน์สุดท้าย')
    add(3,'patterns','แบบรูป','constant-step-index',[11,15],['pattern_far_term_p3'],
        'หาพจน์ในลำดับที่กำหนด','คูณจำนวนก้าวจากพจน์แรกด้วยผลต่างคงที่ แล้วรวมกับพจน์แรกโดยคงเครื่องหมายของผลต่าง')
    add(3,'patterns','แบบรูป','constant-step-two-missing',[12,16],['pattern_two_missing_p3'],
        'เติมพจน์ที่ขาดสองตำแหน่ง','ตรวจผลต่างคงที่แล้วนับก้าวให้ถูกทุกตำแหน่งที่ขาด')
    add(3,'patterns','แบบรูป','constant-step-first',[13,17],['number_pattern_p3'],
        'ย้อนหาพจน์แรกของแบบรูป','ลบผลต่างคงที่ออกจากพจน์ที่สองเพื่อย้อนหนึ่งก้าวกลับไปยังพจน์แรก')
    add(3,'multi-step','โจทย์ปัญหาระคน','purchase-sentence-models',[18,19],['purchase_sentence_models_p3'],
        'เลือกประโยคสัญลักษณ์รวมการซื้อหรือแบ่งยอดคงเหลือ','จับคู่ราคากับจำนวนของแต่ละชนิดก่อนรวมผลคูณ หรือหักเงินจ่ายแล้วออกจากราคาแล้วหารจำนวนงวด')
    add(3,'multi-step','โจทย์ปัญหาระคน','balance-after-several',[20],['two_step_sentence_p3'])
    assert len(claims) == len(set(claims)) == 60
    assert set(claims) == {(source,n) for source in SOURCES.values() for n in range(1,21)}
    for path,(name,units,level) in files.items():
        write_topic(path,name,units,level)


if __name__ == '__main__':
    main()
