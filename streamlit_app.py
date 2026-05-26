import streamlit as st
from streamlit.components.v1 import html
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Fellou AI Browser",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800;900&display=swap');

*{
    font-family: 'Inter', sans-serif;
}

html{
    scroll-behavior:smooth;
}

.stApp{

background:

radial-gradient(circle at top left,
rgba(139,92,246,0.25),
transparent 25%),

radial-gradient(circle at top right,
rgba(59,130,246,0.22),
transparent 30%),

radial-gradient(circle at bottom,
rgba(6,182,212,0.18),
transparent 30%),

linear-gradient(
135deg,
#020617 0%,
#000000 35%,
#050816 65%,
#0f172a 100%
);

background-attachment:fixed;

color:white;
}
[data-testid="stAppViewContainer"]{
background:transparent;
}

.main{
background:transparent;
}
radial-gradient(circle at top left,#312e81,#0f172a 35%,#020617 70%);
overflow-x:hidden;
color:white;
}

/* REMOVE STREAMLIT STYLING */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.main{
    background:transparent;
}

/* ANIMATED BACKGROUND */

.glow{
position:fixed;
width:700px;
height:700px;
background:radial-gradient(circle,
rgba(59,130,246,.18),
transparent 70%);

filter:blur(120px);
z-index:-1;
animation: float 10s ease infinite;
top:-150px;
left:-150px;
}

.glow2{
position:fixed;
width:600px;
height:600px;
background:radial-gradient(circle,
rgba(168,85,247,.15),
transparent 70%);

filter:blur(120px);
z-index:-1;
bottom:-150px;
right:-150px;
animation: float2 12s ease infinite;
}

@keyframes float{
0%{transform:translate(0,0);}
50%{transform:translate(120px,70px);}
100%{transform:translate(0,0);}
}

@keyframes float2{
0%{transform:translate(0,0);}
50%{transform:translate(-100px,-80px);}
100%{transform:translate(0,0);}
}

/* NAVBAR */

.navbar{
position:sticky;
top:0;
z-index:999;

backdrop-filter:blur(18px);
background:rgba(255,255,255,0.04);

border:1px solid rgba(255,255,255,.08);

padding:18px 40px;
border-radius:20px;

margin-bottom:40px;
}

.nav-flex{
display:flex;
justify-content:space-between;
align-items:center;
}

