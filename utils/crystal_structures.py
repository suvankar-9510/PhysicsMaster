"""
PhysicsMaster - Crystal Structures, Lattices & Brillouin Zone Geometry
Graduate & M.Sc Standard 3D Crystallographic Models & Reciprocal Space Solvers
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================================
# 1. 3D REAL-SPACE CRYSTAL GENERATORS
# ============================================================================

def generate_simple_cubic(a=1.0, n_cells=2):
    """Generate coordinates for a simple cubic lattice."""
    points = []
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                points.append([i * a, j * a, k * a])
    return np.array(points, dtype=float)


def generate_bcc(a=1.0, n_cells=2):
    """Generate coordinates for a body-centered cubic (BCC) lattice."""
    corners = []
    centers = []
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                corners.append([i * a, j * a, k * a])
    for i in range(max(1, n_cells - 1)):
        for j in range(max(1, n_cells - 1)):
            for k in range(max(1, n_cells - 1)):
                centers.append([(i + 0.5) * a, (j + 0.5) * a, (k + 0.5) * a])
    if not centers:
        centers.append([0.5 * a, 0.5 * a, 0.5 * a])
    return np.vstack([corners, centers])


def generate_fcc(a=1.0, n_cells=2):
    """Generate coordinates for a face-centered cubic (FCC) lattice."""
    corners = []
    faces = []
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                corners.append([i * a, j * a, k * a])
                
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                if k < n_cells:
                    faces.append([(i + 0.5) * a, (j + 0.5) * a, k * a])
                if j < n_cells:
                    faces.append([(i + 0.5) * a, j * a, (k + 0.5) * a])
                if i < n_cells:
                    faces.append([i * a, (j + 0.5) * a, (k + 0.5) * a])
                    
    return np.vstack([corners, faces])


def generate_diamond_cubic(a=1.0, n_cells=2):
    """
    Generate coordinates for the Diamond Cubic lattice (e.g. C, Si, Ge).
    FCC Bravais lattice with 2-atom basis: (0,0,0) and (1/4, 1/4, 1/4).
    """
    fcc_pts = generate_fcc(a, n_cells)
    basis_shift = np.array([0.25 * a, 0.25 * a, 0.25 * a])
    sublattice_2 = fcc_pts + basis_shift
    return np.vstack([fcc_pts, sublattice_2])


def generate_zincblende(a=1.0, n_cells=2):
    """
    Generate Zincblende (GaAs) crystal structure:
    FCC lattice of Ga atoms + FCC lattice of As atoms shifted by (a/4, a/4, a/4).
    Returns (Ga_points, As_points).
    """
    ga_pts = generate_fcc(a, n_cells)
    as_pts = ga_pts + np.array([0.25 * a, 0.25 * a, 0.25 * a])
    return ga_pts, as_pts


def generate_nacl(a=1.0, n_cells=2):
    """
    Generate Rocksalt (NaCl) crystal structure:
    FCC lattice of Na + FCC lattice of Cl shifted by (a/2, 0, 0).
    Returns (Na_points, Cl_points).
    """
    na_pts = generate_fcc(a, n_cells)
    cl_pts = na_pts + np.array([0.5 * a, 0.0, 0.0])
    return na_pts, cl_pts


def generate_cscl(a=1.0, n_cells=2):
    """
    Generate CsCl structure:
    Cs at simple cubic corners, Cl at cube centers.
    Returns (Cs_points, Cl_points).
    """
    cs_pts = generate_simple_cubic(a, n_cells)
    cl_pts = cs_pts + np.array([0.5 * a, 0.5 * a, 0.5 * a])
    return cs_pts, cl_pts


def generate_hcp(a=1.0, c_over_a=1.633, n_cells=2):
    """
    Generate Hexagonal Close-Packed (HCP) lattice with ABAB layer stacking.
    """
    c = a * c_over_a
    points = []
    # Layer A at z = 0, c, 2c...
    # Layer B at z = c/2, 3c/2... shifted by (a/2, a/(2*sqrt(3)))
    for k in range(n_cells):
        z_A = k * c
        z_B = (k + 0.5) * c
        for i in range(n_cells):
            for j in range(n_cells):
                # Triangular basis vectors
                x_A = i * a + j * 0.5 * a
                y_A = j * np.sqrt(3.0) / 2.0 * a
                points.append([x_A, y_A, z_A])
                
                x_B = x_A + 0.5 * a
                y_B = y_A + (a / (2.0 * np.sqrt(3.0)))
                points.append([x_B, y_B, z_B])
                
    return np.array(points, dtype=float)


def generate_perovskite(a=1.0, n_cells=1):
    """
    Generate Perovskite (ABO3, e.g. BaTiO3 / SrTiO3) structure:
    A (Ba) at corners (0,0,0)
    B (Ti) at body center (1/2, 1/2, 1/2)
    O at face centers (1/2, 1/2, 0), (1/2, 0, 1/2), (0, 1/2, 1/2)
    Returns (A_points, B_points, O_points).
    """
    A_pts = []
    B_pts = []
    O_pts = []
    
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                # A cation at corners
                A_pts.append([i * a, j * a, k * a])
                # B cation at body center
                B_pts.append([(i + 0.5) * a, (j + 0.5) * a, (k + 0.5) * a])
                # Oxygen at face centers
                O_pts.append([(i + 0.5) * a, (j + 0.5) * a, k * a])
                O_pts.append([(i + 0.5) * a, j * a, (k + 0.5) * a])
                O_pts.append([i * a, (j + 0.5) * a, (k + 0.5) * a])
                
    return np.array(A_pts), np.array(B_pts), np.array(O_pts)


# ============================================================================
# 2. RECIPROCAL SPACE & 3D FIRST BRILLOUIN ZONE
# ============================================================================

def create_3d_brillouin_zone(lattice_type="FCC", k_scale=1.0):
    """
    Construct the 3D First Brillouin Zone polyhedron and high-symmetry k-points.
    - SC (Real) -> SC (Reciprocal): Cube
    - FCC (Real) -> BCC (Reciprocal): Truncated Octahedron (14 faces: 8 hexagons, 6 squares)
    - BCC (Real) -> FCC (Reciprocal): Rhombic Dodecahedron (12 rhombic faces)
    
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    if lattice_type == "FCC":
        # First Brillouin Zone for FCC is a Truncated Octahedron in reciprocal space
        # High symmetry points: Gamma=(0,0,0), X=(1,0,0), L=(0.5, 0.5, 0.5), W=(1, 0.5, 0), K=(0.75, 0.75, 0)
        scale = 2.0 * np.pi * k_scale
        
        # 24 vertices of truncated octahedron: all permutations of (0, +-1, +-2)*scale/2
        vertices = []
        for x in [-1, 1]:
            for y in [-2, 2]:
                vertices.extend([[0, x*0.5*scale, y*0.5*scale], [x*0.5*scale, 0, y*0.5*scale], [x*0.5*scale, y*0.5*scale, 0]])
        vertices = np.unique(np.array(vertices), axis=0)
        
        # Mesh surface representing the truncated octahedron
        # Define the 14 faces via Delaunay / Convex hull approximation
        x_v, y_v, z_v = vertices[:, 0], vertices[:, 1], vertices[:, 2]
        
        fig.add_trace(go.Mesh3d(
            x=x_v, y=y_v, z=z_v,
            alphahull=0,
            opacity=0.35,
            color='#3b82f6',
            name='1st Brillouin Zone (Truncated Octahedron)',
            hoverinfo='skip'
        ))
        
        # Add High Symmetry Points
        hs_points = {
            r"$\Gamma$ (0,0,0)": [0, 0, 0],
            "X (2π/a, 0, 0)": [scale * 0.5, 0, 0],
            "L (π/a, π/a, π/a)": [scale * 0.25, scale * 0.25, scale * 0.25],
            "W (2π/a, π/a, 0)": [scale * 0.5, scale * 0.25, 0],
            "K (3π/2a, 3π/2a, 0)": [scale * 0.375, scale * 0.375, 0]
        }
        
        for name, pt in hs_points.items():
            fig.add_trace(go.Scatter3d(
                x=[pt[0]], y=[pt[1]], z=[pt[2]],
                mode='markers+text',
                marker=dict(size=8, color='#ef4444' if pt == [0,0,0] else '#f59e0b', symbol='diamond'),
                text=[name],
                textposition='top center',
                name=name
            ))
            
        # Draw high-symmetry path: Gamma -> X -> W -> K -> Gamma -> L
        path = np.array([
            [0, 0, 0],
            [scale * 0.5, 0, 0],
            [scale * 0.5, scale * 0.25, 0],
            [scale * 0.375, scale * 0.375, 0],
            [0, 0, 0],
            [scale * 0.25, scale * 0.25, scale * 0.25]
        ])
        fig.add_trace(go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode='lines',
            line=dict(color='#10b981', width=5),
            name='High-Symmetry Path (Γ-X-W-K-Γ-L)'
        ))
        
        title_str = "<b>FCC 1st Brillouin Zone (Reciprocal BCC - Truncated Octahedron)</b>"
        
    elif lattice_type == "BCC":
        # First Brillouin Zone for BCC is a Rhombic Dodecahedron (12 faces)
        scale = 2.0 * np.pi * k_scale
        # 14 vertices: 8 of type (+-0.5, +-0.5, +-0.5), 6 of type (+-1, 0, 0)
        v1 = []
        for x in [-0.5, 0.5]:
            for y in [-0.5, 0.5]:
                for z in [-0.5, 0.5]:
                    v1.append([x * scale, y * scale, z * scale])
        v2 = [
            [scale, 0, 0], [-scale, 0, 0],
            [0, scale, 0], [0, -scale, 0],
            [0, 0, scale], [0, 0, -scale]
        ]
        vertices = np.vstack([v1, v2])
        
        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
            alphahull=0,
            opacity=0.35,
            color='#8b5cf6',
            name='1st Brillouin Zone (Rhombic Dodecahedron)',
            hoverinfo='skip'
        ))
        
        hs_points = {
            r"$\Gamma$ (0,0,0)": [0, 0, 0],
            "H (0, 2π/a, 0)": [0, scale, 0],
            "P (π/a, π/a, π/a)": [scale * 0.5, scale * 0.5, scale * 0.5],
            "N (π/a, π/a, 0)": [scale * 0.5, scale * 0.5, 0]
        }
        for name, pt in hs_points.items():
            fig.add_trace(go.Scatter3d(
                x=[pt[0]], y=[pt[1]], z=[pt[2]],
                mode='markers+text',
                marker=dict(size=8, color='#ef4444' if pt == [0,0,0] else '#f59e0b', symbol='diamond'),
                text=[name],
                textposition='top center',
                name=name
            ))
            
        path = np.array([
            [0, 0, 0],
            [0, scale, 0],
            [scale * 0.5, scale * 0.5, scale * 0.5],
            [0, 0, 0],
            [scale * 0.5, scale * 0.5, 0]
        ])
        fig.add_trace(go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode='lines',
            line=dict(color='#10b981', width=5),
            name='High-Symmetry Path (Γ-H-P-Γ-N)'
        ))
        title_str = "<b>BCC 1st Brillouin Zone (Reciprocal FCC - Rhombic Dodecahedron)</b>"
        
    else:  # Simple Cubic
        scale = np.pi * k_scale
        # Cube from -scale to +scale
        v = []
        for x in [-scale, scale]:
            for y in [-scale, scale]:
                for z in [-scale, scale]:
                    v.append([x, y, z])
        vertices = np.array(v)
        
        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
            alphahull=0,
            opacity=0.35,
            color='#06b6d4',
            name='1st Brillouin Zone (Cube)',
            hoverinfo='skip'
        ))
        
        hs_points = {
            r"$\Gamma$ (0,0,0)": [0, 0, 0],
            "X (π/a, 0, 0)": [scale, 0, 0],
            "M (π/a, π/a, 0)": [scale, scale, 0],
            "R (π/a, π/a, π/a)": [scale, scale, scale]
        }
        for name, pt in hs_points.items():
            fig.add_trace(go.Scatter3d(
                x=[pt[0]], y=[pt[1]], z=[pt[2]],
                mode='markers+text',
                marker=dict(size=8, color='#ef4444' if pt == [0,0,0] else '#f59e0b', symbol='diamond'),
                text=[name],
                textposition='top center',
                name=name
            ))
            
        path = np.array([
            [0, 0, 0],
            [scale, 0, 0],
            [scale, scale, 0],
            [0, 0, 0],
            [scale, scale, scale]
        ])
        fig.add_trace(go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode='lines',
            line=dict(color='#10b981', width=5),
            name='High-Symmetry Path (Γ-X-M-Γ-R)'
        ))
        title_str = "<b>Simple Cubic 1st Brillouin Zone (Cube)</b>"
        
    fig.update_layout(
        title=dict(text=title_str, font=dict(size=18, color='#1e293b')),
        scene=dict(
            xaxis_title='kx (Å⁻¹)',
            yaxis_title='ky (Å⁻¹)',
            zaxis_title='kz (Å⁻¹)',
            aspectmode='cube',
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.6))
        ),
        width=750,
        height=650,
        showlegend=True,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig


