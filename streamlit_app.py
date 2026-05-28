"""
Executive Summary:
- Added real capabilities: OpenAI chat, web search (Serper), browser automation (Playwright),
  agent example (LangChain), vector memory demo (Chroma), multi-tab reasoning (OpenAI).
- Kept all original UI/CSS unchanged. New controls are in the Launch section as requested.
- Use environment variables for keys:
    * OPENAI_API_KEY: for OpenAI (chat/completion)
    * SERPER_API_KEY: for Serper (Google search API) or set BING_API_KEY as alternative.
    * CHROMA_API_KEY: (optional) if using Chroma Cloud.
- Requires packages: streamlit, openai, requests, playwright, langchain, chromadb (see requirements.txt).
- Graceful fallbacks included if libraries or keys are missing.
"""

import os
import asyncio
import logging
import streamlit as st

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Fellou AI Browser",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# EXECUTIVE SUMMARY (display requirements)
# =========================================================
st.markdown("""
**Required files:** `requirements.txt` (list dependencies), `.streamlit/secrets.toml` (for API keys).  
**Environment variables:** 
- `OPENAI_API_KEY`: your OpenAI secret key  
- `SERPER_API_KEY`: your Serper.dev API key for Google Search (or use `BING_API_KEY` for Bing Search)  
- (optional) `CHROMA_API_KEY`: Chroma Cloud API key if using Cloud instance.  
If keys are missing, fallbacks or dummy responses will be used.
""", unsafe_allow_html=True)

st.markdown("""| File | Purpose |
| --- | --- |
| `streamlit_app.py` | Main Streamlit app (this file) |
| `requirements.txt` | Lists Python dependencies (`streamlit`, `openai`, `requests`, `playwright`, `langchain`, `chromadb`) |
| `.streamlit/secrets.toml` | (Optional) Place API keys here under [general] e.g. `OPENAI_API_KEY = "..."` |
""", unsafe_allow_html=True)

# =========================================================
# MERMAID DIAGRAM: UI -> LLM -> Agent -> Browser -> Memory
# =========================================================
st.markdown("""
<div class="mermaid">
graph LR
    UI["Streamlit UI"] --> LLM["LLM (OpenAI)"]
    LLM --> Agent["Agent (LangChain)"]
    Agent --> Browser["Browser Automation (Playwright)"]
    Agent --> Memory["Memory Store (Chroma)"]
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });</script>
""", unsafe_allow_html=True)

# =========================================================
# IMPORTS AND INITIALIZATION FOR FEATURES
# =========================================================

# OpenAI setup
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    try:
        import openai
        openai.api_key = openai_key
    except ImportError:
        openai = None
        logging.error("OpenAI library not installed.")
else:
    openai = None
    logging.info("OPENAI_API_KEY not set; ChatGPT functionality will use fallback responses.")

# Serper (Google Search) or Bing Search setup
serper_key = os.getenv("SERPER_API_KEY")
bing_key = os.getenv("BING_API_KEY")
# Attempt to import requests for web queries
try:
    import requests
except ImportError:
    requests = None
    logging.error("Requests library not installed; web search disabled.")

# Playwright setup
try:
    from playwright.async_api import async_playwright
    playwright_available = True
except ImportError:
    playwright_available = False
    logging.warning("Playwright not installed; browser automation will use fallback.")
except Exception as e:
    playwright_available = False
    logging.error(f"Playwright import error: {e}")

# LangChain (Agent) setup
try:
    from langchain.agents import Tool, AgentExecutor, initialize_agent
    from langchain.llms import OpenAI as LangChainOpenAI
    agent_available = True
except ImportError:
    agent_available = False
    logging.warning("LangChain not installed; agent example will use dummy logic.")

# Chroma (Memory) setup
try:
    import chromadb
    from chromadb.utils import embedding_functions
    memory_available = True
    # Initialize local Chroma client
    chroma_client = chromadb.Client()
    memory_collection = chroma_client.get_or_create_collection("browser_memory")
except ImportError:
    memory_available = False
    logging.warning("Chroma not installed; using in-memory list for memory.")
    memory_collection = []
except Exception as e:
    memory_available = False
    logging.error(f"Chroma error: {e}")
    memory_collection = []

# Fallback memory list if Chroma is unavailable
if not memory_available:
    memory_texts = []  # simple list to store memory strings

# =========================================================
# BACKEND FEATURE FUNCTIONS
# =========================================================

# Function: Chat with LLM
def chat_with_ai(prompt):
    if openai:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return "Error in OpenAI API call."
    else:
        # Fallback: simple placeholder
        return f"*No API key.* Echo: {prompt}"

