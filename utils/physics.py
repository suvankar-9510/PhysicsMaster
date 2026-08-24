"""
PhysicsMaster - Core Physics Computational Engine
Graduate & M.Sc Standard Analytical & Numerical Physics Solvers
"""

import numpy as np
from scipy import constants
from scipy.integrate import quad


# ============================================================================
# 1. CRYSTALLOGRAPHY & DIFFRACTION
# ============================================================================

def calculate_bragg_angle(d_spacing, wavelength, order=1):
    """
    Calculate the Bragg angle using Bragg's law: n*lambda = 2*d*sin(theta).
    
    Parameters:
    -----------
    d_spacing : float (Angstroms)
    wavelength : float (Angstroms)
    order : int
    
    Returns:
    --------
    float: Bragg angle in radians (or np.nan if evanescent)
    """
    sin_theta = (order * wavelength) / (2.0 * d_spacing)
    if abs(sin_theta) <= 1.0:
        return np.arcsin(sin_theta)
    return np.nan


def calculate_structure_factor(h, k, l, lattice_type="FCC", basis_type="monatomic"):
    """
    Calculate the geometric structure factor F_hkl and check extinction rules.
    
    F_hkl = sum_j f_j * exp(-2*pi*i*(h*u_j + k*v_j + l*w_j))
    """
    if lattice_type == "Simple Cubic":
        # Basis at (0,0,0)
        return 1.0, True, "All reflections allowed"
    
    elif lattice_type == "BCC":
        # Basis at (0,0,0) and (1/2, 1/2, 1/2)
        # F = f * (1 + exp(-i*pi*(h+k+l))) = f * (1 + (-1)^(h+k+l))
        is_allowed = (h + k + l) % 2 == 0
        intensity_factor = 4.0 if is_allowed else 0.0
        msg = "Allowed: h+k+l is even" if is_allowed else "Extinct: h+k+l is odd"
        return intensity_factor, is_allowed, msg
    
    elif lattice_type == "FCC":
        # Basis at (0,0,0), (1/2, 1/2, 0), (1/2, 0, 1/2), (0, 1/2, 1/2)
        # F = 4f if h,k,l are unmixed (all even or all odd), else 0
        h_even, k_even, l_even = (h % 2 == 0), (k % 2 == 0), (l % 2 == 0)
        is_allowed = (h_even == k_even == l_even)
        intensity_factor = 16.0 if is_allowed else 0.0
        msg = "Allowed: h,k,l unmixed" if is_allowed else "Extinct: h,k,l mixed parity"
        return intensity_factor, is_allowed, msg
    
    elif lattice_type == "Diamond Cubic":
        # FCC lattice with 2-atom basis: (0,0,0) and (1/4, 1/4, 1/4)
        h_even, k_even, l_even = (h % 2 == 0), (k % 2 == 0), (l % 2 == 0)
        if h_even == k_even == l_even:
            if not h_even:  # All odd
                intensity_factor = 32.0  # 4 * sqrt(2)^2 * 4 = 32
                return intensity_factor, True, "Allowed: h,k,l all odd"
            else:  # All even
                if (h + k + l) % 4 == 0:
                    return 64.0, True, "Allowed: h,k,l all even and h+k+l = 4n"
                else:
                    return 0.0, False, "Extinct: h+k+l = 4n+2"
        return 0.0, False, "Extinct: mixed parity"
    
    elif lattice_type == "NaCl":
        # Na at FCC positions, Cl at FCC + (1/2, 0, 0)
        h_even, k_even, l_even = (h % 2 == 0), (k % 2 == 0), (l % 2 == 0)
        if h_even == k_even == l_even:
            if not h_even:
                return 16.0, True, "Allowed: |f_Na - f_Cl|^2 (all odd)"
            else:
                return 32.0, True, "Allowed: |f_Na + f_Cl|^2 (all even)"
        return 0.0, False, "Extinct: mixed parity"
    
    return 1.0, True, "Allowed"


# ============================================================================
# 2. THERMAL DYNAMICS & LATTICE SPECIFIC HEAT
# ============================================================================

def debye_integrand(x):
    """Integrand for Debye specific heat: x^4 * e^x / (e^x - 1)^2."""
    if x < 1e-6:
        return x**2
    if x > 100:
        return 0.0
    ex = np.exp(x)
    return (x**4 * ex) / (ex - 1.0)**2


def calculate_debye_heat_capacity(temperature, debye_temp, n_atoms=1.0):
    """
    Calculate the lattice specific heat C_V(T) using the exact Debye model.
    C_V = 9 * N * k_B * (T / Theta_D)^3 * int_0^{Theta_D/T} (x^4 e^x / (e^x - 1)^2) dx
    
    Returns:
    --------
    float: Specific heat in J / (mol * K)
    """
    R = 8.314462618  # Gas constant J/(mol*K)
    if temperature <= 1e-4:
        return 0.0
    
    xD = debye_temp / temperature
    if xD > 150.0:
        # Low temperature T^3 asymptotic limit: (12 * pi^4 / 5) * R * (T / Theta_D)^3
        return (12.0 * np.pi**4 / 5.0) * R * (temperature / debye_temp)**3
    
    if xD < 0.05:
        # High temperature Dulong-Petit limit: 3 * R * (1 - xD^2 / 20)
        return 3.0 * R * (1.0 - xD**2 / 20.0)
    
    # Exact numerical quadrature
    integral, _ = quad(debye_integrand, 0.0, xD, epsabs=1e-8, epsrel=1e-8, limit=100)
    cv = 9.0 * R * (temperature / debye_temp)**3 * integral
    return cv


