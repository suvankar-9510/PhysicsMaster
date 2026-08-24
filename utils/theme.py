import streamlit as st
import plotly.graph_objects as go

def init_theme():
    """Initialize theme session state if not already set."""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True


def render_theme_sidebar():
    """Renders the persistent theme switcher in the sidebar and returns the active theme dict."""
    init_theme()
    
    with st.sidebar:
        st.markdown("### 🎨 Laboratory Theme")
        mode = st.radio(
            "Select Theme:",
            ["🌙 Dark Mode", "☀️ Light Mode"],
            index=0 if st.session_state.dark_mode else 1,
            key="global_theme_mode_selector",
            horizontal=True
        )
        st.session_state.dark_mode = (mode == "🌙 Dark Mode")
        st.markdown("---")
        
    return get_theme()


def get_theme():
    """Return dictionary of theme variables and inject full CSS overrides."""
    init_theme()
    dark = st.session_state.dark_mode
    
    if dark:
        theme = {
            "dark": True,
            "app_bg": "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%)",
            "sidebar_bg": "#111827",
            "card_bg": "rgba(17, 24, 39, 0.88)",
            "card_border": "rgba(255, 255, 255, 0.12)",
            "text_primary": "#f8fafc",
            "text_secondary": "#94a3b8",
            "theory_bg": "rgba(99, 102, 241, 0.14)",
            "theory_border": "#818cf8",
            "metric_bg": "rgba(30, 41, 59, 0.85)",
            "plot_bg": "rgba(15, 23, 42, 0.85)",
            "paper_bg": "rgba(0, 0, 0, 0)",
            "grid_color": "rgba(255, 255, 255, 0.12)",
            "accent": "#38bdf8",
            "accent_grad": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #6366f1 100%)"
        }
    else:
        theme = {
            "dark": False,
            "app_bg": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%)",
            "sidebar_bg": "#ffffff",
            "card_bg": "rgba(255, 255, 255, 0.98)",
            "card_border": "rgba(203, 213, 225, 0.9)",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "theory_bg": "rgba(238, 242, 255, 0.98)",
            "theory_border": "#4f46e5",
            "metric_bg": "rgba(255, 255, 255, 0.98)",
            "plot_bg": "rgba(255, 255, 255, 0.98)",
            "paper_bg": "rgba(0, 0, 0, 0)",
            "grid_color": "rgba(0, 0, 0, 0.08)",
            "accent": "#1d4ed8",
            "accent_grad": "linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #6366f1 100%)"
        }
        
    inject_theme_css(theme)
    return theme


def apply_figure_theme(fig, theme=None):
    """Apply unified font colors, plot background, gridlines, and 3D scene parameters to any Plotly figure."""
    if theme is None:
        theme = get_theme()
        
    text_c = theme["text_primary"]
    grid_c = theme["grid_color"]
    plot_b = theme["plot_bg"]
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=plot_b,
        font=dict(family='Plus Jakarta Sans, sans-serif', color=text_c),
        title=dict(font=dict(color=text_c, family='Plus Jakarta Sans, sans-serif')),
        legend=dict(
            font=dict(color=text_c),
            bgcolor='rgba(15,23,42,0.6)' if theme['dark'] else 'rgba(255,255,255,0.85)',
            bordercolor=theme['card_border'],
            borderwidth=1
        )
    )
    
    # 2D Axes
    fig.update_xaxes(color=text_c, gridcolor=grid_c, zerolinecolor=grid_c, tickfont=dict(color=text_c))
    fig.update_yaxes(color=text_c, gridcolor=grid_c, zerolinecolor=grid_c, tickfont=dict(color=text_c))
    
    # 3D Scene Axes
    fig.update_scenes(
        xaxis=dict(color=text_c, gridcolor=grid_c, backgroundcolor='rgba(0,0,0,0)', tickfont=dict(color=text_c), title=dict(font=dict(color=text_c))),
        yaxis=dict(color=text_c, gridcolor=grid_c, backgroundcolor='rgba(0,0,0,0)', tickfont=dict(color=text_c), title=dict(font=dict(color=text_c))),
        zaxis=dict(color=text_c, gridcolor=grid_c, backgroundcolor='rgba(0,0,0,0)', tickfont=dict(color=text_c), title=dict(font=dict(color=text_c)))
    )
    
    return fig


