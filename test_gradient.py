import numpy as np
import pandas as pd
from copy import deepcopy
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc

k_boltz = 1.63e-23
eV = 1.602E-19
MPa = 1E6
Angstrom = 1E-10

T_kelvin = 293
lamb = burgers = 2.86378*Angstrom
G = 49765.7 * MPa

f_rho = 2
f_tau = 3

def waiting_time(values, density, ref_stress):
    c_length = values[1]
    mfp_0 = c_length / np.sqrt(1e12)
    mfp = c_length / np.sqrt(f_rho*density)
    freq_ref = values[0]
    Q_ref = values[2]
    tau_P = values[3]
    xi = values[4]
    c_back = values[7]
    tau_c = c_back * G * burgers * np.sqrt(f_tau*density)
    tau_eff = abs(ref_stress * tau_c) - tau_c
    Q_act = Q_ref * (1-np.sign(tau_eff) * (abs(tau_eff)/tau_P)**xi)
    Q_act[Q_act > 500*T_kelvin*k_boltz] = 500*T_kelvin*k_boltz
    Q_act[Q_act < -500*T_kelvin*k_boltz] = -500*T_kelvin*k_boltz
    return (1 / freq_ref) * np.exp(Q_act/(T_kelvin*k_boltz))

def running_time(values, density, ref_stress):
    c_length = values[1]
    speed_sat = values[5]
    c_drag = values[6]
    c_back = values[7]
    tau_eff = abs(ref_stress * c_back * G * burgers * np.sqrt(f_tau*density)) - c_back * G * burgers * np.sqrt(f_tau*density)
    coeff_B = (c_drag * k_boltz * T_kelvin) / (speed_sat * burgers**2)
    v_norm = 2 * burgers * tau_eff / (coeff_B * speed_sat)
    v_norm[v_norm < 1e-40] = 1e-40
    mean_free_path = c_length / np.sqrt(f_rho*density)
    velocity = speed_sat * (np.sqrt(1 + (1/v_norm**2) )- 1/v_norm)
    velocity[velocity < 1e-40] = 1e-40
    return mean_free_path / velocity

def time_proportion(values, density, ref_stress):
    c_length = values[1]
    mfp = c_length / np.sqrt(f_rho*density)
    waiting = waiting_time(values, density, ref_stress)
    running = running_time(values, density, ref_stress)
    return waiting/(waiting+running), mfp / (waiting+running)

def velocity(values, density, ref_stress):
    c_length = values[1]
    mfp = c_length / np.sqrt(f_rho*density)
    waiting = waiting_time(values, density, ref_stress)
    running = running_time(values, density, ref_stress)
    return mfp/(waiting+running)

def time_values(values, density, ref_stress):
    waiting = waiting_time(values, density, ref_stress)
    running = running_time(values, density, ref_stress)
    return waiting, running

def greyscale_plot(sep_data):
    # Extracting the data
    data = np.vstack(sep_data)
    dislocation_density = data[:, 0]
    strain_rate = data[:, 2]
    time_fraction = data[:, 1]
    colormap = cmc.batlow

    plt.figure(figsize=(10, 8))
    # Create a contour plot
    plt.tricontourf(np.log10(dislocation_density), np.log10(strain_rate), 1-time_fraction, cmap=colormap, vmin = 0., vmax = 1., levels=100)
    #plt.tricontourf(np.log10(dislocation_density), (strain_rate), 1-time_fraction, cmap=cmc.batlowW, vmin = 0.1, vmax = 0.9, levels=100)
    plt.ylim((-3,10))
    #plt.xscale("log")
    #plt.yscale("log")
    # plt.plot(np.log10(sep_data[-1][:,0]), np.log10(sep_data[-1][:,2]))
    # plt.plot(np.log10(sep_data[0][:,0]), np.log10(sep_data[0][:,2]))

    # Add white cover
    plt.fill_between(np.log10(sep_data[-1][:,0]), np.ones_like(sep_data[-1][:,0])*-8, np.log10(sep_data[-1][:,2]), color=colormap(0.))
    plt.fill_between(np.log10(sep_data[0][:,0]), np.ones_like(sep_data[-1][:,0])*15, np.log10(sep_data[0][:,2]), color=colormap(1.))
    #
    # Add colorbar
    plt.colorbar()

    # Set labels and title
    plt.xlabel("Dislocation Density (log scale)")
    plt.ylabel("Strain Rate")
    plt.title("Contour Map of Dislocation Density, Strain Rate, and Time Fraction")
    
    # Show the plot
    plt.show()