def calculate_einstein_heat_capacity(temperature, einstein_temp):
    """
    Calculate the lattice specific heat C_V(T) using the Einstein model.
    C_V = 3 * R * (Theta_E / T)^2 * (e^(Theta_E / T) / (e^(Theta_E / T) - 1)^2)
    """
    R = 8.314462618
    if temperature <= 1e-4:
        return 0.0
    xE = einstein_temp / temperature
    if xE > 150.0:
        return 0.0
    ex = np.exp(xE)
    return 3.0 * R * xE**2 * ex / (ex - 1.0)**2


def calculate_electronic_specific_heat(temperature, gamma_coeff):
    """
    Calculate electronic specific heat C_e = gamma * T.
    gamma_coeff in mJ / (mol * K^2).
    """
    return (gamma_coeff * 1e-3) * temperature


# ============================================================================
# 3. ELECTRONIC BAND THEORY & KRONIG-PENNEY
# ============================================================================

def solve_kronig_penney(P_barrier, energy_max=25.0, n_points=500):
    """
    Solve the 1D Kronig-Penney delta-potential model:
    cos(ka) = P * sin(alpha*a)/(alpha*a) + cos(alpha*a)
    where alpha*a = sqrt(2mE/hbar^2) * a.
    
    Parameters:
    -----------
    P_barrier : float (Barrier strength parameter P = m V_0 b a / hbar^2)
    energy_max : float
    n_points : int
    
    Returns:
    --------
    dict with alpha_a, f_val, allowed_mask, ka_vals, energy_bands
    """
    alpha_a = np.linspace(0.01, np.sqrt(energy_max) * np.pi, n_points)
    f_val = P_barrier * np.sin(alpha_a) / alpha_a + np.cos(alpha_a)
    
    allowed = np.abs(f_val) <= 1.0
    ka = np.full_like(alpha_a, np.nan)
    ka[allowed] = np.arccos(f_val[allowed])
    
    # Energy in normalized units (alpha*a / pi)^2
    energy = (alpha_a / np.pi)**2
    
    return {
        "alpha_a": alpha_a,
        "f_val": f_val,
        "allowed": allowed,
        "ka": ka,
        "energy": energy
    }


def tight_binding_1d(k_array, a=1.0, E0=0.0, t=1.0):
    """1D s-band Tight Binding dispersion: E(k) = E0 - 2*t*cos(k*a)."""
    return E0 - 2.0 * t * np.cos(k_array * a)


def tight_binding_2d_square(kx_grid, ky_grid, a=1.0, E0=0.0, t=1.0):
    """2D Square lattice Tight Binding: E(kx, ky) = E0 - 2*t*(cos(kx*a) + cos(ky*a))."""
    return E0 - 2.0 * t * (np.cos(kx_grid * a) + np.cos(ky_grid * a))


def tight_binding_graphene(kx_grid, ky_grid, a=1.42, t=2.8):
    """
    Graphene Tight-Binding dispersion (pi and pi* bands):
    E_pm(k) = pm t * sqrt(1 + 4*cos(sqrt(3)*ky*a/2)*cos(3*kx*a/2) + 4*cos^2(sqrt(3)*ky*a/2))
    """
    term = 1.0 + 4.0 * np.cos(np.sqrt(3.0) * ky_grid * a / 2.0) * np.cos(3.0 * kx_grid * a / 2.0) + \
           4.0 * (np.cos(np.sqrt(3.0) * ky_grid * a / 2.0))**2
    gamma_k = np.sqrt(np.maximum(0.0, term))
    E_conduction = t * gamma_k
    E_valence = -t * gamma_k
    return E_valence, E_conduction


def calculate_carrier_concentration(doping_type, doping_concentration, temperature):
    """Calculate electron and hole concentrations in semiconductor (Si model)."""
    Eg = 1.12  # eV
    kB = 8.617333e-5  # eV/K
    ni = 5.2e19 * (temperature / 300.0)**1.5 * np.exp(-Eg / (2.0 * kB * max(temperature, 1.0)))
    
    if doping_type == "n-type":
        Nd = doping_concentration
        n0 = 0.5 * (Nd + np.sqrt(Nd**2 + 4.0 * ni**2))
        p0 = ni**2 / max(n0, 1e-10)
    elif doping_type == "p-type":
        Na = doping_concentration
        p0 = 0.5 * (Na + np.sqrt(Na**2 + 4.0 * ni**2))
        n0 = ni**2 / max(p0, 1e-10)
    else:  # Intrinsic
        n0 = ni
        p0 = ni
        
    return n0, p0


def calculate_mobility(carrier_type, temperature):
    """Calculate carrier mobility in Silicon vs temperature."""
    T_ratio = 300.0 / max(temperature, 10.0)
    if carrier_type == "electron":
        return 1400.0 * (T_ratio**2.5)
    return 450.0 * (T_ratio**2.5)


