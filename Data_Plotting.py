import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


mydata = pd.read_csv('TestData.csv', error_bad_lines=False)


# Plot bar chart

prf1 = mydata[('Performance')]

prf1 = pd.DataFrame(prf1)

prf1.columns = ['Performance']

my_colors = ['red', 'blue']

ax = plt.gca()

prf1.groupby('Performance').Performance.count().plot.bar(color=my_colors, width=0.3)
plt.rcParams['figure.figsize'] = (6,5)
#plt.plot(default_x_ticks, df_count)
plt.title('Performance Analysis Test')
plt.ylabel('Frequency')
plt.xlabel('')
plt.xticks(rotation=0)
plt.bar_label(ax.containers[0])
plt.show()


# Counting categories and plot bar chart

df_class = mydata[('Predicted_Class')]

df_class = pd.DataFrame(df_class)

df_class.columns = ['Class']

df_count = df_class.groupby('Class').Class.count().reset_index(name="Count")

df_count_sorted = df_count.sort_values(by="Count", ascending=True)

categories = df_count_sorted['Class']

default_x_ticks = range(len(df_count_sorted))

df_count = df_count_sorted['Count']

mycolor = ['steelblue']

df_count_sorted.plot.barh(color=mycolor, legend=None)
plt.rcParams['figure.figsize'] = (6,5)
#plt.plot(default_x_ticks, df_count)
plt.title('Frequency of classes')
plt.xlabel('Frequency')
plt.yticks(default_x_ticks, categories, fontsize=8)

#plt.yticks(rotation=45, ha='right')

plt.show()


# Count values within certain ranges for TRUE Values

df_acc = pd.DataFrame(mydata)
#bins = [0,35,65,100]
bins = [0,25,55,100]

df_clean = df_acc.loc[df_acc.Perf_1st] # filter true values

df_clean = pd.DataFrame(df_clean)

my_colors = ['red', 'yellow', 'green']

positions = (0, 1, 2)
# positions = list(range(0,3))
#x_labels = ['<35 %', '35-65 %', '>65 %']
x_labels = ['<25 %', '25-55 %', '>55 %']

ax = plt.gca()

df_clean['Prob_1st'].value_counts(bins=bins, sort=False).plot.bar(color=my_colors, width=0.5)
plt.rcParams['figure.figsize'] = (6,5)
plt.xticks(positions, x_labels, rotation=0) #,ha='right')
plt.bar_label(ax.containers[0])
plt.title('Frequencies of probability ranges of correct classifications (n=96)')
plt.xlabel('Probability ranges')
plt.ylabel('Frequency')
#plt.figtext(.1, .1, "T = 4K")
#plt.grid(color='grey', linestyle='--', linewidth=1, axis='both', alpha=0.2)
plt.show()


# Count values within certain ranges for FALSE Values

df_clean2 = df_acc.loc[~df_acc.Perf_1st] # filter false values

df_clean2 = pd.DataFrame(df_clean2)

my_colors = ['red', 'yellow', 'green']

positions = (0, 1, 2)
# positions = list(range(0,3))
x_labels = ['<25 %', '25-55 %', '>55 %']

ax = plt.gca()

df_clean2['Prob_1st'].value_counts(bins=bins, sort=False).plot.bar(color=my_colors, width=0.5)
plt.rcParams['figure.figsize'] = (6,5)
plt.xticks(positions, x_labels, rotation=0) #,ha='right')
plt.bar_label(ax.containers[0])
plt.title('Frequencies of probability ranges of incorrect classifications (n=31)')
plt.xlabel('Probability ranges')
plt.ylabel('Frequency')
plt.ylim(0, 35)
#plt.figtext(.1, .1, "T = 4K")
#plt.grid(color='grey', linestyle='--', linewidth=1, axis='both', alpha=0.2)
plt.show()


# Curve Variablenverteilung

mydata = pd.read_csv('Variable_nach_häufigkeit_aggregriert.csv')
df_anzahl = mydata['Anzahl']
df_anzahl = pd.DataFrame(df_anzahl)

plt.rcParams['figure.figsize'] = (6,5)
plt.plot(df_anzahl, color='blue')
plt.xlabel('Kategorien')
plt.ylabel('Frequency')
plt.title('Häufigkeit von Kategorien')
plt.show()


## Plot top 500 Herold Branchen

df_top500 = mydata.head(500)

df_anzahl_500 = df_top500['Anzahl']

plt.rcParams['figure.figsize'] = (6,5)
plt.plot(df_anzahl_500, color='blue')
plt.xlabel('Kategorien')
plt.ylabel('Frequency')
plt.title('Häufigkeit von Top 500 Kategorien')
plt.show()


## Plot WKO Branchenverteilung

mydata = pd.read_csv('Kategorien_Aggregiert.csv')

df_anzahl = mydata['Anzahl']

df_anzahl2 = pd.DataFrame(df_anzahl2)

df_anzahl_sort = df_anzahl2.sort_values('Anzahl', ascending=False)

df_anzahl_sort2 = df_anzahl_sort.reset_index()

plt.rcParams['figure.figsize'] = (6,5)
plt.plot(df_anzahl_sort2['Anzahl'], color='red')
plt.xlabel('Kategorien')
plt.ylabel('Frequency')
plt.title('Häufigkeit von Kategorien')
plt.show()


## Plot Top 500 Kategorien

df_anzahl2 = df_anzahl['Anzahl']

df_anzahl2 = pd.DataFrame(df_anzahl2)

df_anzahl_sort = df_anzahl2.sort_values('Anzahl', ascending=False)

df_anzahl_sort2 = df_anzahl_sort.reset_index()

df_top500 = mydata.head(500)

plt.rcParams['figure.figsize'] = (6,5)
plt.plot(df_top500['Anzahl'], color='red')
plt.xlabel('Kategorien')
plt.ylabel('Frequency')
plt.title('Häufigkeit der Top 500 Kategorien')
plt.show()


# Word Cloud

from wordcloud import WordCloud

mydata = pd.read_csv('Google_Analytics.csv')

mydata200 = mydata.head(400)

mydata_dict = dict(zip(mydata200['SearchTerm'].tolist(), mydata200['Views'].tolist()))

wordcloud = WordCloud(width = 800, height = 800, colormap='inferno', mode='RGBA' min_font_size = 10, max_words=400).generate_from_frequencies(mydata_dict)
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


# Calculate growth rate from probabilities_1st_class to probababilities_3rd_class

df_mydata = pd.DataFrame(mydata)

df_true = df_mydata.loc[df_mydata.Performance_1st_Class] # Filter true values

df_false = df_mydata.loc[~df_mydata.Performance_1st_Class] # Filter false values

df_true_25 = df_true[(df_true['Probabilities_1st_Class'] < 25)] # Filter true rows with lower than 25 % in column Probabilities 1st Class
df_false_25 = df_false[(df_false['Probabilities_1st_Class'] < 25)] # Filter false rows with lower than 25 % in column Probabilities 1st Class


# Save dataframe as csv File

df_empty.to_csv(r'Output_Text_Top100_50_30_10_Empty.csv', index = False, header=True)

