import os
import re
import ast
import json
import time
import math
import html
import random
import asyncio
import operator as op
from datetime import datetime
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

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

# =========================================================
# RESEARCH DATA: AI BROWSER MARKET SCAN
# =========================================================

AI_BROWSER_LANDSCAPE = [
    {"name": "Dia", "class": "AI-native browser", "signature": "Proactive workspace context, briefs, tab-aware answers", "lesson": "AI should understand user workflow, not only a single prompt."},
    {"name": "Arc", "class": "Productivity browser", "signature": "Spaces, profiles, split view, organized browsing", "lesson": "Browser structure is a product feature."},
    {"name": "Arc Search", "class": "Mobile AI browser", "signature": "Browse-for-me answer-first search", "lesson": "Users like direct synthesized answers before raw links."},
    {"name": "Arc Max", "class": "AI feature layer", "signature": "Previews, AI summaries, tidied titles/downloads", "lesson": "Small AI utilities save time."},
    {"name": "Perplexity Comet", "class": "AI-native browser", "signature": "Research, shopping, email and assistant-style browsing", "lesson": "The browser can become a personal assistant."},
    {"name": "Opera One", "class": "Mainstream AI browser", "signature": "Tab Islands, modular UI, AI sidebar", "lesson": "Tabs need intelligent grouping."},
    {"name": "Opera Aria", "class": "AI browser layer", "signature": "Page context, image generation, file analysis, voice", "lesson": "AI should work across content types."},
    {"name": "Opera GX", "class": "Gaming browser", "signature": "Theming, sidebar apps, gaming utilities", "lesson": "A browser can target a specific audience."},
    {"name": "Opera Air", "class": "Wellness browser", "signature": "Breaks, boosts, mindful browsing", "lesson": "Emotional design differentiates commodity browsers."},
    {"name": "Opera Neon", "class": "Agentic browser", "signature": "Automates tasks and understands web pages", "lesson": "Task execution is the next frontier."},
    {"name": "Brave Leo", "class": "Privacy AI layer", "signature": "Private AI chat, page/PDF summaries, BYOM", "lesson": "Privacy and model choice matter."},
    {"name": "DuckDuckGo Browser", "class": "Privacy browser", "signature": "Private search, tracker blocking, optional AI", "lesson": "Trust can be the main product story."},
    {"name": "Duck.ai", "class": "Private AI chat", "signature": "Multi-model AI with privacy posture", "lesson": "AI access should feel safe and optional."},
    {"name": "Microsoft Edge Copilot", "class": "Mainstream AI browser", "signature": "Copilot, tab understanding, browsing assistance", "lesson": "AI is moving into default browsers."},
    {"name": "Google Chrome Gemini", "class": "Mainstream AI browser", "signature": "Gemini for tabs, summaries and browsing context", "lesson": "Search and browser AI are merging."},
    {"name": "Safari + Apple Intelligence", "class": "System AI browser", "signature": "On-device privacy, summaries, writing help", "lesson": "Local/private processing is a strong trust message."},
    {"name": "Firefox AI Chatbot", "class": "Mainstream AI browser", "signature": "Provider choice, sidebar chatbot, selected-text prompts", "lesson": "Open choice can be a differentiator."},
    {"name": "Samsung Internet", "class": "Mobile AI browser", "signature": "Ask AI, summarize, translate, read aloud", "lesson": "Mobile browsing needs quick actions."},
    {"name": "SigmaOS", "class": "Productivity browser", "signature": "Tabs-as-tasks and workspaces", "lesson": "Workflow organization reduces tab chaos."},
    {"name": "SigmaOS Airis", "class": "AI browser engine", "signature": "Contextual answers and internet lookup", "lesson": "AI should be native to the browser surface."},
    {"name": "Wavebox", "class": "Work browser", "signature": "Multi-account apps, spaces, split screen", "lesson": "Professional users need account/workspace separation."},
    {"name": "Wavebox Brainbox", "class": "AI work assistant", "signature": "AI on every page, custom skills", "lesson": "Custom skills create defensibility."},
    {"name": "Fellou", "class": "Agentic browser", "signature": "Deep action, shadow workspace, visible workflows", "lesson": "Users need to watch and trust automation."},
    {"name": "Shift Browser", "class": "Productivity browser", "signature": "Apps, workspaces, builder customization", "lesson": "Customization can turn a browser into an OS."},
    {"name": "Shift AI", "class": "AI productivity layer", "signature": "Private writing, summarizing, answer tools", "lesson": "AI should be available where work happens."},
    {"name": "BrowserOS", "class": "Open-source agentic browser", "signature": "Built-in AI agents, BYO LLM, MCP integrations", "lesson": "Open-source and connectors can build power-user trust."},
    {"name": "Aloha Browser", "class": "Privacy browser", "signature": "VPN, ad blocking, privacy utilities", "lesson": "Security utilities can create stickiness."},
    {"name": "Aloha Private AI", "class": "Private AI layer", "signature": "Private AI and ad-blocking intelligence", "lesson": "AI + privacy is a strong positioning pair."},
    {"name": "Maxthon", "class": "AI-era browser", "signature": "Notes, password manager, AI chat", "lesson": "Utility bundles can compete with AI-only tools."},
    {"name": "Sidekick", "class": "Productivity browser", "signature": "App sidebar, work apps, focus workflows", "lesson": "App-centric navigation is better for professionals."},
    {"name": "You.com Browser/Search", "class": "Answer engine", "signature": "AI search and research answers", "lesson": "Search result synthesis is central."},
    {"name": "Phind", "class": "AI search for developers", "signature": "Technical answers and source-backed search", "lesson": "Niche vertical AI can beat generic search."},
    {"name": "Kagi Assistant", "class": "Premium search + AI", "signature": "Paid private search and AI tools", "lesson": "Quality can justify subscription."},
    {"name": "Andi", "class": "AI search browser-like UX", "signature": "Conversational search cards", "lesson": "Clean answer UI matters."},
    {"name": "Neeva AI Legacy", "class": "AI search precedent", "signature": "Answer-first search with sources", "lesson": "Citation-first search is not optional."},
    {"name": "Vivaldi", "class": "Power-user browser", "signature": "Tab stacks, panels, customization", "lesson": "Power users value control over AI hype."},
    {"name": "Yandex Browser", "class": "AI-enhanced browser", "signature": "Translation, assistants, smart services", "lesson": "Localized AI can win regional markets."},
    {"name": "Naver Whale", "class": "Regional productivity browser", "signature": "Sidebar tools and local ecosystem", "lesson": "Ecosystem integrations create retention."},
    {"name": "QQ Browser", "class": "Regional super-app browser", "signature": "Content, services, utility integration", "lesson": "Browsers can become service hubs."},
    {"name": "UC Browser", "class": "Mobile utility browser", "signature": "Data-saving and mobile optimization", "lesson": "Performance remains a feature."},
    {"name": "Kiwi Browser", "class": "Mobile power browser", "signature": "Extensions on Android", "lesson": "Extensibility differentiates mobile."},
    {"name": "Orion Browser", "class": "Privacy/performance browser", "signature": "WebKit, extensions, performance", "lesson": "Speed and compatibility still matter."},
    {"name": "Mullvad Browser", "class": "Privacy browser", "signature": "Anti-fingerprinting and privacy posture", "lesson": "Privacy can be deeply technical."},
    {"name": "Tor Browser", "class": "Anonymity browser", "signature": "Onion routing and strong anonymity", "lesson": "Different users need different threat models."},
    {"name": "LibreWolf", "class": "Privacy browser", "signature": "Firefox hardening and privacy defaults", "lesson": "Default settings communicate values."},
    {"name": "Waterfox", "class": "Independent browser", "signature": "Firefox-like independence and customization", "lesson": "Independence can appeal to enthusiasts."},
    {"name": "Pale Moon", "class": "Legacy/power browser", "signature": "Classic browser philosophy", "lesson": "Not all users want modern complexity."},
    {"name": "Zen Browser", "class": "Modern Firefox-based browser", "signature": "Beautiful UI and tab organization", "lesson": "Aesthetic browser design matters."},
    {"name": "Floorp", "class": "Firefox-based productivity browser", "signature": "Workspaces, sidebar, custom layout", "lesson": "Open productivity UX has space to grow."},
    {"name": "Thorium", "class": "Performance browser", "signature": "Chromium performance build", "lesson": "Performance and AI should coexist."},
]

