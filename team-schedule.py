import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import datetime
import time
import re
import sys
import queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

def displayTeams(dict):
    counter = 0
    record = {}
    for team in sorted(dict):
        counter += 1
        record[counter] = team
        print("%s. %s" % (counter, team))
    return record

def chooseTeam(record, teams):
    print("\nPick a number:")
    num = input()
    num = int(num)
    if num in record:        
        print(record[num]+"\n")
        return record[num], teams[record[num]]
    
def getsportURL(sport):
    urlDict = {"MLB" : "https://sports.yahoo.com/mlb/teams",
               "NBA" : "https://sports.yahoo.com/nba/teams",
               "NHL" : "https://sports.yahoo.com/nhl/teams",
               "NFL" : "https://sports.yahoo.com/nfl/teams"}
    return urlDict[sport.upper()]
    
def displayYears(sport):
    siteHas1Year = ["MLB"]
    if sport.upper() in siteHas1Year:
        return 1
    else:
        return 2

today = date.today()
format_today = today.strftime("%a, %b %d %Y")
print(format_today)

baseURL="https://sports.yahoo.com"
print("MLB, NBA, NHL, or NFL")
sport = input()
URL = getsportURL(sport)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#get all teams
results = soup.findAll("a", {"class": "D(ib) C(primary-text) C(primary-text):link C(primary-text):visited Fz(13px) Maw(200px) Ell"})

teams = {}
for res in results:
    if res.next_element.name == 'img':
        continue
    teams[res.text.strip()]=res.find_next('a').attrs["href"]

record = displayTeams(teams)
team, teamlink = chooseTeam(record, teams)
schedulelink = teamlink[:10] + 'schedule/' + teamlink[10:]
schedList = "/?scheduleType=list"

start_time = time.time()

URL = baseURL+teamlink+schedList
#page = requests.get(URL)
driver.get(URL)
page = driver.page_source
soup = BeautifulSoup(page, "html.parser")

#get year/s of sport
results = soup.find("div", {"class": "column-header Pb(0)! Fz(12px) My(0px) Pb(0)! Fz(12px) My(0px)"}).text.strip()
years = displayYears(sport)

if years == 1:
    y = results[-4:]
    z = str(int(y)+1)
elif years == 2:
    y = results[-9:-5]
    z = results[-4:]

#print record of team
results = soup.find("div", {"class": "C(#888)"})
print(results.text.strip())

#get all game rows
#javascript
gameInfo = []
months_master = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
lastMonth = ""
firstYear = True

results = soup.findAll("tr", {"class": "Bgc(bg-mod) Bgc(secondary):h Pos(r) H(45px) Cur(p)"})
for res in results:
    game = []
    for r in res:
        txt = r.text.strip()
        d = re.match('[a-zA-z]{3}.\s[a-zA-z]{3}\s\d+',txt)        
        if(d):
            before = txt[d.start():d.end()]
            after = txt[d.end():]
            month = [i for i in months_master if i in txt.casefold()]
            thisMonth = month[0]
            if(lastMonth != thisMonth):
                if(lastMonth == "dec" and thisMonth == "jan"):
                    firstYear = False
                lastMonth = thisMonth 
            if(firstYear):
                tempDate = before + " " + y
            else:
                tempDate = before + " " + z
            game.append(tempDate)
            if(len(after) != 0):
                game.append(after)
            continue
        m = re.search('\d{1,3}-\d{1,3}$', txt)
        if(m):
            start = m.start()
            game.append(txt[0:start])
            continue
        game.append(r.text.strip())
    gameInfo.append(game)

amount = 10
q1 = queue.Queue(amount)
q2 = queue.Queue(amount)

for game in gameInfo:
    g = datetime.strptime(game[0], "%a, %b %d %Y").date()
    if(today >= g):
        if not (q1.full()):
            q1.put(game)
        else: 
            q1.get()
            q1.put(game)
    else:
        if not (q2.full()):
            q2.put(game)
        else:
            break

print("Last "+str(amount)+" games:")
for q in q1.queue:
    print(*q)

print("Next "+str(amount)+" games:")
for q in q2.queue:
    print(*q)

print("--- %s seconds ---" % (time.time() - start_time))
#sys.exit()
