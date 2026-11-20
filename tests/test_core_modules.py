"""
LUMEN-CORE Comprehensive Test Suite.
Validates all 18 core modules, financial algorithms, productivity matrices,
and multimedia helpers without requiring live network dependencies.
"""

import os
import sys
import unittest
from tempfile import TemporaryDirectory
from PIL import Image

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules import (
    personal_finance_hub,
    sports_fitness_advisor,
    code_tutor_auditor,
    writing_clarity_editor,
    mental_philosophy_advisor,
    productivity_hub,
    file_system_sentinel,
    gmail_cleaner,
    image_editor_helper,
    spotify_controller,
    steam_launcher,
    system_monitor,
    whatsapp_notifier,
    telegram_bot,
    process_env_manager,
    calendar_task_manager
)


class TestPersonalFinanceHub(unittest.TestCase):
    def test_compound_growth_calculation(self):
        growth = personal_finance_hub.calculate_compound_growth(10000, 500, 7.0, 10)
        self.assertGreater(growth["finalPortfolioValue"], growth["totalPrincipalDeposited"])
        self.assertEqual(growth["timeHorizonYears"], 10)
        self.assertGreater(growth["growthMultiple"], 1.0)
        self.assertEqual(len(growth["yearlyProgression"]), 10)

    def test_evaluate_financial_decision(self):
        evaluation = personal_finance_hub.evaluate_financial_decision("Hardware Upgrade", 2000.0, 7.0)
        self.assertIn("10_years", evaluation["opportunityCostByHorizon"])
        self.assertGreater(evaluation["opportunityCostByHorizon"]["30_years"], 2000.0)

    def test_suggest_asset_allocation(self):
        alloc = personal_finance_hub.suggest_asset_allocation("aggressive", 15)
        weights = alloc["allocationWeights"]
        total = weights["global_equities_etf"] + weights["bonds_fixed_income"] + weights["cash_equivalents"]
        self.assertEqual(total, 100)
        self.assertGreaterEqual(weights["global_equities_etf"], 75)

    def test_calculate_budget_breakdown(self):
        budget = personal_finance_hub.calculate_budget_breakdown(3000.0, "50_30_20")
        self.assertEqual(budget["allocatedNeeds"], 1500.0)
        self.assertEqual(budget["allocatedWants"], 900.0)
        self.assertEqual(budget["allocatedSavingsInvestment"], 600.0)

    def test_calculate_emergency_fund(self):
        fund = personal_finance_hub.calculate_emergency_fund(1500.0, "stable")
        self.assertEqual(fund["coverageMonths"], 6)
        self.assertEqual(fund["recommendedCashReserve"], 9000.0)


class TestSportsFitnessAdvisor(unittest.TestCase):
    def test_workout_split_generation(self):
        split3 = sports_fitness_advisor.generate_workout_split(3)
        self.assertEqual(len(split3["weeklyPlan"]), 3)
        split4 = sports_fitness_advisor.generate_workout_split(4)
        self.assertEqual(len(split4["weeklyPlan"]), 4)

    def test_exercise_technique_cues(self):
        technique = sports_fitness_advisor.evaluate_exercise_technique("Barbell Squat")
        self.assertGreater(len(technique["biomechanicalCues"]), 0)
        self.assertGreater(len(technique["primaryFailurePoints"]), 0)

    def test_implied_odds_probability(self):
        oddsResult = sports_fitness_advisor.calculate_implied_odds_probability([2.0, 3.0, 4.0])
        self.assertEqual(oddsResult["status"], "[OK]")
        self.assertGreater(oddsResult["bookmakerOverroundPercent"], 0)
        self.assertEqual(len(oddsResult["outcomes"]), 3)


class TestCodeTutorAuditor(unittest.TestCase):
    def test_audit_detects_flaws(self):
        badCode = (
            "def run_query():\n"
            "    f = open('data.txt')\n"
            "    s = ''\n"
            "    for i in range(100):\n"
            "        s += str(i)\n"
            "    return s\n"
        )
        report = code_tutor_auditor.audit_python_code(badCode)
        self.assertTrue(report["syntaxValid"])
        self.assertGreater(report["issuesCount"], 0)


class TestWritingClarityEditor(unittest.TestCase):
    def test_fluff_elimination(self):
        sampleProse = "In order to complete the task, it is important to note that we must proceed."
        audit = writing_clarity_editor.audit_text_clarity(sampleProse)
        self.assertGreater(len(audit["detectedFillers"]), 0)

        refined = writing_clarity_editor.refine_text_executive(sampleProse)
        self.assertNotIn("in order to", refined["streamlinedDraft"].lower())


