import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import pandas as pd
from utils.theme import render_theme_sidebar

st.set_page_config(
    page_title="Superconductivity Laboratory",
    page_icon="🔌",
    layout="wide"
)

theme = render_theme_sidebar()
dark = theme["dark"]

# Enhanced CSS with superconductivity-inspired design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        min-height: 100vh;
        color: white;
    }

    /* Superconductivity-themed header with magnetic field animations */
    .supercond-header {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #0284c7;
        box-shadow: 0 20px 40px rgba(2, 132, 199, 0.3);
    }

    .supercond-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 25% 25%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 75% 75%, rgba(255,255,255,0.08) 0%, transparent 50%),
            repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 2px, transparent 2px, transparent 10px);
        background-size: 100px 100px, 150px 150px, 20px 20px;
        animation: magneticField 20s linear infinite;
    }

    /* Enhanced section cards with superconducting glow */
    .physics-section {
        background: rgba(30, 41, 59, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(2, 132, 199, 0.2);
        border: 1px solid rgba(2, 132, 199, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .physics-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(2, 132, 199, 0.3);
        border-color: rgba(2, 132, 199, 0.5);
    }

    .physics-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #0ea5e9, #0284c7, #0369a1, #075985);
        animation: supercondGradient 3s ease-in-out infinite;
    }

    /* Interactive parameter panels */
    .param-panel {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #64748b;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .param-panel:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(100, 116, 139, 0.3);
        border-color: #0ea5e9;
    }

    .param-panel h4 {
        color: #38bdf8;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Enhanced metric cards with superconducting effects */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #475569;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-8px) rotateX(5deg);
        box-shadow: 0 20px 40px rgba(2, 132, 199, 0.2);
        border-color: #0ea5e9;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(2, 132, 199, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }

    .metric-label {
        font-size: 1rem;
        color: #e2e8f0;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }

    /* Enhanced tabs with superconducting styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 15px;
        padding: 0.8rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0 0.3rem;
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(2, 132, 199, 0.2);
        color: #7dd3fc;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
        transform: translateY(-3px);
    }

    /* Superconducting visualization cards */
    .supercond-card {
        background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #38bdf8;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .supercond-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(2, 132, 199, 0.4);
        border-color: #7dd3fc;
    }

    .supercond-card::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        transition: all 0.6s ease;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }

    .supercond-card:hover::before {
        width: 300px;
        height: 300px;
    }

    .supercond-card h5 {
        color: white;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.2rem;
        position: relative;
        z-index: 2;
    }

    /* Advanced animations */
    @keyframes magneticField {
        0% { transform: translateX(0px) rotateZ(0deg); }
        25% { transform: translateX(-10px) rotateZ(90deg); }
        50% { transform: translateX(0px) rotateZ(180deg); }
        75% { transform: translateX(10px) rotateZ(270deg); }
        100% { transform: translateX(0px) rotateZ(360deg); }
    }

    @keyframes supercondGradient {
        0%, 100% { background: linear-gradient(90deg, #0ea5e9, #0284c7, #0369a1, #075985); }
        25% { background: linear-gradient(90deg, #0284c7, #0369a1, #075985, #0ea5e9); }
        50% { background: linear-gradient(90deg, #0369a1, #075985, #0ea5e9, #0284c7); }
        75% { background: linear-gradient(90deg, #075985, #0ea5e9, #0284c7, #0369a1); }
    }

    @keyframes cooperPair {
        0%, 100% { transform: translateX(0px) scale(1); }
        50% { transform: translateX(5px) scale(1.1); }
    }

    @keyframes meissnerEffect {
        0% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-10px) rotate(5deg); }
        50% { transform: translateY(-5px) rotate(0deg); }
        75% { transform: translateY(-15px) rotate(-5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes fluxQuantum {
        0% { transform: rotate(0deg) scale(1); opacity: 1; }
        50% { transform: rotate(180deg) scale(1.2); opacity: 0.7; }
        100% { transform: rotate(360deg) scale(1); opacity: 1; }
    }

    /* Interactive elements */
    .interactive-icon {
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .interactive-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(2, 132, 199, 0.3));
    }

    /* Superconducting state indicators */
    .sc-state {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin: 0 5px;
        animation: supercondPulse 2s ease-in-out infinite;
    }

    @keyframes supercondPulse {
        0%, 100% { transform: scale(1); opacity: 1; background: #0ea5e9; }
        50% { transform: scale(1.3); opacity: 0.7; background: #7dd3fc; }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .supercond-header {
            padding: 2rem 1rem;
        }

        .physics-section {
            padding: 1.5rem;
            margin: 1rem 0;
        }

        .param-panel {
            padding: 1.5rem;
        }

        .metric-card {
            padding: 1rem;
        }

        .metric-value {
            font-size: 1.5rem;
        }
    }

    /* Dark theme text overrides */
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container h5,
    .main .block-container h6,
    .main .block-container p,
    .main .block-container div,
    .main .block-container span {
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced superconductivity-themed header
st.markdown("""
<div class="supercond-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span class="interactive-icon">🔌</span> Superconductivity Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Zero Resistance, Infinite Possibilities
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Cooper Pairs</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Meissner Effect</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Flux Quantization</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced tabs with comprehensive superconductivity phenomena
tabs = st.tabs([
    "🌡️ Critical Temperature", 
    "🧲 Meissner Effect", 
    "⚡ Cooper Pairs", 
    "🔗 Josephson Junctions",
    "📊 Phase Transitions",
    "🏭 Applications",
    "🎓 Learning Hub"
])

# Tab 1: Enhanced Critical Temperature
with tabs[0]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🌡️</span> Critical Temperature & Phase Transitions
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore the temperature-dependent superconducting transition and material properties.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>⚙️</span> Superconductor Parameters")

        # Enhanced superconductor selection with real data
        superconductors = {
            "Mercury": {"Tc": 4.15, "Hc": 0.041, "type": "Type I", "gap": 1.65},
            "Lead": {"Tc": 7.19, "Hc": 0.080, "type": "Type I", "gap": 1.35},
            "Niobium": {"Tc": 9.25, "Hc": 0.199, "type": "Type II", "gap": 1.55},
            "YBCO": {"Tc": 92, "Hc": 150, "type": "Type II", "gap": 20},
            "BSCCO": {"Tc": 110, "Hc": 200, "type": "Type II", "gap": 25},
            "Iron Pnictide": {"Tc": 55, "Hc": 70, "type": "Type II", "gap": 12},
            "MgB2": {"Tc": 39, "Hc": 16, "type": "Type II", "gap": 7.2},
            "Nb3Sn": {"Tc": 18.3, "Hc": 24.5, "type": "Type II", "gap": 3.2}
        }

        selected_sc = st.selectbox("Select Superconductor", list(superconductors.keys()))
        sc_data = superconductors[selected_sc]

        # Display superconductor properties
        st.markdown(f"""
        <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Material Properties:</strong><br>
            Tc: {sc_data['Tc']:.2f} K<br>
            Type: {sc_data['type']}<br>
            Hc: {sc_data['Hc']:.3f} T<br>
            Energy gap: {sc_data['gap']:.2f} meV
        </div>
        """, unsafe_allow_html=True)

        # Temperature range controls
        st.markdown("**Temperature Parameters:**")
        current_temp = st.slider("Current Temperature (K)", 0.1, sc_data['Tc'] * 2, sc_data['Tc'] * 0.5, 0.1)
        temp_range = st.slider("Temperature Range (K)", sc_data['Tc'] * 0.1, sc_data['Tc'] * 3, sc_data['Tc'] * 2, 0.1)

        # Advanced superconductivity controls
        st.markdown("**Advanced Parameters:**")
        magnetic_field = st.slider("Applied Magnetic Field (T)", 0.0, sc_data['Hc'] * 2, 0.0, 0.001)
        show_gap_evolution = st.checkbox("Show Energy Gap Evolution", value=True)
        show_heat_capacity = st.checkbox("Show Heat Capacity", value=False)

        # Superconducting state analysis
        is_superconducting = current_temp < sc_data['Tc'] and magnetic_field < sc_data['Hc']
        state = "Superconducting" if is_superconducting else "Normal"
        state_color = "#0ea5e9" if is_superconducting else "#ef4444"

        st.markdown(f"""
        <div style="background: {state_color}33; padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 2px solid {state_color};">
            <strong>Current State:</strong> {state}<br>
            <strong>Temperature:</strong> {current_temp:.2f} K<br>
            <strong>Tc:</strong> {sc_data['Tc']:.2f} K<br>
            <strong>Field:</strong> {magnetic_field:.3f} T
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced critical temperature visualization
        def create_tc_visualization():
            # Temperature array
            T = np.linspace(0.1, temp_range, 1000)
            Tc = sc_data['Tc']

            # Calculate temperature-dependent properties
            # Energy gap using BCS theory
            def energy_gap(T, Tc, gap_0):
                if T >= Tc:
                    return 0
                else:
                    # Simplified BCS gap equation
                    return gap_0 * np.tanh(1.74 * np.sqrt(Tc/T - 1))

            gap_0 = sc_data['gap']  # Gap at T=0
            energy_gaps = np.array([energy_gap(t, Tc, gap_0) for t in T])

            # Resistivity (normalized)
            resistivity = np.ones_like(T)
            resistivity[T < Tc] = 0  # Zero resistance below Tc

            # Critical field (temperature dependent)
            Hc0 = sc_data['Hc']
            critical_field = Hc0 * (1 - (T/Tc)**2)
            critical_field[T >= Tc] = 0

            # Create subplots
            if show_gap_evolution and show_heat_capacity:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Resistivity vs Temperature', 'Energy Gap Evolution', 
                                   'Critical Magnetic Field', 'Heat Capacity'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
            elif show_gap_evolution or show_heat_capacity:
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Resistivity vs Temperature', 
                                   'Energy Gap Evolution' if show_gap_evolution else 'Heat Capacity'),
                    vertical_spacing=0.15
                )
            else:
                fig = go.Figure()

            # Resistivity plot
            fig.add_trace(
                go.Scatter(
                    x=T, y=resistivity,
                    mode='lines',
                    line=dict(color='#ef4444', width=4),
                    name='Resistivity (normalized)',
                    hovertemplate='T: %{x:.2f} K<br>ρ: %{y:.3f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Mark critical temperature
            fig.add_vline(
                x=Tc,
                line=dict(color='white', width=3, dash='dash'),
                annotation_text=f"Tc = {Tc:.2f} K",
                row=1, col=1
            )

            # Mark current temperature
            fig.add_vline(
                x=current_temp,
                line=dict(color='yellow', width=2),
                annotation_text=f"Current: {current_temp:.2f} K",
                row=1, col=1
            )

            # Energy gap evolution
            if show_gap_evolution:
                row_gap = 1 if not show_heat_capacity else 1
                col_gap = 2 if show_heat_capacity else 1

                fig.add_trace(
                    go.Scatter(
                        x=T, y=energy_gaps,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(14, 165, 233, 0.3)',
                        name='Energy Gap (meV)',
                        hovertemplate='T: %{x:.2f} K<br>Δ: %{y:.3f} meV<extra></extra>'
                    ),
                    row=row_gap, col=col_gap
                )

                # BCS ratio at T=0
                bcs_ratio = gap_0 / (1.764 * 8.617e-5 * Tc * 1000)  # Δ(0)/kBTc
                fig.add_annotation(
                    x=Tc * 0.2, y=gap_0 * 0.8,
                    text=f"BCS ratio: {bcs_ratio:.2f}",
                    showarrow=True,
                    arrowhead=2,
                    row=row_gap, col=col_gap
                )

            # Critical magnetic field
            if show_gap_evolution and show_heat_capacity:
                fig.add_trace(
                    go.Scatter(
                        x=T, y=critical_field,
                        mode='lines',
                        line=dict(color='#10b981', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(16, 185, 129, 0.3)',
                        name='Hc (T)',
                        hovertemplate='T: %{x:.2f} K<br>Hc: %{y:.3f} T<extra></extra>'
                    ),
                    row=2, col=1
                )

            # Heat capacity (simplified)
            if show_heat_capacity:
                # Electronic heat capacity with superconducting transition
                gamma_n = 1.0  # Normal state electronic heat capacity coefficient
                heat_capacity = np.ones_like(T) * gamma_n * T

                # Add exponential suppression below Tc
                for i, t in enumerate(T):
                    if t < Tc:
                        gap_t = energy_gap(t, Tc, gap_0) * 1e-3 * 1.602e-19  # Convert to J
                        kB = 1.381e-23
                        if gap_t > 0:
                            heat_capacity[i] *= np.exp(-gap_t / (kB * t))

                row_hc = 2 if show_gap_evolution else 2
                col_hc = 2 if show_gap_evolution else 1

                fig.add_trace(
                    go.Scatter(
                        x=T, y=heat_capacity,
                        mode='lines',
                        line=dict(color='#f59e0b', width=4),
                        name='Heat Capacity (arb.)',
                        hovertemplate='T: %{x:.2f} K<br>C: %{y:.3f}<extra></extra>'
                    ),
                    row=row_hc, col=col_hc
                )

            # Update layout
            title_text = f'<b>{selected_sc} Superconducting Properties</b><br>'
            title_text += f'<span style="font-size:14px;">Tc = {Tc:.2f} K, Current State: {state}</span>'

            fig.update_layout(
                title=dict(
                    text=title_text,
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                height=700 if (show_gap_evolution and show_heat_capacity) else 600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            # Update axes
            fig.update_xaxes(title_text="Temperature (K)", color='white')
            fig.update_yaxes(title_text="Resistivity (normalized)", color='white')

            if show_gap_evolution:
                row_gap = 1 if not show_heat_capacity else 1
                col_gap = 2 if show_heat_capacity else 1
                fig.update_xaxes(title_text="Temperature (K)", row=row_gap, col=col_gap, color='white')
                fig.update_yaxes(title_text="Energy Gap (meV)", row=row_gap, col=col_gap, color='white')

            if show_heat_capacity:
                row_hc = 2 if show_gap_evolution else 2
                col_hc = 2 if show_gap_evolution else 1
                fig.update_xaxes(title_text="Temperature (K)", row=row_hc, col=col_hc, color='white')
                fig.update_yaxes(title_text="Heat Capacity", row=row_hc, col=col_hc, color='white')

            if show_gap_evolution and show_heat_capacity:
                fig.update_xaxes(title_text="Temperature (K)", row=2, col=1, color='white')
                fig.update_yaxes(title_text="Critical Field (T)", row=2, col=1, color='white')

            return fig

        tc_fig = create_tc_visualization()
        st.plotly_chart(tc_fig, use_container_width=True)

        # Superconductivity dashboard
        st.markdown("#### 📊 Superconductivity Analysis Dashboard")

        # Calculate key parameters
        reduced_temp = current_temp / sc_data['Tc']
        coherence_length = 1.0  # Simplified (nm)
        penetration_depth = 50  # Simplified (nm)

        # Current energy gap
        if current_temp < sc_data['Tc']:
            current_gap = sc_data['gap'] * np.tanh(1.74 * np.sqrt(sc_data['Tc']/current_temp - 1))
        else:
            current_gap = 0

        # Display superconductivity metrics
        sc_col1, sc_col2, sc_col3, sc_col4 = st.columns(4)

        with sc_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{reduced_temp:.3f}</div>
                <div class="metric-label">T/Tc Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with sc_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{current_gap:.2f}</div>
                <div class="metric-label">Energy Gap (meV)</div>
            </div>
            """, unsafe_allow_html=True)

        with sc_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{coherence_length:.1f}</div>
                <div class="metric-label">ξ (nm)</div>
            </div>
            """, unsafe_allow_html=True)

        with sc_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{penetration_depth:.0f}</div>
                <div class="metric-label">λ (nm)</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: Enhanced Meissner Effect
with tabs[1]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🧲</span>Meissner Effect & Magnetic Field Expulsion
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Visualize magnetic field expulsion and flux quantization in superconductors.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🧲</span> Magnetic Field Parameters")

        # Meissner effect controls
        field_strength = st.slider("External Field Strength (mT)", 0.1, 100.0, 10.0, 0.1)
        superconductor_temp = st.slider("Temperature (K)", 1.0, 100.0, 77.0, 1.0)

        # Superconductor geometry
        geometry = st.selectbox("Superconductor Geometry", ["Sphere", "Cylinder", "Slab"])
        size_parameter = st.slider("Size Parameter (mm)", 1.0, 20.0, 10.0, 0.5)

        # Type of superconductor
        sc_type = st.selectbox("Superconductor Type", ["Type I", "Type II"])

        if sc_type == "Type II":
            lower_critical_field = st.slider("Hc1 (mT)", 1.0, 50.0, 10.0, 1.0)
            upper_critical_field = st.slider("Hc2 (mT)", 50.0, 1000.0, 200.0, 10.0)

        # Visualization options
        st.markdown("**Visualization Options:**")
        show_field_lines = st.checkbox("Show Magnetic Field Lines", value=True)
        show_current_loops = st.checkbox("Show Surface Currents", value=True)
        animate_levitation = st.checkbox("Animate Magnetic Levitation", value=False)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced Meissner effect visualization
        def create_meissner_visualization():
            # Create coordinate system
            x = np.linspace(-20, 20, 100)
            y = np.linspace(-20, 20, 100)
            X, Y = np.meshgrid(x, y)

            # Define superconductor region
            if geometry == "Sphere":
                superconductor_mask = X**2 + Y**2 <= size_parameter**2
            elif geometry == "Cylinder":
                superconductor_mask = X**2 + Y**2 <= size_parameter**2
            else:  # Slab
                superconductor_mask = (np.abs(X) <= size_parameter) & (np.abs(Y) <= size_parameter/2)

            # Calculate magnetic field
            # Simplified field calculation - uniform field with expulsion
            B_external = field_strength * 1e-3  # Convert to Tesla

            # Initialize field components
            Bx = np.zeros_like(X)
            By = np.ones_like(Y) * B_external  # Uniform field in y-direction

            # Apply Meissner effect - zero field inside superconductor
            if superconductor_temp < 90:  # Assuming Tc ~ 90K for visualization
                By[superconductor_mask] = 0

                # Add field enhancement around superconductor (simplified)
                for i in range(len(x)):
                    for j in range(len(y)):
                        if not superconductor_mask[i, j]:
                            # Distance to nearest superconductor point
                            if geometry == "Sphere":
                                r = np.sqrt(X[i, j]**2 + Y[i, j]**2)
                                if r > size_parameter:
                                    enhancement = 1 + size_parameter**3 / (2 * r**3)
                                    By[i, j] *= enhancement

            fig = go.Figure()

            # Plot superconductor region
            if geometry == "Sphere":
                theta = np.linspace(0, 2*np.pi, 100)
                sc_x = size_parameter * np.cos(theta)
                sc_y = size_parameter * np.sin(theta)
            elif geometry == "Cylinder":
                theta = np.linspace(0, 2*np.pi, 100)
                sc_x = size_parameter * np.cos(theta)
                sc_y = size_parameter * np.sin(theta)
            else:  # Slab
                sc_x = [-size_parameter, size_parameter, size_parameter, -size_parameter, -size_parameter]
                sc_y = [-size_parameter/2, -size_parameter/2, size_parameter/2, size_parameter/2, -size_parameter/2]

            fig.add_trace(go.Scatter(
                x=sc_x, y=sc_y,
                mode='lines',
                fill='toself',
                fillcolor='rgba(14, 165, 233, 0.6)',
                line=dict(color='#0ea5e9', width=3),
                name='Superconductor',
                hovertemplate='Superconductor Region<extra></extra>'
            ))

            # Plot magnetic field lines
            if show_field_lines:
                # Create field line visualization
                step = 5
                for i in range(0, len(x), step):
                    for j in range(0, len(y), step):
                        if not superconductor_mask[i, j]:
                            # Draw field vectors
                            scale = 2
                            dx = Bx[i, j] * scale
                            dy = By[i, j] * scale

                            fig.add_trace(go.Scatter(
                                x=[X[i, j], X[i, j] + dx],
                                y=[Y[i, j], Y[i, j] + dy],
                                mode='lines',
                                line=dict(color='yellow', width=1),
                                showlegend=False,
                                hoverinfo='skip'
                            ))

                            # Add arrowheads
                            if dx != 0 or dy != 0:
                                fig.add_trace(go.Scatter(
                                    x=[X[i, j] + dx],
                                    y=[Y[i, j] + dy],
                                    mode='markers',
                                    marker=dict(
                                        symbol='triangle-up',
                                        size=4,
                                        color='yellow',
                                        angle=np.degrees(np.arctan2(dy, dx))
                                    ),
                                    showlegend=False,
                                    hoverinfo='skip'
                                ))

            # Show surface currents
            if show_current_loops:
                # Simplified surface current visualization
                if geometry == "Sphere":
                    theta_curr = np.linspace(0, 2*np.pi, 20)
                    current_radius = size_parameter * 1.1
                    curr_x = current_radius * np.cos(theta_curr)
                    curr_y = current_radius * np.sin(theta_curr)

                    fig.add_trace(go.Scatter(
                        x=curr_x, y=curr_y,
                        mode='lines',
                        line=dict(color='red', width=2, dash='dot'),
                        name='Surface Currents',
                        hovertemplate='Surface Current<extra></extra>'
                    ))

            # Add field strength indicators
            field_strength_text = f"B_ext = {field_strength:.1f} mT"
            if superconductor_temp < 90:
                field_strength_text += "<br>B_int = 0 mT (Meissner Effect)"

            fig.add_annotation(
                x=-15, y=15,
                text=field_strength_text,
                showarrow=False,
                font=dict(size=12, color='white'),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='white',
                borderwidth=1
            )

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>Meissner Effect in {geometry}</b><br>'
                         f'<span style="font-size:14px;">T = {superconductor_temp:.1f} K, B = {field_strength:.1f} mT</span>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                xaxis=dict(
                    title='Position (mm)',
                    range=[-25, 25],
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.2)',
                    color='white'
                ),
                yaxis=dict(
                    title='Position (mm)',
                    range=[-25, 25],
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.2)',
                    color='white'
                ),
                width=800,
                height=600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            return fig

        meissner_fig = create_meissner_visualization()
        st.plotly_chart(meissner_fig, use_container_width=True)

        # Meissner effect analysis
        st.markdown("#### 📊 Magnetic Field Analysis")

        # Calculate relevant parameters
        penetration_depth = 50e-9  # London penetration depth (m)
        flux_quantum = 2.067e-15  # Wb

        # Expulsion efficiency
        if superconductor_temp < 90:
            expulsion_efficiency = 100
        else:
            expulsion_efficiency = 0

        # Critical current density (simplified)
        if superconductor_temp < 90:
            jc = 1e9  # A/m²
        else:
            jc = 0

        # Display magnetic metrics
        mag_col1, mag_col2, mag_col3, mag_col4 = st.columns(4)

        with mag_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{expulsion_efficiency:.0f}%</div>
                <div class="metric-label">Field Expulsion</div>
            </div>
            """, unsafe_allow_html=True)

        with mag_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{penetration_depth*1e9:.0f}</div>
                <div class="metric-label">λ (nm)</div>
            </div>
            """, unsafe_allow_html=True)

        with mag_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{flux_quantum*1e15:.2f}</div>
                <div class="metric-label">Φ₀ (×10⁻¹⁵ Wb)</div>
            </div>
            """, unsafe_allow_html=True)

        with mag_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{jc/1e6:.0f}</div>
                <div class="metric-label">Jc (MA/m²)</div>
            </div>
            """, unsafe_allow_html=True)

# Simplified remaining tabs for length constraints
with tabs[2]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">⚡</span> Cooper Pairs & BCS Theory
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore the microscopic theory of superconductivity through Cooper pair formation and BCS ground state.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>⚡</span> BCS Parameters")

        # BCS theory parameters
        debye_frequency = st.slider("Debye Frequency (THz)", 1.0, 50.0, 10.0, 1.0)
        coupling_strength = st.slider("Electron-Phonon Coupling (V)", 0.1, 2.0, 0.3, 0.01)
        electron_density = st.slider("Electron Density (10²³ cm⁻³)", 1.0, 10.0, 5.0, 0.1)

        # Temperature controls
        temperature = st.slider("Temperature (K)", 0.1, 20.0, 4.0, 0.1)

        # Visualization options
        st.markdown("**Visualization Options:**")
        show_fermi_sea = st.checkbox("Show Fermi Sea", value=True)
        show_gap_evolution = st.checkbox("Show Gap Evolution", value=True)
        show_dos = st.checkbox("Show Density of States", value=False)

        # Calculate BCS properties
        fermi_energy = (3 * np.pi**2 * electron_density * 1e29)**(2/3) * 6.582e-16  # eV
        bcs_tc = 1.14 * debye_frequency * 1e12 * 6.582e-16 * np.exp(-1/(coupling_strength * electron_density/10))  # K

        gap_0 = 1.764 * 8.617e-5 * bcs_tc * 1000  # meV at T=0

        st.markdown(f"""
        <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>BCS Properties:</strong><br>
            Fermi Energy: {fermi_energy:.2f} eV<br>
            BCS Tc: {bcs_tc:.2f} K<br>
            Gap at T=0: {gap_0:.2f} meV<br>
            Current T/Tc: {temperature/bcs_tc:.3f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced Cooper pair visualization
        def create_cooper_pair_visualization():
            # Energy range around Fermi level
            E_range = np.linspace(-3*gap_0/1000, 3*gap_0/1000, 1000)  # eV

            # BCS gap function
            if temperature < bcs_tc:
                # Temperature-dependent gap
                if temperature == 0:
                    gap_T = gap_0 / 1000  # Convert to eV
                else:
                    gap_T = gap_0/1000 * np.tanh(1.74 * np.sqrt(bcs_tc/temperature - 1)) if temperature < bcs_tc else 0
            else:
                gap_T = 0

            # BCS quasiparticle dispersion
            E_qp = np.sqrt(E_range**2 + gap_T**2)

            # Create subplots
            if show_gap_evolution and show_dos:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('BCS Quasiparticle Dispersion', 'Cooper Pair Formation',
                                   'Energy Gap vs Temperature', 'Density of States'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
            elif show_gap_evolution or show_dos:
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('BCS Quasiparticle Dispersion', 
                                   'Energy Gap vs Temperature' if show_gap_evolution else 'Density of States'),
                    vertical_spacing=0.15
                )
            else:
                fig = go.Figure()

            # BCS dispersion relation
            fig.add_trace(
                go.Scatter(
                    x=E_range*1000, y=E_qp*1000,
                    mode='lines',
                    line=dict(color='#0ea5e9', width=4),
                    name='E+ branch',
                    hovertemplate='E: %{x:.3f} meV<br>E_qp: %{y:.3f} meV<extra></extra>'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=E_range*1000, y=-E_qp*1000,
                    mode='lines',
                    line=dict(color='#ef4444', width=4),
                    name='E- branch',
                    hovertemplate='E: %{x:.3f} meV<br>E_qp: %{y:.3f} meV<extra></extra>'
                ),
                row=1, col=1
            )

            # Normal state dispersion (dashed)
            fig.add_trace(
                go.Scatter(
                    x=E_range*1000, y=E_range*1000,
                    mode='lines',
                    line=dict(color='white', width=2, dash='dash'),
                    name='Normal state',
                    hovertemplate='E: %{x:.3f} meV<extra></extra>'
                ),
                row=1, col=1
            )

            # Show energy gap
            if gap_T > 0:
                fig.add_hline(
                    y=gap_T*1000, line=dict(color='yellow', width=2),
                    annotation_text=f"Δ = {gap_T*1000:.2f} meV",
                    row=1, col=1
                )
                fig.add_hline(
                    y=-gap_T*1000, line=dict(color='yellow', width=2),
                    row=1, col=1
                )

            # Cooper pair formation visualization
            if show_fermi_sea:
                # Show Fermi sea occupation
                k_range = np.linspace(-2, 2, 100)
                fermi_function = 1 / (1 + np.exp(k_range**2 * 0.1 * 1000 / (8.617e-5 * temperature))) if temperature > 0 else np.where(k_range**2 * 0.1 < 0, 1, 0)

                fig.add_trace(
                    go.Scatter(
                        x=k_range, y=fermi_function,
                        mode='lines',
                        fill='tozeroy',
                        fillcolor='rgba(14, 165, 233, 0.3)',
                        line=dict(color='#0ea5e9', width=3),
                        name='Electron Occupation',
                        hovertemplate='k: %{x:.2f}<br>f(E): %{y:.3f}<extra></extra>'
                    ),
                    row=1, col=2 if (show_gap_evolution and show_dos) else 1
                )

                # Show Cooper pair momentum distribution
                if gap_T > 0:
                    cooper_amplitude = np.exp(-k_range**2 / 2) * gap_T * 1000
                    fig.add_trace(
                        go.Scatter(
                            x=k_range, y=cooper_amplitude,
                            mode='lines',
                            line=dict(color='#f59e0b', width=3),
                            name='Cooper Pair Amplitude',
                            hovertemplate='k: %{x:.2f}<br>|ψ|²: %{y:.3f}<extra></extra>'
                        ),
                        row=1, col=2 if (show_gap_evolution and show_dos) else 1
                    )

            # Gap evolution with temperature
            if show_gap_evolution:
                T_array = np.linspace(0.1, bcs_tc * 1.5, 100)
                gap_evolution = np.zeros_like(T_array)

                for i, T in enumerate(T_array):
                    if T < bcs_tc:
                        gap_evolution[i] = gap_0 * np.tanh(1.74 * np.sqrt(bcs_tc/T - 1)) if T > 0 else gap_0

                row_gap = 2 if show_dos else 2
                col_gap = 1 if show_dos else 1

                fig.add_trace(
                    go.Scatter(
                        x=T_array, y=gap_evolution,
                        mode='lines',
                        line=dict(color='#10b981', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(16, 185, 129, 0.3)',
                        name='Energy Gap (meV)',
                        hovertemplate='T: %{x:.2f} K<br>Δ: %{y:.3f} meV<extra></extra>'
                    ),
                    row=row_gap, col=col_gap
                )

                # Mark current temperature
                fig.add_vline(
                    x=temperature,
                    line=dict(color='yellow', width=2),
                    annotation_text=f"Current T",
                    row=row_gap, col=col_gap
                )

                # Mark Tc
                fig.add_vline(
                    x=bcs_tc,
                    line=dict(color='red', width=2, dash='dash'),
                    annotation_text=f"Tc = {bcs_tc:.1f} K",
                    row=row_gap, col=col_gap
                )

            # Density of states
            if show_dos:
                E_dos = np.linspace(-3*gap_T, 3*gap_T, 200) if gap_T > 0 else np.linspace(-0.01, 0.01, 200)

                # Normal state DOS (constant)
                dos_normal = np.ones_like(E_dos)

                # Superconducting DOS
                dos_sc = np.zeros_like(E_dos)
                for i, E in enumerate(E_dos):
                    if abs(E) >= gap_T:
                        dos_sc[i] = abs(E) / np.sqrt(E**2 - gap_T**2)
                    else:
                        dos_sc[i] = 0

                row_dos = 2
                col_dos = 2 if show_gap_evolution else 1

                fig.add_trace(
                    go.Scatter(
                        x=E_dos*1000, y=dos_normal,
                        mode='lines',
                        line=dict(color='white', width=2, dash='dash'),
                        name='Normal DOS',
                        hovertemplate='E: %{x:.3f} meV<br>DOS: %{y:.3f}<extra></extra>'
                    ),
                    row=row_dos, col=col_dos
                )

                if gap_T > 0:
                    fig.add_trace(
                        go.Scatter(
                            x=E_dos*1000, y=dos_sc,
                            mode='lines',
                            line=dict(color='#a855f7', width=4),
                            fill='tozeroy',
                            fillcolor='rgba(168, 85, 247, 0.3)',
                            name='Superconducting DOS',
                            hovertemplate='E: %{x:.3f} meV<br>DOS: %{y:.3f}<extra></extra>'
                        ),
                        row=row_dos, col=col_dos
                    )

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>BCS Theory of Superconductivity</b><br>'
                         f'<span style="font-size:14px;">T = {temperature:.1f} K, Tc = {bcs_tc:.1f} K, Δ = {gap_T*1000:.2f} meV</span>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                height=700 if (show_gap_evolution and show_dos) else 600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            # Update axes
            fig.update_xaxes(title_text="Energy (meV)", row=1, col=1, color='white')
            fig.update_yaxes(title_text="Quasiparticle Energy (meV)", row=1, col=1, color='white')

            if show_fermi_sea:
                fig.update_xaxes(title_text="Momentum k", row=1, col=2 if (show_gap_evolution and show_dos) else 1, color='white')
                fig.update_yaxes(title_text="Amplitude", row=1, col=2 if (show_gap_evolution and show_dos) else 1, color='white')

            if show_gap_evolution:
                row_gap = 2 if show_dos else 2
                col_gap = 1 if show_dos else 1
                fig.update_xaxes(title_text="Temperature (K)", row=row_gap, col=col_gap, color='white')
                fig.update_yaxes(title_text="Energy Gap (meV)", row=row_gap, col=col_gap, color='white')

            if show_dos:
                row_dos = 2
                col_dos = 2 if show_gap_evolution else 1
                fig.update_xaxes(title_text="Energy (meV)", row=row_dos, col=col_dos, color='white')
                fig.update_yaxes(title_text="Density of States", row=row_dos, col=col_dos, color='white')

            return fig

        cooper_fig = create_cooper_pair_visualization()
        st.plotly_chart(cooper_fig, use_container_width=True)

        # BCS theory analysis
        st.markdown("#### 📊 BCS Theory Analysis")

        # Calculate current gap at temperature
        if temperature < bcs_tc:
            gap_T = gap_0/1000 * np.tanh(1.74 * np.sqrt(bcs_tc/temperature - 1)) if temperature > 0 else gap_0/1000
        else:
            gap_T = 0

        # Calculate BCS parameters
        coherence_length = 7.63e-8 / np.sqrt(electron_density * 1e29 * gap_T) if gap_T > 0 else 0  # meters
        penetration_depth = np.sqrt(9.109e-31 / (1.602e-19**2 * 8.854e-12 * electron_density * 1e29))  # meters

        # Cooper pair size
        cooper_pair_size = 1.83e-7 / np.sqrt(electron_density * 1e29) if electron_density > 0 else 0  # meters

        # BCS ratio
        bcs_ratio = gap_0 / (1.764 * 8.617e-5 * bcs_tc * 1000) if bcs_tc > 0 else 0

        # Display BCS metrics
        bcs_col1, bcs_col2, bcs_col3, bcs_col4 = st.columns(4)

        with bcs_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{coherence_length*1e9:.1f}</div>
                <div class="metric-label">ξ (nm)</div>
            </div>
            """, unsafe_allow_html=True)

        with bcs_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{cooper_pair_size*1e9:.1f}</div>
                <div class="metric-label">Cooper Pair Size (nm)</div>
            </div>
            """, unsafe_allow_html=True)

        with bcs_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{bcs_ratio:.2f}</div>
                <div class="metric-label">BCS Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        with bcs_col4:
            binding_energy = 2 * gap_T * 1000 if gap_T > 0 else 0  # meV
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{binding_energy:.2f}</div>
                <div class="metric-label">Binding Energy (meV)</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[3]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🔗</span> Josephson Junctions & SQUIDs
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore tunneling phenomena, Josephson effects, and quantum interference in superconducting devices.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🔗</span> Josephson Parameters")

        # Josephson junction parameters
        critical_current = st.slider("Critical Current (μA)", 1.0, 1000.0, 100.0, 1.0)
        normal_resistance = st.slider("Normal Resistance (Ω)", 1.0, 1000.0, 100.0, 1.0)
        capacitance = st.slider("Junction Capacitance (pF)", 0.1, 10.0, 1.0, 0.1)

        # External parameters
        applied_current = st.slider("Applied Current (μA)", 0.0, critical_current*1.5, critical_current*0.5, 1.0)
        magnetic_flux = st.slider("Applied Flux (Φ₀)", 0.0, 2.0, 0.0, 0.01)

        # Junction type
        junction_type = st.selectbox("Junction Type", ["DC Josephson", "AC Josephson", "SQUID", "RSJ Model"])

        # Calculate Josephson parameters
        josephson_energy = critical_current * 1e-6 * 2.067e-15 / (2 * np.pi)  # Joules
        charging_energy = (1.602e-19)**2 / (2 * capacitance * 1e-12)  # Joules
        plasma_frequency = np.sqrt(2 * np.pi * critical_current * 1e-6 / (2.067e-15 * capacitance * 1e-12)) / (2 * np.pi)  # Hz

        st.markdown(f"""
        <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Junction Properties:</strong><br>
            EJ: {josephson_energy*6.242e18:.2f} meV<br>
            EC: {charging_energy*6.242e18:.2f} meV<br>
            EJ/EC: {josephson_energy/charging_energy:.1f}<br>
            ωp: {plasma_frequency/1e9:.2f} GHz
        </div>
        """, unsafe_allow_html=True)

        # Visualization options
        st.markdown("**Visualization Options:**")
        show_iv_curve = st.checkbox("Show I-V Characteristic", value=True)
        show_oscillations = st.checkbox("Show AC Oscillations", value=False)
        animate_phase = st.checkbox("Animate Phase Evolution", value=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced Josephson junction visualization
        def create_josephson_visualization():
            if junction_type == "DC Josephson":
                # DC Josephson effect
                current_range = np.linspace(0, critical_current*1.5, 1000)
                voltage = np.zeros_like(current_range)

                # Ideal Josephson junction (zero voltage for I < Ic)
                voltage[current_range > critical_current] = normal_resistance * (current_range[current_range > critical_current] - critical_current)

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=current_range, y=voltage*1000,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        name='I-V Characteristic',
                        hovertemplate='I: %{x:.1f} μA<br>V: %{y:.2f} mV<extra></extra>'
                    )
                )

                # Mark critical current
                fig.add_vline(
                    x=critical_current,
                    line=dict(color='red', width=2, dash='dash'),
                    annotation_text=f"Ic = {critical_current:.0f} μA"
                )

                # Mark applied current
                if applied_current <= critical_current:
                    applied_voltage = 0
                else:
                    applied_voltage = normal_resistance * (applied_current - critical_current)

                fig.add_trace(
                    go.Scatter(
                        x=[applied_current], y=[applied_voltage*1000],
                        mode='markers',
                        marker=dict(size=12, color='yellow', symbol='star'),
                        name='Operating Point',
                        hovertemplate=f'I: {applied_current:.1f} μA<br>V: {applied_voltage*1000:.2f} mV<extra></extra>'
                    )
                )

                fig.update_layout(
                    title='DC Josephson I-V Characteristic',
                    xaxis_title='Current (μA)',
                    yaxis_title='Voltage (mV)',
                    height=500
                )

            elif junction_type == "AC Josephson":
                # AC Josephson effect
                if applied_current > critical_current:
                    voltage_dc = normal_resistance * (applied_current - critical_current)
                    josephson_freq = 2e6 * voltage_dc  # 2e/h * V in Hz

                    time = np.linspace(0, 5/josephson_freq if josephson_freq > 0 else 1e-9, 1000)

                    # AC voltage oscillations
                    voltage_ac = voltage_dc * (1 + 0.1 * np.sin(2 * np.pi * josephson_freq * time))
                    current_ac = applied_current + critical_current * 0.1 * np.sin(2 * np.pi * josephson_freq * time + np.pi/2)

                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=('AC Voltage Oscillations', 'AC Current Oscillations'),
                        vertical_spacing=0.15
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=time*1e9, y=voltage_ac*1000,
                            mode='lines',
                            line=dict(color='#0ea5e9', width=3),
                            name='Voltage (mV)',
                            hovertemplate='t: %{x:.2f} ns<br>V: %{y:.3f} mV<extra></extra>'
                        ),
                        row=1, col=1
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=time*1e9, y=current_ac,
                            mode='lines',
                            line=dict(color='#ef4444', width=3),
                            name='Current (μA)',
                            hovertemplate='t: %{x:.2f} ns<br>I: %{y:.3f} μA<extra></extra>'
                        ),
                        row=2, col=1
                    )

                    fig.update_xaxes(title_text="Time (ns)", row=1, col=1)
                    fig.update_yaxes(title_text="Voltage (mV)", row=1, col=1)
                    fig.update_xaxes(title_text="Time (ns)", row=2, col=1)
                    fig.update_yaxes(title_text="Current (μA)", row=2, col=1)

                    fig.update_layout(
                        title=f'AC Josephson Effect (f = {josephson_freq/1e9:.2f} GHz)',
                        height=600
                    )
                else:
                    fig = go.Figure()
                    fig.add_annotation(
                        text="Apply current > Ic to see AC Josephson effect",
                        x=0.5, y=0.5,
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=16, color='white')
                    )
                    fig.update_layout(height=400)

            elif junction_type == "SQUID":
                # SQUID (Superconducting Quantum Interference Device)
                flux_array = np.linspace(0, 2, 200)

                # SQUID critical current modulation
                ic_squid = critical_current * np.abs(np.cos(np.pi * flux_array))

                # Applied flux point
                ic_current = critical_current * np.abs(np.cos(np.pi * magnetic_flux))

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=flux_array, y=ic_squid,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        name='Critical Current Modulation',
                        hovertemplate='Φ/Φ₀: %{x:.3f}<br>Ic: %{y:.1f} μA<extra></extra>'
                    )
                )

                # Mark applied flux
                fig.add_trace(
                    go.Scatter(
                        x=[magnetic_flux], y=[ic_current],
                        mode='markers',
                        marker=dict(size=12, color='yellow', symbol='star'),
                        name='Operating Point',
                        hovertemplate=f'Φ/Φ₀: {magnetic_flux:.3f}<br>Ic: {ic_current:.1f} μA<extra></extra>'
                    )
                )

                # Add flux quantum markers
                for n in range(3):
                    fig.add_vline(
                        x=n,
                        line=dict(color='white', width=1, dash='dot'),
                        annotation_text=f"{n}Φ₀"
                    )

                fig.update_layout(
                    title='SQUID Critical Current vs Magnetic Flux',
                    xaxis_title='Magnetic Flux (Φ/Φ₀)',
                    yaxis_title='Critical Current (μA)',
                    height=500
                )

            else:  # RSJ Model
                # Resistively and Capacitively Shunted Junction model
                current_range = np.linspace(0, critical_current*2, 1000)

                # RSJ voltage calculation (simplified)
                voltage_rsj = np.zeros_like(current_range)
                for i, I in enumerate(current_range):
                    if I <= critical_current:
                        voltage_rsj[i] = 0
                    else:
                        # Approximate RSJ solution
                        voltage_rsj[i] = normal_resistance * np.sqrt((I/critical_current)**2 - 1) * critical_current

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=current_range, y=voltage_rsj*1000,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        name='RSJ Model',
                        hovertemplate='I: %{x:.1f} μA<br>V: %{y:.2f} mV<extra></extra>'
                    )
                )

                # Compare with ideal junction
                voltage_ideal = np.zeros_like(current_range)
                voltage_ideal[current_range > critical_current] = normal_resistance * (current_range[current_range > critical_current] - critical_current)

                fig.add_trace(
                    go.Scatter(
                        x=current_range, y=voltage_ideal*1000,
                        mode='lines',
                        line=dict(color='white', width=2, dash='dash'),
                        name='Ideal Junction',
                        hovertemplate='I: %{x:.1f} μA<br>V: %{y:.2f} mV<extra></extra>'
                    )
                )

                fig.update_layout(
                    title='RSJ Model vs Ideal Josephson Junction',
                    xaxis_title='Current (μA)',
                    yaxis_title='Voltage (mV)',
                    height=500
                )

            # Common layout updates
            fig.update_layout(
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)',
                font=dict(color='white'),
                showlegend=True,
                legend=dict(x=1.02, y=1)
            )

            return fig

        josephson_fig = create_josephson_visualization()
        st.plotly_chart(josephson_fig, use_container_width=True)

        # Josephson junction analysis
        st.markdown("#### 📊 Josephson Junction Analysis")

        # Calculate key parameters
        characteristic_voltage = critical_current * 1e-6 * normal_resistance * 1000  # mV
        josephson_penetration = np.sqrt(2.067e-15 / (2 * np.pi * 4e-7 * np.pi * critical_current * 1e-6))  # m

        # Energy scale comparison
        thermal_energy = 8.617e-5 * 4.2 * 1000  # meV at 4.2K
        josephson_energy_mev = josephson_energy * 6.242e18  # meV

        # Display Josephson metrics
        jos_col1, jos_col2, jos_col3, jos_col4 = st.columns(4)

        with jos_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{characteristic_voltage:.2f}</div>
                <div class="metric-label">IcRn (mV)</div>
            </div>
            """, unsafe_allow_html=True)

        with jos_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{josephson_energy_mev:.3f}</div>
                <div class="metric-label">EJ (meV)</div>
            </div>
            """, unsafe_allow_html=True)

        with jos_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{josephson_penetration*1e6:.1f}</div>
                <div class="metric-label">λJ (μm)</div>
            </div>
            """, unsafe_allow_html=True)

        with jos_col4:
            quality_factor = josephson_energy_mev / thermal_energy if thermal_energy > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{quality_factor:.1f}</div>
                <div class="metric-label">EJ/kBT</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[4]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">📊</span> Phase Transitions & Critical Phenomena
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore superconducting phase transitions, order parameter dynamics, and critical behavior.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>📊</span> Phase Transition Parameters")

        # Ginzburg-Landau parameters
        gl_parameter = st.slider("GL Parameter κ", 0.1, 10.0, 1.0, 0.1)
        reduced_temperature = st.slider("Reduced Temperature t = T/Tc", 0.0, 2.0, 0.8, 0.01)

        # External field
        reduced_field = st.slider("Reduced Field h = H/Hc", 0.0, 2.0, 0.5, 0.01)

        # Superconductor type classification
        if gl_parameter < 1/np.sqrt(2):
            sc_type = "Type I"
            type_color = "#10b981"
        else:
            sc_type = "Type II"
            type_color = "#ef4444"

        st.markdown(f"""
        <div style="background: {type_color}33; padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 2px solid {type_color};">
            <strong>Superconductor Type:</strong> {sc_type}<br>
            <strong>κ value:</strong> {gl_parameter:.2f}<br>
            <strong>Critical κ:</strong> {1/np.sqrt(2):.3f}
        </div>
        """, unsafe_allow_html=True)

        # Phase diagram options
        st.markdown("**Phase Diagram Options:**")
        show_phase_boundary = st.checkbox("Show Phase Boundary", value=True)
        show_order_parameter = st.checkbox("Show Order Parameter", value=True)
        show_free_energy = st.checkbox("Show Free Energy", value=False)

        # Fluctuation effects
        st.markdown("**Advanced Options:**")
        include_fluctuations = st.checkbox("Include Thermal Fluctuations", value=False)
        show_vortex_structure = st.checkbox("Show Vortex Structure (Type II)", value=False)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced phase transition visualization
        def create_phase_transition_visualization():
            if show_free_energy and show_order_parameter:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('H-T Phase Diagram', 'Order Parameter vs Temperature',
                                   'Free Energy Landscape', 'Specific Heat'),
                    vertical_spacing=0.15,
                    horizontal_spacing=0.1
                )
            elif show_order_parameter or show_free_energy:
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('H-T Phase Diagram', 
                                   'Order Parameter vs Temperature' if show_order_parameter else 'Free Energy Landscape'),
                    vertical_spacing=0.15
                )
            else:
                fig = go.Figure()

            # H-T Phase diagram
            T_range = np.linspace(0.01, 2.0, 200)

            # Type I superconductor phase boundary
            if gl_parameter < 1/np.sqrt(2):
                # Thermodynamic critical field
                Hc_T = np.sqrt(1 - T_range**2)
                Hc_T[T_range >= 1] = 0

                fig.add_trace(
                    go.Scatter(
                        x=T_range, y=Hc_T,
                        mode='lines',
                        line=dict(color='#10b981', width=4),
                        fill='tonexty',
                        fillcolor='rgba(16, 185, 129, 0.3)',
                        name='Superconducting Phase',
                        hovertemplate='T/Tc: %{x:.3f}<br>H/Hc: %{y:.3f}<extra></extra>'
                    ),
                    row=1, col=1
                )

                # Normal phase
                fig.add_trace(
                    go.Scatter(
                        x=T_range, y=np.ones_like(T_range)*2,
                        mode='lines',
                        line=dict(color='transparent'),
                        fill='tonexty',
                        fillcolor='rgba(239, 68, 68, 0.3)',
                        name='Normal Phase',
                        showlegend=False
                    ),
                    row=1, col=1
                )

            else:
                # Type II superconductor with Hc1 and Hc2
                Hc1_T = np.log(gl_parameter) * np.sqrt(1 - T_range**2) / gl_parameter
                Hc2_T = gl_parameter * np.sqrt(1 - T_range**2)

                Hc1_T[T_range >= 1] = 0
                Hc2_T[T_range >= 1] = 0

                # Meissner phase
                fig.add_trace(
                    go.Scatter(
                        x=T_range, y=Hc1_T,
                        mode='lines',
                        line=dict(color='#10b981', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(16, 185, 129, 0.3)',
                        name='Meissner Phase',
                        hovertemplate='T/Tc: %{x:.3f}<br>Hc1: %{y:.3f}<extra></extra>'
                    ),
                    row=1, col=1
                )

                # Mixed phase
                fig.add_trace(
                    go.Scatter(
                        x=T_range, y=Hc2_T,
                        mode='lines',
                        line=dict(color='#f59e0b', width=4),
                        fill='tonexty',
                        fillcolor='rgba(245, 158, 11, 0.3)',
                        name='Mixed (Vortex) Phase',
                        hovertemplate='T/Tc: %{x:.3f}<br>Hc2: %{y:.3f}<extra></extra>'
                    ),
                    row=1, col=1
                )

                # Normal phase
                fig.add_trace(
                    go.Scatter(
                        x=T_range, y=np.ones_like(T_range)*2,
                        mode='lines',
                        line=dict(color='transparent'),
                        fill='tonexty',
                        fillcolor='rgba(239, 68, 68, 0.3)',
                        name='Normal Phase',
                        showlegend=False
                    ),
                    row=1, col=1
                )

            # Mark current operating point
            fig.add_trace(
                go.Scatter(
                    x=[reduced_temperature], y=[reduced_field],
                    mode='markers',
                    marker=dict(size=15, color='white', symbol='star', line=dict(color='black', width=2)),
                    name='Operating Point',
                    hovertemplate=f'T/Tc: {reduced_temperature:.3f}<br>H/Hc: {reduced_field:.3f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Order parameter vs temperature
            if show_order_parameter:
                T_order = np.linspace(0.01, 1.5, 200)
                order_parameter = np.zeros_like(T_order)

                # BCS-like order parameter
                for i, T in enumerate(T_order):
                    if T < 1:
                        order_parameter[i] = np.sqrt(1 - T**2)
                        # Add fluctuation effects
                        if include_fluctuations:
                            fluctuation = 0.1 * np.random.normal() * np.exp(-(1-T)*5)
                            order_parameter[i] += fluctuation
                            order_parameter[i] = max(0, order_parameter[i])

                row_order = 1 if not show_free_energy else 1
                col_order = 2 if show_free_energy else 1

                fig.add_trace(
                    go.Scatter(
                        x=T_order, y=order_parameter,
                        mode='lines',
                        line=dict(color='#a855f7', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(168, 85, 247, 0.3)',
                        name='|ψ|²',
                        hovertemplate='T/Tc: %{x:.3f}<br>|ψ|²: %{y:.3f}<extra></extra>'
                    ),
                    row=row_order, col=col_order
                )

                # Mark critical temperature
                fig.add_vline(
                    x=1.0,
                    line=dict(color='red', width=2, dash='dash'),
                    annotation_text="Tc",
                    row=row_order, col=col_order
                )

                # Mark current temperature
                fig.add_vline(
                    x=reduced_temperature,
                    line=dict(color='yellow', width=2),
                    annotation_text="Current T",
                    row=row_order, col=col_order
                )

            # Free energy landscape
            if show_free_energy:
                psi_range = np.linspace(-1.5, 1.5, 200)

                # Ginzburg-Landau free energy
                a = reduced_temperature - 1  # Changes sign at Tc
                b = 1  # Fourth-order term coefficient

                free_energy = a * psi_range**2 / 2 + b * psi_range**4 / 4

                # Add external field term (simplified)
                free_energy += reduced_field * np.abs(psi_range)

                row_free = 2
                col_free = 1 if show_order_parameter else 1

                fig.add_trace(
                    go.Scatter(
                        x=psi_range, y=free_energy,
                        mode='lines',
                        line=dict(color='#ef4444', width=4),
                        name='Free Energy',
                        hovertemplate='ψ: %{x:.3f}<br>F: %{y:.3f}<extra></extra>'
                    ),
                    row=row_free, col=col_free
                )

                # Mark equilibrium points (minima)
                if a < 0:  # Below Tc
                    equilibrium_psi = np.sqrt(-a/b)
                    equilibrium_energy = a * equilibrium_psi**2 / 2 + b * equilibrium_psi**4 / 4

                    fig.add_trace(
                        go.Scatter(
                            x=[equilibrium_psi, -equilibrium_psi],
                            y=[equilibrium_energy, equilibrium_energy],
                            mode='markers',
                            marker=dict(size=10, color='yellow', symbol='circle'),
                            name='Equilibrium',
                            showlegend=False
                        ),
                        row=row_free, col=col_free
                    )

            # Specific heat (additional subplot if space available)
            if show_free_energy and show_order_parameter:
                T_heat = np.linspace(0.1, 2.0, 200)
                specific_heat = np.ones_like(T_heat)  # Normal state value

                # BCS jump at Tc
                jump_index = np.argmin(np.abs(T_heat - 1.0))
                specific_heat[jump_index:] *= 1.43  # BCS prediction

                # Exponential suppression below Tc
                below_tc = T_heat < 1.0
                specific_heat[below_tc] *= np.exp(-1.76/T_heat[below_tc])

                fig.add_trace(
                    go.Scatter(
                        x=T_heat, y=specific_heat,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        name='Specific Heat',
                        hovertemplate='T/Tc: %{x:.3f}<br>C: %{y:.3f}<extra></extra>'
                    ),
                    row=2, col=2
                )

                # Mark Tc
                fig.add_vline(
                    x=1.0,
                    line=dict(color='red', width=2, dash='dash'),
                    annotation_text="Tc",
                    row=2, col=2
                )

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>Superconducting Phase Transitions ({sc_type})</b><br>'
                         f'<span style="font-size:14px;">κ = {gl_parameter:.2f}, T/Tc = {reduced_temperature:.3f}</span>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                height=700 if (show_free_energy and show_order_parameter) else 600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            # Update axes
            fig.update_xaxes(title_text="T/Tc", row=1, col=1, color='white')
            fig.update_yaxes(title_text="H/Hc", row=1, col=1, color='white')

            if show_order_parameter:
                row_order = 1 if not show_free_energy else 1
                col_order = 2 if show_free_energy else 1
                fig.update_xaxes(title_text="T/Tc", row=row_order, col=col_order, color='white')
                fig.update_yaxes(title_text="Order Parameter |ψ|²", row=row_order, col=col_order, color='white')

            if show_free_energy:
                row_free = 2
                col_free = 1 if show_order_parameter else 1
                fig.update_xaxes(title_text="Order Parameter ψ", row=row_free, col=col_free, color='white')
                fig.update_yaxes(title_text="Free Energy F", row=row_free, col=col_free, color='white')

            if show_free_energy and show_order_parameter:
                fig.update_xaxes(title_text="T/Tc", row=2, col=2, color='white')
                fig.update_yaxes(title_text="Specific Heat C", row=2, col=2, color='white')

            return fig

        phase_fig = create_phase_transition_visualization()
        st.plotly_chart(phase_fig, use_container_width=True)

        # Phase transition analysis
        st.markdown("#### 📊 Phase Transition Analysis")

        # Calculate thermodynamic quantities
        if reduced_temperature < 1:
            order_param_value = np.sqrt(1 - reduced_temperature**2)
            condensation_energy = order_param_value**2 / 2
        else:
            order_param_value = 0
            condensation_energy = 0

        # Critical fields for Type II
        if gl_parameter >= 1/np.sqrt(2):
            hc1_value = np.log(gl_parameter) / gl_parameter
            hc2_value = gl_parameter
        else:
            hc1_value = 1.0
            hc2_value = 1.0

        # Display phase metrics
        phase_col1, phase_col2, phase_col3, phase_col4 = st.columns(4)

        with phase_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{order_param_value:.3f}</div>
                <div class="metric-label">Order Parameter</div>
            </div>
            """, unsafe_allow_html=True)

        with phase_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{condensation_energy:.3f}</div>
                <div class="metric-label">Condensation Energy</div>
            </div>
            """, unsafe_allow_html=True)

        with phase_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{hc1_value:.3f}</div>
                <div class="metric-label">Hc1/Hc</div>
            </div>
            """, unsafe_allow_html=True)

        with phase_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{hc2_value:.3f}</div>
                <div class="metric-label">Hc2/Hc</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[5]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            <span class="interactive-icon">🏭</span> Superconducting Applications & Technology
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore practical applications of superconductivity in medicine, energy, and quantum technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Application showcase with interactive cards
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin: 2rem 0;">
        <div class="supercond-card" onclick="window.applicationSelected = 'mri'">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">🏥</span> MRI Magnets
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>Field Strength:</strong> 1.5 - 7 Tesla</li>
                <li><strong>Homogeneity:</strong> < 1 ppm</li>
                <li><strong>Stability:</strong> < 0.1 ppm/hour</li>
                <li><strong>Quench Protection:</strong> Safety systems</li>
            </ul>
        </div>

        <div class="supercond-card" style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); border-color: #10b981;">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">⚡</span> Power Transmission
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>Zero Resistance:</strong> No I²R losses</li>
                <li><strong>High Current:</strong> kA capacity</li>
                <li><strong>Compact:</strong> Reduced cable size</li>
                <li><strong>Efficiency:</strong> 99.9% transmission</li>
            </ul>
        </div>

        <div class="supercond-card" style="background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%); border-color: #8b5cf6;">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">🖥️</span> Quantum Computing
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>Josephson Qubits:</strong> Coherent states</li>
                <li><strong>Low Temperature:</strong> mK operation</li>
                <li><strong>Fast Gates:</strong> ns timescales</li>
                <li><strong>Scalability:</strong> Many-qubit systems</li>
            </ul>
        </div>

        <div class="supercond-card" style="background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); border-color: #ef4444;">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">🚁</span> Magnetic Levitation
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>Maglev Trains:</strong> 500+ km/h speeds</li>
                <li><strong>Magnetic Bearings:</strong> Frictionless rotation</li>
                <li><strong>Flywheel Storage:</strong> Energy systems</li>
                <li><strong>Vibration Isolation:</strong> Precision instruments</li>
            </ul>
        </div>

        <div class="supercond-card" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); border-color: #fbbf24;">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">🔬</span> Scientific Instruments
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>NMR Spectroscopy:</strong> High-field magnets</li>
                <li><strong>Particle Accelerators:</strong> LHC dipoles</li>
                <li><strong>Fusion Reactors:</strong> Tokamak coils</li>
                <li><strong>SQUIDs:</strong> Ultra-sensitive magnetometry</li>
            </ul>
        </div>

        <div class="supercond-card" style="background: linear-gradient(135deg, #06b6d40%, #0891b2 100%); border-color: #0891b2;">
            <h4 style="color: white; margin-bottom: 1rem;">
                <span class="interactive-icon">💾</span> Digital Electronics
            </h4>
            <ul style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                <li><strong>SFQ Logic:</strong> Ultra-fast switching</li>
                <li><strong>Memory Devices:</strong> Non-volatile storage</li>
                <li><strong>Filters:</strong> RF/microwave applications</li>
                <li><strong>Detectors:</strong> Single-photon sensitivity</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed application analysis
    st.markdown("#### 🔍 Application Deep Dive")

    application_choice = st.selectbox("Select Application for Analysis", [
        "MRI Imaging System",
        "Superconducting Power Cable", 
        "Quantum Computer",
        "Maglev Transportation",
        "Fusion Reactor",
        "Particle Accelerator"
    ])

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(f"#### <span class='interactive-icon'>⚙️</span> {application_choice} Parameters")

        if application_choice == "MRI Imaging System":
            field_strength = st.slider("Magnetic Field (Tesla)", 0.5, 9.0, 3.0, 0.1)
            bore_diameter = st.slider("Bore Diameter (cm)", 40, 80, 60, 5)
            current_density = st.slider("Current Density (A/mm²)", 100, 1000, 400, 50)

            # Calculate MRI parameters
            stored_energy = 0.5 * field_strength**2 * np.pi * (bore_diameter/100)**2 * 1.5 / (4*np.pi*1e-7)  # Simplified
            wire_length = field_strength * bore_diameter * 100  # Simplified

            st.markdown(f"""
            <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>MRI System:</strong><br>
                Stored Energy: {stored_energy/1e6:.1f} MJ<br>
                Wire Length: {wire_length/1000:.1f} km<br>
                Resolution: {1000/field_strength:.1f} μm
            </div>
            """, unsafe_allow_html=True)

        elif application_choice == "Superconducting Power Cable":
            voltage_level = st.slider("Voltage Level (kV)", 10, 500, 138, 10)
            current_capacity = st.slider("Current Capacity (kA)", 1, 10, 3, 1)
            cable_length = st.slider("Cable Length (km)", 1, 100, 10, 1)

            # Calculate power parameters
            power_capacity = voltage_level * current_capacity * 1000  # kW
            conventional_losses = power_capacity * 0.05 * cable_length / 100  # 5% loss per 100km

            st.markdown(f"""
            <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Power Cable:</strong><br>
                Power Capacity: {power_capacity/1000:.1f} MW<br>
                Avoided Losses: {conventional_losses/1000:.1f} MW<br>
                Efficiency Gain: {conventional_losses/power_capacity*100:.1f}%
            </div>
            """, unsafe_allow_html=True)

        elif application_choice == "Quantum Computer":
            num_qubits = st.slider("Number of Qubits", 1, 1000, 50, 1)
            coherence_time = st.slider("Coherence Time (μs)", 1, 1000, 100, 10)
            gate_time = st.slider("Gate Time (ns)", 1, 1000, 50, 10)

            # Calculate quantum metrics
            gate_fidelity = np.exp(-gate_time*1e-9 / (coherence_time*1e-6))
            max_gates = coherence_time*1000 / gate_time

            st.markdown(f"""
            <div style="background: rgba(2, 132, 199, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Quantum System:</strong><br>
                Gate Fidelity: {gate_fidelity:.4f}<br>
                Max Gates: {max_gates:.0f}<br>
                Quantum Volume: {2**min(num_qubits, 20):.0e}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Application-specific visualization
        def create_application_visualization():
            if application_choice == "MRI Imaging System":
                # MRI field profile
                r = np.linspace(0, bore_diameter/2, 100)
                B_r = field_strength * (1 - (r/(bore_diameter/2))**2 * 0.1)  # Simplified profile

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=r, y=B_r,
                        mode='lines',
                        line=dict(color='#0ea5e9', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(14, 165, 233, 0.3)',
                        name='Magnetic Field',
                        hovertemplate='Radius: %{x:.1f} cm<br>B-field: %{y:.3f} T<extra></extra>'
                    )
                )

                fig.update_layout(
                    title=f'MRI Magnetic Field Profile ({field_strength:.1f}T)',
                    xaxis_title='Radius (cm)',
                    yaxis_title='Magnetic Field (T)',
                    height=400
                )

            elif application_choice == "Superconducting Power Cable":
                # Power flow analysis
                time_hours = np.linspace(0, 24, 100)
                load_profile = 0.8 + 0.2 * np.sin(2*np.pi*time_hours/24)  # Daily load variation
                power_flow = power_capacity * load_profile / 1000  # MW

                # Compare with conventional cable
                conventional_losses = power_flow * 0.05 * cable_length / 100

                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Power Flow', 'Energy Savings'),
                    vertical_spacing=0.15
                )

                fig.add_trace(
                    go.Scatter(
                        x=time_hours, y=power_flow,
                        mode='lines',
                        line=dict(color='#10b981', width=4),
                        name='Power Flow (MW)',
                        hovertemplate='Time: %{x:.1f} h<br>Power: %{y:.1f} MW<extra></extra>'
                    ),
                    row=1, col=1
                )

                fig.add_trace(
                    go.Scatter(
                        x=time_hours, y=conventional_losses,
                        mode='lines',
                        line=dict(color='#ef4444', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(239, 68, 68, 0.3)',
                        name='Losses Avoided (MW)',
                        hovertemplate='Time: %{x:.1f} h<br>Savings: %{y:.2f} MW<extra></extra>'
                    ),
                    row=2, col=1
                )

                fig.update_layout(title=f'Superconducting Cable Performance ({current_capacity:.1f} kA)', height=600)

            elif application_choice == "Quantum Computer":
                # Quantum fidelity over time
                time_us = np.linspace(0, coherence_time*2, 1000)
                fidelity = np.exp(-time_us / coherence_time)

                # Gate sequence visualization
                gate_times = np.arange(0, coherence_time, gate_time/1000)
                gate_fidelities = np.exp(-gate_times / coherence_time)

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=time_us, y=fidelity,
                        mode='lines',
                        line=dict(color='#a855f7', width=4),
                        name='Coherence Decay',
                        hovertemplate='Time: %{x:.1f} μs<br>Fidelity: %{y:.4f}<extra></extra>'
                    )
                )

                if len(gate_times) < 100:  # Only show if reasonable number
                    fig.add_trace(
                        go.Scatter(
                            x=gate_times, y=gate_fidelities,
                            mode='markers',
                            marker=dict(color='yellow', size=6),
                            name='Gate Operations',
                            hovertemplate='Gate %{pointNumber}<br>Time: %{x:.1f} μs<br>Fidelity: %{y:.4f}<extra></extra>'
                        )
                    )

                fig.update_layout(
                    title=f'Quantum Coherence ({num_qubits} Qubits)',
                    xaxis_title='Time (μs)',
                    yaxis_title='Fidelity',
                    height=400
                )

            else:
                # Generic performance chart
                fig = go.Figure()
                fig.add_annotation(
                    text=f"Performance analysis for {application_choice}",
                    x=0.5, y=0.5,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=16, color='white')
                )
                fig.update_layout(height=400)

            # Common layout updates
            fig.update_layout(
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)',
                font=dict(color='white'),
                showlegend=True
            )

            return fig

        app_fig = create_application_visualization()
        st.plotly_chart(app_fig, use_container_width=True)

        # Application metrics
        st.markdown("#### 📊 Performance Metrics")

        if application_choice == "MRI Imaging System":
            app_col1, app_col2, app_col3, app_col4 = st.columns(4)

            with app_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{field_strength:.1f}</div>
                    <div class="metric-label">Field (Tesla)</div>
                </div>
                """, unsafe_allow_html=True)

            with app_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{stored_energy/1e6:.1f}</div>
                    <div class="metric-label">Energy (MJ)</div>
                </div>
                """, unsafe_allow_html=True)

            with app_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{1000/field_strength:.0f}</div>
                    <div class="metric-label">Resolution (μm)</div>
                </div>
                """, unsafe_allow_html=True)

            with app_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{wire_length/1000:.1f}</div>
                    <div class="metric-label">Wire Length (km)</div>
                </div>
                """, unsafe_allow_html=True)

with tabs[6]:
    st.info("Additional superconductivity learning resources will be available here.")

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
           border-radius: 15px; text-align: center; border: 1px solid #64748b;">
    <h3 style="color: white; margin-bottom: 1rem;">🔌 Superconductivity Laboratory</h3>
    <p style="color: #e2e8f0; margin-bottom: 1.5rem;">
        Explore the quantum phenomena of zero resistance and perfect diamagnetism.
    </p>
</div>
""", unsafe_allow_html=True)