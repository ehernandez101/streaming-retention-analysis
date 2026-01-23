import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# ----------------------------
# Synthetic streaming dataset
# ----------------------------
rng = np.random.default_rng(42)

OUT = Path("../data")
OUT.mkdir(parents=True, exist_ok=True)

# Parameters
N_USERS = 1500
DAYS = 120 # ~4 months
START = datetime(2025, 9, 1)

plans = ["free", "basic", "premium"]
plan_probs = [0.50, 0.35, 0.15]

devices = ["mobile", "web", "tv", "tablet"]
device_probs = [0.40, 0.30, 0.22, 0.08]

genres = ["action", "comedy", "drama", "fantasy", "sports", "sci-fi", "romance"]
countries = ["US", "MX", "BR", "CA", "UK"]

# ----------------------------
# Users table
# ----------------------------
user_ids = np.arange(1, N_USERS + 1)
signup_offsets = rng.integers(0, 60, size=N_USERS) # signup during first 2 months
signup_dates = [START + timedelta(days=int(x)) for x in signup_offsets]

users = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": pd.to_datetime(signup_dates),
    "plan": rng.choice(plans, size=N_USERS, p=plan_probs),
    "country": rng.choice(countries, size=N_USERS, p=[0.60, 0.10, 0.10, 0.10, 0.10]),
})

# ----------------------------
# Sessions (watch events)
# ----------------------------
# Base activity by plan
active_prob = {"free": 0.16, "basic": 0.22, "premium": 0.28}
minutes_mu = {"free": 18, "basic": 26, "premium": 35}

rows = []
session_id = 1

for _, u in users.iterrows():
    # personal watch tendency
    stickiness = float(rng.lognormal(mean=0.0, sigma=0.35))
    stickiness = min(stickiness, 2.3)

    # simple churn proxy: some users become inactive after a random day
    churn_chance = {"free": 0.70, "basic": 0.60, "premium": 0.50}[u["plan"]]
    churn_day = None
    if rng.random() < churn_chance:
        churn_day = int(rng.integers(14, DAYS))

    for d in range(DAYS):
        day = u["signup_date"].to_pydatetime() + timedelta(days=int(d))
        if churn_day is not None and d > churn_day:
            break

        p = active_prob[u["plan"]] * stickiness
        # weekend boost
        if day.weekday() >= 5:
            p *= 1.15

        if rng.random() < min(p, 0.85):
            # sessions per day (1–4 usually)
            n_sessions = max(1, int(rng.poisson(lam=1.0 * stickiness)) + 1)
            for _ in range(n_sessions):
                minutes = int(max(2, rng.normal(loc=minutes_mu[u["plan"]], scale=10)))
                rows.append({
                    "session_id": session_id,
                    "user_id": int(u["user_id"]),
                    "session_date": pd.to_datetime(day.date()),
                    "device": rng.choice(devices, p=device_probs),
                    "genre": rng.choice(genres),
                    "watch_minutes": minutes,
                    "completed_episode": int(minutes >= 20 and rng.random() < 0.60),
                })
                session_id += 1

sessions = pd.DataFrame(rows)

# Save
users.to_csv(OUT / "users.csv", index=False)
sessions.to_csv(OUT / "sessions.csv", index=False)

print("✅ Wrote:", OUT / "users.csv")
print("✅ Wrote:", OUT / "sessions.csv")
print("Rows (sessions):", len(sessions))
