import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Fellou AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800;900&display=swap');

*{
    font-family:'Inter',sans-serif;
}

html{
    scroll-behavior:smooth;
}

/* BACKGROUND FIX */

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

/* REMOVE STREAMLIT UI */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* 3D GRID */

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

@keyframes spin{

0%{
filter:hue-rotate(0deg);
}

100%{
filter:hue-rotate(360deg);
}

}

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

@keyframes rotateRing{

0%{
transform:rotate(0deg);
}

100%{
transform:rotate(-360deg);
}

}

/* PARTICLES */

.particles{
position:relative;
width:0;
height:0;
margin:auto;
}

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

<div class="particles">

<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>
<div class="particle"></div>

</div>

</div>
""", unsafe_allow_html=True)

# ---------------- TERMINAL ----------------

st.markdown("""
<div class="terminal">

> Initializing AI agents...<br>
> Searching 14 websites...<br>
> Comparing market data...<br>
> Executing browser actions...<br>
> Task completed successfully.

</div>
""", unsafe_allow_html=True)
