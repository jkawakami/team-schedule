import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import time
import re

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
    urlDict = {"MLB" : "https://www.espn.com/mlb/teams",
               "NBA" : "https://www.espn.com/nba/teams",
               "NHL" : "https://www.espn.com/nhl/teams",
               "NFL" : "https://www.espn.com/nfl/teams"}
    return urlDict[sport.upper()]

def hasNewYears(sport):
    overNewYear = ["NBA", "NHL", "NFL"]
    if sport.upper() in overNewYear:
        return True
    else:
        return False
    
def displayYears(sport):
    espnHas2Years = ["NBA", "NHL"]
    if sport.upper() in espnHas2Years:
        return 2
    else:
        return 1

today = date.today()
format_today = today.strftime("%a, %b %d %Y")
print(format_today)

baseURL="https://www.espn.com"
print("MLB, NBA, NHL, or NFL")
sport = input()
URL = getsportURL(sport)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.findAll("h2")
teams = {}
for res in results:
    t = res.contents[0].split(" ")
    if len(t)>3:
        continue
    else:
        teams[res.contents[0]]=res.parent.attrs["href"]

record = displayTeams(teams)
team, teamlink = chooseTeam(record, teams)
schedulelink = teamlink[:10] + 'schedule/' + teamlink[10:]

URL = baseURL+schedulelink
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

#get year/s of sport
results = soup.find("h1", {"class": "headline headline__h1 dib"}).text.strip()
hasNewYear = hasNewYears(sport)
years = displayYears(sport)

if years == 1:
    y = results[-4:]
    z = str(int(y)+1)
elif years == 2:
    y = results[-7:-3]
    z = "20"+results[-2:]

results = soup.find("ul", {"class": "list flex ClubhouseHeader__Record n8 ml4"})
children = results.findChildren("li" , recursive=False)

for res in children:
    print(res.text.strip())

results = soup.findAll("td", string = re.compile('[a-zA-z]{3}.\s[a-zA-z]{3}\s\d+'))
gamesToPrint = 20
curGames = 0
dates = {}
months_master = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
lastMonth = ""
useY = True
if years==1: 
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
        print(sorted(dates))
        for d, r in sorted(dates.items()):
            print(d, r)
if years==2:
    if newdate1 >= today:
                if(curGames < gamesToPrint):
                    #print(res.text.strip()+" "+y + " " +res.next_sibling.text + " " + res.next_sibling.next_sibling.text)
                    curGames+=1
    exit


#iterate through dates and find where today is 