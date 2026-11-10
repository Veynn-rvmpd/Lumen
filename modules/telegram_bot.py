"""
Telegram Remote Command & Telemetry Bot.
Handles executive commands, system inspections, financial calculations,
and voice command dispatches via Telegram Bot API with zero emoji output.
"""

import os
import re
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ALLOWED_USER_ID = os.getenv("TELEGRAM_ALLOWED_USER_ID", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}" if TELEGRAM_BOT_TOKEN else ""


def strip_emojis(rawText: str) -> str:
    """
    Guarantees strict prohibition of emojis in Telegram outgoing messages.
    """
    emojiPattern = re.compile(
        r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\ufe0f\u200d]",
        flags=re.UNICODE
    )
    cleaned = emojiPattern.sub("", rawText)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def send_telegram_message(chatId: str, textContent: str) -> Dict[str, Any]:
    """
    Transmits clean text message to a specific Telegram chat destination.
    """
    cleanText = strip_emojis(textContent)

    if not TELEGRAM_BOT_TOKEN:
        print(f"[TELEGRAM LOCAL LOG] Chat: {chatId} | Message: {cleanText}")
        return {
            "status": "[OK]",
            "mode": "simulation",
            "chatId": chatId,
            "message": cleanText
        }

    try:
        endpoint = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            "chat_id": chatId,
            "text": cleanText,
            "parse_mode": "Markdown"
        }
        resp = requests.post(endpoint, json=payload, timeout=5.0)
        return {
            "status": "[OK]" if resp.status_code == 200 else "[ERROR]",
            "statusCode": resp.status_code,
            "chatId": chatId
        }
    except requests.RequestException as networkErr:
        return {"status": "[ERROR]", "error": str(networkErr)}


def handle_incoming_command(commandText: str, senderId: str = "local_user") -> str:
    """
    Parses and dispatches inbound text commands to appropriate LUMEN core engines.
    """
    normalized = commandText.strip()
    tokens = normalized.split()
    primaryCommand = tokens[0].lower() if tokens else "/help"

    if primaryCommand in ["/start", "/help"]:
        return (
            "[READY] LUMEN COMMAND INTERFACE:\n"
            "/status - System health and telemetry\n"
            "/finance <initial> <monthly> <rate> <years> - Investment projection\n"
            "/focus <focus|dev|meeting> - Switch environment mode\n"
            "/tasks - List active priority tasks\n"
            "/system - Hardware resource metrics"
        )

    if primaryCommand == "/status":
        from modules import system_monitor
        metrics = system_monitor.collect_system_telemetry()
        return (
            f"[STATUS REPORT]\n"
            f"Host: {metrics['hostName']}\n"
            f"OS: {metrics['platform']}\n"
            f"CPU Usage: {metrics['cpuPercent']}%\n"
            f"Memory Used: {metrics['memoryPercent']}%\n"
            f"Disk Used: {metrics['diskPercent']}%\n"
            f"Uptime: {metrics['uptimeHours']} hours"
        )

    if primaryCommand == "/finance":
        from modules import personal_finance_hub
        try:
            initial = float(tokens[1]) if len(tokens) > 1 else 10000.0
            monthly = float(tokens[2]) if len(tokens) > 2 else 500.0
            rate = float(tokens[3]) if len(tokens) > 3 else 7.0
            years = int(tokens[4]) if len(tokens) > 4 else 15
            result = personal_finance_hub.calculate_compound_growth(initial, monthly, rate, years)
            return (
                f"[FINANCIAL PROJECTION]\n"
                f"Horizon: {years} years at {rate}%\n"
                f"Total Contributed: {result['totalPrincipalDeposited']:.2f} EUR\n"
                f"Interest Accrued: {result['totalEarnings']:.2f} EUR\n"
                f"Final Portfolio: {result['finalPortfolioValue']:.2f} EUR\n"
                f"Growth Multiple: {result['growthMultiple']}x"
            )
        except (ValueError, IndexError):
            return "[ERROR] Usage: /finance <initialCapital> <monthlyContribution> <annualRate> <years>"

    if primaryCommand == "/focus":
        from modules import process_env_manager
        modeName = tokens[1] if len(tokens) > 1 else "focus"
        result = process_env_manager.activate_environment_profile(modeName)
        return f"[ENVIRONMENT] Profile '{result['activeProfile']}' deployed. Description: {result['profileDetails']['description']}"

    if primaryCommand == "/tasks":
        from modules import calendar_task_manager
        tasks = calendar_task_manager.get_pending_tasks()
        taskList = "\n".join([f"- [{t['priority']}] {t['title']} (Due: {t['dueDate']})" for t in tasks])
        return f"[PENDING ACTION ITEMS]\n{taskList}"

    if primaryCommand == "/system":
        from modules import system_monitor
        return system_monitor.get_executive_summary()

    return f"[ALERT] Unrecognized command '{primaryCommand}'. Send /help for recognized instructions."


def process_voice_note(audioFileBytes: bytes, senderId: str = "remote_operator") -> str:
    """
    Placeholder for automated audio transcription pipeline.
    Directs audio buffer through speech transcription service and returns actionable text.
    """
    simulatedTranscript = "/status"
    return handle_incoming_command(simulatedTranscript, senderId)
