import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "healthcare_analytics.sqlite"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT doctor_id, password FROM Doctor")

for doctor_id, password in cur.fetchall():
    # skip null or already-hashed passwords
    if not password or password.startswith("pbkdf2:"):
        continue

    hashed = generate_password_hash(password, method="pbkdf2:sha256")

    cur.execute(
        "UPDATE Doctor SET password = ? WHERE doctor_id = ?",
        (hashed, doctor_id),
    )

conn.commit()
conn.close()

print("Doctor passwords cleaned and hashed.")
