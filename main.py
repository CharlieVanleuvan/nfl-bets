import bs4 as bs
import re
import urllib.request 
import pandas as pd
import sys

from get_espn_picks import get_espn_picks
from get_cbs_picks import get_cbs_picks
from get_odds import get_odds

#take the command line input and use as the week number
week = int(sys.argv[1])

#load ESPN picks
df_espn = get_espn_picks(weeknumber=week)

#Load CBS picks
df_cbs = get_cbs_picks(weeknumber=week)

#Load Moneylines
df_odds = get_odds(weeknumber=week)

#Join the espn and cbs dataframes
df = df_espn.merge(df_cbs, on = ['Week','Matchup'])

#implementing counting logic to get the true majority pick, if the picks from the 
#respective sites dont match
df['Majority Pick'] = df.apply(lambda x: x['Majority Pick_x'] if 
                                    ((x['Votes_x'] ==7) & (x['Votes_y'] == 5) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                     else
                                     (x['Majority Pick_y'] if ((x['Votes_x'] ==7) & (x['Votes_y'] == 6) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                        else (x['Majority Pick_y'] if ((x['Votes_x'] ==6) & (x['Votes_y'] == 6) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                            else (x['Majority Pick_y'] if ((x['Votes_x'] ==6) & (x['Votes_y'] == 5) & (x['Majority Pick_x'] != x['Majority Pick_y'])) else x['Majority Pick_x']))),axis=1)
#repeat for the number of votes                                     
df['Votes'] = df.apply(lambda x: 10 if 
                                    ((x['Votes_x'] ==7) & (x['Votes_y'] == 5) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                     else
                                     (10 if ((x['Votes_x'] ==7) & (x['Votes_y'] == 6) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                        else (11 if ((x['Votes_x'] ==6) & (x['Votes_y'] == 6) & (x['Majority Pick_x'] != x['Majority Pick_y']))
                                            else (10 if ((x['Votes_x'] ==6) & (x['Votes_y'] == 5) & (x['Majority Pick_x'] != x['Majority Pick_y'])) else (x['Votes_x'] + x['Votes_y'])))),axis=1)

#remove unnecessary columns
df = df[['Week','Matchup','Majority Pick','Votes']]

#join the odds data to the table
df = df.merge(df_odds, on = ['Week', 'Matchup'], how = 'left')

#clear up the NaNs
df['FavoriteML'].fillna(0, inplace = True)
df['UnderdogML'].fillna(0, inplace = True)

#save the files to the project folder
df.to_csv('master_data.csv', index = False)
df_espn.to_csv('espn_picks.csv', index = False)
df_cbs.to_csv('cbs_picks.csv', index = False)
df_odds.to_csv('moneyline_odds.csv', index = False)

#return statement to command prompt signalling end of script
print("File added to folder")
