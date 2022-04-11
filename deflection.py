import numpy as np
import matplotlib.pyplot as plt

def get_rho(temperature, pressure=1., specific_gas_constant=1.):
    return pressure / (temperature * specific_gas_constant)

def get_refractive_index(k, rho):
    return k * rho + 1

def main():
    temperature = np.linspace(20, 500, 100) + 273.15
    r_medium = 148.19  # CO2
    gd_coef = 2.26e-4
    pressure = 101325

    rhos = get_rho(temperature, pressure, r_medium)
    n_medium = get_refractive_index(gd_coef, rhos)
    n_air = 1.00027717
    plt.plot(temperature, n_medium, c="red")
    plt.axhline(1.00027717, c="k")
    plt.axhline(1.000449, c="green")
    plt.show()

    plt.plot(temperature, (n_medium - 1.00027717) / 1.00027717, c="red")
    plt.show()

    deflection = (np.cos(n_medium - 1.00027717) / 1.00027717) * 2.4
    print(deflection)
    plt.plot(temperature, deflection, c="red")
    plt.show()

main()