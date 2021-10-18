import bs4 as bs
import urllib.request 
import pandas as pd
import sys 

def get_odds(weeknumber):
    
    #This function pulls the current money line odds for the NFL matchups from ESPN
    #returns a dataframe of Weeknumber, Matchup, Favorite ML, Underdog ML

    weeknumber = int(weeknumber)

    #create soup object from URL
    link = "https://www.espn.com/nfl/lines"
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source, 'html.parser')

    #build a dictionary for the team names to convert to abbreviations
    team_name_dict = {
                    'Philadelphia Eagles':'PHI',
                    'Atlanta Falcons':'ATL',
                    'Pittsburgh Steelers':'PIT',
                    'Buffalo Bills':'BUF',
                    'Minnesota Vikings':'MIN',
                    'Cincinnati Bengals':'CIN',
                    'San Francisco 49ers':'SF',
                    'Detroit Lions':'DET',
                    'Arizona Cardinals':'ARI',
                    'Tennessee Titans':'TEN',
                    'Seattle Seahawks':'SEA',
                    'Indianapolis Colts':'IND',
                    'Los Angeles Chargers':'LAC',
                    'Washington':'WSH',
                    'Tampa Bay Buccaneers':'TB',
                    'Miami Dolphins':'MIA',
                    'Jacksonville Jaguars':'JAX',
                    'Green Bay Packers':'GB',
                    'Chicago Bears':'CHI',
                    'Houston Texans':'HOU',
                    'Kansas City Chiefs':'KC',
                    'Los Angeles Rams':'LAR',
                    'New York Giants':'NYG',
                    'Baltimore Ravens':'BAL',
                    'Carolina Panthers':'CAR',
                    'Cleveland Browns':'CLE',
                    'Las Vegas Raiders':'LV',
                    'Denver Broncos':'DEN',
                    'Dallas Cowboys':'DAL',
                    'New England Patriots':'NE'
                    }

    # get a list of matchups from the HTML
    odds_matchups = []
    for i in soup.find_all('tbody',{'class':'Table__TBODY'}):
        teams = []
        for j in i.find_all('a',{'class':'AnchorLink'})[1::2]:
            teams.append(team_name_dict[j.string])
        odds_matchups.append(teams[0] + ' at ' + teams[1])

    #moneyline (ML). If positive, add to underdog list, if negative, add to favorite list
    favorite_ML, underdog_ML = [],[]

    #favorite and underdog moneylines
    for i in soup.find_all('tbody',{'class':'Table__TBODY'}):
        for j in i.find_all('tr',{'class':'Table__TR Table__TR--sm Table__even'}):
            k = j.find_all('td',{'class':'Table__TD'})[4]
            ml = int(k.string)
            if ml > 0:
                underdog_ML.append(ml)
            else:
                favorite_ML.append(ml)

    odds_df = pd.DataFrame({'Week':weeknumber, 'Matchup':odds_matchups, 'FavoriteML':favorite_ML, 'UnderdogML':underdog_ML})

    return(odds_df)

if __name__ == "__main__":
    df = get_odds(weeknumber=int(sys.argv[1]))
    df.to_csv('moneyline_odds.csv',index = False)
    print("File saved to folder.")