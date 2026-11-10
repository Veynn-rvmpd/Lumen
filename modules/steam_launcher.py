"""
Steam Local Game Discovery & Protocol Launcher.
Detects installed titles through Steam VDF library manifests and executes
direct launches via the steam://run/<app_id> protocol without third-party overlays.
"""

import os
import re
import sys
import subprocess
import webbrowser
from typing import Dict, List, Any, Optional

try:
    import winreg
except ImportError:
    winreg = None  # Fallback when running outside native Windows host


DEFAULT_KNOWN_STEAM_CATALOG = [
    {"appId": 730, "title": "Counter-Strike 2", "sizeGb": 34.5, "installed": True},
    {"appId": 570, "title": "Dota 2", "sizeGb": 48.0, "installed": False},
    {"appId": 1091500, "title": "Cyberpunk 2077", "sizeGb": 72.1, "installed": True},
    {"appId": 1245620, "title": "Elden Ring", "sizeGb": 49.3, "installed": True},
    {"appId": 1172470, "title": "Apex Legends", "sizeGb": 56.8, "installed": False},
    {"appId": 252490, "title": "Rust", "sizeGb": 24.0, "installed": False},
    {"appId": 1086940, "title": "Baldur's Gate 3", "sizeGb": 122.4, "installed": True},
    {"appId": 413150, "title": "Stardew Valley", "sizeGb": 0.6, "installed": True}
]


def resolve_steam_installation_path() -> Optional[str]:
    """
    Locates the primary Steam directory on Windows via registry or standard filesystem paths.
    """
    if winreg:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as keyHandle:
                steamRootPath, _ = winreg.QueryValueEx(keyHandle, "SteamPath")
                if os.path.exists(steamRootPath):
                    return os.path.normpath(steamRootPath)
        except OSError:
            pass

    standardFallback = r"C:\Program Files (x86)\Steam"
    if os.path.exists(standardFallback):
        return standardFallback

    return None


def _parse_acf_manifest(manifestFilePath: str) -> Optional[Dict[str, Any]]:
    """
    Extracts AppId and Name fields from Steam's Valve Data Format (VDF) manifest file.
    """
    try:
        with open(manifestFilePath, "r", encoding="utf-8", errors="ignore") as manifestFile:
            fileContent = manifestFile.read()

        appIdMatch = re.search(r'"appid"\s+"(\d+)"', fileContent, re.IGNORECASE)
        nameMatch = re.search(r'"name"\s+"([^"]+)"', fileContent, re.IGNORECASE)
        sizeMatch = re.search(r'"SizeOnDisk"\s+"(\d+)"', fileContent, re.IGNORECASE)

        if appIdMatch and nameMatch:
            rawBytes = int(sizeMatch.group(1)) if sizeMatch else 0
            return {
                "appId": int(appIdMatch.group(1)),
                "title": nameMatch.group(1),
                "sizeGb": round(rawBytes / (1024 ** 3), 2),
                "installed": True
            }
    except OSError:
        pass

    return None


def get_installed_games() -> List[Dict[str, Any]]:
    """
    Scans local Steam library folders for installed games using .acf manifests.
    Falls back to a curated catalog if Steam is not installed or accessible.
    """
    steamPath = resolve_steam_installation_path()
    discoveredGames: List[Dict[str, Any]] = []

    if steamPath:
        steamAppsPath = os.path.join(steamPath, "steamapps")
        if os.path.exists(steamAppsPath):
            for fileName in os.listdir(steamAppsPath):
                if fileName.startswith("appmanifest_") and fileName.endswith(".acf"):
                    parsed = _parse_acf_manifest(os.path.join(steamAppsPath, fileName))
                    if parsed:
                        discoveredGames.append(parsed)

    if discoveredGames:
        return sorted(discoveredGames, key=lambda g: g["title"])

    # Fallback to predefined catalogue for dashboard testing
    return DEFAULT_KNOWN_STEAM_CATALOG


def launch_game(appId: int) -> Dict[str, Any]:
    """
    Instructs the local operating system to launch a Steam title using the registered
    steam:// protocol. This is cleaner and more reliable than hunting for game executables.
    """
    steamProtocolUri = f"steam://run/{appId}"

    try:
        if sys.platform == "win32":
            # Direct shell execution for protocol handler
            os.startfile(steamProtocolUri)
        else:
            webbrowser.open(steamProtocolUri)

        return {
            "status": "[OK]",
            "appId": appId,
            "action": "protocol_dispatched",
            "uri": steamProtocolUri,
            "message": f"Dispatched Steam run protocol for application ID {appId}."
        }
    except Exception as launchError:
        return {
            "status": "[ERROR]",
            "appId": appId,
            "action": "protocol_failed",
            "message": str(launchError)
        }


def is_steam_running() -> bool:
    """
    Checks whether the Steam client background process is active.
    """
    try:
        import psutil
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and proc.info["name"].lower() == "steam.exe":
                return True
    except Exception:
        pass
    return False
