-- SHIPTIVITAS TASK 3
-- SQL queries for feature release analysis

-- ==========================================
-- PART 1: AVERAGE DAILY ACTIVE USERS
-- Before and after the feature release
-- ==========================================

WITH daily_users AS (
    SELECT
        DATE(login_timestamp, 'unixepoch') AS activity_date,
        COUNT(DISTINCT user_id) AS daily_active_users
    FROM login_history
    GROUP BY activity_date
)
SELECT
    CASE
        WHEN activity_date < '2018-06-02'
        THEN 'Before Release'
        ELSE 'After Release'
    END AS release_period,
    ROUND(AVG(daily_active_users), 2) AS average_daily_users
FROM daily_users
GROUP BY release_period
ORDER BY release_period;


-- ==========================================
-- PART 2: NUMBER OF STATUS CHANGES BY CARD
-- Excludes initial card creation
-- ==========================================

SELECT
    c.id AS card_id,
    c.name AS card_name,
    COUNT(h.id) AS number_of_status_changes
FROM card c
LEFT JOIN card_change_history h
    ON c.id = h.cardID
    AND h.oldStatus IS NOT NULL
    AND h.oldStatus != h.newStatus
GROUP BY c.id, c.name
ORDER BY number_of_status_changes DESC;