def calculate_band_structure(material, lattice_spacing, bandgap_type="Direct", k_points=150, custom_potential=None):
    """Calculate band structure for Silicon, Germanium, GaAs, or Custom."""
    k_path = np.linspace(-np.pi / lattice_spacing, np.pi / lattice_spacing, k_points)
    
    if material == "Silicon":
        t = 1.1
        bandgap = 1.12
        Ev = -bandgap / 2.0 - 2.0 * t * np.cos(k_path * lattice_spacing)
        Ec = bandgap / 2.0 + 2.0 * t * np.cos((k_path - 0.85 * np.pi / lattice_spacing) * lattice_spacing)
        is_direct = False
    elif material == "Germanium":
        t = 1.2
        bandgap = 0.66
        Ev = -bandgap / 2.0 - 2.0 * t * np.cos(k_path * lattice_spacing)
        Ec = bandgap / 2.0 + 2.0 * t * np.cos((k_path - 0.7 * np.pi / lattice_spacing) * lattice_spacing)
        is_direct = False
    elif material == "GaAs":
        t = 1.4
        bandgap = 1.42
        Ev = -bandgap / 2.0 - 2.0 * t * np.cos(k_path * lattice_spacing)
        Ec = bandgap / 2.0 + 2.0 * t * np.cos(k_path * lattice_spacing)
        is_direct = True
    else:  # Custom
        t = (custom_potential / 4.0) if custom_potential else 1.0
        bandgap = custom_potential if custom_potential else 2.0
        Ev = -bandgap / 2.0 - 2.0 * t * np.cos(k_path * lattice_spacing)
        if bandgap_type == "Indirect":
            Ec = bandgap / 2.0 + 2.0 * t * np.cos((k_path - 0.6 * np.pi / lattice_spacing) * lattice_spacing)
            is_direct = False
        else:
            Ec = bandgap / 2.0 + 2.0 * t * np.cos(k_path * lattice_spacing)
            is_direct = True
            
    actual_bandgap = np.min(Ec) - np.max(Ev)
    return k_path, Ev, Ec, actual_bandgap, is_direct


def calculate_electron_wavefunction(k_point, band_type, lattice_spacing, x_points=300):
    """Calculate 1D Bloch wavefunction psi(x) = u(x) * exp(i*k*x)."""
    x = np.linspace(0, 6 * lattice_spacing, x_points)
    k_val = k_point * np.pi / lattice_spacing
    
    # Periodic atomic potential modulation u(x)
    u_x = np.cos(2.0 * np.pi * x / lattice_spacing) + 1.2
    
    if band_type == "Valence":
        psi = u_x * np.cos(k_val * x) * np.exp(-0.05 * x / lattice_spacing)
    else:
        psi = u_x * np.sin(k_val * x) * np.exp(-0.05 * x / lattice_spacing)
        
    prob_density = psi**2
    atom_positions = np.arange(0, 7 * lattice_spacing, lattice_spacing)
    return x, psi, prob_density, atom_positions


# ============================================================================
# 4. MAGNETIC RESONANCE & SPIN DYNAMICS (NMR, EPR/ESR, FMR)
# ============================================================================

def solve_bloch_equations(t_max=50.0, n_steps=1000, B0=1.0, B1=0.1, omega_rf=1.0,
                          omega_0=1.0, T1=20.0, T2=5.0, M0=1.0, pulse_duration=1.57):
    """
    Numerically solve the Bloch equations using 4th-order Runge-Kutta (RK4).
    
    dMx/dt = (gamma*B0 - omega_rf)*My - Mx/T2
    dMy/dt = -(gamma*B0 - omega_rf)*Mx + gamma*B1*Mz - My/T2
    dMz/dt = -gamma*B1*My - (Mz - M0)/T1
    (written in the rotating frame of reference with Delta_omega = omega_0 - omega_rf).
    
    Returns:
    --------
    dict with time, Mx, My, Mz, M_transverse, M_magnitude
    """
    dt = t_max / n_steps
    t = np.linspace(0, t_max, n_steps)
    
    Mx = np.zeros(n_steps)
    My = np.zeros(n_steps)
    Mz = np.zeros(n_steps)
    
    # Initial state along +z axis (equilibrium magnetization)
    Mx[0] = 0.0
    My[0] = 0.0
    Mz[0] = M0
    
    delta_w = omega_0 - omega_rf
    
    def derivatives(state, current_t):
        x, y, z = state
        # Apply B1 RF field only during pulse duration
        b1_eff = B1 if current_t <= pulse_duration else 0.0
        
        dx = delta_w * y - x / T2
        dy = -delta_w * x + b1_eff * z - y / T2
        dz = -b1_eff * y - (z - M0) / T1
        return np.array([dx, dy, dz])
    
    # RK4 Integration
    for i in range(n_steps - 1):
        s = np.array([Mx[i], My[i], Mz[i]])
        ti = t[i]
        
        k1 = derivatives(s, ti)
        k2 = derivatives(s + 0.5 * dt * k1, ti + 0.5 * dt)
        k3 = derivatives(s + 0.5 * dt * k2, ti + 0.5 * dt)
        k4 = derivatives(s + dt * k3, ti + dt)
        
        s_next = s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        Mx[i+1], My[i+1], Mz[i+1] = s_next
        
    M_perp = np.sqrt(Mx**2 + My**2)
    M_total = np.sqrt(Mx**2 + My**2 + Mz**2)
    
    return {
        "time": t,
        "Mx": Mx,
        "My": My,
        "Mz": Mz,
        "M_transverse": M_perp,
        "M_magnitude": M_total
    }


