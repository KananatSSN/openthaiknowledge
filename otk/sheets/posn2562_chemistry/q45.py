"""3 volumes X2 + one volume Y3 make 3 volumes X2Y."""


def solve(x2_volume=30, y3_volume=10, product_volume=30):
    x_atoms_per_product = 2 * x2_volume / product_volume
    y_atoms_per_product = 3 * y3_volume / product_volume
    return (round(x_atoms_per_product), round(y_atoms_per_product))


def check(x2_volume=30, y3_volume=10, product_volume=30):
    for x in range(1, 6):
        for y in range(1, 6):
            if x * product_volume == 2 * x2_volume and y * product_volume == 3 * y3_volume:
                return (x, y)
    raise ValueError("no formula")


PARAMS = {"x2_volume": 30, "y3_volume": 10, "product_volume": 30}
VARIANTS = [
    {"x2_volume": 60, "y3_volume": 20, "product_volume": 60},
    {"x2_volume": 15, "y3_volume": 5, "product_volume": 15},
    {"x2_volume": 90, "y3_volume": 30, "product_volume": 90},
]
ANSWER = solve(**PARAMS)
