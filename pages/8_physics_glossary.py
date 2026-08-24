
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import time
import pandas as pd

st.set_page_config(
    page_title="Interactive Physics Glossary",
    page_icon="📚",
    layout="wide"
)

# Enhanced CSS for glossary with better animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    /* Glossary header with animated background */
    .glossary-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
    }
    
    .glossary-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.08) 0%, transparent 50%),
            linear-gradient(45deg, rgba(255,255,255,0.05) 25%, transparent 25%);
        animation: glossaryParticles 20s linear infinite;
    }
    
    .glossary-hero h1, .glossary-hero p {
        position: relative;
        z-index: 2;
        color: white;
        margin: 0;
    }
    
    /* Concept cards with enhanced styling */
    .concept-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .concept-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .concept-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        animation: conceptGradient 3s ease-in-out infinite;
    }
    
    .concept-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .concept-icon {
        font-size: 2.5rem;
        animation: iconFloat 3s ease-in-out infinite;
    }
    
    .concept-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
    }
    
    .concept-category {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: auto;
    }
    
    .concept-definition {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    
    .concept-formula {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1rem;
        color: #1e293b;
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    /* Animation controls */
    .animation-controls {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #cbd5e1;
    }
    
    .animation-controls h4 {
        color: #334155;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Search and filter styling */
    .search-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Animations */
    @keyframes glossaryParticles {
        0% { transform: translateX(0px) rotate(0deg); }
        25% { transform: translateX(-20px) rotate(90deg); }
        50% { transform: translateX(0px) rotate(180deg); }
        75% { transform: translateX(20px) rotate(270deg); }
        100% { transform: translateX(0px) rotate(360deg); }
    }
    
    @keyframes conceptGradient {
        0%, 100% { background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c); }
        25% { background: linear-gradient(90deg, #764ba2, #f093fb, #f5576c, #667eea); }
        50% { background: linear-gradient(90deg, #f093fb, #f5576c, #667eea, #764ba2); }
        75% { background: linear-gradient(90deg, #f5576c, #667eea, #764ba2, #f093fb); }
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .glossary-hero {
            padding: 2rem 1rem;
        }
        
        .concept-card {
            padding: 1.5rem;
        }
        
        .concept-header {
            flex-direction: column;
            text-align: center;
        }
        
        .concept-category {
            margin-left: 0;
            margin-top: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def create_wave_animation():
    """Create animated wave visualization"""
    x = np.linspace(0, 4*np.pi, 200)
    frames = 50
    
    fig_frames = []
    for i in range(frames):
        t = 2*np.pi*i/frames
        y = np.sin(x - t)
        
        fig_frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=x, y=y,
                        mode='lines',
                        line=dict(color='#667eea', width=4),
                        fill='tozeroy',
                        fillcolor='rgba(102, 126, 234, 0.3)',
                        name='Wave'
                    )
                ],
                name=f"frame{i}"
            )
        )
    
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x, y=np.sin(x),
                mode='lines',
                line=dict(color='#667eea', width=4),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.3)',
                name='Wave'
            )
        ],
        frames=fig_frames
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Wave Propagation</b>",
            x=0.5,
            font=dict(size=18, color='#1e293b')
        ),
        xaxis_title="Position",
        yaxis_title="Amplitude",
        height=400,
        plot_bgcolor='rgba(248, 250, 252, 0.9)',
        paper_bgcolor='white',
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': '▶ Play Animation',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 100, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate'
                }]
            }, {
                'label': '⏸ Pause',
                'method': 'animate',
                'args': [[None], {
                    'frame': {'duration': 0, 'redraw': False},
                    'mode': 'immediate'
                }]
            }]
        }]
    )
    
    return fig

def create_orbit_animation():
    """Create planetary orbit animation"""
    theta = np.linspace(0, 2*np.pi, 100)
    orbit_x = np.cos(theta)
    orbit_y = np.sin(theta)
    
    frames = 60
    fig_frames = []
    
    for i in range(frames):
        angle = 2*np.pi*i/frames
        planet_x = np.cos(angle)
        planet_y = np.sin(angle)
        
        fig_frames.append(
            go.Frame(
                data=[
                    # Sun
                    go.Scatter(
                        x=[0], y=[0],
                        mode='markers',
                        marker=dict(size=20, color='#fbbf24', symbol='star'),
                        name='Star'
                    ),
                    # Orbit path
                    go.Scatter(
                        x=orbit_x, y=orbit_y,
                        mode='lines',
                        line=dict(color='rgba(156, 163, 175, 0.5)', width=2, dash='dash'),
                        name='Orbit',
                        showlegend=False
                    ),
                    # Planet
                    go.Scatter(
                        x=[planet_x], y=[planet_y],
                        mode='markers',
                        marker=dict(size=12, color='#3b82f6'),
                        name='Planet'
                    )
                ],
                name=f"frame{i}"
            )
        )
    
    fig = go.Figure(
        data=[
            go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=20, color='#fbbf24', symbol='star'), name='Star'),
            go.Scatter(x=orbit_x, y=orbit_y, mode='lines', line=dict(color='rgba(156, 163, 175, 0.5)', width=2, dash='dash'), name='Orbit', showlegend=False),
            go.Scatter(x=[1], y=[0], mode='markers', marker=dict(size=12, color='#3b82f6'), name='Planet')
        ],
        frames=fig_frames
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Gravitational Orbit</b>",
            x=0.5,
            font=dict(size=18, color='#1e293b')
        ),
        xaxis=dict(range=[-1.5, 1.5], title="Position X"),
        yaxis=dict(range=[-1.5, 1.5], title="Position Y"),
        height=400,
        plot_bgcolor='rgba(248, 250, 252, 0.9)',
        paper_bgcolor='white',
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': '▶ Play Animation',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 150, 'redraw': True},
                    'fromcurrent': True,
                    'mode': 'immediate'
                }]
            }]
        }]
    )
    
    return fig

