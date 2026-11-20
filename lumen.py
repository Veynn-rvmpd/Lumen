"""
LUMEN-CORE (Lightweight Universal Multimedia & Executive Network)
Primary System Orchestrator & Asynchronous Executive Loop.
Direct, non-ceremonial coordination of dashboard, telemetry, sentinel routines,
multimedia controllers, and dual messaging listeners.
"""

import os
import sys
import time
import signal
import threading
import argparse
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Base environment configuration
load_dotenv()

# Import core executive modules
from modules import (
    system_monitor,
    process_env_manager,
    spotify_controller,
    steam_launcher,
    personal_finance_hub,
    calendar_task_manager,
    code_tutor_auditor,
    writing_clarity_editor,
    sports_fitness_advisor,
    amazon_cart_assistant,
    review_engine,
    mental_philosophy_advisor,
    productivity_hub,
    file_system_sentinel,
    gmail_cleaner,
    image_editor_helper,
    whatsapp_notifier,
    telegram_bot
)
from dashboard.app import app, append_system_log

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "127.0.0.1")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 5000))

# Flag controlling asynchronous operational loops
SYSTEM_RUNNING = True


def _signal_handler(signalNumber: int, frameObject: Any) -> None:
    """
    Handles SIGINT/SIGTERM to guarantee orderly termination of background loops.
    """
    global SYSTEM_RUNNING
    print(f"\n[HALT] Received termination signal ({signalNumber}). Shutting down LUMEN-CORE...")
    SYSTEM_RUNNING = False
    sys.exit(0)


def start_dashboard_thread(hostAddress: str, portNumber: int) -> threading.Thread:
    """
    Spawns the Flask web server in a dedicated daemon thread so the main orchestrator
    can maintain non-blocking supervision over background telemetry and bots.
    """
    def _run_server():
        # Suppress noisy default Werkzeug logging in favor of LUMEN executive logs
        import logging
        werkzeugLogger = logging.getLogger("werkzeug")
        werkzeugLogger.setLevel(logging.ERROR)

        print(f"[OK] LUMEN Dashboard listening on http://{hostAddress}:{portNumber}")
        app.run(host=hostAddress, port=portNumber, debug=False, threaded=True, use_reloader=False)

    serverThread = threading.Thread(target=_run_server, daemon=True, name="LumenDashboardServer")
    serverThread.start()
    return serverThread


def execute_background_sentinel_cycle() -> None:
    """
    Periodic background heartbeat inspecting host resource metrics and disk volumes.
    Logs warnings if memory or processor constraints cross operational thresholds.
    """
    telemetry = system_monitor.collect_system_telemetry()

    if telemetry["status"] != "[OK]":
        alertSummary = f"Hardware pressure detected: CPU {telemetry['cpuPercent']}%, RAM {telemetry['memoryPercent']}%."
        print(f"[ALERT] {alertSummary}")
        append_system_log("ALERT", alertSummary)

        # Notify via WhatsApp if critical threshold breached
        if telemetry["cpuPercent"] > 90.0 or telemetry["memoryPercent"] > 92.0:
            whatsapp_notifier.send_priority_alert(
                f"Critical hardware saturation: CPU {telemetry['cpuPercent']}%, RAM {telemetry['memoryPercent']}%.",
                priorityLevel="P1"
            )


