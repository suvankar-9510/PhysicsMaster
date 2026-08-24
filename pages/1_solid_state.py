import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import pandas as pd
from scipy.integrate import quad

from utils.physics import (
    calculate_bragg_angle,
    calculate_structure_factor,
    calculate_debye_heat_capacity,
    calculate_einstein_heat_capacity,
    calculate_electronic_specific_heat,
    solve_kronig_penney,
    tight_binding_1d,
    tight_binding_2d_square,
    tight_binding_graphene,
    calculate_carrier_concentration,
    calculate_mobility,
    calculate_band_structure,
    calculate_electron_wavefunction,
    solve_bloch_equations,
    simulate_hahn_echo,
    calculate_epr_hyperfine_spectrum,
    calculate_fmr_kittel,
    calculate_debye_dielectric_dispersion,
    calculate_broadband_dielectric_spectrum,
    calculate_clausius_mossotti,
    simulate_ferroelectric_hysteresis,
    calculate_phonon_polaritons
)
from utils.crystal_structures import (
    generate_simple_cubic,
    generate_bcc,
    generate_fcc,
    generate_diamond_cubic,
    generate_zincblende,
    generate_nacl,
    generate_cscl,
    generate_hcp,
    generate_perovskite,
    create_3d_brillouin_zone,
    create_3d_ewald_sphere,
    create_crystal_defects_visualization
)
from utils.plotting import (
    configure_plotting_style,
    apply_glassmorphic_layout,
    plot_bloch_magnetization_trajectory
)

st.set_page_config(
    page_title="Solid State Physics - Graduate & M.Sc Suite",
    page_icon="🔷",
    layout="wide"
)

# Theme configuration
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Sidebar theme toggle & navigation
with st.sidebar:
    st.markdown("### ⚙️ Laboratory Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Theme", value=st.session_state.dark_mode)
    st.markdown("---")
    st.markdown("### 📌 Quick Navigation")
    st.markdown("""
    - **Tab 1:** Crystal Architecture & BZ
    - **Tab 2:** XRD & Structure Factor
    - **Tab 3:** Phonons & Specific Heat
    - **Tab 4:** Band Theory & Graphene
    - **Tab 5:** Magnetic Resonance (NMR/EPR/FMR)
    - **Tab 6:** Dielectrics & Polaritons
    - **Tab 7:** Defects & Dislocations
    """)