def simulate_hahn_echo(tau=15.0, T2=25.0, T1=60.0, n_isochromats=50, t_max=40.0, n_points=800):
    """
    Simulate the Hahn Spin Echo pulse sequence (90_x - tau - 180_y - tau).
    Demonstrates spin dephasing due to inhomogeneous Delta B_0 and refocusing at t = 2*tau.
    """
    t = np.linspace(0, t_max, n_points)
    dt = t[1] - t[0]
    
    # Inhomogeneous frequency distribution (Gaussian spread around center)
    delta_omegas = np.random.normal(0.0, 1.2, n_isochromats)
    
    # Track isochromats transverse magnetization
    total_Mx = np.zeros(n_points)
    total_My = np.zeros(n_points)
    isochromat_traces = []
    
    tau_idx = int(tau / dt)
    echo_idx = int(2.0 * tau / dt)
    
    for dw in delta_omegas:
        Mx_iso = np.zeros(n_points)
        My_iso = np.zeros(n_points)
        
        # After 90_x pulse at t=0: vector is along +y
        Mx_iso[0] = 0.0
        My_iso[0] = 1.0
        
        phase = 0.0
        for i in range(n_points - 1):
            ti = t[i]
            # Dephasing & T2 decay
            decay = np.exp(-dt / T2)
            
            if i == tau_idx:
                # 180_y pulse: invert x-phase (refocusing)
                Mx_iso[i] = -Mx_iso[i]
                # My remains unchanged under 180_y
            
            # Rotation by dw*dt
            d_phi = dw * dt
            new_x = (Mx_iso[i] * np.cos(d_phi) + My_iso[i] * np.sin(d_phi)) * decay
            new_y = (-Mx_iso[i] * np.sin(d_phi) + My_iso[i] * np.cos(d_phi)) * decay
            
            Mx_iso[i+1] = new_x
            My_iso[i+1] = new_y
            
        total_Mx += Mx_iso
        total_My += My_iso
        if len(isochromat_traces) < 6:
            isochromat_traces.append((Mx_iso, My_iso))
            
    total_Mx /= n_isochromats
    total_My /= n_isochromats
    echo_signal = np.sqrt(total_Mx**2 + total_My**2)
    
    return {
        "time": t,
        "echo_signal": echo_signal,
        "isochromat_traces": isochromat_traces,
        "tau": tau,
        "echo_time": 2.0 * tau
    }


def calculate_epr_hyperfine_spectrum(g_factor=2.0023, spin_I=0.5, n_nuclei=1, a_hyperfine=30.0,
                                      linewidth=4.0, B_center=3480.0, B_range=200.0, n_points=1000):
    """
    Calculate an EPR / ESR absorption and 1st derivative spectrum with Hyperfine coupling.
    Splitting produces (2 * n * I + 1) lines with binomial intensities for equivalent nuclei.
    """
    B = np.linspace(B_center - B_range / 2.0, B_center + B_range / 2.0, n_points)
    
    # Calculate number of peaks and relative intensities
    n_lines = int(2 * n_nuclei * spin_I + 1)
    
    # Multiplicity binomial coefficients
    if n_nuclei == 1:
        intensities = np.ones(n_lines)
    elif n_nuclei == 2 and spin_I == 0.5:
        intensities = np.array([1.0, 2.0, 1.0])
    elif n_nuclei == 3 and spin_I == 0.5:
        intensities = np.array([1.0, 3.0, 3.0, 1.0])
    elif n_nuclei == 4 and spin_I == 0.5:
        intensities = np.array([1.0, 4.0, 6.0, 4.0, 1.0])
    else:
        # Generic Pascal approximation
        intensities = np.array([math.comb(n_lines - 1, i) for i in range(n_lines)])
        
    intensities = intensities / np.max(intensities)
    
    # Peak positions
    offsets = (np.arange(n_lines) - (n_lines - 1) / 2.0) * a_hyperfine
    
    absorption = np.zeros_like(B)
    for pos_offset, ampl in zip(offsets, intensities):
        b0 = B_center + pos_offset
        # Lorentzian line shape
        lor = ampl / (1.0 + ((B - b0) / (linewidth / 2.0))**2)
        absorption += lor
        
    # First derivative spectrum (standard EPR display)
    derivative = np.gradient(absorption, B)
    derivative = derivative / (np.max(np.abs(derivative)) + 1e-12)
    
    return {
        "magnetic_field": B,
        "absorption": absorption,
        "derivative": derivative,
        "n_lines": n_lines,
        "peak_positions": B_center + offsets
    }


def calculate_fmr_kittel(B0_array, Ms=800.0, gamma=28.0, geometry="In-plane Thin Film"):
    """
    Calculate Ferromagnetic Resonance (FMR) frequency vs applied magnetic field B0 (in kG / Tesla).
    Uses the Kittel resonance equations:
    - In-plane Thin Film: omega/gamma = sqrt(B0 * (B0 + 4*pi*Ms))
    - Out-of-plane Thin Film: omega/gamma = B0 - 4*pi*Ms  (for B0 > 4*pi*Ms)
    - Sphere: omega/gamma = B0
    
    Parameters:
    -----------
    B0_array : array (in Gauss / kG)
    Ms : float (Saturation magnetization 4*pi*Ms in Gauss)
    gamma : float (Gyromagnetic ratio in GHz / Tesla or MHz / Gauss)
    """
    if geometry == "In-plane Thin Film":
        freq = gamma * np.sqrt(B0_array * (B0_array + Ms))
    elif geometry == "Out-of-plane Thin Film":
        freq = np.maximum(0.0, gamma * (B0_array - Ms))
    else:  # Sphere
        freq = gamma * B0_array
        
    return freq