def create_electric_field_visualization():
    """Create 3D electric field visualization"""
    # Create a grid of points
    x = np.linspace(-2, 2, 10)
    y = np.linspace(-2, 2, 10)
    X, Y = np.meshgrid(x, y)
    
    # Point charge at origin
    charge_pos = [0, 0]
    
    # Calculate electric field vectors
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    
    for i in range(len(x)):
        for j in range(len(y)):
            if X[i,j] == 0 and Y[i,j] == 0:
                continue
            r = np.sqrt(X[i,j]**2 + Y[i,j]**2)
            Ex[i,j] = X[i,j] / r**3
            Ey[i,j] = Y[i,j] / r**3
    
    fig = go.Figure()
    
    # Add electric field vectors
    for i in range(0, len(x), 2):
        for j in range(0, len(y), 2):
            if X[i,j] == 0 and Y[i,j] == 0:
                continue
            
            fig.add_trace(
                go.Scatter(
                    x=[X[i,j], X[i,j] + 0.3*Ex[i,j]],
                    y=[Y[i,j], Y[i,j] + 0.3*Ey[i,j]],
                    mode='lines',
                    line=dict(color='#ef4444', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )
            
            # Add arrowheads
            fig.add_trace(
                go.Scatter(
                    x=[X[i,j] + 0.3*Ex[i,j]],
                    y=[Y[i,j] + 0.3*Ey[i,j]],
                    mode='markers',
                    marker=dict(
                        symbol='triangle-up',
                        size=8,
                        color='#ef4444',
                        angle=np.degrees(np.arctan2(Ey[i,j], Ex[i,j]))
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )
    
    # Add point charge
    fig.add_trace(
        go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=15, color='#fbbf24', symbol='circle', line=dict(color='black', width=2)),
            name='Point Charge (+)',
            hovertemplate='Positive Point Charge<extra></extra>'
        )
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Electric Field of Point Charge</b>",
            x=0.5,
            font=dict(size=18, color='#1e293b')
        ),
        xaxis=dict(range=[-2.5, 2.5], title="Position X"),
        yaxis=dict(range=[-2.5, 2.5], title="Position Y"),
        height=500,
        plot_bgcolor='rgba(248, 250, 252, 0.9)',
        paper_bgcolor='white'
    )
    
    return fig

def create_photon_visualization():
    """Create 3D photon wave packet visualization"""
    x = np.linspace(-5, 5, 200)
    
    # Photon wave packet
    k0 = 3  # Central wave number
    sigma = 1  # Packet width
    
    envelope = np.exp(-(x**2)/(2*sigma**2))
    wave = np.cos(k0*x)
    photon_packet = envelope * wave
    
    fig = go.Figure()
    
    # Add wave packet
    fig.add_trace(
        go.Scatter(
            x=x, y=photon_packet,
            mode='lines',
            line=dict(color='#a855f7', width=4),
            fill='tozeroy',
            fillcolor='rgba(168, 85, 247, 0.3)',
            name='Photon Wave Packet'
        )
    )
    
    # Add envelope
    fig.add_trace(
        go.Scatter(
            x=x, y=envelope,
            mode='lines',
            line=dict(color='#ef4444', width=2, dash='dash'),
            name='Envelope'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=x, y=-envelope,
            mode='lines',
            line=dict(color='#ef4444', width=2, dash='dash'),
            showlegend=False
        )
    )
    
    fig.update_layout(
        title=dict(
            text="<b>Photon Wave-Particle Duality</b>",
            x=0.5,
            font=dict(size=18, color='#1e293b')
        ),
        xaxis_title="Position",
        yaxis_title="Amplitude",
        height=400,
        plot_bgcolor='rgba(248, 250, 252, 0.9)',
        paper_bgcolor='white'
    )
    
    return fig

def main():
    # Hero Section
    st.markdown("""
    <div class="glossary-hero">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">📚 Interactive Physics Glossary</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Explore physics concepts through 3D animations and interactive visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and Filter Section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search physics concepts...", placeholder="Enter concept name (e.g., wave, gravity, photon)")
    
    with col2:
        category = st.selectbox("📂 Category", [
            "All Concepts", "Mechanics", "Waves", "Electromagnetism", 
            "Quantum Physics", "Thermodynamics", "Optics", "Nuclear Physics"
        ])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Physics Concepts Database
    physics_concepts = {
        "Wave": {
            "category": "Waves",
            "definition": "A wave is a disturbance that transfers energy through space or matter without transferring mass. Waves are characterized by their amplitude, wavelength, frequency, and speed.",
            "formula": "v = fλ (wave speed = frequency × wavelength)",
            "animation": "wave",
            "icon": "🌊"
        },
        "Gravity": {
            "category": "Mechanics",
            "definition": "Gravity is a fundamental force that attracts objects with mass toward each other. It's responsible for planetary orbits, tides, and keeping objects grounded on Earth.",
            "formula": "F = G(m₁m₂)/r² (Newton's law of universal gravitation)",
            "animation": "orbit",
            "icon": "🌍"
        },
        "Electric Field": {
            "category": "Electromagnetism",
            "definition": "An electric field is a region around charged particles where other charged particles experience a force. The field strength decreases with distance from the source charge.",
            "formula": "E = F/q = kQ/r² (electric field strength)",
            "animation": "electric_field",
            "icon": "⚡"
        },
        "Photon": {
            "category": "Quantum Physics",
            "definition": "A photon is a quantum of electromagnetic energy, exhibiting both wave and particle properties. Photons are massless particles that travel at the speed of light.",
            "formula": "E = hf = hc/λ (photon energy)",
            "animation": "photon",
            "icon": "💡"
        },
        "Momentum": {
            "category": "Mechanics",
            "definition": "Momentum is the quantity of motion of a moving body, calculated as the product of mass and velocity. It's conserved in isolated systems.",
            "formula": "p = mv (linear momentum)",
            "animation": None,
            "icon": "⚽"
        },
        "Energy": {
            "category": "Mechanics",
            "definition": "Energy is the capacity to do work or cause change. It exists in various forms including kinetic, potential, thermal, and electromagnetic energy.",
            "formula": "E = mc² (mass-energy equivalence)",
            "animation": None,
            "icon": "⚡"
        },
        "Entropy": {
            "category": "Thermodynamics",
            "definition": "Entropy is a measure of the disorder or randomness in a system. According to the second law of thermodynamics, entropy always increases in isolated systems.",
            "formula": "S = k ln(W) (Boltzmann entropy formula)",
            "animation": None,
            "icon": "🌡️"
        },
        "Interference": {
            "category": "Waves",
            "definition": "Wave interference occurs when two or more waves overlap in space, creating patterns of constructive and destructive interference based on their phase relationship.",
            "formula": "Δ = |x₁ - x₂| (path difference)",
            "animation": None,
            "icon": "〰️"
        }
    }
    
    # Filter concepts based on search and category
    filtered_concepts = {}
    for name, concept in physics_concepts.items():
        if category == "All Concepts" or concept["category"] == category:
            if not search_term or search_term.lower() in name.lower():
                filtered_concepts[name] = concept
    
    # Display concepts
    for name, concept in filtered_concepts.items():
        st.markdown(f"""
        <div class="concept-card">
            <div class="concept-header">
                <div class="concept-icon">{concept['icon']}</div>
                <h2 class="concept-title">{name}</h2>
                <div class="concept-category">{concept['category']}</div>
            </div>
            <div class="concept-definition">
                {concept['definition']}
            </div>
            <div class="concept-formula">
                <strong>Key Formula:</strong> {concept['formula']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add interactive visualization if available
        if concept.get("animation"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if concept["animation"] == "wave":
                    wave_fig = create_wave_animation()
                    st.plotly_chart(wave_fig, use_container_width=True)
                elif concept["animation"] == "orbit":
                    orbit_fig = create_orbit_animation()
                    st.plotly_chart(orbit_fig, use_container_width=True)
                elif concept["animation"] == "electric_field":
                    field_fig = create_electric_field_visualization()
                    st.plotly_chart(field_fig, use_container_width=True)
                elif concept["animation"] == "photon":
                    photon_fig = create_photon_visualization()
                    st.plotly_chart(photon_fig, use_container_width=True)
            
            with col2:
                st.markdown("""
                <div class="animation-controls">
                    <h4>🎮 Interactive Controls</h4>
                    <p>Use the play button to start the animation and explore the physics concept in motion.</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Footer with additional resources
    st.markdown("""
    <div style="margin-top: 3rem; padding: 2rem; background: white; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <h3 style="color: #1e293b; margin-bottom: 1rem;">📖 Continue Learning</h3>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Explore our interactive physics simulations to deepen your understanding of these concepts.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Solid State Physics</span>
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Optics & Photonics</span>
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Nuclear Physics</span>
            <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Superconductivity</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
