# ⚛️ PhysicsMaster: Advanced Graduate & M.Sc Interactive Physics Suite

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PhysicsMaster** is an interactive, research-grade computational physics platform designed for undergraduate, graduate, and M.Sc. level exploration. Featuring real-time 3D visualizations, state-of-the-art glassmorphism design, and rigorous numerical solvers, the platform brings mathematical formulations in modern physics to life.

---

## 🌟 Key Highlights & Modules

### 🔷 1. Solid State Physics (Graduate & M.Sc Standard)
- **Crystal Architecture & Reciprocal Space**: 3D Bravais lattices (SC, BCC, FCC, Diamond, Zincblende, NaCl, CsCl, HCP, Perovskite), Wigner-Seitz primitive cell, reciprocal lattice vectors $\mathbf{b}_1, \mathbf{b}_2, \mathbf{b}_3$, 3D First Brillouin Zone polyhedra (Truncated Octahedron, Rhombic Dodecahedron) with high-symmetry $k$-points ($\Gamma, X, L, W, K$), and Miller index $(hkl)$ slicing.
- **X-Ray Diffraction & Structure Factor**: Analytical calculation of structure factor $F_{hkl} = \sum_j f_j e^{-2\pi i (hu_j + kv_j + lw_j)}$, systematic extinction rules, 3D Ewald sphere geometric construction ($\Delta\mathbf{k} = \mathbf{G}$), and powder XRD diffractograms with Lorentz-polarization and Debye-Waller factors.
- **Phonon Physics & Lattice Dynamics**: Exact dispersion for 1D monatomic & diatomic chains (acoustic vs optical branches, forbidden frequency gaps $\Delta\omega$, group vs phase velocity), exact numerical integration of the Debye heat capacity $C_V(T)$, electronic vs lattice specific heat separation ($C = \gamma T + \beta T^3$), and Umklapp vs boundary thermal conductivity.
- **Electronic Band Theory & Transport**: 1D Kronig-Penney transcendental equation solver $\cos(ka) = P\frac{\sin\alpha a}{\alpha a} + \cos\alpha a$, 1D/2D square lattice and Graphene tight-binding Hamiltonians (Dirac cones with $E = \hbar v_F |\mathbf{q}|$), Density of States in 1D, 2D, and 3D with van Hove singularities, and Fermi-Dirac statistics.
- **Magnetic Resonance (NMR, EPR/ESR, FMR)**:
  - Numerical 4th-order Runge-Kutta integration of the **Bloch Equations**:
    $$\frac{d\mathbf{M}}{dt} = \gamma \mathbf{M} \times \mathbf{B}_{eff} - \frac{M_x\hat{\mathbf{x}} + M_y\hat{\mathbf{y}}}{T_2} - \frac{(M_z - M_0)\hat{\mathbf{z}}}{T_1}$$
  - Interactive 3D trajectory of $\mathbf{M}(t)$ on the unit sphere during $90^\circ$ and $180^\circ$ RF excitation and Free Induction Decay (FID).
  - **Hahn Spin Echo** simulation ($90^\circ_x - \tau - 180^\circ_y - \tau$) showing spin dephasing and rephasing.
  - **EPR / ESR Spectroscopy** with hyperfine coupling ($2nI+1$ splitting lines) and $g$-factor shifts.
  - **Ferromagnetic Resonance (FMR)** with Kittel resonance conditions and demagnetization tensors.
- **Dielectric Properties, Polarization & Ferroelectricity**:
  - Microscopic mechanisms: Electronic ($\alpha_e$), Ionic ($\alpha_i$), Dipolar/Orientational ($\alpha_d = \frac{p^2}{3k_B T}$), and Interfacial polarization.
  - Lorentz local electric field $\mathbf{E}_{loc} = \mathbf{E} + \frac{\mathbf{P}}{3\epsilon_0}$ and the **Clausius-Mossotti relation**.
  - Complex dielectric permittivity $\tilde{\epsilon}(\omega) = \epsilon'(\omega) - i \epsilon''(\omega)$, Debye relaxation equations, Cole-Cole plots, and loss tangent $\tan\delta$.
  - Landau-Devonshire ferroelectric free energy minimizer and $P-E$ hysteresis loop simulation ($P_s, P_r, E_c$).
  - Lyddane-Sachs-Teller (LST) relation $\frac{\epsilon_0}{\epsilon_\infty} = \frac{\omega_{LO}^2}{\omega_{TO}^2}$ and Phonon-Polariton dispersion curve with the Reststrahlen band.