# ============================================================================
# 5. DIELECTRICS, POLARIZATION & FERROELECTRICITY
# ============================================================================

def calculate_debye_dielectric_dispersion(freq_array, eps_static=10.0, eps_optical=2.5, tau_relaxation=1e-10):
    """
    Calculate complex dielectric permittivity using the Debye relaxation model:
    eps*(omega) = eps_inf + (eps_s - eps_inf) / (1 + i * omega * tau)
    eps'(omega)  = eps_inf + (eps_s - eps_inf) / (1 + omega^2 * tau^2)
    eps''(omega) = (eps_s - eps_inf) * omega * tau / (1 + omega^2 * tau^2)
    tan_delta    = eps'' / eps'
    """
    omega = 2.0 * np.pi * freq_array
    wt = omega * tau_relaxation
    denom = 1.0 + wt**2
    
    eps_real = eps_optical + (eps_static - eps_optical) / denom
    eps_imag = (eps_static - eps_optical) * wt / denom
    loss_tangent = eps_imag / eps_real
    
    return {
        "frequency": freq_array,
        "eps_real": eps_real,
        "eps_imag": eps_imag,
        "loss_tangent": loss_tangent,
        "relaxation_freq": 1.0 / (2.0 * np.pi * tau_relaxation)
    }


def calculate_broadband_dielectric_spectrum():
    """
    Generate the classic 4-mechanism broadband dielectric dispersion spectrum
    from 1 Hz to 10^16 Hz showing:
    1. Interfacial / space charge (< 10^3 Hz)
    2. Dipolar / orientational relaxation (10^3 - 10^10 Hz)
    3. Ionic / lattice vibration resonance (10^11 - 10^13 Hz)
    4. Electronic resonance (10^14 - 10^16 Hz)
    """
    freq = np.logspace(0, 16, 800)
    
    # Baseline optical background
    eps_real = np.full_like(freq, 2.0)
    eps_imag = np.zeros_like(freq)
    
    # 1. Interfacial (Debye at 100 Hz)
    debye_space = 25.0 / (1.0 + (freq / 1e2)**2)
    eps_real += debye_space
    eps_imag += 25.0 * (freq / 1e2) / (1.0 + (freq / 1e2)**2)
    
    # 2. Dipolar (Debye at 10^8 Hz)
    debye_dip = 15.0 / (1.0 + (freq / 1e8)**2)
    eps_real += debye_dip
    eps_imag += 15.0 * (freq / 1e8) / (1.0 + (freq / 1e8)**2)
    
    # 3. Ionic resonance at 10^12 Hz (Lorentz oscillator)
    w_res_ion = 1e12
    gamma_ion = 3e11
    f_ion = 8.0
    denom_ion = (w_res_ion**2 - freq**2)**2 + (gamma_ion * freq)**2
    eps_real += f_ion * w_res_ion**2 * (w_res_ion**2 - freq**2) / denom_ion
    eps_imag += f_ion * w_res_ion**2 * (gamma_ion * freq) / denom_ion
    
    # 4. Electronic resonance at 10^15 Hz
    w_res_el = 1e15
    gamma_el = 2e14
    f_el = 4.0
    denom_el = (w_res_el**2 - freq**2)**2 + (gamma_el * freq)**2
    eps_real += f_el * w_res_el**2 * (w_res_el**2 - freq**2) / denom_el
    eps_imag += f_el * w_res_el**2 * (gamma_el * freq) / denom_el
    
    return freq, eps_real, np.maximum(0.0, eps_imag)


def calculate_clausius_mossotti(polarizability_alpha, number_density_N):
    """
    Calculate relative dielectric constant eps_r via the Clausius-Mossotti equation:
    (eps_r - 1) / (eps_r + 2) = (N * alpha) / (3 * eps_0)
    """
    eps_0 = 8.854187817e-12  # F/m
    factor = (number_density_N * polarizability_alpha) / (3.0 * eps_0)
    
    if factor >= 1.0:
        # Dielectric catastrophe (Ferroelectric transition)
        return float('inf'), factor, "Dielectric Catastrophe (Spontaneous Polarization)"
    
    eps_r = (1.0 + 2.0 * factor) / (1.0 - factor)
    return eps_r, factor, "Linear Dielectric"


def simulate_ferroelectric_hysteresis(E_max=50.0, Ec=15.0, Ps=35.0, Pr=28.0, n_points=500):
    """
    Simulate a ferroelectric P-E hysteresis loop with coercive field Ec,
    spontaneous polarization Ps, and remnant polarization Pr using a hyperbolic tangent model.
    """
    # Electric field cycle: 0 -> +E_max -> -E_max -> +E_max
    t = np.linspace(0, 2.0 * np.pi, n_points)
    E_field = E_max * np.sin(t)
    
    # Branch tracking
    P_loop = np.zeros(n_points)
    
    for i in range(n_points):
        E = E_field[i]
        dE = np.cos(t[i])
        
        # Upper branch (decreasing field) vs Lower branch (increasing field)
        if dE < 0:  # Decreasing
            P_loop[i] = Ps * np.tanh((E + Ec) / (Ec * 0.8)) + (Pr - Ps * np.tanh(1.25)) * (E / E_max)
        else:  # Increasing
            P_loop[i] = Ps * np.tanh((E - Ec) / (Ec * 0.8)) + (Pr - Ps * np.tanh(1.25)) * (E / E_max)
            
    # Landau-Devonshire Free Energy curve: F(P) = 1/2*a*(T-Tc)*P^2 + 1/4*b*P^4 - E*P
    P_range = np.linspace(-1.3 * Ps, 1.3 * Ps, 200)
    a_param = -0.5  # Below Tc
    b_param = 0.001
    F_landau = 0.5 * a_param * P_range**2 + 0.25 * b_param * P_range**4
    
    return {
        "electric_field": E_field,
        "polarization": P_loop,
        "P_range": P_range,
        "free_energy": F_landau,
        "coercive_field": Ec,
        "remnant_polarization": Pr,
        "spontaneous_polarization": Ps
    }


