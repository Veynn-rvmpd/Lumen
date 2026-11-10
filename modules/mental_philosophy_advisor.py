"""
Educational Psychology & Applied Philosophy Advisory.
Provides structured cognitive frameworks, mental models for decision-making,
and classical philosophical perspectives strictly for educational and self-reflection purposes.
"""

from typing import Dict, List, Any


def analyze_cognitive_bias(scenarioDescription: str) -> Dict[str, Any]:
    """
    Identifies candidate cognitive biases in a described situation and provides
    mitigation strategies to preserve objective evaluation.
    """
    textLower = scenarioDescription.lower()
    identifiedBiases: List[Dict[str, str]] = []

    if any(k in textLower for k in ["already spent", "invested so much", "cannot quit now", "wasted time"]):
        identifiedBiases.append({
            "bias": "Sunk Cost Fallacy",
            "mechanism": "Valuing past unrecoverable investments over future expected utility.",
            "remedy": "Evaluate the decision strictly moving forward: if you started today from zero, would you commit capital or hours to this path?"
        })

    if any(k in textLower for k in ["always happens", "saw in the news", "just heard", "recent"]):
        identifiedBiases.append({
            "bias": "Availability Heuristic",
            "mechanism": "Overestimating the frequency or likelihood of events easily recalled from memory.",
            "remedy": "Examine base-rate empirical frequencies rather than salient anecdotes."
        })

    if any(k in textLower for k in ["i knew it", "everyone agrees", "only read", "proves my point"]):
        identifiedBiases.append({
            "bias": "Confirmation Bias",
            "mechanism": "Seeking and overweighting evidence that corroborates existing hypotheses while ignoring disconfirming data.",
            "remedy": "Conduct a red-team exercise: deliberately articulate the strongest three counterarguments against your current conclusion."
        })

    if not identifiedBiases:
        identifiedBiases.append({
            "bias": "Fundamental Attribution Error / Overconfidence",
            "mechanism": "Attributing external friction to lack of discipline or overestimating forecast precision.",
            "remedy": "Establish explicit falsification criteria and margin-of-safety buffers before executing."
        })

    return {
        "scenario": scenarioDescription,
        "biasesDetected": len(identifiedBiases),
        "biasProfiles": identifiedBiases,
        "educationalNotice": "Educational framework only. Not clinical assessment."
    }


def apply_philosophical_lens(
    problemStatement: str,
    schoolOfThought: str = "stoicism"
) -> Dict[str, Any]:
    """
    Reframes an operational dilemma through classical philosophical frameworks:
    Stoicism (control dichotomy), Existentialism (radical responsibility),
    or Pragmatism (consequential verification).
    """
    school = schoolOfThought.strip().lower()

    if "stoic" in school:
        frameworkName = "Stoic Dichotomy of Control"
        thinkers = ["Epictetus", "Marcus Aurelius", "Seneca"]
        coreAxiom = "Some things are within our power, while others are not. Pain emerges from confusing the two."
        appliedAction = [
            "Isolate actionable variables: your preparation, code quality, and emotional reaction.",
            "Relinquish attachment to external outcomes: market adoption, competitor actions, peer opinions.",
            "Execute 'Premeditatio Malorum': identify the worst potential setback in advance to eliminate surprise."
        ]
    elif "existential" in school:
        frameworkName = "Existential Agency & Responsibility"
        thinkers = ["Viktor Frankl", "Jean-Paul Sartre"]
        coreAxiom = "Between stimulus and response there is a space. In that space is our power to choose."
        appliedAction = [
            "Accept complete ownership of current circumstances without shifting blame to constraints.",
            "Define the underlying purpose: suffering without purpose degrades morale; suffering for a defined objective builds character.",
            "Act decisively: identity is forged through concrete decisions, not theoretical intent."
        ]
    else:
        frameworkName = "Pragmatism & Operational Truth"
        thinkers = ["William James", "Charles Sanders Peirce", "John Dewey"]
        coreAxiom = "The truth of an idea is determined by its practical consequence and working utility in reality."
        appliedAction = [
            "Disregard dogmatic arguments: test what actually functions under empirical constraints.",
            "Measure feedback velocity: shorten the interval between hypothesis, execution, and measured result.",
            "Retain solutions that solve the immediate friction; discard ceremonial complexity."
        ]

    return {
        "school": frameworkName,
        "historicalThinkers": thinkers,
        "coreAxiom": coreAxiom,
        "appliedDirectives": appliedAction,
        "problemFramed": problemStatement
    }


def generate_deliberate_practice_protocol(skillName: str) -> Dict[str, Any]:
    """
    Generates an Ericsson-style deliberate practice breakdown with focused micro-drills
    and immediate feedback mechanics.
    """
    return {
        "skill": skillName,
        "framework": "Ericsson Deliberate Practice",
        "phase1_Chunking": f"Deconstruct '{skillName}' into isolated atomic mechanics rather than general practice.",
        "phase2_Friction": "Identify the exact point where error rate exceeds 20%; that threshold is your training zone.",
        "phase3_ImmediateFeedback": "Install automated or objective feedback loops (e.g. tests, recordings, metrics) within seconds of execution.",
        "phase4_RestRepetition": "Limit high-intensity deliberate sessions to 45-60 minute uninterrupted blocks."
    }