# Function: Perform a web search (Serper or Bing)
def search_web(query):
    if serper_key and requests:
        try:
            url = "https://google.serper.dev/search"
            headers = {"X-API-KEY": serper_key}
            params = {"q": query, "hl": "en", "gl": "us"}
            res = requests.get(url, headers=headers, params=params, timeout=10)
            data = res.json()
            results = []
            for item in data.get("organic", []):
                title = item.get("title")
                link = item.get("link")
                snippet = item.get("snippet")
                results.append(f"[{title}]({link}) - {snippet}")
            return results or ["No results found."]
        except Exception as e:
            logging.error(f"Serper search error: {e}")
            return ["Error performing search."]
    elif bing_key and requests:
        try:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": bing_key}
            params = {"q": query, "textDecorations": False, "textFormat": "HTML"}
            res = requests.get(url, headers=headers, params=params, timeout=10)
            data = res.json()
            results = []
            for item in data.get("webPages", {}).get("value", []):
                name = item.get("name")
                link = item.get("url")
                snippet = item.get("snippet")
                results.append(f"[{name}]({link}) - {snippet}")
            return results or ["No results found."]
        except Exception as e:
            logging.error(f"Bing search error: {e}")
            return ["Error performing search."]
    else:
        return ["No search API key found (set SERPER_API_KEY or BING_API_KEY)."]

# Function: Browser automation using Playwright
async def get_page_info(url):
    title = ""
    screenshot = None
    if not playwright_available:
        return title, screenshot
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=15000)
            title = await page.title()
            path = "/tmp/screenshot.png"
            await page.screenshot(path=path, full_page=True)
            await browser.close()
            return title, path
    except Exception as e:
        logging.error(f"Playwright failed: {e}")
        return "", None

# Function: Simple agent demonstration (search + chat)
def run_agent(task):
    if agent_available and openai:
        tools = [
            Tool(
                name="Google Search",
                func=lambda q: "\n".join(search_web(q)),
                description="Search the web for information"
            )
        ]
        llm = LangChainOpenAI(temperature=0)
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
        try:
            result = agent.run(task)
            return result
        except Exception as e:
            logging.error(f"Agent error: {e}")
            return f"Agent error: {e}"
    else:
        return f"*Agent not available.* Task was: {task}"

# Function: Summarize multiple URLs
def summarize_tabs(urls_list):
    combined_text = ""
    for u in urls_list:
        if requests:
            try:
                res = requests.get(u, timeout=5)
                combined_text += res.text[:1000]
            except Exception as e:
                logging.error(f"Failed to fetch {u}: {e}")
    if not combined_text:
        return "No content to summarize."
    if openai:
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize the following content: {combined_text[:4000]}"}]
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI summarize error: {e}")
            return "Error in summarization."
    else:
        return "Summarization not available (no OpenAI key)."

# =========================================================
# BACKGROUND EFFECTS (retain existing UI CSS)
# =========================================================
st.markdown("""
<div class="grid-bg"></div>
<div class="glow"></div>
<div class="glow2"></div>
""", unsafe_allow_html=True)

# =========================================================
# NAVBAR
# =========================================================
st.markdown("""
<div class="navbar">
  <div class="nav-flex">
    <div class="logo">
      🚀 Fellou AI
    </div>
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
    An AI-native browser that researches, automates workflows,
    controls apps, reasons across tabs,
    and executes complex tasks autonomously.
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
# LAUNCH SECTION
# =========================================================
st.markdown("""
<div id="launch" class="launch-section">
  <h2 class="section-title">🚀 Launch Autonomous Browser</h2>
  <div class="launch-card">
    <div class="launch-left">
      <h3>AI Browser Control Center</h3>
      <p>
        Operate autonomous AI agents that browse,
        research, compare, summarize,
        and automate workflows in real-time.
      </p>
      <ul>
        <li>✔ Multi-tab AI reasoning</li>
        <li>✔ Autonomous workflows</li>
        <li>✔ Deep internet research</li>
        <li>✔ AI memory engine</li>
        <li>✔ Live browser control</li>
      </ul>
      <a class="primary-btn" href="#">Start AI Session</a>
      <br>
    </div>
    <div class="launch-right">
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
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- NEW UI CONTROLS BELOW ---
st.subheader("💬 Chat with AI Browser Agent")
user_query = st.text_input("Ask a question to the AI browser:", "")
if st.button("Send Chat"):
    answer = chat_with_ai(user_query)
    st.write(answer)

st.subheader("🔎 Web Search (Serper API or Bing)")
search_query = st.text_input("Enter search query:", "")
if st.button("Search"):
    if search_query:
        results = search_web(search_query)
        for res in results:
            st.markdown(res, unsafe_allow_html=True)

st.subheader("🌐 Browser Automation Demo (Playwright)")
fetch_url = st.text_input("Enter URL to fetch:", "")
if st.button("Fetch URL Title & Screenshot"):
    if fetch_url:
        # Attempt to fetch via Playwright if available
        title, screenshot_path = "", None
        try:
            if playwright_available:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                title, screenshot_path = loop.run_until_complete(get_page_info(fetch_url))
        except Exception as e:
            logging.error(f"Playwright error: {e}")
        # Fallback for title
        if not title and requests:
            try:
                res = requests.get(fetch_url, timeout=5)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(res.text, 'html.parser')
                title = soup.title.string if soup.title else "No title found"
            except Exception as e:
                title = f"Failed to retrieve title: {e}"
        st.write(f"**Page Title:** {title}")
        if screenshot_path:
            st.image(screenshot_path, caption="📷 Screenshot of the page")
        else:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (800, 600), color=(30, 30, 30))
            d = ImageDraw.Draw(img)
            d.text((20, 300), "Screenshot not available", fill=(200,200,200))
            st.image(img, caption="Screenshot not available")

