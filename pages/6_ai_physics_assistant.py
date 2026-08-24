
import streamlit as st
from datetime import datetime
from openai import OpenAI
import plotly.graph_objects as go
import re
import numpy as np
import time
from utils.theme import render_theme_sidebar

# Set page configuration
st.set_page_config(page_title="AI Physics Assistant",
                   page_icon="🧠",
                   layout="wide",
                   initial_sidebar_state="expanded")

theme = render_theme_sidebar()
dark = theme["dark"]

# Enhanced modern CSS with minimal design
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
        color: #1e293b;
    }

    /* AI-themed header with subtle animations */
    .ai-header {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #8b5cf6 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 3px solid #6366f1;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
    }

    .ai-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 2px, transparent 2px),
            radial-gradient(circle at 80% 40%, rgba(255,255,255,0.08) 1px, transparent 1px),
            radial-gradient(circle at 40% 80%, rgba(255,255,255,0.06) 1.5px, transparent 1.5px);
        background-size: 60px 60px, 100px 100px, 80px 80px;
        animation: aiPattern 15s linear infinite;
    }

    @keyframes aiPattern {
        0% { transform: translate(0, 0); opacity: 0.3; }
        50% { transform: translate(-20px, -20px); opacity: 0.6; }
        100% { transform: translate(0, 0); opacity: 0.3; }
    }

    /* Clean section cards */
    .ai-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .ai-section:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }

    /* Input and button styling */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #f8fafc;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background: white;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }

    /* Answer display */
    .answer-card {
        background: linear-gradient(135deg, #f8fafc 0%, white 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        font-size: 1rem;
        line-height: 1.7;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        position: relative;
        overflow: hidden;
    }

    .answer-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #4338ca, #6366f1, #8b5cf6);
    }

    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
        transition: all 0.3s ease;
        margin: 0 0.2rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }

    /* Example cards */
    .example-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }

    .example-card:hover {
        background: white;
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.1);
    }

    /* Loading animation */
    .thinking-animation {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: #f1f5f9;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .thinking-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6366f1;
        animation: thinking 1.4s ease-in-out infinite both;
    }

    .thinking-dot:nth-child(2) { animation-delay: -0.32s; }
    .thinking-dot:nth-child(3) { animation-delay: -0.16s; }

    @keyframes thinking {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border-color: #6366f1;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4338ca;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Feature highlight */
    .feature-highlight {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# Inject MathJax for LaTeX rendering
st.markdown("""
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js">
</script>
<script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true,
            macros: { degree: "^\\circ", vec: ["\\boldsymbol{#1}", 1] }
        },
        options: {
            skipHtmlTags: ['script', 'style'],
            processHtmlClass: 'tex2jax_process'
        },
        startup: {
            ready: () => {
                MathJax.startup.defaultReady();
                document.querySelectorAll('.tex2jax_process').forEach(el => {
                    MathJax.typeset([el]);
                });
            }
        }
    };
    new MutationObserver(() => {
        if (typeof MathJax !== 'undefined') MathJax.typeset();
    }).observe(document.body, {childList: true, subtree: true});
</script>
""", unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="ai-header">
    <h1 style="color: white; margin: 0; font-size: 3rem; position: relative; z-index: 2; font-weight: 800;">
        <span style="margin-right: 1rem;">🧠</span> AI Physics Assistant
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 1rem 0 0 0; font-size: 1.3rem; position: relative; z-index: 2; font-weight: 500;">
        Powered by Advanced Language Models
    </p>
    <div style="margin-top: 1.5rem; position: relative; z-index: 2;">
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Step-by-Step Solutions</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Visual Explanations</span>
        <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0 0.5rem; font-size: 0.9rem; backdrop-filter: blur(10px);">Real-time Help</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize AI client
def initialize_ai_client():
    import os
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        except Exception:
            pass
    if not api_key:
        api_key = st.session_state.get("user_api_key", "")
    
    if not api_key:
        return None
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize AI client: {str(e)}")
        return None

# Improved LaTeX processing
def process_latex_for_rendering(text):
    try:
        text = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\\frac{\1}{\2}', text)
        text = re.sub(r'\$(.*?)\$', r'$\1$', text, flags=re.DOTALL)
        text = re.sub(r'\$\$([\s\S]*?)\$\$', r'<div style="text-align: center; margin: 1rem 0; padding: 1rem; background: #f8fafc; border-radius: 8px;">$$\1$$</div>', text)
        return text
    except Exception as e:
        return text

# Enhanced visualization generator with comprehensive physics illustrations
def generate_visualization(question, response):
    question_lower = question.lower()
    try:
        if "wave" in question_lower or "interference" in question_lower:
            x = np.linspace(0, 10, 300)
            t = time.time() % 4
            wave1 = np.sin(2*np.pi*x - 3*t)
            wave2 = np.sin(2*np.pi*1.5*x - 2*t)
            interference = wave1 + wave2
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=wave1, mode='lines', name='Wave 1', 
                                   line=dict(color='#3b82f6', width=2)))
            fig.add_trace(go.Scatter(x=x, y=wave2, mode='lines', name='Wave 2', 
                                   line=dict(color='#ef4444', width=2)))
            fig.add_trace(go.Scatter(x=x, y=interference, mode='lines', name='Interference', 
                                   line=dict(color='#10b981', width=3)))
            
            fig.update_layout(
                title="Wave Interference Pattern",
                xaxis_title="Position",
                yaxis_title="Amplitude",
                template="plotly_white",
                height=400
            )
            return fig

        elif "projectile" in question_lower or "trajectory" in question_lower:
            t = np.linspace(0, 2, 100)
            v0, angle = 20, 45
            g = 9.8
            x = v0 * np.cos(np.radians(angle)) * t
            y = v0 * np.sin(np.radians(angle)) * t - 0.5 * g * t**2
            y = np.maximum(y, 0)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', 
                                   line=dict(color='#8b5cf6', width=3),
                                   marker=dict(size=4)))
            
            fig.update_layout(
                title="Projectile Motion",
                xaxis_title="Horizontal Distance (m)",
                yaxis_title="Height (m)",
                template="plotly_white",
                height=400
            )
            return fig
            
        elif "quantum" in question_lower or "energy" in question_lower:
            # Energy level diagram
            x = np.linspace(-5, 5, 1000)
            potential = 0.5 * x**2  # Harmonic oscillator potential
            energy_levels = [0.5, 1.5, 2.5, 3.5, 4.5]
            
            fig = go.Figure()
            
            # Potential well
            fig.add_trace(go.Scatter(x=x, y=potential, mode='lines', 
                                   name='Potential V(x)', 
                                   line=dict(color='#1f2937', width=3)))
            
            # Energy levels
            for i, E in enumerate(energy_levels):
                fig.add_trace(go.Scatter(x=[-3, 3], y=[E, E], mode='lines',
                                       name=f'n={i}', 
                                       line=dict(color=f'rgb({50 + i*40}, {100 + i*30}, {200 - i*20})', 
                                               width=2, dash='dash')))
            
            fig.update_layout(
                title="Quantum Harmonic Oscillator Energy Levels",
                xaxis_title="Position x",
                yaxis_title="Energy",
                template="plotly_white",
                height=400
            )
            return fig
            
        elif "electromagnetic" in question_lower or "electric" in question_lower or "magnetic" in question_lower:
            # Electric field visualization
            x = np.linspace(-2, 2, 20)
            y = np.linspace(-2, 2, 20)
            X, Y = np.meshgrid(x, y)
            
            # Point charge at origin
            r = np.sqrt(X**2 + Y**2)
            r[r == 0] = 1e-10  # Avoid division by zero
            Ex = X / r**3
            Ey = Y / r**3
            
            fig = go.Figure()
            
            # Electric field vectors
            fig.add_trace(go.Scatter(x=X.flatten(), y=Y.flatten(),
                                   mode='markers',
                                   marker=dict(symbol='arrow-right', size=8, color='blue'),
                                   showlegend=False))
            
            # Central charge
            fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers',
                                   marker=dict(size=20, color='red', symbol='circle'),
                                   name='Positive Charge'))
            
            fig.update_layout(
                title="Electric Field around Point Charge",
                xaxis_title="x",
                yaxis_title="y",
                template="plotly_white",
                height=400
            )
            return fig
            
        elif "crystal" in question_lower or "lattice" in question_lower:
            # 3D crystal structure
            a = 4  # Lattice parameter
            positions = []
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        positions.append([i*a, j*a, k*a])
            
            positions = np.array(positions)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter3d(
                x=positions[:, 0],
                y=positions[:, 1],
                z=positions[:, 2],
                mode='markers',
                marker=dict(size=8, color='blue', opacity=0.8),
                name='Atoms'
            ))
            
            fig.update_layout(
                title="Crystal Lattice Structure",
                scene=dict(
                    xaxis_title="x (Å)",
                    yaxis_title="y (Å)",
                    zaxis_title="z (Å)"
                ),
                height=500
            )
            return fig

        return None
    except Exception:
        return None

