
import os
import time
import json
import math
import random
import asyncio
import textwrap
from datetime import datetime

import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Ghildiyal AI Browser",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# OPTIONAL IMPORTS / SAFE FALLBACKS
# =========================================================

try:
    import requests
except Exception:
    requests = None

try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    async_playwright = None
    PLAYWRIGHT_AVAILABLE = False

try:
    import chromadb
    CHROMA_AVAILABLE = True
except Exception:
    chromadb = None
    CHROMA_AVAILABLE = False

# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Ready. Ask me to search, browse, summarize, or automate."}
    ]

if "workflow_log" not in st.session_state:
    st.session_state.workflow_log = []

if "memory_items" not in st.session_state:
    st.session_state.memory_items = []

if "task_status" not in st.session_state:
    st.session_state.task_status = "Idle"

if "demo_progress" not in st.session_state:
    st.session_state.demo_progress = 0

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Browse"

if "browser_url" not in st.session_state:
    st.session_state.browser_url = "https://example.com"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "command_text" not in st.session_state:
    st.session_state.command_text = "Research the latest AI browser trends"

if "voice_text" not in st.session_state:
    st.session_state.voice_text = "Open research mode and compare AI browsers"

if "file_notes" not in st.session_state:
    st.session_state.file_notes = ""

# =========================================================
# HELPERS
# =========================================================

def add_log(message: str, kind: str = "info") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.workflow_log.insert(0, f"[{ts}] {message}")
    st.session_state.workflow_log = st.session_state.workflow_log[:15]

def add_memory(note: str) -> None:
    note = note.strip()
    if note:
        st.session_state.memory_items.insert(0, {
            "note": note,
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.session_state.memory_items = st.session_state.memory_items[:12]

def simulate_stream(text: str, speed: float = 0.01):
    placeholder = st.empty()
    running = ""
    for ch in text:
        running += ch
        placeholder.markdown(running)
        time.sleep(speed)

def safe_llm_answer(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are a helpful AI browser assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI error: {e}"
    return (
        "Demo mode: connect OPENAI_API_KEY to enable real AI responses. "
        f"Prompt received: {prompt}"
    )

def web_search(query: str):
    """
    Search for query using Tavily or Serper APIs if keys are set,
    else perform DuckDuckGo HTML search (no API key required).
    Returns a list of dicts with keys: title, link, snippet, source.
    """
    import os
    try:
        import requests
    except ImportError:
        requests = None
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        BeautifulSoup = None

    import re
    import ast
    import operator as op
    from urllib.parse import quote_plus

    results = []

    # 1) Simple math check (safe evaluation)
    math_expr = query.strip()
    math_expr = math_expr.replace("×", "*").replace("÷", "/")
    if re.fullmatch(r"[0-9\.\+\-\*\/\%\(\)\s\^]+", math_expr):
        math_expr = math_expr.replace("^", "**")
        try:
            def _eval(node):
                if isinstance(node, ast.Expression):
                    return _eval(node.body)
                if isinstance(node, ast.Constant):
                    return node.value
                if isinstance(node, ast.Num):  # Python <3.8 compatibility
                    return node.n
                if isinstance(node, ast.BinOp):
                    if type(node.op) not in {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod}:
                        raise ValueError("Invalid operator")
                    left = _eval(node.left)
                    right = _eval(node.right)
                    return {
                        ast.Add: op.add, ast.Sub: op.sub,
                        ast.Mult: op.mul, ast.Div: op.truediv,
                        ast.Pow: op.pow, ast.Mod: op.mod
                    }[type(node.op)](left, right)
                if isinstance(node, ast.UnaryOp):
                    if type(node.op) not in {ast.UAdd, ast.USub}:
                        raise ValueError("Invalid unary")
                    operand = _eval(node.operand)
                    return {ast.UAdd: op.pos, ast.USub: op.neg}[type(node.op)](operand)
                raise ValueError("Unsafe expression")
            node = ast.parse(math_expr, mode='eval')
            result = _eval(node)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return [{
                "title": f"Answer: {result}",
                "link": "",
                "snippet": f"{query} = {result}",
                "source": "Calculator",
            }]
        except Exception:
            pass

    # 2) Web search via Tavily or Serper if API keys are set
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()

      # Tavily Search (if key provided)
    if requests is not None and tavily_key:

        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": tavily_key,
                    "query": query,
                    "max_results": 5
                },
                timeout=15
            )

            data = r.json()

            for item in data.get("results", []):

                link = item.get("url", "")

                if link.startswith("//"):
                    link = "https:" + link

                results.append({
                    "title": item.get("title", "No Title"),
                    "link": link,
                    "snippet": item.get("content", ""),
                    "source": "Tavily",
                })

        except Exception as e:

            results.append({
                "title": "Search Error",
                "link": "",
                "snippet": str(e),
                "source": "Tavily",
            })
    link = item.get("url", "")

    # FIX LINKS
    if link.startswith("//"):
        link = "https:" + link

    results.append({
        "title": item.get("title", "No Title"),
        "link": link,
        "snippet": item.get("content", ""),
        "source": "Tavily",
    })
            if results:
                return results
        except Exception as e:
            results.append({
                "title": "Search error",
                "link": "",
                "snippet": str(e),
                "source": "Tavily",
            })
            return results

    # Serper Search (if Tavily not used and key provided)
    if requests is not None and serper_key:
        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": query},
                timeout=15
            )
            data = r.json()
            for item in data.get("organic", [])[:5]:
                results.append({
                    "title": item.get("title", "No Title"),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "Serper",
                })
            if results:
                return results
        except Exception as e:
            results.append({
                "title": "Search error",
                "link": "",
                "snippet": str(e),
                "source": "Serper",
            })
            return results

    # 3) DuckDuckGo HTML search (no API key needed)
    if requests is not None and BeautifulSoup is not None:
        try:
            r = requests.get(
                f"https://html.duckduckgo.com/html/?q={quote_plus(query)}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.select(".result")
            for card in cards[:5]:
                title_tag = card.select_one("a.result__a")
                snippet_tag = card.select_one("a.result__snippet")
                title = title_tag.get_text(strip=True) if title_tag else "No Title"
                link = title_tag.get("href", "") if title_tag else ""
                snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""
                if title or snippet:
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                        "source": "DuckDuckGo",
                    })
            if results:
                return results
        except Exception as e:
            results.append({
                "title": "Search error",
                "link": "",
                "snippet": str(e),
                "source": "DuckDuckGo",
            })
            return results

    # Fallback if all else fails
    return [{
        "title": f"Search results for '{query}'",
        "link": "https://duckduckgo.com",
        "snippet": "No live search available (requests/bs4 missing or an error occurred).",
        "source": "Fallback",
    }]

