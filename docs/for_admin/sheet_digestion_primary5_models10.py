"""Preserve prior claims while covering a complete Primary 5 models paper."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCE='mathematics/level/primary-5/4722-5-2567-2-2.pdf'


def main():
    files,claims={},[]
    def add(slug,topic,key,numbers,covered=(),title=None,statement=None):
        path=ROOT/f'otk/knowledge/math/primary5-{slug}.json'
        if path not in files:
            units=json.loads(path.read_text())['units'] if path.exists() else []
            files[path]=(topic,units)
        units=files[path][1]
        uid='math.primary5.'+key
        unit=next((u for u in units if u['id']==uid),None)
        if unit is None:
            assert title and statement
            unit=dict(id=uid,kind='procedure',title=title,statement=statement,
                      steps=['ระบุข้อมูลและฐานที่ใช้คำนวณ',statement,'ตรวจคำตอบด้วยความสัมพันธ์เดิมและหน่วย'],
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

    add('unitary-method','บัญญัติไตรยางศ์','direct-proportion',[1,2,3,4],['proportion_sentence_p5'])
    add('percentages','ร้อยละ','fraction-decimal-to-percent',[5,6],['fraction_decimal_to_percent_p5'],
        'เปลี่ยนเศษส่วนและทศนิยมเป็นร้อยละ','คูณสัดส่วนด้วยหนึ่งร้อยเพื่อเขียนเป็นเปอร์เซ็นต์ โดยคงค่าเท่าเดิม')
    add('percentages','ร้อยละ','percent-of-amount',[7,10],['percent_part_sentence_p5'])
    add('percentages','ร้อยละ','percent-expression-comparison',[8],['percent_expression_comparison_p5'],
        'เปรียบเทียบผลคูณร้อยละที่มีฐานต่างกัน','คำนวณอัตราร้อยละคูณจำนวนฐานของแต่ละตัวเลือกก่อนเปรียบเทียบ ไม่เรียงตามอัตราหรือฐานอย่างเดียว')
    add('percentages','ร้อยละ','find-percent-from-part',[9],['find_percent_p5'],
        'หาร้อยละจากส่วนที่ทราบและทั้งหมด','หารส่วนที่ทราบด้วยจำนวนทั้งหมดแล้วคูณหนึ่งร้อย')
    add('percentages','ร้อยละ','remainder-as-percent',[11],['percent_remainder_sentence_p5'],
        'คำนวณร้อยละของส่วนที่เหลือ','ลบส่วนที่ทราบออกจากทั้งหมดก่อนหารด้วยฐานทั้งหมดแล้วคูณหนึ่งร้อย')
    add('percentages','ร้อยละ','principal-plus-percent',[12],['profit_sale_sentence_p5'])
    add('percentages','ร้อยละ','profit-rate-model',[13],['profit_rate_sentence_p5'],
        'เลือกฐานในการคิดร้อยละกำไร','ลบทุนออกจากราคาขายเพื่อหากำไร แล้วหารด้วยทุนและคูณหนึ่งร้อย โดยไม่เปลี่ยนฐานเป็นราคาขาย')
    add('percentages','ร้อยละ','percent-complement',[14],['percent_remainder_sentence_p5'])
    add('percentages','ร้อยละ','original-from-discount',[15],['original_from_discount_sentence_p5'],
        'ย้อนหาราคาเดิมจากเงินส่วนลด','เงินส่วนลดเท่ากับอัตราร้อยละของราคาเดิม จึงหารเงินส่วนลดด้วยอัตราสัดส่วนเพื่อย้อนหาฐาน')
    add('percentages','ร้อยละ','cost-from-loss',[16],['cost_from_loss_sentence_p5'],
        'ย้อนหาราคาทุนจากราคาขายขาดทุน','ราคาขายเป็นส่วนที่เหลือของทุนหลังขาดทุน หารราคาขายด้วยหนึ่งลบอัตราขาดทุน โดยคงเศษส่วนแน่นอนเมื่อไม่กำหนดการปัด')
    add('data-presentation','การนำเสนอข้อมูล','double-bar-summary',[17,18],['double_bar_summary_p5'],
        'รวมและเปรียบเทียบข้อมูลสองชุดในแผนภูมิแท่ง','อ่านค่าทั้งสองชุดแยกตามประเภท รวมตามชุดที่ถามหรือรวมสองชุดในแต่ละประเภทก่อนเปรียบเทียบ')
    add('data-presentation','การนำเสนอข้อมูล','line-graph-extreme',[19],['line_graph_highest_p5'],
        'หาตำแหน่งที่ค่าน้อยหรือมากที่สุดในกราฟเส้น','เปรียบเทียบค่าทุกจุดก่อนอ่านป้ายตำแหน่งของค่าที่ถาม โดยไม่สับสนตำแหน่งกับค่าบนแกนตั้ง')
    add('data-presentation','การนำเสนอข้อมูล','line-graph-range',[20],['line_graph_problem_p5'],
        'หาผลต่างระหว่างค่าสูงสุดต่ำสุดจากกราฟเส้น','หาค่าสูงสุดและต่ำสุดจากทุกจุดแล้วลบกัน ไม่ใช้เฉพาะจุดแรกและจุดสุดท้าย')
    assert sorted(claims)==list(range(1,21))
    for path,(topic,units) in files.items():
        write_topic(path,topic,units,'ป.5')


if __name__=='__main__':
    main()
