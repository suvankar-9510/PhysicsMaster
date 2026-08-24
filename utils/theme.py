import streamlit as st

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
            "card_bg": "rgba(17, 24, 39, 0.85)",
            "card_border": "rgba(255, 255, 255, 0.12)",
            "text_primary": "#f8fafc",
            "text_secondary": "#94a3b8",
            "theory_bg": "rgba(99, 102, 241, 0.14)",
            "theory_border": "#818cf8",
            "metric_bg": "rgba(30, 41, 59, 0.8)",
            "plot_bg": "rgba(15, 23, 42, 0.75)",
            "paper_bg": "rgba(0, 0, 0, 0)",
            "grid_color": "rgba(255, 255, 255, 0.1)",
            "accent": "#38bdf8",
            "accent_grad": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #6366f1 100%)"
        }
    else:
        theme = {
            "dark": False,
            "app_bg": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%)",
            "sidebar_bg": "#f8fafc",
            "card_bg": "rgba(255, 255, 255, 0.95)",
            "card_border": "rgba(203, 213, 225, 0.85)",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "theory_bg": "rgba(238, 242, 255, 0.98)",
            "theory_border": "#4f46e5",
            "metric_bg": "rgba(255, 255, 255, 0.95)",
            "plot_bg": "rgba(255, 255, 255, 0.98)",
            "paper_bg": "rgba(0, 0, 0, 0)",
            "grid_color": "rgba(0, 0, 0, 0.08)",
            "accent": "#1d4ed8",
            "accent_grad": "linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #6366f1 100%)"
        }
        
    inject_theme_css(theme)
    return theme


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
        
        /* Typography overrides */
        p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown {{
            color: {theme['text_primary']} !important;
        }}
        
        /* Custom Components */
        .crystal-header {{
            background: {theme['accent_grad']};
            padding: 2.5rem 2rem;
            border-radius: 24px;
            text-align: center;
            margin-bottom: 1.8rem;
            color: white !important;
            box-shadow: 0 15px 35px rgba(30, 58, 138, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }}
        .crystal-header * {{
            color: white !important;
        }}
        
        .metric-card {{
            background: {theme['metric_bg']} !important;
            backdrop-filter: blur(14px);
            border-radius: 16px;
            padding: 1.1rem;
            text-align: center;
            border: 1px solid {theme['card_border']} !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, {'0.15' if dark else '0.06'});
            transition: transform 0.25s ease;
            margin-bottom: 0.8rem;
        }}
        .metric-card:hover {{
            transform: translateY(-3px);
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
            margin-top: 4px;
        }}
        
        .theory-box {{
            background: {theme['theory_bg']} !important;
            border-left: 4px solid {theme['theory_border']} !important;
            padding: 1.1rem 1.4rem;
            border-radius: 12px;
            margin: 1rem 0;
            color: {theme['text_primary']} !important;
            font-size: 0.95rem;
            line-height: 1.6;
            border-top: 1px solid {theme['card_border']} !important;
            border-right: 1px solid {theme['card_border']} !important;
            border-bottom: 1px solid {theme['card_border']} !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, {'0.15' if dark else '0.04'});
        }}
        .theory-box h4 {{
            color: {'#a5b4fc' if dark else '#4338ca'} !important;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }}

        /* Streamlit Tabs */
        [data-baseweb="tab-list"] {{
            background: {theme['card_bg']} !important;
            padding: 6px;
            border-radius: 14px;
            border: 1px solid {theme['card_border']} !important;
        }}
        [data-baseweb="tab"] {{
            color: {theme['text_secondary']} !important;
            font-weight: 600 !important;
            border-radius: 10px;
        }}
        [aria-selected="true"] {{
            background: {'rgba(99, 102, 241, 0.25)' if dark else 'rgba(79, 70, 229, 0.12)'} !important;
            color: {'#38bdf8' if dark else '#1d4ed8'} !important;
        }}

        /* Expander and Table styles */
        .streamlit-expanderHeader {{
            background: {theme['card_bg']} !important;
            color: {theme['text_primary']} !important;
            border-radius: 10px;
        }}

        /* Mobile Responsive */
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