def inject_theme_css(theme):
    dark = theme["dark"]
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
        
        /* Global Root and App View Container */
        html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {{
            background: {theme['app_bg']} !important;
            color: {theme['text_primary']} !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {{
            background-color: {theme['sidebar_bg']} !important;
            color: {theme['text_primary']} !important;
            border-right: 1px solid {theme['card_border']} !important;
        }}
        
        /* KaTeX & Math Formulas */
        .katex, .katex-display, .katex * {{
            color: {theme['text_primary']} !important;
        }}
        
        /* Crystal Header Banner */
        .crystal-header {{
            background: {theme['accent_grad']} !important;
            padding: 2.4rem 2rem !important;
            border-radius: 24px !important;
            text-align: center !important;
            margin-bottom: 1.8rem !important;
            box-shadow: 0 15px 35px rgba(30, 58, 138, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
        }}
        .crystal-header h1, .crystal-header p, .crystal-header div, .crystal-header span {{
            color: #ffffff !important;
        }}
        
        /* Metric Dashboard Cards */
        .metric-card {{
            background: {theme['metric_bg']} !important;
            backdrop-filter: blur(14px) !important;
            border-radius: 16px !important;
            padding: 1.2rem 1rem !important;
            text-align: center !important;
            border: 1px solid {theme['card_border']} !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, {'0.18' if dark else '0.05'}) !important;
            transition: transform 0.25s ease !important;
            margin-bottom: 0.8rem !important;
        }}
        .metric-card:hover {{
            transform: translateY(-3px) !important;
            border-color: #6366f1 !important;
        }}
        
        .metric-value {{
            font-size: 1.6rem !important;
            font-weight: 800 !important;
            color: {theme['accent']} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        
        .metric-label {{
            font-size: 0.82rem !important;
            color: {theme['text_secondary']} !important;
            font-weight: 600 !important;
            margin-top: 4px !important;
        }}
        
        /* Theoretical Derivation Callout Box */
        .theory-box {{
            background: {theme['theory_bg']} !important;
            border-left: 4px solid {theme['theory_border']} !important;
            padding: 1.1rem 1.4rem !important;
            border-radius: 12px !important;
            margin: 1rem 0 !important;
            color: {theme['text_primary']} !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            border-top: 1px solid {theme['card_border']} !important;
            border-right: 1px solid {theme['card_border']} !important;
            border-bottom: 1px solid {theme['card_border']} !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, {'0.15' if dark else '0.04'}) !important;
        }}
        .theory-box h4 {{
            color: {'#a5b4fc' if dark else '#4338ca'} !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            margin-bottom: 0.4rem !important;
        }}

        /* Streamlit Tabs Navigation */
        [data-baseweb="tab-list"] {{
            background: {theme['card_bg']} !important;
            padding: 6px !important;
            border-radius: 14px !important;
            border: 1px solid {theme['card_border']} !important;
        }}
        [data-baseweb="tab"] {{
            color: {theme['text_secondary']} !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
        }}
        [aria-selected="true"] {{
            background: {'rgba(99, 102, 241, 0.25)' if dark else 'rgba(79, 70, 229, 0.12)'} !important;
            color: {'#38bdf8' if dark else '#1d4ed8'} !important;
        }}

        /* Dataframe / Expander */
        .streamlit-expanderHeader {{
            background: {theme['card_bg']} !important;
            color: {theme['text_primary']} !important;
            border-radius: 10px !important;
        }}

        /* Mobile Viewport Breakpoints */
        @media (max-width: 768px) {{
            .crystal-header {{
                padding: 1.6rem 1rem !important;
                border-radius: 18px !important;
            }}
            .crystal-header h1 {{
                font-size: 1.7rem !important;
            }}
            .crystal-header p {{
                font-size: 0.92rem !important;
            }}
            .metric-card {{
                padding: 0.8rem 0.5rem !important;
            }}
            .metric-value {{
                font-size: 1.25rem !important;
            }}
            .theory-box {{
                padding: 0.9rem 1rem !important;
                font-size: 0.88rem !important;
            }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
