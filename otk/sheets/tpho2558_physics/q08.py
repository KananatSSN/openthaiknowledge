"""Theory 2.1 (c): heating at a constant rate, t_B/t_A = (Q_G + Q_W + Q_L)/Q_G = 1 + (1/c_VG)(c_VW + L/(T1 - T0))(T0 P1/(T1 P0) - 1), the water evaporating near T0. Adapted: P0, P1 (kPa) and the temperatures (Celsius) vary with c_VG = 20.8, c_VW = 25.0 J/(mol K) and L = 40.7 kJ/mol; returns t_B/t_A."""


def solve(pressure=100.0, final=129.0, start=27.0, end=100.0, gas_heat=20.8, vapour_heat=25.0, latent=40700.0):
    T0, T1 = start + 273.15, end + 273.15
    return 1 + (vapour_heat + latent / (T1 - T0)) * (T0 * final / (T1 * pressure) - 1) / gas_heat


def check(pressure=100.0, final=129.0, start=27.0, end=100.0, gas_heat=20.8, vapour_heat=25.0, latent=40700.0, R=8.314):
    # Moles of gas and water in a litre, then the three heats directly.
    T0, T1 = start + 273.15, end + 273.15
    V = 1e-3
    gas = pressure * 1e3 * V / (R * T0)
    water = final * 1e3 * V / (R * T1) - gas
    rise = T1 - T0
    q_gas = gas * gas_heat * rise
    return (q_gas + water * vapour_heat * rise + water * latent) / q_gas


PARAMS = {"pressure": 100.0, "final": 129.0, "start": 27.0, "end": 100.0, "gas_heat": 20.8, "vapour_heat": 25.0, "latent": 40700.0}
VARIANTS = [{"final": 135.0}, {"end": 120.0, "final": 140.0}, {"gas_heat": 29.1}]
ANSWER = 2.05402288363372
TOL = 1e-9