# Create physics concepts chart
def create_physics_concepts_chart():
    st.markdown("#### 🔬 Physics Concepts Overview")
    
    # Create a comprehensive physics concepts visualization
    concepts = {
        'Classical Mechanics': 85,
        'Quantum Physics': 78,
        'Thermodynamics': 82,
        'Electromagnetism': 90,
        'Optics': 88,
        'Nuclear Physics': 75,
        'Relativity': 70,
        'Solid State': 80
    }
    
    fig = go.Figure()
    
    # Create radar chart
    categories = list(concepts.keys())
    values = list(concepts.values())
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='AI Knowledge',
        line=dict(color='#6366f1', width=2),
        fillcolor='rgba(99, 102, 241, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="AI Physics Knowledge Coverage",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Create interactive physics demonstration
def create_interactive_demo():
    st.markdown("#### ⚛️ Interactive Physics Demo")
    
    demo_type = st.selectbox("Choose a physics demonstration:", 
                           ["Wave Interference", "Quantum States", "Electric Field", "Crystal Structure"])
    
    if demo_type == "Wave Interference":
        freq1 = st.slider("Wave 1 Frequency", 0.5, 3.0, 1.0, 0.1)
        freq2 = st.slider("Wave 2 Frequency", 0.5, 3.0, 1.5, 0.1)
        
        x = np.linspace(0, 10, 300)
        wave1 = np.sin(2*np.pi*freq1*x)
        wave2 = np.sin(2*np.pi*freq2*x)
        interference = wave1 + wave2
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=wave1, name=f'Wave 1 (f={freq1}Hz)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x, y=wave2, name=f'Wave 2 (f={freq2}Hz)', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=x, y=interference, name='Interference', line=dict(color='green', width=3)))
        
        fig.update_layout(title="Real-time Wave Interference", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    elif demo_type == "Quantum States":
        n = st.slider("Quantum Number n", 1, 5, 1)
        x = np.linspace(-5, 5, 1000)
        
        # Harmonic oscillator wavefunctions (simplified)
        if n == 1:
            psi = np.exp(-0.5*x**2)
        elif n == 2:
            psi = x * np.exp(-0.5*x**2)
        elif n == 3:
            psi = (2*x**2 - 1) * np.exp(-0.5*x**2)
        else:
            psi = np.exp(-0.5*x**2) * np.cos(n*x)
        
        probability = psi**2
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=psi, name='Wavefunction ψ', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=x, y=probability, name='Probability |ψ|²', 
                               fill='tonexty', line=dict(color='red')))
        
        fig.update_layout(title=f"Quantum State n={n}", height=400)
        st.plotly_chart(fig, use_container_width=True)