.logo{
font-size:32px;
font-weight:900;

background:linear-gradient(90deg,#60a5fa,#a855f7);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.nav-links{
display:flex;
gap:30px;
}

.nav-links a{
text-decoration:none;
color:#d1d5db;
transition:.3s;
font-weight:500;
}

.nav-links a:hover{
color:#60a5fa;
}

/* HERO */

.hero{
padding-top:100px;
padding-bottom:130px;
text-align:center;
position:relative;
}

.hero h1{
font-size:90px;
font-weight:900;
line-height:1.05;

background:linear-gradient(
90deg,
#60a5fa,
#818cf8,
#a855f7,
#38bdf8
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

margin-bottom:30px;
}

.hero p{
font-size:24px;
color:#b3b8d0;

max-width:950px;
margin:auto;

line-height:1.9;
}

.hero-buttons{
margin-top:50px;

display:flex;
justify-content:center;
gap:25px;
flex-wrap:wrap;
}

.primary-btn{
background:linear-gradient(
135deg,
#2563eb,
#7c3aed
);

padding:18px 40px;

border-radius:16px;

font-weight:700;
color:white;

text-decoration:none;

transition:.4s;
}

.primary-btn:hover{
transform:translateY(-8px);
box-shadow:0 0 40px rgba(99,102,241,.6);
}

.secondary-btn{
border:1px solid rgba(255,255,255,.1);

padding:18px 40px;

border-radius:16px;

text-decoration:none;
color:white;

transition:.4s;
}

.secondary-btn:hover{
background:rgba(255,255,255,.05);
transform:translateY(-6px);
}

/* AI ORB */

.orb{

position:relative;

width:340px;
height:340px;

margin:80px auto;

border-radius:50%;

background:
conic-gradient(
from 0deg,
#60a5fa,
#a855f7,
#06b6d4,
#60a5fa
);

animation:
spin 10s linear infinite,
floatOrb 6s ease-in-out infinite;

box-shadow:
0 0 60px rgba(96,165,250,.5),
0 0 120px rgba(168,85,247,.35),
0 0 180px rgba(6,182,212,.25);

overflow:hidden;
}

/* INNER GLOW */

.orb::before{

content:"";

position:absolute;

inset:20px;

border-radius:50%;

background:
radial-gradient(circle at top,
rgba(255,255,255,.35),
rgba(255,255,255,.05),
transparent 70%);

filter:blur(12px);

animation:
pulse 4s ease infinite;
}

/* OUTER RING */

.orb::after{

content:"";

position:absolute;

inset:-18px;

border-radius:50%;

border:
2px solid rgba(255,255,255,.12);

animation:
rotateRing 12s linear infinite;

filter:blur(2px);
}

/* FLOATING */

@keyframes floatOrb{

0%{
transform:
translateY(0px)
rotate(0deg);
}

50%{
transform:
translateY(-20px)
rotate(180deg);
}

100%{
transform:
translateY(0px)
rotate(360deg);
}

}

/* MAIN ROTATION */

@keyframes spin{

0%{
filter:hue-rotate(0deg);
}

100%{
filter:hue-rotate(360deg);
}

}

/* GLOW PULSE */

@keyframes pulse{

0%{
opacity:.6;
transform:scale(1);
}

50%{
opacity:1;
transform:scale(1.05);
}

100%{
opacity:.6;
transform:scale(1);
}

}

/* OUTER RING ROTATION */

@keyframes rotateRing{

0%{
transform:rotate(0deg);
}

100%{
transform:rotate(-360deg);
}

}
st.markdown("""
<style>

.particles{
    position:relative;
    width:0;
    height:0;
    margin:auto;
}

/* PARTICLES */

.particle{
    position:absolute;
    width:10px;
    height:10px;
    border-radius:50%;
    background:#60a5fa;

    box-shadow:
    0 0 20px #60a5fa;

    animation:
    particleFloat 6s linear infinite;
}

/* DIFFERENT POSITIONS */

.particle:nth-child(1){
    top:-180px;
    left:-120px;
    animation-delay:0s;
}

.particle:nth-child(2){
    top:-120px;
    left:140px;
    animation-delay:1s;
}

.particle:nth-child(3){
    top:80px;
    left:-160px;
    animation-delay:2s;
}

.particle:nth-child(4){
    top:140px;
    left:120px;
    animation-delay:3s;
}

.particle:nth-child(5){
    top:0px;
    left:200px;
    animation-delay:4s;
}

/* FLOATING ANIMATION */

@keyframes particleFloat{

    0%{
        transform:
        translateY(0px)
        scale(1);

        opacity:0;
    }

    50%{
        opacity:1;
    }

    100%{
        transform:
        translateY(-40px)
        scale(1.5);

        opacity:0;
    }
}

</style>
""", unsafe_allow_html=True)
st.markdown("""

<div class="particles">

<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>

</div>

""", unsafe_allow_html=True)

.particle:nth-child(2){
top:-120px;
left:140px;
animation-delay:1s;
}

.particle:nth-child(3){
top:80px;
left:-160px;
animation-delay:2s;
}

.particle:nth-child(4){
top:140px;
left:120px;
animation-delay:3s;
}

.particle:nth-child(5){
top:0px;
left:200px;
animation-delay:4s;
}

/* FLOATING PARTICLES */

@keyframes particleFloat{

0%{
transform:
translateY(0px)
scale(1);

opacity:0;
}

50%{
opacity:1;
}

100%{
transform:
translateY(-40px)
scale(1.5);

opacity:0;
}

}

</style>
""", unsafe_allow_html=True)
/* DIFFERENT POSITIONS */

.particle:nth-child(1){
top:-180px;
left:-120px;
animation-delay:0s;
}

.particle:nth-child(2){
top:-120px;
left:140px;
animation-delay:1s;
}

.particle:nth-child(3){
top:80px;
left:-160px;
animation-delay:2s;
}

.particle:nth-child(4){
top:140px;
left:120px;
animation-delay:3s;
}

.particle:nth-child(5){
top:0px;
left:200px;
animation-delay:4s;
}

/* FLOATING PARTICLES */

@keyframes particleFloat{

0%{
transform:
translateY(0px)
scale(1);

opacity:0;
}

50%{
opacity:1;
}

100%{
transform:
translateY(-40px)
scale(1.5);

opacity:0;
}

}
background:
radial-gradient(circle at top,
#60a5fa,
#7c3aed,
#111827);

box-shadow:
0 0 120px rgba(99,102,241,.5);

animation: spin 14s linear infinite;
}

@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}

/* SECTION */

.section-title{
font-size:58px;
font-weight:900;
text-align:center;

margin-top:90px;
margin-bottom:50px;

color:white;
}

/* FEATURES */

.feature-grid{
display:grid;

grid-template-columns:
repeat(auto-fit,minmax(320px,1fr));

gap:28px;
}

.feature-card{

background:rgba(255,255,255,.05);

border:1px solid rgba(255,255,255,.08);

backdrop-filter:blur(15px);

padding:35px;

border-radius:28px;

transition:.45s;

transform-style:preserve-3d;
}

.feature-card:hover{

transform:
rotateX(8deg)
rotateY(-8deg)
translateY(-14px);

box-shadow:
0 0 50px rgba(99,102,241,.45);
}

.feature-card h3{
font-size:28px;
margin-bottom:18px;
color:#60a5fa;
}

.feature-card p{
color:#d1d5db;
line-height:1.9;
}

/* TERMINAL */

.terminal{
background:#020617;

border:1px solid rgba(255,255,255,.08);

padding:35px;

border-radius:24px;

margin-top:60px;

font-family:monospace;

color:#4ade80;

line-height:2;
}

/* STATS */

.stats{
display:grid;

grid-template-columns:
repeat(auto-fit,minmax(200px,1fr));

gap:25px;

margin-top:70px;
}

.stat-box{
background:rgba(255,255,255,.05);

padding:35px;

border-radius:22px;

text-align:center;

border:1px solid rgba(255,255,255,.08);
}

.stat-box h2{
font-size:52px;
color:#60a5fa;
}

.stat-box p{
color:#d1d5db;
}

/* TESTIMONIALS */

.testimonial{
background:rgba(255,255,255,.04);

border:1px solid rgba(255,255,255,.08);

padding:35px;

border-radius:24px;

margin-bottom:25px;
}

.testimonial p{
line-height:1.9;
color:#d1d5db;
}

.testimonial h4{
margin-top:18px;
color:#60a5fa;
}

/* FOOTER */

.footer{
margin-top:120px;

padding:60px;

text-align:center;

color:#9ca3af;
}

/* RESPONSIVE */

@media(max-width:768px){

.hero h1{
font-size:52px;
}

.hero p{
font-size:18px;
}

.section-title{
font-size:42px;
}

.nav-links{
display:none;
}

}

</style>
""", unsafe_allow_html=True)

# ---------------- GLOW EFFECTS ----------------

st.markdown("""
<div class="glow"></div>
<div class="glow2"></div>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------

st.markdown("""
<div class="navbar">

<div class="nav-flex">

<div class="logo">🚀 Fellou AI</div>

<div class="nav-links">
<a href="#">Features</a>
<a href="#">AI Demo</a>
<a href="#">Research</a>
<a href="#">Pricing</a>
<a href="#">Docs</a>
<a href="#">Github</a>
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------

st.markdown("""
<div class="hero">

<h1>
The Future of Autonomous Browsing
</h1>

<p>
An AI-native browser that researches, automates,
reasons across tabs, controls workflows,
and executes tasks like a digital operating system.
</p>

<div class="hero-buttons">

<a class="primary-btn" href="#">
Launch AI Browser
</a>

<a class="secondary-btn" href="#">
Watch Live Demo
</a>

</div>

<div class="orb"></div>

</div>
""", unsafe_allow_html=True)

# ---------------- AI DEMO ----------------

st.markdown("""
<h2 class="section-title">
🧠 AI Workflow Simulation
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terminal">

> Initializing autonomous agents...<br>
> Opening 14 research sources...<br>
> Comparing multiple products...<br>
> Analyzing market trends...<br>
> Generating structured report...<br>
> Executing browser workflows...<br>
> Task completed successfully.
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES ----------------

st.markdown("""
<h2 class="section-title">
⚡ Next-Gen AI Features
</h2>
""", unsafe_allow_html=True)

features = [

("Autonomous Web Agents",
"AI agents independently execute workflows across websites and apps."),

("Multi-Tab Intelligence",
"AI understands context across multiple tabs simultaneously."),

("Deep Research Engine",
"Conduct in-depth research from dozens of online sources automatically."),

("AI Workspace Memory",
"Adaptive memory system learns your workflow preferences over time."),

("Real-Time Workflow Monitoring",
"Watch every AI action step-by-step and intervene anytime."),

("Voice Command Navigation",
"Control browser workflows naturally using voice commands."),

("Cross-App Automation",
"Automate actions across apps, websites, and desktop systems."),

("AI Copilot Overlay",
"Instant contextual AI assistant across every webpage."),

("Privacy & Security Layer",
"Human approval system with encrypted memory architecture."),

("Dynamic Task Scheduling",
"Run autonomous tasks in the future automatically."),

("Contextual AI Actions",
"AI predicts your next actions intelligently."),

("AI File System",
"Manage desktop files directly through natural language.")
]

for i in range(0, len(features), 3):

    cols = st.columns(3)

    for j in range(3):

        if i + j < len(features):

            with cols[j]:

                st.markdown(f"""
                <div class="feature-card">

                <h3>{features[i+j][0]}</h3>

                <p>{features[i+j][1]}</p>

                </div>
                """, unsafe_allow_html=True)

# ---------------- STATS ----------------

st.markdown("""
<h2 class="section-title">
📊 Trusted Worldwide
</h2>
""", unsafe_allow_html=True)

stats = [
("10M+","Tasks Automated"),
("150+","AI Integrations"),
("99.9%","Uptime"),
("4.9★","User Rating")
]

cols = st.columns(4)

for i, stat in enumerate(stats):

    with cols[i]:

        st.markdown(f"""
        <div class="stat-box">

        <h2>{stat[0]}</h2>

        <p>{stat[1]}</p>

        </div>
        """, unsafe_allow_html=True)

# ---------------- TESTIMONIALS ----------------

st.markdown("""
<h2 class="section-title">
💬 Stories That Inspire
</h2>
""", unsafe_allow_html=True)

testimonials = [

("“This feels like Jarvis for the internet.”","— MARLON"),

("“The most futuristic browser experience I've ever seen.”","— Guri Saroy"),

("“Deep research and automation are insanely powerful.”","— Felipe")
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
<h2 class="section-title">
❓ Frequently Asked Questions
</h2>
""", unsafe_allow_html=True)

faq = {

"Can AI automate apps and websites?":
"Yes. Fellou AI autonomously executes workflows across websites and desktop apps.",

"Can I monitor AI actions in real-time?":
"Yes. Every AI step is visible and controllable.",

"Does it support deep research?":
"Yes. The AI analyzes information from multiple sources simultaneously.",

"Does it work with local files?":
"Absolutely. AI can manage and operate local desktop files.",

"Can tasks run automatically later?":
"Yes. You can schedule workflows and autonomous tasks."
}

for q, a in faq.items():

    with st.expander(q):
        st.write(a)

# ---------------- MISSION ----------------

st.markdown("""
<h2 class="section-title">
🚀 Our Mission
</h2>

<div class="feature-card" style="text-align:center;">

<h3>
Empowering Humanity with Intelligent Productivity
</h3>

<p>
Building the world's most advanced autonomous AI browsing platform.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">

<h2 style="color:white;">
🚀 Fellou AI Browser
</h2>

<p>
AI-native autonomous browsing platform
</p>

<br>

<p>
Features • Research • Docs • API • Contact • Github
</p>

<br>

<p>
© 2026 Fellou AI. All rights reserved.
</p>

</div>
""", unsafe_allow_html=True)
