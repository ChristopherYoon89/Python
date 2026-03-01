

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm


mydata = pd.read_csv("Running_stats.csv")

for col in mydata.columns:
    print(col)

'''
Date
Time
Duration_min
Total_duration
Distance_km
Calories
Heart_maximum
Heart_vigorous
Heart_moderate
Max_heart_rate_bpmin
Avg_pace
Avg_speed_kmph
Avg_cadence_stepspmin
Note
Cumulative_km
'''


# Plot cumulative distance

mydata["Date"] = pd.to_datetime(mydata["Date"], dayfirst=True)
mydata["Distance_km"] = pd.to_numeric(mydata["Distance_km"], errors="coerce")
mydata["Cumulative_km"] = mydata["Distance_km"].cumsum()

last_date = mydata["Date"].iloc[-1]
last_cum = mydata["Cumulative_km"].iloc[-1]

plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#2E2E2E"
plt.rcParams["figure.facecolor"] = "#2E2E2E"
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["xtick.color"] = "#DDDDDD"
plt.rcParams["ytick.color"] = "#DDDDDD"
plt.rcParams["text.color"] = "#EEEEEE"
plt.rcParams["axes.labelcolor"] = "#EEEEEE"

plt.figure(figsize=(6,5))
plt.plot(mydata["Date"], mydata["Cumulative_km"], color="#C700DA")
plt.xlabel("Date")
plt.ylabel("Cumulative distance (km)")
plt.title("Cumulative running distance in km")
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.annotate(
    f"{last_cum:.1f} km",
    xy=(last_date, last_cum),
    xytext=(8, 0),
    textcoords="offset points",
    va="center"
)
plt.show()


# Plot cumulative calories

mydata["Calories"] = pd.to_numeric(mydata["Calories"], errors="coerce")
mydata["Cumulative_calories"] = mydata["Calories"].cumsum()

last_date = mydata["Date"].iloc[-1]
last_cum = mydata["Cumulative_calories"].iloc[-1]

plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#2E2E2E"  
plt.rcParams["figure.facecolor"] = "#2E2E2E"
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["xtick.color"] = "#DDDDDD"
plt.rcParams["ytick.color"] = "#DDDDDD"
plt.rcParams["text.color"] = "#EEEEEE"
plt.rcParams["axes.labelcolor"] = "#EEEEEE"

plt.figure(figsize=(6,5))
plt.plot(mydata["Date"], mydata["Cumulative_calories"], color="#C700DA")
plt.xlabel("Date")
plt.ylabel("Cumulative calories")
plt.title("Cumulative calories")
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.annotate(
    f"{last_cum}",
    xy=(last_date, last_cum),
    xytext=(8, 0),
    textcoords="offset points",
    va="center"
)
plt.show()


# Plot average speed 

df = mydata.dropna(subset=["Avg_speed_kmph"]).copy()
df["Run_Number"] = range(1, len(df) + 1)

x = df["Run_Number"]
y = df["Avg_speed_kmph"]

slope, intercept = np.polyfit(x, y, 1)
regression_line = slope * x + intercept

plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#2E2E2E"   # dark grey
plt.rcParams["figure.facecolor"] = "#2E2E2E"
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["xtick.color"] = "#DDDDDD"
plt.rcParams["ytick.color"] = "#DDDDDD"
plt.rcParams["text.color"] = "#EEEEEE"
plt.rcParams["axes.labelcolor"] = "#EEEEEE"

plt.figure(figsize=(6,5))
plt.plot(df["Run_Number"], df["Avg_speed_kmph"], color="#C700DA")
plt.plot(df["Run_Number"], regression_line, color="#2195C4")
plt.xlabel("Run Number")
plt.ylabel("Average speed in km/h")
plt.title("Average Speed Progression in km/h")
plt.ylim(0, 15)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()


# Plot average speed adjusted for distance

df = mydata.dropna(subset=["Avg_speed_kmph", "Distance_km"]).copy()

df["Avg_speed_kmph"] = pd.to_numeric(df["Avg_speed_kmph"], errors="coerce")
df["Distance_km"] = pd.to_numeric(df["Distance_km"], errors="coerce")

X = df[["Distance_km"]]
X = sm.add_constant(X)
y = df["Avg_speed_kmph"]
model = sm.OLS(y, X).fit()
df["Adj_speed"] = y - model.predict(X)
df["Run_Number"] = range(1, len(df) + 1)

x = df["Run_Number"]
y_adj = df["Adj_speed"]

slope, intercept = np.polyfit(x, y_adj, 1)
regression_line = slope * x + intercept

plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#2E2E2E"   # dark grey
plt.rcParams["figure.facecolor"] = "#2E2E2E"
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["xtick.color"] = "#DDDDDD"
plt.rcParams["ytick.color"] = "#DDDDDD"
plt.rcParams["text.color"] = "#EEEEEE"
plt.rcParams["axes.labelcolor"] = "#EEEEEE"

plt.figure(figsize=(6,5))
plt.plot(x, y_adj, linestyle="-", color="#C700DA")
plt.plot(x, regression_line, color="#2195C4")
plt.xlabel("Run Number")
plt.ylabel("Distance-adjusted average speed (km/h)")
plt.title("Average speed progression adjusted for distance \n (actual vs predicted)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.ylim(-5, 5)
plt.tight_layout()
plt.show()


# Plot relationship between maximu heart rate and average speed

df = mydata.dropna(subset=["Max_heart_rate_bpmin", "Distance_km", "Avg_speed_kmph"]).copy()
df = df[df["Max_heart_rate_bpmin"] > 160].copy()

df["Distance_km"] = pd.to_numeric(df["Distance_km"], errors="coerce")
df["Avg_speed_kmph"] = pd.to_numeric(df["Avg_speed_kmph"], errors="coerce")
df["Max_heart_rate_bpmin"] = pd.to_numeric(df["Max_heart_rate_bpmin"], errors="coerce")

X = df[["Distance_km", "Avg_speed_kmph"]]
X = sm.add_constant(X)
y = df["Max_heart_rate_bpmin"]
model = sm.OLS(y, X).fit()
print(model.summary())

df["Adj_Max_HR"] = y - model.predict(X)
df["Run_Number"] = range(1, len(df) + 1)

x = df["Run_Number"]
y = df["Adj_Max_HR"]

slope, intercept = np.polyfit(x, y, 1)
regression_line = slope * x + intercept

plt.style.use("dark_background")
plt.rcParams["axes.facecolor"] = "#2E2E2E"
plt.rcParams["figure.facecolor"] = "#2E2E2E"
plt.rcParams["grid.color"] = "gray"
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.edgecolor"] = "#BBBBBB"
plt.rcParams["xtick.color"] = "#DDDDDD"
plt.rcParams["ytick.color"] = "#DDDDDD"
plt.rcParams["text.color"] = "#EEEEEE"
plt.rcParams["axes.labelcolor"] = "#EEEEEE"

plt.figure(figsize=(6,5))
plt.plot(x, y, linestyle="-", label="Adjusted Max HR", color="#C700DA")
plt.plot(x, regression_line, label="Trend", color="#2195C4")
plt.xlabel("Run number")
plt.ylabel("Adjusted max heart rate in bpm")
plt.ylim(-35, 35)
plt.title("Max heart rate progression adjusted for distance & speed \n (actual vs predicted)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()