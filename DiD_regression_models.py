import pandas as pd
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt


# Load dataset into Python console

mydata = pd.read_excel("Dataset.xlsx")


# Check columns/variables

pd.set_option("display.max_columns", None)

for col in mydata.columns:
    print(col)
  

# Create scatterplot matrix

vars_for_plot = [
    "var1", "var2", "var3", "var4", 
    "var5", "var6", "var7", "var8", "var9"
]

g = sns.PairGrid(mydata[vars_for_plot])
g.map_upper(sns.scatterplot, color="blue")
g.map_lower(sns.scatterplot, color="blue")

for i in range(len(vars_for_plot)):
    ax = g.axes[i, i]
    ax.set_frame_on(True)   
    ax.set_xticks([]) 
    ax.set_yticks([])

for ax in g.axes[:, 0]:
    ax.set_ylabel(ax.get_ylabel(), rotation=0, ha='right', va='center')

for ax in g.axes[-1, :]:
    ax.set_xlabel(ax.get_xlabel(), rotation=45, ha='right')

for i in range(len(vars_for_plot)):
    for j in range(len(vars_for_plot)):
        g.axes[i, j].tick_params(left=False, bottom=False)

plt.tight_layout()
plt.show()


# Implement regression model 

# Transform into long format, prepare variables, dummies and interaction term

mydata = pd.read_excel("Mydata.xlsx")

value_vars_score = ['Overall_Score_IT', 'Overall_Score_P1', 'Overall_Score_P2']
value_vars_bmi = ['bmi_it', 'BMI_P1', 'BMI_P2']

score_long = pd.melt(mydata, id_vars=['ID'], value_vars=value_vars_score, var_name='Time', value_name='Overall_Score')
bmi_long = pd.melt(mydata, id_vars=['ID'], value_vars=value_vars_bmi, var_name='Time', value_name='BMI')

score_long['Time'] = score_long['Time'].str.replace('Overall_Score_', '')
bmi_long['Time'] = bmi_long['Time'].str.replace('BMI_', '')

mydata_long = pd.merge(score_long, bmi_long, on=['ID', 'Time'], how='inner')

mydata_long['Time_Num'] = mydata_long['Time'].map({'IT': 0, 'P1': 1, 'P2': 2})

static_vars = ['id', 'group', 'control_var1', 'control_var2', 'control_var3']

mydata_long = mydata_long.merge(mydata[static_vars].drop_duplicates(subset=['ID']), on='ID', how='left')

mydata_long['Post_P1'] = (mydata_long['Time'] == 'P1').astype(int)
mydata_long['Post_P2'] = (mydata_long['Time'] == 'P2').astype(int)

mydata_long['DiD_P1'] = mydata_long['Post_P1'] * mydata_long['Gruppe']
mydata_long['DiD_P2'] = mydata_long['Post_P2'] * mydata_long['Gruppe']


# Model 1

model_1 = smf.ols('Total_Points ~ C(Time) + Gruppe + C(Time):Gruppe', data=mydata_long[mydata_long['Time'] != 'P2']).fit()
print(model_1.summary())

# Model 2 

model_2 = smf.ols('Total_Points ~ C(Time) + Gruppe + C(Time):Gruppe + controL_var2 + controL_var2 + controL_var3', data=mydata_long[mydata_long['Time'] != 'P2']).fit()
print(model_2.summary())

# Model 3

model_3 = smf.ols('Total_Points ~ C(Time) + Gruppe + C(Time):Gruppe', data=mydata_long[mydata_long['Time'] != 'IT']).fit()
print(model_3.summary())

# Model 5

model_5 = smf.ols('Total_Points ~ C(Time) + Gruppe + C(Time):Gruppe', data=mydata_long[mydata_long['Time'] != 'P1']).fit()
print(model_5.summary())


# Dynamic DiD Regression Model 7

mydata_long["Time"] = pd.Categorical(mydata_long["Time"], categories=["IT", "P1", "P2"], ordered=True)
mydata_long["P1_Treat"] = ((mydata_long["Time"] == "P1") & (mydata_long["Gruppe"] == "intervention group")).astype(int)
mydata_long["P2_Treat"] = ((mydata_long["Time"] == "P2") & (mydata_long["Gruppe"] == "intervention group")).astype(int)

model_7 = smf.ols('Total_Points ~ C(Time) + Gruppe + P1_Treat + P2_Treat', data=mydata_long).fit()
print(model_7.summary())

# Dynamic regression model # 8

model_8 = smf.ols('Total_Points ~ C(Time) + Gruppe + P1_Treat + P2_Treat + var1 + var2 + var3', data=mydata_long).fit()
print(model_8.summary())
