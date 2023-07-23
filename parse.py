from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


def parse(url, count, filename):
    count = int(count/3)
    workbook = Workbook()
    ws = workbook.active
    ws.append(['View', 'Title', 'Time', 'Ago', 'Link', 'Image'])
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get(url)
    driver.implicitly_wait(20)
    for i in range(0, count):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        driver.implicitly_wait(10)
    driver.implicitly_wait(60)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('ytd-rich-grid-row', class_='style-scope ytd-rich-grid-renderer')
    for i in items:
        view = i.find('span', class_='inline-metadata-item style-scope ytd-video-meta-block').text
        title = i.find('a', {'id': 'video-title-link'})['title']
        time = i.find('span', class_='ytd-thumbnail-overlay-time-status-renderer').text
        ago = i.find_all("span", {"class": "inline-metadata-item style-scope ytd-video-meta-block"})[1].text
        link = 'https://youtube.com' + i.find('a', {'id': 'video-title-link'})['href']
        img = i.find('yt-image', class_='style-scope ytd-thumbnail').find('img')['src']
        All = view, title, time, ago, link, img
        ws.append(All)
    workbook.save(f'{filename}.xlsx')
