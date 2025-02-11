#------------------------------------------------------------------------------------------------------------------
# Libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from tqdm import tqdm

#------------------------------------------------------------------------------------------------------------------
# Global variables

TM_LEAGUES_IDS = {
    'Premier League'                : {'tm_league_id' : 'GB1'  , 'tm_league_name' : 'premier-league'},
    'Championship'                  : {'tm_league_id' : 'GB2'  , 'tm_league_name' : 'championship'},
    'Serie A'                       : {'tm_league_id' : 'IT1'  , 'tm_league_name' : 'serie-a'},
    'Serie B'                       : {'tm_league_id' : 'IT2'  , 'tm_league_name' : 'serie-b'},
    'La Liga'                       : {'tm_league_id' : 'ES1'  , 'tm_league_name' : 'laliga'},
    'La Liga 2'                     : {'tm_league_id' : 'ES2'  , 'tm_league_name' : 'laliga2'}, 
    'Bundesliga'                    : {'tm_league_id' : 'L1'   , 'tm_league_name' : 'bundesliga'},
    'Bundesliga 2'                  : {'tm_league_id' : 'L2'   , 'tm_league_name' : '2-bundesliga'},
    'Ligue 1'                       : {'tm_league_id' : 'FR1'  , 'tm_league_name' : 'ligue-1'},
    'Ligue 2'                       : {'tm_league_id' : 'FR2'  , 'tm_league_name' : 'ligue-2'},
    'Eredivisie'                    : {'tm_league_id' : 'NL1'  , 'tm_league_name' : 'eredivisie'},
    'Belgian Pro League'            : {'tm_league_id' : 'BE1'  , 'tm_league_name' : 'jupiler-pro-league'},
    'Primeira Liga'                 : {'tm_league_id' : 'PO1'  , 'tm_league_name' : 'liga-nos'},
    'Major League Soccer'           : {'tm_league_id' : 'MLS1'  , 'tm_league_name' : 'major-league-soccer'},
    'Liga MX'                       : {'tm_league_id' : 'MEXA' , 'tm_league_name' : 'liga-mx-apertura'},
    'Campeonato Brasileiro Série A' : {'tm_league_id' : 'BRA1' , 'tm_league_name' : 'campeonato-brasileiro-serie-a'},
}


#------------------------------------------------------------------------------------------------------------------
# Scraper