UNIQUE_FEATURES = [
    ("Answer-first Search", "Every search produces a clear AI answer before raw links."),
    ("Source Confidence", "Each result gets a basic quality score and visible source chip."),
    ("Compare Mode", "Select multiple results and ask the app to compare them."),
    ("Workspace Memory", "Save research sessions under named workspaces."),
    ("Privacy Switches", "Control whether the app remembers context and uses previous searches."),
    ("Report Export", "Download a Markdown research brief from the current session."),
    ("Agent Workflow", "Turn goals into visible step-by-step browser actions."),
    ("URL Intelligence", "Fetch and summarize a page directly from its URL."),
    ("Quick Follow-ups", "One-click prompts for deeper summary, pros/cons, steps, and caveats."),
    ("Market Radar", "Built-in research matrix of AI browser competitors and lessons."),
]

# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "chat_history": [
        {"role": "assistant", "content": "Ready. Ask me to search, browse, summarize, compare, or automate."}
    ],
    "workflow_log": [],
    "memory_items": [],
    "task_status": "Idle",
    "demo_progress": 0,
    "selected_mode": "Research",
    "browser_url": "https://example.com",
    "search_query": "",
    "command_text": "Research the latest AI browser trends",
    "voice_text": "Open research mode and compare AI browsers",
    "file_notes": "",
    "last_search_results": [],
    "last_answer": "",
    "last_compare": "",
    "workspace_name": "Default Workspace",
    "saved_workspaces": {},
    "remember_context": True,
    "use_previous_context": True,
    "source_mode": "Balanced",
    "answer_style": "Executive brief",
    "result_limit": 6,
    "quick_prompt": "",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def add_log(message: str, kind: str = "info") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(kind, "ℹ️")
    st.session_state.workflow_log.insert(0, f"[{ts}] {emoji} {message}")
    st.session_state.workflow_log = st.session_state.workflow_log[:25]


def add_memory(note: str) -> None:
    note = (note or "").strip()
    if note:
        st.session_state.memory_items.insert(
            0,
            {"note": note, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        )
        st.session_state.memory_items = st.session_state.memory_items[:30]


def h(text) -> str:
    return html.escape(str(text or ""), quote=True)


def normalize_result_link(link: str) -> str:
    """Clean provider links so DuckDuckGo redirects become real clickable URLs."""
    link = (link or "").strip()
    if not link:
        return ""

    if link.startswith("//"):
        link = "https:" + link
    elif link.startswith("/"):
        link = "https://duckduckgo.com" + link
    elif link.startswith("www."):
        link = "https://" + link

    if "uddg=" in link:
        parsed = urlparse(link)
        qs = parse_qs(parsed.query)
        if "uddg" in qs and qs["uddg"]:
            link = unquote(qs["uddg"][0])

    parsed = urlparse(link)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return ""

    return link


def short_url(url: str, limit: int = 78) -> str:
    if not url:
        return ""
    cleaned = url.replace("https://", "").replace("http://", "")
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3] + "..."


def get_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return ""


def safe_eval_math(query: str):
    math_expr = query.strip().replace("×", "*").replace("÷", "/")
    if not re.fullmatch(r"[0-9\.\+\-\*\/\%\(\)\s\^]+", math_expr):
        return None
    math_expr = math_expr.replace("^", "**")

    allowed_bin_ops = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
    }
    allowed_unary_ops = {ast.UAdd: op.pos, ast.USub: op.neg}

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed")
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            if type(node.op) not in allowed_bin_ops:
                raise ValueError("Invalid operator")
            return allowed_bin_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in allowed_unary_ops:
                raise ValueError("Invalid unary operator")
            return allowed_unary_ops[type(node.op)](_eval(node.operand))
        raise ValueError("Unsafe expression")

    try:
        node = ast.parse(math_expr, mode="eval")
        result = _eval(node)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return result
    except Exception:
        return None


def safe_llm_answer(prompt: str, system: str = "You are a helpful AI browser assistant.") -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if OpenAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.35,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            return f"OpenAI error: {e}"

    return demo_llm_answer(prompt)


def demo_llm_answer(prompt: str) -> str:
    """Useful local fallback when OPENAI_API_KEY is not connected."""
    lower = prompt.lower()
    if "compare" in lower:
        return (
            "### Demo comparison\n\n"
            "Connect `OPENAI_API_KEY` for a real model-generated comparison. Based on the provided snippets, "
            "I would compare each source by: purpose, key claim, evidence, pricing/availability, and risks."
        )
    if "agent" in lower or "step" in lower:
        return (
            "### Demo agent plan\n\n"
            "1. Understand the goal.\n"
            "2. Search the web.\n"
            "3. Read the top sources.\n"
            "4. Compare claims and remove duplicates.\n"
            "5. Prepare a decision-ready answer.\n\n"
            "Connect `OPENAI_API_KEY` for live AI reasoning."
        )
    return (
        "### Demo AI answer\n\n"
        "Your app is running in demo mode because `OPENAI_API_KEY` is not connected. "
        "The search results below are still useful. After you add the key in Streamlit secrets or environment variables, "
        "this panel will generate a real answer from the sources.\n\n"
        "**Prompt received:**\n\n"
        f"> {prompt[:900]}"
    )


def quality_score(result: dict) -> int:
    url = result.get("link", "") or ""
    domain = get_domain(url)
    score = 50
    if domain:
        score += 10
    if any(x in domain for x in ["gov", "edu", "org"]):
        score += 15
    if result.get("snippet"):
        score += 10
    if result.get("source") in {"Tavily", "Serper"}:
        score += 5
    if "duckduckgo.com/l/" in url:
        score -= 15
    return max(0, min(100, score))


