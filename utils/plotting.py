"""
PhysicsMaster - Advanced Visualization & Plotting Utilities
Modern Glassmorphic Plotly Themes, 3D Vector Fields & Quantum Visualizers
"""

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def configure_plotting_style():
    """Configure default matplotlib and global plotting styles."""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12


def apply_glassmorphic_layout(fig, title="", height=500, dark_mode=False):
    """
    Apply a modern glassmorphic aesthetic to any Plotly figure.
    """
    bg_color = 'rgba(15, 23, 42, 0.75)' if dark_mode else 'rgba(255, 255, 255, 0.85)'
    paper_bg = 'rgba(0, 0, 0, 0)'
    grid_color = 'rgba(255, 255, 255, 0.1)' if dark_mode else 'rgba(0, 0, 0, 0.06)'
    text_color = '#f8fafc' if dark_mode else '#1e293b'
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=18, color=text_color, family='Inter, sans-serif'),
            x=0.5
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=paper_bg,
        font=dict(family='Inter, sans-serif', color=text_color),
        height=height,
        margin=dict(l=50, r=40, t=60, b=50),
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)' if dark_mode else 'rgba(255,255,255,0.85)',
            bordercolor='rgba(255,255,255,0.2)' if dark_mode else 'rgba(0,0,0,0.1)',
            borderwidth=1,
            font=dict(size=11, color=text_color)
        ),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=text_color)
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=text_color)
        )
    )
    return fig


def plot_bloch_magnetization_trajectory(bloch_data, title="3D Magnetization Trajectory M(t) on Bloch Sphere"):
    """
    Plot the 3D trajectory of magnetization vector M(t) = (Mx, My, Mz) on the unit sphere.
    """
    t = bloch_data["time"]
    Mx = bloch_data["Mx"]
    My = bloch_data["My"]
    Mz = bloch_data["Mz"]
    
    fig = go.Figure()
    
    # 1. Semi-transparent Bloch Sphere reference surface
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        opacity=0.15,
        colorscale=[[0, 'rgba(99,102,241,0.2)'], [1, 'rgba(168,85,247,0.2)']],
        showscale=False,
        name='Bloch Sphere |M|=M0',
        hoverinfo='skip'
    ))
    
    # 2. 3D Trajectory Curve
    fig.add_trace(go.Scatter3d(
        x=Mx, y=My, z=Mz,
        mode='lines',
        line=dict(
            color=t,
            colorscale='Viridis',
            width=6,
            cmin=float(np.min(t)),
            cmax=float(np.max(t)),
            colorbar=dict(
                title=dict(text="Time (ms)", font=dict(color='#94a3b8', size=12)),
                thickness=12,
                len=0.6,
                x=1.05
            )
        ),
        name='Trajectory M(t)',
        hovertemplate='t: %{line.color:.1f} ms<br>Mx: %{x:.2f}<br>My: %{y:.2f}<br>Mz: %{z:.2f}<extra></extra>'
    ))
    
    # 3. Final Magnetization Vector Arrow / Marker
    fig.add_trace(go.Scatter3d(
        x=[0, Mx[-1]], y=[0, My[-1]], z=[0, Mz[-1]],
        mode='lines+markers',
        line=dict(color='#ef4444', width=8),
        marker=dict(size=[4, 9], color='#ef4444', symbol='diamond'),
        name='Final Magnetization'
    ))
    
    # Coordinate Axes
    fig.add_trace(go.Scatter3d(
        x=[-1.2, 1.2, None, 0, 0, None, 0, 0],
        y=[0, 0, None, -1.2, 1.2, None, 0, 0],
        z=[0, 0, None, 0, 0, None, -1.2, 1.2],
        mode='lines+text',
        line=dict(color='rgba(148,163,184,0.4)', width=2, dash='dash'),
        text=['-X', '+X (B1)', '', '-Y', '+Y', '', '-Z', '+Z (B0)'],
        textposition='top center',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>"),
        scene=dict(
            xaxis=dict(title='Mx (Transverse)', backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(title='My (Transverse)', backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(title='Mz (Longitudinal)', backgroundcolor='rgba(0,0,0,0)'),
            aspectmode='cube',
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.3))
        ),
        height=540,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig


def plot_bloch_sphere_state(theta, phi, state_label=r"|\psi\rangle"):
    """
    Plot a quantum 2-level state on the Bloch Sphere:
    |psi> = cos(theta/2)|0> + exp(i*phi)*sin(theta/2)|1>.
    """
    fig = go.Figure()
    
    # Wireframe Sphere
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        opacity=0.2,
        colorscale=[[0, 'rgba(59,130,246,0.3)'], [1, 'rgba(147,197,253,0.3)']],
        showscale=False,
        name='Bloch Sphere'
    ))
    
    # State Vector coordinates
    x_s = np.sin(theta) * np.cos(phi)
    y_s = np.sin(theta) * np.sin(phi)
    z_s = np.cos(theta)
    
    # Arrow from center to state
    fig.add_trace(go.Scatter3d(
        x=[0, x_s], y=[0, y_s], z=[0, z_s],
        mode='lines+markers',
        line=dict(color='#ef4444', width=8),
        marker=dict(size=[4, 10], color='#ef4444', symbol='diamond'),
        name=f'State {state_label}'
    ))
    
    # Poles |0> and |1>
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[1.15, -1.15],
        mode='text',
        text=['|0⟩ (North)', '|1⟩ (South)'],
        textposition='top center',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>Quantum 2-Level State on Bloch Sphere</b> (θ = {np.degrees(theta):.1f}°, φ = {np.degrees(phi):.1f}°)",
            font=dict(size=16, color='#1e293b')
        ),
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z (|0⟩ to |1⟩)',
            aspectmode='cube'
        ),
        width=700,
        height=550,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    return fig


