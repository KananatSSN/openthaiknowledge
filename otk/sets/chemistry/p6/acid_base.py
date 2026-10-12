"""กรดและเบสในชีวิตประจำวัน

เคมี · ป.6 · เสริมทักษะ
Indicators: —

Sets moved here from: chemistry.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.chemistry import SUBJECT, TOPIC_MATTER

PROVENANCE = Provenance("original")


@question_type("chem.acid_base",
               display_name={"th": "สารในชีวิตประจำวัน (กรด–เบส)"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_MATTER)
class AcidBase(ClassifyType):
    """จำแนกสารที่พบในชีวิตประจำวันตามฤทธิ์ กรด / เบส / กลาง."""

    CLASSIFY_STEM = "“{member}” เป็นสารที่มีฤทธิ์เป็นแบบใด"
    PICK_STEM = "ข้อใดจัดเป็น{category}"

    CATEGORIES = [
        Category("สารที่มีฤทธิ์เป็นกรด (Acidic)",
                 ("น้ำมะนาว", "น้ำส้มสายชู", "น้ำอัดลม", "วิตามินซี",
                  "น้ำยาล้างห้องน้ำชนิดกรด")),
        Category("สารที่มีฤทธิ์เป็นเบส (Basic)",
                 ("สบู่", "ผงซักฟอก", "ยาสีฟัน", "น้ำปูนใส", "น้ำขี้เถ้า")),
        Category("สารที่มีฤทธิ์เป็นกลาง (Neutral)",
                 ("น้ำบริสุทธิ์", "สารละลายโซเดียมคลอไรด์บริสุทธิ์",
                  "สารละลายน้ำตาลซูโครสบริสุทธิ์")),
    ]
