# Streaming Retention Analysis

Subscription retention + engagement analysis using Python & KPI reporting.

---

## Overview
This project analyzes user streaming behavior to identify retention trends and engagement drivers.

**Goal:** Understand which user segments, subscription plans, and devices influence watch activity and retention.

---

## Key Questions Answered
- How does engagement change over time (Daily Active Users)?
- Which subscription plans have the highest watch minutes?
- Which devices generate the most sessions?
- What does retention look like across D1, D7, and D30?

---

## Key KPIs & Visuals

### Daily Active Users (DAU)
![DAU Trend](visuals/dau_trend.png)

### Avg Watch Minutes by Plan
![Watch Minutes by Plan](visuals/watch_minutes_by_plan.png)

### Sessions by Device
![Sessions by Device](visuals/sessions_by_device.png)

### Retention (Simple) — D1 / D7 / D30
![Retention](visuals/retention_d1_d7_d30.png)

---

## Results / Insights
Based on the KPI visuals and dataset trends:

- **DAU Trend:** Daily active users increased steadily, peaked around mid-cycle, then gradually declined toward the end.
- **Watch Minutes by Plan:** Premium users show the highest engagement (most watch minutes), while free users show the lowest.
- **Sessions by Device:** Mobile generates the most sessions, followed by web, showing most activity occurs on portable/accessible platforms.
- **Retention (D1/D7/D30):** Retention slightly decreases over time, with D30 being the lowest, indicating users drop off as time passes.

---

## Tools Used
- Python (Pandas, NumPy, Matplotlib)
- SQL (analysis queries)
- KPI reporting / visual storytelling

---

# SQL Queries

This folder contains SQL queries used to calculate project KPIs.

## Files
- `01_dau.sql` — Daily active users by day
- `02_watch_minutes_by_plan.sql` — Avg watch minutes grouped by subscription plan
- `03_sessions_by_device.sql` — Session counts by device
- `04_retention_d1_d7_d30.sql` — Simple retention calculation (D1/D7/D30)

---

## Project Structure
- `/data` → datasets (CSV files)
- `/python` → scripts for data generation + chart creation
- `/sql` → SQL queries used for KPI analysis
- `/visuals` → output charts displayed in README

---

## How to Run Locally

### 1) Clone the repo
```bash
