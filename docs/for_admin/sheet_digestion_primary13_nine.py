"""Preserving map for Primary 1 pattern and Primary 3 place-value papers."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-1/4009-1-2565-2-2.pdf'
B='mathematics/level/primary-3/4355-3-2565-1-2.pdf'


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

    add(1,'patterns','แบบรูป','unit-step-choice',A,[1,2,3,4],['unit_step_sequence_choice_p1'],
        'ตรวจผลต่างของทุกคู่ติดกันในแต่ละลำดับเพื่อเลือกแถวที่เพิ่มหรือลดทีละหนึ่งตลอดแถว')
    add(1,'patterns','แบบรูป','single-attribute-choice',A,[5,6,7],['single_attribute_pattern_p1'],
        'แยกการเปลี่ยนรูปร่าง สี และขนาด แล้วเลือกแบบรูปที่เปลี่ยนเฉพาะลักษณะที่ระบุโดยลักษณะอื่นคงเดิม')
    add(1,'comparing-numbers','การเปรียบเทียบ','ordering',A,[8,9,10,11,12])
    add(1,'counting','การนับ','expanded-form-judgement',A,[13])
    add(1,'counting','การนับ','expanded-form',A,[14])
    add(1,'counting','การนับ','digit-place-value',A,[15,16,17])
    add(1,'comparing-numbers','การเปรียบเทียบ','numeric-comparison',A,[18,19],['false_sum_comparison_p1','compare_sums_p1'])
    add(1,'comparing-numbers','การเปรียบเทียบ','false-sum-comparison',A,[20])

    add(3,'place-value','ค่าประจำหลัก','read-large-number-forms',B,[1,2],['number_reading_p3'],
        'อ่านค่าหลักหมื่นถึงหน่วยแล้วเชื่อมตัวเลขฮินดูอารบิก ตัวเลขไทย และคำอ่านไม่เกินหนึ่งแสน')
    add(3,'place-value','ค่าประจำหลัก','expanded-comparison-statement',B,[3,4],['expanded_comparison_statement_p3'],
        'หาค่าผลบวกค่าประจำหลักก่อนตรวจเครื่องหมายเปรียบเทียบ โดยแยกมากกว่าหรือน้อยกว่าออกจากข้อความไม่เท่ากันที่อาจจริงพร้อมกัน')
    add(3,'place-value','ค่าประจำหลัก','digit-place-value-pair',B,[5,6],['digit_place_value_pair_p3'],
        'ระบุตำแหน่งเลขโดดที่ถามแล้วคูณค่าประจำหลักเพื่อบอกหลักและค่ารวมกรณีศูนย์')
    add(3,'place-value','ค่าประจำหลัก','canonical-expansion',B,[7,8],['canonical_expansion_p3'],
        'แยกจำนวนเป็นพจน์ค่าของเลขโดดเพียงหลักเดียวต่อพจน์และละพจน์ศูนย์ โดยไม่ยอมรับเพียงผลบวกที่มีค่าเท่ากัน')
    add(3,'place-value','ค่าประจำหลัก','order-large-sequence',B,[9,10],['order_large_sequence_p3'],
        'เปรียบเทียบจำนวนตามหลักจากซ้ายไปขวาแล้วตรวจลำดับครบทุกตัวตามทิศที่ถาม')
    add(3,'addition-subtraction','การบวกและการลบ','subtract-large-stories',B,[11],['add_sub_large_p3'])
    add(3,'addition-subtraction','การบวกและการลบ','bracket-missing-number',B,[12],['bracket_missing_number_p3'],
        'ย้อนการบวกลบตามวงเล็บและตำแหน่งตัวไม่ทราบค่า แล้วแทนกลับตรวจทั้งประโยค')
    add(3,'measurement','การวัด','appropriate-length-unit',B,[13,14],['estimate_measure_p3'],
        'เลือกหน่วยความยาวที่สอดคล้องกับขนาดสิ่งของหรือสถานที่ โดยแยกการคาดคะเนออกจากการวัดจริง')
    # These questions reinforce already-indexed foundational measurement procedures.
    add(1,'measurement','การวัด','measuring-tool',B,[15,16],['measuring_tool_p3'])
    add(2,'measurement','การวัด','length-relational-statements',B,[17,18],['mixed_length_statement_p2'])
    add(3,'measurement','การวัด','longer-than-reference',B,[19],['longer_than_reference_p3'],
        'เปลี่ยนความยาวอ้างอิงจากเซนติเมตรเป็นมิลลิเมตรแล้วเลือกเฉพาะค่าที่มากกว่าอย่างเคร่งครัด')
    add(3,'measurement','การวัด','length-estimation-error',B,[20],['length_estimation_error_p3'],
        'เปลี่ยนค่าคาดคะเนและค่าที่วัดจริงเป็นเซนติเมตร หาผลต่างบวก แล้วเขียนหน่วยผสมให้ถูกต้อง')
    assert len(claims)==len(set(claims))==40
    assert set(claims)=={(p,n) for p in (A,B) for n in range(1,21)}
    for path,(topic,units,level) in files.items():
        write_topic(path,topic,units,level)


if __name__=='__main__':
    main()
