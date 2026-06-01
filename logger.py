# import logging
# import os
# from logging.handlers import RotatingFileHandler

# LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
# os.makedirs(LOG_DIR, exist_ok=True)
# LOG_FILE = os.path.join(LOG_DIR, "auth.log")

# logger = logging.getLogger("survey_auth")
# logger.setLevel(logging.INFO)

# handler = RotatingFileHandler(
#     LOG_FILE,
#     maxBytes=5 * 1024 * 1024,  # 5 MB per file
#     backupCount=10,             # keep last 10 rotated files
#     encoding="utf-8",
# )

# formatter = logging.Formatter(
#     '%(asctime)s | %(levelname)s | %(message)s',
#     datefmt='%Y-%m-%dT%H:%M:%S'
# )
# handler.setFormatter(formatter)
# logger.addHandler(handler)

import logging
import os
import sys

logger = logging.getLogger("survey_auth")

if not logger.handlers:
    logger.setLevel(logging.INFO)

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

    logger.propagate = False