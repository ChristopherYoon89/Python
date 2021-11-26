import requests
import html2text
import re
import random
import pickle
import csv
import time
from bs4 import BeautifulSoup
from collections import Counter
from textblob import TextBlob
import pandas as pd
from urllib.parse import urlsplit
from urllib.request import urljoin
import urllib.parse
import timeit
from nltk.tag.sequential import ClassifierBasedTagger


# Start time count

start = timeit.default_timer()


# Define some functions that can be reused

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
    filtered_text = re.sub(r'\d', ' ', filtered_text) # remove digits/numbers
    filtered_text = re.sub(r'\s[a-zA-Z]\s+', ' ', filtered_text) # Remove strings with only one character
    filtered_text = re.sub(r'\b\w{1,3}\b', ' ', filtered_text) # Remove strings with less than 4 characters
    filtered_text = re.sub(r'\b\w{17,10000000}\b', ' ', filtered_text) # remove strings larger than 17 characters
    filtered_text = re.sub(r'[^ \nA-Za-z0-9À-ÖØ-öø-ÿЀ-ӿ/]+', ' ', filtered_text) # Enable German characters but remove ASCII symbols
    filtered_text = re.sub(r'\s+', ' ', filtered_text, flags = re.I) # Remove multiple spaces
    filtered_text = re.sub(r'^\s+', '', filtered_text) # Remove spaces at the beginning of string
    filtered_text = re.sub(r'\s+$', '', filtered_text) # Remove spaces at the end of the string
    return filtered_text


class ClassifierBasedGermanTagger(ClassifierBasedTagger):

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


# Load dataset into program and create dataframe with list of urls

df_dataset = pd.read_csv('Dataset_Final_Test.csv', sep=',')

print('\nLoading data into program...')

df_link = pd.DataFrame(df_dataset['Webseite'])


# Load word tagger into program that can classify the words into their word types

with open('nltk_german_classifier_data.pickle', 'rb') as f:
    tagger = pickle.load(f)
    print('\nLoading word tagger into program...')


# Load blacklist into program that should be filtered out from crawled website

stopwords = []

with open('Input_Blacklist.csv', newline='', encoding='utf-8') as inputfile:
    for row in csv.reader(inputfile):
        stopwords.append(row[0])

print(stopwords)


# Create data lists for loop to save crawled text

df_final_top10 = []

df_final_top30 = []

df_final_top50 = []

df_final_top100 = []


# Find all inbound links on start page of firm website

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


## Join relative urls with original website link

        for link in bsObj.findAll('a', href=True):
            if not link.get('href').startswith('http') or not link.get('href').startswith('https'):
                link = urllib.parse.urljoin(url, str(link.get('href')))
                print(link)
                urls.append(link)
            else:
                pass

        print('\n',urls)


## Filter urls and remove links that include to_remove items

        list_links = [line for line in urls if url in line] # Filter those links that include original domain of startpage

        to_remove = ['png','jpg', 'jpeg', 'JPG', 'JPEG', 'PNG', 'mp3', 'mp4', 'pdf', 'mailto', 'tel', 'javascript', 'wmv', 'fileadmin', 'datenschutz', 'privacy', 'agb', 'widerrufsbelehrung', 'impressum', 'kontakt', 'contact']

        list_links = [i for i in list_links if not re.search("|".join(to_remove), i)]

        print(list_links)


## Randomly choose from all links maximum 5 urls plus startpage

        if len(list_links) > 5:
            n = 5
        else:
            n = len(list_links)

        list_links = random.sample(list_links, k=n)
        list_links.append(url)
        print('\n',list_links)

    except Exception as e:
        print(e)


# Loop over the inbound links plus start page and save crawled text to Total_Text list

    Total_text = []

    for url in list_links:

        try:
            page = requests.get(url, time.sleep(1), headers=header, timeout=50)

            if (page.status_code == 404):
                print('Status code: 404 error')
                text_from_html = "404 Fehler"
                Total_text.append(text_from_html)
                break
            else:
                page.encoding
                html_code = page.content

                soup = BeautifulSoup(html_code, 'html.parser')
                page_encoding = soup.original_encoding
                print(page_encoding)

                h = html2text.HTML2Text()
                h.ignore_links = True
                h.ignore_images = True
                text_from_html = h.handle(html_code.decode(page_encoding, 'ignore')) # Handling the HTML code
                text_from_html = text_from_html.replace('\n', ' ') # Replacing next line char
                text_from_html = CleanString(text_from_html)

        except Exception as e:
            print(e)


        # Google language detecter and translater

        
        blob_obj_ger = TextBlob(text_from_html)
        print('\n',blob_obj_ger.detect_language())

        if blob_obj_ger.detect_language() != 'de':
            blob_obj_ger = blob_obj_ger.translate(to='de')
            print('\n Translating... \n')
        else:
            print('\n No translation needed... \n')

        print(blob_obj_ger)


        # Convert string into list, tag words and filter out nouns

        blob_obj_ger = ConvertString(blob_obj_ger)
        print(blob_obj_ger)
        blob_obj_ger = tagger.tag(blob_obj_ger)

        Nomen_tags_NN = [t for t in blob_obj_ger if t[1] == 'NN']
        Nomen_tags_FM = [t for t in blob_obj_ger if t[1] == 'FM']
        Nomen_tags_NE = [t for t in blob_obj_ger if t[1] == 'NE']

        Keywords = Nomen_tags_FM + Nomen_tags_NN + Nomen_tags_NE
        print(Keywords)

        Total_text.extend(Keywords)


    # Remove second column and words from blacklist

    Total_text = [a for a,b in Total_text]
    Total_text = [word for word in Total_text if word not in stopwords]
    print(Total_text)


    # Count the frequency of the keywords / top 100, top 50, top 30, top 10

    Keywords_counted2 = Counter(Total_text)
    print(Keywords_counted2)
    top10 = Keywords_counted2.most_common(10)
    top30 = Keywords_counted2.most_common(30)
    top50 = Keywords_counted2.most_common(50)
    top100 = Keywords_counted2.most_common(100)


    # Remove second column and add them to data lists

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

df.to_csv(r'Test_Run_Crawler.csv', index = False, header=True)
print('Test_Run_Crawler.csv saved')


# Calculate and print processing time

stop = timeit.default_timer()

print('Time: ', stop - start)
