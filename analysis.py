
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect("shiptivity.db")

# ==========================================
# GRAPH 1: DAILY ACTIVE USERS
# ==========================================

dau_query = """
SELECT
    DATE(login_timestamp, 'unixepoch') AS activity_date,
    COUNT(DISTINCT user_id) AS daily_active_users
FROM login_history
GROUP BY activity_date
ORDER BY activity_date;
"""

dau = pd.read_sql_query(dau_query, conn)
dau["activity_date"] = pd.to_datetime(dau["activity_date"])

# Calculate average DAU before and after release
before = dau[dau["activity_date"] < "2018-06-02"]
after = dau[dau["activity_date"] >= "2018-06-02"]

before_avg = round(before["daily_active_users"].mean(), 2)
after_avg = round(after["daily_active_users"].mean(), 2)

print("Average DAU before release:", before_avg)
print("Average DAU after release:", after_avg)

# Plot daily active users
plt.figure(figsize=(12, 6))

plt.plot(
    dau["activity_date"],
    dau["daily_active_users"],
    label="Daily Active Users"
)

plt.axvline(
    pd.Timestamp("2018-06-02"),
    linestyle="--",
    label="Feature Release (June 2, 2018)"
)

plt.title("Daily Active Users Before and After Feature Release")
plt.xlabel("Date")
plt.ylabel("Number of Active Users")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("dau_graph.png", dpi=300)
plt.close()


# ==========================================
# GRAPH 2: STATUS CHANGES BY CARD
# ==========================================

card_query = """
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
"""

card_activity = pd.read_sql_query(card_query, conn)

# Display the status change counts
print("\nStatus changes by card:")
print(card_activity.to_string(index=False))

# Plot status changes for each card
plt.figure(figsize=(12, max(8, len(card_activity) * 0.15)))

plt.barh(
    card_activity["card_id"].astype(str),
    card_activity["number_of_status_changes"]
)

plt.title("Number of Status Changes by Card")
plt.xlabel("Number of Status Changes")
plt.ylabel("Card ID")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("card_activity_graph.png", dpi=300)
plt.close()


# ==========================================
# FINISH
# ==========================================

conn.close()

print("\nBoth graphs generated successfully!")
print("Generated files:")
print("1. dau_graph.png")
print("2. card_activity_graph.png")
