# LUMEN-CORE (Lightweight Universal Multimedia & Executive Network)

Autonomous executive operating assistant, telemetry supervisor, and analytical intelligence platform built in Python. Combines a real-time web dashboard, multimedia controllers (Spotify API text-to-playlist generator, local Steam game protocol launcher), personal finance decision hub, productivity systems, code quality auditor, prose clarity editor, sports analytics, image studio, storage sentinel, and dual remote messaging integration (WhatsApp + Telegram).

---

## 1. System Architecture

```
lumen/
├── lumen.py                         # Primary orchestrator, daemon supervisor & interactive CLI
├── requirements.txt                 # Pinned system dependencies
├── .env.template                    # Environment variables template
├── .gitignore                       # Repository exclusion rules
├── README.md                        # Technical documentation and deployment guide
│
├── dashboard/                       # Executive Real-Time Web Interface
│   ├── app.py                       # Flask server with REST API, OAuth & SSE stream
│   ├── static/
│   │   ├── css/styles.css           # Anti-AI aesthetic (Charcoal #121212, Terracotta #C25E3E)
│   │   └── js/dashboard.js          # Client controller via EventSource & Command Palette (Ctrl+K)
│   └── templates/
│       └── index.html               # Multi-tabbed executive workspace
│
├── modules/                         # Core Subsystems
│   ├── __init__.py
│   ├── spotify_controller.py        # Playback control & text-to-playlist engine
│   ├── steam_launcher.py            # Local Steam game discovery and protocol launcher
│   ├── image_editor_helper.py       # Headless Pillow image processing & WebP compression
│   ├── amazon_cart_assistant.py     # Product search and direct 1-click cart URLs
│   ├── review_engine.py             # Neutral trade-off review and specification analysis
│   ├── sports_fitness_advisor.py    # Training splits & implied odds probability calculator
│   ├── code_tutor_auditor.py        # AST static code inspection & bottleneck detector
│   ├── mental_philosophy_advisor.py # Educational psychology & philosophical decision models
│   ├── personal_finance_hub.py      # Compound growth, asset allocation & opportunity cost
│   ├── productivity_hub.py          # Timeboxing, Eisenhower matrix & decision matrices
│   ├── writing_clarity_editor.py    # Prose clarity, brevity and filler elimination
│   ├── whatsapp_notifier.py         # Priority P1/P2/P3 alert dispatcher (Twilio / Fallback)
│   ├── telegram_bot.py              # Command interpreter and telemetry responder
│   ├── calendar_task_manager.py     # Task queue and action item extractor
│   ├── gmail_cleaner.py             # Inbox triage, unsubscribe finder & filter rules
│   ├── file_system_sentinel.py      # Disk space auditor & automatic file organizer
│   ├── process_env_manager.py       # Workspace profile manager (Focus / Dev / Meeting)
│   └── system_monitor.py            # Host hardware telemetry (psutil)
│
└── tests/                           # Automated Verification Suite
    ├── __init__.py
    └── test_core_modules.py         # Complete unit tests across all 18 modules
```

---

## 2. Core Functional Capabilities

### Personal Finance Hub (`modules/personal_finance_hub.py`)
- `calculate_compound_growth(initialCapital, monthlyContribution, annualReturnRate, years)`: Projects wealth accumulation year-by-year, segregating total deposits from compounded returns.
- `evaluate_financial_decision(expenseOrInvestment, cost, alternativeReturnRate)`: Computes the true opportunity cost of expenditures over 5, 10, 20, and 30-year horizons against index fund benchmarks.
- `suggest_asset_allocation(riskProfile, timeHorizon)`: Recommends portfolio distribution across global equity index ETFs, fixed income bonds, and liquid cash reserves with explicit Total Expense Ratio (TER) guidelines.
- `calculate_budget_breakdown(monthlyNetIncome, framework)`: 50/30/20 capital allocation breakdown for needs, wants, and savings.
- `calculate_emergency_fund(monthlyBasicExpenses, incomeStability)`: Computes recommended liquidity cushion based on employment stability.

### Productivity & Decision Systems (`modules/productivity_hub.py`)
- `prioritize_tasks_eisenhower(taskList)`: Classifies deliverables across Q1 (Do), Q2 (Schedule), Q3 (Delegate), Q4 (Eliminate).
- `generate_timeboxed_schedule(startHour, endHour, focusTask, meetingBlocks)`: Generates structured workday timeblocks isolating deep work from administrative cycles.
- `evaluate_decision_matrix(criteriaWeights, candidates)`: Multi-criteria weighted scoring model for high-stakes trade-offs.

### Multimedia & Steam Launcher
- `spotify_controller.py`: Controls active playback and parses unstructured text lines into structured playlists via Spotify Web API (with deterministic fallback).
- `steam_launcher.py`: Scans Windows Steam installation and library manifests (`.acf`), dispatching instantaneous launches via the `steam://run/<app_id>` protocol.

### Code Quality & Writing Clarity
- `code_tutor_auditor.py`: Runs AST syntax checks, flags bare exceptions, unclosed resource descriptors, and O(N^2) quadratic string concatenations.
- `writing_clarity_editor.py`: Audits prose for passive voice constructions, flags bloated sentences (>25 words), and strips non-essential filler phrases.

### Athletic Analytics & Biomechanics
- `sports_fitness_advisor.py`: Generates periodized training splits (Full Body, Upper/Lower, PPL) with double progression rules, biomechanical cue checklists (Squat, Deadlift, Bench), and calculates bookmaker overround/margins from decimal odds (strictly non-wagering).

### Filesystem Sentinel & Storage Management (`modules/file_system_sentinel.py`)
- `scan_large_files(targetDirectory, thresholdMb)`: Isolates files exceeding specified size threshold.
- `organize_directory_by_type(targetDirectory, dryRun)`: Categorizes messy folders into typed subdirectories (Documents, Images, Media, Archives, Code).
- `clean_temporary_garbage(targetDirectory, dryRun)`: Safe detection and removal of harmless temporary files.

### Image Studio Helper (`modules/image_editor_helper.py`)
- Headless inspection of pixel dimensions, aspect ratio, and color mode.
- Lossy WebP and JPEG compression for web distribution.
- Subtle monochrome text watermark overlay via RGBA buffers.
- Fast format conversions (PNG, JPEG, WEBP, BMP).

### Communications & Inbox Sentinel (`modules/gmail_cleaner.py`)
- Inbox triage digest segregating security alerts, newsletters, and receipts.
- XML filter rule generator for bulk email management.
- Automated extraction of one-click unsubscribe hyperlinks from email bodies.

### System Supervision & Workspace Profiles
- `system_monitor.py`: Non-blocking hardware metrics (CPU, RAM, Disk array, Network I/O, process count, uptime).
- `process_env_manager.py`: Activates workspace profiles (`Focus`, `Dev`, `Meeting`), configuring OS notifications, telemetry polling rates, and background audio contexts.

---

## 3. Setup & Installation

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

## 4. Execution

### Start Primary Orchestrator & Dashboard
```bash
py lumen.py
```

### Start with Interactive CLI Prompt
```bash
py lumen.py -i
```
Allows executing direct commands (`status`, `profile Focus`, `finance 10000 600 7 15`, `tasks`, `scan C:\Users\Public\Downloads`) directly inside the terminal while the web server runs.

Optional CLI parameters:
```bash
py lumen.py --host 127.0.0.1 --port 5000 --profile Dev
```

Access the web interface at `http://127.0.0.1:5000`.

---

## 5. Running Automated Tests

Run the full verification suite covering all modules:
```bash
py -m unittest tests/test_core_modules.py
```

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
