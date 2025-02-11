#------------------------------------------------------------------------------------------------------------------
# Libraries
import pandas as pd
from Scrapers import TransfermarktPlayerScraper

#------------------------------------------------------------------------------------------------------------------
# Global variables

LEAGUES = [
    #'Premier League',          
    #'Championship',                 
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

SEASON    = '2023'
DATA_PATH = '../data/Transfermarkt/'
CSV_PATH  = DATA_PATH + 'players_bio_tm.csv'

#------------------------------------------------------------------------------------------------------------------
# Main
if __name__ == '__main__':
    
    with TransfermarktPlayerScraper() as scraper:
        
        print(f'Retrieving player urls for league {LEAGUES[0]} (season {SEASON})')
        league_df = scraper.get_players_info(league=LEAGUES[0],season=SEASON,verbose=True)
        league_df.drop_duplicates(subset=['Player_ID'],inplace=True)
        league_df.to_csv(f'data/players_bio_tm_{LEAGUES[0]}.csv',index=False)
        
        global_df = league_df.copy()
        
        for league in LEAGUES[1:]:
            print(f'Retrieving player urls for league {league} (season {SEASON})')
            league_df = scraper.get_players_info(league=league,season=SEASON,verbose=True)
            league_df.drop_duplicates(subset=['Player_ID'],inplace=True)
            league_df.to_csv(DATA_PATH+f'players_bio_tm_{league}.csv',index=False)
            global_df = pd.concat([global_df.copy(),league_df.copy()],axis=0,ignore_index=True)
            
    global_df.drop_duplicates(subset=['Player_ID'],inplace=True)
    global_df.to_csv(CSV_PATH,index=False)
    
    print('-'*100)
    print(f"Total number of Leagues : {len(LEAGUES)}")
    print(f"Total number of Players : {global_df.shape[0]}")
    print(f"Total number of features: {global_df.shape[1]}")
    print('-'*100)  