class TransfermarktPlayerScraper:
    
    #------------------------------------------------------------------------------------------------------------------
    
    def __init__(self):
        """
        Set headers in order not to be blocked for scraping its import to request 
        pages with some settings to look more like an actual browser.
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }
        self.session = requests.Session()  
        self.session.headers.update(self.headers)
    def __enter__(self):
        """
        Called when the `with` block is entered.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when the `with` block is exited.
        Cleans up the session or handles exceptions if necessary.
        """
        self.session.close()  # Clean up the session
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  
    
    #------------------------------------------------------------------------------------------------------------------
    
    def get_souped_page(self,page_url):
        '''
        this function takes a page_url from https://www.transfermarkt.com and returns the
        souped page
        '''
        pageTree = requests.get(page_url, headers=self.headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        return(pageSoup)

    #------------------------------------------------------------------------------------------------------------------

    def __get_club_urls_from_league_page(self,league_url,season=None):
        '''
        From a league page such as :
        https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1
        retrived the url links for all clubs
        Note: if i want a specific season, just add /plus/?saison_id=2023 (for example)
        '''
        if season != None:
            league_url = league_url + "/plus/?saison_id=" + str(season)
        
        league_base_page = self.get_souped_page(league_url)

        club_urls = []
        for row in league_base_page.find_all('table', 'items')[0].select('tr'):
            for item in row.find_all('td', 'hauptlink'):
                try:
                    link = item.select('a')[0]['href']
                    if link != None:
                        if len(link) > 0:
                            club_urls.append("https://www.transfermarkt.com" + link)
                except:
                    pass

        return(list(set(club_urls)))

    #------------------------------------------------------------------------------------------------------------------
    
    def __get_player_urls_from_club_page(self,club_url):
        '''
        From a club page such as :
        https://www.transfermarkt.com/manchester-united/startseite/verein/985/saison_id/2019
        retrived the url links for all players
        '''
        
        club_base_page = self.get_souped_page(club_url)

        player_urls = []
        for row in club_base_page.find_all('table', 'items')[0].select('tr'):
            for item in row.find_all('td', 'hauptlink'):
                try:
                    link = item.select('a')[0]['href']
                    if link != None:
                        if (len(link) > 0):
                            player_urls.append("https://www.transfermarkt.com" + link)
                except:
                    pass
        
        # remove all urls with word "marktwertverlauf" and keep only "profil"
        player_urls = [x for x in player_urls if "marktwertverlauf" not in x]

        return(list(set(player_urls)))

    #------------------------------------------------------------------------------------------------------------------
    
    def get_player_urls_from_league_page(self,league, season=None,verbose = False):
        '''
        From a league page such as :
        https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1
        retrived the url links for all players from all clubs

        if you want to check on progress chhange verbose to True
        
        Note: if i want a specific season, just add /plus/?saison_id=2023 (for example)
        '''
        
        if league not in TM_LEAGUES_IDS.keys():
                raise ValueError(f"League {league} not found, please select one among: {list(TM_LEAGUES_IDS.keys())}")
        
        tm_legue_name = TM_LEAGUES_IDS[league]['tm_league_name']
        tm_league_id  = TM_LEAGUES_IDS[league]['tm_league_id']
        league_url = f"https://www.transfermarkt.com/{tm_legue_name}/startseite/wettbewerb/{tm_league_id}"
        
        if season is not None:
            league_url = league_url + "/plus/?saison_id=" + str(season)
        
        players_urls = []
        clubs_urls = self.__get_club_urls_from_league_page(league_url,season)
        for c in clubs_urls:
            players_urls = players_urls +  self.__get_player_urls_from_club_page(c)
            if verbose:
                print(c.split("/")[3].replace("-", " "), "players added")
        return(players_urls)
    
    #------------------------------------------------------------------------------------------------------------------
    
    def __get_player_bio(self,player_url):
        
        player_page = self.get_souped_page(player_url)
        
        player_id     = player_url.split('/')[-1]
        player_name   = player_page.select_one('h1[class="data-header__headline-wrapper"]').text.split('\n')[-1].strip()
        
        player_height_re = re.search(r"Height:.*?([0-9].*?)\n", player_page.text, re.DOTALL)
        player_foot_re = re.search(r"Foot:.*?([A-Za-z].*?)\n", player_page.text, re.DOTALL)
        player_position_re = re.search(r"Position:.*?([A-Za-z].*?)\n", player_page.text, re.DOTALL)
        player_birthyear_re = re.search(r"Date of birth.*?\n\s*([A-Za-z]{3} \d{1,2}, \d{4})", player_page.text, re.DOTALL)
        
        player_height = player_height_re.group(1).strip() if player_height_re else None
        player_foot   = player_foot_re.group(1).strip() if player_foot_re else None
        player_position = player_position_re.group(1).strip() if player_position_re else None
        player_birthyear = player_birthyear_re.group(1).split(" ")[-1] if player_birthyear_re else None
        
        player_history = requests.get(
            url=f'https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/{player_id}',
            headers=self.headers).json()
        
        player_current_marketvalue   = player_history['list'][-1]['mw'] if player_history['list'] else None
        
        return [player_id,player_name,player_birthyear,player_position,player_height,player_foot,player_current_marketvalue]
        
    def get_players_info(self,league,season,verbose=False):
        players_urls = self.get_player_urls_from_league_page(league,season,verbose)
        players_df = pd.DataFrame(columns=['Player_ID','Player','BirthYear','Pos','Height','Foot','MarketValue','League'])
        for url in tqdm(players_urls,desc='Scraping players info'):
            player_info = self.__get_player_bio(url) + [league]
            players_df.loc[len(players_df)] = player_info
        
        return players_df