def print_startup_banner(hostAddress: str, portNumber: int, initialProfile: str) -> None:
    """
    Outputs sober, zero-emoji textual overview of active subsystems upon initialization.
    """
    separator = "=" * 70
    print(separator)
    print("  LUMEN-CORE | Autonomous Universal Executive Network")
    print(f"  Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Active Profile: {initialProfile}")
    print(f"  Web Interface:  http://{hostAddress}:{portNumber}")
    print(f"  Host Platform:  {sys.platform.upper()} (Python {sys.version.split()[0]})")
    print(separator)
    print("  [READY] Spotify Controller:       Online (Web API / Local Mock)")
    print("  [READY] Steam Launcher:           Online (URI Protocol Engine)")
    print("  [READY] Personal Finance Hub:     Online (Compound & Allocation Models)")
    print("  [READY] Productivity Hub:         Online (Eisenhower & Timeboxing)")
    print("  [READY] Athletic & Odds Advisor:  Online (Implied Probability Engine)")
    print("  [READY] Code & Writing Auditor:   Online (AST Static Analyzer)")
    print("  [READY] Filesystem Sentinel:      Online (Space & Garbage Watcher)")
    print("  [READY] Gmail & Comms Sentinel:   Online (Triage & Unsubscribe Finder)")
    print("  [READY] Remote Notifiers:         Online (WhatsApp & Telegram Bus)")
    print(separator)


def execute_cli_command(commandLine: str) -> bool:
    """
    Interprets interactive terminal operator inputs without stopping background servers.
    Returns False when exit or quit is requested.
    """
    cleanCmd = commandLine.strip()
    if not cleanCmd:
        return True

    tokens = cleanCmd.split()
    verb = tokens[0].lower()

    if verb in ["exit", "quit", "q"]:
        return False

    if verb == "help":
        print("\n[LUMEN OPERATOR COMMANDS]")
        print("  status                               - Sample current hardware telemetry")
        print("  profile <Focus|Dev|Meeting>          - Switch active workspace profile")
        print("  finance <init> <monthly> <rate> <yr> - Calculate compound wealth growth")
        print("  budget <monthlyIncome>               - 50/30/20 Capital budgeting")
        print("  tasks                                - List pending deliverables")
        print("  task add <title>                     - Register priority task")
        print("  scan <directory>                     - Scan directory for large files (>100MB)")
        print("  clean <directory>                    - Purge harmless temporary garbage")
        print("  whatsapp <message>                   - Dispatch P1 WhatsApp priority alert")
        print("  telegram <command>                   - Execute Telegram command (e.g. /status)")
        print("  exit                                 - Orderly system shutdown\n")

    elif verb == "status":
        print(system_monitor.get_executive_summary())

    elif verb == "profile":
        target = tokens[1] if len(tokens) > 1 else "Dev"
        res = process_env_manager.activate_environment_profile(target)
        print(f"[OK] Profile switched to '{res['activeProfile']}'.")

    elif verb == "finance":
        try:
            init = float(tokens[1]) if len(tokens) > 1 else 10000.0
            month = float(tokens[2]) if len(tokens) > 2 else 600.0
            rate = float(tokens[3]) if len(tokens) > 3 else 7.0
            years = int(tokens[4]) if len(tokens) > 4 else 15
            res = personal_finance_hub.calculate_compound_growth(init, month, rate, years)
            print(f"[OK] {years}y @ {rate}%: Final={res['finalPortfolioValue']} EUR (Deposits={res['totalPrincipalDeposited']}, Earnings={res['totalEarnings']}, Multiple={res['growthMultiple']}x)")
        except Exception as e:
            print(f"[ERROR] Invalid finance arguments: {e}")

    elif verb == "budget":
        try:
            inc = float(tokens[1]) if len(tokens) > 1 else 3000.0
            res = personal_finance_hub.calculate_budget_breakdown(inc)
            print(f"[OK] Budget: Needs={res['allocatedNeeds']} EUR, Wants={res['allocatedWants']} EUR, Savings={res['allocatedSavingsInvestment']} EUR")
        except Exception as e:
            print(f"[ERROR] Budget error: {e}")

    elif verb == "tasks":
        pending = calendar_task_manager.get_pending_tasks()
        print(f"[OK] {len(pending)} Pending Items:")
        for t in pending:
            print(f"  - [{t['priority']}] ID:{t['taskId']} {t['title']} (Due: {t['dueDate']})")

    elif verb == "task" and len(tokens) > 2 and tokens[1].lower() == "add":
        title = " ".join(tokens[2:])
        res = calendar_task_manager.add_task(title)
        print(f"[OK] Task added: ID {res['task']['taskId']} '{title}'")

    elif verb == "scan":
        path = tokens[1] if len(tokens) > 1 else os.path.expanduser("~\\Downloads")
        res = file_system_sentinel.scan_large_files(path)
        print(f"[OK] Found {len(res)} large files in '{path}':")
        for f in res[:5]:
            print(f"  - {f['sizeMb']} MB | {f['fileName']}")

    elif verb == "clean":
        path = tokens[1] if len(tokens) > 1 else os.path.expanduser("~\\AppData\\Local\\Temp")
        res = file_system_sentinel.clean_temporary_garbage(path, dryRun=False)
        print(f"[OK] Cleaned {res['filesIdentified']} files, freed {res['freedSpaceKb']} KB.")

    elif verb == "whatsapp":
        msg = " ".join(tokens[1:]) if len(tokens) > 1 else "Operational supervisor ping."
        res = whatsapp_notifier.send_priority_alert(msg, priorityLevel="P1")
        print(f"[OK] WhatsApp dispatch: {res['status']}")

    elif verb == "telegram":
        cmd = tokens[1] if len(tokens) > 1 else "/status"
        res = telegram_bot.handle_incoming_command(cmd)
        print(f"[TELEGRAM OUTPUT]\n{res}")

    else:
        print(f"[NOTICE] Unknown command '{verb}'. Type 'help' for available instructions.")

    return True


