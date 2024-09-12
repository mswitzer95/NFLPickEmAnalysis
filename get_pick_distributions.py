import os
import requests
from bs4 import BeautifulSoup


URL = "https://football.fantasysports.yahoo.com/pickem"


def get_pick_distributions() -> dict:
    """
    Gets pick distributions
    Args: None
    Returns: 
        dict: The pick distributions, where the key is the team's name and the 
            value is the pick distribution.
    """
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, features="lxml")    
    table = soup.find(None, attrs={"class": "ysptblcontent1"})
    pick_rows = table.find_all("tr")
    pick_distributions = [
        [data.text for data in pick_row.find_all("td")[:2]]
        for pick_row in pick_rows]
    for i in range(len(pick_distributions)):
        pick_distribution = pick_distributions[i]
        raw_team_name = pick_distribution[0]
        raw_distribution = pick_distribution[1]
        
        if raw_team_name.find("@ ") != -1:
            team_name = raw_team_name[2:]
        else:
            team_name = raw_team_name

        distribution = float(raw_distribution[:-1]) / 100
        
        pick_distributions[i] = (team_name, distribution)

    pick_distributions = {
        pick_distribution[0]: pick_distribution[1]
        for pick_distribution in pick_distributions}

    return pick_distributions
