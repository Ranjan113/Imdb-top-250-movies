# This code scraps all the data except genre


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

s = Service('/Users/ranjanmittal/Desktop/chromedriver-mac-arm64/chromedriver')

driver = webdriver.Chrome(service=s)

driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
time.sleep(2)

driver.find_element(by=By.XPATH,value='//*[@id="list-view-option-detailed"]').click()
time.sleep(2)

html_content = driver.page_source

soup = BeautifulSoup(html_content,'html.parser')

container = soup.find_all('div',{'class':'sc-2bfd043a-3 jpWwpQ dli-parent'})

names = []
year = []
time = []
rating=[]
imdb_rating=[]
plot = []
all_directors = []
all_stars = []

for i in container:

    try:
        names.append(i.find('a',{'class':'ipc-title-link-wrapper'}).text)
    except:
        names.append(np.nan)

    x = i.find('div',{'class':'sc-300a8231-6 dBUjvq dli-title-metadata'}).find_all('span')
    try:
        year.append(x[0].text)
    except:
        year.append(np.nan)
    try:
        time.append(x[1].text)
    except:
        time.append(np.nan)
    try:
        rating.append(x[2].text)
    except:
        rating.append(np.nan)


    try:
        imdb_rating.append(i.find('span',{'class':'ipc-rating-star--rating'}).text)
    except:
        imdb_rating.append(np.nan)
    try:
        plot.append(i.find('div',{'class':'ipc-html-content-inner-div'}).text)
    except:
        plot.append(np.nan)

    directors = []
    stars = []

    for span in i.find_all('span', {'class': 'sc-2bfd043a-5 fIttnm'}):
        link = span.find('a')
        if 'dli-director-item' in link['class']:
            try:
                directors.append(link.text)
            except:
                directors.append(np.nan)
        elif 'dli-cast-item' in link['class']:
            try:
                stars.append(link.text)
            except:
                stars.append(np.nan)

    all_directors.append(directors)
    all_stars.append(stars)


df = pd.DataFrame({
    'movie_name':names,
    'year_of_release':year,
    'duration':time,
    'content_rating':rating,
    'IMDb_score':imdb_rating,
    'Plot':plot,
    'directors':all_directors,
    'cast':all_stars,
})

df.to_csv('/Users/ranjanmittal/Desktop/data/Imdb.csv',index=False)