def plot_wave_interference(k1, k2, phase_diff, amp1=1.0, amp2=1.0):
    """Create an interactive plot showing interference between two waves."""
    x = np.linspace(0, 10, 500)
    t = np.linspace(0, 2, 40)

    fig = go.Figure(frames=[
        go.Frame(
            data=[
                go.Scatter(x=x, y=amp1*np.sin(k1*x - 2*time), mode='lines', line=dict(color='#3b82f6', width=1.5), name='Wave 1'),
                go.Scatter(x=x, y=amp2*np.sin(k2*x - 2*time + phase_diff), mode='lines', line=dict(color='#ef4444', width=1.5), name='Wave 2'),
                go.Scatter(x=x, y=amp1*np.sin(k1*x - 2*time) + amp2*np.sin(k2*x - 2*time + phase_diff), mode='lines', line=dict(color='#10b981', width=3), name='Resultant')
            ],
            name=f"frame{i}"
        )
        for i, time in enumerate(t)
    ])

    fig.add_trace(go.Scatter(x=x, y=amp1*np.sin(k1*x), mode='lines', line=dict(color='#3b82f6', width=1.5), name='Wave 1'))
    fig.add_trace(go.Scatter(x=x, y=amp2*np.sin(k2*x + phase_diff), mode='lines', line=dict(color='#ef4444', width=1.5), name='Wave 2'))
    fig.add_trace(go.Scatter(x=x, y=amp1*np.sin(k1*x) + amp2*np.sin(k2*x + phase_diff), mode='lines', line=dict(color='#10b981', width=3), name='Resultant'))

    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': '▶️ Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 60, 'redraw': True}, 'fromcurrent': True}]
            }]
        }],
        title=f'Wave Superposition & Interference (k₁={k1:.1f}, k₂={k2:.1f}, Δφ={phase_diff:.2f} rad)',
        xaxis_title='Position (x)',
        yaxis_title='Amplitude',
        height=450
    )
    return fig


