"""Preserve prior coverage while claiming a complete Primary 4 time/models paper."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCE='mathematics/level/primary-4/4540-4-2567-2-2.pdf'


def main():
    files,claims={},[]
    def add(slug,topic,key,numbers,covered=(),title=None,statement=None):
        path=ROOT/f'otk/knowledge/math/primary4-{slug}.json'
        if path not in files:
            units=json.loads(path.read_text())['units'] if path.exists() else []
            files[path]=(topic,units)
        units=files[path][1]
        uid='math.primary4.'+key
        unit=next((u for u in units if u['id']==uid),None)
        if unit is None:
            assert title and statement
            unit=dict(id=uid,kind='procedure',title=title,statement=statement,
                      steps=['ระบุข้อมูลและเงื่อนไข',statement,'ตรวจความสัมพันธ์และหน่วยของคำตอบ'],
                      sources=[],covered_by=[])
            units.append(unit)
        for n in numbers:
            claims.append(n)
            source={'sheet':SOURCE,'item':n}
            if source not in unit['sources']:
                unit['sources'].append(source)
        for key in covered:
            if 'math.'+key not in unit['covered_by']:
                unit['covered_by'].append('math.'+key)

    add('time','เวลา','clock-read',[1],['clock_read_p2'],
        'อ่านเวลาเป็นชั่วโมงและนาทีจากหน้าปัด','อ่านเข็มยาวเป็นจำนวนนาทีและเข็มสั้นเป็นชั่วโมงที่ผ่านแล้ว โดยไม่ใช้เข็มวินาที')
    add('time','เวลา','clock-hands-from-minutes',[2],['clock_hands_from_minutes_p4'],
        'ระบุตำแหน่งเข็มเมื่อกำหนดเวลา','หารนาทีด้วยห้าเพื่อหาเลขที่เข็มยาวชี้ เข็มสั้นอยู่ระหว่างชั่วโมงที่ผ่านกับชั่วโมงถัดไป')
    add('time','เวลา','inclusive-date-weeks',[3],['inclusive_date_weeks_p4'],
        'นับสัปดาห์จากช่วงวันที่แบบรวมปลายทั้งสอง','หาผลต่างวันแล้วเพิ่มหนึ่งเพื่อรวมวันเริ่มต้น ก่อนหารด้วยเจ็ดเมื่อถามจำนวนสัปดาห์')
    add('time','เวลา','fractional-year-weeks',[4],['fractional_year_weeks_p4'],
        'แปลงปีและเศษส่วนเป็นสัปดาห์ตามเกณฑ์','เมื่อกำหนดเกณฑ์หนึ่งปีเป็นห้าสิบสองสัปดาห์ ให้คูณทั้งจำนวนเต็มและเศษส่วนของปีด้วยเกณฑ์นี้ ไม่ถือเป็นระยะปฏิทินที่แน่นอน')
    add('time','เวลา','minute-duration-conversion',[5],['time_units_p4','minutes_to_hours_p3'],
        'แปลงนาทีเป็นชั่วโมงกับนาทีที่เหลือ','แบ่งกลุ่มละหกสิบนาทีเป็นชั่วโมง แล้วเก็บเศษเป็นนาที')
    add('time','เวลา','approximate-months-days',[6],['approximate_months_days_p4'],
        'แปลงวันเป็นเดือนและวันตามเกณฑ์สามสิบวัน','เมื่อกำหนดหนึ่งเดือนเท่ากับสามสิบวัน ให้หารด้วยสามสิบแล้วอ่านผลหารเป็นเดือนและเศษเป็นวัน')
    add('time','เวลา','schedule-duration',[7,8],['schedule_duration_p4'],
        'หาระยะเวลาจากรายการในตาราง','เลือกรายการที่ถาม แปลงเวลาเริ่มและจบเป็นนาทีบนวันเดียวกันก่อนลบ แล้วเขียนคำตอบตามหน่วยที่ถาม')
    add('time','เวลา','departure-cutoff',[9],['departure_cutoff_p4'],
        'เลือกเที่ยวรถที่ออกก่อนเวลาตัดสิน','อ่านคอลัมน์เวลาออกและเปรียบเทียบแบบน้อยกว่า ไม่รวมเที่ยวที่ออกตรงเวลาเกณฑ์และไม่ใช้เวลาถึงแทน')
    add('time','เวลา','elapsed-clock-time',[10])
    add('multi-step','โจทย์ปัญหาระคน','add-sub-sentence',[11,12],['add_sub_sentence_p4'],
        'เลือกประโยคสัญลักษณ์ของการลดสองครั้งหรือเปรียบเทียบต่อกัน','ระบุความหมายของการเพิ่มและลดแต่ละขั้น จัดวงเล็บให้ลำดับตรงกับเรื่องแล้วเลือกประโยคที่ให้คำตอบ')
    add('multi-step','โจทย์ปัญหาระคน','remaining-share-sentence',[13],['remaining_share_sentence_p4'],
        'หักของเสียก่อนหารจำนวนผู้รับ','ลบจำนวนของเสียจากทั้งหมดก่อนหารจำนวนคนเพื่อแบ่งของดีเท่า ๆ กัน')
    add('multi-step','โจทย์ปัญหาระคน','product-plus-fee',[14,16],['two_step_sentence_p4','two_step_word_problem_p4'],
        'รวมค่าใช้จ่ายซ้ำกับค่าใช้จ่ายครั้งเดียว','คูณราคาต่อครั้งด้วยจำนวนครั้งก่อนบวกค่าธรรมเนียมหรือค่าภาชนะที่จ่ายครั้งเดียว')
    add('multi-step','โจทย์ปัญหาระคน','quotient-then-add-sentence',[15],['quotient_then_add_sentence_p4'],
        'หาปริมาณจากเงินจ่ายก่อนรวมอีกชนิด','หารเงินจ่ายด้วยราคาต่อหน่วยเพื่อหาปริมาณชนิดแรก แล้วบวกปริมาณอีกชนิดในหน่วยเดียวกัน')
    add('multi-step','โจทย์ปัญหาระคน','needed-total-less-shortfall',[17],['two_step_sentence_p4','two_step_word_problem_p4'],
        'ย้อนหาของเดิมจากเป้าหมายและจำนวนที่ขาด','คูณจำนวนกลุ่มกับจำนวนต่อกลุ่มเพื่อหาเป้าหมายทั้งหมด แล้วลบจำนวนที่ขาดเพื่อหาของเดิม')
    add('multi-step','โจทย์ปัญหาระคน','pack-unit-price-sentence',[18],['pack_unit_price_sentence_p4'],
        'หาราคาต่อลังจากจำนวนชิ้นและยอดขาย','หารจำนวนชิ้นทั้งหมดด้วยจำนวนต่อลังเพื่อหาจำนวนลัง แล้วหารยอดขายด้วยจำนวนลัง')
    add('multi-step','โจทย์ปัญหาระคน','related-story-for-sentence',[19,20],['related_story_for_sentence_p4'],
        'เลือกเรื่องที่ตรงกับประโยคของจำนวนสัมพันธ์กัน','แปลผลบวกที่มีจำนวนเดิมซ้ำหรือการลบก่อนแบ่งให้ตรงกับเรื่อง แล้วตรวจว่าคำถามถามปริมาณเดียวกับประโยค')
    assert sorted(claims)==list(range(1,21))
    for path,(topic,units) in files.items():
        write_topic(path,topic,units,'ป.4')


if __name__=='__main__':
    main()
