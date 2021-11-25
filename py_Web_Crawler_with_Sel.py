import requests
import html2text
import re
import random
import timeit
import pickle
import csv
import time
from bs4 import BeautifulSoup
from collections import Counter
from textblob import TextBlob
from nltk.tag.sequential import ClassifierBasedTagger
import pandas as pd
from urllib.parse import urlsplit
from urllib.request import urljoin
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# cd C:\Users\yoc.HEROLD\OneDrive - dogado group\Dokumente\Python Developing\Branch Classifyer


# start timer

start = timeit.default_timer()


# Define functions and classes that can be reused

def ConvertString(string):
    '''
    Convert string to list
    '''
    li = list(string.split(' '))
    return li


def ConvertTuple(tup):
    '''
    Convert tuple to string
    '''
    str =  ' '.join(tup)
    return str


def CleanString(text):
    '''
    Use regex to clean crawled text
    '''
    filtered_text = re.sub(r'[^ ]+\.[^ ]+',' ', text) # Remove all strings with url path
    filtered_text = re.sub(r'[^\/]+$',' ', filtered_text) # Remove all strings with slash
    filtered_text = re.sub(r'http://\S+|https://\S+', ' ', filtered_text, flags=re.MULTILINE) # Remove html links
    filtered_text = re.sub(r'^jpg\S+', ' ', filtered_text) # Remove html link trash with jpg strings
    filtered_text = re.sub(r'^com\S+', ' ', filtered_text) # Remove html link trash with com strings
    filtered_text = re.sub(r'\/', ' ', filtered_text) # remove all forward slashes
    filtered_text = re.sub(r'\d', ' ', filtered_text) # remove digits/numbers
    filtered_text = re.sub(r'\s[a-zA-Z]\s+', ' ', filtered_text) # Remove strings with only one character
    filtered_text = re.sub(r'\b\w{1,3}\b', ' ', filtered_text) # Remove strings with less than 4 characters
    filtered_text = re.sub(r'\b\w{17,10000000}\b', ' ', filtered_text) # remove strings larger than 17 characters
    filtered_text = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿЀ-ӿ/]+', ' ', filtered_text) # Enable German characters but remove ASCII symbols
    filtered_text = re.sub(r'\s+', ' ', filtered_text, flags = re.I) # Remove multiple spaces
    filtered_text = re.sub(r'\s+',' ', filtered_text) # Remove extra spaces between words
    filtered_text = re.sub(r'^\s+', '', filtered_text) # Remove spaces at the beginning of string
    filtered_text = re.sub(r'\s+$', '', filtered_text) # Remove spaces at the end of the string
    return filtered_text


class ClassifierBasedGermanTagger(ClassifierBasedTagger):
    '''
    Word tagger for German word based on their word type
    '''
    def feature_detector(self, tokens, index, history):

        word = tokens[index]
        if index == 0: # At the beginning of the sentence
            prevword = prevprevword = None
            prevtag = prevprevtag = None
            #word = word.lower() # Lowercase at the beginning of sentence
        elif index == 1:
            prevword = tokens[index-1] # Note: no lowercase
            prevprevword = None
            prevtag = history[index-1]
            prevprevtag = None
        else:
            prevword = tokens[index-1]
            prevprevword = tokens[index-2]
            prevtag = history[index-1]
            prevprevtag = history[index-2]

        if re.match('[0-9]+([\.,][0-9]*)?|[0-9]*[\.,][0-9]+$', word):
            # Included "," as decimal point
            shape = 'number'
        elif re.compile('\W+$', re.UNICODE).match(word):
            # Included unicode flag
            shape = 'punct'
        elif re.match('([A-ZÄÖÜ]+[a-zäöüß]*-?)+$', word):
            # Included dash for dashed words and umlaute
            shape = 'upcase'
        elif re.match('[a-zäöüß]+', word):
            # Included umlaute
            shape = 'downcase'
        elif re.compile("\w+", re.UNICODE).match(word):
            # Included unicode flag
            shape = 'mixedcase'
        else:
            shape = 'other'

        features = {
            'prevtag': prevtag,
            'prevprevtag': prevprevtag,
            'word': word,
            'word.lower': word.lower(),
            'suffix3': word.lower()[-3:],
            #'suffix2': word.lower()[-2:],
            #'suffix1': word.lower()[-1:],
            'preffix1': word[:1], # included
            'prevprevword': prevprevword,
            'prevword': prevword,
            'prevtag+word': '%s+%s' % (prevtag, word),
            'prevprevtag+word': '%s+%s' % (prevprevtag, word),
            'prevword+word': '%s+%s' % (prevword, word),
            'shape': shape
            }
        return features


# Loading dataset into program and subset list of urls

df_dataset = pd.read_csv('Onlineshop/Dataset_Final_Test.csv', sep=',')

print('\nLoading data into program...')

df_link = pd.DataFrame(df_dataset['Webseite'])


# Load word tagger into program

with open('nltk_german_classifier_data.pickle', 'rb') as f:
    tagger = pickle.load(f)
    print('\nLoading word tagger into program...')


# Load black list of words into program

stopwords = []

with open('Input_Blacklist.csv', newline='', encoding='utf-8') as inputfile:
    for row in csv.reader(inputfile):
        stopwords.append(row[0])

print('\nLoading blacklist into program...')


# Create lists for loop

df_final_top10 = []

df_final_top30 = []

df_final_top50 = []

df_final_top100 = []


# Create instance of webdriver

driver = webdriver.Firefox()


