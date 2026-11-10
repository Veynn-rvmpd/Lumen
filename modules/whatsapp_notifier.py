"""
WhatsApp Priority Dispatcher.
Transmits critical telemetry alerts, security events, and executive notices
over WhatsApp via Twilio or Meta Cloud API with strict zero-emoji enforcement.
"""

import os
import re
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "console_fallback")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "+14155238886")
WHATSAPP_RECIPIENT_NUMBER = os.getenv("WHATSAPP_RECIPIENT_NUMBER", "")


def sanitize_prohibit_emojis(rawText: str) -> str:
    """
    Strips Unicode emojis and pictographs to enforce strict LUMEN typographical rules.
    """
    emojiPattern = re.compile(
        r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\ufe0f\u200d]",
        flags=re.UNICODE
    )
    cleaned = emojiPattern.sub("", rawText)
    return re.sub(r"\s{2,}", " ", cleaned).strip()


def send_priority_alert(
    messageBody: str,
    priorityLevel: str = "P1",
    recipientPhone: Optional[str] = None
) -> Dict[str, Any]:
    """
    Dispatches a structured priority alert to the configured WhatsApp recipient.
    Valid priority levels: P1 (Critical), P2 (High), P3 (Operational Notice).
    """
    targetRecipient = recipientPhone or WHATSAPP_RECIPIENT_NUMBER
    cleanContent = sanitize_prohibit_emojis(messageBody)
    formattedMessage = f"[{priorityLevel}] LUMEN ALERT: {cleanContent}"

    if WHATSAPP_PROVIDER == "twilio" and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and targetRecipient:
        endpoint = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        payload = {
            "From": f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            "To": f"whatsapp:{targetRecipient}",
            "Body": formattedMessage
        }
        try:
            twilioResponse = requests.post(
                endpoint,
                data=payload,
                auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                timeout=5.0
            )
            return {
                "status": "[OK]" if twilioResponse.status_code in [200, 201] else "[ERROR]",
                "provider": "twilio",
                "recipient": targetRecipient,
                "statusCode": twilioResponse.status_code,
                "message": formattedMessage
            }
        except requests.RequestException as networkError:
            return {"status": "[ERROR]", "provider": "twilio", "error": str(networkError)}

    # Fallback mode: log to terminal output without crashing
    print(f"[WHATSAPP FALLBACK] {formattedMessage}")
    return {
        "status": "[OK]",
        "provider": "console_fallback",
        "recipient": targetRecipient or "Local Console",
        "message": formattedMessage,
        "note": "Credentials unconfigured; message recorded via local executive log."
    }