def run_orchestrator(hostAddress: str, portNumber: int, requestedProfile: str, enableInteractive: bool = False) -> None:
    """
    Main supervisor loop coordinating all background workers, timers, and listeners.
    """
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Deploy requested environment profile
    process_env_manager.activate_environment_profile(requestedProfile)

    # Launch dashboard daemon
    start_dashboard_thread(hostAddress, portNumber)

    # Display clean executive startup summary
    print_startup_banner(hostAddress, portNumber, requestedProfile)

    append_system_log("OK", f"LUMEN-CORE operational loop started on port {portNumber}.")

    if enableInteractive:
        print("[READY] Interactive CLI prompt active. Type 'help' for command index, 'exit' to terminate.\n")
        while SYSTEM_RUNNING:
            try:
                operatorInput = input("lumen> ")
                keepRunning = execute_cli_command(operatorInput)
                if not keepRunning:
                    break
            except (EOFError, KeyboardInterrupt):
                break
        print("\n[HALT] Interactive session closed. Shutting down LUMEN-CORE.")
        sys.exit(0)
    else:
        # Standard daemon supervisor loop
        while SYSTEM_RUNNING:
            try:
                execute_background_sentinel_cycle()
                time.sleep(10)
            except (KeyboardInterrupt, SystemExit):
                break
            except Exception as loopException:
                print(f"[ERROR] Supervisor loop iteration exception: {loopException}")
                time.sleep(5)


def parse_cli_arguments() -> argparse.Namespace:
    """
    Parses optional operational flags without heavyweight configuration overhead.
    """
    argParser = argparse.ArgumentParser(description="LUMEN-CORE System Orchestrator")
    argParser.add_argument("--host", default=DASHBOARD_HOST, help="Dashboard binding address")
    argParser.add_argument("--port", type=int, default=DASHBOARD_PORT, help="Dashboard binding port")
    argParser.add_argument("--profile", default="Dev", choices=["Focus", "Dev", "Meeting"], help="Initial environment profile")
    argParser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive CLI prompt alongside web dashboard")
    return argParser.parse_args()


if __name__ == "__main__":
    cliArgs = parse_cli_arguments()
    run_orchestrator(
        hostAddress=cliArgs.host,
        portNumber=cliArgs.port,
        requestedProfile=cliArgs.profile,
        enableInteractive=cliArgs.interactive
    )