def greyscale_plot_velocity(sep_data):
    # Extracting the data
    print(sep_data)
    data = sep_data
    pd.DataFrame(data).to_csv("data.csv")
    dislocation_density = data[:, 0]
    velocity = data[:, 2]
    time_fraction = data[:, 1]

    plt.figure(figsize=(10, 8))
    # Create a contour plot
    # plt.tricontourf(np.log10(dislocation_density), (velocity), 1-time_fraction, cmap=cmc.batlowW, vmin = 0., vmax = 1, levels=100)
    plt.scatter(np.log10(dislocation_density), (velocity), c=1-time_fraction, cmap=cmc.batlowW, vmin = 0., vmax = 1, s=10)
    #plt.xscale("log")
    plt.yscale("log")
    # Add white cover
    
    # Add colorbar
    plt.colorbar()

    # Set labels and title
    plt.xlabel("Dislocation Density (log scale)")
    plt.ylabel("velocity m/s")
    plt.title("Contour Map of Dislocation Density, Strain Rate, and Time Fraction")
    
    # Show the plot
    plt.show()


def interpolate_strain_rates(data, keypoint):
    strain_rate = data[:, 0]
    time_fraction = data[:, 1]

    keypoint_cutoff = deepcopy(keypoint)
    keypoint_cutoff[keypoint < np.min(time_fraction)] = np.min(time_fraction)

    # Sort the data based on the 'time_fraction' column
    sorted_indices = np.argsort(time_fraction)
    sorted_time_fraction = time_fraction[sorted_indices]
    sorted_strain_rate = strain_rate[sorted_indices]

    interpolation_func = interp1d(sorted_time_fraction, sorted_strain_rate)
    strain_rate_keypoint = interpolation_func(keypoint_cutoff)
    return strain_rate_keypoint

def poly_fit(data):
    coef = np.polyfit(np.log10(data[:,0]), np.log10(data[:,2]), deg=3)
    func = np.poly1d(coef)
    x_data = np.log10(data[:,0])
    y_data = func(x_data)
    return np.hstack((data[:,0].reshape(-1,1), data[:,1].reshape(-1,1), 10**y_data.reshape(-1,1)))

def bound_plot(data):
    density = data[:, 0]
    lower_bound = data[:, 1]
    upper_bound = data[:, 2]
    fig, ax = plt.subplots()

    # Polynomial fitting for the 1-2 curve
    coef_1_2 = np.polyfit(np.log10(density), np.log10(lower_bound), deg=3)
    f_1_2 = np.poly1d(coef_1_2)
    x_1_2 = np.log10(density)
    y_1_2 = f_1_2(x_1_2)
    ax.plot(10**x_1_2, 10**y_1_2, label='1-2 curve')

    # Polynomial fitting for the 1-3 curve
    coef_1_3 = np.polyfit(np.log10(density), np.log10(upper_bound), deg=3)
    f_1_3 = np.poly1d(coef_1_3)
    x_1_3 = np.log10(density)
    y_1_3 = f_1_3(x_1_3)
    ax.plot(10**x_1_3, 10**y_1_3, label='1-3 curve')

    ax.set_xlabel('Density')
    ax.set_ylabel('Value')
    plt.xscale('log')
    plt.yscale('log')

    ax.legend()
    plt.show()

def seperate_array(data, number, by):
    data_rearrange = data[np.lexsort((data[:,0],data[:,by]))]
    return np.array_split(data_rearrange, data_rearrange.shape[0]/number)

def time_fraction_data_preparation(parameters, rho, frac_vec, ismooth = True):
    stress = np.arange(0.5,10.,0.0001)
    contour_data = []
    for irho in rho:
        result, velocity = time_proportion(parameters, irho, stress)
        rate = irho * velocity * burgers
        merge_matrix = np.hstack((rate.reshape(-1,1), result.reshape(-1,1)))
        rate_vec = interpolate_strain_rates(merge_matrix, frac_vec)
        contour_data.append(np.hstack((np.ones((len(frac_vec),1))*irho, frac_vec.reshape(-1,1), rate_vec.reshape(-1,1))))
    contour_data = np.vstack(contour_data)
    pd.DataFrame(contour_data, columns=['rho', 'frac', 'rate']).to_csv("data.csv")
    data_seperate = seperate_array(contour_data, len(rho), 1)
    new_data = []
    for idata in data_seperate:
        if ismooth == True:
            new_data.append(poly_fit(idata))
        else:
            new_data.append(idata)
    return new_data, contour_data


