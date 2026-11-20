"""Map one complete Primary 1 contest, preserving prior coverage."""
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[2]
write_topic=runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']
SOURCE='mathematics/level/primary-1/10257-LPMC-Math-G1-No26-2568.pdf'


def u(key,title,statement,numbers,covered):
    return dict(id='math.primary1.'+key,kind='procedure',title=title,statement=statement,
                steps=['ระบุข้อมูลและเงื่อนไข',statement,'ตรวจคำตอบกับเงื่อนไขทุกข้อ'],
                sources=[{'sheet':SOURCE,'item':n} for n in numbers],covered_by=['math.'+k for k in covered])


def main():
    files={
        ('patterns','แบบรูป'):[
            u('block-rotation','นับรอบย้ายบล็อกหน้าสุดไปท้าย','จำลองการย้ายโดยรักษาลำดับภายในกลุ่มจนกลับเหมือนเดิม แล้วนับครั้งที่น้อยที่สุด',[5],['block_rotation_p1']),
            u('combined-difference-patterns','รวมพจน์ถัดไปของแบบรูปหลายแถว','หาผลต่างของแต่ละแถว แยกผลต่างคงที่และผลต่างที่เพิ่มคงที่ก่อนหาพจน์ถัดไปแล้วรวมคำตอบ',[30],['number_pattern_p1','sequence_patterns_m6','add_three_numbers_p1']),
        ],
        ('counting','การนับ'):[
            u('digit-clues','หาจำนวนตามเงื่อนไขเลขโดด','ตรวจผลต่างและผลรวมเลขโดดทุกหลัก หรือแจกแจงจำนวนสองหลักตามผลรวมแล้วเลือกมากหรือน้อยที่สุด',[20,26],['digit_clues_p1']),
        ],
        ('comparing-numbers','การเปรียบเทียบ'):[
            u('race-constraints','เลือกอันดับที่สอดคล้องกับทุกเงื่อนไข','ตรวจอันดับแรกและความสัมพันธ์ก่อนหลังของทุกคู่กับตัวเลือก ไม่สรุปว่ามีอันดับที่เป็นไปได้เพียงแบบเดียว',[17],['race_constraints_p1']),
        ],
        ('plane-shapes','เรขาคณิต 2 มิติ'):[
            u('constant-radius-region','จำแนกบริเวณที่เคลื่อนรอบจุดยึดได้','เมื่อไม่มีสิ่งกีดขวาง จุดที่อยู่ไม่เกินระยะเชือกจากจุดยึดเป็นบริเวณวงกลม',[4],['classify_2d_shape']),
            u('equal-cell-count-comparison','เปรียบเทียบจำนวนช่องที่ระบายสี','แบ่งรูปเป็นช่องเท่ากัน นับแต่ละช่องครั้งเดียว แล้วเลือกจำนวนที่ต่างจากจำนวนอ้างอิง',[13],['count_units_nonstandard','count_objects_20_p1','compare_groups_p1']),
            u('seven-segment-removal','ตรวจการหยิบก้านจากเลขแปด','เมื่อห้ามย้ายก้านที่เหลือ ให้นับก้านที่หายไปจากเจ็ดส่วนเพื่อหาตัวเลขที่สร้างได้ตามจำนวนที่หยิบ',[18],['seven_segment_removal_p1']),
            u('grid-path-check','ตรวจเส้นทางลูกศรไปยังจุดปลาย','นับการเดินแนวขวาและแนวขึ้นแยกกันแล้วเทียบระยะทั้งสองแนวกับจุดปลาย',[19],['grid_path_check_p1']),
            u('equal-cell-value','รวมค่าคงที่ของช่องเท่ากัน','ระบุกติกาว่าแต่ละช่องมีค่าเท่ากัน แล้วนับช่องและคูณค่าต่อช่อง ไม่รวมขอบร่วมเป็นก้านเดียว',[22],['count_units_nonstandard','multiplication_word_problem_p2']),
        ],
        ('word-problems','โจทย์ปัญหา'):[
            u('purchase-from-change-total','รวมราคาหลายชิ้นจากเงินทอนชิ้นเดียว','ลบเงินทอนจากเงินจ่ายเพื่อหาราคาหนึ่งชิ้น แล้วคูณจำนวนชิ้นที่ต้องการ',[1],['purchase_from_balance_p1','buy_several_p3']),
            u('multiple-of-related-ages','หาหลายเท่าของผลรวมอายุที่สัมพันธ์กัน','หาบุคคลที่อายุมากกว่าจากผลต่าง รวมอายุที่โจทย์ระบุ แล้วคูณจำนวนเท่า',[2],['age_word_p1','multiplication_word_problem_p2']),
            u('weekday-weekend-total','รวมจำนวนรายวันที่มีสองอัตรา','คูณอัตราวันจันทร์ถึงศุกร์ด้วยห้าและอัตราเสาร์อาทิตย์ด้วยสอง แล้วรวมผลคูณ',[3],['two_purchase_total_p2','daily_total_weeks_p2']),
            u('ordered-sharing','นับวิธีแบ่งของแบบจำนวนเพิ่มตามอายุ','แจกแจงจำนวนเต็มบวกสามจำนวนที่เรียงเพิ่มและรวมได้ทั้งหมด โดยห้ามนับสลับคนซ้ำ',[6],['ordered_sharing_p1']),
            u('grid-relative-position','หาหมายเลขในตารางจากตำแหน่งรอบตัว','เปรียบเทียบจำนวนคนด้านหน้ากับหลังและซ้ายกับขวา โดยทุกด้านต้องมีคน เพื่อหาแถวคอลัมน์แล้วอ่านหมายเลข',[7],['grid_relative_position_p1']),
            u('pair-absence','หาจำนวนสมาชิกกลุ่มที่มาไม่ครบ','กลุ่มสองกลุ่มเริ่มเท่ากัน เมื่อกลุ่มหนึ่งมาครบ จำนวนที่ไม่มีคู่ต่างกลุ่มเท่ากับจำนวนที่ขาดของอีกกลุ่ม',[8],['pair_absence_p1']),
            u('balance-ball-swaps','หาจำนวนแลกขั้นต่ำให้ผลรวมสองถุงเท่ากัน','แต่ละครั้งแลกหนึ่งลูกจากแต่ละถุง ตรวจการเปลี่ยนผลรวมทั้งสองถุงพร้อมกันและหาจำนวนครั้งต่ำสุด',[9],['balance_ball_swaps_p1']),
            u('overlap-circle-sums','รวมค่าของช่องไม่ซ้อนจากวงกลมสามวง','ลบค่าช่องซ้อนจากผลรวมแต่ละวงให้ครบก่อนรวมค่าของสามช่องที่ไม่ซ้อน',[10],['overlap_circle_sums_p1']),
            u('pack-price-and-change','หาราคาหลายแพ็กและเงินทอน','หาจำนวนแพ็กจากจำนวนชิ้นที่ซื้อ คูณราคาแพ็กแล้วลบออกจากเงินที่จ่าย',[11],['pack_price_irrelevant_p2','money_change_left']),
            u('daily-combined-saving','หาจำนวนวันที่ออมจากสองเงินสมทบต่อวัน','รวมเงินออมของตนและเงินสมทบต่อวันก่อนหารยอดรวม โดยนับเฉพาะวันที่ออม',[12],['add_word_problem','division_word_problem_p2']),
            u('change-removal-target','เปลี่ยนจำนวนที่หยิบออกให้ได้ยอดคงเหลือใหม่','บวกจำนวนที่หยิบออกเดิมกับยอดคงเหลือเดิมหาเงินหรือของเริ่มต้น แล้วลบยอดคงเหลือที่ต้องการ',[14],['mixed_start_amount_p1','missing_part_word_problem']),
            u('out-and-back-shorter','รวมเวลาไปกลับเมื่อขากลับสั้นกว่า','หาขากลับด้วยการลบส่วนต่างจากขาไป แล้วรวมเวลาสองขา',[15],['add_sub_mixed_word_problem','two_step_word_problem']),
            u('inverse-add-sub-machine','ย้อนหาค่าเริ่มต้นจากเครื่องบวกลบ','ย้อนจากผลลัพธ์ด้วยการดำเนินการตรงข้ามตามลำดับย้อนกลับ',[16],['mixed_start_amount_p1']),
            u('knockout-matches','นับคู่แข่งขันจนเหลือผู้ชนะหนึ่งคน','แต่ละคู่คัดผู้เล่นออกหนึ่งคน ไม่นับเกมเสมอเป็นคู่ใหม่ จึงนับจำนวนที่ต้องคัดออกจนเหลือหนึ่ง',[21],['knockout_matches_p1']),
            u('heads-and-legs-total','รวมจำนวนหัวและขาของสัตว์สองชนิด','คูณจำนวนสัตว์แต่ละชนิดด้วยจำนวนหัวและขาต่อตัว แล้วรวมทุกชนิด',[23],['multiplication_word_problem_p2','add_word_problem']),
            u('forward-add-sub-chain','คำนวณลำดับบวกและลบตามลูกศร','เริ่มจากจำนวนต้นทางแล้วบวกหรือลบแต่ละขั้นตามลำดับ',[24],['add_sub_mixed']),
            u('whole-pack-price','หาราคาตามจำนวนแพ็กเต็ม','หารจำนวนชิ้นที่ต้องการด้วยจำนวนชิ้นต่อแพ็กแล้วคูณราคาแพ็ก',[25],['pack_price_irrelevant_p2']),
            u('related-amount-total','รวมสองจำนวนเมื่อจำนวนหนึ่งน้อยกว่าอีกจำนวน','ลบส่วนต่างจากจำนวนที่ทราบเพื่อหาอีกจำนวน แล้วรวมสองจำนวน',[27],['add_sub_mixed_word_problem']),
            u('supply-shortfall','หาจำนวนของที่ขาดเพื่อแจกครบ','คูณจำนวนผู้รับด้วยจำนวนต่อคน แล้วลบของที่มีอยู่',[28],['multiplication_word_problem_p2','more_needed_p1']),
            u('reverse-double-balance','ย้อนหาเงินก่อนเพิ่มเท่าตัว','บวกเงินที่ใช้ครั้งสุดท้ายกลับก่อน หารสองเพื่อย้อนการได้เงินเพิ่มเท่าที่เหลือ แล้วบวกเงินที่ใช้ครั้งแรก',[29],['reverse_double_balance_p1']),
        ],
    }
    claims=[s['item'] for units in files.values() for unit in units for s in unit['sources']]
    assert sorted(claims)==list(range(1,31))
    for (slug,topic),units in files.items():
        write_topic(ROOT/f'otk/knowledge/math/primary1-{slug}.json',topic,units)


if __name__=='__main__':
    main()