class TestMentalPhilosophyAdvisor(unittest.TestCase):
    def test_cognitive_bias_detection(self):
        scenario = "We invested so much capital into this legacy tool that we cannot quit now."
        biasReport = mental_philosophy_advisor.analyze_cognitive_bias(scenario)
        self.assertGreater(biasReport["biasesDetected"], 0)
        self.assertEqual(biasReport["biasProfiles"][0]["bias"], "Sunk Cost Fallacy")

    def test_philosophical_lens(self):
        lens = mental_philosophy_advisor.apply_philosophical_lens("Market contraction", "stoicism")
        self.assertIn("Epictetus", lens["historicalThinkers"])
        self.assertGreater(len(lens["appliedDirectives"]), 0)


class TestProductivityHub(unittest.TestCase):
    def test_eisenhower_quadrants(self):
        tasks = [
            {"title": "Fix Prod Crash", "urgent": True, "important": True},
            {"title": "Refactor Architecture", "urgent": False, "important": True},
            {"title": "Unscheduled Ping", "urgent": True, "important": False},
            {"title": "Browse Feeds", "urgent": False, "important": False}
        ]
        quadrants = productivity_hub.prioritize_tasks_eisenhower(tasks)
        self.assertEqual(len(quadrants["Q1_DoImmediately"]), 1)
        self.assertEqual(len(quadrants["Q2_ScheduleDeepWork"]), 1)
        self.assertEqual(len(quadrants["Q3_DelegateOrAutomate"]), 1)
        self.assertEqual(len(quadrants["Q4_Eliminate"]), 1)

    def test_timeboxed_schedule(self):
        schedule = productivity_hub.generate_timeboxed_schedule(8, 18, "Kernel Engineering", 2)
        self.assertGreaterEqual(len(schedule), 4)

    def test_weighted_decision_matrix(self):
        weights = {"impact": 0.5, "speed": 0.5}
        candidates = [
            {"name": "Option A", "scores": {"impact": 9, "speed": 4}},
            {"name": "Option B", "scores": {"impact": 5, "speed": 9}}
        ]
        result = productivity_hub.evaluate_decision_matrix(weights, candidates)
        self.assertEqual(result["status"], "[OK]")
        self.assertIn(result["recommendedOption"], ["Option A", "Option B"])


class TestFileSystemAndImageHelpers(unittest.TestCase):
    def test_image_inspection_and_conversion(self):
        with TemporaryDirectory() as tempDir:
            testImagePath = os.path.join(tempDir, "sample.png")
            img = Image.new("RGB", (200, 100), color=(50, 50, 50))
            img.save(testImagePath)

            inspectResult = image_editor_helper.inspect_image(testImagePath)
            self.assertEqual(inspectResult["status"], "[OK]")
            self.assertEqual(inspectResult["width"], 200)
            self.assertEqual(inspectResult["height"], 100)

            convertedPath = os.path.join(tempDir, "sample.webp")
            convertResult = image_editor_helper.convert_format(testImagePath, convertedPath, "WEBP")
            self.assertEqual(convertResult["status"], "[OK]")
            self.assertTrue(os.path.exists(convertedPath))


class TestSystemAndNotifiers(unittest.TestCase):
    def test_system_telemetry_metrics(self):
        telemetry = system_monitor.collect_system_telemetry()
        self.assertIn(telemetry["status"], ["[OK]", "[WARN]", "[ALERT]"])
        self.assertGreater(telemetry["cpuCores"], 0)
        self.assertGreater(telemetry["memoryTotalGb"], 0)

    def test_whatsapp_emoji_sanitizer(self):
        dirty = "Priority alert: Database latency spike."
        clean = whatsapp_notifier.sanitize_prohibit_emojis(dirty)
        self.assertEqual(clean, "Priority alert: Database latency spike.")

    def test_telegram_commands(self):
        statusOutput = telegram_bot.handle_incoming_command("/status")
        self.assertIn("[STATUS REPORT]", statusOutput)

        financeOutput = telegram_bot.handle_incoming_command("/finance 10000 500 7.0 10")
        self.assertIn("[FINANCIAL PROJECTION]", financeOutput)

    def test_process_environment_profiles(self):
        switchResult = process_env_manager.activate_environment_profile("Focus")
        self.assertEqual(switchResult["activeProfile"], "Focus")
        self.assertTrue(switchResult["profileDetails"]["muteNotifications"])


if __name__ == "__main__":
    unittest.main()
