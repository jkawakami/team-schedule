import requests
from bs4 import BeautifulSoup
from datetime import date

def displayTeams(dict):
    counter = 0
    record = {}
    for team in dict:
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

today = date.today()
format_today = today.strftime("%a, %b %d")

baseURL="https://www.espn.com"
MLB="https://www.espn.com/mlb/teams"
page = requests.get(MLB)
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
results = soup.find("td", string=format_today)
if results is None:
    print(team," zilch")
else:
    print(team," plays today, " + results.text.strip() + " " + results.next_sibling.text)


