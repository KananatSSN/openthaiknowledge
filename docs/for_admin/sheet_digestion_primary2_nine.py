"""Preserving map for three Primary 1 and 2 comprehension papers."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-1/4012-1-2565-1-2.pdf'
B='mathematics/level/primary-2/4170-2-2565-1-2.pdf'
C='mathematics/level/primary-2/4167-2-2565-2-2.pdf'


def main():
    files,claims={},[]
    def add(grade,slug,topic,key,sheet,numbers,covered=(),statement=None):
        path=ROOT/f'otk/knowledge/math/primary{grade}-{slug}.json'
        if path not in files:
            raw=json.loads(path.read_text()) if path.exists() else {'units':[]}
            files[path]=(topic,raw['units'],f'ป.{grade}')
        units=files[path][1]
        uid=f'math.primary{grade}.{key}'
        target=next((u for u in units if u['id']==uid),None)
        if target is None:
            assert statement,uid
            target=dict(id=uid,kind='procedure',title=statement,statement=statement,
                        steps=['อ่านข้อมูลและเงื่อนไขที่กำหนด',statement,'ตรวจทุกตัวเลือกและหน่วย'],sources=[],covered_by=[])
            units.append(target)
        for n in numbers:
            source={'sheet':sheet,'item':n}
            claims.append((sheet,n))
            if source not in target['sources']:
                target['sources'].append(source)
        for k in covered:
            if 'math.'+k not in target['covered_by']:
                target['covered_by'].append('math.'+k)

    add(1,'word-problems','โจทย์ปัญหา','sentence-to-story',A,[1,3,13,14,17,18])
    add(1,'word-problems','โจทย์ปัญหา','story-to-sentence',A,[2,4,11,12,15,16])
    add(1,'counting','การนับ','picture-thai-cardinality',A,[5],['count_objects_20_p1'])
    add(1,'counting','การนับ','expanded-form-judgement',A,[6])
    add(1,'counting','การนับ','digit-place-value',A,[7,8])
    add(1,'comparing-numbers','การเปรียบเทียบ','compare-sums',A,[9,10])
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','shape-identification',A,[19],['shape_2d_picture_p1','classify_2d_shape'],
        'แยกรูปหลายเหลี่ยมตามด้านตรง และแยกวงกลมออกจากวงรีที่ไม่ใช่วงกลมตามแบบเรียน')
    add(1,'solids','เรขาคณิต 3 มิติ','cylinder-object',A,[20],['solid_picture_p1'])

    add(2,'time','เวลา','clock-period-24h',B,[1,8])
    add(2,'time','เวลา','colloquial-clock',B,[2,6,7])
    add(2,'time','เวลา','clock-hands-from-hour',B,[3,4,5])
    add(2,'time','เวลา','daily-schedule-activity',B,[9,11])
    add(2,'time','เวลา','calendar-event-month',B,[10])
    add(2,'time','เวลา','calendar-month-order',B,[12,13],['month_ordinal_p2'])
    add(2,'time','เวลา','month-pair-days',B,[14],['month_pair_days_p2'],
        'เชื่อมลำดับกับชื่อเดือน หาจำนวนวันของแต่ละเดือนตามปีที่กำหนด แล้วรวมโดยคำนึงถึงกุมภาพันธ์')
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','shape-identification',B,[15])
    add(2,'shapes','รูปเรขาคณิต','polygon-picture',B,[16])
    add(2,'patterns','แบบรูป','repeating-shape-next',B,[17],['repeating_colour_pair_p2'])
    add(2,'patterns','แบบรูป','changing-attribute',B,[18])
    add(2,'shapes','รูปเรขาคณิต','solid-identification',B,[19,20])

    add(2,'measurement','การวัด','length-relational-statements',C,[1,7,9,10])
    add(2,'measurement','การวัด','half-metre',C,[2],['half_metre_p2'],
        'ครึ่งเมตรคือห้าสิบเซนติเมตร รวมกับจำนวนเต็มเมตรแล้วเขียนหน่วยเดี่ยวหรือหน่วยผสม')
    add(2,'measurement','การวัด','round-trip-metres',C,[3])
    add(2,'measurement','การวัด','mixed-length-difference',C,[4,8])
    add(2,'measurement','การวัด','route-length-sum',C,[5],['join_lengths_p1','length_word_problem_p2'],
        'รวมความยาวของเส้นทางแต่ละช่วงที่เดินผ่านตามหน่วยเดียวกัน')
    add(1,'measurement','การวัด','order-measured-lengths',C,[6])
    add(2,'measurement','การวัด','unit-quantity',C,[11],['unit_quantity_p2'],
        'ระบุว่าหน่วยเป็นของความยาว น้ำหนัก ปริมาตร หรือเวลา โดยไม่สับสนปริมาณกับสิ่งที่นำมาวัด')
    add(2,'measurement','การวัด','dry-measure-tool',C,[12,14])
    add(2,'measurement','การวัด','calibrated-volume-tools',C,[13],['calibrated_volume_tools_p2'],
        'ตรวจเครื่องตวงทุกชิ้นในกลุ่มว่ามีหน่วยความจุกำกับ ไม่รวมภาชนะไม่ทราบความจุหรือเครื่องมือวัดปริมาณอื่น')
    add(2,'measurement','การวัด','dry-measure-method',C,[15])
    add(2,'measurement','การวัด','weighing-tool-precision',C,[16],['weighing_tool_precision_p2'],
        'เลือกเครื่องชั่งที่รับน้ำหนักได้พอและมีขีดแบ่งละเอียดตามเกณฑ์ โดยต้องผ่านเงื่อนไขทั้งสองพร้อมกัน')
    add(2,'measurement','การวัด','kg-grams',C,[17],['convert_weight_p2','kg_g_to_g_p2'],
        'หนึ่งกิโลกรัมเท่ากับหนึ่งพันกรัม แปลงค่ากิโลกรัมก่อนรวมกรัมที่เหลือ')
    add(2,'measurement','การวัด','weight-threshold',C,[18],['weight_threshold_p2'],
        'แปลงกรัม ขีด และกิโลกรัมให้อยู่หน่วยเดียว แล้วแยกเกินหรือต่ำกว่าอย่างเคร่งครัดออกจากเท่ากัน')
    add(2,'measurement','การวัด','weight-extreme',C,[19,20],['weight_extreme_p2'],
        'แปลงน้ำหนักที่ให้ครบทุกสิ่งรวมจำนวนครึ่งกิโลกรัม แล้วเลือกค่ามากที่สุดหรือน้อยที่สุดโดยไม่เดาจากชื่อสิ่งของ')
    assert len(claims)==len(set(claims))==60
    assert set(claims)=={(p,n) for p in (A,B,C) for n in range(1,21)}
    for path,(topic,units,level) in files.items():
        write_topic(path,topic,units,level)


if __name__=='__main__':
    main()
