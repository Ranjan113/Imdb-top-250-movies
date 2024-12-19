from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup the ChromeDriver
s = Service('/Users/ranjanmittal/Desktop/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=s)

driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
time.sleep(2)

names = []
genre = []

for i in range(1, 251):

    button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{i}]/div[3]/button')
        )
    )

    driver.execute_script("arguments[0].scrollIntoView();", button)

    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()

    time.sleep(2)  

    movie_title = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/a/h3"))
    ).text

    names.append(movie_title)

    genres = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div/div[1]/div[2]/ul[2]/li"))
    )

    genre_list = [g.text for g in genres]  
    genre.append(genre_list)  

    driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div[1]/button').click()
    time.sleep(2)

df = pd.DataFrame({
    'movie_name':names,
    'genre':genre,
})

df.to_csv('File_path.csv',index=False)

driver.quit()