def apply_source_mode(query: str, source_mode: str) -> str:
    q = query.strip()
    if source_mode == "Official sources only":
        return f"{q} official site OR documentation OR government OR company"
    if source_mode == "Recent / news focused":
        return f"{q} latest news recent update 2026"
    if source_mode == "Technical docs":
        return f"{q} documentation API guide docs"
    if source_mode == "Indian context":
        return f"{q} India Indian context"
    return q


def web_search(query: str, max_results: int = 6, source_mode: str = "Balanced"):
    """
    Search using Tavily or Serper if API keys are set.
    Otherwise use DuckDuckGo HTML search without API key.
    Returns list of dicts: title, link, snippet, source, score, domain.
    """
    results = []
    query = (query or "").strip()
    if not query:
        return results

    calc = safe_eval_math(query)
    if calc is not None:
        return [{
            "title": f"Answer: {calc}",
            "link": "",
            "snippet": f"{query} = {calc}",
            "source": "Calculator",
            "score": 100,
            "domain": "local",
        }]

    search_query = apply_source_mode(query, source_mode)
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()

    if requests is not None and tavily_key:
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": tavily_key, "query": search_query, "max_results": max_results},
                timeout=20,
            )
            data = r.json()
            for item in data.get("results", [])[:max_results]:
                link = normalize_result_link(item.get("url", ""))
                result = {
                    "title": item.get("title", "No Title"),
                    "link": link,
                    "snippet": item.get("content", ""),
                    "source": "Tavily",
                    "domain": get_domain(link),
                }
                result["score"] = quality_score(result)
                results.append(result)
            if results:
                return results
        except Exception as e:
            add_log(f"Tavily search failed: {e}", "warning")

    if requests is not None and serper_key:
        try:
            r = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": search_query, "num": max_results},
                timeout=20,
            )
            data = r.json()
            for item in data.get("organic", [])[:max_results]:
                link = normalize_result_link(item.get("link", ""))
                result = {
                    "title": item.get("title", "No Title"),
                    "link": link,
                    "snippet": item.get("snippet", ""),
                    "source": "Serper",
                    "domain": get_domain(link),
                }
                result["score"] = quality_score(result)
                results.append(result)
            if results:
                return results
        except Exception as e:
            add_log(f"Serper search failed: {e}", "warning")

    if requests is not None and BeautifulSoup is not None:
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(search_query)}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.select(".result")
            for card in cards[:max_results]:
                title_tag = card.select_one("a.result__a")
                snippet_tag = card.select_one("a.result__snippet") or card.select_one(".result__snippet")
                title = title_tag.get_text(" ", strip=True) if title_tag else "No Title"
                link = normalize_result_link(title_tag.get("href", "") if title_tag else "")
                snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""
                if title or snippet:
                    result = {
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                        "source": "DuckDuckGo",
                        "domain": get_domain(link),
                    }
                    result["score"] = quality_score(result)
                    results.append(result)
            if results:
                return results
        except Exception as e:
            return [{
                "title": "Search error",
                "link": "",
                "snippet": str(e),
                "source": "DuckDuckGo",
                "domain": "",
                "score": 0,
            }]

    return [{
        "title": f"Search results for '{query}'",
        "link": "https://duckduckgo.com",
        "snippet": "No live search available. Install requests and beautifulsoup4, or add Tavily/Serper API keys.",
        "source": "Fallback",
        "domain": "duckduckgo.com",
        "score": 40,
    }]


def build_answer_from_results(query: str, results: list, answer_style: str = "Executive brief") -> str:
    if not results:
        return "No search results found. Try another query."

    source_block = []
    for idx, item in enumerate(results, 1):
        source_block.append(
            f"[{idx}] Title: {item.get('title','')}\n"
            f"URL: {item.get('link','')}\n"
            f"Source: {item.get('source','')} | Domain: {item.get('domain','')} | Score: {item.get('score','')}\n"
            f"Snippet: {item.get('snippet','')}"
        )

    context_note = ""
    if st.session_state.use_previous_context and st.session_state.memory_items:
        latest_notes = [m["note"] for m in st.session_state.memory_items[:5]]
        context_note = "\nRelevant user notes:\n" + "\n".join(f"- {n}" for n in latest_notes)

    prompt = f"""
User searched: {query}
Answer style required: {answer_style}

Create a practical answer from the search results. Use this format:
1. Direct answer
2. Key points
3. What to verify
4. Best sources to open next

Do not invent facts not present in sources. If sources are weak, say so clearly.

Search results:
{chr(10).join(source_block)}
{context_note}
""".strip()

    return safe_llm_answer(
        prompt,
        system=(
            "You are an AI-native browser assistant. Be accurate, source-aware, concise, and practical. "
            "Use the supplied search snippets only unless clearly explaining uncertainty."
        ),
    )


def compare_results(query: str, selected_results: list) -> str:
    if len(selected_results) < 2:
        return "Select at least two sources to compare."
    items = []
    for idx, item in enumerate(selected_results, 1):
        items.append(
            f"{idx}. {item.get('title','')}\nURL: {item.get('link','')}\nSnippet: {item.get('snippet','')}"
        )
    prompt = f"""
Compare these sources for the user query: {query}

Return a table with:
- Source
- Main claim
- What is useful
- What is missing or risky
- Best use

Then give a final recommendation.

Sources:
{chr(10).join(items)}
""".strip()
    return safe_llm_answer(prompt, system="You compare web sources like an expert research analyst.")


def build_agent_plan(goal: str) -> str:
    prompt = f"""
Create an autonomous browser workflow for this goal:
{goal}

Output:
- Goal interpretation
- Step-by-step browser actions
- Information to collect
- Human approval checkpoints
- Final deliverable
""".strip()
    return safe_llm_answer(prompt, system="You design safe, inspectable browser automation workflows.")


async def fetch_url_info_async(url: str):
    if not PLAYWRIGHT_AVAILABLE:
        return {"title": "Playwright unavailable", "content": "", "error": "Install playwright for full browser fetching."}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1440, "height": 1200})
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            title = await page.title()
            text = await page.locator("body").inner_text(timeout=10000)
            await browser.close()
            return {"title": title, "content": text[:7000], "error": ""}
    except Exception as e:
        return {"title": "", "content": "", "error": str(e)}


def fetch_url_info(url: str):
    url = normalize_result_link(url)
    if not url.startswith(("http://", "https://")):
        return {"title": "", "content": "", "error": "Use a valid URL starting with http:// or https://"}

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
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            title = "Fetched page"
            content = r.text[:7000]
            if BeautifulSoup:
                soup = BeautifulSoup(r.text, "html.parser")
                title = soup.title.get_text(" ", strip=True) if soup.title else title
                for tag in soup(["script", "style", "noscript"]):
                    tag.extract()
                content = soup.get_text(" ", strip=True)[:7000]
            return {"title": title, "content": content, "error": ""}
        except Exception as e:
            return {"title": "", "content": "", "error": str(e)}

    return {"title": "", "content": "", "error": "requests unavailable"}


