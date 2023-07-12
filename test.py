import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
#driver.get('https://www.rottentomatoes.com/browse/cf-dvd-streaming-all')

driver.get('https://sports.yahoo.com/nba/teams/la-lakers/schedule/?scheduleType=list')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
