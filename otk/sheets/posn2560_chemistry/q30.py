"""Source p9, MC30: dissociate the alkene C=C into two fragments, choice ข.

The PDF displays no bond strokes or radical notation in the four reactions. The adaptation
explicitly prints the C=C in the parent and asks which fragmentation severs
that carbon-carbon connection.
"""

import re


def solve(alkene="CH2=CHCH3"):
    left, right = alkene.split("=")
    return (left, right)


def check(alkene="CH2=CHCH3"):
    # Independently parse the carbon chain into CH_n vertices and locate
    # the sole double edge; deleting it gives the two connected components.
    vertices = re.findall(r"CH[0-3]?", alkene)
    assert len(vertices) >= 3
    first = alkene.index("=")
    cut = len(re.findall(r"CH[0-3]?", alkene[:first]))
    return ("".join(vertices[:cut]), "".join(vertices[cut:]))


PARAMS = {"alkene": "CH2=CHCH3"}
VARIANTS = [
    {"alkene": "CH2=CHCH2CH3"},
    {"alkene": "CH3CH=CHCH3"},
    {"alkene": "CH2=CHCH2CH2CH3"},
]
ANSWER = ("CH2", "CHCH3")