def build_research_summary(query: str):
    results = web_search(query, st.session_state.result_limit, st.session_state.source_mode)
    return build_answer_from_results(query, results, st.session_state.answer_style)


def browser_command(command: str):
    command = (command or "").lower().strip()
    if any(word in command for word in ["search", "research", "find"]):
        return "Research mode activated. Search results and answer synthesis are ready."
    if any(word in command for word in ["summarize", "summary"]):
        return "Summary mode activated. The assistant will compress sources into insights."
    if any(word in command for word in ["open", "browse", "visit"]):
        return "Browse mode activated. Enter a URL in the browser panel."
    if any(word in command for word in ["compare", "vs", "versus"]):
        return "Comparison mode activated. Select sources and compare them."
    if any(word in command for word in ["memory", "remember"]):
        return "Memory mode activated. Notes can be saved into workspace memory."
    if any(word in command for word in ["agent", "automate", "workflow"]):
        return "Agent mode activated. Describe a task to create a browser action plan."
    return "Command received. The AI browser will interpret it in the workflow engine."


def fake_status_steps():
    return [
        "Initializing AI agents...",
        "Mapping browser context...",
        "Scanning sources...",
        "Normalizing links...",
        "Ranking source confidence...",
        "Synthesizing answer...",
        "Preparing next actions...",
        "Task completed successfully.",
    ]


def save_current_workspace():
    name = st.session_state.workspace_name.strip() or "Default Workspace"
    st.session_state.saved_workspaces[name] = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": st.session_state.search_query,
        "answer": st.session_state.last_answer,
        "results": st.session_state.last_search_results,
        "memory": st.session_state.memory_items[:10],
    }
    add_log(f"Workspace saved: {name}", "success")


def export_markdown_report() -> str:
    lines = [
        f"# Ghildiyal AI Browser Research Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Workspace: {st.session_state.workspace_name}",
        f"Query: {st.session_state.search_query}",
        "",
        "## AI Answer",
        "",
        st.session_state.last_answer or "No answer generated yet.",
        "",
        "## Search Sources",
        "",
    ]
    for idx, result in enumerate(st.session_state.last_search_results, 1):
        lines += [
            f"### {idx}. {result.get('title','No title')}",
            f"- Source: {result.get('source','')}",
            f"- Domain: {result.get('domain','')}",
            f"- Score: {result.get('score','')}",
            f"- URL: {result.get('link','')}",
            f"- Snippet: {result.get('snippet','')}",
            "",
        ]
    if st.session_state.last_compare:
        lines += ["## Comparison", "", st.session_state.last_compare, ""]
    if st.session_state.memory_items:
        lines += ["## Workspace Memory", ""]
        for item in st.session_state.memory_items[:10]:
            lines.append(f"- {item['ts']}: {item['note']}")
    return "\n".join(lines)

