import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Fellou AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800;900&display=swap');

*{
    font-family:'Inter',sans-serif;
}

html{
    scroll-behavior:smooth;
}

/* MAIN BACKGROUND */

body{

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

overflow-x:hidden;
color:white;
}

.main{
    background:transparent;
}

/* REMOVE STREAMLIT DEFAULTS */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* 3D GRID BACKGROUND */

.grid-bg{
position:fixed;
width:100%;
height:100%;

background-image:
linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);

background-size:50px 50px;

transform:
perspective(1000px)
rotateX(75deg)
scale(2);

transform-origin:top;

opacity:.18;

z-index:-3;

animation:gridmove 18s linear infinite;
}

@keyframes gridmove{

0%{
transform:
perspective(1000px)
rotateX(75deg)
translateY(0)
scale(2);
}

100%{
transform:
perspective(1000px)
rotateX(75deg)
translateY(50px)
scale(2);
}

}

/* GLOW EFFECTS */

.glow{
position:fixed;
width:800px;
height:800px;

background:
radial-gradient(circle,
rgba(168,85,247,.22),
transparent 70%);

filter:blur(140px);

z-index:-1;

top:-250px;
left:-200px;

animation: float 12s ease infinite;
}

.glow2{
position:fixed;
width:700px;
height:700px;

background:
radial-gradient(circle,
rgba(59,130,246,.18),
transparent 70%);

filter:blur(140px);

z-index:-1;

bottom:-250px;
right:-200px;

animation: float2 14s ease infinite;
}

@keyframes float{

0%{
transform:translate(0,0);
}

50%{
transform:translate(120px,80px);
}

100%{
transform:translate(0,0);
}

}

@keyframes float2{

0%{
transform:translate(0,0);
}

50%{
transform:translate(-100px,-60px);
}

100%{
transform:translate(0,0);
}

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

border-radius:22px;

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

background:
linear-gradient(
90deg,
#60a5fa,
#a855f7,
#06b6d4
);

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

padding-top:120px;
padding-bottom:120px;

text-align:center;
}

.hero h1{

font-size:90px;
font-weight:900;

line-height:1.05;

background:
linear-gradient(
90deg,
#60a5fa,
#a855f7,
#06b6d4
);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

margin-bottom:28px;
}

.hero p{

font-size:24px;

max-width:950px;

margin:auto;

line-height:1.9;

color:#b8c1d9;
}

/* BUTTONS */

.hero-buttons{

margin-top:50px;

display:flex;
justify-content:center;

gap:22px;

flex-wrap:wrap;
}

.primary-btn{

background:
linear-gradient(
135deg,
#2563eb,
#a855f7
);

padding:18px 42px;

border-radius:18px;

font-weight:700;

text-decoration:none;

color:white;

transition:.4s;
}

.primary-btn:hover{

transform:translateY(-8px);

box-shadow:
0 0 50px rgba(99,102,241,.6);
}

.secondary-btn{

border:1px solid rgba(255,255,255,.1);

padding:18px 42px;

border-radius:18px;

text-decoration:none;

color:white;

transition:.4s;
}

.secondary-btn:hover{

background:rgba(255,255,255,.05);

transform:translateY(-6px);
}

/* 3D AI ORB */

.orb{

width:340px;
height:340px;

margin:80px auto;

border-radius:50%;

background:
radial-gradient(circle at top,
#60a5fa,
#a855f7,
#020617);

box-shadow:
0 0 120px rgba(99,102,241,.5);

animation:
spin 14s linear infinite,
pulse 5s ease infinite;
}

@keyframes spin{

0%{
transform:rotate(0deg);
}

100%{
transform:rotate(360deg);
}

}

@keyframes pulse{

0%{
box-shadow:0 0 80px rgba(99,102,241,.4);
}

50%{
box-shadow:0 0 150px rgba(168,85,247,.7);
}

100%{
box-shadow:0 0 80px rgba(99,102,241,.4);
}

}

/* SECTION TITLES */

.section-title{

font-size:58px;
font-weight:900;

text-align:center;

margin-top:90px;
margin-bottom:55px;

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

backdrop-filter:blur(16px);

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

line-height:1.9;

color:#d1d5db;
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
font-size:54px;
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

# ---------------- BACKGROUND EFFECTS ----------------

st.markdown("""
<div class="grid-bg"></div>
<div class="glow"></div>
<div class="glow2"></div>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------

st.markdown("""
<div class="navbar">

<div class="nav-flex">

<div class="logo">
🚀 Fellou AI
</div>

<div class="nav-links">
<a href="#">Features</a>
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
An AI-native browser that researches, automates workflows,
controls apps, reasons across tabs,
and executes complex tasks autonomously.
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

# ---------------- TERMINAL ----------------

st.markdown("""
<h2 class="section-title">
🧠 AI Workflow Simulation
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terminal">

> Initializing AI agents...<br>
> Searching 14 websites...<br>
> Comparing market data...<br>
> Opening autonomous workflows...<br>
> Executing browser actions...<br>
> Generating structured report...<br>
> Task completed successfully.
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES ----------------

st.markdown("""
<h2 class="section-title">
⚡ Next-Generation Features
</h2>
""", unsafe_allow_html=True)

features = [

("Autonomous Web Agents",
"AI agents independently perform browser workflows."),

("Deep Research Engine",
"Conduct multi-source internet research automatically."),

("Multi-Tab Intelligence",
"AI reasons across multiple tabs simultaneously."),

("AI Workspace Memory",
"Adaptive memory system learns your habits over time."),

("Voice Command Navigation",
"Control workflows naturally using voice commands."),

("Real-Time AI Monitoring",
"Watch every AI action step-by-step live.")
]

for i in range(0, len(features), 3):

    cols = st.columns(3)

    for j in range(3):

        if i+j < len(features):

            with cols[j]:

                st.markdown(f"""
                <div class="feature-card">

                <h3>{features[i+j][0]}</h3>

                <p>{features[i+j][1]}</p>

                </div>
                """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">

<h2 style="color:white;">
🚀 Fellou AI Browser
</h2>

<p>
The next generation AI-native autonomous browser.
</p>

<br>

<p>
Features • Research • Docs • Github • API
</p>

<br>

<p>
© 2026 Fellou AI
</p>

</div>
""", unsafe_allow_html=True)
