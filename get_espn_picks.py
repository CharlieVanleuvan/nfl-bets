import bs4 as bs
import re
import urllib.request 
import pandas as pd
import sys 


#define a function that takes the week number and generates a table with all matchups and picks and votes
def get_espn_picks(weeknumber):
    #get this weeks number
    week_num = int(weeknumber)

    #get a list of all weeks so far
    week_nums = [str(i) for i in range(1,week_num + 1)]

    #the base url for espn picks
    base_link = r"https://www.espn.com/nfl/picks/_/seasontype/2/week/"

    #Lists that will supply the resulting data frame
    matchup_list_df, consensus_pick_list_df, votes_list_df, week_num_list_df = [],[],[], []

    #repeat the pick scraping for each week
    for week in week_nums:

        #create link
        link = base_link + week

        #open the link
        source = urllib.request.urlopen(link).read()

        #create soup object from BS
        soup = bs.BeautifulSoup(source, 'html.parser')

        #get matchups for this week
        matchups = [j.text for i in soup.find_all('div',{'class':'wrap-competition'}) for j in i.find_all('a')]        

        #list of picks and votes for this week
        consensus_pick_list, votes_list,week_num_list = [],[],[]

        #get the picks and votes
        #The index slice [15:-1] will have to change based on the number of teams having a bye week
        if week == '6':
            for i in soup.find_all('tr',{'class':'Table__TR Table__TR--sm Table__even'})[15:-1]:

                #create a list of the votes in each matchup
                votes = [re.findall(r"[^/]+(?=\.png)",j['src'])[0].upper() for j in i.find_all('img')]

                #create a set of the team names in each matchup
                team_names = set(votes)        

                #find the team with most votes
                consensus_pick = max(team_names, key = votes.count)

                #return the team name and number of votes
                consensus_pick_list.append(consensus_pick)
                votes_list.append(votes.count(consensus_pick))
                week_num_list.append(int(week))
        else:
            for i in soup.find_all('tr',{'class':'Table__TR Table__TR--sm Table__even'})[17:-1]:

                #create a list of the votes in each matchup
                votes = [re.findall(r"[^/]+(?=\.png)",j['src'])[0].upper() for j in i.find_all('img')]

                #create a set of the team names in each matchup
                team_names = set(votes)        

                #find the team with most votes
                consensus_pick = max(team_names, key = votes.count)

                #return the team name and number of votes
                consensus_pick_list.append(consensus_pick)
                votes_list.append(votes.count(consensus_pick))
                week_num_list.append(int(week))
        #append all of this weeks data to the master list
        matchup_list_df.extend(matchups)
        consensus_pick_list_df.extend(consensus_pick_list)
        votes_list_df.extend(votes_list)
        week_num_list_df.extend(week_num_list)

    #Now create the master Data Frame that has all the data from all weeks, all matchups
    df = pd.DataFrame({"Week":week_num_list_df,"Matchup":matchup_list_df,"Majority Pick":consensus_pick_list_df,"Votes":votes_list_df})

    return(df)

if __name__ == "__main__":
    df = get_espn_picks(weeknumber=int(sys.argv[1]))
    df.to_csv('espn_picks.csv', index = False)
    print(df.tail(16))
    print("File added to folder")