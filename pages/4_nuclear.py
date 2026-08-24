import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import pandas as pd

st.set_page_config(page_title="Nuclear Physics Laboratory",
                   page_icon="☢️",
                   layout="wide")

# Enhanced CSS with nuclear-inspired design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0c1821 0%, #1a2332 50%, #2d3748 100%);
        min-height: 100vh;
        color: white;
    }

    /* Nuclear-themed header with radioactive animations */
    .nuclear-header {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 50%, #f97316 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #ef4444;
        box-shadow: 0 20px 40px rgba(239, 68, 68, 0.3);
    }

    .nuclear-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15) 3px, transparent 3px),
            radial-gradient(circle at 70% 60%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 50% 80%, rgba(255,255,255,0.08) 1px, transparent 1px),
            linear-gradient(45deg, rgba(255,255,255,0.05) 25%, transparent 25%);
        background-size: 80px 80px, 60px 60px, 40px 40px, 20px 20px;
        animation: nuclearDecay 15s linear infinite;
    }

    /* Enhanced section cards with radioactive glow */
    .physics-section {
        background: rgba(45, 55, 72, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .physics-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(239, 68, 68, 0.3);
        border-color: rgba(239, 68, 68, 0.5);
    }

    .physics-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #ef4444, #dc2626, #b91c1c, #991b1b);
        animation: radioactiveGradient 3s ease-in-out infinite;
    }

    /* Interactive parameter panels */
    .param-panel {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #718096;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .param-panel:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(113, 128, 150, 0.3);
        border-color: #ef4444;
    }

    .param-panel h4 {
        color: #f56565;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Enhanced metric cards with nuclear effects */
    .metric-card {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #718096;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-8px) rotateX(5deg);
        box-shadow: 0 20px 40px rgba(239, 68, 68, 0.2);
        border-color: #ef4444;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f56565;
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

    /* Enhanced tabs with nuclear styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 15px;
        padding: 0.8rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #a0aec0;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0 0.3rem;
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(239, 68, 68, 0.2);
        color: #fc8181;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
        transform: translateY(-3px);
    }

    /* Nuclear visualization cards */
    .nuclear-card {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #f87171;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .nuclear-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(239, 68, 68, 0.4);
        border-color: #fca5a5;
    }

    .nuclear-card::before {
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

    .nuclear-card:hover::before {
        width: 300px;
        height: 300px;
    }

    .nuclear-card h5 {
        color: white;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.2rem;
        position: relative;
        z-index: 2;
    }

    /* Advanced animations */
    @keyframes nuclearDecay {
        0% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(-5px, -5px) scale(1.02); }
        50% { transform: translate(5px, -5px) scale(0.98); }
        75% { transform: translate(-5px, 5px) scale(1.01); }
        100% { transform: translate(0, 0) scale(1); }
    }

    @keyframes radioactiveGradient {
        0%, 100% { background: linear-gradient(90deg, #ef4444, #dc2626, #b91c1c, #991b1b); }
        25% { background: linear-gradient(90deg, #dc2626, #b91c1c, #991b1b, #ef4444); }
        50% { background: linear-gradient(90deg, #b91c1c, #991b1b, #ef4444, #dc2626); }
        75% { background: linear-gradient(90deg, #991b1b, #ef4444, #dc2626, #b91c1c); }
    }

    @keyframes nuclearPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }

    @keyframes fissionFragment {
        0% { transform: translateX(0) scale(1); opacity: 1; }
        50% { transform: translateX(30px) scale(0.7); opacity: 0.6; }
        100% { transform: translateX(60px) scale(0.5); opacity: 0.3; }
    }

    @keyframes fusionCore {
        0% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.2) rotate(180deg); }
        100% { transform: scale(1.5) rotate(360deg); }
    }

    /* Interactive elements */
    .interactive-icon {
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .interactive-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(239, 68, 68, 0.3));
    }

    /* Radiation warning indicators */
    .radiation-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin: 0 5px;
        animation: radioactivePulse 1.5s ease-in-out infinite;
    }

    @keyframes radioactivePulse {
        0%, 100% { transform: scale(1); opacity: 1; background: #ef4444; }
        50% { transform: scale(1.3); opacity: 0.6; background: #fca5a5; }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .nuclear-header {
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
""",
            unsafe_allow_html=True)

# Enhanced nuclear-themed header
st.markdown("""
<div class="nuclear-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span class="interactive-icon">☢️</span> Nuclear Physics Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Explore the Heart of the Atom
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Radioactive Decay</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Nuclear Fission</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Nuclear Fusion</span>
    </div>
</div>
""",
            unsafe_allow_html=True)

# Enhanced tabs with comprehensive nuclear phenomena
tabs = st.tabs([
    "📉 Radioactive Decay", "💥 Nuclear Fission", "⭐ Nuclear Fusion",
    "🗺️ Nuclear Chart", "⚡ Nuclear Reactions", "🔬 Detection & Dosimetry",
    "🎓 Learning Hub"
])

# Tab 1: Enhanced Radioactive Decay
with tabs[0]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">📉</span> Radioactive Decay & Half-Life
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore exponential decay laws, decay chains, and radioisotope properties through interactive simulations.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>⚙️</span> Decay Parameters")

        # Enhanced isotope selection with real data
        isotopes = {
            "Carbon-14": {
                "half_life": 5730,
                "unit": "years",
                "decay_type": "β⁻",
                "activity": 62.4
            },
            "Uranium-238": {
                "half_life": 4.468e9,
                "unit": "years",
                "decay_type": "α",
                "activity": 12.4
            },
            "Cesium-137": {
                "half_life": 30.17,
                "unit": "years",
                "decay_type": "β⁻",
                "activity": 3.2e12
            },
            "Iodine-131": {
                "half_life": 8.02,
                "unit": "days",
                "decay_type": "β⁻",
                "activity": 4.6e15
            },
            "Radon-222": {
                "half_life": 3.82,
                "unit": "days",
                "decay_type": "α",
                "activity": 5.7e15
            },
            "Technetium-99m": {
                "half_life": 6.01,
                "unit": "hours",
                "decay_type": "γ",
                "activity": 1.9e16
            },
            "Tritium": {
                "half_life": 12.32,
                "unit": "years",
                "decay_type": "β⁻",
                "activity": 3.6e14
            },
            "Plutonium-239": {
                "half_life": 24100,
                "unit": "years",
                "decay_type": "α",
                "activity": 2.3e9
            }
        }

        selected_isotope = st.selectbox("Select Radioisotope",
                                        list(isotopes.keys()))
        isotope_data = isotopes[selected_isotope]

        # Display isotope properties
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Isotope Properties:</strong><br>
            Half-life: {isotope_data['half_life']:g} {isotope_data['unit']}<br>
            Decay mode: {isotope_data['decay_type']}<br>
            Specific activity: {isotope_data['activity']:.1e} Bq/g
        </div>
        """,
                    unsafe_allow_html=True)

        # Decay calculation parameters
        st.markdown("**Calculation Parameters:**")
        initial_amount = st.slider("Initial Amount (g)", 0.1, 100.0, 10.0, 0.1)
        time_span = st.slider("Time Span (half-lives)", 0.1, 10.0, 5.0, 0.1)

        # Convert time to appropriate units
        if isotope_data['unit'] == 'years':
            max_time = time_span * isotope_data['half_life']
            time_unit = 'years'
        elif isotope_data['unit'] == 'days':
            max_time = time_span * isotope_data['half_life']
            time_unit = 'days'
        else:  # hours
            max_time = time_span * isotope_data['half_life']
            time_unit = 'hours'

        # Advanced decay options
        st.markdown("**Advanced Options:**")
        show_activity = st.checkbox("Show Activity Curve", value=True)
        show_decay_products = st.checkbox("Show Decay Products", value=False)
        show_statistics = st.checkbox("Show Statistical Fluctuations",
                                      value=False)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced radioactive decay visualization
        def create_decay_visualization():
            # Time array
            t = np.linspace(0, max_time, 1000)

            # Decay constant
            lambda_decay = np.log(2) / isotope_data['half_life']

            # Calculate remaining nuclei
            N_t = initial_amount * np.exp(-lambda_decay * t)

            # Calculate activity (A = λN)
            avogadro = 6.022e23
            # Assume atomic mass approximately equal to mass number
            atomic_mass = float(selected_isotope.split('-')
                                [1]) if '-' in selected_isotope else 14
            N_nuclei = initial_amount * avogadro / atomic_mass
            activity = lambda_decay * N_nuclei * np.exp(-lambda_decay * t)

            # Create subplots
            if show_activity:
                fig = make_subplots(rows=2,
                                    cols=1,
                                    subplot_titles=('Radioactive Decay Curve',
                                                    'Activity vs Time'),
                                    vertical_spacing=0.15)
                row2_exists = True
            else:
                fig = go.Figure()
                row2_exists = False

            # Add decay curve
            if show_statistics:
                # Add statistical fluctuations
                noise = np.random.normal(0, np.sqrt(N_t * 0.01), len(t))
                N_t_fluctuating = N_t + noise
                N_t_fluctuating = np.maximum(N_t_fluctuating,
                                             0)  # Ensure non-negative

                fig.add_trace(go.Scatter(
                    x=t,
                    y=N_t_fluctuating,
                    mode='lines',
                    line=dict(color='#fca5a5', width=2),
                    name='With Fluctuations',
                    hovertemplate=
                    f'Time: %{{x:.2f}} {time_unit}<br>Amount: %{{y:.3f}} g<extra></extra>'
                ),
                              row=1,
                              col=1)

            # Theoretical decay curve
            fig.add_trace(go.Scatter(
                x=t,
                y=N_t,
                mode='lines',
                line=dict(color='#ef4444', width=4),
                name=f'{selected_isotope} Decay',
                fill='tozeroy' if not show_statistics else None,
                fillcolor='rgba(239, 68, 68, 0.3)',
                hovertemplate=
                f'Time: %{{x:.2f}} {time_unit}<br>Amount: %{{y:.3f}} g<extra></extra>'
            ),
                          row=1,
                          col=1)

            # Add half-life markers
            for i in range(1, int(time_span) + 1):
                half_life_time = i * isotope_data['half_life']
                remaining = initial_amount / (2**i)

                fig.add_vline(
                    x=half_life_time,
                    line=dict(color='white', width=2, dash='dash'),
                    annotation_text=f"{i} half-life{'s' if i > 1 else ''}",
                    row=1,
                    col=1)

                fig.add_trace(go.Scatter(
                    x=[half_life_time],
                    y=[remaining],
                    mode='markers',
                    marker=dict(size=12, color='yellow', symbol='star'),
                    name=f't_{i/2}' if i == 1 else None,
                    showlegend=(i == 1),
                    hovertemplate=
                    f'Half-life {i}<br>Time: {half_life_time:.2f} {time_unit}<br>Remaining: {remaining:.3f} g<extra></extra>'
                ),
                              row=1,
                              col=1)

            # Add activity curve if requested
            if show_activity:
                # Convert activity to appropriate units
                if activity[0] > 1e12:
                    activity_display = activity / 1e12
                    activity_unit = 'TBq'
                elif activity[0] > 1e9:
                    activity_display = activity / 1e9
                    activity_unit = 'GBq'
                elif activity[0] > 1e6:
                    activity_display = activity / 1e6
                    activity_unit = 'MBq'
                else:
                    activity_display = activity
                    activity_unit = 'Bq'

                fig.add_trace(go.Scatter(
                    x=t,
                    y=activity_display,
                    mode='lines',
                    line=dict(color='#f97316', width=4),
                    name=f'Activity ({activity_unit})',
                    fill='tozeroy',
                    fillcolor='rgba(249, 115, 22, 0.3)',
                    hovertemplate=
                    f'Time: %{{x:.2f}} {time_unit}<br>Activity: %{{y:.2e}} {activity_unit}<extra></extra>'
                ),
                              row=2,
                              col=1)

            # Add decay products if requested
            if show_decay_products:
                decay_products = initial_amount - N_t
                fig.add_trace(go.Scatter(
                    x=t,
                    y=decay_products,
                    mode='lines',
                    line=dict(color='#10b981', width=3),
                    name='Decay Products',
                    hovertemplate=
                    f'Time: %{{x:.2f}} {time_unit}<br>Products: %{{y:.3f}} g<extra></extra>'
                ),
                              row=1,
                              col=1)

            # Update layout
            title_text = f'<b>{selected_isotope} Radioactive Decay</b><br>'
            title_text += f'<span style="font-size:14px;">t₁/₂ = {isotope_data["half_life"]:g} {isotope_data["unit"]}, '
            title_text += f'Initial: {initial_amount:.1f} g</span>'

            fig.update_layout(title=dict(text=title_text,
                                         x=0.5,
                                         font=dict(size=18, color='white')),
                              height=600 if row2_exists else 500,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            # Update axes
            fig.update_xaxes(title_text=f"Time ({time_unit})",
                             row=1,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="Amount (g)",
                             row=1,
                             col=1,
                             color='white')

            if row2_exists:
                fig.update_xaxes(title_text=f"Time ({time_unit})",
                                 row=2,
                                 col=1,
                                 color='white')
                fig.update_yaxes(title_text=f"Activity ({activity_unit})",
                                 row=2,
                                 col=1,
                                 color='white')

            return fig

        decay_fig = create_decay_visualization()
        st.plotly_chart(decay_fig, use_container_width=True)

        # Radioactive decay dashboard
        st.markdown("#### 📊 Decay Analysis Dashboard")

        # Calculate key metrics
        lambda_decay = np.log(2) / isotope_data['half_life']

        # Amount remaining after specified time
        final_time = time_span * isotope_data['half_life']
        final_amount = initial_amount * np.exp(-lambda_decay * final_time)

        # Decay rate at t=0
        avogadro = 6.022e23
        atomic_mass = float(
            selected_isotope.split('-')[1]) if '-' in selected_isotope else 14
        initial_nuclei = initial_amount * avogadro / atomic_mass
        initial_activity = lambda_decay * initial_nuclei

        # Mean lifetime
        mean_lifetime = 1 / lambda_decay

        # Display nuclear metrics
        nuclear_col1, nuclear_col2, nuclear_col3, nuclear_col4 = st.columns(4)

        with nuclear_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{final_amount:.3f}</div>
                <div class="metric-label">Final Amount (g)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with nuclear_col2:
            if initial_activity > 1e12:
                activity_display = initial_activity / 1e12
                unit = "TBq"
            elif initial_activity > 1e9:
                activity_display = initial_activity / 1e9
                unit = "GBq"
            else:
                activity_display = initial_activity / 1e6
                unit = "MBq"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{activity_display:.1f}</div>
                <div class="metric-label">Initial Activity ({unit})</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with nuclear_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{lambda_decay:.2e}</div>
                <div class="metric-label">Decay Constant (s⁻¹)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with nuclear_col4:
            if isotope_data['unit'] == 'years':
                mean_display = mean_lifetime
                mean_unit = 'years'
            elif isotope_data['unit'] == 'days':
                mean_display = mean_lifetime
                mean_unit = 'days'
            else:
                mean_display = mean_lifetime
                mean_unit = 'hours'

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{mean_display:.2f}</div>
                <div class="metric-label">Mean Lifetime ({mean_unit})</div>
            </div>
            """,
                        unsafe_allow_html=True)

# Tab 2: Enhanced Nuclear Fission
with tabs[1]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">💥</span> Nuclear Fission & Chain Reactions
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore nuclear fission processes, chain reactions, and reactor physics through animated simulations.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>💥</span> Fission Parameters")

        # Fissile material selection
        fissile_materials = {
            "Uranium-235": {
                "cross_section": 584,  # barns for thermal neutrons
                "avg_neutrons": 2.4,
                "q_value": 200,  # MeV
                "critical_mass": 52,  # kg
                "fission_fragments": ["Ba-144", "Kr-90"]
            },
            "Uranium-233": {
                "cross_section": 531,
                "avg_neutrons": 2.5,
                "q_value": 197,
                "critical_mass": 16,
                "fission_fragments": ["Ba-143", "Kr-91"]
            },
            "Plutonium-239": {
                "cross_section": 747,
                "avg_neutrons": 2.9,
                "q_value": 207,
                "critical_mass": 10,
                "fission_fragments": ["Ba-145", "Kr-94"]
            }
        }

        fissile_material = st.selectbox("Fissile Material",
                                        list(fissile_materials.keys()))
        material_props = fissile_materials[fissile_material]

        # Display material properties
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Fissile Properties:</strong><br>
            Cross-section: {material_props['cross_section']} barns<br>
            Avg. neutrons: {material_props['avg_neutrons']}<br>
            Q-value: {material_props['q_value']} MeV<br>
            Critical mass: {material_props['critical_mass']} kg
        </div>
        """,
                    unsafe_allow_html=True)

        # Chain reaction parameters
        st.markdown("**Chain Reaction Parameters:**")
        k_effective = st.slider("k-effective (multiplication factor)", 0.5,
                                2.0, 1.0, 0.01)
        initial_neutrons = st.slider("Initial Neutron Population", 1, 1000,
                                     100, 1)
        generations = st.slider("Number of Generations", 1, 20, 10, 1)

        # Reactor control
        st.markdown("**Reactor Control:**")
        control_rod_insertion = st.slider("Control Rod Insertion (%)", 0, 100,
                                          0, 1)
        moderator_ratio = st.slider("Moderator-to-Fuel Ratio", 1, 50, 20, 1)

        # Criticality analysis
        if k_effective > 1:
            reactor_state = "Supercritical"
            state_color = "#ef4444"
        elif k_effective == 1:
            reactor_state = "Critical"
            state_color = "#f59e0b"
        else:
            reactor_state = "Subcritical"
            state_color = "#10b981"

        st.markdown(f"""
        <div style="background: {state_color}33; padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 2px solid {state_color};">
            <strong>Reactor State:</strong> {reactor_state}<br>
            <strong>k-effective:</strong> {k_effective:.3f}
        </div>
        """,
                    unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced fission chain reaction visualization
        def create_fission_animation():
            # Calculate neutron population over generations
            generations_array = np.arange(0, generations + 1)

            # Account for control rod absorption
            k_controlled = k_effective * (1 - control_rod_insertion / 100)

            neutron_population = initial_neutrons * (k_controlled**
                                                     generations_array)

            # Create animated chain reaction
            fig = make_subplots(rows=2,
                                cols=1,
                                subplot_titles=('Chain Reaction Evolution',
                                                'Neutron Population Growth'),
                                vertical_spacing=0.15,
                                row_heights=[0.6, 0.4])

            # Chain reaction visualization (simplified network)
            if generations <= 5:  # Only show detailed network for small generations
                # Create network nodes
                for gen in range(min(generations + 1, 6)):
                    n_neutrons = min(
                        int(initial_neutrons * (k_controlled**gen)),
                        100)  # Limit display

                    # Position neutrons in generation
                    if n_neutrons > 0:
                        positions = np.linspace(
                            -gen, gen, n_neutrons) if n_neutrons > 1 else [0]
                        y_pos = -gen * 2

                        for i, x_pos in enumerate(positions):
                            # Add some randomness
                            x_jitter = np.random.normal(0, 0.1)
                            y_jitter = np.random.normal(0, 0.1)

                            fig.add_trace(go.Scatter(
                                x=[x_pos + x_jitter],
                                y=[y_pos + y_jitter],
                                mode='markers',
                                marker=dict(
                                    size=8,
                                    color='red' if gen == 0 else 'orange',
                                    symbol='circle'),
                                name=f'Gen {gen}' if i == 0 else None,
                                showlegend=(i == 0),
                                hovertemplate=
                                f'Generation: {gen}<br>Neutron: {i+1}<extra></extra>'
                            ),
                                          row=1,
                                          col=1)

                            # Connect to next generation
                            if gen < min(generations, 5):
                                next_n = min(int(k_controlled),
                                             5)  # Limit connections
                                for j in range(next_n):
                                    next_x = np.random.normal(x_pos, 0.5)
                                    next_y = -(gen + 1) * 2

                                    fig.add_trace(go.Scatter(
                                        x=[x_pos, next_x],
                                        y=[y_pos, next_y],
                                        mode='lines',
                                        line=dict(
                                            color='rgba(255, 255, 255, 0.3)',
                                            width=1),
                                        showlegend=False,
                                        hoverinfo='skip'),
                                                  row=1,
                                                  col=1)
            else:
                # For many generations, show simplified representation
                st.info(
                    "Showing population graph for large number of generations")

            # Population growth curve
            fig.add_trace(go.Scatter(
                x=generations_array,
                y=neutron_population,
                mode='lines+markers',
                line=dict(color='#ef4444', width=4),
                marker=dict(size=8, color='red'),
                name='Neutron Population',
                hovertemplate=
                'Generation: %{x}<br>Population: %{y:.0f}<extra></extra>'),
                          row=2,
                          col=1)

            # Add exponential fit line
            if k_controlled != 1:
                exponential_fit = initial_neutrons * np.exp(
                    generations_array * np.log(k_controlled))
                fig.add_trace(go.Scatter(
                    x=generations_array,
                    y=exponential_fit,
                    mode='lines',
                    line=dict(color='yellow', width=2, dash='dash'),
                    name='Exponential Fit',
                    hovertemplate=
                    'Generation: %{x}<br>Exponential: %{y:.0f}<extra></extra>'
                ),
                              row=2,
                              col=1)

            # Add criticality line
            critical_line = initial_neutrons * np.ones_like(generations_array)
            fig.add_trace(go.Scatter(
                x=generations_array,
                y=critical_line,
                mode='lines',
                line=dict(color='white', width=2, dash='dot'),
                name='Critical Level',
                hovertemplate='Critical Level<extra></extra>'),
                          row=2,
                          col=1)

            # Update layout
            fig.update_layout(title=dict(
                text=f'<b>{fissile_material} Chain Reaction</b><br>'
                f'<span style="font-size:14px;">k-eff = {k_controlled:.3f}, State: {reactor_state}</span>',
                x=0.5,
                font=dict(size=18, color='white')),
                              height=700,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            # Update axes
            fig.update_xaxes(title_text="Position",
                             row=1,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="Generation Level",
                             row=1,
                             col=1,
                             color='white')
            fig.update_xaxes(title_text="Generation",
                             row=2,
                             col=1,
                             color='white')
            fig.update_yaxes(
                title_text="Neutron Population",
                row=2,
                col=1,
                color='white',
                type='log' if max(neutron_population) > 1000 else 'linear')

            return fig

        fission_fig = create_fission_animation()
        st.plotly_chart(fission_fig, use_container_width=True)

        # Nuclear fission dashboard
        st.markdown("#### 📊 Fission Reactor Analysis")

        # Calculate reactor parameters
        final_population = initial_neutrons * (k_effective**generations)
        power_output = final_population * material_props[
            'q_value'] * 1.602e-19  # Watts (simplified)

        # Calculate doubling time
        if k_effective > 1:
            doubling_time = np.log(2) / np.log(k_effective)
        else:
            doubling_time = float('inf')

        # Reactor period
        if k_effective != 1:
            reactor_period = 1 / (k_effective - 1)
        else:
            reactor_period = float('inf')

        # Display fission metrics
        fission_col1, fission_col2, fission_col3, fission_col4 = st.columns(4)

        with fission_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{final_population:.0f}</div>
                <div class="metric-label">Final Neutrons</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fission_col2:
            if power_output > 1e9:
                power_display = power_output / 1e9
                power_unit = "GW"
            elif power_output > 1e6:
                power_display = power_output / 1e6
                power_unit = "MW"
            else:
                power_display = power_output / 1e3
                power_unit = "kW"

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{power_display:.2f}</div>
                <div class="metric-label">Power ({power_unit})</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fission_col3:
            doubling_display = doubling_time if doubling_time != float(
                'inf') else "∞"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{doubling_display}</div>
                <div class="metric-label">Doubling Time (gen)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fission_col4:
            period_display = f"{reactor_period:.2f}" if reactor_period != float(
                'inf') else "∞"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{period_display}</div>
                <div class="metric-label">Reactor Period</div>
            </div>
            """,
                        unsafe_allow_html=True)

# Tab 3: Enhanced Nuclear Fusion
with tabs[2]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">⭐</span> Nuclear Fusion & Stellar Nucleosynthesis
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore fusion reactions, stellar burning, and the processes that power stars and create elements.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>⭐</span> Fusion Parameters")

        # Fusion reaction selection
        fusion_reactions = {
            "D + T → α + n": {
                "reactants": ["²H", "³H"],
                "products": ["⁴He", "n"],
                "q_value": 17.6,  # MeV
                "threshold": 0.01,  # MeV
                "cross_section": 5000  # mb at 14 MeV
            },
            "D + D → ³He + n": {
                "reactants": ["²H", "²H"],
                "products": ["³He", "n"],
                "q_value": 3.27,
                "threshold": 0.1,
                "cross_section": 100
            },
            "D + D → T + p": {
                "reactants": ["²H", "²H"],
                "products": ["³H", "p"],
                "q_value": 4.03,
                "threshold": 0.1,
                "cross_section": 100
            },
            "³He + ³He → ⁴He + 2p": {
                "reactants": ["³He", "³He"],
                "products": ["⁴He", "2p"],
                "q_value": 12.86,
                "threshold": 1.0,
                "cross_section": 50
            },
            "p + ¹¹B → 3α": {
                "reactants": ["p", "¹¹B"],
                "products": ["3α"],
                "q_value": 8.7,
                "threshold": 0.7,
                "cross_section": 200
            }
        }

        selected_reaction = st.selectbox("Fusion Reaction",
                                         list(fusion_reactions.keys()))
        reaction_data = fusion_reactions[selected_reaction]

        # Display reaction properties
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Reaction:</strong> {selected_reaction}<br>
            <strong>Q-value:</strong> {reaction_data['q_value']:.2f} MeV<br>
            <strong>Threshold:</strong> {reaction_data['threshold']:.2f} MeV<br>
            <strong>Cross-section:</strong> {reaction_data['cross_section']} mb
        </div>
        """,
                    unsafe_allow_html=True)

        # Plasma parameters
        st.markdown("**Plasma Conditions:**")
        temperature = st.slider("Temperature (keV)", 1.0, 100.0, 14.0, 1.0)
        density = st.slider("Particle Density (10²⁰ m⁻³)", 0.1, 10.0, 1.0, 0.1)
        confinement_time = st.slider("Confinement Time (s)", 0.001, 10.0, 1.0,
                                     0.001)

        # Fusion environment
        environment = st.selectbox(
            "Environment",
            ["Laboratory Plasma", "Stellar Core", "Inertial Confinement"])

        # Calculate fusion metrics
        # Lawson criterion
        lawson_product = density * 1e20 * confinement_time
        lawson_criterion = 1.5e20  # m⁻³·s for D-T fusion

        # Fusion rate (simplified)
        # σv approximation for D-T fusion
        if temperature > 0:
            sigma_v = reaction_data['cross_section'] * 1e-31 * np.exp(
                -reaction_data['threshold'] / temperature)
        else:
            sigma_v = 0

        fusion_rate = 0.25 * (density * 1e20)**2 * sigma_v  # reactions/m³/s

        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Fusion Metrics:</strong><br>
            Lawson Product: {lawson_product:.2e} m⁻³·s<br>
            Criterion: {'Met' if lawson_product > lawson_criterion else 'Not Met'}<br>
            Fusion Rate: {fusion_rate:.2e} m⁻³·s⁻¹
        </div>
        """,
                    unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced fusion visualization
        def create_fusion_visualization():
            # Create subplots for fusion analysis
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=('Maxwell-Boltzmann Distribution',
                                'Fusion Cross Section',
                                'Fusion Rate vs Temperature',
                                'Energy Generation'),
                vertical_spacing=0.15,
                horizontal_spacing=0.1)

            # Maxwell-Boltzmann energy distribution
            E_range = np.linspace(0.1, 50, 500)  # keV
            kT = temperature
            maxwell = np.sqrt(E_range /
                              (np.pi * kT**3)) * np.exp(-E_range / kT)

            fig.add_trace(go.Scatter(
                x=E_range,
                y=maxwell,
                mode='lines',
                line=dict(color='#ef4444', width=3),
                fill='tozeroy',
                fillcolor='rgba(239, 68, 68, 0.3)',
                name='Maxwell Distribution',
                hovertemplate='E: %{x:.1f} keV<br>f(E): %{y:.4f}<extra></extra>'
            ),
                          row=1,
                          col=1)

            # Mark average energy
            avg_energy = 1.5 * kT
            fig.add_vline(x=avg_energy,
                          line=dict(color='yellow', width=2),
                          annotation_text=f"⟨E⟩ = {avg_energy:.1f} keV",
                          row=1,
                          col=1)

            # Fusion cross section vs energy
            cross_section = reaction_data['cross_section'] * np.exp(
                -reaction_data['threshold'] / E_range)
            cross_section[
                E_range <
                reaction_data['threshold']] *= 0.1  # Tunneling effect

            fig.add_trace(go.Scatter(
                x=E_range,
                y=cross_section,
                mode='lines',
                line=dict(color='#0ea5e9', width=3),
                name='Cross Section (mb)',
                hovertemplate='E: %{x:.1f} keV<br>σ: %{y:.1f} mb<extra></extra>'
            ),
                          row=1,
                          col=2)

            # Gamow peak (Maxwell × Cross section)
            gamow_peak = maxwell * cross_section / np.max(
                cross_section) * np.max(maxwell)
            fig.add_trace(go.Scatter(
                x=E_range,
                y=gamow_peak,
                mode='lines',
                line=dict(color='#10b981', width=3),
                name='Gamow Peak',
                hovertemplate='E: %{x:.1f} keV<br>Rate: %{y:.4f}<extra></extra>'
            ),
                          row=1,
                          col=2)

            # Fusion rate vs temperature
            T_range = np.linspace(1, 100, 100)
            rates = []
            for T in T_range:
                if T > 0:
                    sv = reaction_data['cross_section'] * 1e-31 * np.exp(
                        -reaction_data['threshold'] / T)
                    rate = 0.25 * (density * 1e20)**2 * sv
                    rates.append(rate)
                else:
                    rates.append(0)

            rates = np.array(rates)

            fig.add_trace(go.Scatter(
                x=T_range,
                y=rates,
                mode='lines',
                line=dict(color='#f59e0b', width=4),
                name='Fusion Rate',
                hovertemplate=
                'T: %{x:.1f} keV<br>Rate: %{y:.2e} m⁻³s⁻¹<extra></extra>'),
                          row=2,
                          col=1)

            # Mark current temperature
            fig.add_vline(x=temperature,
                          line=dict(color='red', width=2),
                          annotation_text=f"Current T",
                          row=2,
                          col=1)

            # Power generation
            power_density = rates * reaction_data[
                'q_value'] * 1.602e-19 * 1e6  # W/m³

            fig.add_trace(go.Scatter(
                x=T_range,
                y=power_density,
                mode='lines',
                line=dict(color='#a855f7', width=4),
                fill='tozeroy',
                fillcolor='rgba(168, 85, 247, 0.3)',
                name='Power Density (MW/m³)',
                hovertemplate=
                'T: %{x:.1f} keV<br>Power: %{y:.2e} MW/m³<extra></extra>'),
                          row=2,
                          col=2)

            # Add ignition criteria
            if environment == "Laboratory Plasma":
                ignition_temp = 10  # keV for D-T
                fig.add_hline(
                    y=1e6,  # 1 MW/m³ threshold
                    line=dict(color='green', width=2, dash='dash'),
                    annotation_text="Ignition Threshold",
                    row=2,
                    col=2)

            # Update layout and axes
            fig.update_layout(title=dict(
                text=f'<b>{selected_reaction} Fusion Analysis</b><br>'
                f'<span style="font-size:14px;">T = {temperature:.1f} keV, n = {density:.1f}×10²⁰ m⁻³</span>',
                x=0.5,
                font=dict(size=18, color='white')),
                              height=700,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            # Update axes
            fig.update_xaxes(title_text="Energy (keV)",
                             row=1,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="f(E)", row=1, col=1, color='white')
            fig.update_xaxes(title_text="Energy (keV)",
                             row=1,
                             col=2,
                             color='white')
            fig.update_yaxes(title_text="Cross Section (mb)",
                             row=1,
                             col=2,
                             color='white')
            fig.update_xaxes(title_text="Temperature (keV)",
                             row=2,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="Reaction Rate (m⁻³s⁻¹)",
                             row=2,
                             col=1,
                             type='log',
                             color='white')
            fig.update_xaxes(title_text="Temperature (keV)",
                             row=2,
                             col=2,
                             color='white')
            fig.update_yaxes(title_text="Power Density (MW/m³)",
                             row=2,
                             col=2,
                             type='log',
                             color='white')

            return fig

        fusion_fig = create_fusion_visualization()
        st.plotly_chart(fusion_fig, use_container_width=True)

        # Fusion analysis dashboard
        st.markdown("#### 📊 Fusion Energy Analysis")

        # Calculate key fusion parameters
        power_output = fusion_rate * reaction_data[
            'q_value'] * 1.602e-19 * 1e6  # MW/m³

        # Breakeven conditions
        q_factor = power_output / (density * 1e20 * temperature * 1.602e-16
                                   )  # Simplified

        # Stellar burning rates (for stellar core conditions)
        if environment == "Stellar Core":
            stellar_rate = fusion_rate * (
                1e8 / temperature)**0.5  # Temperature dependence
        else:
            stellar_rate = 0

        # Triple alpha process rate (for He burning)
        if temperature > 10:  # keV
            triple_alpha_rate = (density * 1e20)**2 * np.exp(-40 / temperature)
        else:
            triple_alpha_rate = 0

        # Display fusion metrics
        fusion_col1, fusion_col2, fusion_col3, fusion_col4 = st.columns(4)

        with fusion_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{power_output:.2e}</div>
                <div class="metric-label">Power (MW/m³)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fusion_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{q_factor:.2f}</div>
                <div class="metric-label">Q Factor</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fusion_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{lawson_product/lawson_criterion:.2f}</div>
                <div class="metric-label">Lawson Ratio</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with fusion_col4:
            burn_time = confinement_time * fusion_rate / (
                density * 1e20) if density > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{burn_time:.2e}</div>
                <div class="metric-label">Burn Time (s)</div>
            </div>
            """,
                        unsafe_allow_html=True)

with tabs[3]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🗺️</span> Nuclear Chart & Stability Valley
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore the chart of nuclides, stability valley, and nuclear shell structure with magic numbers.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>🗺️</span> Chart Parameters")

        # Chart display options
        chart_type = st.selectbox(
            "Chart Type",
            ["Stability Chart", "Binding Energy", "Half-Life", "Decay Mode"])

        # Nucleus range
        z_min = st.slider("Minimum Z (Protons)", 1, 50, 1, 1)
        z_max = st.slider("Maximum Z (Protons)", z_min + 1, 100, 30, 1)
        n_min = st.slider("Minimum N (Neutrons)", 1, 60, 1, 1)
        n_max = st.slider("Maximum N (Neutrons)", n_min + 1, 120, 40, 1)

        # Display options
        st.markdown("**Display Options:**")
        show_magic_numbers = st.checkbox("Show Magic Numbers", value=True)
        show_stability_valley = st.checkbox("Show Valley of Stability",
                                            value=True)
        show_drip_lines = st.checkbox("Show Drip Lines", value=False)

        # Magic numbers
        magic_numbers = [2, 8, 20, 28, 50, 82, 126]

        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Magic Numbers:</strong><br>
            Z,N = {', '.join(map(str, magic_numbers[:6]))}<br>
            <strong>Shell Closures:</strong><br>
            Enhanced stability at magic numbers
        </div>
        """,
                    unsafe_allow_html=True)

        # Nuclear models
        nuclear_model = st.selectbox(
            "Nuclear Model", ["Liquid Drop", "Shell Model", "Semi-Empirical"])

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced nuclear chart visualization
        def create_nuclear_chart():
            # Create coordinate arrays
            Z_range = np.arange(z_min, z_max + 1)
            N_range = np.arange(n_min, n_max + 1)
            Z_grid, N_grid = np.meshgrid(Z_range, N_range)

            # Calculate nuclear properties based on chart type
            if chart_type == "Stability Chart":
                # Simple stability estimate based on N/Z ratio
                stability = np.zeros_like(Z_grid, dtype=float)

                for i, n in enumerate(N_range):
                    for j, z in enumerate(Z_range):
                        if z == 0:
                            continue

                        # Optimal N/Z ratio for stability
                        if z <= 20:
                            optimal_ratio = 1.0
                        else:
                            optimal_ratio = 1.0 + 0.4 * (z - 20) / 80

                        actual_ratio = n / z
                        deviation = abs(actual_ratio - optimal_ratio)

                        # Stability decreases with deviation from optimal ratio
                        stability[i, j] = np.exp(-10 * deviation)

                        # Magic number enhancement
                        if show_magic_numbers:
                            if z in magic_numbers or n in magic_numbers:
                                stability[i, j] *= 2
                            if z in magic_numbers and n in magic_numbers:
                                stability[i, j] *= 3

                colorscale = 'Viridis'
                title_text = 'Nuclear Stability Chart'
                colorbar_title = 'Stability'

            elif chart_type == "Binding Energy":
                # Semi-empirical mass formula (SEMF)
                binding_energy = np.zeros_like(Z_grid, dtype=float)

                for i, n in enumerate(N_range):
                    for j, z in enumerate(Z_range):
                        if z == 0:
                            continue

                        A = z + n

                        # SEMF parameters (MeV)
                        a_v = 15.75  # Volume term
                        a_s = 17.8  # Surface term
                        a_c = 0.711  # Coulomb term
                        a_A = 23.7  # Asymmetry term

                        # Calculate binding energy
                        volume = a_v * A
                        surface = -a_s * A**(2 / 3)
                        coulomb = -a_c * z**2 / A**(1 / 3)
                        asymmetry = -a_A * (n - z)**2 / A

                        # Pairing term (simplified)
                        if n % 2 == 0 and z % 2 == 0:
                            pairing = 11.18 / A**(1 / 2)  # Even-even
                        elif n % 2 == 1 and z % 2 == 1:
                            pairing = -11.18 / A**(1 / 2)  # Odd-odd
                        else:
                            pairing = 0  # Even-odd

                        binding_energy[
                            i,
                            j] = volume + surface + coulomb + asymmetry + pairing

                colorscale = 'Plasma'
                title_text = 'Nuclear Binding Energy (SEMF)'
                colorbar_title = 'BE (MeV)'

            elif chart_type == "Half-Life":
                # Simplified half-life estimation
                half_life = np.zeros_like(Z_grid, dtype=float)

                for i, n in enumerate(N_range):
                    for j, z in enumerate(Z_range):
                        if z == 0:
                            continue

                        # Distance from stability valley
                        optimal_n = z if z <= 20 else z * (1 + 0.4 *
                                                           (z - 20) / 80)
                        distance = abs(n - optimal_n)

                        # Half-life decreases exponentially with distance from stability
                        log_half_life = 10 - 2 * distance

                        # Magic number effects
                        if z in magic_numbers or n in magic_numbers:
                            log_half_life += 2

                        half_life[i, j] = max(log_half_life, -10)

                colorscale = 'Hot'
                title_text = 'Nuclear Half-Life (log scale)'
                colorbar_title = 'log₁₀(t₁/₂ [s])'

            else:  # Decay Mode
                # Simplified decay mode prediction
                decay_mode = np.zeros_like(Z_grid, dtype=float)

                for i, n in enumerate(N_range):
                    for j, z in enumerate(Z_range):
                        if z == 0:
                            continue

                        ratio = n / z

                        if ratio < 1:
                            decay_mode[i, j] = 1  # β+ decay
                        elif ratio > 1.5:
                            decay_mode[i, j] = 2  # β- decay
                        elif z > 82:
                            decay_mode[i, j] = 3  # α decay
                        else:
                            decay_mode[i, j] = 0  # Stable

                colorscale = 'Set1'
                title_text = 'Primary Decay Modes'
                colorbar_title = 'Decay Type'

            # Create the heatmap
            fig = go.Figure(data=go.Heatmap(
                x=Z_range,
                y=N_range,
                z=stability if chart_type == "Stability Chart" else
                binding_energy if chart_type == "Binding Energy" else
                half_life if chart_type == "Half-Life" else decay_mode,
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                hovertemplate='Z: %{x}<br>N: %{y}<br>' + colorbar_title +
                ': %{z:.2f}<extra></extra>'))

            # Add magic number lines
            if show_magic_numbers:
                for magic in magic_numbers:
                    if z_min <= magic <= z_max:
                        fig.add_vline(x=magic,
                                      line=dict(color='white',
                                                width=2,
                                                dash='dash'),
                                      annotation_text=f"Z={magic}")
                    if n_min <= magic <= n_max:
                        fig.add_hline(y=magic,
                                      line=dict(color='white',
                                                width=2,
                                                dash='dash'),
                                      annotation_text=f"N={magic}")

            # Add valley of stability
            if show_stability_valley:
                z_valley = np.arange(z_min, z_max + 1)
                n_valley = []
                for z in z_valley:
                    if z <= 20:
                        n_valley.append(z)
                    else:
                        n_valley.append(z * (1 + 0.4 * (z - 20) / 80))

                fig.add_trace(
                    go.Scatter(
                        x=z_valley,
                        y=n_valley,
                        mode='lines',
                        line=dict(color='red', width=4),
                        name='Valley of Stability',
                        hovertemplate='Z: %{x}<br>N: %{y:.1f}<extra></extra>'))

            # Add drip lines (simplified)
            if show_drip_lines:
                # Proton drip line (approximate)
                z_proton_drip = np.arange(z_min, min(z_max, 100))
                n_proton_drip = 0.8 * z_proton_drip

                fig.add_trace(
                    go.Scatter(x=z_proton_drip,
                               y=n_proton_drip,
                               mode='lines',
                               line=dict(color='blue', width=3, dash='dot'),
                               name='Proton Drip Line',
                               hoverinfo='skip'))

                # Neutron drip line (approximate)
                z_neutron_drip = np.arange(z_min, min(z_max, 100))
                n_neutron_drip = 2 * z_neutron_drip

                fig.add_trace(
                    go.Scatter(x=z_neutron_drip,
                               y=n_neutron_drip,
                               mode='lines',
                               line=dict(color='cyan', width=3, dash='dot'),
                               name='Neutron Drip Line',
                               hoverinfo='skip'))

            # Update layout
            fig.update_layout(title=dict(
                text=f'<b>{title_text}</b><br>'
                f'<span style="font-size:14px;">Z: {z_min}-{z_max}, N: {n_min}-{n_max}</span>',
                x=0.5,
                font=dict(size=18, color='white')),
                              xaxis=dict(title='Atomic Number (Z)',
                                         color='white'),
                              yaxis=dict(title='Neutron Number (N)',
                                         color='white'),
                              height=600,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            return fig

        chart_fig = create_nuclear_chart()
        st.plotly_chart(chart_fig, use_container_width=True)

        # Nuclear chart analysis
        st.markdown("#### 📊 Nuclear Chart Analysis")

        # Calculate chart statistics
        total_nuclei = (z_max - z_min + 1) * (n_max - n_min + 1)
        stable_count = 0
        magic_count = 0

        # Count nuclei in different categories
        for z in range(z_min, z_max + 1):
            for n in range(n_min, n_max + 1):
                if z == 0:
                    continue

                # Check if in stability valley
                if z <= 20:
                    optimal_n = z
                else:
                    optimal_n = z * (1 + 0.4 * (z - 20) / 80)

                if abs(n - optimal_n) < 2:
                    stable_count += 1

                if z in magic_numbers or n in magic_numbers:
                    magic_count += 1

        # Average mass number
        avg_mass = (z_max + z_min + n_max + n_min) / 2

        # Display chart metrics
        chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)

        with chart_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_nuclei}</div>
                <div class="metric-label">Total Nuclei</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with chart_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stable_count}</div>
                <div class="metric-label">Near Stability</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with chart_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{magic_count}</div>
                <div class="metric-label">Magic Nuclei</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with chart_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_mass:.0f}</div>
                <div class="metric-label">Average Mass</div>
            </div>
            """,
                        unsafe_allow_html=True)

with tabs[4]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            <span class="interactive-icon">⚡</span> Nuclear Reactions & Cross Sections
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Analyze nuclear reaction kinematics, cross sections, and interaction probabilities.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>⚡</span> Reaction Parameters")

        # Nuclear reaction selection
        reactions = {
            "p + ⁷Li → α + α": {
                "Q": 17.35,
                "threshold": 1.88,
                "type": "Endothermic"
            },
            "n + ²³⁵U → fission": {
                "Q": 200,
                "threshold": 0,
                "type": "Fission"
            },
            "d + t → α + n": {
                "Q": 17.59,
                "threshold": 0,
                "type": "Fusion"
            },
            "α + ¹⁴N → p + ¹⁷O": {
                "Q": -1.19,
                "threshold": 1.53,
                "type": "Endothermic"
            },
            "p + ¹¹B → 3α": {
                "Q": 8.68,
                "threshold": 0,
                "type": "Aneutronic"
            }
        }

        selected_reaction = st.selectbox("Nuclear Reaction",
                                         list(reactions.keys()))
        reaction_data = reactions[selected_reaction]

        # Beam parameters
        beam_energy = st.slider("Beam Energy (MeV)", 0.1, 100.0, 10.0, 0.1)
        target_thickness = st.slider("Target Thickness (mg/cm²)", 0.1, 100.0,
                                     10.0, 0.1)
        beam_current = st.slider("Beam Current (μA)", 0.1, 100.0, 1.0, 0.1)

        # Calculate reaction parameters
        if beam_energy > reaction_data["threshold"]:
            reaction_possible = True
            available_energy = beam_energy - reaction_data["threshold"]
        else:
            reaction_possible = False
            available_energy = 0

        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Reaction Analysis:</strong><br>
            Q-value: {reaction_data['Q']:.2f} MeV<br>
            Threshold: {reaction_data['threshold']:.2f} MeV<br>
            Type: {reaction_data['type']}<br>
            Status: {'Possible' if reaction_possible else 'Below Threshold'}
        </div>
        """,
                    unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        def create_reaction_visualization():
            # Cross section vs energy plot
            energies = np.linspace(0.1, 50, 500)

            # Simplified cross section calculation
            cross_sections = np.zeros_like(energies)
            for i, E in enumerate(energies):
                if E > reaction_data["threshold"]:
                    if "fission" in selected_reaction:
                        # Fission cross section
                        cross_sections[i] = 580 * np.exp(-0.1 * E)  # barns
                    elif "fusion" in selected_reaction or "d + t" in selected_reaction:
                        # Fusion cross section (simplified Gamow peak)
                        cross_sections[i] = 5000 * np.exp(
                            -19.94 / np.sqrt(E)) * np.exp(-E / 100) * 1e-3
                    else:
                        # General reaction cross section
                        cross_sections[i] = 100 * np.sqrt(
                            E - reaction_data["threshold"]) / E

            fig = make_subplots(rows=2,
                                cols=1,
                                subplot_titles=('Cross Section vs Energy',
                                                'Reaction Rate vs Energy'),
                                vertical_spacing=0.15)

            # Cross section plot
            fig.add_trace(go.Scatter(
                x=energies,
                y=cross_sections,
                mode='lines',
                line=dict(color='#ef4444', width=4),
                name='Cross Section',
                hovertemplate='E: %{x:.2f} MeV<br>σ: %{y:.2f} mb<extra></extra>'
            ),
                          row=1,
                          col=1)

            # Mark threshold energy
            if reaction_data["threshold"] > 0:
                fig.add_vline(
                    x=reaction_data["threshold"],
                    line=dict(color='white', width=2, dash='dash'),
                    annotation_text=
                    f"Threshold: {reaction_data['threshold']:.2f} MeV",
                    row=1,
                    col=1)

            # Mark current beam energy
            fig.add_vline(x=beam_energy,
                          line=dict(color='yellow', width=2),
                          annotation_text=f"Beam: {beam_energy:.2f} MeV",
                          row=1,
                          col=1)

            # Reaction rate calculation
            avogadro = 6.022e23
            target_density = target_thickness * 1e-3 * 1e4  # nuclei/cm²
            beam_intensity = beam_current * 1e-6 / 1.602e-19  # particles/s

            reaction_rates = cross_sections * 1e-27 * target_density * beam_intensity  # reactions/s

            fig.add_trace(go.Scatter(
                x=energies,
                y=reaction_rates,
                mode='lines',
                line=dict(color='#0ea5e9', width=4),
                fill='tozeroy',
                fillcolor='rgba(14, 165, 233, 0.3)',
                name='Reaction Rate',
                hovertemplate=
                'E: %{x:.2f} MeV<br>Rate: %{y:.2e} s⁻¹<extra></extra>'),
                          row=2,
                          col=1)

            # Mark current operating point
            current_cs = np.interp(beam_energy, energies, cross_sections)
            current_rate = np.interp(beam_energy, energies, reaction_rates)

            fig.add_trace(go.Scatter(
                x=[beam_energy],
                y=[current_rate],
                mode='markers',
                marker=dict(size=12, color='yellow', symbol='star'),
                name='Operating Point',
                hovertemplate=f'Rate: {current_rate:.2e} s⁻¹<extra></extra>'),
                          row=2,
                          col=1)

            fig.update_layout(title=dict(
                text=
                f'<b>{selected_reaction}</b><br><span style="font-size:14px;">Q = {reaction_data["Q"]:.2f} MeV, Current Rate: {current_rate:.2e} s⁻¹</span>',
                x=0.5,
                font=dict(size=18, color='white')),
                              height=700,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            fig.update_xaxes(title_text="Energy (MeV)", color='white')
            fig.update_yaxes(title_text="Cross Section (mb)",
                             color='white',
                             row=1,
                             col=1)
            fig.update_yaxes(title_text="Reaction Rate (s⁻¹)",
                             color='white',
                             type='log',
                             row=2,
                             col=1)

            return fig

        reaction_fig = create_reaction_visualization()
        st.plotly_chart(reaction_fig, use_container_width=True)

        # Nuclear reaction analysis
        st.markdown("#### 📊 Reaction Analysis Dashboard")

        # Calculate key parameters
        current_cs = 100 if beam_energy > reaction_data["threshold"] else 0
        current_rate = current_cs * 1e-27 * target_thickness * 1e-3 * 1e4 * beam_current * 1e-6 / 1.602e-19

        # Display reaction metrics
        react_col1, react_col2, react_col3, react_col4 = st.columns(4)

        with react_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{current_cs:.1f}</div>
                <div class="metric-label">Cross Section (mb)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with react_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{current_rate:.2e}</div>
                <div class="metric-label">Reaction Rate (s⁻¹)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with react_col3:
            efficiency = (current_rate * 100) / (
                beam_current * 1e-6 / 1.602e-19) if beam_current > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{efficiency:.2e}</div>
                <div class="metric-label">Efficiency (%)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with react_col4:
            power_deposited = beam_energy * beam_current * 1e-6  # Watts
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{power_deposited:.3f}</div>
                <div class="metric-label">Power (W)</div>
            </div>
            """,
                        unsafe_allow_html=True)

with tabs[5]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            <span class="interactive-icon">🔬</span> Radiation Detection & Dosimetry
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Analyze radiation detection methods, shielding effectiveness, and dose calculations.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown(
            "#### <span class='interactive-icon'>🔬</span> Detection Parameters"
        )

        # Radiation source selection
        sources = {
            "Co-60": {
                "energy": 1.25,
                "half_life": 5.27,
                "type": "γ",
                "activity": 1e12
            },
            "Cs-137": {
                "energy": 0.662,
                "half_life": 30.17,
                "type": "γ",
                "activity": 3.7e10
            },
            "Am-241": {
                "energy": 5.486,
                "half_life": 432.7,
                "type": "α",
                "activity": 3.7e9
            },
            "Sr-90": {
                "energy": 0.546,
                "half_life": 28.8,
                "type": "β",
                "activity": 3.7e10
            },
            "Ra-226": {
                "energy": 4.78,
                "half_life": 1600,
                "type": "α",
                "activity": 3.7e10
            }
        }

        selected_source = st.selectbox("Radiation Source",
                                       list(sources.keys()))
        source_data = sources[selected_source]

        # Detection setup
        detector_type = st.selectbox("Detector Type", [
            "Geiger-Müller", "Scintillator", "Semiconductor", "Ion Chamber",
            "Proportional Counter"
        ])

        distance = st.slider("Source-Detector Distance (cm)", 1.0, 100.0, 10.0,
                             1.0)
        shield_material = st.selectbox(
            "Shield Material",
            ["None", "Lead", "Aluminum", "Concrete", "Water"])
        shield_thickness = st.slider("Shield Thickness (cm)", 0.0, 10.0, 0.0,
                                     0.1) if shield_material != "None" else 0.0

        # Calculate detection parameters
        source_activity = source_data["activity"]  # Bq
        geometric_efficiency = 1 / (4 * np.pi *
                                    (distance * 1e-2)**2)  # solid angle factor

        # Attenuation calculation
        if shield_material == "Lead":
            mu = 1.2  # cm⁻¹ for 1 MeV gamma in lead
        elif shield_material == "Aluminum":
            mu = 0.16
        elif shield_material == "Concrete":
            mu = 0.09
        elif shield_material == "Water":
            mu = 0.07
        else:
            mu = 0

        attenuation_factor = np.exp(
            -mu * shield_thickness) if shield_material != "None" else 1.0
        detected_rate = source_activity * geometric_efficiency * attenuation_factor * 0.1  # simplified efficiency

        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Detection Setup:</strong><br>
            Source: {selected_source}<br>
            Energy: {source_data['energy']:.3f} MeV<br>
            Type: {source_data['type']}-radiation<br>
            Count Rate: {detected_rate:.2e} cps
        </div>
        """,
                    unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        def create_detection_visualization():
            # Create attenuation and detection efficiency plots
            fig = make_subplots(
                rows=2,
                cols=1,
                subplot_titles=('Radiation Attenuation vs Shield Thickness',
                                'Detection Efficiency vs Energy'),
                vertical_spacing=0.15)

            # Attenuation plot
            thicknesses = np.linspace(0, 10, 100)
            if shield_material != "None":
                intensity = np.exp(-mu * thicknesses)
            else:
                intensity = np.ones_like(thicknesses)

            fig.add_trace(go.Scatter(
                x=thicknesses,
                y=intensity,
                mode='lines',
                line=dict(color='#ef4444', width=4),
                name=f'Attenuation ({shield_material})',
                hovertemplate=
                'Thickness: %{x:.2f} cm<br>I/I₀: %{y:.3f}<extra></extra>'),
                          row=1,
                          col=1)

            # Mark current shield thickness
            if shield_material != "None":
                current_attenuation = np.exp(-mu * shield_thickness)
                fig.add_trace(go.Scatter(
                    x=[shield_thickness],
                    y=[current_attenuation],
                    mode='markers',
                    marker=dict(size=12, color='yellow', symbol='star'),
                    name='Current Setup',
                    hovertemplate=
                    f'Attenuation: {current_attenuation:.3f}<extra></extra>'),
                              row=1,
                              col=1)

            # Half-value layer
            if shield_material != "None":
                hvl = np.log(2) / mu
                fig.add_vline(x=hvl,
                              line=dict(color='white', width=2, dash='dash'),
                              annotation_text=f"HVL: {hvl:.2f} cm",
                              row=1,
                              col=1)

            # Detection efficiency vs energy (simplified)
            energies = np.linspace(0.1, 5, 100)
            if detector_type == "Geiger-Müller":
                efficiency = 0.01 * np.ones_like(
                    energies)  # Constant low efficiency
            elif detector_type == "Scintillator":
                efficiency = 0.5 * np.exp(
                    -energies / 2)  # Decreasing with energy
            elif detector_type == "Semiconductor":
                efficiency = 0.8 * np.exp(-energies / 3)  # Higher efficiency
            else:
                efficiency = 0.1 * np.ones_like(energies)

            fig.add_trace(go.Scatter(
                x=energies,
                y=efficiency * 100,
                mode='lines',
                line=dict(color='#0ea5e9', width=4),
                fill='tozeroy',
                fillcolor='rgba(14, 165, 233, 0.3)',
                name=f'{detector_type} Efficiency',
                hovertemplate=
                'Energy: %{x:.2f} MeV<br>Efficiency: %{y:.1f}%<extra></extra>'
            ),
                          row=2,
                          col=1)

            # Mark source energy
            source_efficiency = np.interp(source_data["energy"], energies,
                                          efficiency * 100)
            fig.add_trace(go.Scatter(
                x=[source_data["energy"]],
                y=[source_efficiency],
                mode='markers',
                marker=dict(size=12, color='yellow', symbol='star'),
                name='Source Energy',
                hovertemplate=
                f'Efficiency: {source_efficiency:.1f}%<extra></extra>'),
                          row=2,
                          col=1)

            fig.update_layout(title=dict(
                text=
                f'<b>Radiation Detection Analysis</b><br><span style="font-size:14px;">{selected_source} → {detector_type}, Rate: {detected_rate:.2e} cps</span>',
                x=0.5,
                font=dict(size=18, color='white')),
                              height=700,
                              showlegend=True,
                              legend=dict(x=1.02, y=1),
                              plot_bgcolor='rgba(45, 55, 72, 0.9)',
                              paper_bgcolor='rgba(12, 24, 33, 0.9)')

            fig.update_xaxes(title_text="Shield Thickness (cm)",
                             row=1,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="Relative Intensity",
                             row=1,
                             col=1,
                             color='white')
            fig.update_xaxes(title_text="Energy (MeV)",
                             row=2,
                             col=1,
                             color='white')
            fig.update_yaxes(title_text="Detection Efficiency (%)",
                             row=2,
                             col=1,
                             color='white')

            return fig

        detection_fig = create_detection_visualization()
        st.plotly_chart(detection_fig, use_container_width=True)

        # Dosimetry analysis
        st.markdown("#### 📊 Dosimetry Analysis Dashboard")

        # Calculate dose parameters
        dose_rate = source_activity * source_data["energy"] * 1.602e-13 / (
            4 * np.pi * (distance * 1e-2)**2) * attenuation_factor  # Gy/s
        dose_rate_usv = dose_rate * 1e6  # μSv/s
        annual_dose = dose_rate_usv * 3600 * 24 * 365 / 1000  # mSv/year

        # Display dosimetry metrics
        dose_col1, dose_col2, dose_col3, dose_col4 = st.columns(4)

        with dose_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{detected_rate:.2e}</div>
                <div class="metric-label">Count Rate (cps)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with dose_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dose_rate_usv:.2f}</div>
                <div class="metric-label">Dose Rate (μSv/s)</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with dose_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{attenuation_factor:.3f}</div>
                <div class="metric-label">Attenuation Factor</div>
            </div>
            """,
                        unsafe_allow_html=True)

        with dose_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{annual_dose:.1f}</div>
                <div class="metric-label">Annual Dose (mSv)</div>
            </div>
            """,
                        unsafe_allow_html=True)

with tabs[6]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🎓</span> Nuclear Physics Learning Hub
        </h2>
        <p style="color: #e2e8f0; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Comprehensive learning resources, nuclear data, and interactive problem-solving tools.
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    # Learning resources with enhanced interactivity
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="nuclear-card">
            <h4 style="color: white; margin-bottom: 1rem;">📚 Nuclear Concepts</h4>
            <div style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                <strong>Fundamental Concepts:</strong><br>
                • Nuclear structure and shell model<br>
                • Radioactive decay chains<br>
                • Nuclear reactions and cross sections<br>
                • Fission and fusion processes<br><br>
                
                <strong>Advanced Topics:</strong><br>
                • Neutron activation analysis<br>
                • Reactor physics and criticality<br>
                • Nuclear astrophysics<br>
                • Medical applications<br>
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="nuclear-card">
            <h4 style="color: white; margin-bottom: 1rem;">🧮 Nuclear Calculator</h4>
            <div style="color: rgba(255,255,255,0.9);">
                <strong>Interactive Nuclear Data:</strong><br>
                Enter isotope (e.g., U-235, Pu-239):
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

        # Interactive nuclear calculator
        isotope_input = st.text_input("Isotope",
                                      value="U-235",
                                      key="nuclear_calc")

        # Nuclear data lookup (simplified)
        nuclear_data = {
            "U-235": {
                "mass": 235.044,
                "half_life": "7.04×10⁸ years",
                "decay_mode": "α",
                "abundance": "0.72%"
            },
            "U-238": {
                "mass": 238.051,
                "half_life": "4.47×10⁹ years",
                "decay_mode": "α",
                "abundance": "99.27%"
            },
            "Pu-239": {
                "mass": 239.052,
                "half_life": "2.41×10⁴ years",
                "decay_mode": "α",
                "abundance": "synthetic"
            },
            "C-14": {
                "mass": 14.003,
                "half_life": "5730 years",
                "decay_mode": "β⁻",
                "abundance": "trace"
            },
        }

        if isotope_input in nuclear_data:
            data = nuclear_data[isotope_input]
            st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>{isotope_input} Properties:</strong><br>
                Mass: {data['mass']} u<br>
                Half-life: {data['half_life']}<br>
                Decay mode: {data['decay_mode']}<br>
                Abundance: {data['abundance']}
            </div>
            """,
                        unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="nuclear-card">
            <h4 style="color: white; margin-bottom: 1rem;">⚡ Nuclear Equations</h4>
            <div style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                <strong>Key Nuclear Equations:</strong><br><br>
                
                <strong>Decay Law:</strong><br>
                N(t) = N₀e^(-λt)<br><br>
                
                <strong>Activity:</strong><br>
                A = λN = A₀e^(-λt)<br><br>
                
                <strong>Mass-Energy:</strong><br>
                E = mc² = 931.5 MeV/u<br><br>
                
                <strong>Fission Energy:</strong><br>
                Q = (Σm_reactants - Σm_products)c²<br><br>
                
                <strong>Cross Section:</strong><br>
                σ = λ/(n·v)
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

        # Interactive problem solver
        st.markdown("""
        <div class="nuclear-card">
            <h4 style="color: white; margin-bottom: 1rem;">🔬 Problem Solver</h4>
            <div style="color: rgba(255,255,255,0.9);">
                <strong>Decay Problem Calculator:</strong>
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

        # Problem solving interface
        problem_type = st.selectbox("Problem Type", [
            "Radioactive Decay", "Half-Life Calculation",
            "Activity Conversion", "Mass Defect & Binding Energy"
        ])

        if problem_type == "Radioactive Decay":
            initial_activity = st.number_input("Initial Activity (Bq)",
                                               value=1e6,
                                               format="%.0e")
            half_life_years = st.number_input("Half-life (years)",
                                              value=5730.0)
            time_years = st.number_input("Time elapsed (years)", value=1000.0)

            # Calculate final activity
            lambda_decay = np.log(2) / half_life_years
            final_activity = initial_activity * np.exp(
                -lambda_decay * time_years)

            st.markdown(f"""
            <div style="background: rgba(34, 197, 94, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Solution:</strong><br>
                λ = {lambda_decay:.2e} year⁻¹<br>
                Final Activity = {final_activity:.2e} Bq<br>
                Fraction Remaining = {final_activity/initial_activity:.4f}
            </div>
            """,
                        unsafe_allow_html=True)

    # Enhanced nuclear data visualization
    st.markdown("#### 📊 Nuclear Data Visualization")

    # Create enhanced nuclear data plot
    def create_nuclear_data_plot():
        # Sample nuclear data for visualization
        isotopes = [
            'H-1', 'He-4', 'Li-7', 'C-12', 'O-16', 'Fe-56', 'U-235', 'U-238'
        ]
        binding_energies = [0, 28.3, 39.2, 92.2, 127.6, 492.3, 1783.9,
                            1801.7]  # MeV
        mass_numbers = [1, 4, 7, 12, 16, 56, 235, 238]
        be_per_nucleon = [
            be / a for be, a in zip(binding_energies, mass_numbers)
        ]

        fig = make_subplots(rows=1,
                            cols=2,
                            subplot_titles=('Binding Energy per Nucleon',
                                            'Nuclear Stability Chart'),
                            horizontal_spacing=0.1)

        # Binding energy curve
        fig.add_trace(go.Scatter(
            x=mass_numbers,
            y=be_per_nucleon,
            mode='lines+markers',
            line=dict(color='#ef4444', width=4),
            marker=dict(size=10, color='red'),
            name='BE/A',
            hovertemplate='A: %{x}<br>BE/A: %{y:.2f} MeV<extra></extra>'),
                      row=1,
                      col=1)

        # Mark Fe-56 peak
        fig.add_annotation(x=56,
                           y=8.8,
                           text="Fe-56<br>Most Stable",
                           showarrow=True,
                           arrowhead=2,
                           arrowcolor="white",
                           font=dict(color="white", size=12),
                           bgcolor="rgba(239, 68, 68, 0.8)",
                           row=1,
                           col=1)

        # Nuclear chart visualization (simplified)
        z_vals = [1, 2, 3, 6, 8, 26, 92, 92]
        n_vals = [0, 2, 4, 6, 8, 30, 143, 146]
        colors = [
            'yellow', 'orange', 'green', 'blue', 'purple', 'red', 'darkred',
            'black'
        ]

        fig.add_trace(go.Scatter(
            x=z_vals,
            y=n_vals,
            mode='markers',
            marker=dict(size=15, color=colors),
            text=isotopes,
            textposition="top center",
            name='Isotopes',
            hovertemplate=
            'Z: %{x}<br>N: %{y}<br>Isotope: %{text}<extra></extra>'),
                      row=1,
                      col=2)

        # Add stability valley line
        z_line = np.linspace(1, 100, 100)
        n_line = z_line * 1.2  # Simplified stability line
        fig.add_trace(go.Scatter(x=z_line,
                                 y=n_line,
                                 mode='lines',
                                 line=dict(color='white', width=2,
                                           dash='dash'),
                                 name='Stability Valley',
                                 showlegend=False),
                      row=1,
                      col=2)

        fig.update_layout(title=dict(
            text='<b>Nuclear Physics Data Visualization</b>',
            x=0.5,
            font=dict(size=18, color='white')),
                          height=500,
                          showlegend=True,
                          plot_bgcolor='rgba(45, 55, 72, 0.9)',
                          paper_bgcolor='rgba(12, 24, 33, 0.9)')

        fig.update_xaxes(title_text="Mass Number (A)",
                         row=1,
                         col=1,
                         color='white')
        fig.update_yaxes(title_text="BE/A (MeV)", row=1, col=1, color='white')
        fig.update_xaxes(title_text="Proton Number (Z)",
                         row=1,
                         col=2,
                         color='white')
        fig.update_yaxes(title_text="Neutron Number (N)",
                         row=1,
                         col=2,
                         color='white')

        return fig

    nuclear_data_fig = create_nuclear_data_plot()
    st.plotly_chart(nuclear_data_fig, use_container_width=True)

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); 
           border-radius: 15px; text-align: center; border: 1px solid #718096;">
    <h3 style="color: white; margin-bottom: 1rem;">☢️ Nuclear Physics Laboratory</h3>
    <p style="color: #e2e8f0; margin-bottom: 1.5rem;">
        Explore the fundamental forces and reactions that power the universe.
    </p>
</div>
""",
            unsafe_allow_html=True)
