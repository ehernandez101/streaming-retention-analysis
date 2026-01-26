-- Sessions by device

SELECT
  device,
  COUNT(*) AS session_count
FROM sessions
GROUP BY device
ORDER BY session_count DESC;
