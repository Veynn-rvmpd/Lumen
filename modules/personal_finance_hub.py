"""
Personal Finance & Investment Decision Hub.
Evaluates asset allocation, opportunity cost, compound growth projections,
and capital allocation without speculative advisory claims.
"""

from typing import Dict, List, Any


def calculate_compound_growth(
    initialCapital: float,
    monthlyContribution: float,
    annualReturnRate: float,
    years: int
) -> Dict[str, Any]:
    """
    Computes yearly compounded capital growth, segregating cumulative contributions
    from compounded investment returns to illustrate capital efficiency over time.
    """
    ratePerMonth = annualReturnRate / 100.0 / 12.0
    currentBalance = float(initialCapital)
    cumulativeDeposits = float(initialCapital)
    yearlyMilestones: List[Dict[str, Any]] = []

    for yearIndex in range(1, years + 1):
        for _ in range(12):
            interestAccrued = currentBalance * ratePerMonth
            currentBalance += interestAccrued + monthlyContribution
            cumulativeDeposits += monthlyContribution

        yearlyEarnedInterest = currentBalance - cumulativeDeposits
        yearlyMilestones.append({
            "year": yearIndex,
            "totalBalance": round(currentBalance, 2),
            "contributions": round(cumulativeDeposits, 2),
            "interestEarned": round(yearlyEarnedInterest, 2),
            "interestSharePercent": round((yearlyEarnedInterest / currentBalance) * 100, 2)
        })

    netEarnings = currentBalance - cumulativeDeposits
    return {
        "initialCapital": initialCapital,
        "monthlyContribution": monthlyContribution,
        "annualReturnRate": annualReturnRate,
        "timeHorizonYears": years,
        "finalPortfolioValue": round(currentBalance, 2),
        "totalPrincipalDeposited": round(cumulativeDeposits, 2),
        "totalEarnings": round(netEarnings, 2),
        "growthMultiple": round(currentBalance / max(cumulativeDeposits, 1.0), 2),
        "yearlyProgression": yearlyMilestones
    }


def evaluate_financial_decision(
    expenseOrInvestment: str,
    cost: float,
    alternativeReturnRate: float = 7.0
) -> Dict[str, Any]:
    """
    Quantifies the true opportunity cost of an expense versus deploying that capital
    into a broadly diversified low-cost index fund over multiple compounding horizons.
    """
    annualRateDecimal = alternativeReturnRate / 100.0
    horizons = [5, 10, 20, 30]
    opportunityCostBreakdown: Dict[str, float] = {}

    for horizonYears in horizons:
        compoundedLostValue = cost * ((1 + annualRateDecimal) ** horizonYears)
        opportunityCostBreakdown[f"{horizonYears}_years"] = round(compoundedLostValue, 2)

    tenYearMultiplier = round(opportunityCostBreakdown["10_years"] / max(cost, 1.0), 2)
    thirtyYearMultiplier = round(opportunityCostBreakdown["30_years"] / max(cost, 1.0), 2)

    executiveAssessment = (
        f"A direct expenditure of {cost:.2f} EUR carries an opportunity cost of "
        f"{opportunityCostBreakdown['10_years']:.2f} EUR at 10 years ({tenYearMultiplier}x) "
        f"and {opportunityCostBreakdown['30_years']:.2f} EUR at 30 years ({thirtyYearMultiplier}x) "
        f"assuming a conservative {alternativeReturnRate}% benchmark return."
    )

    return {
        "concept": expenseOrInvestment,
        "nominalAmount": round(cost, 2),
        "benchmarkRate": alternativeReturnRate,
        "opportunityCostByHorizon": opportunityCostBreakdown,
        "assessmentSummary": executiveAssessment,
        "decisionThreshold": "Discretionary purchase justified only if personal utility outweighs 10-year projected value."
    }