def time_fraction_data_preparation_v(parameters, rho, frac_vec):
    stress = np.arange(0.9,1.2,0.0001)
    contour_data = []
    for irho in rho:
        result, velocity = time_proportion(parameters, irho, stress)
        # rate = irho * velocity * burgers
        rate = velocity
        rho_vector = np.ones(len(rate)) * irho
        merge_matrix = np.hstack((rate.reshape(-1,1), result.reshape(-1,1)))
        rate_vec = interpolate_strain_rates(merge_matrix, frac_vec)
        # contour_data.append(np.hstack((np.ones((len(frac_vec),1))*irho, frac_vec.reshape(-1,1), rate_vec.reshape(-1,1))))
        contour_data.append(np.hstack((rho_vector.reshape(-1,1), result.reshape(-1,1), rate.reshape(-1,1))))
        plt.plot(rate, result, label=str(irho))
    contour_data = np.vstack(contour_data)
    data_seperate = seperate_array(contour_data, len(rho), 1)
    new_data = []
    for idata in data_seperate:
        #new_data.append(poly_fit(idata))
        new_data.append(idata)
    return new_data, contour_data

def get_stress_velo_data(parameters, rho):
    stress = np.arange(0.5,2,0.001)
    adf = pd.DataFrame(columns=['Stress']+np.array(rho).astype(str).tolist())
    adf['Stress'] = stress
    for irho in rho:
        c_back = parameters[7]
        tau_c = c_back * G * burgers * np.sqrt(f_tau*irho)
        velo_data = velocity(parameters, irho, stress)
        plt.plot(stress*tau_c, velo_data, label=str(irho))
        adf[str(irho)] = velo_data
    adf.to_csv('stress_velo.csv', index=False)
    plt.show()

def get_time_data(parameters, rho):
    stress = np.arange(0.05, 20, 0.05)
    columns = [str(irho)+'_tw' for irho in rho] + [str(irho)+'_tr' for irho in rho]
    adf = pd.DataFrame(columns=['Stress']+columns)
    adf['Stress'] = stress
    for irho in rho:
        c_back = parameters[7]
        tau_c = c_back * G * burgers * np.sqrt(f_tau*irho)
        tw, tr = time_values(parameters, irho, stress)
        plt.plot(stress*tau_c, tw, label=str(irho)+'_tw')
        plt.plot(stress*tau_c, tr, label=str(irho)+'_tr')
        adf[str(irho)+'_tw'] = tw
        adf[str(irho)+'_tr'] = tr
    plt.yscale('log')
    plt.legend()
    adf.to_csv('stress_time.csv', index=False)
    plt.show()


def plot_greyscale_rate(parameters, rho, frac_vec, ismooth = True):
    new_data, contour_data = time_fraction_data_preparation(parameters, rho, frac_vec, ismooth)
    # bound_plot(contour_data)
    greyscale_plot(new_data)


def plot_greyscale_vel(parameters, rho, frac_vec):
    new_data, contour_data = time_fraction_data_preparation_v(parameters, rho, frac_vec)
    # bound_plot(contour_data)
    greyscale_plot_velocity(contour_data)

if __name__ == "__main__":
    # nu_r, c_l, Q_0, tau_P, xi, v_s, c_d, c_b
    frac_vec = np.arange(0.,1.,0.01)
    parameters = [1e14, 1., 2.8*eV, 1.*MPa, 0.8, 1800, 0.85, 0.075]
    rho = np.array([i*10**k for k in range(10,16) for i in range(1, 10)])
    plot_greyscale_rate(parameters, rho, frac_vec, ismooth=False) # Enable to plot the greyscale plot for the rate
    # plot_greyscale_vel(parameters, rho, frac_vec) # Enable to plot the greyscale plot for the velocity
    # get_stress_velo_data(parameters, [1e12,1e13,1e14,1e15])
    # get_time_data(parameters, [1e12,1e13,1e14,1e15])
