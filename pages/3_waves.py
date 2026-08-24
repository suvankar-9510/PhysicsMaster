
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import time
import math

st.set_page_config(
    page_title="Wave Physics Laboratory",
    page_icon="🌊",
    layout="wide"
)

# Enhanced CSS with modern wave-inspired design
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

    /* Wave-themed header with fluid animations */
    .wave-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #0284c7;
        box-shadow: 0 20px 40px rgba(2, 132, 199, 0.3);
    }

    .wave-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 200%;
        height: 100%;
        background: 
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 10px,
                rgba(255,255,255,0.05) 10px,
                rgba(255,255,255,0.05) 20px
            );
        animation: waveFlow 20s linear infinite;
    }

    @keyframes waveFlow {
        0% { transform: translateX(-50%); }
        100% { transform: translateX(0%); }
    }

    /* Enhanced section cards with wave effects */
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

    .physics-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #0ea5e9, #0284c7, #0369a1, #075985);
        animation: waveGradient 3s ease-in-out infinite;
    }

    @keyframes waveGradient {
        0%, 100% { background: linear-gradient(90deg, #0ea5e9, #0284c7, #0369a1, #075985); }
        25% { background: linear-gradient(90deg, #0284c7, #0369a1, #075985, #0ea5e9); }
        50% { background: linear-gradient(90deg, #0369a1, #075985, #0ea5e9, #0284c7); }
        75% { background: linear-gradient(90deg, #075985, #0ea5e9, #0284c7, #0369a1); }
    }

    /* Parameter panels */
    .param-panel {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #64748b;
        transition: all 0.3s ease;
    }

    .param-panel:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(100, 116, 139, 0.3);
        border-color: #0ea5e9;
    }

    /* Metric cards with wave animations */
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
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(14, 165, 233, 0.2);
        border-color: #0ea5e9;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0ea5e9;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 1rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    /* Wave visualization cards */
    .wave-card {
        background: linear-gradient(135deg, #0c4a6e 0%, #0ea5e9 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #0284c7;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .wave-card::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 20'%3E%3Cpath d='M0,10 Q25,0 50,10 T100,10 L100,20 L0,20 Z' fill='rgba(255,255,255,0.1)'/%3E%3C/svg%3E");
        background-size: 100px 20px;
        animation: waveMotion 4s ease-in-out infinite;
    }

    @keyframes waveMotion {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(-50px); }
    }

    /* Interactive elements */
    .interactive-icon {
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .interactive-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(14, 165, 233, 0.3));
    }

    /* Enhanced tabs */
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
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced wave-themed header
st.markdown("""
<div class="wave-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span class="interactive-icon">🌊</span> Wave Physics Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Explore Wave Mechanics & Oscillatory Phenomena
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Interference</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Standing Waves</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Wave Packets</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced tabs with comprehensive wave phenomena
tabs = st.tabs([
    "🌊 Wave Interference", 
    "📊 Standing Waves", 
    "📦 Wave Packets", 
    "🎵 Doppler Effect",
    "🔄 Wave Dispersion",
    "⚡ Electromagnetic Waves"
])

# Tab 1: Enhanced Wave Interference
with tabs[0]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🌊</span> Wave Interference & Superposition
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore how multiple waves combine to create complex interference patterns through superposition.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>⚙️</span> Wave Parameters")

        # Enhanced wave controls
        num_waves = st.selectbox("Number of Waves", [2, 3, 4, 5], index=0)
        
        waves_params = []
        for i in range(num_waves):
            st.markdown(f"**Wave {i+1}:**")
            col_a, col_b = st.columns(2)
            with col_a:
                amplitude = st.slider(f"Amplitude {i+1}", 0.1, 2.0, 1.0, 0.1, key=f"amp_{i}")
                frequency = st.slider(f"Frequency {i+1}", 0.5, 5.0, 1.0 + i*0.5, 0.1, key=f"freq_{i}")
            with col_b:
                phase = st.slider(f"Phase {i+1} (rad)", 0.0, 2*np.pi, i*np.pi/4, 0.1, key=f"phase_{i}")
                wavelength = st.slider(f"Wavelength {i+1}", 0.5, 3.0, 1.0 + i*0.2, 0.1, key=f"wave_{i}")
            
            waves_params.append({
                'amplitude': amplitude,
                'frequency': frequency,
                'phase': phase,
                'wavelength': wavelength
            })

        # Animation controls
        st.markdown("#### <span class='interactive-icon'>🎬</span> Animation")
        animate = st.checkbox("Real-time Animation", value=True)
        show_envelope = st.checkbox("Show Beat Envelope", value=False)
        show_components = st.checkbox("Show Individual Waves", value=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced wave interference visualization
        def create_wave_interference():
            x = np.linspace(0, 10, 1000)
            t = time.time() if animate else 0
            
            # Create subplots for better visualization
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Wave Interference Pattern', 'Spatial Wave Profile'),
                vertical_spacing=0.12,
                row_heights=[0.7, 0.3]
            )

            # Calculate superposition
            total_wave = np.zeros_like(x)
            colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
            
            for i, params in enumerate(waves_params):
                k = 2 * np.pi / params['wavelength']
                omega = 2 * np.pi * params['frequency']
                wave = params['amplitude'] * np.sin(k * x - omega * t + params['phase'])
                total_wave += wave
                
                if show_components:
                    fig.add_trace(
                        go.Scatter(
                            x=x, y=wave,
                            mode='lines',
                            name=f'Wave {i+1}',
                            line=dict(color=colors[i % len(colors)], width=2, dash='dot'),
                            opacity=0.7
                        ),
                        row=1, col=1
                    )

            # Add total wave
            fig.add_trace(
                go.Scatter(
                    x=x, y=total_wave,
                    mode='lines',
                    name='Superposition',
                    line=dict(color='white', width=4),
                    fill='tonexty' if not show_components else None,
                    fillcolor='rgba(14, 165, 233, 0.3)'
                ),
                row=1, col=1
            )

            # Beat envelope if requested
            if show_envelope and num_waves == 2:
                envelope = waves_params[0]['amplitude'] + waves_params[1]['amplitude']
                envelope_upper = envelope * np.ones_like(x)
                envelope_lower = -envelope * np.ones_like(x)
                
                fig.add_trace(
                    go.Scatter(
                        x=x, y=envelope_upper,
                        mode='lines',
                        name='Beat Envelope',
                        line=dict(color='yellow', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=x, y=envelope_lower,
                        mode='lines',
                        line=dict(color='yellow', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=1, col=1
                )

            # Frequency spectrum
            frequencies = [params['frequency'] for params in waves_params]
            amplitudes = [params['amplitude'] for params in waves_params]
            
            fig.add_trace(
                go.Bar(
                    x=frequencies,
                    y=amplitudes,
                    name='Frequency Spectrum',
                    marker_color='rgba(14, 165, 233, 0.7)'
                ),
                row=2, col=1
            )

            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>Wave Interference ({num_waves} waves)</b>',
                    x=0.5,
                    font=dict(size=18, color='white')
                ),
                height=600,
                showlegend=True,
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            # Update axes
            fig.update_xaxes(title_text="Position", row=1, col=1, color='white')
            fig.update_yaxes(title_text="Amplitude", row=1, col=1, color='white')
            fig.update_xaxes(title_text="Frequency", row=2, col=1, color='white')
            fig.update_yaxes(title_text="Amplitude", row=2, col=1, color='white')

            return fig

        interference_fig = create_wave_interference()
        st.plotly_chart(interference_fig, use_container_width=True)

        # Wave metrics dashboard
        st.markdown("#### 📊 Wave Analysis")
        
        # Calculate wave properties
        total_amplitude = sum([params['amplitude'] for params in waves_params])
        avg_frequency = np.mean([params['frequency'] for params in waves_params])
        avg_wavelength = np.mean([params['wavelength'] for params in waves_params])
        
        # Beat frequency for two waves
        if num_waves == 2:
            beat_freq = abs(waves_params[0]['frequency'] - waves_params[1]['frequency'])
        else:
            beat_freq = 0

        wave_col1, wave_col2, wave_col3, wave_col4 = st.columns(4)

        with wave_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_amplitude:.2f}</div>
                <div class="metric-label">Max Amplitude</div>
            </div>
            """, unsafe_allow_html=True)

        with wave_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_frequency:.2f}</div>
                <div class="metric-label">Avg Frequency</div>
            </div>
            """, unsafe_allow_html=True)

        with wave_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_wavelength:.2f}</div>
                <div class="metric-label">Avg Wavelength</div>
            </div>
            """, unsafe_allow_html=True)

        with wave_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{beat_freq:.2f}</div>
                <div class="metric-label">Beat Frequency</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: Standing Waves
with tabs[1]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">📊</span> Standing Wave Patterns
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Standing Wave Parameters")

        boundary_condition = st.selectbox("Boundary Conditions", 
                                        ["Fixed-Fixed", "Free-Free", "Fixed-Free"])
        string_length = st.slider("String Length (m)", 0.5, 5.0, 2.0, 0.1)
        mode_number = st.slider("Mode Number (n)", 1, 10, 1, 1)
        tension = st.slider("String Tension (N)", 10, 200, 100, 10)
        linear_density = st.slider("Linear Density (kg/m)", 0.001, 0.01, 0.005, 0.001)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Standing wave visualization
        def create_standing_wave():
            x = np.linspace(0, string_length, 500)
            t = np.linspace(0, 2, 60)
            
            # Wave speed
            wave_speed = np.sqrt(tension / linear_density)
            
            # Wavelength and frequency based on boundary conditions
            if boundary_condition == "Fixed-Fixed":
                wavelength = 2 * string_length / mode_number
                k = mode_number * np.pi / string_length
            elif boundary_condition == "Free-Free":
                wavelength = 2 * string_length / mode_number
                k = mode_number * np.pi / string_length
            else:  # Fixed-Free
                wavelength = 4 * string_length / (2 * mode_number - 1)
                k = (2 * mode_number - 1) * np.pi / (2 * string_length)
            
            frequency = wave_speed / wavelength

            # Create animation frames
            frames = []
            for t_val in t:
                if boundary_condition == "Fixed-Fixed":
                    y = np.sin(k * x) * np.cos(2 * np.pi * frequency * t_val)
                elif boundary_condition == "Free-Free":
                    y = np.cos(k * x) * np.cos(2 * np.pi * frequency * t_val)
                else:  # Fixed-Free
                    y = np.cos(k * x) * np.cos(2 * np.pi * frequency * t_val)

                frame = go.Frame(
                    data=[
                        go.Scatter(
                            x=x, y=y,
                            mode='lines',
                            line=dict(color='#0ea5e9', width=4),
                            name='Standing Wave'
                        )
                    ],
                    name=str(t_val)
                )
                frames.append(frame)

            # Create figure with animation
            fig = go.Figure(
                data=frames[0].data,
                frames=frames
            )

            # Add nodes and antinodes
            if boundary_condition == "Fixed-Fixed":
                node_positions = [i * string_length / mode_number for i in range(mode_number + 1)]
                antinode_positions = [(i + 0.5) * string_length / mode_number 
                                    for i in range(mode_number)]
            
            for pos in node_positions:
                fig.add_vline(x=pos, line=dict(color='red', width=2, dash='dash'),
                            annotation_text="Node")
            
            for pos in antinode_positions:
                fig.add_vline(x=pos, line=dict(color='green', width=2, dash='dot'),
                            annotation_text="Antinode")

            # Add animation controls
            fig.update_layout(
                title=f'Standing Wave - {boundary_condition} (Mode {mode_number})',
                xaxis_title='Position (m)',
                yaxis_title='Displacement',
                yaxis_range=[-1.5, 1.5],
                height=400,
                updatemenus=[{
                    'type': 'buttons',
                    'showactive': False,
                    'buttons': [{
                        'label': '▶️ Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 100, 'redraw': True}}]
                    }]
                }],
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            return fig

        standing_fig = create_standing_wave()
        st.plotly_chart(standing_fig, use_container_width=True)

# Tab 3: Wave Packets
with tabs[2]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">📦</span> Wave Packets & Group Velocity
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Wave Packet Parameters")

        central_freq = st.slider("Central Frequency", 1.0, 10.0, 5.0, 0.5)
        bandwidth = st.slider("Frequency Bandwidth", 0.1, 2.0, 0.5, 0.1)
        envelope_type = st.selectbox("Envelope Type", ["Gaussian", "Rectangular", "Exponential"])
        dispersion = st.slider("Dispersion Parameter", 0.0, 1.0, 0.1, 0.05)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Wave packet visualization
        def create_wave_packet():
            x = np.linspace(-20, 20, 1000)
            t = np.linspace(0, 4, 50)
            
            # Create animation frames
            frames = []
            for t_val in t:
                if envelope_type == "Gaussian":
                    envelope = np.exp(-(x - 5*t_val)**2 / (2*(1/bandwidth)**2))
                elif envelope_type == "Rectangular":
                    envelope = np.where(np.abs(x - 5*t_val) < 1/bandwidth, 1, 0)
                else:  # Exponential
                    envelope = np.exp(-np.abs(x - 5*t_val) * bandwidth)
                
                # Include dispersion
                k = central_freq + dispersion * (x - 5*t_val)**2
                carrier = np.cos(k * x - central_freq * t_val)
                wave_packet = envelope * carrier

                frame = go.Frame(
                    data=[
                        go.Scatter(
                            x=x, y=envelope,
                            mode='lines',
                            line=dict(color='red', width=2, dash='dash'),
                            name='Envelope'
                        ),
                        go.Scatter(
                            x=x, y=-envelope,
                            mode='lines',
                            line=dict(color='red', width=2, dash='dash'),
                            showlegend=False
                        ),
                        go.Scatter(
                            x=x, y=wave_packet,
                            mode='lines',
                            line=dict(color='#0ea5e9', width=3),
                            name='Wave Packet'
                        )
                    ],
                    name=str(t_val)
                )
                frames.append(frame)

            fig = go.Figure(
                data=frames[0].data,
                frames=frames
            )

            fig.update_layout(
                title=f'{envelope_type} Wave Packet (f₀={central_freq} Hz)',
                xaxis_title='Position',
                yaxis_title='Amplitude',
                height=400,
                updatemenus=[{
                    'type': 'buttons',
                    'showactive': False,
                    'buttons': [{
                        'label': '▶️ Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 100, 'redraw': True}}]
                    }]
                }],
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            return fig

        packet_fig = create_wave_packet()
        st.plotly_chart(packet_fig, use_container_width=True)

# Tab 4: Doppler Effect
with tabs[3]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🎵</span> Doppler Effect Simulation
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### Doppler Parameters")

        source_velocity = st.slider("Source Velocity (m/s)", -50, 50, 0, 1)
        observer_velocity = st.slider("Observer Velocity (m/s)", -50, 50, 0, 1)
        source_frequency = st.slider("Source Frequency (Hz)", 100, 1000, 440, 10)
        wave_speed = st.slider("Wave Speed (m/s)", 300, 400, 343, 1)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Doppler effect visualization
        def create_doppler_visualization():
            # Calculate observed frequency
            observed_freq = source_frequency * (wave_speed + observer_velocity) / (wave_speed + source_velocity)
            
            # Create wavefront visualization
            fig = go.Figure()
            
            # Source position over time
            time_points = np.linspace(0, 5, 20)
            for i, t in enumerate(time_points):
                source_pos = source_velocity * t
                
                # Wavefronts
                for j in range(5):
                    wavefront_time = t - j
                    if wavefront_time > 0:
                        radius = wave_speed * wavefront_time
                        theta = np.linspace(0, 2*np.pi, 100)
                        x_wave = source_pos + radius * np.cos(theta)
                        y_wave = radius * np.sin(theta)
                        
                        fig.add_trace(go.Scatter(
                            x=x_wave, y=y_wave,
                            mode='lines',
                            line=dict(color=f'rgba(14, 165, 233, {0.8 - j*0.1})', width=2),
                            showlegend=False
                        ))

            # Source trajectory
            source_x = source_velocity * time_points
            fig.add_trace(go.Scatter(
                x=source_x, y=np.zeros_like(source_x),
                mode='markers+lines',
                marker=dict(color='red', size=8),
                line=dict(color='red', dash='dot'),
                name='Source Path'
            ))

            fig.update_layout(
                title=f'Doppler Effect (f₀={source_frequency} Hz → f_obs={observed_freq:.1f} Hz)',
                xaxis_title='Position (m)',
                yaxis_title='Position (m)',
                xaxis=dict(range=[-200, 200]),
                yaxis=dict(range=[-200, 200], scaleanchor="x", scaleratio=1),
                height=500,
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)'
            )

            return fig

        doppler_fig = create_doppler_visualization()
        st.plotly_chart(doppler_fig, use_container_width=True)

# Tab 4: Complete Wave Dispersion & Phase Velocity
with tabs[4]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🔄</span> Wave Dispersion & Phase Velocity
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Analyze dispersive media effects, group velocity, and wave packet spreading in various materials.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🔄</span> Dispersion Parameters")

        # Medium selection
        medium_type = st.selectbox("Dispersive Medium", [
            "Normal Dispersion (Glass)",
            "Anomalous Dispersion (Plasma)",
            "Ocean Waves (Deep Water)",
            "Quantum Mechanical Particle",
            "Optical Fiber",
            "Metamaterial"
        ])

        # Dispersion parameters
        carrier_frequency = st.slider("Carrier Frequency (THz)", 0.1, 10.0, 1.0, 0.1)
        bandwidth = st.slider("Wave Packet Bandwidth (THz)", 0.01, 1.0, 0.1, 0.01)
        propagation_distance = st.slider("Propagation Distance (km)", 0.1, 100.0, 10.0, 0.1)

        # Material-specific parameters
        if medium_type == "Normal Dispersion (Glass)":
            n0 = st.slider("Base Refractive Index", 1.4, 1.8, 1.5, 0.01)
            dispersion_param = st.slider("Dispersion Parameter (ps/nm/km)", 10, 30, 17, 1)
        elif medium_type == "Anomalous Dispersion (Plasma)":
            plasma_freq = st.slider("Plasma Frequency (THz)", 0.1, 5.0, 1.0, 0.1)
            collision_freq = st.slider("Collision Frequency (GHz)", 1, 100, 10, 1)
        else:
            n0 = 1.5
            dispersion_param = 17

        # Calculate dispersion relation
        def calculate_dispersion_relation(freq, medium):
            if medium == "Normal Dispersion (Glass)":
                # Sellmeier dispersion
                n = n0 + 0.01 / (1 - (freq/5)**2)
                return n
            elif medium == "Anomalous Dispersion (Plasma)":
                # Plasma dispersion
                wp = plasma_freq * 2 * np.pi * 1e12
                nu = collision_freq * 2 * np.pi * 1e9
                omega = freq * 2 * np.pi * 1e12
                epsilon = 1 - wp**2 / (omega**2 + 1j*nu*omega)
                return np.sqrt(epsilon)
            elif medium == "Ocean Waves (Deep Water)":
                # Deep water dispersion: ω² = gk
                g = 9.81
                omega = freq * 2 * np.pi
                k = omega**2 / g
                return omega / k  # Phase velocity
            else:
                return n0 * (1 + 0.01*freq)

        # Display medium properties
        n_carrier = calculate_dispersion_relation(carrier_frequency, medium_type)
        
        st.markdown(f"""
        <div style="background: rgba(14, 165, 233, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Medium Properties:</strong><br>
            Type: {medium_type}<br>
            n(f₀): {np.real(n_carrier):.4f}<br>
            Carrier: {carrier_frequency:.2f} THz<br>
            Distance: {propagation_distance:.1f} km
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced dispersion visualization
        def create_dispersion_analysis():
            # Frequency range for analysis
            freq_range = np.linspace(0.1, 2*carrier_frequency, 500)
            
            # Calculate refractive index vs frequency
            n_values = []
            for f in freq_range:
                n = calculate_dispersion_relation(f, medium_type)
                n_values.append(np.real(n))
            
            n_values = np.array(n_values)

            # Calculate group and phase velocities
            c = 3e8  # Speed of light
            phase_velocity = c / n_values
            
            # Group velocity: vg = c / (n - λ dn/dλ)
            dn_df = np.gradient(n_values, freq_range)
            group_velocity = c / (n_values - freq_range * dn_df * 1e12 / c)

            # Create comprehensive dispersion analysis
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Refractive Index vs Frequency',
                    'Phase & Group Velocity',
                    'Wave Packet Evolution',
                    'Dispersion-Induced Pulse Broadening'
                ),
                vertical_spacing=0.15,
                horizontal_spacing=0.1
            )

            # Refractive index plot with enhanced visibility
            fig.add_trace(
                go.Scatter(
                    x=freq_range, y=n_values,
                    mode='lines',
                    line=dict(color='#0ea5e9', width=4),
                    name='Refractive Index',
                    hovertemplate='f: %{x:.2f} THz<br>n: %{y:.4f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Mark carrier frequency
            n_carrier_real = np.real(calculate_dispersion_relation(carrier_frequency, medium_type))
            fig.add_trace(
                go.Scatter(
                    x=[carrier_frequency], y=[n_carrier_real],
                    mode='markers',
                    marker=dict(size=12, color='yellow', symbol='star'),
                    name='Carrier Frequency',
                    hovertemplate=f'f₀: {carrier_frequency:.2f} THz<br>n: {n_carrier_real:.4f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Velocity plot
            fig.add_trace(
                go.Scatter(
                    x=freq_range, y=phase_velocity/c,
                    mode='lines',
                    line=dict(color='#ef4444', width=3),
                    name='Phase Velocity',
                    hovertemplate='f: %{x:.2f} THz<br>vₚ/c: %{y:.4f}<extra></extra>'
                ),
                row=1, col=2
            )

            fig.add_trace(
                go.Scatter(
                    x=freq_range, y=group_velocity/c,
                    mode='lines',
                    line=dict(color='#10b981', width=3, dash='dash'),
                    name='Group Velocity',
                    hovertemplate='f: %{x:.2f} THz<br>vₒ/c: %{y:.4f}<extra></extra>'
                ),
                row=1, col=2
            )

            # Wave packet evolution
            x = np.linspace(0, propagation_distance, 100)
            t_values = [0, 0.25, 0.5, 0.75, 1.0]  # Normalized time steps
            
            for i, t_norm in enumerate(t_values):
                # Simplified wave packet with dispersion
                t_actual = t_norm * propagation_distance * 1000 / (c/n_carrier_real)  # Convert to seconds
                
                # Gaussian envelope with dispersion broadening
                sigma_initial = c / (2 * np.pi * bandwidth * 1e12)  # Initial pulse width
                beta2 = dispersion_param * 1e-27  # GVD parameter
                sigma_t = sigma_initial * np.sqrt(1 + (beta2 * propagation_distance * 1000 / sigma_initial**2)**2)
                
                # Wave packet at different times
                amplitude = np.exp(-(x - propagation_distance * t_norm)**2 / (2 * (sigma_t/1000)**2))
                
                fig.add_trace(
                    go.Scatter(
                        x=x, y=amplitude,
                        mode='lines',
                        line=dict(width=3, color=px.colors.sequential.Viridis[i*2]),
                        name=f't = {t_norm:.2f}T',
                        opacity=0.7,
                        hovertemplate='Distance: %{x:.1f} km<br>Amplitude: %{y:.3f}<extra></extra>'
                    ),
                    row=2, col=1
                )

            # Pulse broadening analysis
            distances = np.linspace(0, 100, 50)
            initial_width = 1.0  # ps
            broadened_widths = []
            
            for dist in distances:
                beta2 = dispersion_param * 1e-27
                broadening_factor = np.sqrt(1 + (beta2 * dist * 1000 / initial_width**2)**2)
                broadened_widths.append(initial_width * broadening_factor)

            fig.add_trace(
                go.Scatter(
                    x=distances, y=broadened_widths,
                    mode='lines',
                    line=dict(color='#f59e0b', width=4),
                    fill='tozeroy',
                    fillcolor='rgba(245, 158, 11, 0.3)',
                    name='Pulse Width',
                    hovertemplate='Distance: %{x:.1f} km<br>Width: %{y:.2f} ps<extra></extra>'
                ),
                row=2, col=2
            )

            # Mark current distance
            current_width = np.interp(propagation_distance, distances, broadened_widths)
            fig.add_trace(
                go.Scatter(
                    x=[propagation_distance], y=[current_width],
                    mode='markers',
                    marker=dict(size=12, color='red', symbol='diamond'),
                    name='Current Distance',
                    hovertemplate=f'Distance: {propagation_distance:.1f} km<br>Width: {current_width:.2f} ps<extra></extra>'
                ),
                row=2, col=2
            )

            # Update layout with enhanced visibility
            fig.update_layout(
                title=dict(
                    text=f'<b>Wave Dispersion Analysis: {medium_type}</b><br>'
                         f'<span style="font-size:16px; color:#0ea5e9;">f₀ = {carrier_frequency:.2f} THz, Distance = {propagation_distance:.1f} km</span>',
                    x=0.5,
                    font=dict(size=20, color='white', family='Inter')
                ),
                height=700,
                showlegend=True,
                legend=dict(x=1.02, y=1, font=dict(size=11)),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)',
                annotations=[
                    dict(
                        text="Advanced Dispersion Analysis",
                        x=0.5, y=1.02,
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=14, color='#cbd5e1')
                    )
                ]
            )

            # Update axes with better visibility
            fig.update_xaxes(title_text="Frequency (THz)", row=1, col=1, color='white')
            fig.update_yaxes(title_text="Refractive Index", row=1, col=1, color='white')
            fig.update_xaxes(title_text="Frequency (THz)", row=1, col=2, color='white')
            fig.update_yaxes(title_text="Velocity/c", row=1, col=2, color='white')
            fig.update_xaxes(title_text="Distance (km)", row=2, col=1, color='white')
            fig.update_yaxes(title_text="Amplitude", row=2, col=1, color='white')
            fig.update_xaxes(title_text="Distance (km)", row=2, col=2, color='white')
            fig.update_yaxes(title_text="Pulse Width (ps)", row=2, col=2, color='white')

            return fig

        dispersion_fig = create_dispersion_analysis()
        st.plotly_chart(dispersion_fig, use_container_width=True)

        # Dispersion metrics dashboard
        st.markdown("#### 📊 Dispersion Analysis Dashboard")

        # Calculate key dispersion parameters
        n_carrier_real = np.real(calculate_dispersion_relation(carrier_frequency, medium_type))
        phase_vel = 3e8 / n_carrier_real
        
        # Group velocity (simplified calculation)
        delta_f = 0.01  # THz
        n_plus = np.real(calculate_dispersion_relation(carrier_frequency + delta_f, medium_type))
        n_minus = np.real(calculate_dispersion_relation(carrier_frequency - delta_f, medium_type))
        dn_df = (n_plus - n_minus) / (2 * delta_f)
        group_vel = 3e8 / (n_carrier_real - carrier_frequency * dn_df * 1e12 / 3e8)

        # GVD parameter
        gvd = dispersion_param * 1e-27  # s²/m
        
        # Walk-off time
        walk_off = abs(1/group_vel - 1/phase_vel) * propagation_distance * 1000 * 1e12  # ps

        disp_col1, disp_col2, disp_col3, disp_col4 = st.columns(4)

        with disp_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{phase_vel/1e8:.2f}</div>
                <div class="metric-label">Phase Velocity (×10⁸ m/s)</div>
            </div>
            """, unsafe_allow_html=True)

        with disp_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{group_vel/1e8:.2f}</div>
                <div class="metric-label">Group Velocity (×10⁸ m/s)</div>
            </div>
            """, unsafe_allow_html=True)

        with disp_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{gvd*1e27:.1f}</div>
                <div class="metric-label">GVD (ps²/km)</div>
            </div>
            """, unsafe_allow_html=True)

        with disp_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{walk_off:.2f}</div>
                <div class="metric-label">Walk-off (ps)</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 5: Complete Electromagnetic Wave Propagation
with tabs[5]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">⚡</span> Electromagnetic Wave Propagation
        </h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore Maxwell's equations solutions with complete E and B field visualizations in various media.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>⚡</span> EM Wave Parameters")

        # Wave configuration
        wave_type = st.selectbox("Wave Type", [
            "Plane Wave (Free Space)",
            "Plane Wave (Dielectric)",
            "Plane Wave (Conductor)",
            "Spherical Wave",
            "Guided Wave (Waveguide)",
            "Evanescent Wave"
        ])

        # Field parameters
        frequency = st.slider("Frequency (GHz)", 0.1, 100.0, 10.0, 0.1)
        electric_amplitude = st.slider("Electric Field Amplitude (V/m)", 1.0, 1000.0, 100.0, 1.0)
        
        # Polarization
        polarization = st.selectbox("Polarization", [
            "Linear (x-direction)",
            "Linear (y-direction)", 
            "Circular (Right)",
            "Circular (Left)",
            "Elliptical"
        ])

        # Medium properties
        if "Dielectric" in wave_type:
            epsilon_r = st.slider("Relative Permittivity", 1.0, 10.0, 2.0, 0.1)
            mu_r = 1.0
            sigma = 0.0
        elif "Conductor" in wave_type:
            epsilon_r = 1.0
            mu_r = 1.0
            sigma = st.slider("Conductivity (S/m)", 1e4, 1e8, 1e6, format="%.0e")
        else:
            epsilon_r = 1.0
            mu_r = 1.0
            sigma = 0.0

        # Calculate wave properties
        omega = 2 * np.pi * frequency * 1e9  # rad/s
        epsilon_0 = 8.854e-12  # F/m
        mu_0 = 4*np.pi*1e-7  # H/m
        c = 1/np.sqrt(epsilon_0 * mu_0)

        # Wave vector and impedance
        if sigma > 0:  # Conducting medium
            epsilon_complex = epsilon_r * epsilon_0 - 1j * sigma / omega
            k = omega * np.sqrt(mu_r * mu_0 * epsilon_complex)
            impedance = np.sqrt(mu_r * mu_0 / epsilon_complex)
        else:  # Dielectric
            k = omega * np.sqrt(epsilon_r * mu_r) / c
            impedance = np.sqrt(mu_r * mu_0 / (epsilon_r * epsilon_0))

        wavelength = 2 * np.pi / np.real(k)
        skin_depth = 1 / np.imag(k) if np.imag(k) > 0 else float('inf')

        st.markdown(f"""
        <div style="background: rgba(14, 165, 233, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Wave Properties:</strong><br>
            λ: {wavelength*1000:.2f} mm<br>
            |Z|: {abs(impedance):.1f} Ω<br>
            δ: {skin_depth*1000:.2f} mm<br>
            Type: {wave_type.split('(')[0]}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced EM wave visualization
        def create_em_wave_visualization():
            # Spatial and temporal grids
            z = np.linspace(0, 4*wavelength, 200)
            t = np.linspace(0, 2*np.pi/omega, 60)

            # Create comprehensive EM wave analysis
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Electric & Magnetic Fields',
                    'Poynting Vector & Energy Flow',
                    'Field Animation (t=0)',
                    'Power Spectrum & Impedance'
                ),
                vertical_spacing=0.15,
                horizontal_spacing=0.1,
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"type": "scatter3d"}, {"secondary_y": False}]]
            )

            # Calculate fields for t=0
            k_real = np.real(k)
            k_imag = np.imag(k)
            
            # Electric field
            if polarization == "Linear (x-direction)":
                Ex = electric_amplitude * np.exp(-k_imag * z) * np.cos(k_real * z)
                Ey = np.zeros_like(z)
            elif polarization == "Linear (y-direction)":
                Ex = np.zeros_like(z)
                Ey = electric_amplitude * np.exp(-k_imag * z) * np.cos(k_real * z)
            elif polarization == "Circular (Right)":
                Ex = electric_amplitude * np.exp(-k_imag * z) * np.cos(k_real * z) / np.sqrt(2)
                Ey = electric_amplitude * np.exp(-k_imag * z) * np.sin(k_real * z) / np.sqrt(2)
            elif polarization == "Circular (Left)":
                Ex = electric_amplitude * np.exp(-k_imag * z) * np.cos(k_real * z) / np.sqrt(2)
                Ey = -electric_amplitude * np.exp(-k_imag * z) * np.sin(k_real * z) / np.sqrt(2)
            else:  # Elliptical
                Ex = electric_amplitude * np.exp(-k_imag * z) * np.cos(k_real * z) / np.sqrt(2)
                Ey = electric_amplitude * 0.5 * np.exp(-k_imag * z) * np.sin(k_real * z) / np.sqrt(2)

            # Magnetic field (B = k × E / ω)
            Bx = -Ey * k_real / omega if wave_type != "Conductor" else -Ey * np.real(k) / omega
            By = Ex * k_real / omega if wave_type != "Conductor" else Ex * np.real(k) / omega

            # Plot E and B fields
            fig.add_trace(
                go.Scatter(
                    x=z*1000, y=Ex,
                    mode='lines',
                    line=dict(color='#ef4444', width=4),
                    name='Ex',
                    hovertemplate='z: %{x:.2f} mm<br>Ex: %{y:.2f} V/m<extra></extra>'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=z*1000, y=Ey,
                    mode='lines',
                    line=dict(color='#3b82f6', width=4),
                    name='Ey',
                    hovertemplate='z: %{x:.2f} mm<br>Ey: %{y:.2f} V/m<extra></extra>'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=z*1000, y=Bx*1e6,  # Convert to µT
                    mode='lines',
                    line=dict(color='#10b981', width=3, dash='dash'),
                    name='Bx (µT)',
                    hovertemplate='z: %{x:.2f} mm<br>Bx: %{y:.2f} µT<extra></extra>'
                ),
                row=1, col=1
            )

            # Poynting vector
            S = (Ex * By - Ey * Bx) / mu_0  # W/m²
            energy_density = 0.5 * (epsilon_r * epsilon_0 * (Ex**2 + Ey**2) + (Bx**2 + By**2) / mu_0)

            fig.add_trace(
                go.Scatter(
                    x=z*1000, y=S,
                    mode='lines',
                    line=dict(color='#f59e0b', width=4),
                    fill='tozeroy',
                    fillcolor='rgba(245, 158, 11, 0.3)',
                    name='Poynting Vector',
                    hovertemplate='z: %{x:.2f} mm<br>S: %{y:.2e} W/m²<extra></extra>'
                ),
                row=1, col=2
            )

            fig.add_trace(
                go.Scatter(
                    x=z*1000, y=energy_density,
                    mode='lines',
                    line=dict(color='#8b5cf6', width=3, dash='dot'),
                    name='Energy Density',
                    hovertemplate='z: %{x:.2f} mm<br>u: %{y:.2e} J/m³<extra></extra>'
                ),
                row=1, col=2
            )

            # 3D field visualization
            z_3d = np.linspace(0, 2*wavelength, 50)
            x_3d = np.linspace(-wavelength/4, wavelength/4, 20)
            Z_3d, X_3d = np.meshgrid(z_3d, x_3d)

            # Electric field in 3D
            Ex_3d = electric_amplitude * np.exp(-k_imag * Z_3d) * np.cos(k_real * Z_3d)
            
            fig.add_trace(
                go.Surface(
                    x=X_3d*1000, y=Z_3d*1000, z=Ex_3d,
                    colorscale='RdBu',
                    name='Electric Field 3D',
                    showscale=False,
                    hovertemplate='x: %{x:.1f} mm<br>z: %{y:.1f} mm<br>Ex: %{z:.2f} V/m<extra></extra>'
                ),
                row=2, col=1
            )

            # Frequency spectrum and impedance
            freq_spectrum = np.array([frequency])
            impedance_real = np.array([np.real(impedance)])
            impedance_imag = np.array([np.imag(impedance)])

            fig.add_trace(
                go.Bar(
                    x=freq_spectrum, y=impedance_real,
                    name='Re(Z)',
                    marker_color='rgba(239, 68, 68, 0.7)',
                    hovertemplate='f: %{x:.1f} GHz<br>Re(Z): %{y:.1f} Ω<extra></extra>'
                ),
                row=2, col=2
            )

            if abs(np.imag(impedance)) > 0.1:
                fig.add_trace(
                    go.Bar(
                        x=freq_spectrum, y=impedance_imag,
                        name='Im(Z)',
                        marker_color='rgba(59, 130, 246, 0.7)',
                        hovertemplate='f: %{x:.1f} GHz<br>Im(Z): %{y:.1f} Ω<extra></extra>'
                    ),
                    row=2, col=2
                )

            # Update layout with enhanced visibility
            fig.update_layout(
                title=dict(
                    text=f'<b>EM Wave Analysis: {wave_type}</b><br>'
                         f'<span style="font-size:16px; color:#0ea5e9;">f = {frequency:.1f} GHz, {polarization}</span>',
                    x=0.5,
                    font=dict(size=20, color='white', family='Inter')
                ),
                height=750,
                showlegend=True,
                legend=dict(x=1.02, y=1, font=dict(size=10)),
                plot_bgcolor='rgba(30, 41, 59, 0.9)',
                paper_bgcolor='rgba(15, 23, 42, 0.9)',
                annotations=[
                    dict(
                        text="Maxwell's Equations Solutions",
                        x=0.5, y=1.02,
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=14, color='#cbd5e1')
                    )
                ]
            )

            # Update axes
            fig.update_xaxes(title_text="Distance (mm)", row=1, col=1, color='white')
            fig.update_yaxes(title_text="Field Amplitude", row=1, col=1, color='white')
            fig.update_xaxes(title_text="Distance (mm)", row=1, col=2, color='white')
            fig.update_yaxes(title_text="Power/Energy", row=1, col=2, color='white')
            fig.update_xaxes(title_text="Frequency (GHz)", row=2, col=2, color='white')
            fig.update_yaxes(title_text="Impedance (Ω)", row=2, col=2, color='white')

            # 3D scene
            fig.update_scenes(
                xaxis_title="x (mm)",
                yaxis_title="z (mm)", 
                zaxis_title="Ex (V/m)",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                row=2, col=1
            )

            return fig

        em_fig = create_em_wave_visualization()
        st.plotly_chart(em_fig, use_container_width=True)

        # EM wave metrics dashboard
        st.markdown("#### 📊 Electromagnetic Wave Analysis")

        # Calculate power and energy metrics
        power_density = 0.5 * electric_amplitude**2 / np.real(impedance)  # W/m²
        energy_velocity = c / np.sqrt(epsilon_r * mu_r)
        phase_velocity = omega / np.real(k)
        group_velocity = phase_velocity  # For non-dispersive media

        em_col1, em_col2, em_col3, em_col4 = st.columns(4)

        with em_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{wavelength*1000:.2f}</div>
                <div class="metric-label">Wavelength (mm)</div>
            </div>
            """, unsafe_allow_html=True)

        with em_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{abs(impedance):.1f}</div>
                <div class="metric-label">Impedance (Ω)</div>
            </div>
            """, unsafe_allow_html=True)

        with em_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{power_density:.2e}</div>
                <div class="metric-label">Power Density (W/m²)</div>
            </div>
            """, unsafe_allow_html=True)

        with em_col4:
            if skin_depth != float('inf'):
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{skin_depth*1000:.2f}</div>
                    <div class="metric-label">Skin Depth (mm)</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">∞</div>
                    <div class="metric-label">Skin Depth</div>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
           border-radius: 15px; text-align: center; border: 1px solid #475569;">
    <h3 style="color: white; margin-bottom: 1rem;">🌊 Wave Physics Laboratory</h3>
    <p style="color: #cbd5e1; margin-bottom: 1.5rem;">
        Explore the fundamental principles of wave mechanics through interactive visualizations.
    </p>
</div>
""", unsafe_allow_html=True)
