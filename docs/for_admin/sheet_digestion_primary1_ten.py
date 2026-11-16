"""Complete claims, with explicit remaining gaps, for Primary 1 LPMC25."""
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
A='mathematics/level/primary-1/11167-LPMC-Math-G1-No25-2567.pdf'


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

    add(1,'word-problems','โจทย์ปัญหา','inverse-add-sub-machine',A,[1],[],None)
    add(1,'patterns','แบบรูป','odd-rotated-tile',A,[2],[],'แยกเส้นของลวดลายแต่ละกระเบื้องแล้วตรวจความเหมือนกันภายใต้การหมุน โดยไม่สับสนเส้นขอบกระเบื้อง')
    add(1,'word-problems','โจทย์ปัญหา','post-interval-distance',A,[3],['post_interval_distance_p1'],'นับจำนวนช่องระหว่างหมายเลขเสาต้นแรกกับต้นสุดท้าย แล้วคูณระยะต่อช่องโดยไม่บวกหนึ่งเหมือนการนับต้นเสา')
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','unfold-corner-cut',A,[4],[],'สะท้อนรอยตัดย้อนแนวพับทั้งสองตามลำดับ เพื่อแยกรอยเว้าขอบออกจากรูด้านในกระดาษ')
    add(1,'word-problems','โจทย์ปัญหา','banknote-total',A,[5],['money_count_p2'],'คูณราคาธนบัตรด้วยจำนวนฉบับของแต่ละชนิด แล้วรวมทุกชนิด')
    add(1,'word-problems','โจทย์ปัญหา','difference',A,[6],[],None)
    add(1,'word-problems','โจทย์ปัญหา','rank-both-ends',A,[7],['rank_both_ends_p1'],'รวมอันดับของคนเดียวกันจากปลายแถวทั้งสอง แล้วหักหนึ่งเพราะนับคนนั้นซ้ำ')
    add(1,'word-problems','โจทย์ปัญหา','circular-hand-neighbour',A,[8],[],'เรียงคนเป็นวงกลมตามมือขวาที่จับมือซ้าย โดยคงทิศหันเข้าวงและตรวจเพื่อนบ้านที่มือที่ถาม')
    add(1,'word-problems','โจทย์ปัญหา','possible-nth-weekday',A,[9],['possible_nth_weekday_p1'],'พิจารณาทุกวันเริ่มเดือนที่เป็นไปได้ แล้วหาช่วงวันที่ของวันในสัปดาห์ครั้งที่กำหนด')
    add(1,'comparing-numbers','การเปรียบเทียบ','equal-pieces-size-rank',A,[10],['equal_pieces_size_rank_p1'],'เมื่อกระดาษต้นฉบับเท่ากัน จำนวนชิ้นยิ่งมากขนาดแต่ละชิ้นยิ่งเล็ก จัดอันดับขนาดโดยกลับอันดับจำนวนชิ้น')
    add(1,'counting','การนับ','equal-kind-label-sum',A,[11],[],'นับเฉพาะรูปชนิดที่กำหนดในแต่ละกรอบ แยกยิ้มจากหน้าเศร้า แล้วรวมป้ายชื่อของกรอบที่มีจำนวนเท่ากัน')
    add(1,'word-problems','โจทย์ปัญหา','minimum-coins',A,[12],['minimum_coins_p1'],'หาจำนวนเหรียญน้อยที่สุดที่รวมราคาได้พอดี โดยระบุชนิดที่อนุญาตและเงื่อนไขว่าต้องใช้ครบทุกชนิดหรือไม่')
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','rotated-polyomino-match',A,[13],[],'แทนช่องที่หายไปและชิ้นส่วนด้วยตำแหน่งตาราง ตรวจการเลื่อนและการหมุนที่อนุญาตโดยไม่เปลี่ยนรูปร่าง')
    add(1,'counting','การนับ','latin-missing-sum',A,[14],['latin_missing_sum_p1'],'ทุกแถวมีผลรวมหนึ่งถึงสี่เท่ากัน หักผลรวมช่องที่ให้จากผลรวมทั้งตาราง หรือเติมตารางแล้วรวมช่องว่าง')
    add(1,'comparing-numbers','การเปรียบเทียบ','mixed-age-height-order',A,[15],[],'เปลี่ยนความสัมพันธ์สูงต่ำเป็นอายุตามเงื่อนไขเฉพาะโจทย์ แล้วเชื่อมกับพี่น้องเพื่อหาคนเกิดก่อน')
    add(1,'word-problems','โจทย์ปัญหา','minimum-bags',A,[16],['minimum_bags_p1'],'หารจำนวนสิ่งของด้วยความจุถุง แล้วเพิ่มอีกหนึ่งถุงเมื่อมีเศษเพื่อบรรจุได้ครบโดยไม่จำเป็นต้องเต็มถุงสุดท้าย')
    add(1,'word-problems','โจทย์ปัญหา','heads-and-legs-total',A,[17],[],None)
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','noncrossing-circle-pairs',A,[18],[],'อ่านลำดับจุดรอบวง คู่ปลายทางที่สลับกันตามวงบังคับให้เส้นในวงตัดกัน แล้วเลือกการจับคู่ที่ไม่สลับ')
    add(1,'measurement','การวัด','nearest-typical-length',A,[19],[],'แยกการคาดคะเนจากขนาดสิ่งของทั่วไปออกจากการหาค่าที่ใกล้เป้าหมายที่สุดเมื่อมีค่าที่วัดกำหนด')
    add(1,'counting','การนับ','digit-cryptarithm-extreme',A,[20],[],'แทนรูปผลไม้ด้วยเลขโดดตามเงื่อนไข เขียนสมการตามหลักสิบหน่วย แล้วหาค่าผลต่างมากที่สุดในคำตอบที่เป็นไปได้')
    add(1,'word-problems','โจทย์ปัญหา','distinct-fruit-assignment',A,[21],['distinct_fruit_assignment_p1'],'ตัดชนิดที่แต่ละคนไม่เลือกแล้วใช้เงื่อนไขไม่ซ้ำกันตรวจการจัดสรรทุกคนพร้อมกัน')
    add(1,'word-problems','โจทย์ปัญหา','equalize-piles',A,[22],['equalize_piles_p1'],'หาจำนวนต่อกองเมื่อเท่ากัน แล้วย้ายเฉพาะส่วนเกินไปเติมส่วนขาดโดยนับสิ่งของแต่ละชิ้นที่ย้ายเพียงครั้งเดียว')
    add(1,'solids','เรขาคณิต 3 มิติ','dice-visible-opposites',A,[23],[],'บนลูกเต๋ามาตรฐาน หน้าตรงข้ามรวมเจ็ด หน้าที่เห็นประชิดกันจึงต้องไม่มีคู่รวมเจ็ด')
    add(1,'patterns','แบบรูป','inferred-star-complement',A,[24],[],'นับแฉกแล้วตรวจสมมติฐานผลรวมแฉกกับเลขกลางคงที่ โดยระบุว่าเป็นกฎที่อนุมานจากตัวอย่างจำกัด')
    add(1,'word-problems','โจทย์ปัญหา','nonadjacent-middle',A,[25],[],'ไล่ลำดับสามสิ่งที่เป็นไปได้ภายใต้ข้อห้ามติดกัน แล้วหาสิ่งที่อยู่กลางทุกลำดับที่ผ่านเงื่อนไข')
    add(1,'word-problems','โจทย์ปัญหา','same-year-age-sum',A,[26],[],'ใช้อายุเต็มปีภายใต้เงื่อนไขเกิดปีเดียวกันและผลรวมอายุ แล้วเพิ่มอายุแต่ละคนตามจำนวนปีที่ผ่านไป')
    add(1,'counting','การนับ','digit-inequality-count',A,[27],['digit_inequality_count_p1'],'ตรวจเลขโดดศูนย์ถึงเก้าทุกตัวกับอสมการ โดยรักษาทิศเครื่องหมายและการรวมค่าขอบเขต')
    add(1,'word-problems','โจทย์ปัญหา','changed-allocation-remainder',A,[28],[],'หาจำนวนของเดิมจากจำนวนคนคูณส่วนแบ่งเดิมบวกของเหลือ แล้วหักยอดแจกตามส่วนแบ่งใหม่')
    add(1,'word-problems','โจทย์ปัญหา','two-unit-prices-sum',A,[29],[],'หารราคารวมของแต่ละกลุ่มด้วยจำนวนชิ้นเท่ากันเพื่อหาราคาต่อชิ้น แล้วรวมราคาตามภาพที่ถาม')
    add(1,'plane-shapes','เรขาคณิต 2 มิติ','all-diagonal-triangles',A,[30],[],'รวมจุดตัดกับจุดยอดเดิมแล้วนับสามจุดไม่ร่วมเส้นที่ด้านทั้งสามมีเส้นวาดรองรับ โดยนับสามเหลี่ยมซ้อนด้วย')
    assert len(claims)==len(set(claims))==30
    assert set(claims)=={(A,n) for n in range(1,31)}
    for path,(topic,units,level) in files.items():
        write_topic(path,topic,units,level)


if __name__=='__main__':
    main()