async def fetch_url_info_async(url: str):
    if not PLAYWRIGHT_AVAILABLE:
        return {"title": "Playwright unavailable", "content": "", "error": "Install playwright"}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1440, "height": 1200})
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            title = await page.title()
            text = await page.locator("body").inner_text(timeout=10000)
            await browser.close()
            return {"title": title, "content": text[:5000], "error": ""}
    except Exception as e:
        return {"title": "", "content": "", "error": str(e)}

def fetch_url_info(url: str):
    if PLAYWRIGHT_AVAILABLE:
        try:
            return asyncio.run(fetch_url_info_async(url))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(fetch_url_info_async(url))
        except Exception as e:
            return {"title": "", "content": "", "error": str(e)}
    if requests:
        try:
            r = requests.get(url, timeout=15)
            title = ""
            content = r.text[:5000]
            if BeautifulSoup:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.get_text(strip=True) if soup.title else ""
                content = soup.get_text(" ", strip=True)[:5000]
            return {"title": title or "Fetched page", "content": content, "error": ""}
        except Exception as e:
            return {"title": "", "content": "", "error": str(e)}
    return {"title": "", "content": "", "error": "requests unavailable"}

def build_research_summary(query: str):
    results = web_search(query)
    summary_prompt = "Summarize and compare these search results:\n\n"
    for idx, item in enumerate(results, 1):
        summary_prompt += f"{idx}. {item['title']}\n{item['snippet']}\n{item['link']}\n\n"
    return safe_llm_answer(summary_prompt)

def browser_command(command: str):
    command = command.lower().strip()
    if any(word in command for word in ["search", "research", "find"]):
        return "Research mode activated. Web search results updated."
    if any(word in command for word in ["summarize", "summary"]):
        return "Summary mode activated. The assistant will compress results into insights."
    if any(word in command for word in ["open", "browse", "visit"]):
        return "Browse mode activated. Enter a URL in the browser panel."
    if any(word in command for word in ["compare", "vs", "versus"]):
        return "Comparison mode activated. The dashboard will compare sources and features."
    if any(word in command for word in ["memory", "remember"]):
        return "Memory mode activated. Notes will be stored in the personal memory vault."
    return "Command received. The AI browser will interpret it in the workflow engine."

def fake_status_steps():
    return [
        "Initializing AI agents...",
        "Mapping browser context...",
        "Scanning tabs and sources...",
        "Analyzing page structure...",
        "Synthesizing insights...",
        "Preparing action plan...",
        "Task completed successfully.",
    ]

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

html {
    scroll-behavior: smooth;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(139,92,246,0.25), transparent 25%),
        radial-gradient(circle at top right, rgba(59,130,246,0.22), transparent 30%),
        radial-gradient(circle at bottom, rgba(6,182,212,0.18), transparent 30%),
        linear-gradient(135deg, #020617 0%, #000000 35%, #050816 65%, #0f172a 100%);
    background-attachment: fixed;
    color: white;
}

[data-testid="stAppViewContainer"] { background: transparent; }
.main { background: transparent; }

#MainMenu, footer, header { visibility: hidden; }

.grid-bg {
    position: fixed;
    width: 100%;
    height: 100%;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(1000px) rotateX(75deg) scale(2);
    transform-origin: top;
    opacity: .16;
    z-index: -3;
    animation: gridmove 18s linear infinite;
}

@keyframes gridmove {
    0% { transform: perspective(1000px) rotateX(75deg) translateY(0) scale(2); }
    100% { transform: perspective(1000px) rotateX(75deg) translateY(50px) scale(2); }
}

