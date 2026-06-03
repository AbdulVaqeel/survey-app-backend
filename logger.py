import logging
import os
import sys

logger = logging.getLogger("survey_auth")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    # Standard Fallback Handler (Console for production container, File for local dev)
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

    # ── SPLUNK INTEGRATION LAYER ──
    SPLUNK_HOST = os.getenv("SPLUNK_HOST")
    SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")

    # Only attempt setup if variables exist; prevents local development from crashing
    if SPLUNK_HOST and SPLUNK_TOKEN:
        try:
            from splunk_handler import SplunkHandler

            SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", 8088))
            SPLUNK_INDEX = os.getenv("SPLUNK_INDEX", "survey_auth_logs")
            
            # Use SSL verification in production, disable if your local HEC uses standard HTTP
            is_prod = os.getenv("ENVIRONMENT") == "production"

            splunk_handler = SplunkHandler(
                host=SPLUNK_HOST,
                port=SPLUNK_PORT,
                token=SPLUNK_TOKEN,
                index=SPLUNK_INDEX,
                sourcetype="_json",       # Forces Splunk to auto-extract fields like "status"
                source="auth.log",
                verify=is_prod            # Enforces secure HTTPS validation in production
            )

            # Pass the raw log string directly so Splunk processes the pure JSON payload seamlessly
            splunk_formatter = logging.Formatter("%(message)s")
            splunk_handler.setFormatter(splunk_formatter)
            logger.addHandler(splunk_handler)
            
        except Exception as e:
            print(f"[Splunk Logging Warning]: Failed to initialize SplunkHandler: {e}", file=sys.stderr)

    logger.propagate = False