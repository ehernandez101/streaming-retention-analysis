-- Avg watch minutes by subscription plan
-- Requires joining sessions to users

SELECT
  u.plan,
  AVG(s.watch_minutes) AS avg_watch_minutes
FROM sessions s
JOIN users u
  ON s.user_id = u.user_id
GROUP BY u.plan
ORDER BY avg_watch_minutes DESC;
