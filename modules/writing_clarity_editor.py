"""
Executive Writing Clarity, Tone & Brevity Editor.
Audits prose for passive constructions, filler phrases, sentence bloat,
and provides direct editorial tightening for executive clarity.
"""

import re
from typing import Dict, List, Any


FILLER_PHRASES = {
    "in order to": "to",
    "at this point in time": "currently",
    "due to the fact that": "because",
    "for the purpose of": "for",
    "with reference to": "regarding",
    "in the event that": "if",
    "has the ability to": "can",
    "it is important to note that": "",
    "needless to say": "",
    "at the end of the day": "ultimately",
    "con el fin de": "para",
    "a pesar de que": "aunque",
    "en el momento actual": "actualmente",
    "es necesario señalar que": "",
    "cabe destacar que": ""
}

PASSIVE_INDICATORS = [
    r'\b(?:is|are|was|were|been|being)\s+([a-z]+ed)\b',
    r'\b(?:ha sido|han sido|fue|fueron)\s+([a-z]+do)\b'
]


def audit_text_clarity(rawProse: str) -> Dict[str, Any]:
    """
    Evaluates prose readability, sentence lengths, passive voice density,
    and flags redundant filler phrases.
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', rawProse) if s.strip()]
    words = rawProse.split()
    totalWordCount = len(words)
    totalSentenceCount = max(1, len(sentences))
    averageSentenceLength = round(totalWordCount / totalSentenceCount, 1)

    detectedFillers: List[Dict[str, str]] = []
    textLower = rawProse.lower()
    for filler, replacement in FILLER_PHRASES.items():
        if filler in textLower:
            detectedFillers.append({
                "phrase": filler,
                "suggestedAlternative": replacement if replacement else "Omit entirely"
            })

    longSentences: List[str] = [s for s in sentences if len(s.split()) > 25]

    passiveCount = 0
    for pattern in PASSIVE_INDICATORS:
        passiveCount += len(re.findall(pattern, rawProse, re.IGNORECASE))

    # Base clarity score on sentence brevity and low filler density
    clarityScore = 100 - (len(detectedFillers) * 6) - (len(longSentences) * 8) - (passiveCount * 5)
    clarityScore = max(10, min(100, clarityScore))

    return {
        "wordCount": totalWordCount,
        "sentenceCount": totalSentenceCount,
        "averageSentenceLengthWords": averageSentenceLength,
        "clarityScorePercent": clarityScore,
        "detectedFillers": detectedFillers,
        "passiveConstructionsDetected": passiveCount,
        "oversizedSentencesCount": len(longSentences),
        "oversizedSentences": longSentences[:3],
        "verdict": "Clear and direct" if clarityScore >= 80 else "Requires tightening and elimination of fluff"
    }


def refine_text_executive(rawProse: str) -> Dict[str, Any]:
    """
    Applies automatic replacement of filler phrases and provides a streamlined draft.
    """
    streamlinedText = rawProse
    for filler, replacement in FILLER_PHRASES.items():
        streamlinedText = re.sub(
            rf'\b{re.escape(filler)}\b',
            replacement,
            streamlinedText,
            flags=re.IGNORECASE
        )

    # Clean double spaces
    streamlinedText = re.sub(r'\s{2,}', ' ', streamlinedText).strip()

    return {
        "status": "[OK]",
        "originalText": rawProse,
        "streamlinedDraft": streamlinedText,
        "characterReductionPercent": round((1 - (len(streamlinedText) / max(len(rawProse), 1))) * 100, 1)
    }
