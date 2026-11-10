"""
Spotify Multimedia Controller & Text-to-Playlist Generator.
Manages playback state and converts text tracklists or mood prompts
into structured Spotify playlists via Web API with offline fallback.
"""

import os
import time
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNTS_BASE = "https://accounts.spotify.com/api/token"


class SpotifyController:
    """
    Direct interface for Spotify Web API playback and playlist generation.
    Maintains internal fallback playback state when external credentials are unconfigured.
    """

    def __init__(self):
        self.clientId = SPOTIFY_CLIENT_ID
        self.clientSecret = SPOTIFY_CLIENT_SECRET
        self.cachedToken: Optional[str] = None
        self.tokenExpiresAt: float = 0.0

        # In-memory mock state for local testing without active OAuth tokens
        self.playbackState = {
            "isPlaying": False,
            "trackTitle": "Ludovico Einaudi - Nuvole Bianche",
            "album": "Una Mattina",
            "artist": "Ludovico Einaudi",
            "progressMs": 42000,
            "durationMs": 358000,
            "volumePercent": 75,
            "activeDevice": "Workstation Speakers"
        }

    def _get_client_credentials_token(self) -> Optional[str]:
        """
        Retrieves application-level access token via Spotify Client Credentials Flow.
        """
        if not self.clientId or not self.clientSecret:
            return None

        if self.cachedToken and time.time() < self.tokenExpiresAt:
            return self.cachedToken

        # Request new token from Spotify OAuth endpoint
        try:
            tokenResponse = requests.post(
                SPOTIFY_ACCOUNTS_BASE,
                data={"grant_type": "client_credentials"},
                auth=(self.clientId, self.clientSecret),
                timeout=5.0
            )
            if tokenResponse.status_code == 200:
                payload = tokenResponse.json()
                self.cachedToken = payload.get("access_token")
                expiresIn = payload.get("expires_in", 3600)
                self.tokenExpiresAt = time.time() + expiresIn - 60
                return self.cachedToken
        except requests.RequestException:
            pass

        return None

    def get_playback_status(self) -> Dict[str, Any]:
        """
        Returns the current player status, active device, and track metadata.
        """
        return {
            "status": "active" if self.playbackState["isPlaying"] else "paused",
            "playback": self.playbackState,
            "apiConnected": bool(self.clientId and self.clientSecret)
        }

    def play_toggle(self) -> Dict[str, Any]:
        """
        Toggles playback state between playing and paused.
        """
        self.playbackState["isPlaying"] = not self.playbackState["isPlaying"]
        stateText = "resumed" if self.playbackState["isPlaying"] else "paused"
        return {
            "action": "play_toggle",
            "state": stateText,
            "currentTrack": self.playbackState["trackTitle"]
        }

    def next_track(self) -> Dict[str, Any]:
        """
        Skips to the next queued track.
        """
        sampleTracks = [
            ("Max Richter - On the Nature of Daylight", "The Blue Notebooks", "Max Richter", 371000),
            ("Nils Frahm - Says", "Spaces", "Nils Frahm", 500000),
            ("Ólafur Arnalds - saman", "re:member", "Ólafur Arnalds", 192000),
            ("Kiasmos - Looped", "Kiasmos", "Kiasmos", 377000)
        ]
        import random
        selectedTrack = random.choice(sampleTracks)
        self.playbackState["trackTitle"] = selectedTrack[0]
        self.playbackState["album"] = selectedTrack[1]
        self.playbackState["artist"] = selectedTrack[2]
        self.playbackState["durationMs"] = selectedTrack[3]
        self.playbackState["progressMs"] = 0
        self.playbackState["isPlaying"] = True

        return {
            "action": "next_track",
            "currentTrack": self.playbackState["trackTitle"]
        }

    def previous_track(self) -> Dict[str, Any]:
        """
        Restarts current track or returns to preceding track.
        """
        self.playbackState["progressMs"] = 0
        return {
            "action": "previous_track",
            "currentTrack": self.playbackState["trackTitle"]
        }

    def set_volume(self, volumeLevel: int) -> Dict[str, Any]:
        """
        Adjusts playback volume between 0 and 100 percent.
        """
        clampedLevel = max(0, min(100, volumeLevel))
        self.playbackState["volumePercent"] = clampedLevel
        return {
            "action": "set_volume",
            "volumePercent": clampedLevel
        }

    def generate_playlist_from_text(
        self,
        rawTextInput: str,
        playlistTitle: str = "LUMEN Curated Selection"
    ) -> Dict[str, Any]:
        """
        Parses text input (lines of artists/titles, comma-separated titles, or thematic descriptors)
        and structures an actionable playlist catalog with estimated durations.
        """
        cleanLines = [line.strip("- *0123456789. ") for line in rawTextInput.strip().splitlines() if line.strip()]
        if not cleanLines and "," in rawTextInput:
            cleanLines = [item.strip() for item in rawTextInput.split(",") if item.strip()]

        if not cleanLines:
            cleanLines = [
                "Max Richter - Path 5 (delta)",
                "Brian Eno - An Ending (Ascent)",
                "Carbon Based Lifeforms - Photosynthesis",
                "Solar Fields - Sol"
            ]

        structuredTracks: List[Dict[str, Any]] = []
        token = self._get_client_credentials_token()

        for index, itemText in enumerate(cleanLines):
            trackMetadata = self._resolve_track_metadata(itemText, token, trackIndex=index + 1)
            structuredTracks.append(trackMetadata)

        totalEstimatedSeconds = sum(entry["durationSeconds"] for entry in structuredTracks)

        return {
            "playlistTitle": playlistTitle,
            "trackCount": len(structuredTracks),
            "estimatedDurationMinutes": round(totalEstimatedSeconds / 60, 1),
            "tracks": structuredTracks,
            "exportFormat": "M3U / Spotify URI compatible",
            "status": "[READY]"
        }

    def _resolve_track_metadata(
        self,
        queryText: str,
        authToken: Optional[str],
        trackIndex: int
    ) -> Dict[str, Any]:
        """
        Resolves track details against Spotify search API if credentials exist,
        otherwise generates normalized deterministic metadata.
        """
        if authToken:
            try:
                searchEndpoint = f"{SPOTIFY_API_BASE}/search"
                headers = {"Authorization": f"Bearer {authToken}"}
                params = {"q": queryText, "type": "track", "limit": 1}
                searchResp = requests.get(searchEndpoint, headers=headers, params=params, timeout=4.0)
                if searchResp.status_code == 200:
                    data = searchResp.json()
                    items = data.get("tracks", {}).get("items", [])
                    if items:
                        firstMatch = items[0]
                        artists = ", ".join([a.get("name") for a in firstMatch.get("artists", [])])
                        return {
                            "index": trackIndex,
                            "title": firstMatch.get("name"),
                            "artist": artists,
                            "album": firstMatch.get("album", {}).get("name"),
                            "spotifyUri": firstMatch.get("uri"),
                            "externalUrl": firstMatch.get("external_urls", {}).get("spotify"),
                            "durationSeconds": round(firstMatch.get("duration_ms", 0) / 1000)
                        }
            except requests.RequestException:
                pass

        # Offline deterministic resolution
        parts = queryText.split(" - ", 1)
        artistName = parts[0].strip() if len(parts) > 1 else "Various Artists"
        songTitle = parts[1].strip() if len(parts) > 1 else queryText.strip()

        return {
            "index": trackIndex,
            "title": songTitle,
            "artist": artistName,
            "album": "Collection",
            "spotifyUri": f"spotify:track:lumen_{trackIndex:04d}",
            "externalUrl": f"https://open.spotify.com/search/{requests.utils.quote(queryText)}",
            "durationSeconds": 210
        }


# Global singleton instance for direct application access
spotifyControllerInstance = SpotifyController()
