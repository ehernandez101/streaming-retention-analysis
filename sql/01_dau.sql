-- Daily Active Users (DAU)
-- Count distinct users per day

SELECT
  session_date,
  COUNT(DISTINCT user_id) AS dau
FROM sessions
GROUP BY session_date
ORDER BY session_date;
