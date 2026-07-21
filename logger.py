from dotenv import load_dotenv
load_dotenv()

import logging
import os
import sys
from urllib.parse import urlparse

logger = logging.getLogger("survey_auth")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    # ── STANDARD HANDLER ──
    # Console for production (Render), rotating file for local dev
    if os.getenv("ENVIRONMENT") == "production":
        handler = logging.StreamHandler(sys.stdout)
    else:
        from logging.handlers import RotatingFileHandler
        os.makedirs("logs", exist_ok=True)
        handler = RotatingFileHandler(
            "logs/auth.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=10,
            encoding="utf-8",
        )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # ── SPLUNK HANDLER ──
    SPLUNK_HOST_RAW = os.getenv("SPLUNK_HOST")
    SPLUNK_TOKEN    = os.getenv("SPLUNK_TOKEN")

    if SPLUNK_HOST_RAW and SPLUNK_TOKEN:
        try:
            from splunk_handler import SplunkHandler

            # Strip protocol (https:// or http://) from ngrok URL
            # SplunkHandler expects bare hostname only e.g.
            # "grimacing-reenact-shudder.ngrok-free.dev"
            parsed = urlparse(SPLUNK_HOST_RAW)
            SPLUNK_HOSTNAME = parsed.hostname or SPLUNK_HOST_RAW

            # ngrok runs on 443 (HTTPS), local Splunk HEC runs on 8088
            # Auto-detect based on whether it's an ngrok URL
            is_ngrok = "ngrok" in SPLUNK_HOSTNAME
            SPLUNK_PORT  = int(os.getenv("SPLUNK_PORT", 443 if is_ngrok else 8088))
            SPLUNK_INDEX = os.getenv("SPLUNK_INDEX", "survey_auth_logs")
            is_prod      = os.getenv("ENVIRONMENT") == "production"

            splunk_handler = SplunkHandler(
                host=SPLUNK_HOSTNAME,
                port=SPLUNK_PORT,
                token=SPLUNK_TOKEN,
                index=SPLUNK_INDEX,
                sourcetype="_json",   # auto-extracts JSON fields in Splunk
                source="auth.log",
                verify=is_prod,       # SSL verify on in production, off locally
                protocol="https" if (is_ngrok or is_prod) else "http",
            )

            splunk_formatter = logging.Formatter("%(message)s")
            splunk_handler.setFormatter(splunk_formatter)
            logger.addHandler(splunk_handler)

            print(
                f"[Splunk] Handler attached → {SPLUNK_HOSTNAME}:{SPLUNK_PORT} "
                f"index={SPLUNK_INDEX}",
                file=sys.stdout
            )

        except Exception as e:
            print(
                f"[Splunk Warning] SplunkHandler failed: {e} — "
                f"Run: pip install splunk-handler",
                file=sys.stderr
            )

    logger.propagate = False