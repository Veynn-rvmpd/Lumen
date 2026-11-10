# LUMEN-CORE (Lightweight Universal Multimedia & Executive Network)

Autonomous executive operating assistant, telemetry supervisor, and analytical intelligence platform built in Python. Combines a real-time web dashboard, multimedia controllers (Spotify API text-to-playlist generator, local Steam game protocol launcher), personal finance decision hub, code quality auditor, prose clarity editor, sports analytics, and dual remote messaging integration (WhatsApp + Telegram).

---

## 1. System Architecture

```
lumen/
├── lumen.py                         # Primary orchestrator and supervisor loop
├── requirements.txt                 # Pinned system dependencies
├── .env.template                    # Environment variables template
├── .gitignore                       # Repository exclusion rules
├── README.md                        # Technical documentation and deployment guide
│
├── dashboard/                       # Executive Real-Time Web Interface
│   ├── app.py                       # Flask server with REST API and SSE stream
│   ├── static/
│   │   ├── css/styles.css           # Anti-AI aesthetic (Charcoal #121212, Terracotta #C25E3E)
│   │   └── js/dashboard.js          # Real-time client controller via EventSource
│   └── templates/
│       └── index.html               # Clean, responsive workspace layout
│
└── modules/                         # Core Subsystems
    ├── __init__.py
    ├── spotify_controller.py        # Playback control & text-to-playlist engine
    ├── steam_launcher.py            # Local Steam game discovery and protocol launcher
    ├── image_editor_helper.py       # Headless Pillow image processing & WebP compression
    ├── amazon_cart_assistant.py     # Product search and direct 1-click cart URLs
    ├── review_engine.py             # Neutral trade-off review and specification analysis
    ├── sports_fitness_advisor.py    # Training splits & implied odds probability calculator
    ├── code_tutor_auditor.py        # AST static code inspection & bottleneck detector
    ├── mental_philosophy_advisor.py # Educational psychology & philosophical decision models
    ├── personal_finance_hub.py      # Compound growth, asset allocation & opportunity cost
    ├── productivity_hub.py          # Timeboxing, Eisenhower matrix & decision matrices
    ├── writing_clarity_editor.py    # Prose clarity, brevity and filler elimination
    ├── whatsapp_notifier.py         # Priority P1/P2/P3 alert dispatcher (Twilio / Fallback)
    ├── telegram_bot.py              # Command interpreter and telemetry responder
    ├── calendar_task_manager.py     # Task queue and action item extractor
    ├── gmail_cleaner.py             # Inbox triage, unsubscribe finder & filter rules
    ├── file_system_sentinel.py      # Disk space auditor & automatic file organizer
    ├── process_env_manager.py       # Workspace profile manager (Focus / Dev / Meeting)
    └── system_monitor.py            # Host hardware telemetry (psutil)
```

---

## 2. Design Principles & Anti-AI Aesthetic

- Zero Emojis: Absolute prohibition of emoji pictographs across code, logs, user interfaces, and messaging alerts. Sober status tokens (`[OK]`, `[INFO]`, `[ALERT]`, `[READY]`) and 6px monochrome CSS dots are used instead.
- Color Palette: Zinc and charcoal background (`#121212`), high-contrast off-white typography (`#EDEDED`), razor-sharp borders (`#27272A`), and a single matte terracotta accent (`#C25E3E`).
- Typography: Clean system sans-serif font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`) with monospace tabular numbers.
- Pragmatic Codebase: Clear, readable functions with real domain variable names (`portfolioYield`, `matchScore`, `weeklyPlan`). No tutorial-style boilerplate or unnecessary design patterns.

---

## 3. Core Functional Capabilities

### Personal Finance Hub (`modules/personal_finance_hub.py`)
- `calculate_compound_growth(initialCapital, monthlyContribution, annualReturnRate, years)`: Proyects wealth accumulation year-by-year, segregating total deposits from compounded returns.
- `evaluate_financial_decision(expenseOrInvestment, cost, alternativeReturnRate)`: Computes the true opportunity cost of expenditures over 5, 10, 20, and 30-year horizons against index fund benchmarks.
- `suggest_asset_allocation(riskProfile, timeHorizon)`: Recommends portfolio distribution across global equity index ETFs, fixed income bonds, and liquid cash reserves with explicit Total Expense Ratio (TER) guidelines.

### Multimedia & Steam Launcher
- `spotify_controller.py`: Controls active playback and parses unstructured text lines into structured playlists via Spotify Web API (with deterministic fallback).
- `steam_launcher.py`: Scans Windows Steam installation and library manifests (`.acf`), dispatching instantaneous launches via the `steam://run/<app_id>` protocol.

### Code Quality & Writing Clarity
- `code_tutor_auditor.py`: Runs AST syntax checks, flags bare exceptions, unclosed resource descriptors, and O(N^2) quadratic string concatenations.
- `writing_clarity_editor.py`: Audits prose for passive voice constructions, flags bloated sentences (>25 words), and strips non-essential filler phrases.

### Athletic Analytics & Probability
- `sports_fitness_advisor.py`: Generates periodized training splits (Full Body, Upper/Lower, PPL) with double progression rules and calculates bookmaker overround/margins from decimal odds (strictly non-wagering).

### System Supervision & Workspace Profiles
- `system_monitor.py`: Non-blocking hardware metrics (CPU, RAM, Disk array, Network I/O, process count, uptime).
- `process_env_manager.py`: Activates workspace profiles (`Focus`, `Dev`, `Meeting`), configuring OS notifications, telemetry polling rates, and background audio contexts.

---

## 4. Setup & Installation

### Requirements
- Python 3.10+ (Tested on Python 3.14 / 3.15)
- Windows 10/11 or modern Linux/macOS host

### Dependency Installation
```bash
py -m pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.template` to `.env` and populate any third-party credentials:
```bash
cp .env.template .env
```

---

## 5. Execution

### Start Primary Orchestrator & Dashboard
```bash
py lumen.py
```

Optional CLI parameters:
```bash
py lumen.py --host 127.0.0.1 --port 5000 --profile Dev
```

Access the web interface at `http://127.0.0.1:5000`.

---

## 6. Remote Messaging Configuration

### WhatsApp Priority Notifier
Configure Twilio credentials in `.env` to enable priority P1/P2 WhatsApp alerts:
```ini
WHATSAPP_PROVIDER=twilio
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
WHATSAPP_RECIPIENT_NUMBER=+34600000000
```
When credentials are not supplied, the system automatically falls back to local console logging without interrupting execution.

### Telegram Remote Bot
Configure a bot token from `@BotFather` in `.env`:
```ini
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
```
Supported remote commands:
- `/status` - Hardware telemetry and host load
- `/finance <initial> <monthly> <rate> <years>` - Compound growth simulation
- `/focus <profile>` - Activate Focus, Dev, or Meeting environment
- `/tasks` - Display uncompleted action items
- `/system` - Host executive summary

---

## 7. License & Compliance
Proprietary executive software. All rights reserved.
