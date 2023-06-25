import requests
from bs4 import BeautifulSoup
from datetime import date
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
        print(record[num])
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
format_today = today.strftime("%a, %b %d")

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
twoyears = False
hasNewYear = hasNewYears(sport)
if hasNewYear:
    years = displayYears(sport)
    if years == 1:
        y = results[-4:]
    elif years == 2:
        twoyears = True
        y = results[-5:-3]
        z = results[-2:]



results = soup.findAll("td", text = re.compile('[a-zA-z]{3}.\s[a-zA-z]{3}\s\d+'))
for res in results:
    #get all dates, append year to it
    if years==1:
        print(res.text.strip()+" "+y)
    #print(res.next_sibling.text)


#iterate through dates and find where today is 