# Generate AI response
def generate_answer(client, question):
    if not question.strip():
        return "Please enter a physics question to get started!"
    
    if client is None:
        return "**AI Service Unavailable:** Please check your connection and try again."
    
    system_prompt = """
    You are an expert physics tutor for undergraduate and graduate students. Provide clear, comprehensive explanations using:
    - Step-by-step mathematical derivations
    - Physical intuition and concepts
    - LaTeX formatting for equations: $...$ for inline, $$...$$ for block equations
    - Real-world applications and examples
    Keep explanations accessible but rigorous.
    """
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content
        return process_latex_for_rendering(response)
    
    except Exception as e:
        return f"**Error:** Unable to generate response. Please try again. ({str(e)})"

# Save to history
def save_to_history(question, response):
    if "history" not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "response": response
    })
    
    # Keep last 8 entries
    if len(st.session_state.history) > 8:
        st.session_state.history = st.session_state.history[:8]

# Main application
def main():
    # Clear any potential cached content that might be causing display issues
    if 'cached_html' in st.session_state:
        del st.session_state['cached_html']
    
    client = initialize_ai_client()
    
    # Main interface
    col1, col2 = st.columns([2.5, 1.5], gap="large")
    
    with col1:
        st.markdown("""
        <div class="ai-section">
            <h2 style="color: #1e293b; margin-bottom: 1.5rem; font-size: 1.8rem; font-weight: 600;">
                💭 Ask Your Physics Question
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Question input
        question_text = st.text_area(
            "Enter your question here:",
            height=120,
            placeholder="e.g., Explain quantum tunneling or derive the wave equation..."
        )
        
        # Submit button with loading state
        if st.button("🚀 Get AI Answer", type="primary"):
            if question_text:
                # Show thinking animation
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("""
                <div class="thinking-animation">
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                    <div class="thinking-dot"></div>
                    <span style="margin-left: 0.5rem; color: #64748b;">AI is thinking...</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate response
                response = generate_answer(client, question_text)
                visualization = generate_visualization(question_text, response)
                save_to_history(question_text, response)
                
                # Clear thinking animation
                thinking_placeholder.empty()
                
                # Display response
                st.markdown("### 🎯 AI Response")
                st.markdown(f'<div class="answer-card tex2jax_process">{response}</div>', 
                           unsafe_allow_html=True)
                
                # Show visualization if available
                if visualization:
                    st.plotly_chart(visualization, use_container_width=True)
                
                # Copy functionality
                with st.expander("📋 Copy Answer"):
                    st.text_area("", value=response, height=150)

    with col2:
        # Feature highlights using clean Streamlit components
        st.markdown("#### ⚡ AI Capabilities")
        
        # Use clean Streamlit elements instead of complex HTML
        capabilities = [
            "🧮 Complex problem solving",
            "📊 Step-by-step derivations", 
            "🎨 Visual explanations",
            "⚡ Instant responses"
        ]
        
        for capability in capabilities:
            st.markdown(f"- {capability}")
        
        st.markdown("---")
        
        # Physics concepts illustration
        create_physics_concepts_chart()
        
        # Tabs for history and examples
        tab1, tab2 = st.tabs(["📚 Recent Questions", "💡 Examples"])
        
        with tab1:
            if "history" in st.session_state and st.session_state.history:
                for i, entry in enumerate(st.session_state.history):
                    with st.expander(f"Q: {entry['question'][:40]}..." if len(entry['question']) > 40 else f"Q: {entry['question']}"):
                        st.markdown(f"**Asked:** {entry['timestamp']}")
                        st.markdown("**Question:**")
                        st.write(entry['question'])
                        st.markdown("**Answer:**")
                        st.markdown(f'<div class="answer-card tex2jax_process">{entry["response"]}</div>', 
                                   unsafe_allow_html=True)
            else:
                st.info("💡 Your question history will appear here")

        with tab2:
            st.markdown("**Click to try these examples:**")
            examples = [
                "What is the uncertainty principle?",
                "Derive the Schrödinger equation",
                "Explain electromagnetic induction",
                "How do lasers work?",
                "What causes superconductivity?",
                "Explain black hole thermodynamics",
                "Derive Einstein's mass-energy relation",
                "What is quantum entanglement?"
            ]
            
            for example in examples:
                if st.button(example, key=f"ex_{example[:20]}", help="Click to use this example"):
                    st.session_state.example_question = example
                    st.rerun()

    # Interactive demonstrations section
    st.markdown("---")
    create_interactive_demo()
    
    # Statistics dashboard
    if "history" in st.session_state:
        st.markdown("### 📊 Usage Statistics")
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.history)}</div>
                <div class="metric-label">Questions Asked</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            avg_length = np.mean([len(entry['response']) for entry in st.session_state.history]) if st.session_state.history else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{int(avg_length)}</div>
                <div class="metric-label">Avg Response Length</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">⚡</div>
                <div class="metric-label">AI Status</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🎯</div>
                <div class="metric-label">Ready to Help</div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
