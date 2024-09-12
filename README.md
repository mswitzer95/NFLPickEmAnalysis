This package runs a scraping and data processing pipeline that retrieves odds and pick 'em distributions for the current week's NFL games, and saves an analysis to a CSV file.


The odds data comes from OddsAPI at https://the-odds-api.com/. The pick 'em distributions data comes from Yahoo! Sports at https://football.fantasysports.yahoo.com/pickem.


In order to run the script, you will have to supply an API key for OddsAPI. This API key should be stored (with no additional characters) in a file titled "odds-api-api-key.txt" within the base directory of this project.


The pipeline can be run by calling "python3 make_csv.py" from the command line from the base directory of this project. The results are saved to a file in the base directory named "Pick_Em_Analysis.csv".