# =========================================================
# STYLING
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }
html { scroll-behavior: smooth; }
.stApp {
    background:
        radial-gradient(circle at top left, rgba(139,92,246,0.28), transparent 24%),
        radial-gradient(circle at top right, rgba(59,130,246,0.24), transparent 30%),
        radial-gradient(circle at bottom, rgba(6,182,212,0.16), transparent 32%),
        linear-gradient(135deg, #020617 0%, #000000 38%, #050816 68%, #0f172a 100%);
    background-attachment: fixed;
    color: white;
}
[data-testid="stAppViewContainer"] { background: transparent; }
.main { background: transparent; }
#MainMenu, footer, header { visibility: hidden; }
.grid-bg {
    position: fixed; width: 100%; height: 100%; inset: 0;
    background-image: linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(1000px) rotateX(75deg) scale(2);
    transform-origin: top; opacity: .18; z-index: -3;
    animation: gridmove 18s linear infinite;
}
@keyframes gridmove { 0% { transform: perspective(1000px) rotateX(75deg) translateY(0) scale(2); } 100% { transform: perspective(1000px) rotateX(75deg) translateY(50px) scale(2); } }
.glow { position: fixed; width: 800px; height: 800px; background: radial-gradient(circle, rgba(168,85,247,.22), transparent 70%); filter: blur(140px); z-index: -1; top: -250px; left: -200px; animation: float 12s ease infinite; }
.glow2 { position: fixed; width: 700px; height: 700px; background: radial-gradient(circle, rgba(59,130,246,.18), transparent 70%); filter: blur(140px); z-index: -1; bottom: -250px; right: -200px; animation: float2 14s ease infinite; }
@keyframes float { 0% { transform: translate(0,0); } 50% { transform: translate(120px,80px); } 100% { transform: translate(0,0); } }
@keyframes float2 { 0% { transform: translate(0,0); } 50% { transform: translate(-100px,-60px); } 100% { transform: translate(0,0); } }
.navbar { position: sticky; top: 0; z-index: 999; backdrop-filter: blur(18px); background: rgba(255,255,255,0.055); border: 1px solid rgba(255,255,255,.10); padding: 18px 34px; border-radius: 24px; margin-bottom: 34px; box-shadow: 0 20px 80px rgba(0,0,0,.18); }
.nav-flex { display: flex; justify-content: space-between; align-items: center; gap: 20px; }
.logo { font-size: 32px; font-weight: 900; background: linear-gradient(90deg, #60a5fa, #a855f7, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-links { display: flex; gap: 24px; flex-wrap: wrap; }
.nav-links a { text-decoration: none; color: #d1d5db; transition: .3s; font-weight: 600; }
.nav-links a:hover { color: #60a5fa; }
.hero { padding-top: 72px; padding-bottom: 54px; text-align: center; }
.hero h1 { font-size: 82px; font-weight: 900; line-height: 1.03; background: linear-gradient(90deg, #60a5fa, #a855f7, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 26px; }
.hero p { font-size: 22px; max-width: 980px; margin: auto; line-height: 1.8; color: #b8c1d9; }
.hero-buttons { margin-top: 38px; display: flex; justify-content: center; gap: 18px; flex-wrap: wrap; }
.primary-btn, .secondary-btn { display: inline-block; text-decoration: none; color: white; border-radius: 18px; padding: 16px 34px; transition: .35s; }
.primary-btn { background: linear-gradient(135deg, #2563eb, #a855f7); font-weight: 800; box-shadow: 0 0 35px rgba(99,102,241,.25); }
.primary-btn:hover { transform: translateY(-6px); box-shadow: 0 0 50px rgba(99,102,241,.6); }
.secondary-btn { border: 1px solid rgba(255,255,255,.12); background: rgba(255,255,255,.035); }
.secondary-btn:hover { background: rgba(255,255,255,.07); transform: translateY(-5px); }
.orb { position: relative; width: 270px; height: 270px; margin: 58px auto 28px auto; border-radius: 50%; background: conic-gradient(from 0deg, #60a5fa, #a855f7, #06b6d4, #60a5fa); animation: spin 10s linear infinite, floatOrb 6s ease-in-out infinite; box-shadow: 0 0 60px rgba(96,165,250,.5), 0 0 120px rgba(168,85,247,.35), 0 0 180px rgba(6,182,212,.25); overflow: hidden; }
.orb::before { content: ""; position: absolute; inset: 20px; border-radius: 50%; background: radial-gradient(circle at top, rgba(255,255,255,.35), rgba(255,255,255,.05), transparent 70%); filter: blur(12px); animation: pulse 4s ease infinite; }
@keyframes floatOrb { 0% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-20px) rotate(180deg); } 100% { transform: translateY(0px) rotate(360deg); } }
@keyframes spin { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
@keyframes pulse { 0% { opacity:.6; transform:scale(1); } 50% { opacity:1; transform:scale(1.05); } 100% { opacity:.6; transform:scale(1); } }
.section-title { font-size: 48px; font-weight: 900; text-align: center; margin-top: 80px; margin-bottom: 42px; color: white; }
.glass-card, .feature-card, .sidebar-card, .mini-panel, .answer-card, .source-card { background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.10); backdrop-filter: blur(16px); border-radius: 26px; box-shadow: 0 20px 70px rgba(0,0,0,.16); }
.feature-card { padding: 28px; transition: .35s; min-height: 206px; }
.feature-card:hover { transform: translateY(-8px); box-shadow: 0 0 46px rgba(99,102,241,.35); }
.feature-card h3 { font-size: 24px; margin-bottom: 14px; color: #93c5fd; }
.feature-card p { line-height: 1.8; color: #d1d5db; }
.answer-card { padding: 28px; margin: 16px 0 22px 0; border-left: 4px solid #60a5fa; }
.answer-card h3 { margin-top: 0; color: #bfdbfe; font-size: 26px; }
.source-card { padding: 22px; margin-bottom: 16px; transition: .25s; }
.source-card:hover { transform: translateY(-4px); border-color: rgba(96,165,250,.35); }
.small-kicker { text-transform: uppercase; letter-spacing: .18em; font-size: 12px; color: #94a3b8; margin-bottom: 10px; }
.command-pill { display: inline-block; border: 1px solid rgba(255,255,255,.13); border-radius: 999px; padding: 8px 14px; margin: 4px 6px 4px 0; color: #cbd5e1; font-size: 13px; background: rgba(255,255,255,.05); }
.quality-pill { display: inline-block; border-radius: 999px; padding: 6px 12px; font-size: 12px; font-weight: 800; color: #dbeafe; background: rgba(37,99,235,.22); border: 1px solid rgba(96,165,250,.25); }
.domain-pill { display: inline-block; border-radius: 999px; padding: 6px 12px; font-size: 12px; color: #ccfbf1; background: rgba(20,184,166,.18); border: 1px solid rgba(45,212,191,.18); }
.terminal { background: #020617; border: 1px solid rgba(255,255,255,.08); padding: 28px; border-radius: 24px; margin-top: 22px; font-family: monospace; color: #4ade80; line-height: 2; box-shadow: 0 0 40px rgba(6,182,212,.12); }
.stat-box { background: rgba(255,255,255,.055); padding: 28px; border-radius: 22px; text-align: center; border: 1px solid rgba(255,255,255,.10); min-height: 140px; }
.stat-box h2 { font-size: 42px; color: #60a5fa; margin: 0; }
.stat-box p { color: #d1d5db; }
.browser-window { background: #020617; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255,255,255,.10); box-shadow: 0 0 50px rgba(99,102,241,.26); }
.browser-top { display: flex; gap: 10px; padding: 16px; background: #111827; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.red { background: #ef4444; } .yellow { background: #facc15; } .green { background: #22c55e; }
.browser-content { padding: 30px; font-family: monospace; line-height: 2.1; color: #4ade80; }
.footer { margin-top: 100px; padding: 50px; text-align: center; color: #9ca3af; }
hr { border-color: rgba(255,255,255,.08) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { background: rgba(255,255,255,.055); border-radius: 14px; color: #cbd5e1; padding: 10px 16px; }
@media(max-width: 768px) { .hero h1 { font-size: 48px; } .hero p { font-size: 17px; } .nav-links { display: none; } .section-title { font-size: 36px; } }
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# RENDER HELPERS
# =========================================================

def render_result_card(result: dict, idx: int):
    link = result.get("link", "")
    title = result.get("title", "No Title")
    snippet = result.get("snippet", "")
    domain = result.get("domain") or get_domain(link)
    source = result.get("source", "")
    score = result.get("score", quality_score(result))
    clickable_title = f'<a href="{h(link)}" target="_blank" style="color:#93c5fd;text-decoration:none;">{h(title)}</a>' if link else h(title)
    open_line = f'<div style="margin-top:12px;color:#60a5fa;font-size:14px;word-break:break-all;">{h(short_url(link))}</div>' if link else ""
    st.markdown(
        f"""
        <div class="source-card">
            <div class="small-kicker">{h(source)} • Result {idx}</div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
                <span class="domain-pill">{h(domain or 'local')}</span>
                <span class="quality-pill">Confidence {h(score)}%</span>
            </div>
            <div style="font-size:22px;font-weight:850;line-height:1.35;">{clickable_title}</div>
            <div style="color:#cbd5e1;margin-top:12px;line-height:1.8;">{h(snippet)}</div>
            {open_line}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer(answer: str):
    st.markdown(
        f"""
        <div class="answer-card">
            <h3>🧠 AI Answer from Search</h3>
            <div style="color:#e5e7eb;line-height:1.85;font-size:16px;">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(answer or "No answer generated yet.")
    st.markdown("</div></div>", unsafe_allow_html=True)

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
    st.caption("AI-native browser companion, research engine, source analyzer, and automation console.")

    st.markdown("### Quick Modes")
    mode = st.radio(
        "Choose a mode",
        ["Browse", "Research", "Compare", "Summarize", "Automate", "Memory"],
        index=["Browse", "Research", "Compare", "Summarize", "Automate", "Memory"].index(st.session_state.selected_mode) if st.session_state.selected_mode in ["Browse", "Research", "Compare", "Summarize", "Automate", "Memory"] else 1,
        horizontal=False,
        key="sidebar_mode",
    )
    st.session_state.selected_mode = mode

    st.markdown("### Workspace")
    st.text_input("Workspace name", key="workspace_name")
    save_col, clear_col = st.columns(2)
    with save_col:
        if st.button("Save", use_container_width=True):
            save_current_workspace()
            st.success("Saved")
    with clear_col:
        if st.button("Clear", use_container_width=True):
            st.session_state.last_search_results = []
            st.session_state.last_answer = ""
            st.session_state.last_compare = ""
            st.success("Cleared")

    if st.session_state.saved_workspaces:
        selected_workspace = st.selectbox("Open saved workspace", list(st.session_state.saved_workspaces.keys()))
        if st.button("Load workspace", use_container_width=True):
            data = st.session_state.saved_workspaces[selected_workspace]
            st.session_state.workspace_name = selected_workspace
            st.session_state.search_query = data.get("query", "")
            st.session_state.last_answer = data.get("answer", "")
            st.session_state.last_search_results = data.get("results", [])
            st.session_state.memory_items = data.get("memory", st.session_state.memory_items)
            add_log(f"Loaded workspace: {selected_workspace}", "success")
            st.success("Loaded")

    st.markdown("### Search Intelligence")
    st.selectbox(
        "Source mode",
        ["Balanced", "Official sources only", "Recent / news focused", "Technical docs", "Indian context"],
        key="source_mode",
    )
    st.selectbox(
        "Answer style",
        ["Executive brief", "Detailed research", "Simple explanation", "Action plan", "Pros and cons"],
        key="answer_style",
    )
    st.slider("Number of results", 3, 10, key="result_limit")

    st.markdown("### Privacy Controls")
    st.toggle("Remember context", key="remember_context")
    st.toggle("Use previous notes in answers", key="use_previous_context")

    st.markdown("### Fast Commands")
    for label in ["Search the web", "Compare sources", "Summarize page", "Save memory", "Run agent", "Export report"]:
        st.markdown(f'<span class="command-pill">{h(label)}</span>', unsafe_allow_html=True)

    st.markdown("### Memory Vault")
    memory_note = st.text_area("Save a note", placeholder="Remember this workflow...", height=110)
    if st.button("Save to memory", use_container_width=True):
        add_memory(memory_note)
        add_log("Saved a new memory item.", "success")
        st.success("Saved.")

    st.markdown("### Voice Input (demo)")
    st.text_input("Voice command", key="voice_text")
    if st.button("Interpret voice", use_container_width=True):
        st.info(browser_command(st.session_state.voice_text))
        add_log(f"Voice command interpreted: {st.session_state.voice_text}")

# =========================================================
# NAVBAR + HERO
# =========================================================

st.markdown(
    """
<div class="navbar">
  <div class="nav-flex">
    <div class="logo">🚀 Ghildiyal AI</div>
    <div class="nav-links">
      <a href="#search">AI Search</a>
      <a href="#compare">Compare</a>
      <a href="#workspace">Workspace</a>
      <a href="#radar">Market Radar</a>
      <a href="#agent">Agent</a>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h1>The Future of AI-Native Browsing</h1>
  <p>
    A cinematic browser interface that searches the web, cleans broken links,
    produces answer-first research, compares sources, remembers workspaces,
    and turns browsing goals into visible AI workflows.
  </p>
  <div class="hero-buttons">
    <a class="primary-btn" href="#search">Launch AI Search</a>
    <a class="secondary-btn" href="#radar">View AI Browser Radar</a>
  </div>
  <div class="orb"></div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# TOP CONTROL STRIP
# =========================================================

st.markdown("---")
left, center, right = st.columns([1.1, 1.8, 1.1])

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
    st.markdown("### 🔎 Search + Answer")
    quick_query = st.text_input(
        "Search query",
        value=st.session_state.search_query,
        placeholder="Search anything, for example: top AI browsers, GST e-invoice rules, IRS refund status...",
        label_visibility="collapsed",
        key="top_search_input",
    )
    if st.button("Search web + generate answer", use_container_width=True, key="top_search_button"):
        st.session_state.search_query = quick_query.strip()
        if st.session_state.search_query:
            with st.spinner("Searching, cleaning links, ranking sources, and generating answer..."):
                st.session_state.last_search_results = web_search(
                    st.session_state.search_query,
                    max_results=st.session_state.result_limit,
                    source_mode=st.session_state.source_mode,
                )
                st.session_state.last_answer = build_answer_from_results(
                    st.session_state.search_query,
                    st.session_state.last_search_results,
                    st.session_state.answer_style,
                )
                if st.session_state.remember_context:
                    add_memory(f"Search: {st.session_state.search_query}")
            st.session_state.task_status = "Search answer generated."
            add_log(f"Search run: {st.session_state.search_query}", "success")
            st.success("Done")

with right:
    st.markdown("### 🎛 Live Status")
    st.markdown(
        f"""
        <div class="mini-panel" style="padding:20px;">
            <div class="small-kicker">Mode</div>
            <div style="font-size:22px;font-weight:850;">{h(st.session_state.selected_mode)}</div>
            <div class="small-kicker" style="margin-top:14px;">State</div>
            <div style="font-size:16px;color:#cbd5e1;line-height:1.6;">{h(st.session_state.task_status)}</div>
            <div class="small-kicker" style="margin-top:14px;">Workspace</div>
            <div style="font-size:15px;color:#bfdbfe;">{h(st.session_state.workspace_name)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# MAIN AI SEARCH ENGINE
# =========================================================

st.markdown('<div id="search"></div>', unsafe_allow_html=True)
st.markdown("## 🧠 Answer-First AI Search Engine")

search_tab, answer_tab, compare_tab, export_tab = st.tabs(["🔎 Search", "🧠 Answer", "⚖️ Compare", "📤 Export"])

with search_tab:
    s_col1, s_col2 = st.columns([1.5, 1])
    with s_col1:
        search_term = st.text_input(
            "Search anything",
            value=st.session_state.search_query,
            placeholder="Search like Google, but get an AI answer with clickable sources...",
            key="main_search_term",
        )
    with s_col2:
        st.markdown("#### Search options")
        st.caption(f"Mode: {st.session_state.source_mode} • Style: {st.session_state.answer_style}")

    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        run_search = st.button("Search Web", use_container_width=True, key="main_search_btn")
    with b2:
        run_answer = st.button("Search + AI Answer", use_container_width=True, key="main_answer_btn")
    with b3:
        if st.button("Save Workspace", use_container_width=True, key="save_workspace_main"):
            save_current_workspace()
            st.success("Workspace saved")

    if run_search or run_answer:
        st.session_state.search_query = search_term.strip()
        if not st.session_state.search_query:
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching web and fixing links..."):
                st.session_state.last_search_results = web_search(
                    st.session_state.search_query,
                    max_results=st.session_state.result_limit,
                    source_mode=st.session_state.source_mode,
                )
            if run_answer:
                with st.spinner("Generating source-aware answer..."):
                    st.session_state.last_answer = build_answer_from_results(
                        st.session_state.search_query,
                        st.session_state.last_search_results,
                        st.session_state.answer_style,
                    )
            else:
                st.session_state.last_answer = ""
            if st.session_state.remember_context:
                add_memory(f"Search: {st.session_state.search_query}")
            st.session_state.task_status = "Search completed."
            add_log(f"Search completed: {st.session_state.search_query}", "success")

    if st.session_state.last_answer:
        render_answer(st.session_state.last_answer)

    if st.session_state.last_search_results:
        st.markdown("### Search Results")
        for idx, result in enumerate(st.session_state.last_search_results, 1):
            render_result_card(result, idx)
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                if st.button("Summarize this", key=f"sum_{idx}", use_container_width=True):
                    prompt = f"Summarize this source for the query '{st.session_state.search_query}':\n{json.dumps(result, indent=2)}"
                    st.info(safe_llm_answer(prompt))
            with c2:
                if st.button("Pros / Cons", key=f"pros_{idx}", use_container_width=True):
                    prompt = f"Give pros, cons, usefulness and risk of this source:\n{json.dumps(result, indent=2)}"
                    st.info(safe_llm_answer(prompt))
            with c3:
                if result.get("link"):
                    st.link_button("Open Source", result.get("link"), use_container_width=True)
    else:
        st.info("Run a search to see answer-first results here.")

with answer_tab:
    st.markdown("### AI Answer Panel")
    if st.session_state.last_answer:
        render_answer(st.session_state.last_answer)
    else:
        st.info("No AI answer generated yet. Use Search + AI Answer.")

    st.markdown("### Quick Follow-up")
    quicks = [
        "Make this answer simpler",
        "Give me only action steps",
        "Compare source quality",
        "Find what is missing",
        "Create a professional report",
    ]
    q_cols = st.columns(len(quicks))
    for col, q in zip(q_cols, quicks):
        with col:
            if st.button(q, use_container_width=True, key=f"quick_{q}"):
                if st.session_state.last_answer:
                    prompt = f"Query: {st.session_state.search_query}\nExisting answer:\n{st.session_state.last_answer}\n\nInstruction: {q}"
                    st.session_state.last_answer = safe_llm_answer(prompt)
                    add_log(f"Quick follow-up used: {q}", "success")
                    st.rerun()
                else:
                    st.warning("Generate an answer first.")

with compare_tab:
    st.markdown('<div id="compare"></div>', unsafe_allow_html=True)
    st.markdown("### Compare Selected Sources")
    results = st.session_state.last_search_results or []
    if len(results) >= 2:
        options = [f"{i+1}. {r.get('title','No title')}" for i, r in enumerate(results)]
        selected = st.multiselect("Select two or more sources", options, default=options[: min(3, len(options))])
        if st.button("Compare selected sources", use_container_width=True):
            selected_results = []
            for label in selected:
                idx = int(label.split(".", 1)[0]) - 1
                selected_results.append(results[idx])
            with st.spinner("Comparing selected sources..."):
                st.session_state.last_compare = compare_results(st.session_state.search_query, selected_results)
            add_log("Source comparison generated.", "success")
        if st.session_state.last_compare:
            st.markdown(st.session_state.last_compare)
    else:
        st.info("Run a search first. At least two results are needed for compare mode.")

with export_tab:
    st.markdown('<div id="workspace"></div>', unsafe_allow_html=True)
    st.markdown("### Export Current Research")
    report = export_markdown_report()
    st.download_button(
        "Download Markdown Report",
        data=report.encode("utf-8"),
        file_name=f"ghildiyal_ai_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.text_area("Report preview", value=report, height=360)

# =========================================================
# LAUNCH / BROWSER URL INTELLIGENCE
# =========================================================

st.markdown("---")
st.markdown('<div id="agent"></div>', unsafe_allow_html=True)
st.markdown("## 🚀 AI Browser Workspace")

workspace_col1, workspace_col2 = st.columns([1.05, 1])

with workspace_col1:
    st.markdown("### Browser URL Analyzer")
    st.session_state.browser_url = st.text_input(
        "URL",
        value=st.session_state.browser_url,
        placeholder="https://example.com",
        key="browser_url_input",
    )
    url_action1, url_action2 = st.columns(2)
    with url_action1:
        inspect = st.button("Fetch page info", use_container_width=True)
    with url_action2:
        summarize_url = st.button("Fetch + summarize", use_container_width=True)

    if inspect or summarize_url:
        if st.session_state.browser_url.startswith(("http://", "https://")) or st.session_state.browser_url.startswith("www."):
            with st.spinner("Inspecting page..."):
                info = fetch_url_info(st.session_state.browser_url)
            if info["error"]:
                st.warning(info["error"])
            else:
                st.success(info["title"])
                if summarize_url:
                    summary = safe_llm_answer(
                        f"Summarize this webpage for a browser user. Title: {info['title']}\nContent:\n{info['content'][:5000]}"
                    )
                    st.markdown(summary)
                else:
                    st.code(info["content"][:1800])
                add_log(f"Analyzed URL: {st.session_state.browser_url}", "success")
        else:
            st.error("Use a valid URL starting with http://, https://, or www.")

    st.markdown("### Upload a file for AI reading")
    upload = st.file_uploader("Upload PDF / text / image", type=None)
    if upload is not None:
        st.session_state.file_notes = f"Uploaded: {upload.name} ({upload.type})"
        add_log(f"File uploaded: {upload.name}")
        st.success(st.session_state.file_notes)
        try:
            raw = upload.read()
            if upload.type and "text" in upload.type:
                text = raw.decode("utf-8", errors="ignore")[:6000]
                st.text_area("File preview", text, height=200)
                if st.button("Summarize uploaded text", use_container_width=True):
                    st.markdown(safe_llm_answer("Summarize this uploaded file:\n" + text))
        except Exception as e:
            st.warning(f"Could not preview file: {e}")

with workspace_col2:
    st.markdown("### Holographic Browser Matrix")
    st.markdown(
        f"""
        <div class="browser-window">
            <div class="browser-top"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
            <div class="browser-content">
                <p>> Workspace: {h(st.session_state.workspace_name)}</p>
                <p>> Mode: {h(st.session_state.selected_mode)}</p>
                <p>> Results cached: {len(st.session_state.last_search_results)}</p>
                <p>> AI answer: {'Ready' if st.session_state.last_answer else 'Not generated'}</p>
                <p>> Link cleaner: Active</p>
                <p>> Source confidence: Active</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Autonomous Agent Plan")
    agent_goal = st.text_area(
        "Describe an autonomous browser task",
        placeholder="Example: Research top AI browsers, compare them, and prepare a launch plan.",
        height=130,
    )
    if st.button("Run autonomous agent", use_container_width=True):
        if agent_goal.strip():
            with st.spinner("Creating inspectable agent plan..."):
                result = build_agent_plan(agent_goal.strip())
            st.markdown(result)
            add_log("Autonomous agent plan created.", "success")
        else:
            st.warning("Describe an agent task first.")

# =========================================================
# MULTI-TAB REASONING
# =========================================================

st.markdown("---")
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
        progress = st.progress(0)
        for i, u in enumerate(urls[:5]):
            fetched = fetch_url_info(u)
            snippet = fetched["content"][:1000] if fetched["content"] else ""
            combined.append({"url": normalize_result_link(u), "title": fetched["title"], "snippet": snippet, "error": fetched["error"]})
            progress.progress((i + 1) / min(len(urls), 5))
        prompt = "Summarize these tabs and compare them:\n" + json.dumps(combined, indent=2)
        summary = safe_llm_answer(prompt)
        st.markdown(summary)
        add_log("Tabs summarized.", "success")
    else:
        st.warning("Paste at least one URL.")

# =========================================================
# AI BROWSER MARKET RADAR
# =========================================================

st.markdown("---")
st.markdown('<div id="radar"></div>', unsafe_allow_html=True)
st.markdown("## 🔬 AI Browser Market Radar")
st.caption("Built from the research ideas: answer-first search, context, privacy, workspaces, compare mode, and agentic automation.")

r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown('<div class="stat-box"><h2>50</h2><p>Browsers / AI layers scanned</p></div>', unsafe_allow_html=True)
with r2:
    st.markdown('<div class="stat-box"><h2>10</h2><p>Unique features added</p></div>', unsafe_allow_html=True)
with r3:
    st.markdown('<div class="stat-box"><h2>AI</h2><p>Answer-first search</p></div>', unsafe_allow_html=True)
with r4:
    st.markdown('<div class="stat-box"><h2>Safe</h2><p>Privacy controls</p></div>', unsafe_allow_html=True)

feature_cols = st.columns(5)
for idx, (title, desc) in enumerate(UNIQUE_FEATURES):
    with feature_cols[idx % 5]:
        st.markdown(
            f"""
            <div class="feature-card">
                <h3>{h(title)}</h3>
                <p>{h(desc)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Competitor Scan")
category_filter = st.selectbox(
    "Filter by class",
    ["All"] + sorted(set(item["class"] for item in AI_BROWSER_LANDSCAPE)),
)
filtered_landscape = AI_BROWSER_LANDSCAPE if category_filter == "All" else [x for x in AI_BROWSER_LANDSCAPE if x["class"] == category_filter]
st.dataframe(filtered_landscape, use_container_width=True, hide_index=True)

st.markdown("### Product Strategy Takeaway")
st.markdown(
    """
<div class="answer-card">
<h3>What makes this app more unique now?</h3>
<div style="color:#e5e7eb;line-height:1.85;">
Most AI browser clones only add a chatbot. This version adds a full research workflow:
answer-first search, clean clickable links, source confidence, compare mode, workspace memory,
privacy switches, URL intelligence, report export, and visible agent planning. That makes the app feel
closer to an AI-native browser workspace rather than a normal landing page.
</div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DEMO / WORKFLOW SIMULATION
# =========================================================

st.markdown("---")
st.markdown("## 🎥 Live AI Workflow Simulation")
steps = fake_status_steps()
progress_speed = st.slider("Simulation speed", 1, 10, 4)
if st.button("Run workflow simulation", use_container_width=True):
    progress_bar = st.progress(0)
    status_box = st.empty()
    for i, step in enumerate(steps):
        st.session_state.task_status = step
        st.session_state.demo_progress = int((i + 1) / len(steps) * 100)
        add_log(step)
        status_box.markdown(f"### {step}")
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(max(0.03, 0.12 - progress_speed * 0.007))
    st.success("Workflow simulation completed.")

st.markdown(
    "<div class='terminal'>" + "".join([f"> {h(step)}<br>" for step in steps]) + "</div>",
    unsafe_allow_html=True,
)

# =========================================================
# AI CHAT
# =========================================================

st.markdown("---")
st.markdown("## 💬 AI Browser Chat")
chat_col1, chat_col2 = st.columns([1, 1])

with chat_col1:
    chat_prompt = st.text_area(
        "Message",
        value=st.session_state.quick_prompt,
        placeholder="Summarize this site, compare two products, or plan a workflow...",
        height=120,
    )
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        if st.button("Send to AI", use_container_width=True):
            if chat_prompt.strip():
                st.session_state.chat_history.append({"role": "user", "content": chat_prompt.strip()})
                context = ""
                if st.session_state.last_search_results:
                    context = "\nRecent search results:\n" + json.dumps(st.session_state.last_search_results[:5], indent=2)
                reply = safe_llm_answer(chat_prompt.strip() + context)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                add_log("AI chat response generated.", "success")
    with c2:
        if st.button("Save msg", use_container_width=True):
            if chat_prompt.strip():
                add_memory(chat_prompt.strip())
                st.success("Saved.")

with chat_col2:
    st.markdown("### Conversation")
    for msg in st.session_state.chat_history[-8:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")

# =========================================================
# MEMORY + LOGS
# =========================================================

st.markdown("---")
st.markdown("## 🗂 Workspace Memory & Activity")
mem_col, log_col = st.columns(2)

with mem_col:
    st.markdown("### Memory Vault")
    if st.session_state.memory_items:
        for item in st.session_state.memory_items[:12]:
            st.markdown(
                f"""
                <div class="source-card">
                    <div class="small-kicker">{h(item['ts'])}</div>
                    <div style="color:#e2e8f0;line-height:1.7;">{h(item['note'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No memory saved yet.")

with log_col:
    st.markdown("### Activity Log")
    if st.session_state.workflow_log:
        for entry in st.session_state.workflow_log[:14]:
            st.code(entry)
    else:
        st.caption("No activity yet.")

# =========================================================
# FAQ / ROADMAP
# =========================================================

st.markdown("---")
st.markdown("## 💎 Product Roadmap")
roadmap_cols = st.columns(3)
roadmap = [
    ("Starter", "Answer-first search, clickable sources, memory vault, and URL summaries."),
    ("Pro", "Compare mode, report export, quality scoring, workspace sessions, and agent plans."),
    ("Studio", "Team workspaces, approvals, custom connectors, browser automation, and BYO model."),
]
for col, (title, desc) in zip(roadmap_cols, roadmap):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{h(title)}</h3>
            <p>{h(desc)}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("## ❓ Frequently Asked Questions")
faq = {
    "Will search links be clickable?": "Yes. DuckDuckGo redirect links are normalized into real URLs before rendering.",
    "Will I get an AI answer when searching?": "Yes. Use Search + AI Answer. Add OPENAI_API_KEY for live model answers; otherwise demo mode appears.",
    "Can I export a report?": "Yes. The Export tab downloads the current research as Markdown.",
    "Can this become a real browser?": "This is a Streamlit web interface. Real browser control can be added using Playwright, Browserbase, or extension-based architecture.",
}
for q, a in faq.items():
    with st.expander(q):
        st.write(a)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
  <h2 style="color:white;">🚀 Ghildiyal AI Browser</h2>
  <p>AI-native autonomous browsing platform</p>
  <br>
  <p>Answer-first Search • Source Confidence • Compare Mode • Workspaces • Agent Plans • Export</p>
  <br>
  <p>© 2026 Ghildiyal AI. All rights reserved.</p>
  <p style="margin-top:10px;font-size:14px;color:#60a5fa;">Made by Adhyayan Ghildiyal</p>
</div>
""",
    unsafe_allow_html=True,
)