.glow {
    position: fixed;
    width: 800px;
    height: 800px;
    background: radial-gradient(circle, rgba(168,85,247,.22), transparent 70%);
    filter: blur(140px);
    z-index: -1;
    top: -250px;
    left: -200px;
    animation: float 12s ease infinite;
}

.glow2 {
    position: fixed;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(59,130,246,.18), transparent 70%);
    filter: blur(140px);
    z-index: -1;
    bottom: -250px;
    right: -200px;
    animation: float2 14s ease infinite;
}

@keyframes float {
    0% { transform: translate(0,0); }
    50% { transform: translate(120px,80px); }
    100% { transform: translate(0,0); }
}

@keyframes float2 {
    0% { transform: translate(0,0); }
    50% { transform: translate(-100px,-60px); }
    100% { transform: translate(0,0); }
}

.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(18px);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,.08);
    padding: 18px 40px;
    border-radius: 22px;
    margin-bottom: 40px;
}

.nav-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(90deg, #60a5fa, #a855f7, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-links {
    display: flex;
    gap: 30px;
}

.nav-links a {
    text-decoration: none;
    color: #d1d5db;
    transition: .3s;
    font-weight: 500;
}

.nav-links a:hover {
    color: #60a5fa;
}

.hero {
    padding-top: 110px;
    padding-bottom: 80px;
    text-align: center;
}

.hero h1 {
    font-size: 90px;
    font-weight: 900;
    line-height: 1.05;
    background: linear-gradient(90deg, #60a5fa, #a855f7, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 28px;
}

.hero p {
    font-size: 24px;
    max-width: 950px;
    margin: auto;
    line-height: 1.9;
    color: #b8c1d9;
}

.hero-buttons {
    margin-top: 50px;
    display: flex;
    justify-content: center;
    gap: 22px;
    flex-wrap: wrap;
}

.primary-btn, .secondary-btn {
    display: inline-block;
    text-decoration: none;
    color: white;
    border-radius: 18px;
    padding: 18px 42px;
    transition: .4s;
}

.primary-btn {
    background: linear-gradient(135deg, #2563eb, #a855f7);
    font-weight: 700;
}

.primary-btn:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 50px rgba(99,102,241,.6);
}

.secondary-btn {
    border: 1px solid rgba(255,255,255,.1);
}

.secondary-btn:hover {
    background: rgba(255,255,255,.05);
    transform: translateY(-6px);
}

.orb {
    position: relative;
    width: 340px;
    height: 340px;
    margin: 80px auto 40px auto;
    border-radius: 50%;
    background: conic-gradient(from 0deg, #60a5fa, #a855f7, #06b6d4, #60a5fa);
    animation: spin 10s linear infinite, floatOrb 6s ease-in-out infinite;
    box-shadow:
        0 0 60px rgba(96,165,250,.5),
        0 0 120px rgba(168,85,247,.35),
        0 0 180px rgba(6,182,212,.25);
    overflow: hidden;
}

.orb::before {
    content: "";
    position: absolute;
    inset: 20px;
    border-radius: 50%;
    background: radial-gradient(circle at top, rgba(255,255,255,.35), rgba(255,255,255,.05), transparent 70%);
    filter: blur(12px);
    animation: pulse 4s ease infinite;
}

.orb::after {
    content: "";
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,.12);
    animation: rotateRing 12s linear infinite;
    filter: blur(2px);
}

@keyframes floatOrb {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
    100% { transform: translateY(0px) rotate(360deg); }
}

@keyframes spin {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}

@keyframes pulse {
    0% { opacity:.6; transform:scale(1); }
    50% { opacity:1; transform:scale(1.05); }
    100% { opacity:.6; transform:scale(1); }
}

@keyframes rotateRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(-360deg); }
}

.particles {
    position: relative;
    width: 0;
    height: 0;
    margin: auto;
}

.particle {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #60a5fa;
    box-shadow: 0 0 20px #60a5fa;
    animation: particleFloat 6s linear infinite;
}

.particle:nth-child(1) { top: -180px; left: -120px; animation-delay: 0s; }
.particle:nth-child(2) { top: -120px; left: 140px; animation-delay: 1s; }
.particle:nth-child(3) { top: 80px; left: -160px; animation-delay: 2s; }
.particle:nth-child(4) { top: 140px; left: 120px; animation-delay: 3s; }
.particle:nth-child(5) { top: 0px; left: 200px; animation-delay: 4s; }

@keyframes particleFloat {
    0% { transform: translateY(0px) scale(1); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(-40px) scale(1.5); opacity: 0; }
}

.section-title {
    font-size: 58px;
    font-weight: 900;
    text-align: center;
    margin-top: 90px;
    margin-bottom: 55px;
    color: white;
}

.feature-card {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(16px);
    padding: 35px;
    border-radius: 28px;
    transition: .45s;
    transform-style: preserve-3d;
    min-height: 220px;
}

.feature-card:hover {
    transform: rotateX(8deg) rotateY(-8deg) translateY(-14px);
    box-shadow: 0 0 50px rgba(99,102,241,.45);
}

