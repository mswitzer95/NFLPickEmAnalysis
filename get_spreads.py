import os
from statistics import median
import requests
from datetime import datetime, timedelta
from json import loads
from statistics import median


API_KEY_FILE_NAME = "odds-api-api-key.txt"
BASE_API_URL = "https://api.the-odds-api.com/v4/sports/"


def get_spreads() -> list:
    """
    Gets games and spreads.
    Args: None
    Returns: 
        list(dict): The games and spreads.
    
    Games and spreads will be returned as dicts of structure:
        {
            "home_team": str,
            "home_team_spread": float,
            "away_team": str,
            "away_team_spread": float
        }
    """
    
    with open(API_KEY_FILE_NAME, mode="r") as file:
        api_key = file.read()

    sport = "americanfootball_nfl"
    API_URL = f"{BASE_API_URL}{sport}/odds/"
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    params = {
        "apiKey": api_key,
        "regions": "us,us2",
        "markets": "spreads",
        "commenceTimeFrom": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commenceTimeTo": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Got {response.status_code} from odds-api.")
    response_json = loads(response.text)
    
    games = []
    for json_game in response_json:
        home_team = json_game["home_team"]
        away_team = json_game["away_team"]
        bookmaker_outcomes = [
            (
                (outcome_pair[0]["name"], outcome_pair[0]["point"]),
                (outcome_pair[1]["name"], outcome_pair[1]["point"]))
            for outcome_pair in [
                bookmaker["markets"][0]["outcomes"]
                for bookmaker in json_game["bookmakers"]]]
        bookmaker_outcomes = list(sum(bookmaker_outcomes, ()))
        home_team_spread = median(
            [
                outcome[1] for outcome in bookmaker_outcomes
                if outcome[0] == home_team])
        away_team_spread = median(
            [
                outcome[1] for outcome in bookmaker_outcomes
                if outcome[0] == away_team])
        game = {
            "home_team": home_team,
            "home_team_spread": home_team_spread,
            "away_team": away_team,
            "away_team_spread": away_team_spread}
        games.append(game)

    return games
