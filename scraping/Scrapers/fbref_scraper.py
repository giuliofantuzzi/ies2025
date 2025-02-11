#------------------------------------------------------------------------------------------------------------------
# Libraries
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO 
import time
from tqdm import tqdm

#------------------------------------------------------------------------------------------------------------------
# Global variables

FBREF_TABLE_IDS = {
    'shooting'              : 'stats_shooting',
    'passing'               : 'stats_passing',
    'pass types'            : 'stats_passing_types',
    'goal and shot creation': 'stats_gca',
    'defensive actions'     : 'stats_defense',
    'possession'            : 'stats_possession',
    'miscellaneous'         : 'stats_misc',
}


FBREF_STAT_TYPE = {
    'shooting'              : 'shooting',
    'passing'               : 'passing',
    'pass types'            : 'passing_types',
    'goal and shot creation': 'gca',
    'defensive actions'     : 'defense',
    'possession'            : 'possession',
    'miscellaneous'         : 'misc',
}

FBREF_LEAGUES = {
    'Premier League'                : {'fbref_league_id' : 9,  'fbref_league_name' : 'Premier-League'},
    'Championship'                  : {'fbref_league_id' : 10, 'fbref_league_name' : 'Championship'},
    'Serie A'                       : {'fbref_league_id' : 11, 'fbref_league_name' : 'Serie-A'},
    'Serie B'                       : {'fbref_league_id' : 18, 'fbref_league_name' : 'Serie-B'},
    'La Liga'                       : {'fbref_league_id' : 12, 'fbref_league_name' : 'La-Liga'},
    'La Liga 2'                     : {'fbref_league_id' : 17, 'fbref_league_name' : 'Segunda-Division'}, 
    'Bundesliga'                    : {'fbref_league_id' : 20, 'fbref_league_name' : 'Bundesliga'},
    'Bundesliga 2'                  : {'fbref_league_id' : 33, 'fbref_league_name' : '2-Bundesliga'},
    'Ligue 1'                       : {'fbref_league_id' : 13, 'fbref_league_name' : 'Ligue-1'},
    'Ligue 2'                       : {'fbref_league_id' : 60, 'fbref_league_name' : 'Ligue-2'},
    'Eredivisie'                    : {'fbref_league_id' : 23, 'fbref_league_name' : 'Eredivisie'},
    'Belgian Pro League'            : {'fbref_league_id' : 37, 'fbref_league_name' : 'Belgian-Pro-League'},
    'Primeira Liga'                 : {'fbref_league_id' : 32, 'fbref_league_name' : 'Primeira-Liga'},
    'Major League Soccer'           : {'fbref_league_id' : 22, 'fbref_league_name' : 'Major-League-Soccer'},
    'Liga MX'                       : {'fbref_league_id' : 31, 'fbref_league_name' : 'Liga-MX'},
    'Campeonato Brasileiro Série A' : {'fbref_league_id' : 24, 'fbref_league_name' : 'Campeonato-Brasileiro-Serie-A'},
}

#------------------------------------------------------------------------------------------------------------------
# Scraper

class FbrefPlayerScraper:
    
    #------------------------------------------------------------------------------------------------------------------
    
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless") 
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=self.chrome_options)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


    #------------------------------------------------------------------------------------------------------------------
              
    def __scrape_table(self,league,season,stat_type):
        
        fbref_league_name = FBREF_LEAGUES[league]['fbref_league_name']
        fbref_league_id   = FBREF_LEAGUES[league]['fbref_league_id']
        fbref_table_id    = FBREF_TABLE_IDS[stat_type]
        fbref_stat_type   = FBREF_STAT_TYPE[stat_type]
        
        url = f"https://fbref.com/en/comps/{fbref_league_id}/{season}/{fbref_stat_type}/{season}-{fbref_league_name}-Stats"
        
        
        self.driver.get(url)
        
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, fbref_table_id))
            )
        except TimeoutException:
            print(f"⏳Timeout: Table with ID '{fbref_table_id}' not found.")
            return None
        
        # Extract page source
        page_source = self.driver.page_source

        # Use BeautifulSoup to parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Locate the table by ID
        table = soup.find('table', {'id': fbref_table_id})

        # Use StringIO to wrap the HTML string
        html_string = str(table)
        df = pd.read_html(StringIO(html_string))[0]
        
        # Remove multiindex columns and remove useless columns
        df.columns = [' '.join(col).strip() for col in df.columns]
        df = df.reset_index(drop=True)
        new_columns = []
        for col in df.columns:
            if 'level_0' in col:
                new_col = col.split()[-1]
            else:
                new_col = col
            new_col = new_col.replace(' ', '_')
            new_columns.append(new_col)    
        # rename columns
        df.columns = new_columns
        df = df.fillna(value=np.nan)
        df = df.drop_duplicates()
        df.drop(labels=['Rk','Matches'], axis=1, inplace=True)  
        df.insert(4,'League',league)
        
        return df
    
    #------------------------------------------------------------------------------------------------------------------
    
    def get_players_stats(self,league=None,season=None,stat_type=None):

            if league not in FBREF_LEAGUES.keys():
                raise ValueError(f"League {league} not found, please select one among: {list(FBREF_LEAGUES.keys())}")
            if stat_type not in FBREF_TABLE_IDS.keys():
                raise ValueError(f"Stat type {stat_type} not found, please select one among: {list(FBREF_TABLE_IDS.keys())}")
            
            #print(f"🔍Scraping players's data for league: {league}, season: {season}, stat: {stat_type}...")    
            return self.__scrape_table(league,season,stat_type)
            
    #------------------------------------------------------------------------------------------------------------------
    
    def get_players_report(self,league=None,season=None):
        df_list = []
        for stat_type in tqdm(FBREF_STAT_TYPE.keys(),desc=f'Scraping stats for League: {league} (Season: {season})'):
            df_list.append(self.get_players_stats(league=league,season=season,stat_type=stat_type))
            time.sleep(5) # sleep for 5 seconds to avoid being blocked by the website
            
        left_df = df_list[0]
        for right_df in df_list[1:]:
            left_df = pd.merge(left_df,right_df,on=['Player', 'Nation', 'Pos', 'Squad','League','Age', 'Born', '90s'],how='inner')
        
        return left_df
             
    # #------------------------------------------------------------------------------------------------------------------