.feature-card h3 {
    font-size: 28px;
    margin-bottom: 18px;
    color: #60a5fa;
}

.feature-card p {
    line-height: 1.9;
    color: #d1d5db;
}

.terminal {
    background: #020617;
    border: 1px solid rgba(255,255,255,.08);
    padding: 35px;
    border-radius: 24px;
    margin-top: 28px;
    font-family: monospace;
    color: #4ade80;
    line-height: 2;
    box-shadow: 0 0 40px rgba(6,182,212,.12);
}

.stat-box {
    background: rgba(255,255,255,.05);
    padding: 35px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid rgba(255,255,255,.08);
    min-height: 160px;
}

.stat-box h2 {
    font-size: 52px;
    color: #60a5fa;
}

.stat-box p {
    color: #d1d5db;
}

.testimonial {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    padding: 35px;
    border-radius: 24px;
    margin-bottom: 25px;
}

.testimonial p {
    line-height: 1.9;
    color: #d1d5db;
}

.testimonial h4 {
    margin-top: 18px;
    color: #60a5fa;
}

.launch-section {
    margin-top: 120px;
}

.launch-card {
    display: flex;
    gap: 40px;
    align-items: center;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    padding: 50px;
    border-radius: 32px;
    backdrop-filter: blur(18px);
    flex-wrap: wrap;
}

.launch-left {
    flex: 1;
    min-width: 300px;
}

.launch-left h3 {
    font-size: 42px;
    margin-bottom: 20px;
    color: white;
}

.launch-left p {
    line-height: 1.9;
    color: #d1d5db;
    margin-bottom: 25px;
}

.launch-left ul {
    line-height: 2.2;
    color: #d1d5db;
    margin-bottom: 30px;
}

.browser-window {
    flex: 1;
    min-width: 320px;
    background: #020617;
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 0 50px rgba(99,102,241,.3);
    animation: floatWindow 6s ease infinite;
}

.browser-top {
    display: flex;
    gap: 10px;
    padding: 16px;
    background: #111827;
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.red { background: #ef4444; }
.yellow { background: #facc15; }
.green { background: #22c55e; }

.browser-content {
    padding: 35px;
    font-family: monospace;
    line-height: 2.2;
    color: #4ade80;
}

@keyframes floatWindow {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

.demo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px,1fr));
    gap: 28px;
    margin-top: 28px;
}

.demo-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    padding: 35px;
    border-radius: 28px;
    transition: .4s;
}

.demo-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 0 40px rgba(99,102,241,.35);
}

.demo-card h3 {
    font-size: 28px;
    margin-bottom: 18px;
    color: #60a5fa;
}

.demo-card p {
    line-height: 1.9;
    color: #d1d5db;
}

.footer {
    margin-top: 120px;
    padding: 60px;
    text-align: center;
    color: #9ca3af;
}

.sidebar-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
}

.small-kicker {
    text-transform: uppercase;
    letter-spacing: .18em;
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 10px;
}

.command-pill {
    display: inline-block;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 999px;
    padding: 8px 14px;
    margin: 4px 6px 0 0;
    color: #cbd5e1;
    font-size: 13px;
    background: rgba(255,255,255,.04);
}

.workflow-step {
    border-left: 2px solid rgba(96,165,250,.35);
    padding-left: 14px;
    margin-bottom: 14px;
}

.mini-panel {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 24px;
    padding: 20px;
}

.holo-window {
    background:
        radial-gradient(circle at top left, rgba(96,165,250,.20), transparent 35%),
        radial-gradient(circle at bottom right, rgba(168,85,247,.18), transparent 35%),
        rgba(2,6,23,.85);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 28px;
    padding: 24px;
    min-height: 240px;
    box-shadow: 0 0 60px rgba(59,130,246,.15);
}

.holo-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 12px;
}

.holo-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.holo-chip {
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px;
    padding: 14px 16px;
}

.fake-meter {
    height: 10px;
    border-radius: 999px;
    background: rgba(255,255,255,.08);
    overflow: hidden;
}

.fake-meter > div {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #60a5fa, #a855f7, #06b6d4);
}

