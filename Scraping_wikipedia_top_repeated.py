# Scraping twenty words form wikipedia articles
# and get their frequency percentage
# with highest repeating so its applications are
# recommender systems , chatbots and NLP, sentiment analysis
# data visualization
# market research

# Importing the libraries

# Beautifullsoup is used to scrap words
from bs4 import BeautifulSoup
# Request is used to request to request server for the
# for pulling and pushing and authenticating the data

import requests

# Regular expression operations
# special text string for describing a search pattern.
# find and replace
import re
# Parses json and formats it
import  json
# provides the arithmetic operation capabilities
import operator

# representing the data as in table form

from tabulate import  tabulate
# for system calls
import sys

# list of commong stop words various languages like the
from stop_words import get_stop_words

#  get the words

def getWordlist(url):
    word_list = []
    # raw data
    source_code = requests.get(url)
    # convert to text
    plain_text = source_code.text
    # lXML format
    soup = BeautifulSoup(plain_text, 'lxml')

    # find the words in paragraph tag

    for text in soup.find_all('p'):
        if(text.text is None):
            continue
        #content
        content = text.text
        # lower case and split an array
        words = content.lower().split()

        # for each word
        for word in words:
            # remove non-chars
            cleaned_word = clean_word(word)
            #if there is still something there
            if len(cleaned_word)>0 :
                # add it to the word_list
                word_list.append(cleaned_word)

    return word_list

def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+','',word)
    return cleaned_word

def createFrequencyTable(word_list):
    #word count
    word_count = {}
    for word in word_list:
        #index is the word
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

# remove step words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key,value])
    return temp_list

# access wiki API.json format for quering the data
wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"

# if the search word is too small, throw error
if(len(sys.argv) < 2):
    print("Enter valid string")
    exit()

# get the search word
string_query = sys.argv[1]

# to remove stop words or not
if(len(sys.argv)>2):
    search_mode = True
else:
    search_mode = False

# create our URL
url = wikipedia_api_link + string_query

# try-except block. simple way to deal with exceptions
# great for HTTP requests

try:
    # use requests to revive raw0 data from wiki API URL we
     response = requests.get(url)
     # format that data as a JSON directory
     data = json.loads(response.content.decode("utf-8"))
    # page title , first option
    # show this web broser
     wikipedia_page_tag = data['query']['search'][0]['title']

    # get actual wiki page based on retrived title
     url = wikipedia_link+ wikipedia_page_tag
    # get list of words from that page
     page_word_list = getWordlist(url)
    # create table of words count , dictionary
     page_word_count = createFrequencyTable(page_word_list)
    # sort the table by the frequency count
     sorted_word_frequency_list = sorted(page_word_count.items(),key = operator.itemgetter(1), reverse = True)
    # remove stop words if the user specified

     if search_mode:
        sortes_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    # sum the total words to calculating the frequency
     total_words_sum =0
     for key,value in sorted_word_frequency_list:
        total_words_sum = total_words_sum +value

    # getting the top 20 words
     if len(sorted_word_frequency_list)>20:
        sorted_word_frequency_list = sorted_word_frequency_list[:20]


    # create our final talble contain words , frequency and word count, precentage
     final_list = []
     for key,value in sorted_word_frequency_list:
        percentage_value = float(value*100)/total_words_sum
        final_list.append([key,value,round(percentage_value,4)])

      # getting header for the table
     print_headers = ['Word','Frequency','Frequency Percentage']

      # print the table with tabulate
     print(tabulate(final_list,headers=print_headers,tablefmt = 'orgtbl'))

# add an exception in case if the code breaks
except requests.exception.Timeout:
      print('The server did not  respond.Please, try again later')

