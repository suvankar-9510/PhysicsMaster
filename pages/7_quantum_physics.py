import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import cmath
from scipy.special import hermite, factorial
from scipy.integrate import quad
from utils.theme import render_theme_sidebar

st.set_page_config(
    page_title="Quantum Physics Laboratory",
    page_icon="⚛️",
    layout="wide"
)

theme = render_theme_sidebar()
dark = theme["dark"]

# Enhanced CSS with quantum-inspired design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
        color: white;
    }

    /* Quantum-themed header with particle animations */
    .quantum-header {
        background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #a855f7 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #8b5cf6;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
    }

    .quantum-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 80% 40%, rgba(255,255,255,0.08) 1px, transparent 1px),
            radial-gradient(circle at 40% 80%, rgba(255,255,255,0.06) 1.5px, transparent 1.5px),
            radial-gradient(circle at 60% 20%, rgba(255,255,255,0.04) 1px, transparent 1px);
        background-size: 50px 50px, 80px 80px, 60px 60px, 40px 40px;
        animation: quantumField 20s linear infinite;
    }

    /* Enhanced section cards with quantum glow */
    .physics-section {
        background: rgba(30, 41, 59, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .physics-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
    }

    .physics-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #8b5cf6, #7c3aed, #6d28d9, #5b21b6);
        animation: quantumGradient 3s ease-in-out infinite;
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
        border-color: #8b5cf6;
    }

    .param-panel h4 {
        color: #a855f7;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Enhanced metric cards with quantum effects */
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
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2);
        border-color: #8b5cf6;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1), transparent);
        transition: left 0.5s ease;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #a855f7;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }

    .metric-label {
        font-size: 1rem;
        color: #cbd5e1;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }

    /* Enhanced tabs with quantum styling */
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
        background: rgba(139, 92, 246, 0.2);
        color: #c084fc;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        transform: translateY(-3px);
    }

    /* Quantum visualization cards */
    .quantum-card {
        background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #8b5cf6;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .quantum-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.4);
        border-color: #a855f7;
    }

    .quantum-card::before {
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

    .quantum-card:hover::before {
        width: 300px;
        height: 300px;
    }

    .quantum-card h5 {
        color: white;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.2rem;
        position: relative;
        z-index: 2;
    }

    /* Advanced animations */
    @keyframes quantumField {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-10px, -10px); }
        50% { transform: translate(-20px, 10px); }
        75% { transform: translate(10px, -20px); }
        100% { transform: translate(0, 0); }
    }

    @keyframes quantumGradient {
        0%, 100% { background: linear-gradient(90deg, #8b5cf6, #7c3aed, #6d28d9, #5b21b6); }
        25% { background: linear-gradient(90deg, #7c3aed, #6d28d9, #5b21b6, #8b5cf6); }
        50% { background: linear-gradient(90deg, #6d28d9, #5b21b6, #8b5cf6, #7c3aed); }
        75% { background: linear-gradient(90deg, #5b21b6, #8b5cf6, #7c3aed, #6d28d9); }
    }

    @keyframes waveFunction {
        0%, 100% { transform: scaleY(1) rotateX(0deg); }
        50% { transform: scaleY(1.1) rotateX(5deg); }
    }

    @keyframes electronOrbit {
        0% { transform: rotate(0deg) translateX(20px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(20px) rotate(-360deg); }
    }

    @keyframes quantumTunnel {
        0% { transform: translateX(-50px) scale(1); opacity: 0.8; }
        50% { transform: translateX(0px) scale(0.5); opacity: 0.3; }
        100% { transform: translateX(50px) scale(1); opacity: 0.8; }
    }

    /* Interactive elements */
    .interactive-icon {
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .interactive-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(139, 92, 246, 0.3));
    }

    /* Quantum state indicators */
    .quantum-state {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin: 0 5px;
        animation: quantumPulse 2s ease-in-out infinite;
    }

    @keyframes quantumPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .quantum-header {
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

# Enhanced quantum-themed header
st.markdown("""
<div class="quantum-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span class="interactive-icon">⚛️</span> Quantum Physics Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Explore the Fundamental Nature of Reality
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Wave Functions</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Quantum States</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Entanglement</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced tabs with comprehensive quantum phenomena
tabs = st.tabs([
    "🌊 Wave Functions", 
    "🎯 Quantum States", 
    "🔗 Quantum Entanglement", 
    "🚇 Quantum Tunneling",
    "🎲 Quantum Measurement",
    "🧮 Quantum Computing",
    "🎓 Learning Hub"
])

# Tab 1: Enhanced Wave Functions
with tabs[0]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🌊</span> Quantum Wave Functions & Probability
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore the fundamental wave nature of quantum particles through interactive Schrödinger equation solutions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>⚙️</span> Quantum Parameters")

        # Enhanced quantum system selection
        quantum_system = st.selectbox("Quantum System", [
            "Particle in a Box",
            "Quantum Harmonic Oscillator", 
            "Hydrogen Atom",
            "Quantum Well",
            "Quantum Barrier",
            "Custom Potential"
        ])

        if quantum_system == "Particle in a Box":
            box_length = st.slider("Box Length (nm)", 0.1, 5.0, 1.0, 0.1)
            quantum_number = st.slider("Quantum Number (n)", 1, 10, 1, 1)

        elif quantum_system == "Quantum Harmonic Oscillator":
            frequency = st.slider("Oscillator Frequency (THz)", 1, 100, 10, 1)
            quantum_number = st.slider("Quantum Number (n)", 0, 10, 0, 1)

        elif quantum_system == "Hydrogen Atom":
            principal_n = st.slider("Principal Quantum Number (n)", 1, 5, 1, 1)
            angular_l = st.slider("Angular Quantum Number (l)", 0, principal_n-1, 0, 1)
            magnetic_m = st.slider("Magnetic Quantum Number (m)", -angular_l, angular_l, 0, 1)

        else:
            # Default parameters for other systems
            quantum_number = st.slider("Energy Level", 0, 5, 0, 1)
            potential_strength = st.slider("Potential Strength", 0.1, 10.0, 1.0, 0.1)

        # Visualization controls
        st.markdown("#### <span class='interactive-icon'>🎨</span> Visualization")
        show_probability = st.checkbox("Show Probability Density", value=True)
        show_classical = st.checkbox("Show Classical Analogue", value=False)
        animate_wave = st.checkbox("Animate Wave Function", value=True)

        # Physical constants
        st.markdown("#### <span class='interactive-icon'>📊</span> Physical Properties")

        # Calculate energy levels
        if quantum_system == "Particle in a Box":
            # E_n = n²h²/(8mL²)
            mass = 9.109e-31  # electron mass
            h = 6.626e-34
            L = box_length * 1e-9
            energy = (quantum_number**2 * h**2) / (8 * mass * L**2) * 6.242e18  # Convert to eV

        elif quantum_system == "Quantum Harmonic Oscillator":
            # E_n = ℏω(n + 1/2)
            hbar = 1.055e-34
            omega = frequency * 1e12 * 2 * np.pi
            energy = hbar * omega * (quantum_number + 0.5) * 6.242e18  # Convert to eV

        else:
            energy = quantum_number * 1.0  # Simplified

        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Energy Level:</strong> {energy:.3f} eV<br>
            <strong>System:</strong> {quantum_system}<br>
            <strong>State:</strong> |n={quantum_number}⟩
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced quantum wave function visualization
        def create_quantum_wave_visualization():
            if quantum_system == "Particle in a Box":
                x = np.linspace(0, box_length, 1000)
                L = box_length
                n = quantum_number

                # Normalized wave function
                psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
                probability = np.abs(psi)**2

                # Classical probability (uniform)
                classical_prob = np.ones_like(x) / L if show_classical else None

                title = f"Particle in a Box (n={n}, L={L:.1f} nm)"
                x_label = "Position (nm)"

            elif quantum_system == "Quantum Harmonic Oscillator":
                # Use dimensionless coordinates
                x_max = 5
                x = np.linspace(-x_max, x_max, 1000)
                n = quantum_number

                # Hermite polynomials for harmonic oscillator
                H_n = hermite(n)
                normalization = 1 / np.sqrt(2**n * factorial(n) * np.sqrt(np.pi))
                psi = normalization * H_n(x) * np.exp(-x**2 / 2)
                probability = np.abs(psi)**2

                # Classical turning points
                if show_classical:
                    E_n = n + 0.5
                    x_classical = np.sqrt(2 * E_n)
                    classical_prob = np.where(np.abs(x) <= x_classical, 
                                            1 / (2 * x_classical), 0)
                else:
                    classical_prob = None

                title = f"Quantum Harmonic Oscillator (n={n})"
                x_label = "Position (ξ)"

            else:
                # Generic wave function
                x = np.linspace(-5, 5, 1000)
                k = quantum_number + 1
                psi = np.sin(k * x) * np.exp(-x**2 / 4)
                psi = psi / np.sqrt(np.trapz(np.abs(psi)**2, x))  # Normalize
                probability = np.abs(psi)**2
                classical_prob = None

                title = f"Generic Quantum System (n={quantum_number})"
                x_label = "Position"

            # Create subplots
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Wave Function ψ(x)', 'Probability Density |ψ(x)|²'),
                vertical_spacing=0.15
            )

            # Wave function plot
            if animate_wave:
                # Create animation frames
                n_frames = 60
                frames = []

                for frame in range(n_frames):
                    t = frame / n_frames * 2 * np.pi
                    # Time evolution: ψ(x,t) = ψ(x) * exp(-iEt/ℏ)
                    phase = np.exp(1j * energy * t / 0.658)  # Using ℏ ≈ 0.658 eV·fs
                    psi_real = np.real(psi * phase)
                    psi_imag = np.imag(psi * phase)

                    frame_data = [
                        go.Scatter(
                            x=x, y=psi_real,
                            mode='lines',
                            line=dict(color='#3b82f6', width=3),
                            name='Re[ψ(x,t)]',
                            hovertemplate='x: %{x:.3f}<br>ψ: %{y:.3f}<extra></extra>'
                        ),
                        go.Scatter(
                            x=x, y=psi_imag,
                            mode='lines',
                            line=dict(color='#ef4444', width=3, dash='dash'),
                            name='Im[ψ(x,t)]',
                            hovertemplate='x: %{x:.3f}<br>ψ: %{y:.3f}<extra></extra>'
                        )
                    ]

                    frames.append(go.Frame(data=frame_data, name=str(frame)))

                # Initial frame
                fig.add_traces(frames[0].data, rows=1, cols=1)
                fig.frames = frames

                # Add animation controls
                fig.update_layout(
                    updatemenus=[{
                        'type': 'buttons',
                        'showactive': False,
                        'x': 0.1,
                        'y': 1.15,
                        'buttons': [
                            {
                                'label': '▶️ Play',
                                'method': 'animate',
                                'args': [None, {
                                    'frame': {'duration': 100, 'redraw': True},
                                    'fromcurrent': True,
                                    'transition': {'duration': 50},
                                    'mode': 'immediate'
                                }]
                            },
                            {
                                'label': '⏸️ Pause',
                                'method': 'animate',
                                'args': [[None], {
                                    'frame': {'duration': 0, 'redraw': False},
                                    'mode': 'immediate',
                                    'transition': {'duration': 0}
                                }]
                            }
                        ]
                    }]
                )
            else:
                # Static wave function
                fig.add_trace(
                    go.Scatter(
                        x=x, y=np.real(psi),
                        mode='lines',
                        line=dict(color='#3b82f6', width=3),
                        name='ψ(x)',
                        hovertemplate='x: %{x:.3f}<br>ψ: %{y:.3f}<extra></extra>'
                    ),
                    row=1, col=1
                )

            # Probability density plot
            if show_probability:
                fig.add_trace(
                    go.Scatter(
                        x=x, y=probability,
                        mode='lines',
                        line=dict(color='#8b5cf6', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(139, 92, 246, 0.3)',
                        name='|ψ(x)|²',
                        hovertemplate='x: %{x:.3f}<br>|ψ|²: %{y:.3f}<extra></extra>'
                    ),
                    row=2, col=1
                )

                # Add classical probability if requested
                if show_classical and classical_prob is not None:
                    fig.add_trace(
                        go.Scatter(
                            x=x, y=classical_prob,
                            mode='lines',
                            line=dict(color='#f59e0b', width=3, dash='dot'),
                            name='Classical',
                            hovertemplate='x: %{x:.3f}<br>P_classical: %{y:.3f}<extra></extra>'
                        ),
                        row=2, col=1
                    )

            # Add quantum nodes (zeros)
            if quantum_system == "Particle in a Box" and quantum_number > 1:
                nodes = [i * box_length / quantum_number for i in range(1, quantum_number)]
                for node in nodes:
                    fig.add_vline(
                        x=node,
                        line=dict(color='red', width=2, dash='dash'),
                        annotation_text=f"Node",
                        row=1, col=1
                    )

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>{title}</b><br>'
                         f'<span style="font-size:14px;">Energy: {energy:.3f} eV</span>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                height=600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 15, 35, 0.9)'
            )

            fig.update_xaxes(title_text=x_label, row=1, col=1, color='white')
            fig.update_yaxes(title_text="ψ(x)", row=1, col=1, color='white')
            fig.update_xaxes(title_text=x_label, row=2, col=1, color='white')
            fig.update_yaxes(title_text="|ψ(x)|²", row=2, col=1, color='white')

            return fig

        wave_fig = create_quantum_wave_visualization()
        st.plotly_chart(wave_fig, use_container_width=True)

        # Quantum mechanics dashboard
        st.markdown("#### 📊 Quantum Mechanics Dashboard")

        # Calculate quantum properties
        uncertainty = 1.0  # Simplified uncertainty calculation
        wavelength = 6.626e-34 / np.sqrt(2 * 9.109e-31 * energy * 1.602e-19) * 1e9  # de Broglie wavelength in nm

        # Display quantum metrics
        q_col1, q_col2, q_col3, q_col4 = st.columns(4)

        with q_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{energy:.3f}</div>
                <div class="metric-label">Energy (eV)</div>
            </div>
            """, unsafe_allow_html=True)

        with q_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{wavelength:.2f}</div>
                <div class="metric-label">de Broglie λ (nm)</div>
            </div>
            """, unsafe_allow_html=True)

        with q_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{quantum_number}</div>
                <div class="metric-label">Quantum Number</div>
            </div>
            """, unsafe_allow_html=True)

        with q_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{uncertainty:.3f}</div>
                <div class="metric-label">Uncertainty (ℏ)</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: Enhanced Quantum States
with tabs[1]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🎯</span> Quantum States & Superposition
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore quantum superposition, spin states, and the bizarre world of quantum mechanics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🎯</span> Quantum State Parameters")

        # Qubit state controls
        st.markdown("**Qubit State |ψ⟩ = α|0⟩ + β|1⟩:**")
        alpha_real = st.slider("α (real part)", -1.0, 1.0, 1.0, 0.01)
        alpha_imag = st.slider("α (imaginary part)", -1.0, 1.0, 0.0, 0.01)
        beta_real = st.slider("β (real part)", -1.0, 1.0, 0.0, 0.01)
        beta_imag = st.slider("β (imaginary part)", -1.0, 1.0, 0.0, 0.01)

        # Normalize the state
        alpha = complex(alpha_real, alpha_imag)
        beta = complex(beta_real, beta_imag)
        norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
        if norm > 0:
            alpha = alpha / norm
            beta = beta / norm

        st.markdown("**Measurement Basis:**")
        measurement_basis = st.selectbox("Basis", ["Computational (Z)", "Hadamard (X)", "Circular (Y)"])

        # Bloch sphere controls
        st.markdown("**Bloch Sphere Visualization:**")
        show_trajectory = st.checkbox("Show Evolution Trajectory", value=False)
        animate_rotation = st.checkbox("Animate Precession", value=True)

        # Calculate state properties
        prob_0 = abs(alpha)**2
        prob_1 = abs(beta)**2

        st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>State Properties:</strong><br>
            |0⟩ probability: {prob_0:.3f}<br>
            |1⟩ probability: {prob_1:.3f}<br>
            <strong>Normalization:</strong> {abs(alpha)**2 + abs(beta)**2:.3f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced Bloch sphere visualization
        def create_bloch_sphere():
            # Calculate Bloch vector components
            # |ψ⟩ = α|0⟩ + β|1⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

            # Extract angles from complex amplitudes
            if abs(alpha) > 1e-10:
                theta = 2 * np.arccos(abs(alpha))
                if abs(beta) > 1e-10:
                    phi = np.angle(beta) - np.angle(alpha)
                else:
                    phi = 0
            else:
                theta = np.pi
                phi = np.angle(beta) if abs(beta) > 1e-10 else 0

            # Bloch vector
            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)

            fig = go.Figure()

            # Draw Bloch sphere
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x_sphere = np.outer(np.cos(u), np.sin(v))
            y_sphere = np.outer(np.sin(u), np.sin(v))
            z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

            fig.add_trace(go.Surface(
                x=x_sphere, y=y_sphere, z=z_sphere,
                colorscale=[[0, 'rgba(139, 92, 246, 0.1)'], [1, 'rgba(139, 92, 246, 0.2)']],
                showscale=False,
                name='Bloch Sphere',
                opacity=0.3
            ))

            # Draw coordinate axes
            axes_length = 1.2

            # X-axis
            fig.add_trace(go.Scatter3d(
                x=[-axes_length, axes_length], y=[0, 0], z=[0, 0],
                mode='lines',
                line=dict(color='red', width=4),
                name='X-axis',
                showlegend=False
            ))

            # Y-axis
            fig.add_trace(go.Scatter3d(
                x=[0, 0], y=[-axes_length, axes_length], z=[0, 0],
                mode='lines',
                line=dict(color='green', width=4),
                name='Y-axis',
                showlegend=False
            ))

            # Z-axis
            fig.add_trace(go.Scatter3d(
                x=[0, 0], y=[0, 0], z=[-axes_length, axes_length],
                mode='lines',
                line=dict(color='blue', width=4),
                name='Z-axis',
                showlegend=False
            ))

            # Add axis labels
            fig.add_trace(go.Scatter3d(
                x=[axes_length], y=[0], z=[0],
                mode='text',
                text=['|+⟩'],
                textfont=dict(size=16, color='white'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter3d(
                x=[0], y=[axes_length], z=[0],
                mode='text',
                text=['|i⟩'],
                textfont=dict(size=16, color='white'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[axes_length],
                mode='text',
                text=['|0⟩'],
                textfont=dict(size=16, color='white'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[-axes_length],
                mode='text',
                text=['|1⟩'],
                textfont=dict(size=16, color='white'),
                showlegend=False
            ))

            # Draw state vector
            fig.add_trace(go.Scatter3d(
                x=[0, x], y=[0, y], z=[0, z],
                mode='lines+markers',
                line=dict(color='yellow', width=8),
                marker=dict(size=12, color='yellow'),
                name='|ψ⟩',
                hovertemplate=f'State Vector<br>θ: {np.degrees(theta):.1f}°<br>φ: {np.degrees(phi):.1f}°<extra></extra>'
            ))

            # Add trajectory if requested
            if show_trajectory:
                # Create a precession trajectory
                t_vals = np.linspace(0, 2*np.pi, 100)
                traj_x = np.sin(theta) * np.cos(phi + t_vals * 0.1)
                traj_y = np.sin(theta) * np.sin(phi + t_vals * 0.1)
                traj_z = np.full_like(t_vals, z)

                fig.add_trace(go.Scatter3d(
                    x=traj_x, y=traj_y, z=traj_z,
                    mode='lines',
                    line=dict(color='orange', width=3, dash='dot'),
                    name='Trajectory',
                    showlegend=False
                ))

            fig.update_layout(
                title=dict(
                    text=f'<b>Bloch Sphere Representation</b><br>'
                         f'<span style="font-size:14px;">|ψ⟩ = {alpha:.3f}|0⟩ + {beta:.3f}|1⟩</span>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                scene=dict(
                    xaxis=dict(title='X', range=[-1.5, 1.5], color='white'),
                    yaxis=dict(title='Y', range=[-1.5, 1.5], color='white'),
                    zaxis=dict(title='Z', range=[-1.5, 1.5], color='white'),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                    bgcolor='rgba(15, 15, 35, 0.9)',
                    aspectmode='cube'
                ),
                height=500,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 15, 35, 0.9)'
            )

            return fig

        bloch_fig = create_bloch_sphere()
        st.plotly_chart(bloch_fig, use_container_width=True)

        # Quantum state analysis
        st.markdown("#### 📊 Quantum State Analysis")

        # Calculate quantum information measures
        # Von Neumann entropy
        p0, p1 = abs(alpha)**2, abs(beta)**2
        if p0 > 0 and p1 > 0:
            entropy = -p0 * np.log2(p0) - p1 * np.log2(p1)
        else:
            entropy = 0

        # Purity
        purity = p0**2 + p1**2

        # Concurrence (for single qubit, always 0)
        concurrence = 0

        # Fidelity with |0⟩ state
        fidelity_0 = abs(alpha)**2

        # Display quantum metrics
        qs_col1, qs_col2, qs_col3, qs_col4 = st.columns(4)

        with qs_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{entropy:.3f}</div>
                <div class="metric-label">Entropy (bits)</div>
            </div>
            """, unsafe_allow_html=True)

        with qs_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{purity:.3f}</div>
                <div class="metric-label">Purity</div>
            </div>
            """, unsafe_allow_html=True)

        with qs_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fidelity_0:.3f}</div>
                <div class="metric-label">Fidelity |0⟩</div>
            </div>
            """, unsafe_allow_html=True)

        with qs_col4:
            coherence = 2 * abs(alpha * np.conj(beta))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{coherence:.3f}</div>
                <div class="metric-label">Coherence</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Quantum Entanglement
with tabs[2]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🔗</span> Quantum Entanglement & Bell States
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Bell State Parameters")

        bell_state = st.selectbox("Bell State", [
            "|Φ⁺⟩ = (|00⟩ + |11⟩)/√2",
            "|Φ⁻⟩ = (|00⟩ - |11⟩)/√2", 
            "|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2",
            "|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2"
        ])

        measurement_basis_A = st.selectbox("Alice's Basis", ["Z", "X", "Y"])
        measurement_basis_B = st.selectbox("Bob's Basis", ["Z", "X", "Y"])
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Bell state correlations
        def create_bell_correlations():
            angles = np.linspace(0, 2*np.pi, 100)
            
            # CHSH correlation function
            correlation = np.cos(2 * angles)
            quantum_bound = 2 * np.sqrt(2)
            classical_bound = 2
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=angles * 180/np.pi, y=correlation,
                mode='lines',
                name='Quantum Correlation',
                line=dict(color='#8b5cf6', width=4)
            ))
            
            fig.add_hline(y=quantum_bound, line_dash="dash", line_color="red",
                         annotation_text="Quantum Bound (2√2)")
            fig.add_hline(y=classical_bound, line_dash="dot", line_color="orange",
                         annotation_text="Classical Bound (2)")
            
            fig.update_layout(
                title="Bell Inequality Violation (CHSH)",
                xaxis_title="Measurement Angle (degrees)",
                yaxis_title="Correlation",
                height=400,
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 15, 35, 0.9)'
            )
            
            return fig

        bell_fig = create_bell_correlations()
        st.plotly_chart(bell_fig, use_container_width=True)

# Tab 4: Quantum Tunneling
with tabs[3]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🚇</span> Quantum Tunneling & Barrier Penetration
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Tunneling Parameters")

        barrier_height = st.slider("Barrier Height (eV)", 1.0, 10.0, 5.0, 0.5)
        barrier_width = st.slider("Barrier Width (nm)", 0.1, 2.0, 1.0, 0.1)
        particle_energy = st.slider("Particle Energy (eV)", 0.1, 8.0, 3.0, 0.1)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Quantum tunneling visualization
        def create_tunneling_plot():
            x = np.linspace(-3, 5, 1000)
            
            # Potential barrier
            V = np.where((x >= 0) & (x <= barrier_width), barrier_height, 0)
            
            # Wave function calculation (simplified)
            k1 = np.sqrt(2 * 9.109e-31 * particle_energy * 1.602e-19) / 1.055e-34 * 1e-9
            k2 = np.sqrt(2 * 9.109e-31 * (barrier_height - particle_energy) * 1.602e-19) / 1.055e-34 * 1e-9 if barrier_height > particle_energy else k1
            
            # Transmission coefficient
            if barrier_height > particle_energy:
                T = 1 / (1 + (barrier_height - particle_energy)**2 / (4 * particle_energy * (barrier_height - particle_energy)) * np.sinh(k2 * barrier_width)**2)
            else:
                T = 1.0
                
            R = 1 - T
            
            # Wave function
            psi_real = np.zeros_like(x)
            psi_real[x < 0] = np.cos(k1 * x[x < 0]) + R * np.cos(k1 * x[x < 0] + np.pi)
            psi_real[(x >= 0) & (x <= barrier_width)] = np.exp(-k2 * x[(x >= 0) & (x <= barrier_width)])
            psi_real[x > barrier_width] = T * np.cos(k1 * (x[x > barrier_width] - barrier_width))
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Potential Barrier & Wave Function', 'Transmission Probability'),
                vertical_spacing=0.15
            )
            
            # Potential and wave function
            fig.add_trace(go.Scatter(x=x, y=V, mode='lines', name='Potential', line=dict(color='red', width=3)), row=1, col=1)
            fig.add_trace(go.Scatter(x=x, y=psi_real**2 + particle_energy, mode='lines', name='|ψ|²', line=dict(color='blue', width=2)), row=1, col=1)
            fig.add_hline(y=particle_energy, line_dash="dash", annotation_text="Particle Energy", row=1, col=1)
            
            # Transmission vs energy
            energies = np.linspace(0.1, 10, 100)
            transmissions = []
            for E in energies:
                if barrier_height > E:
                    k2_temp = np.sqrt(2 * 9.109e-31 * (barrier_height - E) * 1.602e-19) / 1.055e-34 * 1e-9
                    T_temp = 1 / (1 + (barrier_height - E)**2 / (4 * E * (barrier_height - E)) * np.sinh(k2_temp * barrier_width)**2)
                else:
                    T_temp = 1.0
                transmissions.append(T_temp)
            
            fig.add_trace(go.Scatter(x=energies, y=transmissions, mode='lines', name='T(E)', line=dict(color='green', width=3)), row=2, col=1)
            fig.add_vline(x=particle_energy, line_dash="dot", annotation_text=f"Current E", row=2, col=1)
            
            fig.update_layout(height=600, title=f"Quantum Tunneling (T = {T:.3f}, R = {R:.3f})",
                            plot_bgcolor='rgba(30, 41, 59, 0.9)', paper_bgcolor='rgba(15, 15, 35, 0.9)')
            
            return fig

        tunneling_fig = create_tunneling_plot()
        st.plotly_chart(tunneling_fig, use_container_width=True)

# Tab 5: Quantum Measurement
with tabs[4]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🎲</span> Quantum Measurement & State Collapse
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Measurement Setup")

        num_measurements = st.slider("Number of Measurements", 10, 1000, 100, 10)
        measurement_type = st.selectbox("Measurement Type", ["Projective", "POVM", "Weak Measurement"])
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Measurement statistics
        def create_measurement_stats():
            # Simulate measurement outcomes
            np.random.seed(42)
            prob_0 = abs(alpha)**2
            outcomes = np.random.choice([0, 1], size=num_measurements, p=[prob_0, 1-prob_0])
            
            # Running average
            running_avg = np.cumsum(outcomes) / np.arange(1, len(outcomes) + 1)
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Measurement Outcomes', 'Convergence to Born Rule'),
                vertical_spacing=0.15
            )
            
            # Histogram of outcomes
            fig.add_trace(go.Histogram(x=outcomes, nbinsx=2, name='Outcomes', marker_color='purple'), row=1, col=1)
            
            # Running average
            fig.add_trace(go.Scatter(x=list(range(1, num_measurements+1)), y=running_avg, 
                                   mode='lines', name='Running Average', line=dict(color='blue', width=2)), row=2, col=1)
            fig.add_hline(y=1-prob_0, line_dash="dash", annotation_text=f"Theoretical: {1-prob_0:.3f}", row=2, col=1)
            
            fig.update_layout(height=500, title=f"Quantum Measurement Statistics ({num_measurements} trials)",
                            plot_bgcolor='rgba(30, 41, 59, 0.9)', paper_bgcolor='rgba(15, 15, 35, 0.9)')
            
            return fig

        measurement_fig = create_measurement_stats()
        st.plotly_chart(measurement_fig, use_container_width=True)

# Tab 6: Quantum Computing
with tabs[5]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🧮</span> Quantum Computing & Algorithms
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Quantum Circuit")

        num_qubits = st.slider("Number of Qubits", 1, 4, 2, 1)
        algorithm = st.selectbox("Algorithm", ["Quantum Fourier Transform", "Grover's Search", "Bell State Creation"])
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Quantum circuit visualization
        def create_quantum_circuit():
            fig = go.Figure()
            
            # Draw qubit lines
            for i in range(num_qubits):
                fig.add_trace(go.Scatter(x=[0, 10], y=[i, i], mode='lines', 
                                       line=dict(color='white', width=2), 
                                       name=f'Qubit {i}', showlegend=False))
            
            # Add gates based on algorithm
            if algorithm == "Bell State Creation" and num_qubits >= 2:
                # Hadamard gate on qubit 0
                fig.add_shape(type="rect", x0=2, y0=-0.2, x1=3, y1=0.2, 
                            fillcolor="yellow", line=dict(color="black"))
                fig.add_annotation(x=2.5, y=0, text="H", showarrow=False, font=dict(size=16))
                
                # CNOT gate
                fig.add_trace(go.Scatter(x=[4, 4], y=[0, 1], mode='lines+markers',
                                       line=dict(color='red', width=3),
                                       marker=dict(size=[8, 12], symbol=['circle', 'cross']),
                                       showlegend=False))
            
            fig.update_layout(
                title=f"{algorithm} Circuit ({num_qubits} qubits)",
                xaxis=dict(range=[-0.5, 10.5], showticklabels=False),
                yaxis=dict(range=[-0.5, num_qubits-0.5], showticklabels=False),
                height=300,
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 15, 35, 0.9)'
            )
            
            return fig

        circuit_fig = create_quantum_circuit()
        st.plotly_chart(circuit_fig, use_container_width=True)

with tabs[6]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🎓</span> Quantum Physics Learning Hub
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Comprehensive quantum mechanics resources, problem solving tools, and advanced concepts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced learning hub with interactive content
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="quantum-card">
            <h4 style="color: white; margin-bottom: 1rem;">📚 Quantum Fundamentals</h4>
            <div style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                <strong>Core Principles:</strong><br>
                • Wave-particle duality<br>
                • Heisenberg uncertainty principle<br>
                • Quantum superposition<br>
                • Wave function collapse<br><br>
                
                <strong>Mathematical Framework:</strong><br>
                • Schrödinger equation solutions<br>
                • Operator formalism<br>
                • Commutation relations<br>
                • Quantum observables
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive quantum calculator
        st.markdown("""
        <div class="quantum-card">
            <h4 style="color: white; margin-bottom: 1rem;">🧮 Quantum Calculator</h4>
            <div style="color: rgba(255,255,255,0.9);">
                <strong>Uncertainty Principle Calculator:</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Uncertainty principle calculator
        calculation_type = st.selectbox("Calculation", [
            "Position-Momentum Uncertainty",
            "Energy-Time Uncertainty", 
            "Angular Momentum",
            "Spin Measurements"
        ])

        if calculation_type == "Position-Momentum Uncertainty":
            sigma_x = st.number_input("Position Uncertainty Δx (nm)", value=1.0, min_value=0.01)
            
            # Calculate minimum momentum uncertainty
            hbar = 1.055e-34  # J⋅s
            delta_p_min = hbar / (2 * sigma_x * 1e-9)  # kg⋅m/s
            
            # Convert to more convenient units
            delta_p_min_eV = delta_p_min * 3e8 / 1.602e-19 * 1e-9  # eV/c
            
            st.markdown(f"""
            <div style="background: rgba(139, 92, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Uncertainty Relation:</strong><br>
                Δx⋅Δp ≥ ℏ/2<br><br>
                <strong>Results:</strong><br>
                Δp_min = {delta_p_min:.2e} kg⋅m/s<br>
                Δp_min = {delta_p_min_eV:.2f} eV/c<br>
                ΔxΔp = {sigma_x * delta_p_min_eV:.2f} eV⋅nm/c
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="quantum-card">
            <h4 style="color: white; margin-bottom: 1rem;">⚛️ Quantum Phenomena</h4>
            <div style="color: rgba(255,255,255,0.9); line-height: 1.6;">
                <strong>Key Phenomena:</strong><br>
                • Quantum tunneling<br>
                • Quantum interference<br>
                • Entanglement & nonlocality<br>
                • Decoherence effects<br><br>
                
                <strong>Applications:</strong><br>
                • Quantum computing<br>
                • Quantum cryptography<br>
                • Quantum sensing<br>
                • Quantum materials
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive problem solver
        st.markdown("""
        <div class="quantum-card">
            <h4 style="color: white; margin-bottom: 1rem;">🔬 Problem Solver</h4>
            <div style="color: rgba(255,255,255,0.9);">
                <strong>Quantum Mechanics Problems:</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        problem_type = st.selectbox("Problem Type", [
            "Particle in a Box",
            "Harmonic Oscillator",
            "Hydrogen Atom",
            "Quantum Tunneling"
        ])

        if problem_type == "Particle in a Box":
            box_length = st.number_input("Box Length (nm)", value=1.0, min_value=0.1)
            quantum_n = st.number_input("Quantum Number n", value=1, min_value=1)
            
            # Calculate energy levels
            mass_electron = 9.109e-31  # kg
            h = 6.626e-34  # J⋅s
            L = box_length * 1e-9  # m
            
            energy_joules = (quantum_n**2 * h**2) / (8 * mass_electron * L**2)
            energy_eV = energy_joules / 1.602e-19
            
            # Calculate wavelength
            momentum = quantum_n * h / (2 * L)
            wavelength = h / momentum * 1e9  # nm
            
            st.markdown(f"""
            <div style="background: rgba(34, 197, 94, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Solution:</strong><br>
                E_n = n²h²/(8mL²)<br><br>
                <strong>Results:</strong><br>
                Energy: {energy_eV:.3f} eV<br>
                Wavelength: {wavelength:.2f} nm<br>
                Momentum: {momentum:.2e} kg⋅m/s
            </div>
            """, unsafe_allow_html=True)

    # Enhanced quantum visualizations
    st.markdown("#### 📊 Interactive Quantum Demonstrations")

    # Create comprehensive quantum physics demonstration
    def create_quantum_demonstrations():
        # Create multiple quantum phenomena in one plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Quantum Wave Packets',
                'Probability Current Density', 
                'Quantum Interference Pattern',
                'Entangled State Evolution'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )

        # Wave packet demonstration
        x = np.linspace(-10, 10, 500)
        k0 = 1.0  # Central wave number
        sigma = 2.0  # Wave packet width
        
        # Gaussian wave packet
        psi_real = np.exp(-x**2/(4*sigma**2)) * np.cos(k0*x)
        psi_imag = np.exp(-x**2/(4*sigma**2)) * np.sin(k0*x)
        probability = psi_real**2 + psi_imag**2

        fig.add_trace(
            go.Scatter(
                x=x, y=psi_real,
                mode='lines',
                line=dict(color='#3b82f6', width=3),
                name='Re[ψ]',
                hovertemplate='x: %{x:.2f}<br>Re[ψ]: %{y:.3f}<extra></extra>'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=x, y=psi_imag,
                mode='lines',
                line=dict(color='#ef4444', width=3, dash='dash'),
                name='Im[ψ]',
                hovertemplate='x: %{x:.2f}<br>Im[ψ]: %{y:.3f}<extra></extra>'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=x, y=probability,
                mode='lines',
                line=dict(color='#8b5cf6', width=4),
                fill='tozeroy',
                fillcolor='rgba(139, 92, 246, 0.3)',
                name='|ψ|²',
                hovertemplate='x: %{x:.2f}<br>|ψ|²: %{y:.3f}<extra></extra>'
            ),
            row=1, col=1
        )

        # Probability current density
        hbar = 1.055e-34
        mass = 9.109e-31
        j_x = (hbar / (2j * mass)) * (psi_real * np.gradient(psi_imag, x) - psi_imag * np.gradient(psi_real, x))
        j_x = np.real(j_x)  # Take real part

        fig.add_trace(
            go.Scatter(
                x=x, y=j_x * 1e30,  # Scale for visibility
                mode='lines',
                line=dict(color='#10b981', width=4),
                name='Current Density',
                hovertemplate='x: %{x:.2f}<br>j: %{y:.2e}<extra></extra>'
            ),
            row=1, col=2
        )

        # Add arrow indicators for current flow
        arrow_positions = x[::50]
        arrow_values = j_x[::50] * 1e30
        for i, (pos, val) in enumerate(zip(arrow_positions, arrow_values)):
            if abs(val) > max(abs(arrow_values))*0.1:  # Only show significant currents
                fig.add_annotation(
                    x=pos, y=val,
                    ax=pos, ay=val + np.sign(val)*0.1,
                    arrowhead=2, arrowsize=1, arrowwidth=2,
                    arrowcolor='green',
                    showarrow=True,
                    row=1, col=2
                )

        # Quantum interference (double-slit-like)
        y = np.linspace(-5, 5, 200)
        slit_separation = 2.0
        screen_distance = 10.0
        wavelength = 1.0

        # Interference pattern
        phase_diff = 2 * np.pi * slit_separation * y / (wavelength * screen_distance)
        intensity = np.cos(phase_diff/2)**2

        fig.add_trace(
            go.Scatter(
                x=y, y=intensity,
                mode='lines',
                line=dict(color='#f59e0b', width=4),
                fill='tozeroy',
                fillcolor='rgba(245, 158, 11, 0.3)',
                name='Interference Pattern',
                hovertemplate='Position: %{x:.2f}<br>Intensity: %{y:.3f}<extra></extra>'
            ),
            row=2, col=1
        )

        # Mark interference maxima and minima
        maxima_pos = []
        minima_pos = []
        for i in range(len(y)-1):
            if intensity[i-1] < intensity[i] > intensity[i+1] and intensity[i] > 0.8:
                maxima_pos.append(y[i])
            elif intensity[i-1] > intensity[i] < intensity[i+1] and intensity[i] < 0.2:
                minima_pos.append(y[i])

        if maxima_pos:
            fig.add_trace(
                go.Scatter(
                    x=maxima_pos, y=[1]*len(maxima_pos),
                    mode='markers',
                    marker=dict(color='red', size=8, symbol='circle'),
                    name='Maxima',
                    showlegend=False
                ),
                row=2, col=1
            )

        # Entangled state evolution (Bell state)
        t_values = np.linspace(0, 2*np.pi, 100)
        
        # Bell state evolution on Bloch sphere (simplified projection)
        bloch_x = np.cos(t_values)
        bloch_y = np.sin(t_values)
        correlation = np.cos(2*t_values)  # Entanglement correlation

        fig.add_trace(
            go.Scatter(
                x=t_values, y=correlation,
                mode='lines',
                line=dict(color='#ec4899', width=4),
                name='Entanglement Correlation',
                hovertemplate='Time: %{x:.2f}<br>Correlation: %{y:.3f}<extra></extra>'
            ),
            row=2, col=2
        )

        # Add quantum correlation bounds
        fig.add_hline(y=1, line=dict(color='white', width=2, dash='dash'), 
                     annotation_text="Perfect Correlation", row=2, col=2)
        fig.add_hline(y=-1, line=dict(color='white', width=2, dash='dash'), 
                     annotation_text="Anti-Correlation", row=2, col=2)

        # Update layout with enhanced visibility
        fig.update_layout(
            title=dict(
                text='<b>Quantum Physics Demonstrations</b><br>'
                     '<span style="font-size:16px; color:#8b5cf6;">Interactive Quantum Phenomena</span>',
                x=0.5,
                font=dict(size=20, color='white', family='Inter')
            ),
            height=700,
            showlegend=True,
            legend=dict(x=1.02, y=1, font=dict(size=10)),
            plot_bgcolor='rgba(30, 41, 59, 0.9)',
            paper_bgcolor='rgba(15, 23, 42, 0.9)',
            annotations=[
                dict(
                    text="Advanced Quantum Mechanics",
                    x=0.5, y=1.02,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=14, color='#cbd5e1')
                )
            ]
        )

        # Update axes with better visibility
        fig.update_xaxes(title_text="Position", row=1, col=1, color='white')
        fig.update_yaxes(title_text="Wave Function", row=1, col=1, color='white')
        fig.update_xaxes(title_text="Position", row=1, col=2, color='white')
        fig.update_yaxes(title_text="Current Density", row=1, col=2, color='white')
        fig.update_xaxes(title_text="Screen Position", row=2, col=1, color='white')
        fig.update_yaxes(title_text="Intensity", row=2, col=1, color='white')
        fig.update_xaxes(title_text="Evolution Parameter", row=2, col=2, color='white')
        fig.update_yaxes(title_text="Quantum Correlation", row=2, col=2, color='white')

        return fig

    quantum_demo_fig = create_quantum_demonstrations()
    st.plotly_chart(quantum_demo_fig, use_container_width=True)

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
           border-radius: 15px; text-align: center; border: 1px solid #475569;">
    <h3 style="color: white; margin-bottom: 1rem;">⚛️ Quantum Physics Laboratory</h3>
    <p style="color: #cbd5e1; margin-bottom: 1.5rem;">
        Explore the fundamental mysteries of quantum mechanics through interactive simulations.
    </p>
</div>
""", unsafe_allow_html=True)