# Dynamic theme styling
dark = st.session_state.dark_mode
card_bg = "rgba(17, 24, 39, 0.75)" if dark else "rgba(255, 255, 255, 0.88)"
card_border = "rgba(255, 255, 255, 0.12)" if dark else "rgba(226, 232, 240, 0.8)"
text_primary = "#f8fafc" if dark else "#0f172a"
text_secondary = "#94a3b8" if dark else "#475569"
theory_bg = "rgba(99, 102, 241, 0.12)" if dark else "rgba(238, 242, 255, 0.85)"
theory_border = "#818cf8" if dark else "#4f46e5"
metric_bg = "rgba(30, 41, 59, 0.7)" if dark else "rgba(240, 249, 255, 0.9)"
plot_bg = 'rgba(15, 23, 42, 0.65)' if dark else 'rgba(255, 255, 255, 0.85)'

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .main .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }}
    
    .crystal-header {{
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #6366f1 100%);
        padding: 3rem 2.5rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 20px 40px rgba(30, 58, 138, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.25);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card {{
        background: {metric_bg};
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid {card_border};
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        border-color: #6366f1;
    }}
    
    .metric-value {{
        font-size: 1.7rem;
        font-weight: 800;
        color: {'#38bdf8' if dark else '#1e40af'};
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .metric-label {{
        font-size: 0.85rem;
        color: {text_secondary};
        font-weight: 600;
        margin-top: 4px;
    }}
    
    .theory-box {{
        background: {theory_bg};
        border-left: 4px solid {theory_border};
        padding: 1.2rem 1.6rem;
        border-radius: 10px;
        margin: 1.2rem 0;
        color: {text_primary};
        font-size: 0.98rem;
        line-height: 1.65;
        border-top: 1px solid {card_border};
        border-right: 1px solid {card_border};
        border-bottom: 1px solid {card_border};
    }}
    
    .theory-box h4 {{
        margin: 0 0 0.5rem 0;
        color: {'#a5b4fc' if dark else '#4338ca'};
        font-weight: 700;
        font-size: 1.1rem;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="crystal-header">
    <div style="font-size: 2.8rem; margin-bottom: 8px;">🔷</div>
    <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 800; letter-spacing: -0.5px;">
        Solid State Physics Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 0.8rem auto 0 auto; font-size: 1.2rem; max-width: 800px; font-weight: 300;">
        Graduate & M.Sc Level Simulations: Crystal Architecture, Reciprocal Space, Phonon Dynamics, Tight-Binding Bands, Magnetic Resonance (NMR/EPR/FMR), and Dielectric Polarization.
    </p>
</div>
""", unsafe_allow_html=True)

# 7 Graduate Tabs
tabs = st.tabs([
    "🏗️ Crystal Architecture & Reciprocal Space",
    "🔬 X-Ray Diffraction & Structure Factor",
    "🌡️ Phonons & Lattice Dynamics",
    "⚡ Electronic Band Theory & Transport",
    "🧲 Magnetic Resonance (NMR / EPR / FMR)",
    "⚡ Dielectrics, Polarization & Ferroelectrics",
    "🔬 Defects & Materials Engineering"
])


# ============================================================================
# TAB 1: CRYSTAL ARCHITECTURE & RECIPROCAL SPACE
# ============================================================================
with tabs[0]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Theoretical Foundation</h4>
        A periodic crystal is formed by translating a basis of atoms across all lattice vectors of a 3D Bravais lattice:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\mathbf{R} = u\mathbf{a}_1 + v\mathbf{a}_2 + w\mathbf{a}_3, \quad \mathbf{b}_i \cdot \mathbf{a}_j = 2\pi \delta_{ij}")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        The <strong>First Brillouin Zone</strong> is the Wigner-Seitz primitive cell of the reciprocal lattice, enclosing all uniquely defined crystal wavevectors \(\mathbf{k}\). Interplanar spacing for cubic systems is given by:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"d_{hkl} = \frac{a}{\sqrt{h^2 + k^2 + l^2}}")

    col1, col2 = st.columns([1, 2.3], gap="large")

    with col1:
        st.markdown("#### 🔧 Lattice Configuration")
        crystal_choice = st.selectbox(
            "Crystal System / Basis",
            [
                "Face-Centered Cubic (FCC - Al, Cu, Au)",
                "Body-Centered Cubic (BCC - Fe, Cr, W)",
                "Simple Cubic (SC - Po)",
                "Diamond Cubic (C, Si, Ge)",
                "Zincblende (GaAs)",
                "Rocksalt (NaCl)",
                "Cesium Chloride (CsCl)",
                "Hexagonal Close-Packed (HCP - Mg, Ti, Zn)",
                "Perovskite (BaTiO3 / SrTiO3)"
            ]
        )

        lattice_a = st.slider("Lattice Constant a (Å)", 2.0, 7.0, 4.0, 0.1)
        n_repeat = st.slider("Supercell Dimension (N×N×N)", 1, 4, 2)
        atom_scale = st.slider("Atomic Radius Scale", 0.2, 1.5, 0.6, 0.05)
        
        st.markdown("#### 📐 Miller Indices (h k l)")
        show_miller_plane = st.checkbox("Display Crystallographic Plane", value=True)
        col_h, col_k, col_l = st.columns(3)
        with col_h:
            mh = st.number_input("h", -3, 3, 1)
        with col_k:
            mk = st.number_input("k", -3, 3, 1)
        with col_l:
            ml = st.number_input("l", -3, 3, 1)

        view_mode = st.radio("Visualization Target:", ["3D Real-Space Crystal", "3D First Brillouin Zone (Reciprocal)"])

    with col2:
        if view_mode == "3D First Brillouin Zone (Reciprocal)":
            bz_type = "FCC" if "FCC" in crystal_choice or "Diamond" in crystal_choice or "Zincblende" in crystal_choice or "NaCl" in crystal_choice else "BCC" if "BCC" in crystal_choice or "CsCl" in crystal_choice else "SC"
            fig_bz = create_3d_brillouin_zone(bz_type, k_scale=1.0)
            fig_bz.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor=plot_bg
            )
            st.plotly_chart(fig_bz, use_container_width=True)
        else:
            fig_crys = go.Figure()
            
            if "Simple Cubic" in crystal_choice:
                pts = generate_simple_cubic(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers', marker=dict(size=atom_scale*30, color='#3b82f6'), name='Atoms'))
                n_basis = 1
                coord_num = 6
                pack_eff = 52.4
            elif "BCC" in crystal_choice:
                pts = generate_bcc(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers', marker=dict(size=atom_scale*30, color='#10b981'), name='BCC Atoms'))
                n_basis = 2
                coord_num = 8
                pack_eff = 68.0
            elif "Diamond" in crystal_choice:
                pts = generate_diamond_cubic(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers', marker=dict(size=atom_scale*26, color='#6366f1'), name='C / Si / Ge'))
                n_basis = 8
                coord_num = 4
                pack_eff = 34.0
            elif "Zincblende" in crystal_choice:
                ga_pts, as_pts = generate_zincblende(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=ga_pts[:,0], y=ga_pts[:,1], z=ga_pts[:,2], mode='markers', marker=dict(size=atom_scale*28, color='#3b82f6'), name='Ga (Cation)'))
                fig_crys.add_trace(go.Scatter3d(x=as_pts[:,0], y=as_pts[:,1], z=as_pts[:,2], mode='markers', marker=dict(size=atom_scale*30, color='#ef4444'), name='As (Anion)'))
                n_basis = 8
                coord_num = 4
                pack_eff = 34.0
            elif "NaCl" in crystal_choice:
                na_pts, cl_pts = generate_nacl(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=na_pts[:,0], y=na_pts[:,1], z=na_pts[:,2], mode='markers', marker=dict(size=atom_scale*24, color='#8b5cf6'), name='Na⁺'))
                fig_crys.add_trace(go.Scatter3d(x=cl_pts[:,0], y=cl_pts[:,1], z=cl_pts[:,2], mode='markers', marker=dict(size=atom_scale*32, color='#10b981'), name='Cl⁻'))
                n_basis = 8
                coord_num = 6
                pack_eff = 66.0
            elif "CsCl" in crystal_choice:
                cs_pts, cl_pts = generate_cscl(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=cs_pts[:,0], y=cs_pts[:,1], z=cs_pts[:,2], mode='markers', marker=dict(size=atom_scale*34, color='#f59e0b'), name='Cs⁺'))
                fig_crys.add_trace(go.Scatter3d(x=cl_pts[:,0], y=cl_pts[:,1], z=cl_pts[:,2], mode='markers', marker=dict(size=atom_scale*28, color='#10b981'), name='Cl⁻'))
                n_basis = 2
                coord_num = 8
                pack_eff = 68.0
            elif "Perovskite" in crystal_choice:
                a_pts, b_pts, o_pts = generate_perovskite(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=a_pts[:,0], y=a_pts[:,1], z=a_pts[:,2], mode='markers', marker=dict(size=atom_scale*32, color='#3b82f6'), name='A (Ba²⁺)'))
                fig_crys.add_trace(go.Scatter3d(x=b_pts[:,0], y=b_pts[:,1], z=b_pts[:,2], mode='markers', marker=dict(size=atom_scale*24, color='#f59e0b'), name='B (Ti⁴⁺)'))
                fig_crys.add_trace(go.Scatter3d(x=o_pts[:,0], y=o_pts[:,1], z=o_pts[:,2], mode='markers', marker=dict(size=atom_scale*20, color='#ef4444'), name='O (O²⁻)'))
                n_basis = 5
                coord_num = 12
                pack_eff = 72.0
            else:
                pts = generate_fcc(lattice_a, n_repeat)
                fig_crys.add_trace(go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers', marker=dict(size=atom_scale*28, color='#0284c7'), name='FCC Atoms'))
                n_basis = 4
                coord_num = 12
                pack_eff = 74.0

            # Miller Plane rendering
            if show_miller_plane and (mh != 0 or mk != 0 or ml != 0):
                box_sz = n_repeat * lattice_a
                if ml != 0:
                    u_p = np.linspace(0, box_sz, 25)
                    v_p = np.linspace(0, box_sz, 25)
                    xx, yy = np.meshgrid(u_p, v_p)
                    zz = (lattice_a - mh * xx - mk * yy) / ml
                    zz = np.where((zz >= 0) & (zz <= box_sz), zz, np.nan)
                    fig_crys.add_trace(go.Surface(
                        x=xx, y=yy, z=zz,
                        opacity=0.45,
                        colorscale=[[0, 'rgba(239,68,68,0.6)'], [1, 'rgba(249,115,22,0.6)']],
                        showscale=False,
                        name=f'({mh}{mk}{ml}) Plane'
                    ))
                elif mk != 0:
                    u_p = np.linspace(0, box_sz, 25)
                    w_p = np.linspace(0, box_sz, 25)
                    xx, zz = np.meshgrid(u_p, w_p)
                    yy = (lattice_a - mh * xx) / mk
                    yy = np.where((yy >= 0) & (yy <= box_sz), yy, np.nan)
                    fig_crys.add_trace(go.Surface(
                        x=xx, y=yy, z=zz,
                        opacity=0.45,
                        colorscale=[[0, 'rgba(239,68,68,0.6)'], [1, 'rgba(249,115,22,0.6)']],
                        showscale=False,
                        name=f'({mh}{mk}{ml}) Plane'
                    ))
                else:  # mh != 0
                    v_p = np.linspace(0, box_sz, 25)
                    w_p = np.linspace(0, box_sz, 25)
                    yy, zz = np.meshgrid(v_p, w_p)
                    xx = np.full_like(yy, lattice_a / mh)
                    xx = np.where((xx >= 0) & (xx <= box_sz), xx, np.nan)
                    fig_crys.add_trace(go.Surface(
                        x=xx, y=yy, z=zz,
                        opacity=0.45,
                        colorscale=[[0, 'rgba(239,68,68,0.6)'], [1, 'rgba(249,115,22,0.6)']],
                        showscale=False,
                        name=f'({mh}{mk}{ml}) Plane'
                    ))

            fig_crys.update_layout(
                title=f"<b>3D Crystal Structure: {crystal_choice.split('(')[0]}</b>",
                scene=dict(xaxis_title='X (Å)', yaxis_title='Y (Å)', zaxis_title='Z (Å)', aspectmode='cube'),
                height=560,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor=plot_bg,
                margin=dict(l=0, r=0, t=50, b=0)
            )
            st.plotly_chart(fig_crys, use_container_width=True)

        # Quantitative Metrics Dashboard
        hkl_sq = mh**2 + mk**2 + ml**2
        d_spacing = lattice_a / np.sqrt(max(1, hkl_sq))
        vol_cell = lattice_a**3
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{d_spacing:.3f} Å</div><div class='metric-label'>d_({mh}{mk}{ml}) Interplanar Spacing</div></div>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{coord_num}</div><div class='metric-label'>Coordination Number</div></div>", unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{pack_eff:.1f}%</div><div class='metric-label'>Atomic Packing Factor</div></div>", unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{vol_cell:.1f} Å³</div><div class='metric-label'>Unit Cell Volume</div></div>", unsafe_allow_html=True)


# ============================================================================
# TAB 2: X-RAY DIFFRACTION & STRUCTURE FACTOR
# ============================================================================
with tabs[1]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Laue Condition & Structure Factor</h4>
        Constructive interference occurs when the elastic scattering vector equals a reciprocal lattice vector:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\Delta \mathbf{k} = \mathbf{k}' - \mathbf{k} = \mathbf{G}_{hkl}, \quad F_{hkl} = \sum_{j=1}^N f_j \exp\left[-2\pi i (h u_j + k v_j + l w_j)\right]")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        Diffracted peak intensities incorporate structure factors, Lorentz-polarization factor \(\text{LP}(\theta)\), and Debye-Waller thermal damping \(e^{-2W}\):
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"I_{hkl} \propto |F_{hkl}|^2 \left(\frac{1 + \cos^2 2\theta}{\sin^2\theta \cos\theta}\right) \exp\left[-2B\left(\frac{\sin\theta}{\lambda}\right)^2\right]")

    xrd_col1, xrd_col2 = st.columns([1, 2.3], gap="large")

    with xrd_col1:
        st.markdown("#### 🔬 Diffractometer Parameters")
        xrd_lattice = st.selectbox("Sample Crystal Structure", ["FCC", "BCC", "Simple Cubic", "Diamond Cubic", "NaCl"], key="xrd_lat")
        xrd_lambda = st.slider("X-ray Source (λ in Å)", 0.5, 2.5, 1.5406, 0.01, help="Cu K-alpha = 1.5406 Å, Mo K-alpha = 0.7107 Å")
        xrd_a = st.slider("Lattice Constant a (Å)", 2.5, 6.5, 4.05, 0.05, key="xrd_a_val")
        temp_debye_waller = st.slider("Temperature Damping (Debye-Waller B in Å²)", 0.1, 2.0, 0.5, 0.1)
        xrd_mode = st.radio("XRD View:", ["Powder Diffractogram (2θ vs Intensity)", "3D Ewald Sphere Geometry"])

    with xrd_col2:
        if xrd_mode == "3D Ewald Sphere Geometry":
            fig_ewald = create_3d_ewald_sphere(xrd_lambda, xrd_a, n_nodes=3)
            fig_ewald.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg)
            st.plotly_chart(fig_ewald, use_container_width=True)
        else:
            planes_list = [
                (1,0,0), (1,1,0), (1,1,1), (2,0,0), (2,1,0), (2,1,1), (2,2,0),
                (3,0,0), (3,1,0), (3,1,1), (2,2,2), (3,2,0), (3,2,1), (4,0,0),
                (3,3,0), (3,3,1), (4,2,0), (4,2,2)
            ]
            
            xrd_peaks = []
            for h, k, l in planes_list:
                d_sp = xrd_a / np.sqrt(h**2 + k**2 + l**2)
                f_sq, is_allowed, msg = calculate_structure_factor(h, k, l, xrd_lattice)
                if is_allowed and f_sq > 0:
                    bragg_rad = calculate_bragg_angle(d_sp, xrd_lambda)
                    if not np.isnan(bragg_rad):
                        two_theta_deg = 2.0 * np.degrees(bragg_rad)
                        lp_factor = (1.0 + np.cos(2.0 * bragg_rad)**2) / (np.sin(bragg_rad)**2 * np.cos(bragg_rad) + 1e-4)
                        dw_factor = np.exp(-2.0 * temp_debye_waller * (np.sin(bragg_rad) / xrd_lambda)**2)
                        intensity = f_sq * lp_factor * dw_factor
                        xrd_peaks.append((two_theta_deg, intensity, f"({h}{k}{l})", d_sp))
                        
            two_theta_axis = np.linspace(10, 100, 1000)
            diffractogram = np.zeros_like(two_theta_axis)
            fwhm = 0.35
            
            for tth, intens, label, d_val in xrd_peaks:
                diffractogram += intens * np.exp(-4.0 * np.log(2.0) * ((two_theta_axis - tth) / fwhm)**2)
                
            max_int = np.max(diffractogram) + 1e-12
            diffractogram = (diffractogram / max_int) * 100.0
            
            fig_xrd = go.Figure()
            fig_xrd.add_trace(go.Scatter(
                x=two_theta_axis, y=diffractogram,
                mode='lines',
                line=dict(color='#38bdf8' if dark else '#2563eb', width=2.5),
                name='Simulated Intensity'
            ))
            
            for tth, intens, label, d_val in xrd_peaks:
                if tth <= 100:
                    peak_h = (intens / np.max([p[1] for p in xrd_peaks])) * 100.0
                    fig_xrd.add_annotation(
                        x=tth, y=peak_h,
                        text=f"{label}<br>{d_val:.2f}Å",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=1.5,
                        arrowcolor='#ef4444',
                        ay=-35,
                        font=dict(size=10, color=text_primary)
                    )
                    
            fig_xrd.update_layout(
                title=f"<b>Powder X-Ray Diffractogram ({xrd_lattice}, λ = {xrd_lambda:.4f} Å)</b>",
                xaxis_title="Diffraction Angle 2θ (degrees)",
                yaxis=dict(title="Relative Intensity (%)", range=[0, 120]),
                height=480,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_xrd, use_container_width=True)


# ============================================================================
# TAB 3: PHONONS & LATTICE DYNAMICS
# ============================================================================
with tabs[2]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Lattice Dynamics & Debye Specific Heat</h4>
        For a 1D diatomic chain with alternating masses \(M_1, M_2\) and interatomic spring constant \(C\):
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\omega_\pm^2(k) = C\left(\frac{1}{M_1} + \frac{1}{M_2}\right) \pm C\sqrt{\left(\frac{1}{M_1} + \frac{1}{M_2}\right)^2 - \frac{4\sin^2(ka/2)}{M_1 M_2}}")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        The exact numerical Debye heat capacity integral accounting for 3D acoustic modes:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"C_V(T) = 9 N k_B \left(\frac{T}{\Theta_D}\right)^3 \int_0^{\Theta_D/T} \frac{x^4 e^x}{(e^x - 1)^2} dx \quad \xrightarrow{T \ll \Theta_D} \quad \frac{12\pi^4}{5} N k_B \left(\frac{T}{\Theta_D}\right)^3")

    ph_col1, ph_col2 = st.columns([1, 2.3], gap="large")

    with ph_col1:
        st.markdown("#### 📊 Phonon Chain Parameters")
        chain_type = st.radio("Lattice System:", ["1D Diatomic Chain (Optical + Acoustic)", "1D Monatomic Chain"])
        mass1 = st.slider("Atom Mass M₁ (amu)", 1.0, 80.0, 28.0, 1.0)
        mass2 = st.slider("Atom Mass M₂ (amu)", 1.0, 80.0, 14.0, 1.0) if "Diatomic" in chain_type else mass1
        spring_C = st.slider("Interatomic Force Constant C (N/m)", 5.0, 100.0, 30.0, 5.0)
        
        st.markdown("#### 🌡️ Specific Heat Analysis")
        debye_T = st.slider("Debye Temperature Θ_D (K)", 100.0, 1200.0, 420.0, 20.0)
        gamma_el = st.slider("Electronic Sommerfeld γ (mJ/mol·K²)", 0.5, 10.0, 1.35, 0.1)

    with ph_col2:
        ph_plot_mode = st.radio("Select Physics View:", ["Phonon Dispersion Curves ω(k)", "Debye & Einstein Heat Capacity C_V(T)", "Electronic vs Lattice C/T vs T² Separation"], horizontal=True)

        if "Dispersion" in ph_plot_mode:
            k_vals = np.linspace(-np.pi, np.pi, 500)
            M1_kg = mass1 * 1.66054e-27
            M2_kg = mass2 * 1.66054e-27
            
            term_sum = spring_C * (1.0/M1_kg + 1.0/M2_kg)
            term_diff = (spring_C * (1.0/M1_kg + 1.0/M2_kg))**2 - (4.0 * spring_C**2 * np.sin(k_vals/2.0)**2) / (M1_kg * M2_kg)
            
            omega_plus = np.sqrt(np.maximum(0.0, term_sum + np.sqrt(np.maximum(0.0, term_diff)))) / (2.0 * np.pi * 1e12)
            omega_minus = np.sqrt(np.maximum(0.0, term_sum - np.sqrt(np.maximum(0.0, term_diff)))) / (2.0 * np.pi * 1e12)
            
            fig_ph = go.Figure()
            fig_ph.add_trace(go.Scatter(x=k_vals/np.pi, y=omega_minus, mode='lines', name='Acoustic Branch (LA)', line=dict(color='#38bdf8' if dark else '#3b82f6', width=3.5)))
            if "Diatomic" in chain_type:
                fig_ph.add_trace(go.Scatter(x=k_vals/np.pi, y=omega_plus, mode='lines', name='Optical Branch (LO)', line=dict(color='#ef4444', width=3.5)))
                gap_min = np.max(omega_minus)
                gap_max = np.min(omega_plus)
                if gap_max > gap_min:
                    fig_ph.add_hrect(y0=gap_min, y1=gap_max, fillcolor="rgba(239,68,68,0.12)", line_width=0, annotation_text="Phonon Bandgap", annotation_position="top left")

            fig_ph.update_layout(
                title=f"<b>Phonon Dispersion Relation (M₁={mass1} amu, M₂={mass2} amu, C={spring_C} N/m)</b>",
                xaxis_title="Wavevector k (π/a)",
                yaxis_title="Phonon Frequency ω (THz)",
                height=460,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_ph, use_container_width=True)

        elif "Heat Capacity" in ph_plot_mode:
            T_array = np.linspace(1.0, 1000.0, 200)
            cv_debye = np.array([calculate_debye_heat_capacity(t, debye_T) for t in T_array])
            cv_einstein = np.array([calculate_einstein_heat_capacity(t, debye_T * 0.75) for t in T_array])
            
            fig_cv = go.Figure()
            fig_cv.add_trace(go.Scatter(x=T_array, y=cv_debye, mode='lines', name='Debye Model C_V (Acoustic)', line=dict(color='#38bdf8' if dark else '#3b82f6', width=3)))
            fig_cv.add_trace(go.Scatter(x=T_array, y=cv_einstein, mode='lines', name='Einstein Model C_V (Optical)', line=dict(color='#ef4444', width=2.5, dash='dash')))
            fig_cv.add_hline(y=3.0 * 8.314, line=dict(color='#10b981', width=2, dash='dot'), annotation_text="Dulong-Petit Limit 3R = 24.94 J/mol·K")

            fig_cv.update_layout(
                title=f"<b>Lattice Heat Capacity C_V(T) (Debye Temp Θ_D = {debye_T:.0f} K)</b>",
                xaxis_title="Temperature T (K)",
                yaxis_title="Specific Heat C_V (J / mol·K)",
                height=460,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_cv, use_container_width=True)

        else:
            T_low = np.linspace(0.5, 20.0, 100)
            T_sq = T_low**2
            beta = (12.0 * np.pi**4 / 5.0) * 8.314 / (debye_T**3) * 1e3
            C_over_T = gamma_el + beta * T_sq
            
            fig_sep = go.Figure()
            fig_sep.add_trace(go.Scatter(x=T_sq, y=C_over_T, mode='lines', name='C_total / T = γ + β T²', line=dict(color='#8b5cf6', width=3)))
            fig_sep.add_hline(y=gamma_el, line=dict(color='#ef4444', dash='dash'), annotation_text=f"Sommerfeld γ = {gamma_el} mJ/mol·K² (Electronic Intercept)")

            fig_sep.update_layout(
                title="<b>Low-Temperature Specific Heat Separation: C/T vs T²</b>",
                xaxis_title="T² (K²)",
                yaxis_title="C / T (mJ / mol·K²)",
                height=460,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_sep, use_container_width=True)


# ============================================================================
# TAB 4: ELECTRONIC BAND THEORY & QUANTUM TRANSPORT
# ============================================================================
with tabs[3]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Electronic Band Theory & Tight-Binding</h4>
        In a 1D periodic delta-potential, electron energy eigenvalues obey the <strong>Kronig-Penney</strong> relation:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"P\frac{\sin\alpha a}{\alpha a} + \cos\alpha a = \cos ka, \quad \alpha = \sqrt{\frac{2mE}{\hbar^2}}")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        In 2D Graphene, nearest-neighbor hopping on the honeycomb lattice creates massless Dirac fermion dispersion around the \(K\) and \(K'\) points:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"E(\mathbf{k}) = \pm t \sqrt{1 + 4\cos\left(\frac{\sqrt{3}k_x a}{2}\right)\cos\left(\frac{k_y a}{2}\right) + 4\cos^2\left(\frac{k_y a}{2}\right)} \approx \pm \hbar v_F |\mathbf{q}|")

    band_tab1, band_tab2, band_tab3 = st.tabs(["1D Kronig-Penney Model", "2D Graphene & Tight-Binding", "Semiconductor Transport"])

    with band_tab1:
        kp_col1, kp_col2 = st.columns([1, 2.3])
        with kp_col1:
            P_strength = st.slider("Barrier Strength P", 0.5, 20.0, 5.0, 0.5)
            e_max = st.slider("Energy Range (Normalized)", 5.0, 50.0, 25.0, 5.0)
        with kp_col2:
            kp_data = solve_kronig_penney(P_strength, e_max, n_points=800)
            
            fig_kp = make_subplots(rows=1, cols=2, subplot_titles=["Dispersion f(αa) vs αa", "Allowed Energy Bands E(k)"])
            fig_kp.add_trace(go.Scatter(x=kp_data["alpha_a"], y=kp_data["f_val"], mode='lines', name='f(αa)', line=dict(color='#38bdf8' if dark else '#3b82f6', width=2)), row=1, col=1)
            fig_kp.add_hline(y=1.0, line=dict(color='gray', dash='dash'), row=1, col=1)
            fig_kp.add_hline(y=-1.0, line=dict(color='gray', dash='dash'), row=1, col=1)
            
            fig_kp.add_trace(go.Scatter(x=kp_data["ka"]/np.pi, y=kp_data["energy"], mode='markers', marker=dict(size=2.5, color='#10b981'), name='E(k) Bands'), row=1, col=2)
            fig_kp.update_xaxes(title_text="αa (Normalized Momentum)", row=1, col=1)
            fig_kp.update_yaxes(title_text="f(αa)", range=[-3, 3], row=1, col=1)
            fig_kp.update_xaxes(title_text="Crystal Momentum ka / π", range=[0, 1], row=1, col=2)
            fig_kp.update_yaxes(title_text="Energy E / E₀", row=1, col=2)
            fig_kp.update_layout(height=450, title=f"<b>Kronig-Penney Band Structure (Barrier Strength P = {P_strength})</b>", plot_bgcolor=plot_bg, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_kp, use_container_width=True)

    with band_tab2:
        st.markdown("#### 🌌 Graphene Honeycomb Lattice (Dirac Cones & Linear Dispersion)")
        kx_mesh = np.linspace(-np.pi/1.42, np.pi/1.42, 100)
        ky_mesh = np.linspace(-np.pi/1.42, np.pi/1.42, 100)
        KX, KY = np.meshgrid(kx_mesh, ky_mesh)
        E_val, E_cond = tight_binding_graphene(KX, KY, a=1.42, t=2.8)
        
        fig_graphene = go.Figure()
        fig_graphene.add_trace(go.Surface(x=KX, y=KY, z=E_cond, colorscale='Viridis', name='π* Conduction Band', opacity=0.85, showscale=False))
        fig_graphene.add_trace(go.Surface(x=KX, y=KY, z=E_val, colorscale='Plasma', name='π Valence Band', opacity=0.85, showscale=False))
        fig_graphene.update_layout(
            title="<b>Graphene 2D Tight-Binding Band Structure: Relativistic Dirac Cones at K and K' Points</b>",
            scene=dict(xaxis_title='kx (Å⁻¹)', yaxis_title='ky (Å⁻¹)', zaxis_title='Energy E (eV)', camera=dict(eye=dict(x=1.6, y=1.6, z=1.2))),
            height=540,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor=plot_bg,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig_graphene, use_container_width=True)

    with band_tab3:
        semi_col1, semi_col2 = st.columns([1, 2.3])
        with semi_col1:
            doping_type = st.selectbox("Doping Type", ["n-type", "p-type", "Intrinsic"])
            doping_conc = st.number_input("Dopant Concentration (cm⁻³)", 1e14, 1e20, 1e16, format="%.1e")
            temp_semi = st.slider("Temperature (K)", 100, 600, 300, 20)
        with semi_col2:
            n0, p0 = calculate_carrier_concentration(doping_type, doping_conc, temp_semi)
            mu_n = calculate_mobility("electron", temp_semi)
            mu_p = calculate_mobility("hole", temp_semi)
            sigma = (n0 * mu_n + p0 * mu_p) * 1.602e-19
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{n0:.2e}</div><div class='metric-label'>Electron Density n (cm⁻³)</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{p0:.2e}</div><div class='metric-label'>Hole Density p (cm⁻³)</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{sigma:.2e}</div><div class='metric-label'>Conductivity σ (S/cm)</div></div>", unsafe_allow_html=True)


# ============================================================================
# TAB 5: MAGNETIC RESONANCE (NMR / EPR / FMR)
# ============================================================================
with tabs[4]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Bloch Dynamics & Magnetic Resonance</h4>
        The macroscopic magnetization vector \(\mathbf{M}(t)\) under static \(B_0\hat{\mathbf{z}}\) and rotating RF \(B_1\) fields obeys the <strong>Bloch Equations</strong>:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\frac{d\mathbf{M}}{dt} = \gamma \mathbf{M} \times \mathbf{B}_{\text{eff}} - \frac{M_x\hat{\mathbf{x}} + M_y\hat{\mathbf{y}}}{T_2} - \frac{(M_z - M_0)\hat{\mathbf{z}}}{T_1}")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        In ferromagnetic resonance (FMR), the <strong>Kittel equations</strong> describe uniform precessional modes:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\omega = \gamma \sqrt{B_0(B_0 + 4\pi M_s)} \quad (\text{In-Plane Film}), \quad \omega = \gamma (B_0 - 4\pi M_s) \quad (\text{Out-of-Plane Film})")

    mr_mode = st.radio("Select Resonance Technique:", ["3D Bloch Vector Dynamics & NMR Pulses", "Hahn Spin Echo (90°-τ-180° Refocusing)", "EPR / ESR Hyperfine Spectroscopy", "Ferromagnetic Resonance (FMR - Kittel Formula)"], horizontal=True)

    if "3D Bloch Vector" in mr_mode:
        b_col1, b_col2 = st.columns([1, 2.3], gap="large")
        with b_col1:
            st.markdown("#### 🧲 Pulse & Relaxation Controls")
            pulse_type = st.selectbox("RF Pulse Flip Angle", ["90° Pulse (π/2 - Complete Transverse)", "180° Pulse (π - Population Inversion)", "45° Pulse"])
            t1_val = st.slider("Spin-Lattice Relaxation T₁ (ms)", 5.0, 100.0, 30.0, 5.0)
            t2_val = st.slider("Spin-Spin Relaxation T₂ (ms)", 1.0, 40.0, 8.0, 1.0)
            b1_rf = st.slider("RF Amplitude B₁ (mT)", 0.05, 0.5, 0.2, 0.05)
            
            p_dur = 1.57 if "90°" in pulse_type else 3.14 if "180°" in pulse_type else 0.785
            
        with b_col2:
            bloch_data = solve_bloch_equations(t_max=60.0, n_steps=600, B1=b1_rf, T1=t1_val, T2=t2_val, pulse_duration=p_dur)
            fig_bloch_3d = plot_bloch_magnetization_trajectory(bloch_data, f"Bloch Magnetization Trajectory ({pulse_type.split(' ')[0]})")
            fig_bloch_3d.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg)
            st.plotly_chart(fig_bloch_3d, use_container_width=True)

    elif "Hahn Spin Echo" in mr_mode:
        echo_col1, echo_col2 = st.columns([1, 2.3])
        with echo_col1:
            tau_delay = st.slider("Pulse Delay τ (ms)", 5.0, 25.0, 12.0, 1.0)
            t2_echo = st.slider("Dephasing Time T₂ (ms)", 10.0, 50.0, 25.0, 5.0)
            n_spins = st.slider("Number of Isochromats", 20, 100, 50, 10)
        with echo_col2:
            echo_data = simulate_hahn_echo(tau=tau_delay, T2=t2_echo, n_isochromats=n_spins, t_max=45.0)
            
            fig_echo = go.Figure()
            fig_echo.add_trace(go.Scatter(x=echo_data["time"], y=echo_data["echo_signal"], mode='lines', name='Transverse Signal |M_⊥(t)|', line=dict(color='#38bdf8' if dark else '#2563eb', width=3.5)))
            fig_echo.add_vline(x=0, line=dict(color='#10b981', dash='dash'), annotation_text="90° Pulse")
            fig_echo.add_vline(x=tau_delay, line=dict(color='#ef4444', dash='dash'), annotation_text="180° Pulse (t = τ)")
            fig_echo.add_vline(x=2.0*tau_delay, line=dict(color='#8b5cf6', width=2), annotation_text="Hahn Echo (t = 2τ)")
            
            fig_echo.update_layout(
                title=f"<b>Hahn Spin Echo Formation (Refocusing at t = 2τ = {2.0*tau_delay:.1f} ms)</b>",
                xaxis_title="Time t (ms)",
                yaxis_title="Transverse Signal Amplitude",
                height=460,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_echo, use_container_width=True)

    elif "EPR / ESR" in mr_mode:
        epr_col1, epr_col2 = st.columns([1, 2.3])
        with epr_col1:
            spin_i = st.selectbox("Coupled Nuclear Spin I", [0.5, 1.0, 1.5], help="I=1/2: 1H, 19F, 31P; I=1: 14N; I=3/2: 23Na, 35Cl")
            n_nuc = st.slider("Number of Equivalent Nuclei n", 1, 4, 1)
            a_hf = st.slider("Hyperfine Coupling a (Gauss)", 5.0, 60.0, 25.0, 2.0)
            lw = st.slider("Linewidth ΔB (Gauss)", 1.0, 10.0, 3.5, 0.5)
        with epr_col2:
            epr_spec = calculate_epr_hyperfine_spectrum(spin_I=spin_i, n_nuclei=n_nuc, a_hyperfine=a_hf, linewidth=lw)
            
            fig_epr = make_subplots(rows=2, cols=1, subplot_titles=["Absorption Spectrum A(B)", "1st Derivative Spectrum dA/dB (Standard EPR Format)"], vertical_spacing=0.15)
            fig_epr.add_trace(go.Scatter(x=epr_spec["magnetic_field"], y=epr_spec["absorption"], mode='lines', name='Absorption', line=dict(color='#38bdf8' if dark else '#3b82f6', width=2.5)), row=1, col=1)
            fig_epr.add_trace(go.Scatter(x=epr_spec["magnetic_field"], y=epr_spec["derivative"], mode='lines', name='1st Derivative', line=dict(color='#ef4444', width=2.5)), row=2, col=1)
            
            fig_epr.update_xaxes(title_text="Magnetic Field B (Gauss)", row=2, col=1)
            fig_epr.update_layout(height=480, title=f"<b>EPR Hyperfine Multiplet: {epr_spec['n_lines']} Peak Splitting (2nI+1)</b>", plot_bgcolor=plot_bg, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_epr, use_container_width=True)

    else:
        fmr_col1, fmr_col2 = st.columns([1, 2.3])
        with fmr_col1:
            ms_val = st.slider("Saturation Magnetization 4πMs (Gauss)", 500.0, 5000.0, 1750.0, 250.0)
            gamma_val = st.slider("Gyromagnetic Ratio γ/2π (GHz/Tesla)", 20.0, 35.0, 28.0, 1.0)
        with fmr_col2:
            B_kG = np.linspace(0.1, 5.0, 200)
            f_in = calculate_fmr_kittel(B_kG * 1000.0, Ms=ms_val, gamma=gamma_val/1000.0, geometry="In-plane Thin Film")
            f_out = calculate_fmr_kittel(B_kG * 1000.0, Ms=ms_val, gamma=gamma_val/1000.0, geometry="Out-of-plane Thin Film")
            f_sph = calculate_fmr_kittel(B_kG * 1000.0, Ms=ms_val, gamma=gamma_val/1000.0, geometry="Sphere")
            
            fig_fmr = go.Figure()
            fig_fmr.add_trace(go.Scatter(x=B_kG, y=f_in, mode='lines', name='In-Plane Film: ω = γ√(B(B+4πMs))', line=dict(color='#38bdf8' if dark else '#3b82f6', width=3)))
            fig_fmr.add_trace(go.Scatter(x=B_kG, y=f_out, mode='lines', name='Out-of-Plane Film: ω = γ(B - 4πMs)', line=dict(color='#ef4444', width=3)))
            fig_fmr.add_trace(go.Scatter(x=B_kG, y=f_sph, mode='lines', name='Sphere: ω = γB', line=dict(color='#10b981', width=2.5, dash='dash')))
            
            fig_fmr.update_layout(
                title="<b>Ferromagnetic Resonance (FMR) Kittel Frequency vs Applied Field B₀</b>",
                xaxis_title="Applied Magnetic Field B₀ (Tesla)",
                yaxis_title="Resonance Frequency f (GHz)",
                height=460,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_fmr, use_container_width=True)


# ============================================================================
# TAB 6: DIELECTRIC PROPERTIES, POLARIZATION & FERROELECTRICS
# ============================================================================
with tabs[5]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Dielectrics, Polarization & Polaritons</h4>
        The macroscopic dielectric constant relates to microscopic polarizability via the <strong>Clausius-Mossotti relation</strong>:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\frac{\varepsilon_r - 1}{\varepsilon_r + 2} = \frac{N \alpha}{3 \varepsilon_0}, \quad \tilde{\varepsilon}(\omega) = \varepsilon_\infty + \frac{\varepsilon_s - \varepsilon_\infty}{1 + i\omega\tau} = \varepsilon'(\omega) - i\varepsilon''(\omega)")
    st.markdown(r"""
    <div class="theory-box" style="margin-top: -10px;">
        In polar crystals, coupling of optical phonons with electromagnetic photons yields <strong>Phonon-Polaritons</strong> governed by the <strong>Lyddane-Sachs-Teller (LST) relation</strong>:
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\frac{\varepsilon_0}{\varepsilon_\infty} = \frac{\omega_{LO}^2}{\omega_{TO}^2}, \quad F(P) = \frac{\alpha_0(T - T_0)}{2} P^2 + \frac{\beta}{4} P^4 - E P")

    diel_view = st.radio(
        "Dielectric Laboratory Mode:",
        [
            "Broadband Dielectric Spectroscopy (4 Mechanisms)",
            "Debye Dielectric Relaxation & Cole-Cole Arc",
            "Ferroelectric P-E Hysteresis & Landau Theory",
            "Phonon-Polaritons & LST Reststrahlen Band"
        ],
        horizontal=True
    )

    if "Broadband" in diel_view:
        f_axis, eps_1, eps_2 = calculate_broadband_dielectric_spectrum()
        
        fig_broad = make_subplots(rows=2, cols=1, subplot_titles=["Real Permittivity ε'(f) - Energy Storage", "Dielectric Loss ε''(f) - Energy Dissipation"], vertical_spacing=0.14)
        fig_broad.add_trace(go.Scatter(x=f_axis, y=eps_1, mode='lines', line=dict(color='#38bdf8' if dark else '#2563eb', width=3), name="ε' (Storage)"), row=1, col=1)
        fig_broad.add_trace(go.Scatter(x=f_axis, y=eps_2, mode='lines', line=dict(color='#dc2626', width=2.5), name='ε" (Loss)'), row=2, col=1)
        
        fig_broad.update_xaxes(type="log", title_text="Frequency f (Hz)", row=2, col=1)
        fig_broad.update_xaxes(type="log", row=1, col=1)
        fig_broad.update_yaxes(title_text="ε'", row=1, col=1)
        fig_broad.update_yaxes(title_text="ε''", row=2, col=1)
        
        fig_broad.add_vrect(x0=1, x1=1e3, fillcolor="rgba(59,130,246,0.08)", line_width=0, annotation_text="Interfacial", row=1, col=1)
        fig_broad.add_vrect(x0=1e3, x1=1e10, fillcolor="rgba(16,185,129,0.08)", line_width=0, annotation_text="Dipolar", row=1, col=1)
        fig_broad.add_vrect(x0=1e11, x1=1e13, fillcolor="rgba(245,158,11,0.08)", line_width=0, annotation_text="Ionic", row=1, col=1)
        fig_broad.add_vrect(x0=1e14, x1=1e16, fillcolor="rgba(239,68,68,0.08)", line_width=0, annotation_text="Electronic", row=1, col=1)
        
        fig_broad.update_layout(height=520, title="<b>Complete Dielectric Response Spectrum from DC to Optical UV</b>", plot_bgcolor=plot_bg, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_broad, use_container_width=True)

    elif "Debye Dielectric Relaxation" in diel_view:
        deb_col1, deb_col2 = st.columns([1, 2.3])
        with deb_col1:
            eps_s = st.slider("Static Permittivity ε_s (Low f)", 5.0, 80.0, 25.0, 2.0)
            eps_inf = st.slider("Optical Permittivity ε_∞ (High f)", 1.0, 10.0, 3.0, 0.5)
            tau_rel = st.slider("Relaxation Time τ (log₁₀ s)", -12.0, -6.0, -9.0, 0.5)
        with deb_col2:
            f_range = np.logspace(-tau_rel - 4, -tau_rel + 4, 300)
            deb_res = calculate_debye_dielectric_dispersion(f_range, eps_static=eps_s, eps_optical=eps_inf, tau_relaxation=10**tau_rel)
            
            fig_deb = make_subplots(rows=1, cols=2, subplot_titles=["Permittivity vs Frequency", "Cole-Cole Plot (ε'' vs ε')"])
            fig_deb.add_trace(go.Scatter(x=deb_res["frequency"], y=deb_res["eps_real"], mode='lines', name="ε'(ω)", line=dict(color='#38bdf8' if dark else '#2563eb', width=3)), row=1, col=1)
            fig_deb.add_trace(go.Scatter(x=deb_res["frequency"], y=deb_res["eps_imag"], mode='lines', name='ε"(ω)', line=dict(color='#ef4444', width=3)), row=1, col=1)
            fig_deb.add_trace(go.Scatter(x=deb_res["eps_real"], y=deb_res["eps_imag"], mode='lines', name='Cole-Cole Arc', line=dict(color='#8b5cf6', width=3.5), fill='tozeroy', fillcolor='rgba(139,92,246,0.1)'), row=1, col=2)
            
            fig_deb.update_xaxes(type="log", title_text="Frequency (Hz)", row=1, col=1)
            fig_deb.update_xaxes(title_text="ε' (Real)", row=1, col=2)
            fig_deb.update_yaxes(title_text="ε'' (Imaginary)", row=1, col=2)
            fig_deb.update_layout(height=460, title="<b>Debye Relaxation Equations & Semicircular Cole-Cole Arc</b>", plot_bgcolor=plot_bg, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_deb, use_container_width=True)

    elif "Ferroelectric P-E" in diel_view:
        fe_col1, fe_col2 = st.columns([1, 2.3])
        with fe_col1:
            p_sat = st.slider("Spontaneous Polarization P_s (µC/cm²)", 10.0, 60.0, 35.0, 5.0)
            p_rem = st.slider("Remnant Polarization P_r (µC/cm²)", 5.0, p_sat, min(28.0, p_sat), 2.0)
            e_coercive = st.slider("Coercive Field E_c (kV/cm)", 5.0, 40.0, 15.0, 2.0)
        with fe_col2:
            hyst_data = simulate_ferroelectric_hysteresis(E_max=50.0, Ec=e_coercive, Ps=p_sat, Pr=p_rem)
            
            fig_fe = make_subplots(rows=1, cols=2, subplot_titles=["P-E Ferroelectric Hysteresis Loop", "Landau Double-Well Free Energy F(P)"])
            fig_fe.add_trace(go.Scatter(x=hyst_data["electric_field"], y=hyst_data["polarization"], mode='lines', name='P(E) Loop', line=dict(color='#38bdf8' if dark else '#2563eb', width=3.5)), row=1, col=1)
            
            fig_fe.add_trace(go.Scatter(x=[0, 0], y=[p_rem, -p_rem], mode='markers', name='Remnant P_r', marker=dict(size=10, color='#ef4444', symbol='diamond')), row=1, col=1)
            fig_fe.add_trace(go.Scatter(x=[e_coercive, -e_coercive], y=[0, 0], mode='markers', name='Coercive E_c', marker=dict(size=10, color='#10b981', symbol='square')), row=1, col=1)
            
            fig_fe.add_trace(go.Scatter(x=hyst_data["P_range"], y=hyst_data["free_energy"], mode='lines', name='F(P)', line=dict(color='#8b5cf6', width=3)), row=1, col=2)
            
            fig_fe.update_xaxes(title_text="Electric Field E (kV/cm)", row=1, col=1)
            fig_fe.update_yaxes(title_text="Polarization P (µC/cm²)", row=1, col=1)
            fig_fe.update_xaxes(title_text="Polarization P (µC/cm²)", row=1, col=2)
            fig_fe.update_yaxes(title_text="Landau Energy F(P)", row=1, col=2)
            fig_fe.update_layout(height=460, title="<b>Ferroelectric Domain Polarization & Landau-Devonshire Free Energy</b>", plot_bgcolor=plot_bg, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_fe, use_container_width=True)

    else:
        pol_col1, pol_col2 = st.columns([1, 2.3])
        with pol_col1:
            w_to = st.slider("Transverse Optical ω_TO (THz)", 2.0, 15.0, 6.0, 0.5)
            eps_st = st.slider("Static Permittivity ε_0", 8.0, 25.0, 12.0, 1.0)
            eps_opt = st.slider("Optical Permittivity ε_∞", 1.5, 8.0, 4.0, 0.5)
        with pol_col2:
            pol_data = calculate_phonon_polaritons(omega_TO=w_to, eps_static=eps_st, eps_optical=eps_opt)
            
            fig_pol = go.Figure()
            fig_pol.add_trace(go.Scatter(x=pol_data["k_values"], y=pol_data["omega_lower"], mode='lines', name='Lower Polariton Branch', line=dict(color='#38bdf8' if dark else '#3b82f6', width=3.5)))
            fig_pol.add_trace(go.Scatter(x=pol_data["k_values"], y=pol_data["omega_upper"], mode='lines', name='Upper Polariton Branch', line=dict(color='#ef4444', width=3.5)))
            fig_pol.add_trace(go.Scatter(x=pol_data["k_values"], y=pol_data["photon_line"], mode='lines', name='Photon Line ω = ck/√ε_∞', line=dict(color='#10b981', width=2, dash='dash')))
            fig_pol.add_hline(y=pol_data["omega_TO"], line=dict(color='#64748b', dash='dot'), annotation_text=f"ω_TO = {pol_data['omega_TO']:.1f} THz")
            fig_pol.add_hline(y=pol_data["omega_LO"], line=dict(color='#64748b', dash='dot'), annotation_text=f"ω_LO = {pol_data['omega_LO']:.1f} THz (LST Relation)")
            
            fig_pol.add_hrect(y0=pol_data["omega_TO"], y1=pol_data["omega_LO"], fillcolor="rgba(239,68,68,0.15)", line_width=0, annotation_text="Reststrahlen Band (Polariton Gap - 100% Reflectivity)", annotation_position="top left")
            
            fig_pol.update_layout(
                title=f"<b>Phonon-Polariton Dispersion Relation & Reststrahlen Band (LST: ω_LO/ω_TO = √(ε₀/ε_∞) = {np.sqrt(eps_st/eps_opt):.2f})</b>",
                xaxis_title="Wavevector k (Arbitrary Units)",
                yaxis_title="Frequency ω (THz)",
                height=480,
                plot_bgcolor=plot_bg,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pol, use_container_width=True)


# ============================================================================
# TAB 7: DEFECTS & MATERIALS ENGINEERING
# ============================================================================
with tabs[6]:
    st.markdown(r"""
    <div class="theory-box">
        <h4>Crystal Defects & Volterra Dislocations</h4>
        Real crystals contain 0D point defects (Schottky vacancies, Frenkel interstitials) and 1D line defects (Edge dislocations with \(\mathbf{b} \perp \boldsymbol{\xi}\), Screw dislocations with \(\mathbf{b} \parallel \boldsymbol{\xi}\)).
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\mathbf{u}_{\text{edge}}(r, \theta) = \frac{\mathbf{b}}{2\pi}\left[\theta + \frac{\sin 2\theta}{4(1-\nu)}\right], \quad \sigma_{xx} = -\frac{G b}{2\pi(1-\nu)} \frac{y(3x^2 + y^2)}{(x^2 + y^2)^2}")

    def_col1, def_col2 = st.columns([1, 2.3], gap="large")
    with def_col1:
        st.markdown("#### 🔬 Defect Configuration")
        defect_sel = st.selectbox("Defect Mechanism", ["Edge Dislocation", "Vacancy", "Interstitial", "Substitutional"])
        
    with def_col2:
        fig_def = create_crystal_defects_visualization("Simple Cubic", a=1.0, defect_type=defect_sel)
        fig_def.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg)
        st.plotly_chart(fig_def, use_container_width=True)