def calculate_phonon_polaritons(omega_TO=5.0, eps_static=12.0, eps_optical=9.0, k_max=15.0, n_points=400):
    """
    Calculate Phonon-Polariton dispersion relation and the Reststrahlen band
    via the Lyddane-Sachs-Teller (LST) relation:
    omega_LO = omega_TO * sqrt(eps_0 / eps_inf)
    eps(omega) = eps_inf * (omega_LO^2 - omega^2) / (omega_TO^2 - omega^2)
    dispersion: (c*k)^2 = omega^2 * eps(omega)
    
    Parameters:
    -----------
    omega_TO : float (Transverse optical phonon frequency in THz)
    eps_static : float (Low-frequency dielectric constant eps_0)
    eps_optical : float (High-frequency dielectric constant eps_inf)
    """
    # LST Relation
    omega_LO = omega_TO * np.sqrt(eps_static / eps_optical)
    
    k_vals = np.linspace(0.01, k_max, n_points)
    c_speed = 1.0  # Normalized units
    
    # Solve quadratic dispersion for omega^2 at each k:
    # eps_inf * omega^4 - (c^2*k^2 + eps_inf*omega_LO^2)*omega^2 + c^2*k^2*omega_TO^2 = 0
    A = eps_optical
    B = -(c_speed**2 * k_vals**2 + eps_optical * omega_LO**2)
    C = c_speed**2 * k_vals**2 * omega_TO**2
    
    discriminant = np.maximum(0.0, B**2 - 4.0 * A * C)
    omega_sq_upper = (-B + np.sqrt(discriminant)) / (2.0 * A)
    omega_sq_lower = (-B - np.sqrt(discriminant)) / (2.0 * A)
    
    omega_upper = np.sqrt(omega_sq_upper)
    omega_lower = np.sqrt(omega_sq_lower)
    
    # Uncoupled photon line: omega = c * k / sqrt(eps_inf)
    photon_line = c_speed * k_vals / np.sqrt(eps_optical)
    
    return {
        "k_values": k_vals,
        "omega_lower": omega_lower,
        "omega_upper": omega_upper,
        "omega_TO": omega_TO,
        "omega_LO": omega_LO,
        "photon_line": photon_line,
        "reststrahlen_gap": (omega_TO, omega_LO)
    }


# ============================================================================
# 6. ADVANCED GRADUATE & RESEARCH PHYSICS SOLVERS
# ============================================================================

def calculate_fermi_surface_2d(k_fermi=0.8, n_points=200):
    """
    Calculate 2D Fermi Surface cross-sections in reciprocal k-space.
    Compares spherical free electron circle against tight-binding contours.
    """
    kx = np.linspace(-np.pi, np.pi, n_points)
    ky = np.linspace(-np.pi, np.pi, n_points)
    KX, KY = np.meshgrid(kx, ky)
    
    # Free electron parabola: E = kx^2 + ky^2
    E_free = KX**2 + KY**2
    
    # 2D Square lattice tight-binding: E(k) = -2t*(cos(kx*a) + cos(ky*a))
    E_tb = -2.0 * (np.cos(KX) + np.cos(KY))
    
    return {
        "kx": kx,
        "ky": ky,
        "KX": KX,
        "KY": KY,
        "E_free": E_free,
        "E_tb": E_tb,
        "k_fermi": k_fermi
    }


def calculate_hall_effect(current_mA=10.0, magnetic_field_T=1.0, carrier_density_cm3=1e17, thickness_um=100.0, carrier_type="electron"):
    """
    Calculate the Hall effect parameters:
    - Hall Voltage: V_H = (I * B) / (n * q * t)
    - Hall Coefficient: R_H = -1 / (n * q)  [electrons] or +1 / (p * q) [holes]
    - Hall Mobility: mu_H = |R_H| * sigma
    """
    q_charge = 1.602176634e-19  # Coulombs
    I_amps = current_mA * 1e-3
    B_tesla = magnetic_field_T
    t_meters = thickness_um * 1e-6
    n_m3 = carrier_density_cm3 * 1e6
    
    sign = -1.0 if carrier_type == "electron" else 1.0
    R_H = sign / (n_m3 * q_charge)  # m^3 / C
    V_H = (I_amps * B_tesla * R_H) / t_meters  # Volts
    
    # Typical mobility for silicon
    mu_std = 1400.0 if carrier_type == "electron" else 450.0  # cm^2 / V*s
    sigma = n_m3 * q_charge * (mu_std * 1e-4)  # S / m
    
    return {
        "hall_voltage_mV": V_H * 1e3,
        "hall_coefficient_cm3_C": R_H * 1e6,
        "conductivity_S_cm": sigma * 1e-2,
        "carrier_density": carrier_density_cm3,
        "carrier_type": carrier_type,
        "lorentz_force_direction": "Right" if carrier_type == "electron" else "Left"
    }


