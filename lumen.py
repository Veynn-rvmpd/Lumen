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
    file_system_sentinel,
    gmail_cleaner,
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
    print("  [READY] Athletic & Odds Advisor:  Online (Implied Probability Engine)")
    print("  [READY] Code & Writing Auditor:   Online (AST Static Analyzer)")
    print("  [READY] Filesystem Sentinel:      Online (Space & Garbage Watcher)")
    print("  [READY] Remote Notifiers:         Online (WhatsApp & Telegram Bus)")
    print(separator)


def run_orchestrator(hostAddress: str, portNumber: int, requestedProfile: str) -> None:
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

    # Main supervision loop running every 10 seconds
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
    return argParser.parse_args()


if __name__ == "__main__":
    cliArgs = parse_cli_arguments()
    run_orchestrator(
        hostAddress=cliArgs.host,
        portNumber=cliArgs.port,
        requestedProfile=cliArgs.profile
    )
