"""
LUMEN Executive Web Dashboard Server.
Exposes REST endpoints and a low-latency Server-Sent Events (SSE) telemetry stream
for real-time system monitoring, media control, financial simulations, and module orchestration.
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Ensure parent directory is in Python path for direct module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, jsonify, Response, redirect
from flask_cors import CORS
from dotenv import load_dotenv

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

load_dotenv()

templateFolder = os.path.join(os.path.dirname(__file__), "templates")
staticFolder = os.path.join(os.path.dirname(__file__), "static")

app = Flask(
    __name__,
    template_folder=templateFolder,
    static_folder=staticFolder
)
CORS(app)

# In-memory circular log buffer for dashboard terminal console
SYSTEM_EVENT_LOGS: List[Dict[str, str]] = [
    {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": "[INFO]",
        "message": "LUMEN-CORE executive supervisor initialized."
    },
    {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": "[OK]",
        "message": "Core dispatch bus online. Telemetry stream ready."
    }
]


def append_system_log(level: str, message: str) -> None:
    """
    Appends a timestamped executive event to the internal log buffer.
    """
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": f"[{level.strip('[]')}]",
        "message": message
    }
    SYSTEM_EVENT_LOGS.append(entry)
    if len(SYSTEM_EVENT_LOGS) > 100:
        SYSTEM_EVENT_LOGS.pop(0)


# Primary Dashboard View
@app.route("/")
def index():
    initialTelemetry = system_monitor.collect_system_telemetry()
    currentProfile = process_env_manager.get_current_profile()
    pendingTasks = calendar_task_manager.get_pending_tasks()
    steamGames = steam_launcher.get_installed_games()
    spotifyState = spotify_controller.spotifyControllerInstance.get_playback_status()

    return render_template(
        "index.html",
        telemetry=initialTelemetry,
        profile=currentProfile,
        tasks=pendingTasks,
        steamGames=steamGames,
        spotify=spotifyState
    )


# Telemetry SSE Stream Endpoint
@app.route("/api/stream")
def sse_telemetry_stream():
    """
    Continuous Server-Sent Events stream delivering hardware metrics,
    environment profile state, and real-time event logs every 2 seconds.
    """
    def event_generator():
        while True:
            telemetryPayload = {
                "telemetry": system_monitor.collect_system_telemetry(),
                "profile": process_env_manager.get_current_profile(),
                "spotify": spotify_controller.spotifyControllerInstance.get_playback_status(),
                "timestamp": datetime.now().isoformat(),
                "recentLogs": SYSTEM_EVENT_LOGS[-6:]
            }
            yield f"data: {json.dumps(telemetryPayload)}\n\n"
            time.sleep(2)

    return Response(
        event_generator(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# REST Endpoints: System & Environment
@app.route("/api/telemetry", methods=["GET"])
def get_telemetry():
    return jsonify(system_monitor.collect_system_telemetry())


@app.route("/api/profile", methods=["GET", "POST"])
def handle_profile():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        profileName = payload.get("profile", "Dev")
        switchResult = process_env_manager.activate_environment_profile(profileName)
        append_system_log("INFO", f"Environment profile altered to '{profileName}'.")
        return jsonify(switchResult)
    return jsonify(process_env_manager.get_available_profiles())


# REST Endpoints: Spotify
@app.route("/api/spotify/status", methods=["GET"])
def spotify_status():
    return jsonify(spotify_controller.spotifyControllerInstance.get_playback_status())


@app.route("/api/spotify/control", methods=["POST"])
def control_spotify():
    payload = request.get_json(silent=True) or {}
    action = payload.get("action", "toggle")
    controller = spotify_controller.spotifyControllerInstance

    if action == "toggle":
        res = controller.play_toggle()
    elif action == "next":
        res = controller.next_track()
    elif action == "previous":
        res = controller.previous_track()
    elif action == "volume":
        vol = int(payload.get("volume", 70))
        res = controller.set_volume(vol)
    else:
        res = {"status": "[ERROR]", "message": f"Unknown action {action}"}

    append_system_log("INFO", f"Spotify action dispatched: {action}")
    return jsonify(res)


@app.route("/api/spotify/playlist", methods=["POST"])
def generate_playlist():
    payload = request.get_json(silent=True) or {}
    textCatalog = payload.get("text", "")
    title = payload.get("title", "LUMEN Curated Selection")
    result = spotify_controller.spotifyControllerInstance.generate_playlist_from_text(textCatalog, title)
    append_system_log("OK", f"Playlist compiled: '{title}' ({result['trackCount']} tracks).")
    return jsonify(result)


@app.route("/login/spotify")
def spotify_oauth_redirect():
    clientId = os.getenv("SPOTIFY_CLIENT_ID", "")
    redirectUri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback/spotify")
    if not clientId:
        return jsonify({"status": "[ERROR]", "message": "SPOTIFY_CLIENT_ID not configured in .env"}), 400

    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-modify-public"
    authUrl = (
        f"https://accounts.spotify.com/authorize?response_type=code"
        f"&client_id={clientId}&scope={scope}&redirect_uri={redirectUri}"
    )
    return redirect(authUrl)


@app.route("/callback/spotify")
def spotify_oauth_callback():
    code = request.args.get("code")
    if code:
        append_system_log("OK", "Spotify authorization code received.")
        return redirect("/?spotify=connected")
    return redirect("/?spotify=error")


# REST Endpoints: Steam Launcher
@app.route("/api/steam/games", methods=["GET"])
def list_steam_games():
    return jsonify(steam_launcher.get_installed_games())


@app.route("/api/steam/launch", methods=["POST"])
def launch_steam_title():
    payload = request.get_json(silent=True) or {}
    appId = payload.get("appId")
    if not appId:
        return jsonify({"status": "[ERROR]", "message": "Missing appId"}), 400

    launchResult = steam_launcher.launch_game(int(appId))
    append_system_log("INFO", f"Steam protocol dispatch: AppId {appId}")
    return jsonify(launchResult)


# REST Endpoints: Personal Finance Hub
@app.route("/api/finance/compound", methods=["POST"])
def calculate_compound():
    payload = request.get_json(silent=True) or {}
    initial = float(payload.get("initialCapital", 10000.0))
    monthly = float(payload.get("monthlyContribution", 500.0))
    rate = float(payload.get("annualReturnRate", 7.0))
    years = int(payload.get("years", 15))

    projection = personal_finance_hub.calculate_compound_growth(initial, monthly, rate, years)
    append_system_log("INFO", f"Compound projection computed: {years}y @ {rate}%")
    return jsonify(projection)


@app.route("/api/finance/evaluate", methods=["POST"])
def evaluate_expense():
    payload = request.get_json(silent=True) or {}
    concept = payload.get("concept", "Discretionary Capital Expenditure")
    cost = float(payload.get("cost", 1500.0))
    rate = float(payload.get("benchmarkRate", 7.0))

    evaluation = personal_finance_hub.evaluate_financial_decision(concept, cost, rate)
    return jsonify(evaluation)


@app.route("/api/finance/allocation", methods=["POST"])
def suggest_allocation():
    payload = request.get_json(silent=True) or {}
    risk = payload.get("riskProfile", "moderate")
    horizon = int(payload.get("timeHorizon", 10))

    allocation = personal_finance_hub.suggest_asset_allocation(risk, horizon)
    return jsonify(allocation)


@app.route("/api/finance/budget", methods=["POST"])
def calculate_budget():
    payload = request.get_json(silent=True) or {}
    income = float(payload.get("monthlyNetIncome", 3000.0))
    framework = payload.get("framework", "50_30_20")
    breakdown = personal_finance_hub.calculate_budget_breakdown(income, framework)
    return jsonify(breakdown)


@app.route("/api/finance/emergency", methods=["POST"])
def calculate_emergency():
    payload = request.get_json(silent=True) or {}
    expenses = float(payload.get("monthlyBasicExpenses", 1600.0))
    stability = payload.get("incomeStability", "stable")
    fund = personal_finance_hub.calculate_emergency_fund(expenses, stability)
    return jsonify(fund)


# REST Endpoints: Calendar & Tasks
@app.route("/api/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        title = payload.get("title", "")
        priority = payload.get("priority", "Medium")
        category = payload.get("category", "General")
        dueDate = payload.get("dueDate")

        if not title:
            return jsonify({"status": "[ERROR]", "message": "Task title required"}), 400

        result = calendar_task_manager.add_task(title, priority, dueDate, category)
        append_system_log("OK", f"Task registered: '{title}' [{priority}]")
        return jsonify(result)

    return jsonify(calendar_task_manager.get_pending_tasks())


@app.route("/api/tasks/<int:taskId>/complete", methods=["POST"])
def mark_task_complete(taskId: int):
    result = calendar_task_manager.complete_task(taskId)
    append_system_log("OK", f"Task ID {taskId} marked completed.")
    return jsonify(result)


@app.route("/api/tasks/extract", methods=["POST"])
def extract_tasks():
    payload = request.get_json(silent=True) or {}
    rawNotes = payload.get("notes", "")
    extracted = calendar_task_manager.extract_action_items_from_text(rawNotes)
    return jsonify({"extractedCount": len(extracted), "items": extracted})


# REST Endpoints: Productivity Hub
@app.route("/api/productivity/eisenhower", methods=["POST"])
def calculate_eisenhower():
    payload = request.get_json(silent=True) or {}
    taskList = payload.get("tasks", calendar_task_manager.get_pending_tasks())
    for t in taskList:
        if "urgent" not in t:
            t["urgent"] = t.get("priority") == "High"
        if "important" not in t:
            t["important"] = t.get("priority") in ["High", "Medium"]
    quadrants = productivity_hub.prioritize_tasks_eisenhower(taskList)
    return jsonify(quadrants)


@app.route("/api/productivity/timebox", methods=["POST"])
def calculate_timebox():
    payload = request.get_json(silent=True) or {}
    startHour = int(payload.get("startHour", 8))
    endHour = int(payload.get("endHour", 18))
    focusTask = payload.get("focusTask", "Core Architecture Execution")
    meetings = int(payload.get("meetingBlocks", 2))
    schedule = productivity_hub.generate_timeboxed_schedule(startHour, endHour, focusTask, meetings)
    return jsonify({"schedule": schedule})


@app.route("/api/productivity/matrix", methods=["POST"])
def evaluate_matrix():
    payload = request.get_json(silent=True) or {}
    weights = payload.get("weights", {"impact": 0.40, "feasibility": 0.35, "speed": 0.25})
    candidates = payload.get("candidates", [
        {"name": "Architecture Refactoring", "scores": {"impact": 9, "feasibility": 8, "speed": 6}},
        {"name": "Feature Prototyping", "scores": {"impact": 7, "feasibility": 9, "speed": 9}},
        {"name": "Technical Debt Sweep", "scores": {"impact": 8, "feasibility": 7, "speed": 8}}
    ])
    matrixResult = productivity_hub.evaluate_decision_matrix(weights, candidates)
    return jsonify(matrixResult)


# REST Endpoints: Code Tutor & Writing Clarity
@app.route("/api/code/audit", methods=["POST"])
def audit_code():
    payload = request.get_json(silent=True) or {}
    codeSnippet = payload.get("code", "")
    auditReport = code_tutor_auditor.audit_python_code(codeSnippet)
    append_system_log("INFO", f"Static code audit executed ({auditReport['issuesCount']} issues found).")
    return jsonify(auditReport)


@app.route("/api/editor/audit", methods=["POST"])
def audit_prose():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    auditReport = writing_clarity_editor.audit_text_clarity(text)
    return jsonify(auditReport)


@app.route("/api/editor/refine", methods=["POST"])
def refine_prose():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    refined = writing_clarity_editor.refine_text_executive(text)
    return jsonify(refined)


# REST Endpoints: Fitness & Implied Odds
@app.route("/api/fitness/split", methods=["POST"])
def generate_split():
    payload = request.get_json(silent=True) or {}
    days = int(payload.get("days", 4))
    focus = payload.get("focus", "hypertrophy")
    return jsonify(sports_fitness_advisor.generate_workout_split(days, focus))


@app.route("/api/fitness/odds", methods=["POST"])
def compute_odds():
    payload = request.get_json(silent=True) or {}
    oddsList = payload.get("odds", [1.85, 3.40, 4.20])
    return jsonify(sports_fitness_advisor.calculate_implied_odds_probability(oddsList))


@app.route("/api/fitness/technique", methods=["POST"])
def check_technique():
    payload = request.get_json(silent=True) or {}
    exercise = payload.get("exercise", "Barbell Back Squat")
    return jsonify(sports_fitness_advisor.evaluate_exercise_technique(exercise))


@app.route("/api/fitness/scoreboard", methods=["GET"])
def get_scoreboard():
    return jsonify(sports_fitness_advisor.get_current_scoreboard())


# REST Endpoints: Amazon & Reviews
@app.route("/api/amazon/search", methods=["POST"])
def search_amazon():
    payload = request.get_json(silent=True) or {}
    query = payload.get("query", "Keychron mechanical keyboard")
    marketplace = payload.get("marketplace", "amazon.es")
    results = amazon_cart_assistant.search_amazon_catalog(query, marketplace)
    return jsonify(results)


@app.route("/api/review/product", methods=["POST"])
def review_product():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "Dell UltraSharp 27 4K")
    category = payload.get("category", "Display Hardware")
    price = float(payload.get("price", 520.0))
    return jsonify(review_engine.generate_product_review(name, category, price))


# REST Endpoints: Philosophy & Cognitive Bias
@app.route("/api/philosophy/lens", methods=["POST"])
def apply_lens():
    payload = request.get_json(silent=True) or {}
    problem = payload.get("problem", "Delayed product launch and shifting client demands")
    school = payload.get("school", "stoicism")
    return jsonify(mental_philosophy_advisor.apply_philosophical_lens(problem, school))


@app.route("/api/philosophy/bias", methods=["POST"])
def analyze_bias():
    payload = request.get_json(silent=True) or {}
    scenario = payload.get("scenario", "We spent six months building this module so we must deploy it despite poor initial metrics.")
    return jsonify(mental_philosophy_advisor.analyze_cognitive_bias(scenario))


@app.route("/api/philosophy/practice", methods=["POST"])
def deliberate_practice():
    payload = request.get_json(silent=True) or {}
    skill = payload.get("skill", "Distributed System Profiling")
    return jsonify(mental_philosophy_advisor.generate_deliberate_practice_protocol(skill))


# REST Endpoints: Filesystem Sentinel
@app.route("/api/files/large", methods=["POST"])
def find_large_files():
    payload = request.get_json(silent=True) or {}
    targetDir = payload.get("directory", os.path.expanduser("~\\Downloads"))
    threshold = float(payload.get("thresholdMb", 100.0))
    files = file_system_sentinel.scan_large_files(targetDir, threshold)
    return jsonify({"directory": targetDir, "count": len(files), "largeFiles": files[:20]})


@app.route("/api/files/organize", methods=["POST"])
def organize_files():
    payload = request.get_json(silent=True) or {}
    targetDir = payload.get("directory", os.path.expanduser("~\\Downloads"))
    dryRun = bool(payload.get("dryRun", True))
    result = file_system_sentinel.organize_directory_by_type(targetDir, dryRun)
    append_system_log("INFO", f"Directory organize scan executed on '{targetDir}' (DryRun: {dryRun}).")
    return jsonify(result)


@app.route("/api/files/clean", methods=["POST"])
def clean_garbage():
    payload = request.get_json(silent=True) or {}
    targetDir = payload.get("directory", os.path.expanduser("~\\AppData\\Local\\Temp"))
    dryRun = bool(payload.get("dryRun", True))
    result = file_system_sentinel.clean_temporary_garbage(targetDir, dryRun)
    append_system_log("INFO", f"Temporary garbage scan on '{targetDir}' (Cleaned: {result['filesIdentified']}).")
    return jsonify(result)


# REST Endpoints: Gmail Sentinel
@app.route("/api/gmail/triage", methods=["GET"])
def triage_gmail():
    triageReport = gmail_cleaner.triage_sample_inbox()
    return jsonify(triageReport)


@app.route("/api/gmail/filters", methods=["GET"])
def gmail_filters():
    rules = gmail_cleaner.generate_gmail_filter_rules()
    return jsonify({"rulesCount": len(rules), "filterRules": rules})


@app.route("/api/gmail/unsubscribe", methods=["POST"])
def extract_unsub():
    payload = request.get_json(silent=True) or {}
    bodyText = payload.get("body", "")
    links = gmail_cleaner.extract_unsubscribe_links(bodyText)
    return jsonify({"linksFound": len(links), "unsubscribeUrls": links})


# REST Endpoints: Image Editor Helper
@app.route("/api/image/inspect", methods=["POST"])
def inspect_img():
    payload = request.get_json(silent=True) or {}
    path = payload.get("path", "")
    return jsonify(image_editor_helper.inspect_image(path))


@app.route("/api/image/compress", methods=["POST"])
def compress_img():
    payload = request.get_json(silent=True) or {}
    src = payload.get("sourcePath", "")
    out = payload.get("outputPath", "")
    maxDim = int(payload.get("maxDimension", 1920))
    qual = int(payload.get("quality", 82))
    fmt = payload.get("format", "WEBP")
    return jsonify(image_editor_helper.compress_for_web(src, out, maxDim, qual, fmt))


@app.route("/api/image/watermark", methods=["POST"])
def watermark_img():
    payload = request.get_json(silent=True) or {}
    src = payload.get("sourcePath", "")
    out = payload.get("outputPath", "")
    text = payload.get("text", "CONFIDENTIAL")
    opacity = int(payload.get("opacity", 40))
    pos = payload.get("position", "bottom_right")
    return jsonify(image_editor_helper.add_text_watermark(src, out, text, opacity, pos))


@app.route("/api/image/crop", methods=["POST"])
def crop_img():
    payload = request.get_json(silent=True) or {}
    src = payload.get("sourcePath", "")
    out = payload.get("outputPath", "")
    box = tuple(payload.get("box", [0, 0, 500, 500]))
    return jsonify(image_editor_helper.crop_image(src, out, box))


@app.route("/api/image/convert", methods=["POST"])
def convert_img():
    payload = request.get_json(silent=True) or {}
    src = payload.get("sourcePath", "")
    out = payload.get("outputPath", "")
    targetFmt = payload.get("format", "JPEG")
    return jsonify(image_editor_helper.convert_format(src, out, targetFmt))


# REST Endpoints: Messaging Dispatches
@app.route("/api/notify/whatsapp", methods=["POST"])
def trigger_whatsapp():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "Telemetry threshold test.")
    level = payload.get("priority", "P2")
    res = whatsapp_notifier.send_priority_alert(message, level)
    append_system_log("ALERT", f"WhatsApp alert dispatched: [{level}] {message}")
    return jsonify(res)


@app.route("/api/telegram/command", methods=["POST"])
def trigger_telegram():
    payload = request.get_json(silent=True) or {}
    cmd = payload.get("command", "/status")
    output = telegram_bot.handle_incoming_command(cmd)
    append_system_log("INFO", f"Telegram command evaluated: {cmd}")
    return jsonify({"command": cmd, "response": output})


@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(SYSTEM_EVENT_LOGS)


def run_dashboard_server(host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
    """
    Direct blocking invocation for standalone execution.
    """
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    run_dashboard_server()