def suggest_asset_allocation(
    riskProfile: str,
    timeHorizon: int
) -> Dict[str, Any]:
    """
    Provides disciplined portfolio weightings across low-cost index equities,
    fixed income instruments, and liquid cash reserves. Explicitly highlights
    rebalancing frequency and Total Expense Ratio (TER) drag.
    """
    profileKey = riskProfile.strip().lower()

    if profileKey in ["conservative", "conservador"]:
        equityWeight = 20 if timeHorizon < 3 else 35
        fixedIncomeWeight = 60
        cashWeight = 100 - equityWeight - fixedIncomeWeight
        targetTER = 0.15
        expectedVolatility = "Low (4-7% annual standard deviation)"
    elif profileKey in ["aggressive", "agresivo", "crecimiento"]:
        equityWeight = 85 if timeHorizon >= 10 else 75
        fixedIncomeWeight = 10
        cashWeight = 100 - equityWeight - fixedIncomeWeight
        targetTER = 0.18
        expectedVolatility = "High (14-19% annual standard deviation)"
    else:
        # Default to balanced/moderate configuration
        equityWeight = 60 if timeHorizon >= 5 else 45
        fixedIncomeWeight = 35
        cashWeight = 100 - equityWeight - fixedIncomeWeight
        targetTER = 0.16
        expectedVolatility = "Moderate (8-12% annual standard deviation)"

    return {
        "profile": riskProfile,
        "timeHorizonYears": timeHorizon,
        "allocationWeights": {
            "global_equities_etf": equityWeight,
            "bonds_fixed_income": fixedIncomeWeight,
            "cash_equivalents": cashWeight
        },
        "instrumentGuidelines": {
            "global_equities": "MSCI World or FTSE All-World UCITS ETF with physical replication and TER under 0.20%.",
            "fixed_income": "Eurozone sovereign / aggregate inflation-protected bond index ETF (hedged).",
            "cash_reserve": "High-yield savings or overnight rate monetary funds (e.g., €STR trackers)."
        },
        "rebalancingPolicy": (
            "Review semiannually or trigger when asset weight deviates by +/- 5% "
            "from target allocation. Rebalance via new cash contributions where feasible to minimize tax drag."
        ),
        "feeImpactNotice": (
            f"Target aggregate portfolio TER: <= {targetTER}%. Over a 20-year horizon, "
            "each 0.50% in fund management fees compounds to roughly an 11% reduction in total capital accumulation."
        ),
        "volatilityExpectation": expectedVolatility
    }


def calculate_budget_breakdown(
    monthlyNetIncome: float,
    framework: str = "50_30_20"
) -> Dict[str, Any]:
    """
    Allocates net monthly income according to standard capital budgeting frameworks.
    """
    if framework == "50_30_20":
        needsCapital = monthlyNetIncome * 0.50
        wantsCapital = monthlyNetIncome * 0.30
        savingsCapital = monthlyNetIncome * 0.20
    else:
        needsCapital = monthlyNetIncome * 0.40
        wantsCapital = monthlyNetIncome * 0.20
        savingsCapital = monthlyNetIncome * 0.40

    return {
        "monthlyNetIncome": round(monthlyNetIncome, 2),
        "frameworkUsed": framework,
        "allocatedNeeds": round(needsCapital, 2),
        "allocatedWants": round(wantsCapital, 2),
        "allocatedSavingsInvestment": round(savingsCapital, 2),
        "annualSavingsCapacity": round(savingsCapital * 12, 2)
    }


def calculate_emergency_fund(
    monthlyBasicExpenses: float,
    incomeStability: str = "stable"
) -> Dict[str, Any]:
    """
    Calculates safety reserve based on income stability and non-discretionary commitments.
    """
    multiplierMonths = 3 if incomeStability == "high" else (6 if incomeStability == "stable" else 12)
    recommendedReserve = monthlyBasicExpenses * multiplierMonths

    return {
        "monthlyBasicExpenses": round(monthlyBasicExpenses, 2),
        "incomeStability": incomeStability,
        "coverageMonths": multiplierMonths,
        "recommendedCashReserve": round(recommendedReserve, 2),
        "holdingVehicle": "Liquid money market fund or high-yield deposit account."
    }
