# Data card

Due to the lack of a readily available datasets for our analysis, we built our own by integrating
data from three different sources: [`FBref`](https://fbref.com/en/), [`Transfermarkt`](https://www.transfermarkt.com) and [`clubelo`](http://clubelo.com). Our analysis focuses on the <u>2023/2024 season</u>, with each source providing complementary information to
enable a comprehensive evaluation.

## `FBref`
We extracted a wide range of player statistics covering various aspects of performance. These included:

- **Shooting**
    - `Standard_Gls/90` : Goals per 90 minutes
    - `Standard_Sh/90` : Shots per 90 minutes        
    - `Standard_SoT/90` : Shots on target per 90 minutes    
    - `Standard_Dist/90`: Average shot distance per 90 minutes          
    - `Standard_FK/Sh`: Free-kick proportion of total shots         
    - `Expected_xG/90`: Expected goals per 90 minutes       
    - `Expected_npxG/90`: Non-penalty expected goals per 90 minutes

- **Passing**
    - `Total_Cmp_P90` : Total passes completed per 90 minutes
    - `Total_Att_P90` : Total passes attempted per 90 minutes
    - `Average_TotDist` : Average total pass distance 
    - `Average_PrgDist` : Average progressive pass distance
    - `Short_Cmp_P90` : Short passes completed per 90 minutes
    - `Short_Att_P90` : Short passes attempted per 90 minutes
    - `Medium_Cmp_P90` : Medium passes completed per 90 minutes
    - `Medium_Att_P90` : Medium passes attempted per 90 minutes
    - `Long_Cmp_P90` : Long passes completed per 90 minutes
    - `Long_Att_P90` : Long passes attempted per 90 minutes
    - `Ast_P90` : Assists per 90 minutes
    - `Expected_xA_P90` : Expected assists per 90 minutes
    - `Expected_A-xAG` : Difference between assists and expected assists
    - `KP_P90` : Key passes per 90 minutes
    - `1/3_P90` : Final third passes per 90 minutes
    - `PPA_P90` : Passes into the penalty area per 90 minutes
    - `CrsPA_P90` : Crosses into the penalty area per 90 minutes
    - `PrgP_P90` : Progressive passes per 90 minutes

- **Pass types**
    - `Pass_Types_Live/90` : Live-ball passes per 90 minutes
    - `Pass_Types_Dead/90` : Dead-ball passes per 90 minutes
    - `Pass_Types_FK/90` : Free-kick passes per 90 minutes
    - `Pass_Types_TB/90` : Through balls (pass sent between back defenders into open space) per 90 minutes
    - `Pass_Types_Sw/90` : Switches per 90 minutes
    - `Pass_Types_Crs/90` : Crosses per 90 minutes
    - `Pass_Types_TI/90` : Throw-ins per 90 minutes
    - `Outcomes_Cmp/90` : Completed passes per 90 minutes
    - `Outcomes_Off/90` : Offside passes per 90 minutes
    - `Outcomes_Blocks/90` : Blocked passes per 90 minutes

- **Goal and shot creating actions**
    - `SCA_SCA90` : Shot-creating actions per 90 minutes
    - `GCA_GCA90` : Goal-creating actions per 90 minutes
    - `SCA_Types_PassLive/90` : Live-ball pass shot-creating actions per 90 minutes
    - `SCA_Types_PassDead/90` : Dead-ball pass shot-creating actions per 90 minutes
    - `SCA_Types_TO/90`: Successful take-ons leading to shot attempts per 90 minutes
    - `SCA_Types_Sh/90`: Shots leading to another shot per 90 minutes
    - `SCA_Types_Fld/90` : Fouls drawn leading to shot attempts per 90 minutes
    - `SCA_Types_Def/90` : Defensive actions leading to shot attempts per 90 minutes
    - `GCA_Types_PassLive/90` : Live-ball pass goal-creating actions per 90 minutes
    - `GCA_Types_PassDead/90 `: Dead-ball pass goal-creating actions per 90 minutes
    - `GCA_Types_TO/90` : Successful take-ons leading to goals per 90 minutes
    - `GCA_Types_Sh/90` : Shots leading to goals per 90 minutes
    - `GCA_Types_Fld/90` : Fouls drawn leading to goals per 90 minutes
    - `GCA_Types_Def/90` : Defensive actions leading to goals per 90 minutes

- **Defensive actions**
    - `Tackles_Tkl/90` : Tackles per 90 minutes
    - `Tackles_TklW/90` : Tackles won per 90 minutes
    - `Tackles_Def_3rd/90` : Tackles in the defensive third per 90 minutes
    - `Tackles_Mid_3rd/90` : Tackles in the middle third per 90 minutes
    - `Tackles_Att_3rd/90` : Tackles in the attacking third per 90 minutes
    - `Challenges_Tkl/90` : Dribblers tackled per 90 minutes
    - `Challenges_Att/90` : Dribblers faced per 90 minutes
    - `Challenges_Lost/90` : Unsuccessful attempts to face dribblers per 90 minutes
    - `Blocks_Blocks/90` : Blocks per 90 minutes
    - `Blocks_Sh/90` : Shots blocked per 90 minutes
    - `Blocks_Pass/90` : Passes blocked per 90 minutes
    - `Int/90`: Interceptions per 90 minutes
    - `Clr/90` : Clearances per 90 minutes
    - `Err/90` : Errors leading to an opponent's shot per 90 minutes

- **Possession**
    - `Touches_Touches/90` : Total touches per 90 minutes
    - `Touches_Def_Pen/90` : Touches in the defensive penalty area per 90 minutes
    - `Touches_Def_3rd/90` : Touches in the defensive third per 90 minutes
    - `Touches_Mid_3rd/90` : Touches in the middle third per 90 minutes
    - `Touches_Att_3rd/90` : Touches in the attacking third per 90 minutes
    - `Touches_Att_Pen/90` : Touches in the attacking penalty area per 90 minutes
    - `Take-Ons_Att/90` : Dribbles attempted per 90 minutes
    - `Take-Ons_Succ/90` : Dribbles completed per 90 minutes
    - `Take-Ons_Tkld/90` : Dribbles failed per 90 minutes
    - `Carries_Carries/90` : Carries per 90 minutes
    - `Carries_AverageTotDist` : Average total distance per carry
    - `Carries_AveragePrgDist` : Average progressive distance per carry
    - `Carries_PrgC/90` : Progressive carries per 90 minutes
    - `Carries_1/3/90` : Final third carries per 90 minutes
    - `Carries_CPA/90` : Carries into the penalty area per 90 minutes
    - `Carries_Mis/90` : Miscontrols per 90 minutes
    - `Carries_Dis/90` : Dispossessions per 90 minutes
    - `Receiving_Rec/90` : Passes received per 90 minutes
    - `Receiving_PrgR/90` : Progressive passes received per 90 minutes

- **Miscellaneous statistic**
    - `Performance_CrdY/90` : Yellow cards per 90 minutes
    - `Performance_Fls/90` : Fouls committed per 90 minutes
    - `Performance_Fld/90` : Fouls drawn per 90 minutes
    - `Performance_Off/90` : Offsides per 90 minutes
    - `Performance_Crs/90` : Crosses per 90 minutes
    - `Performance_Int/90` : Interceptions per 90 minutes
    - `Aerial_Duels_Won/90` : Aerial duels won per 90 minutes
    - `Aerial_Duels_Lost/90` : Aerial duels lost per 90 minutes

Data was gathered for players across the following leagues:
- *Premier League* (🏴󠁧󠁢󠁥󠁮󠁧󠁿)
- *Championship* (🏴󠁧󠁢󠁥󠁮󠁧󠁿)
- *Serie A* (🇮🇹)
- *Serie B* (🇮🇹)
- *La Liga* (🇪🇸)
- *La Liga 2* (🇪🇸)
- *Bundesliga* (🇩🇪)
- *Bundesliga 2* (🇩🇪)
- *Ligue 1* (🇫🇷)
- *Ligue 2* (🇫🇷)
- *Eredivisie* (🇳🇱)
- *Belgian Pro League* (🇧🇪)
- *Primeira Liga* (🇵🇹)
- *Major League Soccer* (🇺🇸)
- *Liga MX* (🇲🇽)
- *Campeonato Brasileiro* (🇧🇷)


> [!WARNING]  
> ⚠ Warning:
> As of 2025-01-15, we successfully scraped all data from FBref. However, starting from February 2025, we noticed that FBref has restricted the availability of certain statistics for minor leagues, including:
>    - Eredivisie
>    - Primeira Liga
>    - Spanish Segunda División
>    - Liga MX
>    - Belgian Pro League
> 
> If you plan to use the scraper, be aware that these leagues may have missing values (NaN). You can either:
>    - Remove these leagues from the league list in the Python scripts.
>    - Account for missing values when processing the data

> [!NOTE]
> We made the following data processing choices:
>    - Goalkeepers were excluded due to significant differences in their statistical profiles compared to outfield players.
>    - Players who had played fewer than 5 matches (intended as 450 minutes) were excluded to ensure meaningful statistical representation
>    - Feature engineering was performed by removing redundant statistics (e.g.,*Goals-per-Shot*, *Tackles win percentage*, etc.) and converting all per-game metrics into per-90-minute statistics (*P90*)



## `Transfermarkt`

We collected biographical and contractual information, such as:

- `Player Position`
- `Age`
- `Height`
- `Preferred Foot`
- `Market Value`

> [!NOTE]
> Merging `FBref` data with `Transfermarkt` required resolving inconsistencies in player and club names across the two sources. This was addressed by implementing an automated matching algorithm based on the [*Jaro-Winkler*](https://en.wikipedia.org/wiki/Jaro–Winkler_distance) text similarity metric, with a confidence threshold of 0.9 set to prioritize matching accuracy over quantity.


## `clubelo`

We leveraged the ClubElo API ([documentation](http://clubelo.com/API)), which provided a structured and readily accessible way to retrieve historical and current club ratings. This allowed us to seamlessly integrate Elo ratings into our dataset without the need for additional web scraping. Since `clubelo` only covers data for European leagues, players from *MLS*, *Liga MX*, and *Campeonato Brasileiro* were excluded.
From this dataset we:

- Maintained team Elo ratings 
- Computed a league Elo as the average Elo of its teams