# ============================================================================
# 3. 3D EWALD SPHERE CONSTRUCTOR
# ============================================================================

def create_3d_ewald_sphere(wavelength=1.54, lattice_constant=3.5, n_nodes=3):
    """
    Construct 3D Ewald Sphere of radius k = 2*pi/lambda intersecting reciprocal lattice.
    Laue condition: k_out - k_in = G.
    """
    k_radius = 2.0 * np.pi / wavelength  # Radius of Ewald sphere (Å⁻¹)
    b_step = 2.0 * np.pi / lattice_constant  # Reciprocal lattice vector length
    
    fig = go.Figure()
    
    # Generate 3D Reciprocal Lattice Nodes
    recip_points = []
    for h in range(-n_nodes, n_nodes + 1):
        for k in range(-n_nodes, n_nodes + 1):
            for l in range(-n_nodes, n_nodes + 1):
                recip_points.append([h * b_step, k * b_step, l * b_step])
    recip_points = np.array(recip_points)
    
    # Reciprocal nodes trace
    fig.add_trace(go.Scatter3d(
        x=recip_points[:, 0], y=recip_points[:, 1], z=recip_points[:, 2],
        mode='markers',
        marker=dict(size=5, color='#64748b', opacity=0.7),
        name='Reciprocal Nodes (G_hkl)'
    ))
    
    # Ewald Sphere Center at (-k_radius, 0, 0), Sphere passes through origin (0,0,0)
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    xs = -k_radius + k_radius * np.outer(np.cos(u), np.sin(v))
    ys = k_radius * np.outer(np.sin(u), np.sin(v))
    zs = k_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        opacity=0.25,
        colorscale=[[0, 'rgba(59,130,246,0.3)'], [1, 'rgba(147,197,253,0.3)']],
        showscale=False,
        name='Ewald Sphere (k = 2π/λ)'
    ))
    
    # Incident beam k_in from center to origin
    fig.add_trace(go.Scatter3d(
        x=[-k_radius, 0], y=[0, 0], z=[0, 0],
        mode='lines+markers',
        line=dict(color='#ef4444', width=6),
        marker=dict(size=[6, 10], color=['#ef4444', '#ef4444']),
        name='Incident Wavevector (k_in)'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>3D Ewald Sphere Diffraction Geometry</b> (λ = {wavelength:.2f} Å, a = {lattice_constant:.2f} Å)",
            font=dict(size=16, color='#1e293b')
        ),
        scene=dict(
            xaxis_title='kx (Å⁻¹)',
            yaxis_title='ky (Å⁻¹)',
            zaxis_title='kz (Å⁻¹)',
            aspectmode='cube'
        ),
        width=750,
        height=600,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig


# ============================================================================
# 4. 3D CRYSTAL DISLOCATION & DEFECT GENERATOR
# ============================================================================

def create_crystal_defects_visualization(structure_type="Simple Cubic", a=1.0, defect_type="Edge Dislocation"):
    """
    Create 3D visualization of point and line crystal defects:
    - Vacancy (Schottky)
    - Interstitial (Frenkel)
    - Substitutional impurity
    - Edge Dislocation (extra half plane of atoms, Burgers vector b)
    - Screw Dislocation (helical ramp of atoms)
    """
    n_cells = 4
    points = generate_simple_cubic(a, n_cells)
    colors = ['#3b82f6'] * len(points)
    sizes = [14] * len(points)
    
    center = np.mean(points, axis=0)
    
    if defect_type == "Vacancy":
        # Remove atom closest to center
        dist_sq = np.sum((points - center)**2, axis=1)
        remove_idx = np.argmin(dist_sq)
        points = np.delete(points, remove_idx, axis=0)
        colors = np.delete(colors, remove_idx)
        sizes = np.delete(sizes, remove_idx)
        title_info = "Schottky Vacancy (Missing atomic site)"
        
    elif defect_type == "Interstitial":
        # Add interstitial atom in octahedral/tetrahedral void
        interstitial_pt = center + np.array([0.5 * a, 0.5 * a, 0.5 * a])
        points = np.vstack([points, interstitial_pt])
        colors.append('#ef4444')
        sizes.append(18)
        title_info = "Frenkel Interstitial (Self-interstitial in lattice void)"
        
    elif defect_type == "Substitutional":
        # Replace center atom with dopant
        dist_sq = np.sum((points - center)**2, axis=1)
        sub_idx = np.argmin(dist_sq)
        colors[sub_idx] = '#10b981'
        sizes[sub_idx] = 22
        title_info = "Substitutional Impurity / Dopant Atom"
        
    elif defect_type == "Edge Dislocation":
        # Deform lattice according to Volterra edge dislocation displacement:
        # u_x = (b/2pi) * [theta + sin(2theta)/(4*(1-nu))]
        # u_y = -(b/2pi) * [(1-2nu)/(2(1-nu)) * ln(r) + cos(2theta)/(4*(1-nu))]
        b = a  # Burgers vector magnitude
        nu = 0.3  # Poisson's ratio
        deformed_pts = []
        
        for pt in points:
            dx = pt[0] - center[0]
            dy = pt[1] - center[1]
            r = np.sqrt(dx**2 + dy**2) + 1e-4
            theta = np.arctan2(dy, dx)
            
            # Volterra displacement
            ux = (b / (2.0 * np.pi)) * (theta + np.sin(2.0 * theta) / (4.0 * (1.0 - nu)))
            uy = -(b / (2.0 * np.pi)) * (((1.0 - 2.0 * nu) / (2.0 * (1.0 - nu))) * np.log(r) + np.cos(2.0 * theta) / (4.0 * (1.0 - nu)))
            
            # Damp far away
            decay = np.exp(-r / (2.5 * a))
            deformed_pts.append([pt[0] + ux * decay, pt[1] + uy * decay, pt[2]])
            
        points = np.array(deformed_pts)
        title_info = "Edge Dislocation (Extra half-plane, Burgers vector b ⊥ dislocation line)"
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='white'),
            opacity=0.9
        ),
        name='Lattice Atoms'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>{defect_type}</b><br><span style='font-size:13px; color:#64748b;'>{title_info}</span>",
            font=dict(size=16, color='#1e293b')
        ),
        scene=dict(
            xaxis_title='X (Å)',
            yaxis_title='Y (Å)',
            zaxis_title='Z (Å)',
            aspectmode='cube'
        ),
        width=700,
        height=600,
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    return fig


