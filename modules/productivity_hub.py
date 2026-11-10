"""
Productivity Engineering, Timeboxing & Decision Matrix Hub.
Provides deterministic routines for task prioritization, timeblocking schedules,
and weighted multi-criteria decision matrices.
"""

from typing import Dict, List, Any


def prioritize_tasks_eisenhower(
    taskList: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Sorts tasks into Eisenhower Matrix quadrants:
    Q1: Urgent & Important (Execute immediately)
    Q2: Not Urgent but Important (Schedule deep work)
    Q3: Urgent but Not Important (Delegate or automate)
    Q4: Neither (Eliminate or defer)
    """
    quadrants: Dict[str, List[Dict[str, Any]]] = {
        "Q1_DoImmediately": [],
        "Q2_ScheduleDeepWork": [],
        "Q3_DelegateOrAutomate": [],
        "Q4_Eliminate": []
    }

    for taskItem in taskList:
        isUrgent = bool(taskItem.get("urgent", False))
        isImportant = bool(taskItem.get("important", False))

        if isUrgent and isImportant:
            quadrants["Q1_DoImmediately"].append(taskItem)
        elif not isUrgent and isImportant:
            quadrants["Q2_ScheduleDeepWork"].append(taskItem)
        elif isUrgent and not isImportant:
            quadrants["Q3_DelegateOrAutomate"].append(taskItem)
        else:
            quadrants["Q4_Eliminate"].append(taskItem)

    return quadrants


def generate_timeboxed_schedule(
    startHour: int = 8,
    endHour: int = 18,
    focusTask: str = "Deep Engineering & Architecture",
    meetingBlocks: int = 2
) -> List[Dict[str, Any]]:
    """
    Generates an uninterrupted timeboxed day dividing deep work blocks,
    admin batches, and physiological recovery windows.
    """
    schedule: List[Dict[str, Any]] = []
    currentHour = startHour

    # Morning high-cognitive block
    schedule.append({
        "timeRange": f"{currentHour:02d}:00 - {currentHour+3:02d}:00",
        "blockType": "Deep Work",
        "activity": focusTask,
        "protocol": "Zero notifications, single task focus, full screen environment."
    })
    currentHour += 3

    # Recovery & Lunch
    schedule.append({
        "timeRange": f"{currentHour:02d}:00 - {currentHour+1:02d}:00",
        "blockType": "Recovery",
        "activity": "Nutritional intake, physical walk, non-digital rest.",
        "protocol": "No screen engagement."
    })
    currentHour += 1

    # Collaboration / Meetings
    schedule.append({
        "timeRange": f"{currentHour:02d}:00 - {currentHour+meetingBlocks:02d}:00",
        "blockType": "Sync & Communications",
        "activity": "Team syncs, PR reviews, email triage, alignment.",
        "protocol": "Batch processed."
    })
    currentHour += meetingBlocks

    # Afternoon Tactical Execution
    remainingHours = endHour - currentHour - 1
    if remainingHours > 0:
        schedule.append({
            "timeRange": f"{currentHour:02d}:00 - {currentHour+remainingHours:02d}:00",
            "blockType": "Secondary Execution",
            "activity": "Implementation, bug fixing, test coverage.",
            "protocol": "Continuous integration cycle."
        })
        currentHour += remainingHours

    # Shutdown routine
    schedule.append({
        "timeRange": f"{endHour-1:02d}:00 - {endHour:02d}:00",
        "blockType": "System Shutdown",
        "activity": "Log review, clean workspace, set tomorrow's 3 priority deliverables.",
        "protocol": "Closure state."
    })

    return schedule


def evaluate_decision_matrix(
    criteriaWeights: Dict[str, float],
    candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes a weighted scoring model for complex decisions.
    criteriaWeights: e.g. {"impact": 0.40, "feasibility": 0.30, "risk_inverse": 0.30}
    candidates: list of {"name": "Option A", "scores": {"impact": 8, "feasibility": 9, "risk_inverse": 5}}
    """
    scoredCandidates: List[Dict[str, Any]] = []

    for option in candidates:
        optionName = option.get("name", "Unnamed")
        rawScores = option.get("scores", {})
        totalWeightedScore = 0.0

        for criterionKey, weightFactor in criteriaWeights.items():
            criterionScore = float(rawScores.get(criterionKey, 0))
            totalWeightedScore += criterionScore * weightFactor

        scoredCandidates.append({
            "name": optionName,
            "weightedScore": round(totalWeightedScore, 2),
            "breakdown": rawScores
        })

    sortedCandidates = sorted(scoredCandidates, key=lambda x: x["weightedScore"], reverse=True)
    winner = sortedCandidates[0]["name"] if sortedCandidates else "None"

    return {
        "status": "[OK]",
        "criteriaWeights": criteriaWeights,
        "rankedResults": sortedCandidates,
        "recommendedOption": winner,
        "guidance": f"Option '{winner}' scored highest based on normalized criteria weights."
    }
