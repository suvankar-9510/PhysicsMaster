"""
Vercel Serverless Entrypoint for PhysicsMaster
Provides an HTTP interface and redirection/preview for Vercel deployment.
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhysicsMaster - Graduate Physics Simulation Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body {
            background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .container {
            max-width: 900px;
            width: 100%;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 28px;
            padding: 3.5rem 2.5rem;
            text-align: center;
            box-shadow: 0 25px 60px -12px rgba(79, 70, 229, 0.35);
        }
        .badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid #6366f1;
            color: #818cf8;
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1.5rem;
        }
        h1 {
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p {
            color: #94a3b8;
            font-size: 1.15rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.2rem;
            margin: 2.5rem 0;
            text-align: left;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.2rem;
        }
        .card h3 { font-size: 1.05rem; margin-bottom: 0.4rem; color: #e2e8f0; }
        .card p { font-size: 0.85rem; color: #94a3b8; margin: 0; }
        .btn-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.9rem 2rem;
            border-radius: 14px;
            font-weight: 700;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.18);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">⚛️ PhysicsMaster v2.5 M.Sc</div>
        <h1>Advanced Graduate Physics Suite</h1>
        <p>
            Interactive 3D WebGL simulations for Solid State Physics (NMR/EPR/FMR, Dielectrics, Brillouin Zones), 
            Quantum Mechanics, Wave Dynamics, Optics, and Superconductivity.
        </p>

        <div class="grid">
            <div class="card">
                <h3>🔷 Solid State Suite</h3>
                <p>3D Brillouin Zones, Phonon Dispersions, NMR/EPR Bloch Dynamics & Ferroelectrics.</p>
            </div>
            <div class="card">
                <h3>🌌 Quantum Mechanics</h3>
                <p>Bloch Sphere 2-Level States, Harmonic Oscillator & Finite Barrier Tunneling.</p>
            </div>
            <div class="card">
                <h3>❄️ Superconductivity</h3>
                <p>London Penetration, Ginzburg-Landau Vortex Lattice & Josephson SQUID.</p>
            </div>
            <div class="card">
                <h3>🌊 Wave Physics</h3>
                <p>2D Chladni Plates, Multi-Wave Superposition & Dispersive Wavepackets.</p>
            </div>
        </div>

        <div class="btn-group">
            <a href="https://share.streamlit.io/" target="_blank" class="btn btn-primary">
                🚀 Launch on Streamlit Cloud (Instant Live)
            </a>
            <a href="https://github.com/suvankar-9510/PhysicsMaster" target="_blank" class="btn btn-secondary">
                📂 View GitHub Repository
            </a>
        </div>
    </div>
</body>
</html>"""
        self.wfile.write(html_content.encode('utf-8'))