# ============================================================================
# 5. LEGACY PLOT COMPATIBILITY
# ============================================================================

def create_3d_crystal_plot(points, title="Crystal Structure", show_plane=False, h=1, k=1, l=1):
    """Create an interactive 3D plot of crystal structure."""
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode='markers',
        marker=dict(size=8, color=points[:, 2], colorscale='Viridis', opacity=0.8),
        name='Atoms'
    ))
    fig.update_layout(
        title=title,
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        width=700,
        height=600
    )
    return fig


def create_unit_cell_visualization(structure_type, a=1.0):
    """Create a unit cell wireframe visualization."""
    if structure_type == "Simple Cubic":
        pts = generate_simple_cubic(a, 1)
    elif structure_type == "BCC":
        pts = generate_bcc(a, 1)
    else:
        pts = generate_fcc(a, 1)
        
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
        mode='markers',
        marker=dict(size=12, color='#3b82f6'),
        name='Unit Cell Atoms'
    ))
    fig.update_layout(title=f"{structure_type} Unit Cell", width=500, height=500)
    return fig


def create_thermal_vibration_plot(points, amplitude=0.1, frames=20, title="Thermal Vibrations"):
    """Animation of thermal vibration in crystal."""
    vibration_frames = []
    for i in range(frames):
        random_displacements = np.random.normal(0, amplitude, size=points.shape)
        vibrated = points + random_displacements
        vibration_frames.append(go.Frame(data=[
            go.Scatter3d(
                x=vibrated[:, 0], y=vibrated[:, 1], z=vibrated[:, 2],
                mode='markers',
                marker=dict(size=8, color=vibrated[:, 2], colorscale='Viridis')
            )
        ]))
        
    fig = go.Figure(
        data=[go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2],
            mode='markers',
            marker=dict(size=8, color=points[:, 2], colorscale='Viridis')
        )],
        frames=vibration_frames
    )
    fig.update_layout(title=title, width=700, height=600)
    return fig


def create_phonon_visualization(structure_type, amplitude=0.1, mode="longitudinal", frames=20):
    """Animation of phonon displacement in crystal."""
    pts = generate_simple_cubic(1.0, 3)
    frames_list = []
    for i in range(frames):
        phase = 2.0 * np.pi * i / frames
        displaced = pts.copy()
        if mode == "longitudinal":
            displaced[:, 0] += amplitude * np.sin(pts[:, 0] + phase)
        else:
            displaced[:, 2] += amplitude * np.sin(pts[:, 0] + phase)
        frames_list.append(go.Frame(data=[
            go.Scatter3d(
                x=displaced[:, 0], y=displaced[:, 1], z=displaced[:, 2],
                mode='markers',
                marker=dict(size=10, color=displaced[:, 2], colorscale='Viridis')
            )
        ]))
        
    fig = go.Figure(
        data=[go.Scatter3d(
            x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
            mode='markers',
            marker=dict(size=10, color=pts[:, 2], colorscale='Viridis')
        )],
        frames=frames_list
    )
    fig.update_layout(title=f"{mode.capitalize()} Phonon Mode in {structure_type}", width=700, height=600)
    return fig