def calculate_phonon_dos(omega_max=10.0, n_points=300):
    """
    Calculate 1D and 3D Acoustic Phonon Density of States g(omega):
    - 1D Chain: g(omega) = 2 / (pi * sqrt(omega_max^2 - omega^2))  (Van Hove singularity at omega_max)
    - 3D Debye: g(omega) = (3 * V / 2*pi^2 * v^3) * omega^2  (Parabolic ~ omega^2)
    """
    omega = np.linspace(0.01, omega_max - 0.05, n_points)
    
    # 1D Van Hove density of states
    dos_1d = 2.0 / (np.pi * np.sqrt(np.maximum(1e-4, omega_max**2 - omega**2)))
    dos_1d = dos_1d / np.max(dos_1d) * 100.0
    
    # 3D Debye quadratic density of states
    dos_3d = (omega / omega_max)**2 * 100.0
    
    return {
        "frequency": omega,
        "dos_1d": dos_1d,
        "dos_3d": dos_3d,
        "omega_max": omega_max
    }


def calculate_reststrahlen_reflectivity(omega_TO=6.0, eps_static=12.0, eps_optical=4.0, damping_gamma=0.2, n_points=500):
    """
    Calculate the complex dielectric function and normal-incidence optical reflectivity R(omega):
    eps(omega) = eps_inf + (eps_0 - eps_inf)*omega_TO^2 / (omega_TO^2 - omega^2 - i*gamma*omega)
    Reflectivity: R = |(sqrt(eps) - 1) / (sqrt(eps) + 1)|^2
    """
    omega_LO = omega_TO * np.sqrt(eps_static / eps_optical)
    omega = np.linspace(0.5 * omega_TO, 1.5 * omega_LO, n_points)
    
    # Complex dielectric function with damping
    eps_complex = eps_optical + (eps_static - eps_optical) * (omega_TO**2) / (omega_TO**2 - omega**2 - 1j * damping_gamma * omega)
    
    # Complex refractive index n + i*k = sqrt(eps)
    n_complex = np.sqrt(eps_complex)
    
    # Normal incidence reflectivity
    reflectivity = np.abs((n_complex - 1.0) / (n_complex + 1.0))**2
    
    return {
        "frequency": omega,
        "reflectivity": reflectivity * 100.0,
        "eps_real": np.real(eps_complex),
        "eps_imag": np.imag(eps_complex),
        "omega_TO": omega_TO,
        "omega_LO": omega_LO
    }


def calculate_dislocation_stress_field(b=1.0, nu=0.3, G=40.0, grid_size=3.0, n_points=100):
    """
    Calculate 2D stress field tensor around a Volterra edge dislocation:
    - sigma_xx = -D * y*(3x^2 + y^2) / (x^2 + y^2)^2
    - sigma_yy =  D * y*(x^2 - y^2) / (x^2 + y^2)^2
    - sigma_xy =  D * x*(x^2 - y^2) / (x^2 + y^2)^2
    where D = G * b / (2*pi*(1-nu))
    """
    D = (G * b) / (2.0 * np.pi * (1.0 - nu))
    
    x = np.linspace(-grid_size, grid_size, n_points)
    y = np.linspace(-grid_size, grid_size, n_points)
    X, Y = np.meshgrid(x, y)
    
    r_sq = X**2 + Y**2 + 1e-4  # Regularization at core
    
    sigma_xx = -D * Y * (3.0 * X**2 + Y**2) / (r_sq**2)
    sigma_yy = D * Y * (X**2 - Y**2) / (r_sq**2)
    sigma_xy = D * X * (X**2 - Y**2) / (r_sq**2)
    
    # Hydrostatic pressure: P = -(sigma_xx + sigma_yy) / 2
    hydro_pressure = -(sigma_xx + sigma_yy) / 2.0
    
    return {
        "x": x,
        "y": y,
        "X": X,
        "Y": Y,
        "sigma_xx": sigma_xx,
        "sigma_yy": sigma_yy,
        "sigma_xy": sigma_xy,
        "pressure": hydro_pressure
    }


def calculate_fid_spectrum(bloch_data):
    """
    Compute the Fourier Transform of the transverse NMR Free Induction Decay (FID) signal:
    M_trans(t) = M_x(t) + i * M_y(t)
    """
    t = bloch_data["time"]
    dt = t[1] - t[0]
    Mx = bloch_data["Mx"]
    My = bloch_data["My"]
    
    signal = Mx + 1j * My
    fft_vals = np.fft.fftshift(np.fft.fft(signal))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(t), d=dt * 1e-3))  # in kHz
    
    return {
        "frequencies_kHz": freqs,
        "fft_spectrum": np.abs(fft_vals) / (np.max(np.abs(fft_vals)) + 1e-12) * 100.0
    }


