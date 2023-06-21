import requests
from bs4 import BeautifulSoup
from datetime import date

today = date.today()
format_today = today.strftime("%a, %b %d")

MLB="https://www.espn.com/mlb/teams"
page = requests.get(MLB)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("h2")
t = results.contents[0].split(" ")
teams = []
i=0
while i<30:
    results = results.find_next('h2')
    t = results.contents[0].split(" ")
    if len(t)>3:
        break
    else:
        teams.append(results.contents[0])
    
    i+=1

print(teams)

team = input("Enter Team: ")
if team == "UCLA" or team=="ucla":
    URL = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/26/ucla-bruins"
elif team == "dodgers" or team=="Dodgers":
    URL = "https://www.espn.com/mlb/team/schedule/_/name/lad/los-angeles-dodgers"
#URL = "https://realpython.github.io/fake-jobs/"


page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("td", string=format_today)
if results is None:
    print(team," doesn't play today")
else:
    print(team," plays today, " + results.text.strip() + " " + results.next_sibling.text)


