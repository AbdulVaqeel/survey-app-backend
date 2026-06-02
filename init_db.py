"""
Run this once to seed the database with the initial user.
Usage: python init_db.py
"""

import os
from database import engine, SessionLocal
import models
from auth import hash_password

# Load default password from environment
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "change_me")


db = SessionLocal()

try:
    username = "vaqeel@vs.sa"

    existing = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

    if not existing:
        user = models.User(
            username=username,
            full_name="Vaqeel",
            hashed_password=hash_password(DEFAULT_PASSWORD),
            is_active=True,
        )

        db.add(user)
        db.commit()

        print(f"✅ User created: {username}")

    else:
        print(f"ℹ️ User already exists: {username}")

finally:
    db.close()

print("Database seeded successfully.")