@media(max-width: 768px) {
    .hero h1 { font-size: 54px; }
    .hero p { font-size: 18px; }
    .section-title { font-size: 42px; }
    .nav-links { display: none; }
    .launch-card { padding: 24px; }
    .nav-flex { gap: 14px; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# BACKGROUND EFFECTS
# =========================================================

st.markdown("""
<div class="grid-bg"></div>
<div class="glow"></div>
<div class="glow2"></div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR COMMAND CENTER
# =========================================================

with st.sidebar:
    st.markdown("## 🚀 Ghildiyal AI Command Center")
    st.caption("Your browser companion, research engine, and automation console.")
    st.markdown("### Quick Modes")
    mode = st.radio(
        "Choose a mode",
        ["Browse", "Research", "Compare", "Summarize", "Automate", "Memory"],
        index=0,
        horizontal=False,
        key="sidebar_mode",
    )
    st.session_state.selected_mode = mode

    st.markdown("### Fast Commands")
    st.markdown('<span class="command-pill">Search the web</span>', unsafe_allow_html=True)
    st.markdown('<span class="command-pill">Open a URL</span>', unsafe_allow_html=True)
    st.markdown('<span class="command-pill">Summarize tabs</span>', unsafe_allow_html=True)
    st.markdown('<span class="command-pill">Save memory</span>', unsafe_allow_html=True)
    st.markdown('<span class="command-pill">Run agent</span>', unsafe_allow_html=True)

    st.markdown("### Memory Vault")
    memory_note = st.text_area("Save a note", placeholder="Remember this workflow...", height=110)
    if st.button("Save to memory", use_container_width=True):
        add_memory(memory_note)
        add_log("Saved a new memory item.")
        st.success("Saved.")

    st.markdown("### Voice Input (demo)")
    st.text_input("Voice command", key="voice_text")
    if st.button("Interpret voice", use_container_width=True):
        st.info(browser_command(st.session_state.voice_text))
        add_log(f"Voice command interpreted: {st.session_state.voice_text}")

# =========================================================
# NAVBAR
# =========================================================

st.markdown("""
<div class="navbar">
  <div class="nav-flex">
    <div class="logo">🚀 Ghildiyal AI</div>
    <div class="nav-links">
      <a href="#launch">Launch</a>
      <a href="#demo">Demo</a>
      <a href="#features">Features</a>
      <a href="#research">Research</a>
      <a href="#pricing">Pricing</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
  <h1>The Future of Autonomous Browsing</h1>
  <p>
    A cinematic AI-native browser that researches, automates workflows,
    controls apps, reasons across tabs, and executes complex tasks like a true
    browser operating system.
  </p>
  <div class="hero-buttons">
    <a class="primary-btn" href="#launch">Launch AI Browser</a>
    <a class="secondary-btn" href="#demo">Watch Live Demo</a>
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

# =========================================================
# TOP CONTROL STRIP
# =========================================================

st.markdown("---")
left, center, right = st.columns([1.2, 1.8, 1.2])

with left:
    st.markdown("### ⚙️ Browser Command")
    st.session_state.command_text = st.text_input(
        "Ask the browser to do something",
        value=st.session_state.command_text,
        label_visibility="collapsed",
    )
    if st.button("Execute command", use_container_width=True):
        response = browser_command(st.session_state.command_text)
        st.session_state.task_status = response
        add_log(response)
        st.success(response)

with center:
    st.markdown("### 🔎 Search + Open")
    col_a, col_b = st.columns([1.2, 0.8])
    with col_a:
        st.session_state.search_query = st.text_input(
            "Search query",
            value=st.session_state.search_query,
            placeholder="Search AI browsers, products, docs...",
            label_visibility="collapsed",
        )
    with col_b:
        if st.button("Search web", use_container_width=True):
            st.session_state.task_status = "Searching the web..."
            add_log(f"Searched: {st.session_state.search_query}")
    st.markdown("### 🌐 Open URL")
    st.session_state.browser_url = st.text_input(
        "URL",
        value=st.session_state.browser_url,
        placeholder="https://example.com",
        label_visibility="collapsed",
    )

with right:
    st.markdown("### 🎛 Live Status")
    st.markdown(
        f"""
        <div class="mini-panel">
            <div class="small-kicker">Mode</div>
            <div style="font-size:22px;font-weight:800;">{st.session_state.selected_mode}</div>
            <div class="small-kicker" style="margin-top:14px;">State</div>
            <div style="font-size:18px;color:#cbd5e1;">{st.session_state.task_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# REAL FUNCTIONAL PANELS
# =========================================================

st.markdown('<div id="launch"></div>', unsafe_allow_html=True)
st.markdown("## 🚀 Launch Autonomous Browser")

launch_col1, launch_col2 = st.columns([1.05, 1])

with launch_col1:
    st.markdown(
        """
        <div class="launch-card">
            <div class="launch-left">
                <h3>AI Browser Control Center</h3>
                <p>
                    Operate autonomous AI agents that browse, research, compare,
                    summarize, and automate workflows in real-time.
                </p>
                <ul>
                    <li>✔ Multi-tab AI reasoning</li>
                    <li>✔ Autonomous workflows</li>
                    <li>✔ Deep internet research</li>
                    <li>✔ AI memory engine</li>
                    <li>✔ Live browser control</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Start Session")
    session_name = st.text_input("Session name", value="Ghildiyal Session")
    start_col1, start_col2, start_col3 = st.columns(3)
    with start_col1:
        if st.button("Browse", use_container_width=True):
            st.session_state.selected_mode = "Browse"
            st.session_state.task_status = "Browse session started."
            add_log("Browse session launched.")
    with start_col2:
        if st.button("Research", use_container_width=True):
            st.session_state.selected_mode = "Research"
            st.session_state.task_status = "Research session started."
            add_log("Research session launched.")
    with start_col3:
        if st.button("Automate", use_container_width=True):
            st.session_state.selected_mode = "Automate"
            st.session_state.task_status = "Automation session started."
            add_log("Automation session launched.")

    st.markdown("### Upload a file for AI reading")
    upload = st.file_uploader("Upload PDF / text / image", type=None)
    if upload is not None:
        st.session_state.file_notes = f"Uploaded: {upload.name} ({upload.type})"
        add_log(f"File uploaded: {upload.name}")
        st.success(st.session_state.file_notes)

with launch_col2:
    st.markdown(
        """
        <div class="browser-window">
            <div class="browser-top">
                <div class="dot red"></div>
                <div class="dot yellow"></div>
                <div class="dot green"></div>
            </div>
            <div class="browser-content">
                <p>> Opening 12 websites...</p>
                <p>> Comparing AI models...</p>
                <p>> Extracting market data...</p>
                <p>> Generating insights...</p>
                <p>> Workflow completed.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Browser URL Analyzer")
    if st.button("Fetch page info", use_container_width=True):
        if st.session_state.browser_url.startswith(("http://", "https://")):
            with st.spinner("Inspecting page..."):
                info = fetch_url_info(st.session_state.browser_url)
            if info["error"]:
                st.warning(info["error"])
            else:
                st.success(info["title"])
                st.code(info["content"][:1500])
                add_log(f"Analyzed URL: {st.session_state.browser_url}")
        else:
            st.error("Use a valid URL starting with http:// or https://")

# =========================================================
# AI CHAT + SEARCH + BROWSER COMMANDS
# =========================================================

st.markdown("---")
chat_col1, chat_col2 = st.columns([1.05, 1])

with chat_col1:
    st.markdown("## 💬 AI Browser Chat")
    st.caption("Ask for summaries, plans, research, or browser steps.")
    chat_prompt = st.text_area(
        "Message",
        placeholder="Summarize this site, compare two products, or plan a workflow...",
        height=120,
    )
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        if st.button("Send to AI", use_container_width=True):
            if chat_prompt.strip():
                st.session_state.chat_history.append({"role": "user", "content": chat_prompt.strip()})
                reply = safe_llm_answer(chat_prompt.strip())
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                add_log("AI chat response generated.")
    with c2:
        if st.button("Save msg", use_container_width=True):
            if chat_prompt.strip():
                add_memory(chat_prompt.strip())
                st.success("Saved.")

    st.markdown("### Conversation")
    for msg in st.session_state.chat_history[-8:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")


# =========================================================
# SEARCH ENGINE
# =========================================================
    st.markdown("## 🔎 Search the Web")

    search_term = st.text_input(
        "Search anything",
        value="",
        placeholder="Search like Google..."
    )

if st.button("Search Web", use_container_width=True):
    st.session_state.search_query = search_term.strip()
    st.session_state.task_status = "Search completed."
    add_log(f"Search run: {search_term}")

if st.session_state.get("search_query", "").strip():
    query = st.session_state.search_query.strip()
    results = web_search(query)

    st.markdown("### Search Results")

    for result in results:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="small-kicker">{result['source']}</div>
                <div style="font-size:22px; font-weight:800; margin-top:10px;">
                    <a href="{result['link']}" target="_blank" style="color:#93c5fd; text-decoration:none;">
                        {result['title']}
                    </a>
                </div>
                <div style="color:#cbd5e1; margin-top:10px; line-height:1.8;">
                    {result['snippet']}
                </div>
                <div style="margin-top:12px; color:#60a5fa; font-size:14px;">
                    {result['link']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# DEMO SECTION
# =========================================================

st.markdown('<div id="demo"></div>', unsafe_allow_html=True)
st.markdown("## 🎥 Live AI Demonstration")

demo_cards = st.columns(3)
demo_data = [
    ("AI Research Mode", "Searches the internet, compares sources, and builds structured reports."),
    ("Autonomous Shopping", "Compares products, analyzes reviews, and recommends the best options."),
    ("Workflow Automation", "Executes repetitive browser steps across multiple websites and apps."),
]
for col, (title, desc) in zip(demo_cards, demo_data):
    with col:
        st.markdown(f"""
        <div class="demo-card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("### AI Workflow Simulation")
steps = fake_status_steps()
progress = st.slider("Simulation speed", 1, 10, 4)
if st.button("Run workflow simulation", use_container_width=True):
    for i, step in enumerate(steps):
        st.session_state.task_status = step
        st.session_state.demo_progress = int((i + 1) / len(steps) * 100)
        add_log(step)
        time.sleep(max(0.03, 0.10 - progress * 0.006))
    st.success("Workflow simulation completed.")

st.markdown(
    f"""
    <div class="terminal">
        > {steps[0]}<br>
        > {steps[1]}<br>
        > {steps[2]}<br>
        > {steps[3]}<br>
        > {steps[4]}<br>
        > {steps[5]}<br>
        > {steps[6]}
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(st.session_state.demo_progress / 100.0)

# =========================================================
# FEATURES
# =========================================================

st.markdown('<div id="features"></div>', unsafe_allow_html=True)
st.markdown("## ⚡ Next-Gen AI Features")

features = [
    ("Autonomous Web Agents", "AI agents independently execute workflows across websites and apps."),
    ("Multi-Tab Intelligence", "AI understands context across multiple tabs simultaneously."),
    ("Deep Research Engine", "Conduct in-depth research from dozens of online sources automatically."),
    ("AI Workspace Memory", "Adaptive memory learns your workflow preferences over time."),
    ("Real-Time Workflow Monitoring", "Watch every AI action step-by-step and intervene anytime."),
    ("Voice Command Navigation", "Control browser workflows naturally using voice commands."),
    ("Contextual AI Actions", "The browser anticipates what to do next."),
    ("Cross-App Automation", "Connect desktop apps and web apps in one workflow."),
    ("Secure Approval Layer", "Keep human approval on sensitive actions."),
    ("Live Knowledge Cards", "Generate dynamic research cards from the current task."),
    ("Tab Summaries", "Condense multiple sources into a single decision view."),
    ("Workspace Memory Vault", "Store notes, prompts, and reusable workflows."),
]

feature_cols = st.columns(3)
for idx, (title, desc) in enumerate(features):
    with feature_cols[idx % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# REAL AI BROWSER WORKSPACE
# =========================================================

st.markdown("## 🧭 AI Browser Workspace")
workspace_col1, workspace_col2 = st.columns([1.05, 1])

with workspace_col1:
    st.markdown("### Browser Intelligence Panel")
    tabs = st.tabs(["Research", "Agent", "Memory", "Logs", "Controls"])

    with tabs[0]:
        research_q = st.text_input("Research topic", placeholder="Top 10 AI browsers and why they matter")
        if st.button("Create research brief", use_container_width=True):
            if research_q.strip():
                brief = build_research_summary(research_q.strip())
                st.markdown(brief)
                add_log(f"Research brief created: {research_q}")

    with tabs[1]:
        agent_goal = st.text_area("Agent goal", placeholder="Plan a trip, compare products, or draft a report", height=110)
        if st.button("Run agent plan", use_container_width=True):
            if agent_goal.strip():
                response = safe_llm_answer(
                    "Create a step-by-step agent plan for this task:\n\n" + agent_goal.strip()
                )
                st.markdown(response)
                add_log("Agent plan created.")

    with tabs[2]:
        st.markdown("#### Memory Vault")
        if st.session_state.memory_items:
            for item in st.session_state.memory_items:
                st.markdown(
                    f"""
                    <div class="sidebar-card">
                        <div class="small-kicker">{item['ts']}</div>
                        <div style="color:#e2e8f0;">{item['note']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No memory saved yet.")

    with tabs[3]:
        st.markdown("#### Activity Log")
        if st.session_state.workflow_log:
            for entry in st.session_state.workflow_log:
                st.code(entry)
        else:
            st.caption("No activity yet.")

    with tabs[4]:
        st.markdown("#### Browser Controls")
        control_col1, control_col2, control_col3 = st.columns(3)
        with control_col1:
            if st.button("Browse mode", use_container_width=True):
                st.session_state.selected_mode = "Browse"
                st.session_state.task_status = "Browse mode active."
                add_log("Switched to browse mode.")
        with control_col2:
            if st.button("Research mode", use_container_width=True):
                st.session_state.selected_mode = "Research"
                st.session_state.task_status = "Research mode active."
                add_log("Switched to research mode.")
        with control_col3:
            if st.button("Automate mode", use_container_width=True):
                st.session_state.selected_mode = "Automate"
                st.session_state.task_status = "Automation mode active."
                add_log("Switched to automate mode.")

        st.markdown("#### Quick chips")
        st.markdown('<span class="command-pill">Open tabs</span>', unsafe_allow_html=True)
        st.markdown('<span class="command-pill">Compare pages</span>', unsafe_allow_html=True)
        st.markdown('<span class="command-pill">Summarize results</span>', unsafe_allow_html=True)
        st.markdown('<span class="command-pill">Store notes</span>', unsafe_allow_html=True)

with workspace_col2:
    st.markdown("### 3D Holographic Browser Card")
    st.markdown(
        """
        <div class="holo-window">
            <div class="holo-title">Live Browser Matrix</div>
            <div class="holo-row">
                <div class="holo-chip">
                    <div class="small-kicker">Focus</div>
                    <div style="font-size:22px;font-weight:800;">Autonomous context</div>
                </div>
                <div class="holo-chip">
                    <div class="small-kicker">State</div>
                    <div style="font-size:22px;font-weight:800;">Active</div>
                </div>
            </div>
            <div style="height:18px"></div>
            <div class="holo-chip">
                <div class="small-kicker">Current command</div>
                <div style="font-size:18px;">The AI browser is interpreting your task into actions.</div>
            </div>
            <div style="height:18px"></div>
            <div class="fake-meter"><div style="width: 76%;"></div></div>
            <div style="display:flex;justify-content:space-between;margin-top:10px;color:#cbd5e1;font-size:13px;">
                <span>Reasoning</span>
                <span>76%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Real action simulation")
    if st.button("Plan next action", use_container_width=True):
        action = safe_llm_answer(
            "Give the next browser action for this task: "
            + st.session_state.command_text
        )
        st.success(action)
        add_log("Planned the next action.")

# =========================================================
# AI AGENT + BROWSER AUTOMATION
# =========================================================

st.markdown("---")
st.markdown("## 🤖 AI Agent + Browser Automation")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Open a URL")
    url_to_open = st.text_input("Enter a URL", value=st.session_state.browser_url, key="url_open")
    if st.button("Inspect URL", use_container_width=True):
        if url_to_open.startswith(("http://", "https://")):
            with st.spinner("Inspecting page..."):
                info = fetch_url_info(url_to_open)
            if info["error"]:
                st.warning(info["error"])
            else:
                st.success(info["title"])
                st.text(info["content"][:1200] if info["content"] else "No visible text found.")
                add_log(f"Inspected URL: {url_to_open}")
        else:
            st.error("Enter a valid URL starting with http:// or https://")

with col2:
    st.markdown("### Agent Simulation")
    agent_instruction = st.text_area(
        "Describe an autonomous browser task",
        placeholder="Example: Research the best AI browsers and make a comparison table.",
        height=130,
    )
    if st.button("Run autonomous agent", use_container_width=True):
        if agent_instruction.strip():
            result = safe_llm_answer(
                "You are an autonomous browser agent. Create an action plan for:\n\n"
                + agent_instruction.strip()
            )
            st.markdown(result)
            add_log("Autonomous agent run completed.")

# =========================================================
# MULTI-TAB REASONING
# =========================================================

st.markdown("## 🧠 Multi-Tab Reasoning")
tab_input = st.text_area(
    "Paste multiple URLs, one per line",
    placeholder="https://example.com\nhttps://example.org",
    height=110,
)
if st.button("Summarize tabs", use_container_width=True):
    urls = [x.strip() for x in tab_input.splitlines() if x.strip()]
    if urls:
        combined = []
        for u in urls[:4]:
            fetched = fetch_url_info(u)
            snippet = fetched["content"][:900] if fetched["content"] else ""
            combined.append({"url": u, "title": fetched["title"], "snippet": snippet})
        prompt = "Summarize these tabs and compare them:\n" + json.dumps(combined, indent=2)
        summary = safe_llm_answer(prompt)
        st.markdown(summary)
        add_log("Tabs summarized.")

# =========================================================
# RESEARCH CARD GRID
# =========================================================

st.markdown("## 🔬 Research Cards")
research_cols = st.columns(3)
cards = [
    ("Deep Search", "Search the web, cluster sources, and surface evidence."),
    ("Browser Memory", "Save user intent, notes, and repeatable workflows."),
    ("Command Layer", "Convert prompts into actions and next steps."),
]
for col, (title, desc) in zip(research_cols, cards):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STATS
# =========================================================

st.markdown("## 📊 Trusted Worldwide")
stats = [
    ("10M+", "Tasks Automated"),
    ("150+", "AI Integrations"),
    ("99.9%", "Uptime"),
    ("4.9★", "User Rating"),
]
stat_cols = st.columns(4)
for col, stat in zip(stat_cols, stats):
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <h2>{stat[0]}</h2>
            <p>{stat[1]}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TESTIMONIALS
# =========================================================

st.markdown("## 💬 Stories That Inspire")
testimonials = [
    ("“This feels like Jarvis for the internet.”", "— MARLON"),
    ("“The most futuristic browser experience I've ever seen.”", "— Guri Saroy"),
    ("“Deep research and automation are insanely powerful.”", "— Felipe"),
]
for quote, author in testimonials:
    st.markdown(f"""
    <div class="testimonial">
      <p>{quote}</p>
      <h4>{author}</h4>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FAQ
# =========================================================

st.markdown("## ❓ Frequently Asked Questions")

faq = {
    "Can AI automate apps and websites?":
        "Yes. Ghildiyal AI can automate workflows across websites and desktop apps.",
    "Can I monitor AI actions in real-time?":
        "Yes. Every AI step is visible and controllable.",
    "Does it support deep research?":
        "Yes. The assistant can analyze information from multiple sources.",
    "Does it work with local files?":
        "Yes. The interface includes file upload and memory tools.",
}

for q, a in faq.items():
    with st.expander(q):
        st.write(a)

# =========================================================
# MISSION
# =========================================================

st.markdown("## 🚀 Our Mission")
st.markdown(
    """
    <div class="feature-card" style="text-align:center;">
      <h3>Empowering Humanity with Intelligent Productivity</h3>
      <p>Building the world's most advanced autonomous AI browsing platform.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# PRICING / PRODUCT ROADMAP
# =========================================================

st.markdown('<div id="pricing"></div>', unsafe_allow_html=True)
st.markdown("## 💎 Product Roadmap")

roadmap_cols = st.columns(3)
roadmap = [
    ("Starter", "Chat, search, memory vault, and smart browsing."),
    ("Pro", "Agent workflows, automation, tab summaries, and live plans."),
    ("Studio", "Team workspaces, advanced orchestration, and custom connectors."),
]
for col, (title, desc) in zip(roadmap_cols, roadmap):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

  <h2 style="color:white;">
    🚀 Ghildiyal AI Browser
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
    © 2026 Ghildiyal AI. All rights reserved.
  </p>

  <p style="
    margin-top:10px;
    font-size:14px;
    color:#60a5fa;
  ">
    Made by Adhyayan Ghildiyal
  </p>

</div>
""", unsafe_allow_html=True)
