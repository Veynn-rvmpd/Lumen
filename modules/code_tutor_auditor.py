"""
Code Quality Auditor, Architectural Simplifier & Engineering Tutor.
Performs pragmatic static inspections, identifies latency and memory bottlenecks,
and provides direct refactoring guidance without academic pedantry.
"""

import ast
import re
from typing import Dict, List, Any


def audit_python_code(codeSnippet: str) -> Dict[str, Any]:
    """
    Analyzes Python source snippets for performance antipatterns, unnecessary complexity,
    unhandled resource contexts, and structural flaws.
    """
    detectedIssues: List[Dict[str, str]] = []
    complexityScore = 1

    # Check for bare exceptions
    if re.search(r'except\s*:', codeSnippet):
        detectedIssues.append({
            "severity": "High",
            "type": "BareExcept",
            "observation": "Bare 'except:' suppresses SystemExit, KeyboardInterrupt, and masks runtime bugs.",
            "remedy": "Catch specific exception types or use 'except Exception as errorContext:'."
        })

    # Check for unmanaged file opens
    if re.search(r'\bopen\(', codeSnippet) and 'with open(' not in codeSnippet:
        detectedIssues.append({
            "severity": "Medium",
            "type": "UnclosedFileResource",
            "observation": "Direct 'open()' call detected outside a 'with' context manager.",
            "remedy": "Wrap in 'with open(...) as fileHandle:' to guarantee descriptor cleanup under failures."
        })

    # Check for string concatenation inside loops
    if re.search(r'for\s+.*\n.*(\+=.*str|\+=\s*["\'])', codeSnippet):
        detectedIssues.append({
            "severity": "Medium",
            "type": "QuadraticStringConcat",
            "observation": "String concatenation inside iterative loop creates O(N^2) memory allocations.",
            "remedy": "Collect substring tokens into a list and apply ''.join(tokenList) once."
        })

    # Check for nested loops
    nestedLoopMatches = len(re.findall(r'for\s+.*:\s*\n\s+for\s+.*:', codeSnippet))
    if nestedLoopMatches > 0:
        detectedIssues.append({
            "severity": "Medium",
            "type": "NestedLoops",
            "observation": f"Found {nestedLoopMatches} nested iteration block(s) indicating potential O(N^2) complexity.",
            "remedy": "Index the lookup collection using a dict or set to achieve O(1) membership checks."
        })

    # AST parsing for syntax and depth analysis
    try:
        parsedTree = ast.parse(codeSnippet)
        functionCount = sum(1 for node in ast.walk(parsedTree) if isinstance(node, ast.FunctionDef))
        classCount = sum(1 for node in ast.walk(parsedTree) if isinstance(node, ast.ClassDef))
        syntaxValid = True
    except SyntaxError as parseErr:
        syntaxValid = False
        detectedIssues.append({
            "severity": "Critical",
            "type": "SyntaxError",
            "observation": f"Syntax error at line {parseErr.lineno}: {parseErr.msg}",
            "remedy": "Resolve syntax errors before running static audit."
        })
        functionCount = 0
        classCount = 0

    return {
        "status": "[OK]" if syntaxValid else "[ERROR]",
        "syntaxValid": syntaxValid,
        "functionCount": functionCount,
        "classCount": classCount,
        "issuesCount": len(detectedIssues),
        "issues": detectedIssues,
        "pragmaticVerdict": (
            "Code conforms to clean production standards."
            if not detectedIssues else
            f"Found {len(detectedIssues)} architectural or performance concerns requiring remediation."
        )
    }


def explain_algorithmic_tradeoff(
    algorithmChoice: str,
    dataVolume: int
) -> Dict[str, Any]:
    """
    Explains the engineering trade-offs between memory footprint and time complexity
    for a chosen algorithmic strategy.
    """
    algoKey = algorithmChoice.strip().lower()

    if "hash" in algoKey or "dict" in algoKey:
        timeComplexity = "O(1) average lookup, O(N) insertion"
        spaceComplexity = "O(N) with ~2.5x memory overhead compared to packed arrays"
        verdict = "Optimal for frequent lookups when available RAM is unconstrained."
    elif "sort" in algoKey:
        timeComplexity = "O(N log N)"
        spaceComplexity = "O(1) to O(N) depending on in-place TimSort implementation"
        verdict = "Preferred when repeated ordered queries or range lookups follow single-pass sorting."
    else:
        timeComplexity = "O(N) scan"
        spaceComplexity = "O(1)"
        verdict = "Best suited for small datasets (N < 10,000) where allocation overhead outweighs linear search."

    return {
        "strategy": algorithmChoice,
        "dataPoints": dataVolume,
        "timeComplexity": timeComplexity,
        "spaceComplexity": spaceComplexity,
        "engineeringGuidance": verdict
    }
