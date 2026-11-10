"""
Executive Calendar, Action Item & Agenda Manager.
Maintains schedule entries, tracks priority deliverables, and extracts
actionable commitments from unstructured notes or communications.
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime, date, timedelta


IN_MEMORY_TASKS: List[Dict[str, Any]] = [
    {
        "taskId": 1,
        "title": "Complete Q4 Portfolio Rebalancing and Tax-Loss Review",
        "priority": "High",
        "dueDate": (date.today() + timedelta(days=2)).isoformat(),
        "status": "In Progress",
        "category": "Finance"
    },
    {
        "taskId": 2,
        "title": "Review Distributed Service Telemetry Latency Benchmarks",
        "priority": "High",
        "dueDate": (date.today() + timedelta(days=1)).isoformat(),
        "status": "Pending",
        "category": "Engineering"
    },
    {
        "taskId": 3,
        "title": "Audit Physical Storage Drive Space & Archive Old Logs",
        "priority": "Medium",
        "dueDate": (date.today() + timedelta(days=5)).isoformat(),
        "status": "Pending",
        "category": "Operations"
    }
]


def get_pending_tasks(categoryFilter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns uncompleted tasks, optionally filtered by category.
    """
    activeTasks = [task for task in IN_MEMORY_TASKS if task["status"] != "Completed"]
    if categoryFilter:
        return [t for t in activeTasks if t["category"].lower() == categoryFilter.lower()]
    return activeTasks


def add_task(
    title: str,
    priority: str = "Medium",
    dueDate: Optional[str] = None,
    category: str = "General"
) -> Dict[str, Any]:
    """
    Inserts a new structured task into the agenda queue.
    """
    assignedId = max([t["taskId"] for t in IN_MEMORY_TASKS], default=0) + 1
    newTask = {
        "taskId": assignedId,
        "title": title.strip(),
        "priority": priority if priority in ["High", "Medium", "Low"] else "Medium",
        "dueDate": dueDate or (date.today() + timedelta(days=3)).isoformat(),
        "status": "Pending",
        "category": category.strip()
    }
    IN_MEMORY_TASKS.append(newTask)
    return {"status": "[OK]", "task": newTask}


def complete_task(taskId: int) -> Dict[str, Any]:
    """
    Marks the specified task ID as completed.
    """
    for taskItem in IN_MEMORY_TASKS:
        if taskItem["taskId"] == taskId:
            taskItem["status"] = "Completed"
            return {"status": "[OK]", "taskId": taskId, "title": taskItem["title"]}
    return {"status": "[ERROR]", "message": f"Task ID {taskId} not found."}


def extract_action_items_from_text(rawNotes: str) -> List[Dict[str, Any]]:
    """
    Scans unstructured meeting transcripts or notes for action verbs and commitments
    (e.g., 'need to', 'must', 'TODO', 'schedule', 'review', 'debe', 'hay que').
    """
    actionIndicators = [
        r'\b(?:todo|action item|task):\s*(.*)',
        r'\b(?:need to|must|have to)\s+([^.!?]+)',
        r'\b(?:hay que|debe|debemos|tarea:)\s+([^.!?]+)',
        r'\b(?:schedule|review|deploy|finalize)\s+([^.!?]+)'
    ]

    extractedItems: List[Dict[str, Any]] = []
    lines = rawNotes.splitlines()

    for lineIndex, line in enumerate(lines):
        cleanLine = line.strip()
        for pattern in actionIndicators:
            match = re.search(pattern, cleanLine, re.IGNORECASE)
            if match:
                actionText = match.group(1).strip()
                extractedItems.append({
                    "lineIndex": lineIndex + 1,
                    "extractedItem": actionText,
                    "priority": "High" if any(w in actionText.lower() for w in ["urgent", "asap", "critico"]) else "Medium",
                    "inferredCategory": "Operations"
                })
                break

    return extractedItems


def get_daily_agenda_overview() -> Dict[str, Any]:
    """
    Produces an executive view of today's schedule and imminent deadlines.
    """
    todayIso = date.today().isoformat()
    dueToday = [t for t in IN_MEMORY_TASKS if t["dueDate"] == todayIso and t["status"] != "Completed"]

    return {
        "currentDate": todayIso,
        "tasksDueToday": len(dueToday),
        "totalPending": len(get_pending_tasks()),
        "dueTodayItems": dueToday,
        "status": "[READY]"
    }