st.subheader("🤖 AI Agent Orchestration Example")
agent_task = st.text_input("Describe a task for the AI agent:", "")
if st.button("Run Agent"):
    if agent_task:
        result = run_agent(agent_task)
        st.write(result)

st.subheader("🧠 Vector Memory Demo")
mem_input = st.text_input("Type something to store in memory:", "")
if st.button("Save to Memory"):
    if mem_input:
        if memory_available:
            try:
                memory_collection.add(
                    ids=[str(len(memory_collection.get(ids=[], query_texts=[mem_input])['ids'][0]) )],
                    documents=[mem_input]
                )
                st.write("✅ Saved to Chroma memory collection.")
            except Exception as e:
                st.write(f"Error saving to Chroma: {e}")
        else:
            memory_texts.append(mem_input)
            st.write("✅ Saved to in-memory list.")
st.write("**Memory Contents:**")
if memory_available:
    try:
        docs = memory_collection.query(query_texts=[""], n_results=10)
        st.write(docs)
    except Exception as e:
        st.write(f"Memory query error: {e}")
else:
    st.write(memory_texts)

st.subheader("📑 Multi-Tab Reasoning Demo")
urls_input = st.text_area("Enter multiple URLs (comma-separated):", "")
if st.button("Analyze Tabs"):
    if urls_input:
        urls_list = [u.strip() for u in urls_input.split(",") if u.strip()]
        summary = summarize_tabs(urls_list)
        st.write(summary)

# =========================================================
# LIVE DEMO SECTION
# =========================================================
st.markdown("""
<div id="demo">
  <h2 class="section-title">🎥 Live AI Demonstration</h2>
  <div class="demo-grid">
    <div class="demo-card">
      <h3>AI Research Mode</h3>
      <p>
        The AI independently searches the internet,
        compares sources,
        and generates structured reports.
      </p>
    </div>
    <div class="demo-card">
      <h3>Autonomous Shopping</h3>
      <p>
        AI agents compare products,
        analyze reviews,
        and recommend best choices instantly.
      </p>
    </div>
    <div class="demo-card">
      <h3>Workflow Automation</h3>
      <p>
        Execute repetitive workflows automatically
        across multiple websites and apps.
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# AI TERMINAL
# =========================================================
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

# =========================================================
# FEATURES
# =========================================================
st.markdown("""
<div id="features">
<h2 class="section-title">⚡ Next-Gen AI Features</h2>
</div>
""", unsafe_allow_html=True)
features = [
    ("Autonomous Web Agents", "AI agents independently execute workflows across websites and apps."),
    ("Multi-Tab Intelligence", "AI understands context across multiple tabs simultaneously."),
    ("Deep Research Engine", "Conduct in-depth research from dozens of online sources automatically."),
    ("AI Workspace Memory", "Adaptive memory system learns your workflow preferences over time."),
    ("Real-Time Workflow Monitoring", "Watch every AI action step-by-step and intervene anytime."),
    ("Voice Command Navigation", "Control browser workflows naturally using voice commands.")
]
cols = st.columns(3)
for i, (title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
        <h3>{title}</h3>
        <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# STATS
# =========================================================
st.markdown("""
<h2 class="section-title">📊 Trusted Worldwide</h2>
""", unsafe_allow_html=True)
stats = [("10M+","Tasks Automated"),("150+","AI Integrations"),("99.9%","Uptime"),("4.9★","User Rating")]
cols = st.columns(len(stats))
for col, stat in zip(cols, stats):
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
st.markdown("""
<h2 class="section-title">💬 Stories That Inspire</h2>
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

# =========================================================
# FAQ
# =========================================================
st.markdown("""
<h2 class="section-title">❓ Frequently Asked Questions</h2>
""", unsafe_allow_html=True)
faq = {
    "Can AI automate apps and websites?": "Yes. Fellou AI autonomously executes workflows across websites and desktop apps.",
    "Can I monitor AI actions in real-time?": "Yes. Every AI step is visible and controllable.",
    "Does it support deep research?": "Yes. The AI analyzes information from multiple sources simultaneously.",
    "Does it work with local files?": "Absolutely. AI can manage and operate local desktop files."
}
for q, a in faq.items():
    with st.expander(q):
        st.write(a)

# =========================================================
# MISSION
# =========================================================
st.markdown("""
<h2 class="section-title">🚀 Our Mission</h2>
<div class="feature-card" style="text-align:center;">
  <h3>Empowering Humanity with Intelligent Productivity</h3>
  <p>Building the world's most advanced autonomous AI browsing platform.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
  <h2 style="color:white;">🚀 Fellou AI Browser</h2>
  <p>AI-native autonomous browsing platform</p><br>
  <p>Features • Research • Docs • API • Contact • Github</p><br>
  <p>© 2026 Fellou AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
