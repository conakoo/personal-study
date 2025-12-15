"""scrape.py

Web scrapping script to ingest and transform the data
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def league_table():
    url = "https://www.bbc.com/sport/football/premier-league/table"
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table", attrs={"data-testid": "football-table"})

    for i in table.find_all("th"):
        title = i.text
        headers.append(title)
    league_table = pd.DataFrame(columns=headers)
    for j in table.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [i.text for i in row_data]
        length = len(league_table)
        league_table.loc[length] = row
    league_table.drop(["Form, Last 6 games, Oldest first"], axis=1, inplace=True)
    return league_table


def top_scorers():
    url = "https://www.bbc.com/sport/football/premier-league/top-scorers"
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table", attrs={"data-testid": "sport-table"})

    for i in table.find_all("th"):
        title = i.text
        headers.append(title)
    top_scorers = pd.DataFrame(columns=headers)
    for j in table.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [i.text for i in row_data]
        length = len(top_scorers)
        top_scorers.loc[length] = row

    top_scorers.Name = top_scorers.Name.replace(
        r"([A-Z])", r" \1", regex=True
    ).str.split()
    top_scorers.Name = top_scorers.Name.apply(
        lambda x: " ".join(dict.fromkeys(x).keys())
    )

    top_scorers["Club"] = top_scorers.Name.str.split().str[2:].str.join(" ")
    top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(" ")
    col = top_scorers.pop("Club")
    top_scorers.insert(2, "Club", col)
    top_scorers.Club = top_scorers.Club.apply(
        lambda x: "Manchester City" if "Manchester City" in x else x
    )
    top_scorers.Club = top_scorers.Club.apply(
        lambda x: "Manchester United" if "Manchester United" in x else x
    )
    top_scorers.Club = top_scorers.Club.apply(
        lambda x: "Brighton & Hove Albion" if "Brighton & Hove Albion" in x else x
    )

    return top_scorers
