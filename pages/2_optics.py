import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from utils.physics import calculate_snell

st.set_page_config(
    page_title="Optics & Photonics Laboratory",
    page_icon="🔬",
    layout="wide"
)

# Enhanced CSS with optics-inspired design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        min-height: 100vh;
    }

    /* Optics-themed header with light animations */
    .optics-header {
        background: linear-gradient(135deg, #bfdbfe 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #2563eb;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
    }

    .optics-header::before {
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: 
            radial-gradient(circle at 25% 25%, rgba(255,255,255,0.2) 0%, transparent 30%),
            radial-gradient(circle at 75% 75%, rgba(255,255,255,0.15) 0%, transparent 30%),
            linear-gradient(45deg, rgba(255,255,255,0.1) 25%, transparent 25%);
        background-size: 80px 80px, 60px 60px, 40px 40px;
        animation: lightRays 25s linear infinite;
    }

    /* Enhanced section cards with glass morphism */
    .physics-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .physics-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 60px rgba(0,0,0,0.15);
    }

    .physics-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #3b82f6, #2563eb, #1d4ed8, #1e40af);
        animation: gradientShift 3s ease-in-out infinite;
    }

    /* Interactive parameter panels */
    .param-panel {
        background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #f59e0b;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .param-panel:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }

    .param-panel h4 {
        color: #92400e;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #e2e8f0;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-8px) rotateX(5deg);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: #3b82f6;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e40af;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }

    .metric-label {
        font-size: 1rem;
        color: #3730a3;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }

    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 15px;
        padding: 0.8rem;
        margin-bottom: 2rem;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #6b7280;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0 0.3rem;
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #1e40af;
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #bfdbfe 0%, #3b82f6 100%);
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transform: translateY(-3px);
    }

    /* Optics visualization cards */
    .optics-card {
        background: linear-gradient(135deg, #bfdbfe 0%, #3b82f6 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 3px solid #2563eb;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .optics-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(59, 130, 246, 0.4);
        border-color: #1d4ed8;
    }

    .optics-card h5 {
        color: white;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.2rem;
        position: relative;
        z-index: 2;
    }

    /* Advanced animations */
    @keyframes lightRays {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(90deg, #3b82f6, #2563eb, #1d4ed8, #1e40af); }
        25% { background: linear-gradient(90deg, #2563eb, #1d4ed8, #1e40af, #3b82f6); }
        50% { background: linear-gradient(90deg, #1d4ed8, #1e40af, #3b82f6, #2563eb); }
        75% { background: linear-gradient(90deg, #1e40af, #3b82f6, #2563eb, #1d4ed8); }
    }

    @keyframes waveMotion {
        0%, 100% { transform: translateY(0px) scaleY(1); }
        50% { transform: translateY(-3px) scaleY(1.1); }
    }

    @keyframes lightPropagation {
        0% { transform: translateX(-100%) scale(0.5); opacity: 0; }
        50% { transform: translateX(0%) scale(1); opacity: 1; }
        100% { transform: translateX(100%) scale(0.5); opacity: 0; }
    }

    /* Interactive elements */
    .interactive-icon {
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .interactive-icon:hover {
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .optics-header {
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
</style>
""", unsafe_allow_html=True)

# Enhanced optics-themed header
st.markdown("""
<div class="optics-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span class="interactive-icon">🔬</span> Optics & Photonics Laboratory
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Advanced Light Manipulation & Wave Phenomena
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Ray Optics</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Wave Optics</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Quantum Optics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced tabs with comprehensive optical phenomena
tabs = st.tabs([
    "🌈 Ray Optics", 
    "🌊 Wave Interference", 
    "🔍 Optical Instruments", 
    "💎 Optical Materials",
    "🚀 Advanced Optics",
    "🎓 Learning Hub"
])

# Tab 1: Enhanced Ray Optics
with tabs[0]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: #1e293b; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🌈</span> Geometric Ray Optics
        </h2>
        <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore light propagation, refraction, reflection, and lens systems through interactive ray tracing simulations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🔧</span> Ray Parameters")

        # Enhanced optics parameter controls
        st.markdown("**Material Properties:**")
        n1 = st.slider("Medium 1 Refractive Index", 1.0, 2.5, 1.0, 0.01, 
                      help="Refractive index of first medium (air = 1.0)")
        n2 = st.slider("Medium 2 Refractive Index", 1.0, 3.0, 1.5, 0.01,
                      help="Refractive index of second medium (glass ≈ 1.5)")

        # Material selection with properties
        materials = {
            "Air": 1.000,
            "Water": 1.333,
            "Glass (Crown)": 1.52,
            "Glass (Flint)": 1.62,
            "Diamond": 2.42,
            "Silicon": 3.42
        }

        material1 = st.selectbox("Select Medium 1", list(materials.keys()))
        material2 = st.selectbox("Select Medium 2", list(materials.keys()), index=2)

        if st.button("Use Material Values"):
            n1 = materials[material1]
            n2 = materials[material2]

        st.markdown("**Incident Ray:**")
        incident_angle = st.slider("Incident Angle (degrees)", 0, 90, 30, 1)
        num_rays = st.slider("Number of Rays", 1, 10, 5, 1)

        # Critical angle calculation
        if n1 > n2:
            critical_angle = np.degrees(np.arcsin(n2/n1))
            st.markdown(f"""
            <div style="background: #fee2e2; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Critical Angle:</strong> {critical_angle:.1f}°<br>
                <strong>Total Internal Reflection:</strong> {'Yes' if incident_angle > critical_angle else 'No'}
            </div>
            """, unsafe_allow_html=True)

        # Snell's law calculation
        sin_theta2 = (n1 * np.sin(np.radians(incident_angle))) / n2
        if sin_theta2 <= 1.0:
            refracted_angle = np.degrees(np.arcsin(sin_theta2))
            st.markdown(f"""
            <div style="background: #dbeafe; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Refracted Angle:</strong> {refracted_angle:.1f}°<br>
                <strong>Deviation:</strong> {abs(incident_angle - refracted_angle):.1f}°
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Total Internal Reflection</strong><br>
                No refracted ray exists
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced ray diagram with multiple rays and better visualization
        def create_enhanced_ray_diagram():
            fig = go.Figure()

            # Interface position
            interface_y = 0

            # Draw interface
            fig.add_shape(
                type="line",
                x0=-5, y0=interface_y, x1=5, y1=interface_y,
                line=dict(color="black", width=4),
            )

            # Add medium labels with background
            fig.add_annotation(
                x=-3, y=2,
                text=f"{material1}<br>n = {n1:.3f}",
                showarrow=False,
                font=dict(size=14, color="blue"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="blue",
                borderwidth=1
            )

            fig.add_annotation(
                x=-3, y=-2,
                text=f"{material2}<br>n = {n2:.3f}",
                showarrow=False,
                font=dict(size=14, color="red"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="red",
                borderwidth=1
            )

            # Draw normal line
            fig.add_shape(
                type="line",
                x0=0, y0=-4, x1=0, y1=4,
                line=dict(color="gray", width=2, dash="dash"),
            )

            colors = px.colors.qualitative.Set1

            # Draw multiple incident and refracted rays
            for i in range(num_rays):
                angle_offset = (i - num_rays//2) * 2  # Spread rays
                current_incident = incident_angle + angle_offset
                current_incident = max(0, min(90, current_incident))  # Clamp to valid range

                color = colors[i % len(colors)]

                # Incident ray
                incident_rad = np.radians(current_incident)
                x_start = -3
                y_start = 3
                x_end = 0
                y_end = interface_y

                fig.add_trace(go.Scatter(
                    x=[x_start, x_end],
                    y=[y_start, y_end],
                    mode='lines+markers',
                    line=dict(color=color, width=3),
                    marker=dict(size=8),
                    name=f'Incident Ray {i+1}',
                    hovertemplate=f'Incident Angle: {current_incident:.1f}°<extra></extra>'
                ))

                # Add arrow for incident ray
                fig.add_annotation(
                    x=x_end - 0.5, y=y_end + 0.5,
                    ax=x_start + 0.5, ay=y_start - 0.5,
                    xref="x", yref="y", axref="x", ayref="y",
                    arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=color
                )

                # Calculate refracted ray
                sin_theta2 = (n1 * np.sin(incident_rad)) / n2
                if sin_theta2 <= 1.0:  # Refraction occurs
                    refracted_rad = np.arcsin(sin_theta2)
                    refracted_deg = np.degrees(refracted_rad)

                    # Refracted ray
                    x_start_ref = 0
                    y_start_ref = interface_y
                    x_end_ref = 3 * np.sin(refracted_rad)
                    y_end_ref = interface_y - 3 * np.cos(refracted_rad)

                    fig.add_trace(go.Scatter(
                        x=[x_start_ref, x_end_ref],
                        y=[y_start_ref, y_end_ref],
                        mode='lines+markers',
                        line=dict(color=color, width=3, dash='dot'),
                        marker=dict(size=8),
                        name=f'Refracted Ray {i+1}',
                        hovertemplate=f'Refracted Angle: {refracted_deg:.1f}°<extra></extra>'
                    ))

                    # Add arrow for refracted ray
                    fig.add_annotation(
                        x=x_end_ref - 0.2, y=y_end_ref + 0.2,
                        ax=x_start_ref + 0.2, ay=y_start_ref - 0.2,
                        xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=color
                    )
                else:  # Total internal reflection
                    reflected_rad = incident_rad
                    x_start_refl = 0
                    y_start_refl = interface_y
                    x_end_refl = 3 * np.sin(reflected_rad)
                    y_end_refl = interface_y + 3 * np.cos(reflected_rad)

                    fig.add_trace(go.Scatter(
                        x=[x_start_refl, x_end_refl],
                        y=[y_start_refl, y_end_refl],
                        mode='lines+markers',
                        line=dict(color=color, width=3, dash='dashdot'),
                        marker=dict(size=8),
                        name=f'Reflected Ray {i+1}',
                        hovertemplate=f'Reflected Angle: {current_incident:.1f}°<extra></extra>'
                    ))

                    # Add arrow for reflected ray
                    fig.add_annotation(
                        x=x_end_refl - 0.2, y=y_end_refl - 0.2,
                        ax=x_start_refl + 0.2, ay=y_start_refl + 0.2,
                        xref="x", yref="y", axref="x", ayref="y",
                        arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=color
                    )

            # Add angle arcs for main ray
            if num_rays > 0:
                # Incident angle arc
                theta_range = np.linspace(np.radians(90), np.radians(90 - incident_angle), 50)
                arc_radius = 0.8
                arc_x = arc_radius * np.cos(theta_range)
                arc_y = interface_y + arc_radius * np.sin(theta_range)

                fig.add_trace(go.Scatter(
                    x=arc_x, y=arc_y,
                    mode='lines',
                    line=dict(color='blue', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))

                # Angle label
                fig.add_annotation(
                    x=0.5, y=0.5,
                    text=f"θ₁ = {incident_angle}°",
                    showarrow=False,
                    font=dict(size=12, color="blue")
                )

            fig.update_layout(
                title=dict(
                    text=f'<b>Ray Refraction: {material1} → {material2}</b><br>'
                         f'<span style="font-size:14px;">Snell\'s Law: n₁sin(θ₁) = n₂sin(θ₂)</span>',
                    x=0.5,
                    font=dict(size=18, color='#1e293b')
                ),
                xaxis=dict(
                    title='Distance',
                    range=[-5, 5],
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                yaxis=dict(
                    title='Height',
                    range=[-4, 4],
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)'
                ),
                width=800,
                height=600,
                showlegend=True,
                legend=dict(x=1.02, y=1),
                plot_bgcolor='rgba(248,250,252,0.9)'
            )

            return fig

        ray_fig = create_enhanced_ray_diagram()
        st.plotly_chart(ray_fig, use_container_width=True)

        # Optical properties dashboard
        st.markdown("#### 📊 Optical Properties Dashboard")

        # Calculate various optical parameters
        fresnel_r_s = ((n1 * np.cos(np.radians(incident_angle)) - n2 * np.sqrt(1 - (n1/n2 * np.sin(np.radians(incident_angle)))**2)) / 
                      (n1 * np.cos(np.radians(incident_angle)) + n2 * np.sqrt(1 - (n1/n2 * np.sin(np.radians(incident_angle)))**2)))**2 if sin_theta2 <= 1 else 1.0

        transmittance = 1 - fresnel_r_s if sin_theta2 <= 1 else 0.0

        brewster_angle = np.degrees(np.arctan(n2/n1)) if n1 != n2 else 0

        # Display optical metrics
        opt_col1, opt_col2, opt_col3, opt_col4 = st.columns(4)

        with opt_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fresnel_r_s:.3f}</div>
                <div class="metric-label">Reflectance</div>
            </div>
            """, unsafe_allow_html=True)

        with opt_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{transmittance:.3f}</div>
                <div class="metric-label">Transmittance</div>
            </div>
            """, unsafe_allow_html=True)

        with opt_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{brewster_angle:.1f}°</div>
                <div class="metric-label">Brewster Angle</div>
            </div>
            """, unsafe_allow_html=True)

        with opt_col4:
            numerical_aperture = np.sqrt(n2**2 - n1**2) if n2 > n1 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{numerical_aperture:.3f}</div>
                <div class="metric-label">Numerical Aperture</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: Enhanced Wave Interference
with tabs[1]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: #1e293b; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🌊</span> Wave Optics & Interference
        </h2>
        <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore wave interference, diffraction patterns, and coherence phenomena with interactive simulations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🌊</span> Wave Parameters")

        # Enhanced wave interference controls
        wavelength = st.slider("Wavelength (nm)", 400, 700, 550, 10,
                              help="Visible light wavelength")

        # Color mapping based on wavelength
        def wavelength_to_color(wl):
            if wl < 450:
                return '#4c1d95'  # Violet
            elif wl < 495:
                return '#1e40af'  # Blue
            elif wl < 570:
                return '#059669'  # Green
            elif wl < 590:
                return '#d97706'  # Yellow
            elif wl < 620:
                return '#ea580c'  # Orange
            else:
                return '#dc2626'  # Red

        wave_color = wavelength_to_color(wavelength)
        st.markdown(f"""
        <div style="background: {wave_color}; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: center;">
            <strong>Current Color: {wavelength} nm</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Interference Setup:**")
        experiment_type = st.selectbox("Experiment Type", 
                                     ["Double Slit", "Single Slit", "Multiple Slit", "Diffraction Grating"])

        if experiment_type == "Double Slit":
            slit_separation = st.slider("Slit Separation (μm)", 1.0, 100.0, 20.0, 1.0)
            slit_width = st.slider("Slit Width (μm)", 0.5, 10.0, 2.0, 0.1)
        elif experiment_type == "Single Slit":
            slit_width = st.slider("Slit Width (μm)", 0.5, 20.0, 5.0, 0.1)
            slit_separation = None
        elif experiment_type == "Multiple Slit":
            num_slits = st.slider("Number of Slits", 3, 10, 5, 1)
            slit_separation = st.slider("Slit Separation (μm)", 1.0, 50.0, 15.0, 1.0)
            slit_width = st.slider("Slit Width (μm)", 0.5, 5.0, 1.0, 0.1)
        else:  # Diffraction Grating
            lines_per_mm = st.slider("Lines per mm", 100.0, 2000.0, 600.0, 50.0)
            slit_separation = 1000.0 / lines_per_mm  # Convert to μm
            slit_width = slit_separation * 0.8  # Assume 80% duty cycle

        screen_distance = st.slider("Screen Distance (cm)", 10.0, 200.0, 100.0, 5.0)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced interference pattern visualization
        def create_enhanced_interference_pattern():
            # Convert units
            wavelength_m = wavelength * 1e-9
            screen_distance_m = screen_distance * 1e-2

            # Create screen position array
            screen_width = 0.05  # 5 cm screen width
            y_positions = np.linspace(-screen_width/2, screen_width/2, 1000)

            if experiment_type == "Single Slit":
                slit_width_m = slit_width * 1e-6

                # Single slit diffraction pattern
                beta = np.pi * slit_width_m * y_positions / (wavelength_m* screen_distance_m)
                # Avoid division by zero
                beta[beta == 0] = 1e-10
                intensity = (np.sin(beta) / beta)**2

            elif experiment_type == "Double Slit":
                slit_width_m = slit_width * 1e-6
                slit_separation_m = slit_separation * 1e-6

                # Double slit pattern (single slit envelope × interference)
                beta = np.pi * slit_width_m * y_positions / (wavelength_m * screen_distance_m)
                alpha = np.pi * slit_separation_m * y_positions / (wavelength_m * screen_distance_m)

                beta[beta == 0] = 1e-10
                single_slit = (np.sin(beta) / beta)**2
                interference = np.cos(alpha)**2
                intensity = single_slit * interference

            elif experiment_type == "Multiple Slit":
                slit_width_m = slit_width * 1e-6
                slit_separation_m = slit_separation * 1e-6

                # Multiple slit pattern
                beta = np.pi * slit_width_m * y_positions / (wavelength_m * screen_distance_m)
                alpha = np.pi * slit_separation_m * y_positions / (wavelength_m * screen_distance_m)

                beta[beta == 0] = 1e-10
                alpha[alpha == 0] = 1e-10

                single_slit = (np.sin(beta) / beta)**2
                multi_slit = (np.sin(num_slits * alpha) / np.sin(alpha))**2
                intensity = single_slit * multi_slit / num_slits**2

            else:  # Diffraction Grating
                slit_width_m = slit_width * 1e-6
                slit_separation_m = slit_separation * 1e-6
                N = 50  # Effective number of illuminated slits

                beta = np.pi * slit_width_m * y_positions / (wavelength_m * screen_distance_m)
                alpha = np.pi * slit_separation_m * y_positions / (wavelength_m * screen_distance_m)

                beta[beta == 0] = 1e-10
                alpha[alpha == 0] = 1e-10

                single_slit = (np.sin(beta) / beta)**2
                grating = (np.sin(N * alpha) / np.sin(alpha))**2
                intensity = single_slit * grating / N**2

            # Normalize intensity
            intensity = intensity / np.max(intensity)

            # Create the interference pattern plot
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=(f'{experiment_type} Intensity Pattern', '2D Interference Visualization'),
                vertical_spacing=0.15,
                row_heights=[0.6, 0.4]
            )

            # 1D intensity plot
            fig.add_trace(
                go.Scatter(
                    x=y_positions * 100,  # Convert to cm
                    y=intensity,
                    mode='lines',
                    line=dict(color=wave_color, width=3),
                    name='Intensity Pattern',
                    fill='tozeroy',
                    fillcolor=f'rgba{tuple(list(bytes.fromhex(wave_color[1:])[:3]) + [0.3])}',
                    hovertemplate='Position: %{x:.2f} cm<br>Intensity: %{y:.3f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Find and mark maxima and minima
            from scipy.signal import find_peaks

            # Find maxima
            maxima_indices, _ = find_peaks(intensity, height=0.1, distance=10)
            if len(maxima_indices) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=y_positions[maxima_indices] * 100,
                        y=intensity[maxima_indices],
                        mode='markers',
                        marker=dict(color='red', size=8, symbol='circle'),
                        name='Maxima',
                        hovertemplate='Maximum at %{x:.2f} cm<extra></extra>'
                    ),
                    row=1, col=1
                )

            # Find minima
            minima_indices, _ = find_peaks(-intensity, height=-0.95, distance=10)
            if len(minima_indices) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=y_positions[minima_indices] * 100,
                        y=intensity[minima_indices],
                        mode='markers',
                        marker=dict(color='blue', size=8, symbol='x'),
                        name='Minima',
                        hovertemplate='Minimum at %{x:.2f} cm<extra></extra>'
                    ),
                    row=1, col=1
                )

            # 2D visualization
            y_2d = np.linspace(-screen_width/2, screen_width/2, 200)
            x_2d = np.linspace(0, 0.01, 50)  # 1 cm depth
            Y, X = np.meshgrid(y_2d, x_2d)

            # Interpolate intensity for 2D
            intensity_2d = np.interp(y_2d, y_positions, intensity)
            intensity_2d_full = np.tile(intensity_2d, (len(x_2d), 1))

            fig.add_trace(
                go.Heatmap(
                    x=y_2d * 100,
                    y=x_2d * 100,
                    z=intensity_2d_full,
                    colorscale=[[0, 'black'], [1, wave_color]],
                    showscale=False,
                    name='2D Pattern',
                    hovertemplate='Y: %{x:.2f} cm<br>X: %{y:.2f} cm<br>Intensity: %{z:.3f}<extra></extra>'
                ),
                row=2, col=1
            )

            # Update layout
            fig.update_xaxes(title_text="Screen Position (cm)", row=1, col=1)
            fig.update_yaxes(title_text="Relative Intensity", row=1, col=1)
            fig.update_xaxes(title_text="Screen Position (cm)", row=2, col=1)
            fig.update_yaxes(title_text="Distance from Screen (cm)", row=2, col=1)

            fig.update_layout(
                title=dict(
                    text=f'<b>{experiment_type} Interference Pattern</b><br>'
                         f'<span style="font-size:14px;">λ = {wavelength} nm, Screen Distance = {screen_distance} cm</span>',
                    x=0.5,
                    font=dict(size=18, color='#1e293b')
                ),
                height=700,
                showlegend=True,
                legend=dict(x=1.02, y=1)
            )

            return fig

        interference_fig = create_enhanced_interference_pattern()
        st.plotly_chart(interference_fig, use_container_width=True)

        # Wave optics properties
        st.markdown("#### 📊 Wave Optics Analysis")

        # Calculate theoretical properties
        if experiment_type == "Double Slit" and slit_separation:
            angular_width = wavelength * 1e-9 / (slit_separation * 1e-6)
            fringe_width = angular_width * screen_distance * 1e-2 * 100  # cm

            # Calculate resolution
            rayleigh_criterion = 1.22 * wavelength * 1e-9 / (slit_width * 1e-6)
            resolution_angle = np.degrees(rayleigh_criterion)

        elif experiment_type == "Diffraction Grating":
            # Grating equation: d sin(θ) = mλ
            d = slit_separation * 1e-6
            max_order = int(d / (wavelength * 1e-9))
            angular_dispersion = 1 / (d * np.cos(np.arcsin(wavelength * 1e-9 / d)) if d > wavelength * 1e-9 else d)

        else:
            fringe_width = 0
            resolution_angle = 0

        # Display wave metrics
        wave_col1, wave_col2, wave_col3, wave_col4 = st.columns(4)

        with wave_col1:
            frequency = 3e8 / (wavelength * 1e-9) / 1e12  # THz
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{frequency:.1f}</div>
                <div class="metric-label">Frequency (THz)</div>
            </div>
            """, unsafe_allow_html=True)

        with wave_col2:
            energy = 1240 / wavelength  # eV (using hc/λ with hc ≈ 1240 eV·nm)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{energy:.2f}</div>
                <div class="metric-label">Photon Energy (eV)</div>
            </div>
            """, unsafe_allow_html=True)

        with wave_col3:
            if 'fringe_width' in locals() and fringe_width > 0:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{fringe_width:.3f}</div>
                    <div class="metric-label">Fringe Width (cm)</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">N/A</div>
                    <div class="metric-label">Fringe Width</div>
                </div>
                """, unsafe_allow_html=True)

        with wave_col4:
            coherence_length = (wavelength * 1e-9)**2 / (10e-9) * 1e6  # μm (assuming 10 nm linewidth)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{coherence_length:.0f}</div>
                <div class="metric-label">Coherence Length (μm)</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Enhanced Optical Instruments
with tabs[2]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: #1e293b; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            <span class="interactive-icon">🔍</span> Optical Instruments & Systems
        </h2>
        <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Design and analyze optical instruments including telescopes, microscopes, and laser systems.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🔬</span> Instrument Parameters")

        # Instrument selection
        instrument_type = st.selectbox("Optical Instrument", [
            "Refracting Telescope", "Reflecting Telescope", "Compound Microscope", 
            "Laser System", "Fiber Optic System", "Interferometer"
        ])

        if instrument_type == "Refracting Telescope":
            focal_length_obj = st.slider("Objective Focal Length (cm)", 50.0, 500.0, 200.0, 10.0)
            focal_length_eye = st.slider("Eyepiece Focal Length (cm)", 1.0, 10.0, 5.0, 0.5)
            aperture_diameter = st.slider("Aperture Diameter (cm)", 5.0, 50.0, 20.0, 1.0)

            # Calculate telescope properties
            magnification = focal_length_obj / focal_length_eye
            light_gathering = (aperture_diameter / 2)**2 * np.pi
            resolution_limit = 1.22 * 550e-9 / (aperture_diameter * 0.01)  # arcseconds

            st.markdown(f"""
            <div style="background: rgba(59, 130, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Telescope Properties:</strong><br>
                Magnification: {magnification:.1f}×<br>
                Light Gathering: {light_gathering:.1f} cm²<br>
                Resolution: {np.degrees(resolution_limit)*3600:.2f} arcsec
            </div>
            """, unsafe_allow_html=True)

        elif instrument_type == "Compound Microscope":
            obj_focal_length = st.slider("Objective Focal Length (mm)", 1.0, 20.0, 4.0, 0.5)
            eye_focal_length = st.slider("Eyepiece Focal Length (mm)", 10.0, 50.0, 25.0, 1.0)
            tube_length = st.slider("Tube Length (mm)", 150.0, 200.0, 160.0, 5.0)
            numerical_aperture = st.slider("Numerical Aperture", 0.1, 1.4, 0.65, 0.05)

            # Calculate microscope properties
            lateral_magnification = tube_length / obj_focal_length
            angular_magnification = 250 / eye_focal_length  # 250mm normal viewing distance
            total_magnification = lateral_magnification * angular_magnification
            resolution = 0.61 * 550e-9 / numerical_aperture * 1e6  # micrometers

            st.markdown(f"""
            <div style="background: rgba(59, 130, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>Microscope Properties:</strong><br>
                Total Magnification: {total_magnification:.0f}×<br>
                Resolution: {resolution:.2f} μm<br>
                Working Distance: {obj_focal_length:.1f} mm
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced optical instrument visualization
        def create_instrument_visualization():
            if instrument_type == "Refracting Telescope":
                # Create telescope ray diagram
                fig = go.Figure()

                # Objective lens
                obj_y = np.linspace(-aperture_diameter/2, aperture_diameter/2, 100)
                obj_x = np.zeros_like(obj_y)

                fig.add_trace(go.Scatter(
                    x=obj_x, y=obj_y,
                    mode='lines',
                    line=dict(color='#0ea5e9', width=5),
                    name='Objective Lens'
                ))

                # Eyepiece lens
                eye_x = focal_length_obj + focal_length_eye
                eye_y = np.linspace(-2, 2, 50)
                eye_x_arr = np.full_like(eye_y, eye_x)

                fig.add_trace(go.Scatter(
                    x=eye_x_arr, y=eye_y,
                    mode='lines',
                    line=dict(color='#10b981', width=5),
                    name='Eyepiece Lens'
                ))

                # Light rays from distant object
                ray_angles = np.linspace(-0.1, 0.1, 5)
                colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#22c55e']

                for i, angle in enumerate(ray_angles):
                    # Incident rays (parallel)
                    x_incident = np.linspace(-50, 0, 50)
                    y_incident = x_incident * angle + aperture_diameter/4 * (i-2)/2

                    # Refracted rays to focus
                    x_focus = np.linspace(0, focal_length_obj, 50)
                    y_focus = np.linspace(y_incident[-1], 0, 50)

                    # Rays from focus to eyepiece
                    x_to_eye = np.linspace(focal_length_obj, eye_x, 50)
                    y_to_eye = np.linspace(0, y_incident[-1] * focal_length_eye / focal_length_obj, 50)

                    # Final rays (parallel again)
                    x_final = np.linspace(eye_x, eye_x + 50, 50)
                    y_final = np.full_like(x_final, y_to_eye[-1])

                    fig.add_trace(go.Scatter(
                        x=np.concatenate([x_incident, x_focus, x_to_eye, x_final]),
                        y=np.concatenate([y_incident, y_focus, y_to_eye, y_final]),
                        mode='lines',
                        line=dict(color=colors[i], width=2),
                        name=f'Light Ray {i+1}',
                        showlegend=(i == 0)
                    ))

                # Add focal points
                fig.add_trace(go.Scatter(
                    x=[focal_length_obj], y=[0],
                    mode='markers',
                    marker=dict(size=10, color='red', symbol='x'),
                    name='Primary Focus'
                ))

                fig.update_layout(
                    title=dict(
                        text=f'<b>Refracting Telescope Design</b><br><span style="font-size:14px;">Magnification: {magnification:.1f}×, Aperture: {aperture_diameter:.1f} cm</span>',
                        x=0.5,
                        font=dict(size=18, color='#1e293b')
                    ),
                    xaxis=dict(title='Distance (cm)', range=[-60, eye_x + 60]),
                    yaxis=dict(title='Height (cm)', range=[-aperture_diameter/2 - 5, aperture_diameter/2 + 5]),
                    height=500,
                    showlegend=True,
                    plot_bgcolor='rgba(248,250,252,0.9)'
                )

            elif instrument_type == "Compound Microscope":
                # Create microscope ray diagram
                fig = go.Figure()

                # Objective lens
                fig.add_trace(go.Scatter(
                    x=[obj_focal_length, obj_focal_length],
                    y=[-5, 5],
                    mode='lines',
                    line=dict(color='#0ea5e9', width=5),
                    name='Objective'
                ))

                # Eyepiece lens
                eye_position = tube_length + eye_focal_length
                fig.add_trace(go.Scatter(
                    x=[eye_position, eye_position],
                    y=[-3, 3],
                    mode='lines',
                    line=dict(color='#10b981', width=5),
                    name='Eyepiece'
                ))

                # Object and images
                object_height = 1
                image1_height = object_height * lateral_magnification

                # Object
                fig.add_trace(go.Scatter(
                    x=[0, 0],
                    y=[0, object_height],
                    mode='lines+markers',
                    line=dict(color='#ef4444', width=3),
                    marker=dict(size=8),
                    name='Object'
                ))

                # Intermediate image
                fig.add_trace(go.Scatter(
                    x=[tube_length, tube_length],
                    y=[0, image1_height],
                    mode='lines+markers',
                    line=dict(color='#f59e0b', width=3),
                    marker=dict(size=6),
                    name='Intermediate Image'
                ))

                # Ray tracing
                ray_x = [0, obj_focal_length, tube_length, eye_position, eye_position + 50]
                ray_y = [object_height, object_height, image1_height, image1_height * 2, image1_height * 2]

                fig.add_trace(go.Scatter(
                    x=ray_x, y=ray_y,
                    mode='lines',
                    line=dict(color='#a855f7', width=2, dash='dash'),
                    name='Principal Ray'
                ))

                fig.update_layout(
                    title=dict(
                        text=f'<b>Compound Microscope</b><br><span style="font-size:14px;">Total Magnification: {total_magnification:.0f}×, Resolution: {resolution:.2f} μm</span>',
                        x=0.5,
                        font=dict(size=18, color='#1e293b')
                    ),
                    xaxis=dict(title='Distance (mm)', range=[-10, eye_position + 60]),
                    yaxis=dict(title='Height (mm)'),
                    height=500,
                    showlegend=True,
                    plot_bgcolor='rgba(248,250,252,0.9)'
                )

            else:
                # Placeholder for other instruments
                fig = go.Figure()
                fig.add_annotation(
                    text=f"{instrument_type} simulation coming soon!",
                    x=0.5, y=0.5,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=18, color='#64748b')
                )
                fig.update_layout(height=400)

            return fig

        instrument_fig = create_instrument_visualization()
        st.plotly_chart(instrument_fig, use_container_width=True)

        # Instrument analysis
        st.markdown("#### 📊 Optical Performance Analysis")

        if instrument_type == "Refracting Telescope":
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

            with perf_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{magnification:.1f}×</div>
                    <div class="metric-label">Magnification</div>
                </div>
                """, unsafe_allow_html=True)

            with perf_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{light_gathering:.0f}</div>
                    <div class="metric-label">Light Gathering (cm²)</div>
                </div>
                """, unsafe_allow_html=True)

            with perf_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{np.degrees(resolution_limit)*3600:.2f}</div>
                    <div class="metric-label">Resolution (arcsec)</div>
                </div>
                """, unsafe_allow_html=True)

            with perf_col4:
                field_of_view = np.degrees(aperture_diameter * 0.01 / focal_length_obj) * 60  # arcmin
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{field_of_view:.1f}</div>
                    <div class="metric-label">Field of View (arcmin)</div>
                </div>
                """, unsafe_allow_html=True)

# Tab 3: Complete Optical Materials & Metamaterials
with tabs[3]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: #1e293b; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">💎</span> Optical Materials & Metamaterials
        </h2>
        <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore advanced optical materials, dispersion phenomena, and metamaterials with negative refractive index.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>💎</span> Material Parameters")

        # Material selection
        materials = {
            "Fused Silica": {"n0": 1.458, "B1": 0.696, "B2": 0.408, "B3": 0.897},
            "BK7 Glass": {"n0": 1.519, "B1": 1.030, "B2": 0.231, "B3": 1.010},
            "Sapphire": {"n0": 1.754, "B1": 1.430, "B2": 0.650, "B3": 5.341},
            "Diamond": {"n0": 2.418, "B1": 0.300, "B2": 4.000, "B3": 0.000},
            "Silicon": {"n0": 3.420, "B1": 10.668, "B2": 0.003, "B3": 1.540}
        }

        selected_material = st.selectbox("Material", list(materials.keys()))
        props = materials[selected_material]

        wavelength_range = st.slider("Wavelength Range (nm)", 300, 1500, (400, 800), 50)
        show_absorption = st.checkbox("Show Absorption", value=True)
        show_group_velocity = st.checkbox("Show Group Velocity Dispersion", value=False)

        # Metamaterial properties
        st.markdown("#### <span class='interactive-icon'>🔬</span> Metamaterial Design")
        metamaterial_type = st.selectbox("Metamaterial Type", 
                                       ["Split Ring Resonator", "Wire Array", "Fishnet Structure"])
        
        epsilon_r = st.slider("Relative Permittivity", -5.0, 5.0, 1.0, 0.1)
        mu_r = st.slider("Relative Permeability", -5.0, 5.0, 1.0, 0.1)
        
        # Calculate refractive index
        n_metamaterial = np.sqrt(epsilon_r * mu_r)
        
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Metamaterial Properties:</strong><br>
            n = √(εᵣμᵣ) = {n_metamaterial:.3f}<br>
            Type: {'Left-handed' if n_metamaterial < 0 else 'Right-handed'}<br>
            Band: {'Forbidden' if epsilon_r < 0 and mu_r > 0 else 'Allowed'}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced material dispersion visualization
        def create_material_dispersion():
            wavelengths = np.linspace(wavelength_range[0], wavelength_range[1], 300)
            
            # Sellmeier equation for refractive index
            def sellmeier(wl, props):
                wl_um = wl / 1000  # Convert to micrometers
                n_squared = props["n0"]**2
                n_squared += props["B1"] * wl_um**2 / (wl_um**2 - 0.01)
                n_squared += props["B2"] * wl_um**2 / (wl_um**2 - 0.02)
                n_squared += props["B3"] * wl_um**2 / (wl_um**2 - 100)
                return np.sqrt(np.abs(n_squared))

            n_values = [sellmeier(wl, props) for wl in wavelengths]

            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    f'{selected_material} Refractive Index',
                    'Group Velocity Dispersion',
                    'Absorption Coefficient',
                    'Phase & Group Velocity'
                ),
                vertical_spacing=0.12,
                horizontal_spacing=0.1
            )

            # Refractive index plot with enhanced visibility
            fig.add_trace(
                go.Scatter(
                    x=wavelengths, y=n_values,
                    mode='lines',
                    line=dict(color='#1e40af', width=4),
                    name='Refractive Index',
                    hovertemplate='λ: %{x:.0f} nm<br>n: %{y:.4f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Add visible region shading
            fig.add_vrect(
                x0=380, x1=750,
                fillcolor="rgba(255, 255, 0, 0.1)",
                layer="below", line_width=0,
                annotation_text="Visible",
                annotation_position="top left",
                row=1, col=1
            )

            # Group velocity dispersion
            if show_group_velocity:
                # Calculate GVD (simplified)
                dn_dlambda = np.gradient(n_values, wavelengths)
                d2n_dlambda2 = np.gradient(dn_dlambda, wavelengths)
                gvd = wavelengths**3 / (2 * np.pi * 3e8 * 1e9) * d2n_dlambda2

                fig.add_trace(
                    go.Scatter(
                        x=wavelengths, y=gvd,
                        mode='lines',
                        line=dict(color='#dc2626', width=3),
                        name='GVD',
                        hovertemplate='λ: %{x:.0f} nm<br>GVD: %{y:.2e} s²/m<extra></extra>'
                    ),
                    row=1, col=2
                )

            # Absorption coefficient
            if show_absorption:
                # Simplified absorption model
                alpha = 0.1 * np.exp(-(wavelengths - 500)**2 / (2 * 100**2))  # Gaussian absorption
                
                fig.add_trace(
                    go.Scatter(
                        x=wavelengths, y=alpha,
                        mode='lines',
                        line=dict(color='#059669', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(5, 150, 105, 0.3)',
                        name='Absorption',
                        hovertemplate='λ: %{x:.0f} nm<br>α: %{y:.3f} cm⁻¹<extra></extra>'
                    ),
                    row=2, col=1
                )

            # Phase and group velocity
            c = 3e8  # Speed of light
            v_phase = c / np.array(n_values)
            v_group = c / (np.array(n_values) - wavelengths * np.gradient(n_values, wavelengths) * 1e-9)

            fig.add_trace(
                go.Scatter(
                    x=wavelengths, y=v_phase / c,
                    mode='lines',
                    line=dict(color='#7c3aed', width=3),
                    name='Phase Velocity',
                    hovertemplate='λ: %{x:.0f} nm<br>vₚ/c: %{y:.4f}<extra></extra>'
                ),
                row=2, col=2
            )

            fig.add_trace(
                go.Scatter(
                    x=wavelengths, y=v_group / c,
                    mode='lines',
                    line=dict(color='#ea580c', width=3, dash='dash'),
                    name='Group Velocity',
                    hovertemplate='λ: %{x:.0f} nm<br>vₒ/c: %{y:.4f}<extra></extra>'
                ),
                row=2, col=2
            )

            # Update layout with enhanced visibility
            fig.update_layout(
                title=dict(
                    text=f'<b>{selected_material} Optical Properties</b><br>'
                         f'<span style="font-size:16px; color:#1e40af;">Wavelength Range: {wavelength_range[0]}-{wavelength_range[1]} nm</span>',
                    x=0.5,
                    font=dict(size=20, color='#1e293b', family='Inter')
                ),
                height=700,
                showlegend=True,
                legend=dict(x=1.02, y=1, font=dict(size=12)),
                plot_bgcolor='rgba(248,250,252,0.9)',
                annotations=[
                    dict(
                        text="Enhanced Material Analysis",
                        x=0.5, y=1.02,
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=14, color='#64748b')
                    )
                ]
            )

            # Update axes with better visibility
            for i in range(1, 3):
                for j in range(1, 3):
                    fig.update_xaxes(
                        title_text="Wavelength (nm)" if i == 2 else "",
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.1)',
                        linecolor='rgba(0,0,0,0.2)',
                        row=i, col=j
                    )
                    fig.update_yaxes(
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.1)',
                        linecolor='rgba(0,0,0,0.2)',
                        row=i, col=j
                    )

            return fig

        materials_fig = create_material_dispersion()
        st.plotly_chart(materials_fig, use_container_width=True)

        # Material properties dashboard
        st.markdown("#### 📊 Material Properties Analysis")

        # Calculate key properties
        wl_center = (wavelength_range[0] + wavelength_range[1]) / 2
        n_center = 1.5  # Simplified for display
        abbe_number = (n_center - 1) / 0.01  # Simplified calculation
        
        mat_col1, mat_col2, mat_col3, mat_col4 = st.columns(4)

        with mat_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{n_center:.3f}</div>
                <div class="metric-label">Refractive Index</div>
            </div>
            """, unsafe_allow_html=True)

        with mat_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{abbe_number:.1f}</div>
                <div class="metric-label">Abbe Number</div>
            </div>
            """, unsafe_allow_html=True)

        with mat_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{epsilon_r:.2f}</div>
                <div class="metric-label">Permittivity</div>
            </div>
            """, unsafe_allow_html=True)

        with mat_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{mu_r:.2f}</div>
                <div class="metric-label">Permeability</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[4]:
    st.markdown("""
    <div class="physics-section">
        <h2 style="color: #1e293b; margin-bottom: 2rem; font-size: 2.2rem; font-weight: 700;">
            <span class="interactive-icon">🚀</span> Advanced Quantum Optics & Nonlinear Phenomena
        </h2>
        <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.1rem; line-height: 1.6;">
            Explore quantum coherence, photon statistics, and nonlinear optical effects in advanced optical systems.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.markdown('<div class="param-panel">', unsafe_allow_html=True)
        st.markdown("#### <span class='interactive-icon'>🚀</span> Quantum Optics Parameters")

        # Quantum light source
        light_source = st.selectbox("Light Source", [
            "Coherent State (Laser)",
            "Thermal Light",
            "Single Photon",
            "Squeezed Light",
            "Entangled Photons"
        ])

        # Nonlinear crystal properties
        crystal_type = st.selectbox("Nonlinear Crystal", [
            "BBO (β-BaB₂O₄)",
            "KDP (KH₂PO₄)",
            "LiIO₃",
            "PPLN (Periodically Poled LiNbO₃)"
        ])

        # Interaction parameters
        pump_power = st.slider("Pump Power (mW)", 0.1, 100.0, 10.0, 0.1)
        crystal_length = st.slider("Crystal Length (mm)", 0.1, 50.0, 5.0, 0.1)
        phase_matching = st.selectbox("Phase Matching", ["Type I", "Type II", "Quasi Phase Matching"])

        # Quantum parameters
        photon_number = st.slider("Average Photon Number", 0.1, 10.0, 1.0, 0.1)
        coherence_time = st.slider("Coherence Time (ps)", 0.1, 100.0, 10.0, 0.1)

        # Calculate quantum properties
        g2_coherent = 1.0  # Second-order correlation for coherent light
        g2_thermal = 2.0   # For thermal light
        g2_single = 0.0    # For single photons

        if light_source == "Coherent State (Laser)":
            g2_value = g2_coherent
            statistics = "Poissonian"
        elif light_source == "Thermal Light":
            g2_value = g2_thermal
            statistics = "Super-Poissonian"
        elif light_source == "Single Photon":
            g2_value = g2_single
            statistics = "Sub-Poissonian"
        else:
            g2_value = 0.5
            statistics = "Non-classical"

        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.2); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>Quantum Properties:</strong><br>
            g²(0): {g2_value:.2f}<br>
            Statistics: {statistics}<br>
            Crystal: {crystal_type}<br>
            Phase Matching: {phase_matching}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Enhanced quantum optics visualization
        def create_quantum_optics_visualization():
            # Create comprehensive quantum optics analysis
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Photon Number Distribution',
                    'Second-Order Correlation g²(τ)',
                    'Quantum State Evolution',
                    'Nonlinear Conversion Efficiency'
                ),
                vertical_spacing=0.15,
                horizontal_spacing=0.1
            )

            # Photon number distribution
            n_max = 20
            n_values = np.arange(0, n_max)

            if light_source == "Coherent State (Laser)":
                # Poissonian distribution
                prob = np.exp(-photon_number) * photon_number**n_values / np.array([math.factorial(n) for n in n_values])
            elif light_source == "Thermal Light":
                # Bose-Einstein distribution
                prob = (photon_number/(1+photon_number))**n_values / (1+photon_number)
            elif light_source == "Single Photon":
                # Delta function at n=1
                prob = np.zeros(n_max)
                prob[1] = 1.0
            else:
                # Sub-Poissonian (squeezed)
                prob = np.exp(-photon_number) * photon_number**n_values / np.array([math.factorial(n) for n in n_values])
                prob *= np.exp(-0.5 * (n_values - photon_number)**2)  # Squeezing effect

            fig.add_trace(
                go.Bar(
                    x=n_values, y=prob,
                    name='P(n)',
                    marker_color='rgba(59, 130, 246, 0.7)',
                    hovertemplate='n: %{x}<br>P(n): %{y:.4f}<extra></extra>'
                ),
                row=1, col=1
            )

            # Second-order correlation function
            tau_values = np.linspace(-5, 5, 100)
            if light_source == "Coherent State (Laser)":
                g2_tau = np.ones_like(tau_values)
            elif light_source == "Thermal Light":
                g2_tau = 1 + np.exp(-np.abs(tau_values) / coherence_time)
            elif light_source == "Single Photon":
                g2_tau = np.where(np.abs(tau_values) < 0.1, 0, 1)
            else:
                g2_tau = 0.5 * (1 + np.exp(-np.abs(tau_values) / coherence_time))

            fig.add_trace(
                go.Scatter(
                    x=tau_values, y=g2_tau,
                    mode='lines',
                    line=dict(color='#dc2626', width=4),
                    name='g²(τ)',
                    hovertemplate='τ: %{x:.2f} ps<br>g²(τ): %{y:.3f}<extra></extra>'
                ),
                row=1, col=2
            )

            # Add antibunching/bunching indicators
            fig.add_hline(y=1, line=dict(color='black', width=2, dash='dash'), 
                         annotation_text="Classical limit", row=1, col=2)

            # Quantum state evolution (Bloch sphere projection)
            time_points = np.linspace(0, 2*np.pi, 100)
            qubit_x = np.cos(time_points)
            qubit_y = np.sin(time_points)

            fig.add_trace(
                go.Scatter(
                    x=qubit_x, y=qubit_y,
                    mode='lines+markers',
                    line=dict(color='#059669', width=3),
                    marker=dict(size=6),
                    name='State Evolution',
                    hovertemplate='x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>'
                ),
                row=2, col=1
            )

            # Add quantum gates effects
            fig.add_trace(
                go.Scatter(
                    x=[1, 0, -1, 0], y=[0, 1, 0, -1],
                    mode='markers',
                    marker=dict(size=12, color='red', symbol='star'),
                    name='Special States',
                    showlegend=False
                ),
                row=2, col=1
            )

            # Nonlinear conversion efficiency
            power_range = np.linspace(0.1, 100, 100)
            
            # Second harmonic generation efficiency
            shg_efficiency = np.sin(np.sqrt(power_range / 10))**2 * (power_range / 100)
            
            # Parametric down-conversion
            pdc_efficiency = 1 - np.exp(-power_range / 50)

            fig.add_trace(
                go.Scatter(
                    x=power_range, y=shg_efficiency * 100,
                    mode='lines',
                    line=dict(color='#7c3aed', width=3),
                    name='SHG Efficiency',
                    hovertemplate='Power: %{x:.1f} mW<br>Efficiency: %{y:.2f}%<extra></extra>'
                ),
                row=2, col=2
            )

            fig.add_trace(
                go.Scatter(
                    x=power_range, y=pdc_efficiency * 100,
                    mode='lines',
                    line=dict(color='#ea580c', width=3, dash='dot'),
                    name='PDC Efficiency',
                    hovertemplate='Power: %{x:.1f} mW<br>Efficiency: %{y:.2f}%<extra></extra>'
                ),
                row=2, col=2
            )

            # Mark current operating point
            current_shg = np.interp(pump_power, power_range, shg_efficiency * 100)
            fig.add_trace(
                go.Scatter(
                    x=[pump_power], y=[current_shg],
                    mode='markers',
                    marker=dict(size=12, color='yellow', symbol='star'),
                    name='Operating Point',
                    hovertemplate=f'Current: {current_shg:.2f}% efficiency<extra></extra>'
                ),
                row=2, col=2
            )

            # Update layout with enhanced visibility
            fig.update_layout(
                title=dict(
                    text=f'<b>Quantum Optics Analysis: {light_source}</b><br>'
                         f'<span style="font-size:16px; color:#1e40af;">Crystal: {crystal_type}, Power: {pump_power:.1f} mW</span>',
                    x=0.5,
                    font=dict(size=20, color='#1e293b', family='Inter')
                ),
                height=700,
                showlegend=True,
                legend=dict(x=1.02, y=1, font=dict(size=11)),
                plot_bgcolor='rgba(248,250,252,0.9)',
                annotations=[
                    dict(
                        text="Advanced Quantum Photonics",
                        x=0.5, y=1.02,
                        xref="paper", yref="paper",
                        showarrow=False,
                        font=dict(size=14, color='#64748b')
                    )
                ]
            )

            # Update axes with better visibility
            fig.update_xaxes(title_text="Photon Number", row=1, col=1)
            fig.update_yaxes(title_text="Probability", row=1, col=1)
            fig.update_xaxes(title_text="Delay τ (ps)", row=1, col=2)
            fig.update_yaxes(title_text="g²(τ)", row=1, col=2)
            fig.update_xaxes(title_text="State Space", row=2, col=1)
            fig.update_yaxes(title_text="State Space", row=2, col=1)
            fig.update_xaxes(title_text="Pump Power (mW)", row=2, col=2)
            fig.update_yaxes(title_text="Efficiency (%)", row=2, col=2)

            return fig

        quantum_fig = create_quantum_optics_visualization()
        st.plotly_chart(quantum_fig, use_container_width=True)

        # Quantum optics metrics
        st.markdown("#### 📊 Quantum Optics Metrics")

        # Calculate advanced quantum parameters
        mandel_q = (photon_number**2 - photon_number**2) / photon_number - 1  # Mandel Q parameter
        squeezing_dB = -10 * np.log10(0.5) if light_source == "Squeezed Light" else 0
        visibility = 0.99 if light_source == "Coherent State (Laser)" else 0.5
        fidelity = 0.95  # State preparation fidelity

        qo_col1, qo_col2, qo_col3, qo_col4 = st.columns(4)

        with qo_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{g2_value:.3f}</div>
                <div class="metric-label">g²(0) Correlation</div>
            </div>
            """, unsafe_allow_html=True)

        with qo_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{squeezing_dB:.1f}</div>
                <div class="metric-label">Squeezing (dB)</div>
            </div>
            """, unsafe_allow_html=True)

        with qo_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{visibility:.3f}</div>
                <div class="metric-label">Visibility</div>
            </div>
            """, unsafe_allow_html=True)

        with qo_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fidelity:.3f}</div>
                <div class="metric-label">State Fidelity</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[5]:
    st.info("Additional learning resources and concepts will be available here.")

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
           border-radius: 15px; text-align: center; border: 1px solid #bfdbfe;">
    <h3 style="color: #1e293b; margin-bottom: 1rem;">🔬 Advanced Optics Laboratory</h3>
    <p style="color: #64748b; margin-bottom: 1.5rem;">
        Explore the fascinating world of light through interactive simulations and comprehensive analysis tools.
    </p>
</div>
""", unsafe_allow_html=True)