# Find inbound links of startpage and create a list of urls

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

for link in df_link.iterrows():
    url = link[1]['Webseite']

    try:

        html = requests.get(url, time.sleep(1), headers=header, timeout=50, verify=True)
        html_text = html.text
        bsObj = BeautifulSoup(html_text, features='html.parser');
        urls = []

## Find all urls of startpage

        for link in bsObj.findAll('a', href=True):
            if link.get('href') not in urls:
                urls.append(link.get('href'))
            else:
                pass

## Join relative urls and original website link

        for link in bsObj.findAll('a', href=True):
            if not link.get('href').startswith('http') or not link.get('href').startswith('https'):
                link = urllib.parse.urljoin(url, str(link.get('href')))
                print(link)
                urls.append(link)
            else:
                pass

        print('\n',urls)

# Filter urls and remove specific links with items in to_remove list

        list_links = [line for line in urls if url in line] # Filter those links that include original domain of startpage

        to_remove = ['png','jpg', 'jpeg', 'JPG', 'JPEG', 'PNG', 'mp3', 'mp4', 'pdf', 'mailto', 'tel', 'javascript', 'wmv', 'fileadmin', 'datenschutz', 'privacy', 'agb', 'widerrufsbelehrung', 'impressum', 'kontakt', 'contact']

        list_links = [i for i in list_links if not re.search("|".join(to_remove), i)]

        list_links = list(set(list_links))

        print(list_links)

# Randomly choose from all links maximum 5 urls plus startpage

        if len(list_links) > 5:
            n = 5
        else:
            n = len(list_links)

        list_links = random.sample(list_links, k=n)
        list_links.append(url)
        print('\n',list_links)

    except Exception as e:
        print(e)


# Loop through the link list of website

    Total_text = []

    for url in list_links:
        try:
            driver.get(url)
            pagebody = driver.find_element_by_tag_name('body')
            pagetext = pagebody.text
            print(pagetext)
            pagetext = ' '.join(pagetext.split())
        except Exception:
            pagetext = "None"

        try:
            pagetext = CleanString(pagetext)
        except Exception as e:
            print(e)


# Detect language, if not German translate it

        try:
            pagetext = TextBlob(pagetext)
            print('\n',pagetext.detect_language())
            if pagetext.detect_language() != 'de':
                pagetext = pagetext.translate(to='de')
                print('\n Translating... \n')
            else:
                print('\n No translation needed... \n')
        except Exception as e:
            print(e)


# Tag words based on their word type and filter nouns

        try:
            pagetext = ConvertString(pagetext)
            pagetext = tagger.tag(pagetext)
            print(pagetext)

            Nomen_tags_NN = [t for t in pagetext if t[1] == "NN"]
            Nomen_tags_FM = [t for t in pagetext if t[1] == "FM"]
            Nomen_tags_NE = [t for t in pagetext if t[1] == "NE"]

            Keywords = Nomen_tags_FM + Nomen_tags_NN + Nomen_tags_NE

            Total_text.extend(Keywords)
        except Exception as e:
            print(e)


# Remove second column and words from blacklist

    try:
        Total_text = [a for a,b in Total_text]
        Total_text = [word for word in Total_text if word not in stopwords]
        print(Total_text)
    except Exception as e:
        print(e)


# Counter words and extract most frequent words

    try:
        Keywords_counted2 = Counter(Total_text)
        print(Keywords_counted2)
        top10 = Keywords_counted2.most_common(10)
        top30 = Keywords_counted2.most_common(30)
        top50 = Keywords_counted2.most_common(50)
        top100 = Keywords_counted2.most_common(100)
    except Exception as e:
        print(e)


# Remove second column and add them to data lists

    try:
        top10 = [a for a,b in top10]
        mydata_top30 = [a for a,b in top30]
        mydata_top50 = [a for a,b in top50]
        mydata_top100 = [a for a,b in top100]

        endstring_top10 = ConvertTuple(top10)
        print(endstring_top10)
        df_final_top10.append(endstring_top10)

        endstring_top30 = ConvertTuple(mydata_top30)
        print(endstring_top30)
        df_final_top30.append(endstring_top30)

        endstring_top50 = ConvertTuple(mydata_top50)
        print(endstring_top50)
        df_final_top50.append(endstring_top50)

        endstring_top100 = ConvertTuple(mydata_top100)
        print(endstring_top100)
        df_final_top100.append(endstring_top100)

    except Exception as e:
        print(e)


# Convert lists into Pandas dataframes and merge them

df_links_pd = pd.DataFrame(df_link)
df_dataset_pd = pd.DataFrame(df_dataset)

df_total_text_top10 = pd.DataFrame(df_final_top10)
df_total_text_top10.columns = ['Text_Top10']

df_total_text_top30 = pd.DataFrame(df_final_top30)
df_total_text_top30.columns = ['Text_Top30']

df_total_text_top50 = pd.DataFrame(df_final_top50)
df_total_text_top50.columns = ['Text_Top50']

df_total_text_top100 = pd.DataFrame(df_final_top100)
df_total_text_top100.columns = ['Text_Top100']

df = pd.concat([df_dataset_pd, df_total_text_top100, df_total_text_top50, df_total_text_top30, df_total_text_top10], axis=1)


# Save dataframe to csv

df.to_csv(r'Onlineshop/Test_Run_Crawler.csv', index = False, header=True)
print('Test_Run_Crawler.csv saved')


# Calculate and print time

stop = timeit.default_timer()

print('Time: ', stop - start)


# quit webdriver

driver.quit()
