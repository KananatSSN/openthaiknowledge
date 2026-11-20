"""Theory 2.8: the condensation's share of the heat removed is 1929/2506 = 77%. Adapted: the room volume and both humidities vary; returns the percentage."""


def solve(room=75.0, humid=70.0, dry=50.0, coil=10.0):
    from otk.sheets.tpho2559_physics import q11, q12

    return 100 * q11.solve(room=room, humid=humid, dry=dry, coil=coil) / q12.solve(room=room, humid=humid, dry=dry, coil=coil)


def check(room=75.0, humid=70.0, dry=50.0, coil=10.0):
    from otk.sheets.tpho2559_physics._aircon import balance

    b = balance(room, humid=humid, dry=dry, coil=coil)
    return 100 * b["latent"] / b["total"]


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "coil": 10.0}
VARIANTS = [{"room": 60.0}, {"coil": 5.0}, {"dry": 40.0, "humid": 80.0}]
ANSWER = 76.96052325488577
TOL = 5e-3
