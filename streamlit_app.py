import streamlit as st

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Fellou AI Browser",
    page_icon="🌐",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    body { background-color: #0d0d0d; }
    .main { background-color: #0d0d0d; }

    h1 { color: #ffffff; font-size: 2.5rem; }
    h2 { color: #c084fc; }
    h3 { color: #e2e8f0; }

    .hero-box {
        background: linear-gradient(135deg, #1e1b4b, #0f172a);
        border: 1px solid #4f46e5;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-box h1 { font-size: 2.8rem; color: #ffffff; }
    .hero-box p  { color: #94a3b8; font-size: 1.1rem; }

    .feature-card {
        background: #1e293b;
        border-left: 4px solid #7c3aed;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .feature-card h4 { color: #a78bfa; margin: 0 0 0.4rem; }
    .feature-card p  { color: #cbd5e1; margin: 0; font-size: 0.95rem; }

    .testimonial-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
    }
    .testimonial-card .quote { color: #e2e8f0; font-style: italic; }
    .testimonial-card .author { color: #7c3aed; font-weight: bold; margin-top: 0.5rem; }

    .use-case-badge {
        display: inline-block;
        background: #312e81;
        color: #c4b5fd;
        border-radius: 20px;
        padding: 0.3rem 1rem;
        margin: 0.3rem;
        font-size: 0.9rem;
    }

    .diff-card {
        background: #0f172a;
        border: 1px solid #4f46e5;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .diff-card strong { color: #a78bfa; }
    .diff-card span   { color: #94a3b8; }

    .mission-box {
        background: linear-gradient(135deg, #312e81, #1e1b4b);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: #e2e8f0;
        font-size: 1.2rem;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────
fellou_info = {
    "name": "Fellou",
    "tagline": "The World's First Agentic Browser",
    "description": (
        "Fellou is an AI-powered browser that goes beyond browsing by taking "
        "automated web actions. It executes complex cross-app workflows through "
        "natural language descriptions."
    ),
    "contact": "hi@fellou.ai",
    "website": "https://fellou.ai",
    "key_features": [
        {"title": "Automated Complex Web Tasks with One Prompt",
         "detail": "Automatically execute cross-app workflows through natural language descriptions."},
        {"title": "End-To-End Web Automation",
         "detail": "From complex data scraping to form filling, handles every step from a single command."},
        {"title": "Handles Desktop Files, Zero Effort",
         "detail": "Computer Use transforms Fellou into a true system-level agent to operate local apps and manage files."},
        {"title": "Intervene at Any Step in Real Time",
         "detail": "Fellou shows its entire plan step by step. Edit, approve, or step in at any moment."},
        {"title": "Agentic Memory Learns You",
         "detail": "Securely learns from your browser history and notes to instantly recall past information."},
        {"title": "Multi-Source Research Reports",
         "detail": "Automates deep research across the entire internet including logged-in accounts like Reddit."},
    ],
    "use_cases": ["Data Analytics", "Career Growth", "Study", "Marketing", "Daily Life", "Productivity"],
    "differences": {
        "Deep Action": "Independently plans and executes complex web and desktop tasks across multiple apps.",
        "Deep Search": "Automates in-depth research across the internet including logged-in accounts on X, Reddit, or Salesforce.",
        "Dynamic Multitasking": "Runs multiple tasks simultaneously in its back-end workspace while you browse.",
        "Agentic Memory": "Offers proactive, personalized help by connecting browser history and chat context.",
    },
    "testimonials": [
        {"quote": "Fellou didn't just beat the competition, it crushed them. Most accurate, clearest reports, deepest insights. 3.1x faster than OpenAI.",
         "user": "Guri Saroy", "handle": "@HeyGurisaroy"},
        {"quote": "Chrome was for browsing. Fellou is for doing it. The future is not the search, it is an exploration of action.",
         "user": "Filipe | IA", "handle": "@filicroval"},
        {"quote": "This is the future of web browsing.",
         "user": "MARLON", "handle": "@MarlonNFTs"},
    ],
    "faq": [
        "Can AI browsers do more than just summarize pages and organize tabs?",
        "Can AI automate my work across different apps and websites?",
        "Does it work on sites that require a login or CAPTCHA?",
        "Can I see and control exactly what the AI agent is doing?",
        "What can AI Browser create other than answering questions by text?",
        "Can I schedule tasks to run automatically in the future?",
        "Can I build my own custom AI agents and workflows?",
    ],
    "mission": "Bring a digital companion to every person, on every device. Empowering humanity with intelligent productivity.",
}

# ── HERO ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-box">
    <h1>🌐 {fellou_info['name']}</h1>
    <h3 style="color:#a78bfa;">{fellou_info['tagline']}</h3>
    <p>{fellou_info['description']}</p>
    <p style="margin-top:1rem;">
        🔗 <a href="{fellou_info['website']}" target="_blank" style="color:#7c3aed;">{fellou_info['website']}</a>
        &nbsp;|&nbsp; 📧 {fellou_info['contact']}
    </p>
</div>
""", unsafe_allow_html=True)

# ── KEY FEATURES ──────────────────────────────────────────────
st.markdown("## ⚡ Key Features")
col1, col2 = st.columns(2)
for i, feature in enumerate(fellou_info["key_features"]):
    target = col1 if i % 2 == 0 else col2
    with target:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{feature['title']}</h4>
            <p>{feature['detail']}</p>
        </div>
        """, unsafe_allow_html=True)

# ── USE CASES ─────────────────────────────────────────────────
st.markdown("## 🎯 Use Cases")
badges = "".join(
    f'<span class="use-case-badge">{uc}</span>'
    for uc in fellou_info["use_cases"]
)
st.markdown(f"<div style='margin-bottom:1.5rem;'>{badges}</div>", unsafe_allow_html=True)

# ── VS CHAT ASSISTANT ─────────────────────────────────────────
st.markdown("## 🤖 Fellou vs Chat Assistant")
st.info("An AI chat assistant is **reactive** — it only answers questions. Fellou's agentic AI **acts** — it runs tasks automatically and proactively helps you complete things you've forgotten.")

for key, val in fellou_info["differences"].items():
    st.markdown(f"""
    <div class="diff-card">
        <strong>{key}:</strong> <span>{val}</span>
    </div>
    """, unsafe_allow_html=True)

# ── TESTIMONIALS ──────────────────────────────────────────────
st.markdown("## 💬 Stories That Inspire")
for t in fellou_info["testimonials"]:
    st.markdown(f"""
    <div class="testimonial-card">
        <div class="quote">"{t['quote']}"</div>
        <div class="author">— {t['user']} <span style="color:#64748b;">{t['handle']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ── FAQ ───────────────────────────────────────────────────────
st.markdown("## ❓ Frequently Asked Questions")
for q in fellou_info["faq"]:
    with st.expander(q):
        st.write("Visit [fellou.ai](https://fellou.ai) for the full answer.")

# ── MISSION ───────────────────────────────────────────────────
st.markdown(f"""
<div class="mission-box">
    🚀 <strong>Our Mission</strong><br><br>
    {fellou_info['mission']}
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#475569;'>Fellou AI Browser · hi@fellou.ai · "
    "<a href='https://fellou.ai' style='color:#7c3aed;'>fellou.ai</a></p>",
    unsafe_allow_html=True
)
