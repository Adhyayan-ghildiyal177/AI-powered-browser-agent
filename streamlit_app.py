import streamlit as st
from streamlit.components.v1 import html

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fellou AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800&display=swap');

*{
    font-family: 'Inter', sans-serif;
}

html{
    scroll-behavior:smooth;
}

body{
    background: linear-gradient(135deg,#050816,#0b1026,#111827);
    color:white;
}

.main{
    background: transparent;
}

/* NAVBAR */

.navbar{
    position: sticky;
    top: 0;
    z-index:999;
    backdrop-filter: blur(10px);
    background: rgba(10,10,20,0.6);
    border:1px solid rgba(255,255,255,0.08);
    padding:18px 30px;
    border-radius:20px;
    margin-bottom:40px;
}

.nav-flex{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:28px;
    font-weight:800;
    color:#60a5fa;
}

.nav-links{
    display:flex;
    gap:30px;
}

.nav-links a{
    color:white;
    text-decoration:none;
    transition:0.3s;
}

.nav-links a:hover{
    color:#60a5fa;
}

/* HERO SECTION */

.hero{
    padding-top:80px;
    padding-bottom:100px;
    text-align:center;
}

.hero h1{
    font-size:72px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:25px;

    background: linear-gradient(90deg,#60a5fa,#818cf8,#c084fc);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    font-size:22px;
    color:#b3b8d0;
    max-width:900px;
    margin:auto;
    line-height:1.8;
}

.hero-buttons{
    margin-top:40px;
    display:flex;
    justify-content:center;
    gap:20px;
    flex-wrap:wrap;
}

.primary-btn{
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    padding:15px 35px;
    border-radius:14px;
    color:white;
    font-weight:700;
    text-decoration:none;
    transition:0.3s;
}

.primary-btn:hover{
    transform:translateY(-5px);
    box-shadow:0 0 35px rgba(99,102,241,.6);
}

.secondary-btn{
    border:1px solid rgba(255,255,255,.15);
    padding:15px 35px;
    border-radius:14px;
    color:white;
    text-decoration:none;
    transition:0.3s;
}

.secondary-btn:hover{
    background:rgba(255,255,255,.05);
}

/* FEATURE SECTION */

.section-title{
    font-size:48px;
    font-weight:800;
    margin-top:70px;
    margin-bottom:40px;
    text-align:center;
}

.feature-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
    gap:25px;
}

.feature-card{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);

    padding:30px;
    border-radius:24px;

    transition:0.4s;
}

.feature-card:hover{
    transform:translateY(-10px);
    box-shadow:0 0 35px rgba(59,130,246,.35);
}

.feature-card h3{
    color:#60a5fa;
    font-size:26px;
    margin-bottom:15px;
}

.feature-card p{
    color:#c7c9d3;
    line-height:1.8;
}

/* STATS */

.stats{
    margin-top:90px;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
    gap:20px;
}

.stat-box{
    background:rgba(255,255,255,0.04);
    border-radius:20px;
    padding:35px;
    text-align:center;
}

.stat-box h2{
    font-size:50px;
    color:#60a5fa;
}

.stat-box p{
    color:#d1d5db;
}

/* TESTIMONIALS */

.testimonial{
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    padding:30px;
    border-radius:22px;
    margin-bottom:25px;
}

.testimonial p{
    color:#d1d5db;
    line-height:1.8;
}

.testimonial h4{
    margin-top:15px;
    color:#60a5fa;
}

/* FAQ */

.faq{
    background:rgba(255,255,255,.04);
    border-radius:18px;
    padding:18px;
    margin-bottom:15px;
    border:1px solid rgba(255,255,255,.08);
}

/* FOOTER */

.footer{
    margin-top:100px;
    padding:50px;
    text-align:center;
    color:#9ca3af;
}

/* GLOW */

