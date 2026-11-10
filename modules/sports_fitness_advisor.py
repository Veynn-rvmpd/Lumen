"""
Athletic Training, Biomechanics & Sports Analytical Hub.
Generates structured training programming, technique checklists, scoreboard tracking,
and mathematical implied probability analysis for market odds (strictly non-wagering).
"""

from typing import Dict, List, Any


def generate_workout_split(
    trainingDaysPerWeek: int = 4,
    trainingFocus: str = "hypertrophy"
) -> Dict[str, Any]:
    """
    Builds a periodized training split based on available weekly frequency and mechanical goals.
    """
    days = max(2, min(6, trainingDaysPerWeek))

    if days == 3:
        routineName = "Full Body Alternating (A/B)"
        sessions = [
            {"session": "Day 1", "focus": "Squat, Overhead Press, Pull-ups, Core"},
            {"session": "Day 2", "focus": "Deadlift, Incline Dumbbell Bench, Barbell Row, Calves"},
            {"session": "Day 3", "focus": "Front Squat, Dips, Romanian Deadlift, Lateral Raises"}
        ]
    elif days == 4:
        routineName = "Upper / Lower Split"
        sessions = [
            {"session": "Day 1", "focus": "Upper Heavy: Bench Press, Barbell Row, Overhead Press, Biceps"},
            {"session": "Day 2", "focus": "Lower Heavy: Barbell Squat, RDL, Leg Press, Calves"},
            {"session": "Day 3", "focus": "Upper Hypertrophy: Incline Press, Lat Pulldown, Lateral Raises, Triceps"},
            {"session": "Day 4", "focus": "Lower Hypertrophy: Deadlift, Bulgarian Split Squats, Hamstring Curls, Abs"}
        ]
    else:
        routineName = "Push / Pull / Legs (PPL)"
        sessions = [
            {"session": "Day 1", "focus": "Push A: Flat Bench, Overhead Press, Incline DB, Triceps"},
            {"session": "Day 2", "focus": "Pull A: Weighted Pull-ups, Barbell Rows, Facepulls, Curls"},
            {"session": "Day 3", "focus": "Legs A: Back Squat, Romanian Deadlift, Quad Extensions, Calves"},
            {"session": "Day 4", "focus": "Push B: Overhead Press, Dips, Cable Flyes, Lateral Raises"},
            {"session": "Day 5", "focus": "Pull B: Deadlift, Chest Supported Row, Hammer Curls, Rear Delts"}
        ]

    return {
        "routineName": routineName,
        "frequencyWeekly": f"{days} days/week",
        "primaryFocus": trainingFocus,
        "progressiveOverloadProtocol": (
            "Double progression model: establish a rep target range (e.g. 8-12). "
            "Increase weight by 2.5% only once the upper limit is achieved across all planned sets with clean form."
        ),
        "deloadFrequency": "Every 6 to 8 weeks reduce working load by 30% to manage systemic nervous fatigue.",
        "weeklyPlan": sessions
    }


def evaluate_exercise_technique(exerciseName: str) -> Dict[str, Any]:
    """
    Provides key biomechanical cues and common failure points for foundational compounds.
    """
    exerciseKey = exerciseName.strip().lower()

    if "squat" in exerciseKey:
        cues = [
            "Maintain 3-point foot contact (heel, first metatarsal, fifth metatarsal).",
            "Brace abdominal wall with diaphragmatic 360-degree breath before descent.",
            "Drive knees outward tracking in line with second toe.",
            "Maintain neutral cervical spine; avoid excessive upward gaze."
        ]
        failurePoints = ["Knee valgus collapse", "Premature hip rise (good-morning squat)", "Heel lifting"]
    elif "deadlift" in exerciseKey:
        cues = [
            "Pull slack out of the barbell before leg drive initiation.",
            "Engage lats by squeezing armpits shut (protecting spinal neutrality).",
            "Drive floor away with midfoot; avoid yanking with lower lumbar."
        ]
        failurePoints = ["Spinal flexion under heavy load", "Bar drifting away from shins", "Hyperextension at lockout"]
    elif "bench" in exerciseKey:
        cues = [
            "Retract and depress scapulae firmly against the bench pad.",
            "Tuck elbows at roughly 45 to 60 degrees relative to torso.",
            "Maintain firm leg drive through heels into the floor."
        ]
        failurePoints = ["Flaring elbows to 90 degrees", "Bouncing bar off sternum", "Lifting glutes off pad"]
    else:
        cues = [
            "Control eccentric tempo (2-3 seconds down).",
            "Ensure full active range of motion without momentum compensation.",
            "Maintain abdominal bracing throughout the set."
        ]
        failurePoints = ["Jerking weights", "Cutting range of motion short", "Lack of controlled eccentric phase"]

    return {
        "exercise": exerciseName,
        "biomechanicalCues": cues,
        "primaryFailurePoints": failurePoints,
        "injuryPreventionRule": "Terminate set when technical failure occurs; do not sacrifice bar path for an extra repetition."
    }


def calculate_implied_odds_probability(decimalOddsList: List[float]) -> Dict[str, Any]:
    """
    Calculates exact implied probabilities from bookmaker decimal odds, determines
    the overround (bookmaker vigorish/margin), and computes theoretical fair odds.
    Strictly for statistical analysis; no betting advice or encouragement.
    """
    if not decimalOddsList or any(odds <= 1.0 for odds in decimalOddsList):
        return {"status": "[ERROR]", "message": "Decimal odds must be strictly greater than 1.0"}

    rawProbabilities = [1.0 / odds for odds in decimalOddsList]
    totalProbabilitySum = sum(rawProbabilities)
    bookmakerMarginPercent = (totalProbabilitySum - 1.0) * 100.0

    fairProbabilities = [prob / totalProbabilitySum for prob in rawProbabilities]
    fairOdds = [round(1.0 / fairProb, 3) for fairProb in fairProbabilities]

    outcomesSummary: List[Dict[str, Any]] = []
    for idx, odds in enumerate(decimalOddsList):
        outcomesSummary.append({
            "outcomeIndex": idx + 1,
            "offeredDecimalOdds": odds,
            "rawImpliedProbabilityPercent": round(rawProbabilities[idx] * 100, 2),
            "fairImpliedProbabilityPercent": round(fairProbabilities[idx] * 100, 2),
            "fairDecimalOdds": fairOdds[idx]
        })

    return {
        "status": "[OK]",
        "outcomesEvaluated": len(decimalOddsList),
        "bookmakerOverroundPercent": round(bookmakerMarginPercent, 2),
        "marketEfficiencyAnalysis": (
            f"The bookmaker built a {bookmakerMarginPercent:.2f}% theoretical margin into these odds. "
            f"Total market probability is {totalProbabilitySum * 100:.2f}%. Any long-term expectation against "
            "this bookmaker margin requires an edge exceeding this percentage."
        ),
        "outcomes": outcomesSummary,
        "disclaimer": "Pure mathematical calculation. LUMEN does not support, promote, or recommend sports wagering."
    }


def get_current_scoreboard() -> List[Dict[str, Any]]:
    """
    Returns latest tracked sports scores for active leagues.
    """
    return [
        {"match": "Real Madrid vs Manchester City", "tournament": "UEFA Champions League", "score": "3 - 2", "status": "Finished"},
        {"match": "Boston Celtics vs Golden State Warriors", "tournament": "NBA Regular Season", "score": "112 - 104", "status": "Finished"},
        {"match": "Arsenal vs Bayern Munich", "tournament": "UEFA Champions League", "score": "2 - 2", "status": "Finished"}
    ]
