"""Source p4, MC8: P > Ca > As is the one false property order."""


ELEMENTS = ("P", "Ca", "As")
PROPERTIES = {
    "ie": {"P": 1011.8, "Ca": 589.8, "As": 944.5},
    "en": {"P": 2.19, "Ca": 1.00, "As": 2.18},
    "radius": {"P": 180, "Ca": 231, "As": 185},
    "melting": {"P": 44.15, "Ca": 842, "As": 817},
}


def claims(labels=("P", "Ca", "As")):
    symbols = dict(zip(ELEMENTS, labels))
    return (
        ("ie", (symbols["P"], symbols["Ca"], symbols["As"])),
        ("en", (symbols["P"], symbols["As"], symbols["Ca"])),
        ("radius", (symbols["Ca"], symbols["As"], symbols["P"])),
        ("melting", (symbols["Ca"], symbols["As"], symbols["P"])),
    )


def solve(labels=("P", "Ca", "As")):
    assert set(labels) == set(ELEMENTS)
    reverse = dict(zip(labels, ELEMENTS))
    false = [i for i, (property_name, order) in enumerate(claims(labels))
             if not all(PROPERTIES[property_name][reverse[left]] >
                        PROPERTIES[property_name][reverse[right]]
                        for left, right in zip(order, order[1:]))]
    assert len(false) == 1
    return false[0]


def check(labels=("P", "Ca", "As")):
    reverse = dict(zip(labels, ELEMENTS))
    actual = {name: tuple(sorted(labels, key=lambda label: values[reverse[label]],
                                 reverse=True))
              for name, values in PROPERTIES.items()}
    false = [i for i, (name, order) in enumerate(claims(labels))
             if order != actual[name]]
    assert len(false) == 1
    return false[0]


PARAMS = {"labels": ("P", "Ca", "As")}
VARIANTS = [
    {"labels": ("As", "P", "Ca")},
    {"labels": ("Ca", "As", "P")},
    {"labels": ("P", "As", "Ca")},
]
ANSWER = 0
