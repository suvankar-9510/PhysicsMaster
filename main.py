import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import math
from utils.plotting import configure_plotting_style, apply_glassmorphic_layout
from utils.crystal_structures import create_3d_brillouin_zone, generate_fcc
from utils.physics import solve_bloch_equations

# Set page configuration with improved aesthetics
st.set_page_config(
    page_title="PhysicsMaster - Advanced Graduate & M.Sc Physics Suite",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply state-of-the-art Glassmorphic CSS with enhanced 3D lighting and animations
def apply_custom_css(dark_mode=False):
    if dark_mode:
        bg_main = "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%)"
        card_bg = "rgba(17, 24, 39, 0.75)"
        card_border = "rgba(255, 255, 255, 0.12)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        hero_grad = "linear-gradient(135deg, rgba(79, 70, 229, 0.85) 0%, rgba(147, 51, 234, 0.85) 50%, rgba(219, 39, 119, 0.75) 100%)"
        accent_color = "#38bdf8"
    else:
        bg_main = "linear-gradient(135deg, #f0f4fd 0%, #e2e8f0 50%, #ede9fe 100%)"
        card_bg = "rgba(255, 255, 255, 0.82)"
        card_border = "rgba(255, 255, 255, 0.7)"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        hero_grad = "linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%)"
        accent_color = "#2563eb"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    .main .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        background: {bg_main};
        min-height: 100vh;
    }}
    
    /* 3D Glassmorphism Universal Card */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(18px) saturate(180%);
        -webkit-backdrop-filter: blur(18px) saturate(180%);
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 12px 35px -5px rgba(0, 0, 0, 0.1), 0 0 1px 1px {card_border};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}
    
    .glass-card:hover {{
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 22px 45px -5px rgba(0, 0, 0, 0.18), 0 0 20px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.4);
    }}
    
    /* Hero Glass Banner with 3D Depth */
    .hero-banner {{
        background: {hero_grad};
        backdrop-filter: blur(20px);
        border-radius: 28px;
        padding: 3.5rem 2.5rem;
        margin-bottom: 2.5rem;
        color: white;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 25px 60px -12px rgba(79, 70, 229, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.6);
    }}
    
    .hero-glow {{
        position: absolute;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
        top: -100px;
        right: -80px;
        border-radius: 50%;
        animation: floatGlow 8s ease-in-out infinite alternate;
        pointer-events: none;
    }}
    
    @keyframes floatGlow {{
        0% {{ transform: translate(0, 0) scale(1); }}
        100% {{ transform: translate(-30px, 30px) scale(1.15); }}
    }}
    
    /* Glowing Badges */
    .physics-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: white;
        backdrop-filter: blur(10px);
        margin-right: 8px;
        margin-bottom: 12px;
    }}
    
    /* Domain Card with 3D Border Glow */
    .domain-card {{
        background: {card_bg};
        backdrop-filter: blur(16px);
        border: 1px solid {card_border};
        border-radius: 22px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.35s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
    }}
    
    .domain-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.14);
        border-color: #6366f1;
    }}
    
    .domain-icon {{
        font-size: 2.8rem;
        margin-bottom: 14px;
        display: inline-block;
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    .domain-card:hover .domain-icon {{
        transform: scale(1.2) rotate(8deg);
    }}
    
    .math-formula {{
        font-family: 'JetBrains Mono', monospace;
        background: rgba(99, 102, 241, 0.08);
        border-left: 3px solid #6366f1;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin: 10px 0;
        color: {text_primary};
    }}
    
    /* Primary buttons */
    .stButton>button {{
        border-radius: 14px;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.35);
        width: 100%;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.55);
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)


def main():
    configure_plotting_style()

    # Session state for theme
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True

    apply_custom_css(st.session_state.dark_mode)

    # =========================================================================
    # SIDEBAR NAVIGATION & THEME CONTROLS
    # =========================================================================
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.4rem 1rem; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius: 18px; margin-bottom: 1.5rem; color: white; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);">
            <div style="font-size: 2.2rem; margin-bottom: 4px;">⚛️</div>
            <h2 style="color: white; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.5px;">PhysicsMaster</h2>
            <p style="color: rgba(255,255,255,0.85); margin: 4px 0 0 0; font-size: 0.8rem; font-weight: 500;">Graduate & M.Sc Simulator</p>
        </div>
        """, unsafe_allow_html=True)

        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            st.caption("🎨 Interface Mode")
        with col_t2:
            dark_mode = st.toggle("🌙 Dark Glass", st.session_state.dark_mode)
            if dark_mode != st.session_state.dark_mode:
                st.session_state.dark_mode = dark_mode
                st.rerun()

        st.markdown("---")
        st.markdown("### 🧭 Laboratory Modules")

        topic_pages = [
            {"name": "Solid State Physics", "page": "pages/1_solid_state.py", "icon": "🔷", "badge": "M.Sc Suite", "desc": "Brillouin Zones, Phonons, NMR/EPR & Dielectrics"},
            {"name": "Optics & Photonics", "page": "pages/2_optics.py", "icon": "🔬", "badge": "Wave & Ray", "desc": "Jones Polarization, Cavities & Gratings"},
            {"name": "Waves & Oscillations", "page": "pages/3_waves.py", "icon": "🌊", "badge": "Fourier & 2D", "desc": "Chladni Plates, Wavepackets & Dispersion"},
            {"name": "Nuclear Physics", "page": "pages/4_nuclear.py", "icon": "☢️", "badge": "SEMF & Decay", "desc": "Liquid Drop, Bateman Chains & Shell Model"},
            {"name": "Superconductivity", "page": "pages/5_superconductivity.py", "icon": "❄️", "badge": "BCS & GL", "desc": "Meissner, Vortex Lattices & Josephson SQUID"},
            {"name": "AI Physics Assistant", "page": "pages/6_ai_physics_assistant.py", "icon": "🧠", "badge": "LLM Solver", "desc": "Step-by-Step LaTeX Mathematical Reasoning"},
            {"name": "Quantum Physics", "page": "pages/7_quantum_physics.py", "icon": "⚛️", "badge": "Schrödinger", "desc": "Bloch Sphere, Harmonic Oscillator & Tunneling"},
            {"name": "Physics Glossary", "page": "pages/8_physics_glossary.py", "icon": "📚", "badge": "100+ Terms", "desc": "M.Sc Concept Matrix & Interactive Solvers"}
        ]

        for item in topic_pages:
            if st.button(f"{item['icon']} {item['name']}", key=f"side_{item['name']}", help=item['desc']):
                st.switch_page(item['page'])

        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
            <p style="margin: 0; font-size: 0.78rem; color: #94a3b8; font-weight: 600;">PhysicsMaster v2.5 M.Sc</p>
            <p style="margin: 4px 0 0 0; font-size: 0.72rem; color: #64748b;">Ready for GitHub & Cloud Deployment</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # HERO SECTION (3D Glassmorphism & High-Impact Typography)
    # =========================================================================
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-glow"></div>
        <div style="position: relative; z-index: 2; max-width: 850px;">
            <div>
                <span class="physics-badge">🎓 Graduate & M.Sc Standard</span>
                <span class="physics-badge">⚡ Real-Time Numerical Solvers</span>
                <span class="physics-badge">🧊 3D WebGL Glassmorphism</span>
            </div>
            <h1 style="font-size: 3.2rem; font-weight: 800; line-height: 1.15; margin: 0.8rem 0; letter-spacing: -1px; text-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                Explore the Fabric of the Physical Universe
            </h1>
            <p style="font-size: 1.25rem; line-height: 1.6; color: rgba(255,255,255,0.92); font-weight: 300; margin-bottom: 1.8rem;">
                A rigorous computational laboratory providing 3D interactive simulations across 
                <strong>Solid State Physics</strong>, <strong>Magnetic Resonance (NMR/EPR)</strong>, 
                <strong>Dielectrics & Polaritons</strong>, <strong>Quantum Mechanics</strong>, 
                and <strong>Superconductivity</strong>.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # LIVE 3D INTERACTIVE HERO SANDBOX
    # =========================================================================
    st.markdown("""
    <div style="margin: 1.5rem 0 1rem 0;">
        <h2 style="font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0.2rem;">
            🔬 Real-Time Multi-Physics Playground
        </h2>
        <p style="color: #64748b; font-size: 1.05rem;">
            Interact with live graduate simulations directly from the command center.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sandbox_mode = st.radio(
        "Select Interactive Demonstration:",
        [
            "🌊 Multi-Wave Interference & Superposition",
            "🔷 3D Reciprocal Lattice & First Brillouin Zone (FCC)",
            "🧲 3D Bloch Equation Spin Dynamics (NMR/MRI)",
            "⚡ Dielectric Polarization & Broadband Dispersion"
        ],
        horizontal=True
    )

    col_sim, col_info = st.columns([1.6, 1.0], gap="large")

    with col_sim:
        if "Multi-Wave" in sandbox_mode:
            # Multi-wave interference live demo
            x = np.linspace(0, 6 * np.pi, 400)
            t = time.time() * 1.5
            w1 = 1.0 * np.sin(x - t) * np.exp(-0.04 * x)
            w2 = 0.8 * np.sin(1.25 * x - 0.9 * t + np.pi/4) * np.exp(-0.03 * x)
            w3 = 0.6 * np.sin(0.75 * x - 1.3 * t + np.pi/2) * np.exp(-0.05 * x)
            superposition = w1 + w2 + w3

            fig_wave = go.Figure()
            fig_wave.add_trace(go.Scatter(x=x, y=w1, mode='lines', name='ψ₁(x,t) [ω₁]', line=dict(color='#3b82f6', width=2)))
            fig_wave.add_trace(go.Scatter(x=x, y=w2, mode='lines', name='ψ₂(x,t) [ω₂]', line=dict(color='#ec4899', width=2)))
            fig_wave.add_trace(go.Scatter(x=x, y=w3, mode='lines', name='ψ₃(x,t) [ω₃]', line=dict(color='#8b5cf6', width=2)))
            fig_wave.add_trace(go.Scatter(x=x, y=superposition, mode='lines', name='Ψ_total (Superposition)', line=dict(color='#10b981', width=3.5), fill='tozeroy', fillcolor='rgba(16,185,129,0.12)'))
            
            fig_wave.update_layout(
                title="<b>Superposition of Coherent Wavepackets: Ψ(x,t) = Σ A_n sin(k_n x - ω_n t + δ_n)</b>",
                xaxis_title="Spatial Coordinate x",
                yaxis_title="Wave Amplitude Ψ",
                height=460,
                plot_bgcolor='rgba(15,23,42,0.6)' if st.session_state.dark_mode else 'rgba(255,255,255,0.7)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(fig_wave, use_container_width=True)

        elif "Brillouin" in sandbox_mode:
            # 3D Brillouin Zone interactive plot
            bz_fig = create_3d_brillouin_zone("FCC", k_scale=1.0)
            bz_fig.update_layout(height=460, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(bz_fig, use_container_width=True)

        elif "Bloch Equation" in sandbox_mode:
            # Solve Bloch equations for a 90-degree pulse
            bloch_res = solve_bloch_equations(t_max=30.0, n_steps=400, B0=1.0, B1=0.2, omega_rf=1.0, omega_0=1.0, T1=15.0, T2=5.0, pulse_duration=1.57)
            t_pts = bloch_res["time"]
            
            fig_bloch = go.Figure()
            fig_bloch.add_trace(go.Scatter(x=t_pts, y=bloch_res["Mx"], mode='lines', name='M_x (Transverse)', line=dict(color='#3b82f6', width=2)))
            fig_bloch.add_trace(go.Scatter(x=t_pts, y=bloch_res["My"], mode='lines', name='M_y (Transverse)', line=dict(color='#ec4899', width=2)))
            fig_bloch.add_trace(go.Scatter(x=t_pts, y=bloch_res["Mz"], mode='lines', name='M_z (Longitudinal T1)', line=dict(color='#10b981', width=3)))
            fig_bloch.add_trace(go.Scatter(x=t_pts, y=bloch_res["M_transverse"], mode='lines', name='|M_⊥| (FID Envelope T2)', line=dict(color='#f59e0b', width=2.5, dash='dash')))

            fig_bloch.update_layout(
                title="<b>Bloch Vector Relaxation & Free Induction Decay (FID)</b>",
                xaxis_title="Time t (ms)",
                yaxis_title="Magnetization M/M₀",
                height=460,
                plot_bgcolor='rgba(15,23,42,0.6)' if st.session_state.dark_mode else 'rgba(255,255,255,0.7)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(fig_bloch, use_container_width=True)

        else:  # Dielectric
            freq_arr = np.logspace(1, 15, 400)
            # 4 distinct mechanisms
            eps_r = 2.0 + 20.0 / (1.0 + (freq_arr/1e3)**2) + 12.0 / (1.0 + (freq_arr/1e8)**2) + 6.0 * (1e12**2) / np.abs(1e12**2 - freq_arr**2 + 1e11*freq_arr*1j)
            
            fig_diel = go.Figure()
            fig_diel.add_trace(go.Scatter(x=freq_arr, y=np.real(eps_r), mode='lines', name="ε'(ω) Real Permittivity (Storage)", line=dict(color='#3b82f6', width=3)))
            fig_diel.add_trace(go.Scatter(x=freq_arr, y=np.abs(np.imag(eps_r)), mode='lines', name='ε"(ω) Dielectric Loss (Dissipation)', line=dict(color='#ef4444', width=2.5, dash='dot')))
            
            fig_diel.update_xaxes(type="log", title="Frequency f (Hz)")
            fig_diel.update_yaxes(title="Permittivity ε(ω)")
            fig_diel.update_layout(
                title="<b>Broadband Dielectric Spectroscopy & Relaxation Mechanisms</b>",
                height=460,
                plot_bgcolor='rgba(15,23,42,0.6)' if st.session_state.dark_mode else 'rgba(255,255,255,0.7)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(fig_diel, use_container_width=True)

    with col_info:
        st.markdown(f"""
        <div class="glass-card" style="height: 460px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <span class="physics-badge" style="background: rgba(99, 102, 241, 0.25); color: #818cf8; border-color: #6366f1;">Simulation Insight</span>
                <h3 style="margin: 0.5rem 0 1rem 0; font-size: 1.35rem; font-weight: 700;">
                    {sandbox_mode.split(' ')[1]} Dynamics
                </h3>
                <p style="color: #64748b; line-height: 1.6; font-size: 0.92rem;">
                    PhysicsMaster executes real-time differential equation integrations, matrix diagonalizations, and 3D geometric transformations at 60 FPS in WebGL.
                </p>
                <div class="math-formula">
                    {"\\Psi(x,t) = \\sum_{n} A_n e^{i(k_n x - \\omega_n t)}" if "Multi-Wave" in sandbox_mode else 
                     "\\mathbf{b}_1 = 2\\pi \\frac{\\mathbf{a}_2 \\times \\mathbf{a}_3}{\\mathbf{a}_1 \\cdot (\\mathbf{a}_2 \\times \\mathbf{a}_3)}" if "Brillouin" in sandbox_mode else
                     "\\frac{d\\mathbf{M}}{dt} = \\gamma \\mathbf{M} \\times \\mathbf{B} - \\frac{M_x\\hat{x}+M_y\\hat{y}}{T_2} - \\frac{(M_z-M_0)\\hat{z}}{T_1}" if "Bloch" in sandbox_mode else
                     "\\tilde{\\varepsilon}(\\omega) = \\varepsilon_\\infty + \\frac{\\varepsilon_s - \\varepsilon_\\infty}{1 + i\\omega\\tau}"}
                </div>
                <ul style="color: #64748b; font-size: 0.85rem; padding-left: 1.2rem; line-height: 1.6; margin-top: 0.6rem;">
                    <li>High-precision numerical integration</li>
                    <li>Full support for M.Sc coursework & research</li>
                    <li>Interactive 3D camera pan, zoom & orbital rotation</li>
                </ul>
            </div>
            <div>
                <a href="#explore-domains" style="text-decoration: none;">
                    <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; text-align: center; padding: 10px; border-radius: 12px; font-weight: 600; font-size: 0.9rem;">
                        Explore Complete Laboratory Modules ↓
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # 8 FEATURED PHYSICS DOMAINS (M.Sc Standard)
    # =========================================================================
    # =========================================================================
    # 8 FEATURED PHYSICS DOMAINS (M.Sc Standard)
    # =========================================================================
    st.markdown(f"""
    <div id="explore-domains" style="margin: 3.5rem 0 1.5rem 0; text-align: center;">
        <h2 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px; color: {text_primary};">
            🎓 Specialized Physics Laboratories
        </h2>
        <p style="color: {text_secondary}; font-size: 1.1rem; max-width: 750px; margin: 0.5rem auto 2rem auto;">
            Choose a physics domain to launch dedicated 3D interactive laboratories with advanced parameter controls and analytical solvers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    dom_cols1 = st.columns(4, gap="medium")
    
    # 1. Solid State Physics
    with dom_cols1[0]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">🔷</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Solid State Physics</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Crystal lattices, Band Theory, Phonons, Magnetic Resonance & Dielectrics.</p>
                <div class="math-formula">E(k) = E_0 - 2t \\cos(ka)</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • 3D First Brillouin Zones<br>
                    • Exact Debye Heat Capacity<br>
                    • NMR/EPR Bloch Dynamics<br>
                    • Ferroelectric Hysteresis
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Solid State →", key="btn_solid"):
            st.switch_page("pages/1_solid_state.py")

    # 2. Optics & Photonics
    with dom_cols1[1]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">🔭</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Optics & Photonics</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Ray matrices, Jones polarization calculus, cavities & diffraction gratings.</p>
                <div class="math-formula">n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • Poincaré Sphere Polarization<br>
                    • Fabry-Pérot Resonator<br>
                    • Fraunhofer Slit Diffraction<br>
                    • Lens Aberration Models
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Optics →", key="btn_optics"):
            st.switch_page("pages/2_optics.py")

    # 3. Waves & Oscillations
    with dom_cols1[2]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">🌊</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Waves & Oscillations</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Fourier synthesis, dispersive wavepackets & 2D Chladni plates.</p>
                <div class="math-formula">v_g = d\\omega/dk, \\quad v_p = \\omega/k</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • 2D Chladni Eigenmodes<br>
                    • Wavepacket Dispersal<br>
                    • Fourier Harmonic Builder<br>
                    • Doppler Shock Waves
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Waves →", key="btn_waves"):
            st.switch_page("pages/3_waves.py")

    # 4. Nuclear Physics
    with dom_cols1[3]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">⚛️</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Nuclear Physics</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Liquid drop SEMF, Bateman decay chains & nuclear shell model.</p>
                <div class="math-formula">B(A,Z) = a_v A - a_s A^{{2/3}} - \\dots</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • Semi-Empirical Mass Formula<br>
                    • Bateman Decay Chain ODEs<br>
                    • Q-Value Reaction Kinematics<br>
                    • Magic Number Shell Levels
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Nuclear →", key="btn_nuclear"):
            st.switch_page("pages/4_nuclear.py")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    dom_cols2 = st.columns(4, gap="medium")

    # 5. Superconductivity
    with dom_cols2[0]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">❄️</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Superconductivity</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">London theory, BCS energy gap, Abrikosov vortex lattices & SQUIDs.</p>
                <div class="math-formula">\\Delta(T) \\approx 1.764 k_B T_c \\tanh(...)</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • Meissner Effect Simulator<br>
                    • Ginzburg-Landau Vortex Lattice<br>
                    • BCS Gap Energy Dynamics<br>
                    • AC/DC Josephson Quantum
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Superconductivity →", key="btn_supercond"):
            st.switch_page("pages/5_superconductivity.py")

    # 6. Quantum Physics
    with dom_cols2[1]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">🌌</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Quantum Physics</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Schrödinger equation, finite barrier tunneling & 3D Bloch sphere.</p>
                <div class="math-formula">-\\frac{{\\hbar^2}}{{2m}}\\nabla^2\\psi + V\\psi = E\\psi</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • 3D Bloch Qubit States<br>
                    • Harmonic Oscillator Modes<br>
                    • Quantum Barrier Tunneling<br>
                    • Hydrogen Radial Profiles
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Quantum →", key="btn_quantum"):
            st.switch_page("pages/7_quantum_physics.py")

    # 7. AI Physics Assistant
    with dom_cols2[2]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">🧠</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">AI Physics Assistant</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Intelligent mathematical problem solver with LaTeX rendering.</p>
                <div class="math-formula">\\nabla \\times \\mathbf{{B}} = \\mu_0 \\mathbf{{J}} + \\mu_0\\epsilon_0\\frac{{\\partial\\mathbf{{E}}}}{{\\partial t}}</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • Step-by-Step Derivations<br>
                    • Conceptual Socratic Hints<br>
                    • M.Sc Exam Problem Presets<br>
                    • Multi-Model Support
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch AI Assistant →", key="btn_ai"):
            st.switch_page("pages/6_ai_physics_assistant.py")

    # 8. Physics Glossary & Matrix
    with dom_cols2[3]:
        st.markdown(f"""
        <div class="domain-card">
            <div>
                <span class="domain-icon">📚</span>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: {text_primary};">Physics Glossary</h3>
                <p style="color: {text_secondary}; font-size: 0.88rem; margin: 6px 0 12px 0;">Searchable graduate concept definitions with interactive calculators.</p>
                <div class="math-formula">\\oint \\mathbf{{E}} \\cdot d\\mathbf{{A}} = \\frac{{Q_{{\\text{{enc}}}}}}{{\\epsilon_0}}</div>
                <div style="color: {text_secondary}; font-size: 0.82rem; line-height: 1.6; margin-bottom: 15px;">
                    • 100+ Graduate Concepts<br>
                    • Instant LaTeX Formulas<br>
                    • Unit & Constant Converter<br>
                    • Cross-Module Index
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Glossary →", key="btn_glossary"):
            st.switch_page("pages/8_physics_glossary.py")

    # =========================================================================
    # FOOTER & GITHUB / DEPLOYMENT INFO
    # =========================================================================
    st.markdown(f"""
    <div style="margin-top: 4rem; padding: 2.5rem; background: {card_bg}; border-radius: 20px; border: 1px solid {card_border}; text-align: center;">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 700; color: {text_primary};">PhysicsMaster Open Source Platform</h3>
        <p style="color: {text_secondary}; font-size: 0.95rem; max-width: 650px; margin: 0 auto 1.5rem auto;">
            Designed for physics departments, researchers, and students globally. Pushed and configured for immediate deployment on Streamlit Cloud and Vercel.
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <span class="physics-badge" style="background: rgba(59,130,246,0.2); color: #60a5fa; border-color: #3b82f6;">Python 3.11+</span>
            <span class="physics-badge" style="background: rgba(16,185,129,0.2); color: #34d399; border-color: #10b981;">Streamlit 1.42+</span>
            <span class="physics-badge" style="background: rgba(245,158,11,0.2); color: #fbbf24; border-color: #f59e0b;">Plotly 3D WebGL</span>
            <span class="physics-badge" style="background: rgba(168,85,247,0.2); color: #c084fc; border-color: #a855f7;">SciPy & NumPy</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


# =========================================================================
# VERCEL SERVERLESS RUNTIME COMPATIBILITY EXPORTS
# =========================================================================
class VercelWSGIApp:
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = "<h1>PhysicsMaster</h1><p>Platform is running.</p>"
        return [content.encode('utf-8')]

app = VercelWSGIApp()
application = app
handler = app