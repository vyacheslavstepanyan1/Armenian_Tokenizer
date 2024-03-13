# Import dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import time

# Retrieve a random armenian wikipedia page
def get_randomwiki():
    url = r'https://hy.wikipedia.org/wiki/%D5%8D%D5%BA%D5%A1%D5%BD%D5%A1%D6%80%D5%AF%D5%B8%D5%B2:%D5%8A%D5%A1%D5%BF%D5%A1%D5%B0%D5%A1%D5%AF%D5%A1%D5%B6%D5%A7%D5%BB'
    response = requests.get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    return page

# Extract all body texts
def get_wikitext(page):
    arm_txt = ''
    a = page.find_all('p')
    text = ''
    for i in a:
        if str(i.parent).startswith('<div') or str(i.parent).startswith('<met'): # to avoid retrieving text from tables etc.
            arm_txt += i.text
    return arm_txt

def get_wikititle(page):
    return page.find('span', class_="mw-page-title-main").text

# Define a function to clean the text from non armenian words and wiki hyperlinks
def clean_text(text):
    pattern1 = r'[^\u0531-\u0587\u0589 \u0530-\u058F \,\.\:\!\;\=\+\-\_\/\\\*\&\%\$\#\@\'\(\)\[\]\{\}\<\>\|\~\" 1-9]'
    text = re.sub(pattern1, '', text)
    
    text = re.sub(r'\s+', ' ', text).strip()

    pattern2 = r'\s+:'
    text = re.sub(pattern2, ':', text)

    pattern3 = r'\[\d+\]|\(\d+\)'
    text = re.sub(pattern3, '', text)

    return text

# Create the dataframe
def make_dataframe(char_limit):
    assert char_limit > 0, "Limit must be greater than 0!"
    texts = []
    titles = []
    text_lengths = []
    while True:
        try:
            page = get_randomwiki()
            texts.append(clean_text(get_wikitext(page)))
            titles.append(get_wikititle(page))
            text_lengths.append(len(texts[-1]))
            time.sleep(2)
        except AttributeError:
            continue
        if sum(text_lengths) > char_limit:
            break
    df = pd.DataFrame({'title':titles, 'text': texts, 'length':text_lengths})
    return df