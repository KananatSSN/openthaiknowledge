# OpenThaiKnowledge (otk)

[English](README.md) · **ภาษาไทย**

คลังความรู้ตามหลักสูตรไทยในรูปแบบโค้ด: ชุดโจทย์ 3,468 ชุด ตั้งแต่ ป.1 ถึง ม.6
และระดับโอลิมปิก แต่ละชุดสร้างโจทย์ปรนัยข้อใหม่จาก seed ได้ไม่จำกัด
พร้อมเฉลยที่ตรวจสอบแล้ว นอกจากนี้ยังมีหน่วยความรู้ที่ใช้สร้างชุดโจทย์เหล่านั้น
และเครื่องมือที่แปลงข้อสอบและหนังสือเรียนให้เป็นทั้งสองอย่าง

ทุกคนร่วมพัฒนาได้ โดยให้ AI agent ของคุณทำงานตามกติกาของ repository นี้
แล้วคุณตรวจผลงานก่อนส่ง ดูเงื่อนไขการเผยแพร่โครงการและผลงานที่ร่วมพัฒนาได้ที่
[สัญญาอนุญาต](#สัญญาอนุญาต)

## ร่วมพัฒนาด้วย AI agent ของคุณ

สิ่งที่ต้องมี:

- บัญชี GitHub
- [git](https://git-scm.com/), [GitHub CLI](https://cli.github.com/)
  (`gh` ที่ลงชื่อเข้าใช้แล้วด้วย `gh auth login`) และ [uv](https://docs.astral.sh/uv/)
- coding agent ที่สั่งรันคำสั่งได้ เช่น Claude Code หรือ Codex

เปิด agent ในโฟลเดอร์ที่คุณเก็บโปรเจกต์ แล้ววางข้อความนี้:

```text
ช่วยติดตั้ง repository OpenThaiKnowledge บนเครื่องนี้ ให้พร้อมสำหรับร่วมพัฒนา
ชุดโจทย์ ทำตามขั้นตอนตามลำดับ และตรวจว่าแต่ละขั้นสำเร็จก่อนไปขั้นถัดไป
ถ้าขั้นไหนล้มเหลว ให้หยุดและบอกฉันว่าเกิดอะไรขึ้น อย่าหาทางเลี่ยงเอง
ตอบฉันเป็นภาษาไทย

1. ตรวจเครื่องมือ: รัน `git --version`, `gh auth status` และ `uv --version`
   ถ้าขาดตัวไหน หรือ gh ยังไม่ได้ลงชื่อเข้าใช้ ให้บอกวิธีติดตั้งหรือลงชื่อเข้าใช้
   สำหรับระบบปฏิบัติการนี้ แล้วรอฉัน

2. fork repository แล้ว clone fork ของฉัน:
     gh repo fork KananatSSN/openthaiknowledge --clone --default-branch-only
     cd openthaiknowledge
   จากนั้นตรวจ `git remote -v`: `origin` ต้องเป็น fork ของฉัน และ `upstream`
   ต้องเป็น KananatSSN/openthaiknowledge ไฟล์ PDF ต้นฉบับใน sheet_database/
   จะเป็นไฟล์ pointer ขนาดเล็กของ Git LFS ซึ่งเป็นเรื่องปกติ ไม่มีขั้นตอนไหนต้องใช้

3. สร้าง Python environment ในโฟลเดอร์นี้เท่านั้น ระบุ environment ให้ชัดเจน
   เพื่อไม่ให้ไปแก้ virtualenv ที่เปิดใช้อยู่แล้ว:
     uv venv --python 3.12
     uv pip install --python .venv -e ".[test]" ruff
   (บน Windows คำสั่งข้างล่างใช้ .venv\Scripts\ แทน .venv/bin/)

4. ตรวจชื่อและอีเมลใน git ของ repository นี้: `git config user.name` และ
   `git config user.email` ต้องมีค่าทั้งคู่ ถ้ายังไม่มี ให้ถามฉัน แล้วตั้งค่าด้วย
   `git config` (ไม่ใช้ --global) ทุก commit ใน repository นี้ต้อง sign-off
   ด้วย `git commit -s`

5. ตรวจว่าติดตั้งเรียบร้อย (ประมาณหนึ่งนาที):
     .venv/bin/python -m pytest otk/tests/test_golden_draws.py otk/tests/test_provenance.py otk/tests/test_set_safety.py otk/tests/test_sets_layout.py -q -n auto
     .venv/bin/ruff check otk
     .venv/bin/python -c "from random import Random; from otk.api import REGISTRY; print(REGISTRY['math.count_objects_p1'].generate(Random(1)).model_dump_json(indent=1)[:600])"
   ทุก test ต้องผ่าน และ ruff ต้องไม่รายงานปัญหา

6. อ่าน AGENTS.md และ CONTRIBUTING.md ให้จบ ทั้งสองไฟล์คือกติกาของงานทุกอย่าง
   ใน repository นี้ ดู skill ใน .agents/skills/ และ otk/sets/INDEX.md
   ซึ่งบอกว่าชุดโจทย์แต่ละชุดอยู่ที่ไฟล์ไหน

7. ดูงานที่เปิดรับอยู่:
     gh issue list -R KananatSSN/openthaiknowledge --label "task: indicator"
     gh issue list -R KananatSSN/openthaiknowledge --label "task: digest"
   อาจยังไม่มีงานเปิดอยู่

จากนั้นสรุปให้ฉันว่า: ติดตั้งอะไรไปบ้าง ผล test เป็นอย่างไร กติกาใน AGENTS.md
โดยย่อสองบรรทัด และมีงานอะไรเปิดอยู่ แล้วถามฉันว่าจะให้ทำอะไร อย่าแก้ไฟล์
สร้าง branch หรือ commit จนกว่าฉันจะบอก
```

เมื่อ agent สรุปกลับมาแล้ว ให้มอบงานหนึ่งอย่าง เช่น issue ที่จะปิด
ตัวชี้วัดในหลักสูตรที่ยังมีโจทย์ให้ฝึกไม่พอ หรือแหล่งข้อมูลที่คุณมีสิทธิ์ใช้
จากนั้นตรวจผลงานด้วยตัวเองแล้วเปิด pull request
[CONTRIBUTING.md](CONTRIBUTING.md) อธิบายว่างานที่ดีเป็นอย่างไร
และผู้ดูแลตรวจอะไรบ้าง ส่วน [AGENTS.md](AGENTS.md) คือกติกาที่ agent ของคุณต้องทำตาม
(ทั้งสองไฟล์เป็นภาษาอังกฤษ)

## โครงสร้าง

| ที่อยู่ | เก็บอะไร |
|---|---|
| `otk/api.py` | **ส่วนที่เปิดให้ใช้งาน** ผู้ใช้ภายนอก import จากไฟล์นี้เท่านั้น |
| `otk/sets/` | **ชุดโจทย์**: `<วิชา>/<ระดับชั้น>/<หน่วย>.py` หนึ่งไฟล์ต่อหนึ่งหน่วยการเรียนรู้ [`INDEX.md`](otk/sets/INDEX.md) บอกทุกไฟล์และชุดโจทย์ในไฟล์ แต่ละวิชามี `README.md` ของตัวเอง |
| `otk/kit/` | เครื่องมือกลางสำหรับเขียนชุดโจทย์: โจทย์คณิตศาสตร์ ตัวเลือก คลังแนวคิด ตารางจัดหมวดหมู่ เรื่องราวในโจทย์ปัญหา |
| `otk/core/` | โมเดลเนื้อหา registry ตัวลวง คำศัพท์ความผิดพลาด ที่มาของชุดโจทย์ ตำแหน่งในหลักสูตร และใบงาน PDF |
| `otk/pictures/` | ตัววาดภาพและแผนภาพ ไฟล์ PNG ที่ commit ไว้ และ registry ของแผนภาพ |
| `otk/sheets/` | ข้อสอบเก่าที่ย่อยแล้ว หนึ่ง package ต่อหนึ่งชุดข้อสอบ และ `bank.json` ซึ่งเป็นดัชนีของคลังต้นฉบับ |
| `otk/knowledge/` | หน่วยความรู้ที่สกัดจากแหล่งข้อมูล |
| `otk/tools/` | `sheetpipe` (ขั้นตอนย่อยข้อสอบ), `golden_draws`, `explorer_data`, `sets_index`, `curriculum_graph` |
| `otk/tests/` | ชุด test รวมถึง `golden_draws.json` |
| `scripts/` | สคริปต์ตรวจและส่งออกเนื้อหา และ `task_queue.py` (สร้างงานที่เปิดรับเป็น GitHub issue) |
| `explorer/` | เว็บไซต์สำรวจชุดโจทย์ทุกชุดและลองทำตัวอย่างโจทย์ |
| `sheet_database/` | คลังต้นฉบับ: เนื้อหาที่ย่อยแล้ว ข้อความที่ถอดแล้ว และบันทึก ไม่เผยแพร่ไฟล์ PDF ต่อ (ดูด้านล่าง) |
| `.agents/skills/` | skill สำหรับ agent: `sheet-bank`, `sheet-to-generator`, `sheet-transcriber` (Claude Code เข้าถึงผ่าน `.claude/`) |
| `docs/` | แผนงานเนื้อหา ผลการตรวจ และเอกสารหลักสูตรฉบับทางการ |

## พัฒนา

การติดตั้งข้างต้นแบบทำเอง:

```bash
gh repo fork KananatSSN/openthaiknowledge --clone --default-branch-only
cd openthaiknowledge
uv venv --python 3.12 && uv pip install --python .venv -e ".[test]" ruff
```

ก่อนเปิด pull request:

```bash
.venv/bin/python -m pytest otk/tests -q -n auto   # test ทั้งหมด ประมาณ 15 นาทีบน 8 core
.venv/bin/ruff check otk
```

test การจัดวางข้อความภาษาไทยต้องมีฟอนต์ไทย (`fonts-thai-tlwg` บน Debian/Ubuntu)
`pytest -m slow` รันการตรวจคุณภาพแบบหนึ่งพัน seed ที่ CI รันทุกคืน

เมื่อเพิ่มหรือแก้ชุดโจทย์:

```bash
python -m otk.tools.golden_draws --update math.new_set_p5   # บันทึกชุดใหม่ หรือชุดที่ตั้งใจเปลี่ยน
python -m otk.tools.golden_draws --retire math.old_set      # หลังลบชุดโจทย์
python -m otk.tools.sets_index                              # อัปเดต otk/sets/INDEX.md และ README ของแต่ละวิชา
```

## การใช้งาน

```bash
pip install "openthaiknowledge @ git+https://github.com/KananatSSN/openthaiknowledge@v0.5.2"
```

```python
from random import Random
from otk.api import REGISTRY, catalog

question = REGISTRY["math.count_objects_p1"].generate(Random(42))
```

`otk config.json` พิมพ์ใบงาน PDF แบบออฟไลน์จากไฟล์ตั้งค่า JSON (`otk --help`)

### สิ่งที่ผู้ใช้ภายนอกวางใจได้

- **key ไม่เปลี่ยน** key ของชุดโจทย์จะไม่เปลี่ยนความหมายและไม่ถูกนำกลับมาใช้ซ้ำ
  ชุดที่ถูกลบจะอยู่ในรายการที่เลิกใช้แล้ว
- **seed ให้ผลเดิม** key, seed และ params เดียวกันให้โจทย์ข้อเดิมในทุกรุ่น
  เว้นแต่ release notes จะระบุว่าชุดนั้นเปลี่ยน
- **`otk.api` คือข้อตกลง** ส่วนอื่นอาจย้ายที่ระหว่างรุ่นได้

`otk/tests/test_golden_draws.py` บังคับสองข้อแรก โดยเก็บ hash ของโจทย์ทุกชุด
จาก seed คงที่ห้าค่า ชุดโจทย์แต่ละชุดยังระบุที่มาของตัวเอง
(`otk.api.provenance(key)`): เขียนขึ้นใหม่ หรือดัดแปลงจากแหล่งที่อ้างอิงไว้

## คลังต้นฉบับ

`sheet_database/` คือที่เก็บแหล่งข้อมูลสำหรับย่อย ได้แก่ ชุดรวมข้อสอบ
แบบฝึกหัดจากหนังสือเรียน และบันทึก ส่วนใหญ่เป็นเนื้อหาของบุคคลอื่น
ไฟล์ PDF เป็น Git LFS object ที่เก็บอยู่ในที่เก็บส่วนตัวของผู้ดูแล (`.lfsconfig`)
เมื่อ clone จะได้เพียงไฟล์ pointer และส่วนอื่นทั้งหมดใช้งานได้โดยไม่ต้องมีไฟล์เหล่านี้
เนื้อหาที่ย่อยแล้ว ข้อความที่ถอดแล้ว และชุดโจทย์ที่ดัดแปลงจากแหล่งข้อมูล
เผยแพร่พร้อมการอ้างอิง ([SOURCES.md](SOURCES.md)) เจ้าของสิทธิ์ขอให้นำส่วนใดออกได้
และเราจะนำออกให้

การย่อยแหล่งข้อมูลใช้ skill `sheet-bank` (`.agents/skills/sheet-bank`)

## Explorer

`explorer/` คือเว็บไซต์สำรวจชุดโจทย์: บอร์ดหลักสูตร ตัวอย่างโจทย์และเฉลยของทุกชุด
และหน้านี้ ดูวิธีรันหรือนำขึ้นเว็บได้ใน [README](explorer/README.md)

## สัญญาอนุญาต

| อะไร | สัญญาอนุญาต |
|---|---|
| โค้ด: ทุกอย่างที่ไม่ได้ระบุไว้ข้างล่าง รวมถึงชุดโจทย์และข้อความโจทย์ในชุดเหล่านั้น | [Apache-2.0](LICENSE) |
| เนื้อหา: หน่วยความรู้ (`otk/knowledge/`) และเอกสารของโครงการ | [CC BY 4.0](LICENSE-CONTENT) |
| เนื้อหาของบุคคลอื่น: คลังต้นฉบับ (`sheet_database/`: เนื้อหาที่ย่อยแล้ว ข้อความที่ถอดแล้ว) ข้อความและรูปของข้อสอบที่ย่อยแล้ว และสิ่งที่ชุดโจทย์แบบดัดแปลงอ้างอิง | โครงการนี้ไม่ได้ให้สิทธิ์ เนื้อหาเป็นของเจ้าของ มีการอ้างอิงไว้ใน [SOURCES.md](SOURCES.md) และนำออกได้เมื่อมีการร้องขอ |

ผลงานที่ร่วมพัฒนาจะอยู่ภายใต้เงื่อนไขเดียวกัน โดยรับรองทุก commit ด้วย
DCO sign-off (`git commit -s`; ดู [CONTRIBUTING.md](CONTRIBUTING.md))
