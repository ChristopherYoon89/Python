import pandas as pd


# cd C:\Users\yoc.HEROLD\OneDrive - dogado group\Dokumente\Developing\Python\Data Analysis

# Read csv into program

mydata = pd.read_csv('Test_Oleksander/Output_Test_Oleksander_Duplicates_Dropped.csv', error_bad_lines=False, encoding='utf-8')



# Convert data into pd dataframe

df_mydata = pd.DataFrame(mydata)



# Drop duplicates of a dataset

mydata.drop_duplicates(subset=['Text_Top100'], inplace=True, keep='first')



# Store duplicates into separate dataframe

mydata['Duplicates'] = mydata.duplicated(subset='Website_Text')

mydata_duplicates = mydata.loc[mydata['Duplicates'].isin([True])]



# Filter rows with certain value in column

mydata_true = mydata.loc[mydata['Performance'].isin(['Category X'])]


y_true = mydata.loc[mydata['Performance'].isin([True])]


# Drop rows with empty values

mydata.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)



# Drop rows with empty cells in specific columns

mydata.dropna(subset = ['ZTK_TELEFONNR'], inplace=True)



# Filter rows with empty cells/no values and store them into separate dataframe

df_empty = mydata[mydata['Text_Top50'].isnull()]



# Drop rows with certain value in specific column

# Variante 1

mydata.drop(mydata.index[mydata['myvar'] == 'specific_name'], inplace = True)

# Variante 2

mydata = mydata[~mydata['Class'].isin(['Class_18_Handel', 'Class_7_Chemikalien_Kosmetik_Kunststoff_Gummi', 'Class_19_Forschung_Entwicklung'])]



# Drop columns

columns = ['Webseite', 'Branche']

mydata = mydata.drop(columns, axis=1)



# Create a sample of n rows of total dataset

## Variante 1

df_sample = mydata.sample(n=350)


## Variante 2

import random

n=200

list_links = random.sample(list(df_new_links.Domain), k=n)



# Create a sample with specific length per category

mydata = mydata.groupby('Class').apply(lambda s: s.sample(min(len(s), 500)))



# Sort values by a specific column

df_sorted = mydata.sort_values('Website', ascending=True)



# Remove spaces in specific column

mydata['Performance_1st_Class'] = mydata['Performance_1st_Class'].str.replace(' ','')



# Replace empty cells with NaN

nan_value = float("NaN")

mydata.replace('', nan_value, inplace=True)



# Split column by symbol

mydata_final[['Predicted_Class','Probability']] = mydata_final['0'].str.split(n=1, expand=True)



# Extract domain from URL

from urllib.parse import urlparse

mydata = pd.read_csv('Predicted_07.09.2021.csv', error_bad_lines=False)

df_link = mydata['URL']

df_link = pd.DataFrame(df_link)

df_extracted = []

for link in df_link.iterrows():
    url = link[1]['URL']
    domain = urlparse(url).netloc
    df_extracted.append(domain)

df_extracted = pd.DataFrame(df_extracted)
df_extracted.columns = ['Domain']

df_final = pd.concat([mydata, df_extracted], axis=1)



# Select rows that include string 'http' in column 'domain'

new_links = mydata[mydata['Domain'].str.contains('http')] # Select rows that include string 'http' in Column Domain



# Split dataset into train and test datset

## Variante 1

from sklearn import model_selection

dtf_train, dtf_test = model_selection.train_test_split(mydata, test_size=0.1)


## Variante 2

train = mydata.sample(frac=0.9, random_state=200) #random state is a seed value

test = mydata.drop(train.index)



# Split dataframe by rownumbers (all columns)

mydata_new = mydata.iloc[:1000,:]



# String matching by using fuzzywuzzy

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

mydata2 = pd.read_csv('VBR_Branchen_storniert.csv')

df1 = pd.DataFrame(mydata['VBR_BRANCHENBEZ_storniert'])

mydata2 = pd.read_csv('VBR_Branchen_nicht_storniert.csv')

df2 = pd.DataFrame(mydata2['VBR'])


## Variante 1: extract only one match

df1['Match_storniert'] = df1['VBR_BRANCHENBEZ_storniert'].apply(lambda x: process.extractOne(x, df2['VBR'].to_list(),score_cutoff=90))

df2['Match_storniert'] = df2['VBR'].apply(lambda x: process.extractOne(x, df1['VBR_BRANCHENBEZ_storniert'].to_list(),score_cutoff=90))


## Variante 2: extract n number of matches

df1['Match_storniert'] = df1['VBR_BRANCHENBEZ_storniert'].apply(lambda x: process.extract(x, df2['VBR'].to_list(), limit=3))



# String matching by using own function (Only possible when searching for exact matches)

mydata = pd.read_csv('VBR_Branchen3.csv')

df_vbr = pd.DataFrame(mydata['VBR_BRANCHENBEZ_storniert'])

mydata2 = pd.read_csv('Abgleich_Tranche1_Bettina.csv')

df_entity = pd.DataFrame(mydata2['VBR'])

def lookup_prod(ip):
    for row in df_vbr.itertuples():
        if ip in str(row.VBR_BRANCHENBEZ_storniert):
            return row.VBR_BRANCHENBEZ_storniert
    else:
        return 'N/A'


df_entity['Match_storniert'] = df_entity['VBR'].apply(lookup_prod)



# Check whether values in two separate columns are equal or not

def Check(mydata):
   if mydata['Original_Class']== mydata['Class']:
      return "True"
   else:
      return "False"

mydata['ColumnCheck'] = mydata.apply(Check, axis=1)

df_clean_true = mydata.loc[mydata['ColumnCheck'] == 'True']

df_clean_false = mydata.loc[mydata['ColumnCheck'] == 'False']



# Save dataframe

## to csv

mydata.to_csv(r'Test/Output_Test_Duplicates_Dropped_Cleaned.csv', index = False, header=True)

## to excel

mydata.to_excel("output.xlsx", sheet_name='Sheet_name_1')
