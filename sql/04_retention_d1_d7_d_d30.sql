-- Simple retention calculation (D1 / D7 / D30)
-- Using first session date per user as signup_date

WITH first_session AS (
  SELECT
    user_id,
    MIN(session_date) AS signup_date
  FROM sessions
  GROUP BY user_id
),
activity_days AS (
  SELECT DISTINCT
    s.user_id,
    fs.signup_date,
    s.session_date
  FROM sessions s
  JOIN first_session fs
    ON s.user_id = fs.user_id
),
retention_flags AS (
  SELECT
    user_id,
    MAX(CASE WHEN session_date = signup_date + INTERVAL '1 day' THEN 1 ELSE 0 END) AS d1,
    MAX(CASE WHEN session_date = signup_date + INTERVAL '7 day' THEN 1 ELSE 0 END) AS d7,
    MAX(CASE WHEN session_date = signup_date + INTERVAL '30 day' THEN 1 ELSE 0 END) AS d30
  FROM activity_days
  GROUP BY user_id
)
SELECT
  AVG(d1) AS retention_d1,
  AVG(d7) AS retention_d7,
  AVG(d30) AS retention_d30
FROM retention_flags;
