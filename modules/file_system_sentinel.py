"""
Filesystem Sentinel, Space Management & Garbage Collector.
Scans disk pathways for duplicate candidates, isolates oversized artifacts,
and structures disorganized download folders by MIME typology.
"""

import os
import shutil
import hashlib
from typing import Dict, List, Any, Optional

EXT_MAPPINGS = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".md", ".csv"],
    "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp"],
    "Media": [".mp4", ".mkv", ".mp3", ".wav", ".flac", ".mov"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar", ".iso"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".sql"]
}


def scan_large_files(targetDirectory: str, thresholdMb: float = 100.0) -> List[Dict[str, Any]]:
    """
    Identifies files exceeding the specified threshold size within targetDirectory.
    """
    largeFiles: List[Dict[str, Any]] = []
    thresholdBytes = thresholdMb * 1024 * 1024

    if not os.path.exists(targetDirectory):
        return []

    try:
        for rootDir, _, fileNames in os.walk(targetDirectory):
            for fileName in fileNames:
                fullFilePath = os.path.join(rootDir, fileName)
                try:
                    sizeBytes = os.path.getsize(fullFilePath)
                    if sizeBytes >= thresholdBytes:
                        largeFiles.append({
                            "fileName": fileName,
                            "filePath": fullFilePath,
                            "sizeMb": round(sizeBytes / (1024 * 1024), 2)
                        })
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass

    return sorted(largeFiles, key=lambda f: f["sizeMb"], reverse=True)


def organize_directory_by_type(targetDirectory: str, dryRun: bool = True) -> Dict[str, Any]:
    """
    Sorts loose files in targetDirectory into dedicated subdirectories based on extension.
    """
    if not os.path.exists(targetDirectory):
        return {"status": "[ERROR]", "message": f"Path not found: {targetDirectory}"}

    movesPlanned: List[Dict[str, str]] = []

    try:
        for entry in os.listdir(targetDirectory):
            entryPath = os.path.join(targetDirectory, entry)
            if os.path.isfile(entryPath):
                _, ext = os.path.splitext(entry)
                matchedFolder = "Other"

                for categoryFolder, extensions in EXT_MAPPINGS.items():
                    if ext.lower() in extensions:
                        matchedFolder = categoryFolder
                        break

                destinationFolder = os.path.join(targetDirectory, matchedFolder)
                destinationPath = os.path.join(destinationFolder, entry)

                movesPlanned.append({
                    "fileName": entry,
                    "targetFolder": matchedFolder,
                    "source": entryPath,
                    "destination": destinationPath
                })

                if not dryRun:
                    os.makedirs(destinationFolder, exist_ok=True)
                    shutil.move(entryPath, destinationPath)
    except (OSError, PermissionError) as fsError:
        return {"status": "[ERROR]", "message": str(fsError)}

    return {
        "status": "[OK]",
        "targetDirectory": targetDirectory,
        "dryRun": dryRun,
        "totalFilesPlanned": len(movesPlanned),
        "actions": movesPlanned[:10]
    }


def clean_temporary_garbage(targetDirectory: str, dryRun: bool = True) -> Dict[str, Any]:
    """
    Removes standard harmless garbage files (*.tmp, *~, desktop.ini) within directory.
    """
    garbagePatterns = [".tmp", ".temp", ".log~"]
    cleanedFiles: List[str] = []
    freedBytes = 0

    if not os.path.exists(targetDirectory):
        return {"status": "[ERROR]", "message": "Target path does not exist"}

    for rootDir, _, fileNames in os.walk(targetDirectory):
        for name in fileNames:
            if any(name.endswith(pat) for pat in garbagePatterns):
                targetFilePath = os.path.join(rootDir, name)
                try:
                    size = os.path.getsize(targetFilePath)
                    cleanedFiles.append(targetFilePath)
                    freedBytes += size
                    if not dryRun:
                        os.remove(targetFilePath)
                except (OSError, PermissionError):
                    continue

    return {
        "status": "[OK]",
        "dryRun": dryRun,
        "filesIdentified": len(cleanedFiles),
        "freedSpaceKb": round(freedBytes / 1024, 2),
        "files": cleanedFiles[:5]
    }
