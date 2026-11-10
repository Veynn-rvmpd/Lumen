"""
Process Environment & Workspace Profile Manager.
Orchestrates automated operating system profiles (Focus, Dev, Meeting),
adjusting background application states, alerts, and runtime contexts.
"""

from typing import Dict, List, Any


ACTIVE_PROFILE_STATE = {
    "current": "Dev",
    "activatedAt": "2026-11-10T13:30:00",
    "notificationsMuted": False
}

PROFILES_REGISTRY = {
    "Focus": {
        "description": "High-cognitive execution block. Non-essential services suspended.",
        "muteNotifications": True,
        "allowedApplications": ["Terminal", "Code Editor", "Document Viewer"],
        "telemetryIntervalSeconds": 15,
        "spotifyPreset": "Ambient Focus / Minimalist Modern Classical"
    },
    "Dev": {
        "description": "Active engineering and architecture workflow with live watchers.",
        "muteNotifications": False,
        "allowedApplications": ["IDE", "Terminal", "Browser DevTools", "Database Client"],
        "telemetryIntervalSeconds": 5,
        "spotifyPreset": "Electronic / Lo-Fi Precision"
    },
    "Meeting": {
        "description": "Low-latency communications profile. High priority to audio/video buffers.",
        "muteNotifications": True,
        "allowedApplications": ["Video Conference Client", "Calendar", "Scratchpad"],
        "telemetryIntervalSeconds": 30,
        "spotifyPreset": "Muted"
    }
}


def get_available_profiles() -> Dict[str, Any]:
    """
    Returns available operational profiles and current active configuration.
    """
    return {
        "activeProfile": ACTIVE_PROFILE_STATE["current"],
        "profiles": PROFILES_REGISTRY
    }


def activate_environment_profile(profileName: str) -> Dict[str, Any]:
    """
    Applies the target environment profile across system settings and monitors.
    """
    normalizedName = profileName.capitalize()

    if normalizedName not in PROFILES_REGISTRY:
        return {
            "status": "[ERROR]",
            "message": f"Profile '{profileName}' is not defined. Choose from: {list(PROFILES_REGISTRY.keys())}"
        }

    selectedConfig = PROFILES_REGISTRY[normalizedName]
    ACTIVE_PROFILE_STATE["current"] = normalizedName
    ACTIVE_PROFILE_STATE["notificationsMuted"] = selectedConfig["muteNotifications"]

    return {
        "status": "[OK]",
        "activeProfile": normalizedName,
        "profileDetails": selectedConfig,
        "actionReport": [
            f"OS Notification Mute state set to {selectedConfig['muteNotifications']}.",
            f"Telemetry polling frequency adjusted to {selectedConfig['telemetryIntervalSeconds']}s.",
            f"Audio context switched to '{selectedConfig['spotifyPreset']}'."
        ]
    }


def get_current_profile() -> str:
    """
    Returns currently engaged workspace profile name.
    """
    return ACTIVE_PROFILE_STATE["current"]
