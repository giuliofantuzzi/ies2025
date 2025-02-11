#------------------------------------------------------------------------------------------------------------------
# Libraries
import pandas as pd
from Scrapers import FbrefPlayerScraper

#------------------------------------------------------------------------------------------------------------------
# Global variables

LEAGUES = [
    'Premier League',          
    'Championship',                 
    'Serie A',
    'Serie B',
    'La Liga',
    'La Liga 2',
    'Bundesliga',
    'Bundesliga 2',
    'Ligue 1',
    'Ligue 2',
    'Eredivisie',
    'Belgian Pro League',
    'Primeira Liga',
    'Major League Soccer',
    'Liga MX',
    'Campeonato Brasileiro Série A' 
]

SEASON           = '2023-2024'
CATEGORICAL_COLS = ['Player','Nation','League','Pos','Squad']
DATA_PATH        = '../data/FBref/'
CSV_PATH         = DATA_PATH + 'players_stats_FBref.csv'
#------------------------------------------------------------------------------------------------------------------
# Main
if __name__ == '__main__':
    
    with FbrefPlayerScraper() as scraper:
        
        league_df = scraper.get_players_report(league=LEAGUES[0],season=SEASON)
        global_df = league_df.copy()
        for league in LEAGUES[1:]:
            league_df = scraper.get_players_report(league=league,season=SEASON)
            global_df = pd.concat([global_df,league_df],axis=0,ignore_index=True)

    numerical_cols = [col for col in global_df.columns if col not in CATEGORICAL_COLS]
    global_df.loc[:,numerical_cols] = global_df.loc[:,numerical_cols].apply(pd.to_numeric, errors='coerce')
    global_df.to_csv(CSV_PATH,index=False)

    print('-'*100)
    print('FBREF scraping report')
    print('-'*100)
    print(f"Total number of Leagues : {len(LEAGUES)}")
    print(f"Total number of Players : {global_df.shape[0]}")
    print(f"Total number of features: {global_df.shape[1]}")
    print('-'*100)