- **Crystal Defects**: Schottky and Frenkel point defects, Edge and Screw dislocations with Burgers vector $\mathbf{b}$, and slip planes.

---

### 🔬 2. Optics & Photonics
- Ray optics, matrix optics transfer methods, Snell's law refraction.
- Wave optics, diffraction gratings, Airy disk resolution, single/double slit Fraunhofer patterns.
- Polarization physics: Jones calculus, Stokes parameters, linear/circular/elliptical polarization on the Poincaré sphere.
- Optical interferometry: Michelson interferometer and Fabry-Pérot cavity transmission.

### 🌊 3. Waves & Oscillations
- Superposition principle, multi-wave interference, beat patterns.
- Standing waves, harmonic modes, 2D Chladni plate resonance patterns.
- Wavepackets, Fourier synthesis, phase velocity vs group velocity dispersion in dispersive media.
- Doppler effect and acoustic shock waves.

### ⚛️ 4. Nuclear Physics
- Liquid Drop Model & Semi-Empirical Mass Formula (SEMF) binding energy per nucleon curve.
- Radioactive decay kinetics, multi-isotope decay chains with Bateman differential equation solver.
- Nuclear fission and fusion energetics, Q-value kinematics, nuclear shell model magic numbers.

### ❄️ 5. Superconductivity
- London equations and temperature-dependent London penetration depth $\lambda_L(T)$.
- Ginzburg-Landau theory, coherence length $\xi(T)$, and Ginzburg-Landau parameter $\kappa = \lambda/\xi$ (Type-I vs Type-II vortex states).
- BCS theory energy gap $\Delta(T) = 1.764 k_B T_c \tanh\left(1.74 \sqrt{\frac{T_c}{T} - 1}\right)$.
- AC/DC Josephson effect and SQUID quantum interferometry.

### 🧠 6. AI Physics Assistant
- Interactive physics problem solver powered by LLM integrations with rich LaTeX mathematical rendering.
- Pre-configured problem templates across Quantum Mechanics, Solid State, Electromagnetism, and Thermodynamics.

### ⚛️ 7. Quantum Physics
- 1D Time-Independent Schrödinger Equation numerical solver.
- Quantum Harmonic Oscillator eigenfunctions and Hermite polynomials.
- Finite potential barrier tunneling and transmission coefficient $T(E)$.
- Hydrogen atom radial wavefunctions $R_{nl}(r)$ and spherical harmonics $Y_{lm}(\theta, \phi)$.
- Two-level quantum system dynamics and 3D Bloch sphere representation.

### 📚 8. Physics Glossary & Matrix
- Searchable graduate physics glossary with over 100 entries, foundational equations, and interactive unit calculators.

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PhysicsMaster.git
   cd PhysicsMaster
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the platform**:
   ```bash
   streamlit run main.py
   ```
   Open `http://localhost:8501` in your browser.

---

## ☁️ Deployment

### Deploy to Streamlit Community Cloud (Recommended)
1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub repo, set the main file path to `main.py`, and click **Deploy**.

### Deploy to Vercel
The repository includes `vercel.json` and a serverless configuration. Deploy with:
```bash
vercel
```

### Deploy with Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🛠️ Technology Stack
- **Framework**: [Streamlit](https://streamlit.io/)
- **Visualizations**: [Plotly](https://plotly.com/python/) (2D & 3D WebGL Charts)
- **Scientific Computation**: [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Pandas](https://pandas.pydata.org/)
- **Mathematical Typography**: KaTeX / LaTeX
- **UI Architecture**: Glassmorphism with modern CSS3 Backdrop Filters

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
