"""
Fellou AI Browser - Website Content Summary
Source: fellou.ai
"""

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
        {
            "title": "Automated Complex Web Tasks with One Prompt",
            "detail": "Automatically execute cross-app workflows through natural language descriptions."
        },
        {
            "title": "End-To-End Web Automation",
            "detail": (
                "Browser Use gives the Agentic AI Browser power to automate entire workflows. "
                "From complex data scraping to form filling, it handles every step from a single command."
            )
        },
        {
            "title": "Handles Desktop Files, Zero Effort",
            "detail": (
                "Computer Use transforms Fellou into a true system-level agent. "
                "Grant permission to operate local apps and manage files for a truly agentic workflow."
            )
        },
        {
            "title": "Intervene at Any Step of AI Workflows in Real Time",
            "detail": (
                "Fellou never works in a black box. For every task, it shows you its entire plan, "
                "step by step. You can edit, approve, or step in at any moment."
            )
        },
        {
            "title": "Agentic Memory Learns You, Knows You",
            "detail": (
                "Agentic Memory securely learns from your browser history and notes to understand "
                "your context, allowing instant recall of past information without searching."
            )
        },
        {
            "title": "Automate Multi-Source Research into Traceable Reports",
            "detail": (
                "Fellou automates deep research across the entire internet, including logged-in "
                "accounts on platforms like Reddit, generating personalized and in-depth reports "
                "with verifiable sources."
            )
        },
    ],

    "use_cases": [
        "Data Analytics",
        "Career Growth",
        "Study",
        "Marketing",
        "Daily Life",
        "Productivity",
    ],

    "vs_chat_assistant": {
        "summary": (
            "An AI chat assistant is reactive, only answering questions. "
            "Fellou's agentic AI can automatically run redundant work and "
            "proactively help complete tasks you've forgotten."
        ),
        "differences": {
            "Deep Action": "Independently plans and executes complex web and desktop tasks across multiple apps.",
            "Deep Search": "Automates in-depth research across the entire internet, including logged-in accounts on X, Reddit, or Salesforce.",
            "Dynamic Multitasking": "Runs multiple tasks simultaneously in its back-end workspace while users browse other sites.",
            "Agentic Memory": "Offers proactive, personalized help by connecting browser history and chat context.",
        }
    },

    "user_testimonials": [
        {
            "quote": "Fellou didn't just beat the competition, it crushed them. Most accurate, clearest reports, deepest insights. Easiest to read. And it's 3.1x faster than OpenAI.",
            "user": "Guri Saroy",
            "handle": "@HeyGurisaroy"
        },
        {
            "quote": "Chrome was for browsing. Fellou is for doing it. Manage the Internet so you can manage your life. The future is not the search, it is an exploration of action.",
            "user": "Filipe | IA",
            "handle": "@filicroval"
        },
        {
            "quote": "This is the future of web browsing.",
            "user": "MARLON",
            "handle": "@MarlonNFTs"
        },
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

    "footer_links": {
        "Product": ["Use Cases", "Download"],
        "Framework": ["Eko Documentation", "Github Repo", "Quickstart Guide"],
        "Company": ["Blog", "Join us"],
        "Legal": ["Terms of Service", "Privacy Policy"],
    },

    "social": ["X (Twitter)", "Discord", "YouTube", "GitHub"],

    "mission": "Bring a digital companion to every person, on every device. Empowering humanity with intelligent productivity.",
}


def print_summary():
    print("=" * 60)
    print(f"  {fellou_info['name']} — {fellou_info['tagline']}")
    print("=" * 60)
    print(f"\n{fellou_info['description']}\n")

    print("--- KEY FEATURES ---")
    for i, feature in enumerate(fellou_info["key_features"], 1):
        print(f"\n{i}. {feature['title']}")
        print(f"   {feature['detail']}")

    print("\n--- USE CASES ---")
    print(", ".join(fellou_info["use_cases"]))

    print("\n--- MISSION ---")
    print(fellou_info["mission"])

    print("\n--- CONTACT ---")
    print(f"Website : {fellou_info['website']}")
    print(f"Email   : {fellou_info['contact']}")

    print("\n--- USER TESTIMONIALS ---")
    for t in fellou_info["user_testimonials"]:
        print(f'\n"{t["quote"]}"')
        print(f"  — {t['user']} ({t['handle']})")

    print("\n--- FAQ TOPICS ---")
    for q in fellou_info["faq"]:
        print(f"  • {q}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print_summary()
