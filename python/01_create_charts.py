import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "visuals"
OUT.mkdir(parents=True, exist_ok=True)

users_path = DATA / "users.csv"
sessions_path = DATA / "sessions.csv"

users = pd.read_csv(users_path)
sessions = pd.read_csv(sessions_path)

# Parse dates
users["signup_date"] = pd.to_datetime(users["signup_date"])
sessions["session_date"] = pd.to_datetime(sessions["session_date"])

# ----------------------------
# 1) DAU trend
# ----------------------------
dau = sessions.groupby(sessions["session_date"].dt.date)["user_id"].nunique().reset_index()
dau.columns = ["date", "dau"]

plt.figure()
plt.plot(dau["date"], dau["dau"])
plt.title("Daily Active Users (DAU)")
plt.xlabel("Date")
plt.ylabel("Active Users")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "dau_trend.png", dpi=150)
plt.close()

# ----------------------------
# 2) Watch time by plan
# ----------------------------
watch_by_plan = sessions.groupby("plan")["watch_minutes"].mean().reset_index()

plt.figure()
plt.bar(watch_by_plan["plan"], watch_by_plan["watch_minutes"])
plt.title("Avg Watch Minutes by Plan")
plt.xlabel("Plan")
plt.ylabel("Avg Watch Minutes")
plt.tight_layout()
plt.savefig(OUT / "watch_minutes_by_plan.png", dpi=150)
plt.close()

# ----------------------------
# 3) Device mix
# ----------------------------
device_mix = sessions["device"].value_counts().reset_index()
device_mix.columns = ["device", "sessions"]

plt.figure()
plt.bar(device_mix["device"], device_mix["sessions"])
plt.title("Sessions by Device")
plt.xlabel("Device")
plt.ylabel("Sessions")
plt.tight_layout()
plt.savefig(OUT / "sessions_by_device.png", dpi=150)
plt.close()

# ----------------------------
# 4) Simple retention (D1 / D7 / D30)
# ----------------------------
# First session date per user
first_session = sessions.groupby("user_id")["session_date"].min().reset_index()
first_session.columns = ["user_id", "first_session_date"]

tmp = sessions.merge(first_session, on="user_id", how="left")
tmp["days_since_first"] = (tmp["session_date"].dt.date - tmp["first_session_date"].dt.date).apply(lambda x: x.days)

def retention_at(day):
    return tmp[tmp["days_since_first"] == day]["user_id"].nunique() / tmp["user_id"].nunique()

d1 = retention_at(1)
d7 = retention_at(7)
d30 = retention_at(30)

plt.figure()
plt.bar(["D1", "D7", "D30"], [d1, d7, d30])
plt.title("Retention (Simple) — D1 / D7 / D30")
plt.xlabel("Day")
plt.ylabel("Retention Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(OUT / "retention_d1_d7_d30.png", dpi=150)
plt.close()

print("✅ Saved charts to:", OUT)
print(" - dau_trend.png")
print(" - watch_minutes_by_plan.png")
print(" - sessions_by_device.png")
print(" - retention_d1_d7_d30.png")
