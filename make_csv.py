import os
from json import dumps, loads
from get_pick_distributions import *
from get_spreads import *
import pandas as pd
import numpy as np


OUTPUT_FILE_NAME = "Pick_Em_Analysis.csv"

YAHOO_ABBR_MAP = {
    "Arizona": "ARI",
    "Atlanta": "ATL",
    "Baltimore": "BAL",
    "Buffalo": "BUF",
    "Carolina": "CAR",
    "Chicago": "CHI",
    "Cincinnati": "CIN",
    "Cleveland": "CLE",
    "Dallas": "DAL",
    "Denver": "DEN",
    "Detroit": "DET",
    "Green Bay": "GB",
    "Houston": "HOU",
    "Indianapolis": "IND",
    "Jacksonville": "JAC",
    "Kansas City": "KC",
    "Las Vegas": "LV",
    "Los Angeles (LAC)": "LAC",
    "Los Angeles (LAR)": "LAR",
    "Miami": "MIA",
    "Minnesota": "MIN",
    "New England": "NE",
    "New Orleans": "NO",
    "New York (NYG)": "NYG",
    "New York (NYJ)": "NYJ",
    "Philadelphia": "PHI",
    "Pittsburgh": "PIT",
    "San Francisco": "SF",
    "Seattle": "SEA",
    "Tampa Bay": "TB",
    "Tennessee": "TEN",
    "Washington": "WAS"
}

ODDS_API_ABBR_MAP = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAC",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}


def main():
    """
    Makes a CSV containing the NFL Pick Em analysis.
    Args: None
    Returns: None
    """
    
    spreads = get_spreads()
    spreads_table = pd.DataFrame(spreads)
    spreads_table["home_team"] = [
        ODDS_API_ABBR_MAP.get(team_name)
        for team_name in spreads_table["home_team"]]
    spreads_table["away_team"] = [
        ODDS_API_ABBR_MAP.get(team_name)
        for team_name in spreads_table["away_team"]]
    
    
    pick_distributions = get_pick_distributions()
    pick_distributions = [
        {"team": item[0], "pick %": item[1]}
        for item in pick_distributions.items()]
    pick_distributions_table = pd.DataFrame(pick_distributions)
    pick_distributions_table["team"] = [
        YAHOO_ABBR_MAP.get(team_name)
        for team_name in pick_distributions_table["team"]]

    final_table = pd.DataFrame([])
    final_table["AWAY"] = spreads_table["away_team"]
    final_table[""] = "@"
    final_table["HOME"] = spreads_table["home_team"]
    final_table["FAVE"] = np.where(
        spreads_table["away_team_spread"] < spreads_table["home_team_spread"],
        spreads_table["away_team"],
        spreads_table["home_team"])
    final_table["FAVE SPREAD"] = np.min(
        spreads_table[["away_team_spread", "home_team_spread"]], axis=1)
    final_table["FAVE IMPLIED WIN %"] = np.min(
        np.array(
            [
                # Hardcoded based on analysis in "odds_to_win_percent.ipynb
                # jupyter notebook - see notebook.
                (final_table["FAVE SPREAD"] * -0.0305 + 0.5040).to_numpy(),
                np.array([1] * len(final_table))]),
            
        axis=0)
    final_table["FAVE IMPLIED WIN %"] = [
        min(percent, 1.0) 
        for percent in final_table["FAVE IMPLIED WIN %"].tolist()]
    final_table = pd.merge(
        final_table, pick_distributions_table, left_on="FAVE", right_on="team")
    final_table = final_table.drop(columns="team")
    final_table = final_table.rename(columns={"pick %": "FAVE PICK %"})
    final_table["DIFF"] = (
        final_table["FAVE PICK %"] - final_table["FAVE IMPLIED WIN %"])
    
    final_table.to_csv(OUTPUT_FILE_NAME, index=False)


if __name__ == "__main__":
    main()