def plot_band_structure(k_path, valence_band, conduction_band, fermi_level, 
                      material, bandgap, is_direct, high_symmetry_points=None):
    """Create an interactive plot of electronic band structure."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=k_path, y=valence_band,
        mode='lines', name='Valence Band (VB)',
        line=dict(color='#3b82f6', width=3.5)
    ))

    fig.add_trace(go.Scatter(
        x=k_path, y=conduction_band,
        mode='lines', name='Conduction Band (CB)',
        line=dict(color='#ef4444', width=3.5)
    ))

    fig.add_trace(go.Scatter(
        x=k_path, y=[fermi_level] * len(k_path),
        mode='lines', name='Fermi Level (E_F)',
        line=dict(color='#10b981', width=2, dash='dash')
    ))

    fig.update_layout(
        title=f'Band Structure of {material} ({"Direct" if is_direct else "Indirect"} Bandgap: {bandgap:.2f} eV)',
        xaxis_title='Wavevector k (π/a)',
        yaxis_title='Energy E (eV)',
        height=480
    )
    return fig


def plot_semiconductor_carriers(doping_type, n0, p0, position, electrons, holes, electric_field=0):
    """Create an interactive plot of carrier distributions in semiconductor."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=position, y=electrons,
        mode='lines', name='Electrons (n)',
        line=dict(color='#3b82f6', width=2.5)
    ))

    fig.add_trace(go.Scatter(
        x=position, y=holes,
        mode='lines', name='Holes (p)',
        line=dict(color='#ef4444', width=2.5)
    ))

    fig.update_layout(
        title=f'Carrier Distribution in {doping_type} Semiconductor (E = {electric_field} V/cm)',
        xaxis_title='Position (µm)',
        yaxis_title='Carrier Concentration (cm⁻³)',
        yaxis_type='log',
        height=400
    )
    return fig


def nuclear_fission_animation(frames=30):
    """Create an animation showing nuclear fission process."""
    fig = go.Figure(frames=[
        go.Frame(
            data=[
                go.Scatter3d(
                    x=[0], y=[0], z=[0],
                    mode='markers',
                    marker=dict(size=max(5, 20-i*20/frames), color='#dc2626'),
                    name='Parent Nucleus'
                ),
                go.Scatter3d(
                    x=[-i*0.25] if i > frames/4 else [],
                    y=[i*0.1-0.5] if i > frames/4 else [],
                    z=[i*0.05] if i > frames/4 else [],
                    mode='markers',
                    marker=dict(size=12, color='#2563eb'),
                    name='Fission Fragment 1'
                ),
                go.Scatter3d(
                    x=[i*0.25] if i > frames/4 else [],
                    y=[i*0.1+0.5] if i > frames/4 else [],
                    z=[-i*0.05] if i > frames/4 else [],
                    mode='markers',
                    marker=dict(size=12, color='#7c3aed'),
                    name='Fission Fragment 2'
                ),
                go.Scatter3d(
                    x=[i*0.35, -i*0.3, i*0.15] if i > frames/3 else [],
                    y=[i*0.35, i*0.3, -i*0.35] if i > frames/3 else [],
                    z=[i*0.35, i*0.4, i*0.38] if i > frames/3 else [],
                    mode='markers',
                    marker=dict(size=6, color='#10b981'),
                    name='Prompt Neutrons'
                )
            ],
            name=f"frame{i}"
        )
        for i in range(frames)
    ])

    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=20, color='#dc2626'), name='Parent Nucleus'))

    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': '▶️ Play Fission',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 80, 'redraw': True}, 'fromcurrent': True}]
            }]
        }],
        title='Nuclear Fission Dynamics & Prompt Neutron Emission',
        scene=dict(
            xaxis=dict(range=[-10, 10], showticklabels=False),
            yaxis=dict(range=[-10, 10], showticklabels=False),
            zaxis=dict(range=[-10, 10], showticklabels=False)
        ),
        height=500
    )
    return fig


def plot_decay(initial_amount, half_life, time_range):
    """Create a plot of radioactive decay."""
    times = np.linspace(0, time_range, 150)
    decay_constant = np.log(2) / max(half_life, 1e-6)
    amounts = initial_amount * np.exp(-decay_constant * times)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=amounts, mode='lines', name='Active Nuclei N(t)', line=dict(color='#2563eb', width=3)))

    t_half = half_life
    remaining = initial_amount / 2
    hl_times, hl_amounts = [], []
    while t_half <= time_range:
        hl_times.append(t_half)
        hl_amounts.append(remaining)
        t_half += half_life
        remaining /= 2

    fig.add_trace(go.Scatter(x=hl_times, y=hl_amounts, mode='markers', name='Half-Life Points (t₁/₂)', marker=dict(size=10, color='#dc2626', symbol='diamond')))

    fig.update_layout(
        title=f'Radioactive Decay Kinetics (t₁/₂ = {half_life} s)',
        xaxis_title='Time (s)',
        yaxis_title='Remaining Quantity N(t)',
        height=420
    )
    return fig