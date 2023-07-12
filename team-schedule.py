import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import time
import re
import sys

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

def hasNewYears(sport):
    overNewYear = ["NBA", "NHL", "NFL"]
    if sport.upper() in overNewYear:
        return True
    else:
        return False
    
def displayYears(sport):
    siteHas1Year = ["MLB"]
    if sport.upper() in siteHas1Year:
        return 1
    else:
        return 2

today = date.today()
format_today = today.strftime("%a, %b %d %Y")
print(format_today)

#baseURL="https://www.espn.com"
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

URL = baseURL+teamlink+schedList
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

#get year/s of sport
results = soup.find("div", {"class": "column-header Pb(0)! Fz(12px) My(0px) Pb(0)! Fz(12px) My(0px)"}).text.strip()
#hasNewYear = hasNewYears(sport)
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
results = soup.findAll("tr", {"class": "Bgc(bg-mod) Bgc(secondary):h Pos(r) H(45px) Cur(p)"})
for res in results:
    print("hello")

#what next?
#store each element + edit date ?
#print out all game info into a table?
#html?
#option to only print last x before and next x games after todays date

results = soup.findAll("td", string = re.compile('[a-zA-z]{3}.\s[a-zA-z]{3}\s\d+'))
gamesToPrint = 20
curGames = 0
dates = {}
months_master = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
lastMonth = ""
useY = True

for res in results:
    tempDate = res.text.strip()
    month = [i for i in months_master if i in tempDate.casefold()]
    thisMonth = month[0]
    if(lastMonth == "dec" and thisMonth == "jan"):
        useY = False
    if(lastMonth != thisMonth):
        lastMonth = thisMonth 
    if(useY):
        tempDate = tempDate + " " + y
    else:
        tempDate = tempDate + " " + z

    newdate1 = time.strptime(tempDate, "%a, %b %d %Y")
    dates[newdate1] = res.next_sibling.text + " " + res.next_sibling.next_sibling.text

today = time.strptime(format_today, "%a, %b %d %Y")
for d, r in sorted(dates.items()):
    print(time.strftime('%a, %b %d %Y', d), r)
    #if(d >= today):
                
                
if years==2:
    if newdate1 >= today:
                if(curGames < gamesToPrint):
                    #print(res.text.strip()+" "+y + " " +res.next_sibling.text + " " + res.next_sibling.next_sibling.text)
                    curGames+=1
    exit


#iterate through dates and find where today is 