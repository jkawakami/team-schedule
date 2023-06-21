import requests
from bs4 import BeautifulSoup
from datetime import date
import yagmail

today = date.today()
format_today = today.strftime("%a, %b %d")

team = input("Enter Team: ")
if team == "UCLA" or team=="ucla":
    URL = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/26/ucla-bruins"
elif team == "dodgers" or team=="Dodgers":
    URL = "https://www.espn.com/mlb/team/schedule/_/name/lad/los-angeles-dodgers"
#URL = "https://realpython.github.io/fake-jobs/"


page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("td", string=format_today)
#results = soup.find("td", string="asdf")
if results is None:
    print(team," doesn't play today")
else:
    print(team," plays today, " + results.text.strip() + " " + results.next_sibling.text)

sender = 'jameslkawakami@gmail.com'
receivers = ['jameslkawakami@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

""" try:
    #initializing the server connection
    yag = yagmail.SMTP("jameslkawakami@gmail.com", oauth2_file="credentials.json")

    #yag = yagmail.SMTP(user='jameslkawakami@gmail.com', password='1logintoGoogle1!')
    #sending the email
    yag.send(to='jameslkawakami@gmail.com', subject='Testing Yagmail', contents='Hooray, it worked!')
    print("Email sent successfully")
except:
    print("Error, email was not sent") """