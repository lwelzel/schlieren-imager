import numpy as np
import matplotlib.pyplot as plt

### data on GD coefficients from 10.1016/j.combustflame.2018.06.022

def get_rho(temperature, pressure=1., specific_gas_constant=1.):
    return pressure / (temperature * specific_gas_constant)

def get_refractive_index(k, rho):
    return k * rho + 1

def main():
    temperature = np.linspace(20, 500, 100) + 273.15

    r_medium_co2 = 188.92  # CO2
    gd_coef_co2 = 2.26e-4

    r_medium_co = 296.84  # CO
    gd_coef_co = 2.67e-4

    r_medium_h20 = 461.5  # H2O
    gd_coef_h20 = 3.12e-4

    r_medium_h2 = 4124.2  # H2
    gd_coef_h2 = 1.54e-4

    r_medium_n2 = 296.80  # N2
    gd_coef_n2 = 2.38e-4

    r_medium_k2co3 = 0.  # K2CO3
    gd_coef_k2co3 = 0.e-4

    rs = np.array([r_medium_co2, r_medium_co, r_medium_h20, r_medium_h2, r_medium_n2])
    gds = np.array([gd_coef_co2, gd_coef_co, gd_coef_h20, gd_coef_h2, gd_coef_n2])
    weights = np.array([3.8, 5.21, 7.79, 3.07, 3.14])

    pressure = 101325

    medium_depth = 0.05

    n_air = 1.00027717
    n_co2 = 1.00045
    n_co = 1.00035
    n_n2 = 1.00029

    rhos = np.zeros((5, temperature.size))
    n_media = np.zeros((5, temperature.size))
    angles = np.zeros((5, temperature.size))
    deflections = np.zeros((5, temperature.size))
    names = ["CO2", "CO", "H2O", "H2", "N2"]

    fig, axes = plt.subplots(nrows=2, ncols=2,
                             constrained_layout=True,
                             figsize=(12, 12))  # figsize=(width, height)

    axes = np.array(axes).flatten()
    ax0, ax1, ax2, ax3 = axes

    for i, (r, gd, name) in enumerate(zip(rs, gds, names)):

        rho = get_rho(temperature, pressure, r)
        n_medium = get_refractive_index(gd, rho)
        angle = 2 * medium_depth * (n_medium - n_air) / n_air
        deflection = np.tan(angle) * 2.4

        rhos[i] = rho
        n_media[i] = n_medium
        angles[i] = angle
        deflections[i] = deflection

        ax0.plot(temperature, rho, label=name)
        ax1.plot(temperature, n_medium, label=name)
        ax2.plot(temperature, angle * 60., label=name)
        ax3.plot(temperature, deflection * 1000., label=name)


    mean_angle = np.average(angles, weights=weights, axis=0)
    mean_deflection = np.average(deflections,  weights=weights, axis=0)

    # mean_angle = np.mean(angles, axis=0)
    # mean_deflection = np.mean(deflections, axis=0)

    ax0.set_xlabel('T [K]')
    ax0.set_ylabel(r'$\rho$ [kg/m$^3$]')
    ax0.set_title('Density at 1 atm.')


    ax1.axhline(n_air, ls="dashed", label="Air (ref at 273K)",
                color=next(ax1._get_lines.prop_cycler)['color'])
    ax1.axhline(n_co2, ls="dashed", label=r"CO2 (ref at 273K)",
                color=next(ax1._get_lines.prop_cycler)['color'])
    ax1.axhline(n_co, ls="dashed", label="CO (ref at 273K)",
                color=next(ax1._get_lines.prop_cycler)['color'])
    ax1.axhline(n_n2, ls="dashed", label="N2 (ref at 273K)",
                color=next(ax1._get_lines.prop_cycler)['color'])
    ax1.set_xlabel('T [K]')
    ax1.set_ylabel('n [-]')
    ax1.set_title('Refractive index.')
    # ax1.set_ylim(1.00015, 1.00055)

    ax2.plot(temperature, mean_angle * 60., ls="dotted", c="gray", label="avg angle")
    ax2.axhline(0., ls="dashed",
                color="k")
    ax2.set_xlabel('T [K]')
    ax2.set_ylabel(r'$\epsilon$ [arcmin]')
    ax2.set_title('Deflection angle.')

    ax3.plot(temperature, mean_deflection * 1000., ls="dotted", c="gray", label="avg deflection")
    ax3.axhline(0., ls="dashed",
                color="k")
    ax3.set_xlabel('T [K]')
    ax3.set_ylabel(r'$\Delta e$ [mm]')
    ax3.set_title('Deflection at 2f.')

    for ax in axes:
        ax.legend()


    fig.suptitle('Schlieren performance\n- BOE estimations at ~600 nm, 5cm medium -', fontsize=18, weight="bold")
    plt.show()

main()