def calculate_phonon_velocities(k_vals, mass1_amu=28.0, mass2_amu=14.0, spring_C=30.0, a_ang=4.0):
    """
    Calculate acoustic and optical phase velocities v_p = omega / k and group velocities v_g = d(omega)/dk.
    """
    M1 = mass1_amu * 1.66054e-27
    M2 = mass2_amu * 1.66054e-27
    a_m = a_ang * 1e-10
    
    term_sum = spring_C * (1.0/M1 + 1.0/M2)
    term_diff = (spring_C * (1.0/M1 + 1.0/M2))**2 - (4.0 * spring_C**2 * np.sin(k_vals/2.0)**2) / (M1 * M2)
    
    w_plus = np.sqrt(np.maximum(0.0, term_sum + np.sqrt(np.maximum(0.0, term_diff))))
    w_minus = np.sqrt(np.maximum(0.0, term_sum - np.sqrt(np.maximum(0.0, term_diff))))
    
    # Numerical derivatives for group velocity: v_g = d(omega) / d(k_phys) = (d(omega)/dk) * a
    k_phys = k_vals / a_m
    dk = k_phys[1] - k_phys[0]
    
    vg_ac = np.gradient(w_minus, dk)
    vg_op = np.gradient(w_plus, dk)
    
    # Phase velocities: v_p = omega / k_phys
    k_nonzero = np.where(np.abs(k_phys) < 1e-6, 1e-6, k_phys)
    vp_ac = w_minus / k_nonzero
    vp_op = w_plus / k_nonzero
    
    return {
        "k": k_vals,
        "k_norm": k_vals / np.pi,
        "omega_ac_THz": w_minus / (2.0 * np.pi * 1e12),
        "omega_op_THz": w_plus / (2.0 * np.pi * 1e12),
        "vg_ac_km_s": vg_ac / 1000.0,
        "vg_op_km_s": vg_op / 1000.0,
        "vp_ac_km_s": vp_ac / 1000.0,
        "vp_op_km_s": vp_op / 1000.0
    }


def calculate_varshni_bandgap(material="Silicon", temperatures=None):
    """
    Calculate temperature-dependent semiconductor bandgap E_g(T) using Varshni's empirical relation:
    E_g(T) = E_g(0) - alpha * T^2 / (T + beta)
    """
    if temperatures is None:
        temperatures = np.linspace(0, 800, 200)
        
    params = {
        "Silicon": {"Eg0": 1.170, "alpha": 4.73e-4, "beta": 636.0, "type": "Indirect (1.12 eV @ 300K)"},
        "Germanium": {"Eg0": 0.744, "alpha": 4.77e-4, "beta": 235.0, "type": "Indirect (0.66 eV @ 300K)"},
        "Gallium Arsenide (GaAs)": {"Eg0": 1.519, "alpha": 5.405e-4, "beta": 204.0, "type": "Direct (1.42 eV @ 300K)"},
        "Gallium Nitride (GaN)": {"Eg0": 3.470, "alpha": 9.09e-4, "beta": 830.0, "type": "Direct (3.40 eV @ 300K)"},
        "Diamond (C)": {"Eg0": 5.480, "alpha": 4.5e-4, "beta": 1050.0, "type": "Indirect (5.47 eV @ 300K)"},
        "Indium Phosphide (InP)": {"Eg0": 1.424, "alpha": 4.50e-4, "beta": 327.0, "type": "Direct (1.34 eV @ 300K)"}
    }
    
    p = params.get(material, params["Silicon"])
    Eg_T = p["Eg0"] - (p["alpha"] * temperatures**2) / (temperatures + p["beta"])
    
    return {
        "temperature": temperatures,
        "bandgap_eV": Eg_T,
        "material": material,
        "type": p["type"],
        "Eg_300K": p["Eg0"] - (p["alpha"] * 300.0**2) / (300.0 + p["beta"])
    }


def calculate_landau_free_energy_temperature(T_val, Tc=393.0, alpha_0=3.8e5, beta=-1.6e8, gamma=8.0e9):
    """
    Landau-Devonshire Free Energy F(P) as a function of temperature T across phase transition:
    F(P) = (alpha_0*(T - Tc)/2)*P^2 + (beta/4)*P^4 + (gamma/6)*P^6
    """
    P = np.linspace(-0.5, 0.5, 400)
    alpha = alpha_0 * (T_val - Tc)
    F = 0.5 * alpha * (P**2) + 0.25 * beta * (P**4) + (1.0/6.0) * gamma * (P**6)
    
    return {
        "polarization": P,
        "free_energy": F / 1e6  # in MJ/m3
    }


# ============================================================================
# 7. GENERAL OPTICS, WAVES & NUCLEAR HELPERS
# ============================================================================

def calculate_snell(n1, n2, theta1):
    """Calculate angle of refraction using Snell's law."""
    sin_theta2 = (n1 / n2) * np.sin(theta1)
    if abs(sin_theta2) <= 1.0:
        return np.arcsin(sin_theta2)
    return np.nan  # Total internal reflection


def calculate_decay(initial_amount, half_life, time):
    """Calculate radioactive decay: N(t) = N0 * exp(-ln(2)*t / t_half)."""
    decay_constant = np.log(2.0) / max(half_life, 1e-12)
    return initial_amount * np.exp(-decay_constant * time)


def calculate_doppler_shift(frequency, velocity, wave_speed):
    """Calculate Doppler shifted frequency."""
    return frequency * (1.0 + velocity / wave_speed)


def calculate_standing_wave(L, n, wave_speed=343.0):
    """Calculate standing wave frequencies f_n = n * v / (2 * L)."""
    return n * wave_speed / (2.0 * max(L, 1e-6))

