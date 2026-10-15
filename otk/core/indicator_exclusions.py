"""Curriculum indicators that a multiple-choice set cannot assess.

An indicator about an attitude (ตระหนัก…), a project, building something, or
presenting work is shown by doing it, not by picking an answer. These are left
out of coverage on purpose; ``scripts/task_queue.py`` does not list them, and
``otk/tests/test_indicator_exclusions.py`` keeps the list honest (each code is
an official one, and none is practised by a set — if one ever is, take it off).
"""

from __future__ import annotations

ATTITUDE = "an attitude, shown in behaviour"
PROJECT = "project work"

NOT_ASSESSABLE_BY_MCQ: dict[str, str] = {
    "ว 1.2 ม.1/8": ATTITUDE,
    "ว 1.2 ม.1/13": ATTITUDE,
    "ว 1.2 ม.1/18": ATTITUDE,
    "ว 4.1 ม.5/1": PROJECT,
    "ว 4.2 ม.3/1": "developing an application",
    "ว 4.2 ม.4/1": PROJECT,
    "เคมีเพิ่มเติม 3 ม.4/3": "planning, running and reporting an experiment",
    "เคมีเพิ่มเติม 3 ม.6/1": PROJECT,
    "เคมีเพิ่มเติม 3 ม.6/2": "evidence of integrating knowledge in project work",
    "เคมีเพิ่มเติม 3 ม.6/3": "presenting work",
    "เคมีเพิ่มเติม 3 ม.6/4": "taking part in seminars or exhibitions",
    "ส 5.1 ป.3/2": "drawing a plan of the school and community",
    "ส 5.2 ป.1/3": "taking part in caring for the environment at home and in class",
    "ส 5.2 ป.3/6": "taking part in managing the community's environment",
}