.glow{
    position:fixed;
    width:500px;
    height:500px;
    background:radial-gradient(circle,#2563eb55,transparent 70%);
    top:-100px;
    left:-100px;
    z-index:-1;
    filter:blur(80px);
}

/* RESPONSIVE */

@media(max-width:768px){

.hero h1{
    font-size:48px;
}

.hero p{
    font-size:18px;
}

.section-title{
    font-size:38px;
}

}

</style>
""", unsafe_allow_html=True)

# ---------------- GLOW EFFECT ----------------
st.markdown('<div class="glow"></div>', unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
    <div class="nav-flex">
        <div class="logo">🚀 Fellou AI</div>

        <div class="nav-links">
            <a href="#">Features</a>
            <a href="#">Pricing</a>
            <a href="#">Docs</a>
            <a href="#">Github</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">

<h1>The Future of Autonomous Browsing</h1>

<p>
Automate workflows, research smarter, control apps,
and execute web tasks with powerful AI agents.
</p>

<div class="hero-buttons">
    <a class="primary-btn" href="#">Get Started</a>
    <a class="secondary-btn" href="#">Watch Demo</a>
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES ----------------
st.markdown("""
<h2 class="section-title">⚡ Key Features</h2>
""", unsafe_allow_html=True)

features = [
    ("Automated Workflows",
     "Execute complex web tasks with one prompt."),

    ("AI Research",
     "Perform multi-source deep research across the web."),

    ("Desktop Control",
     "Manage local apps and files with AI automation."),

    ("Real-Time Monitoring",
     "Watch and control every AI action step-by-step."),

    ("Memory System",
     "AI learns your workflow preferences over time."),

    ("Dynamic Multitasking",
     "Run multiple autonomous tasks simultaneously.")
]

cols = st.columns(3)

for i, feature in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{feature[0]}</h3>
            <p>{feature[1]}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- STATS ----------------
st.markdown("""
<h2 class="section-title">📊 Trusted Worldwide</h2>
""", unsafe_allow_html=True)

stats_cols = st.columns(4)

stats = [
    ("10M+", "Tasks Automated"),
    ("99.9%", "Uptime"),
    ("150+", "Integrations"),
    ("4.9★", "User Rating")
]

for i, stat in enumerate(stats):
    with stats_cols[i]:
        st.markdown(f"""
        <div class="stat-box">
            <h2>{stat[0]}</h2>
            <p>{stat[1]}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- TESTIMONIALS ----------------
st.markdown("""
<h2 class="section-title">💬 Stories That Inspire</h2>
""", unsafe_allow_html=True)

testimonials = [
    ("“This is the future of browsing.”",
     "— MARLON"),

    ("“Most accurate AI workflow system I’ve used.”",
     "— Guri Saroy"),

    ("“Feels like Jarvis for the internet.”",
     "— Felipe")
]

for t in testimonials:
    st.markdown(f"""
    <div class="testimonial">
        <p>{t[0]}</p>
        <h4>{t[1]}</h4>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FAQ ----------------
st.markdown("""
<h2 class="section-title">❓ Frequently Asked Questions</h2>
""", unsafe_allow_html=True)

faq_data = {
    "Can AI automate apps and websites?":
    "Yes. Fellou AI can automate workflows across apps and browsers.",

    "Can I control the AI actions?":
    "Yes. You can monitor and intervene anytime.",

    "Does it support desktop automation?":
    "Yes. It can operate local apps and files.",

    "Can I schedule tasks?":
    "Absolutely. AI workflows can run automatically."
}

for q, a in faq_data.items():
    with st.expander(q):
        st.write(a)

# ---------------- MISSION ----------------
st.markdown("""
<h2 class="section-title">🚀 Our Mission</h2>

<div class="feature-card" style="text-align:center;">
<h3>Empowering Humanity with Intelligent Productivity</h3>

<p>
Bring a digital companion to every device and every person.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">

<h3>Fellou AI Browser</h3>

<p>
Built with ❤️ using Streamlit
</p>

<p>
Docs • API • Contact • Github
</p>

</div>
""", unsafe_allow_html=True)
