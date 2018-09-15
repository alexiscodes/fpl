
# coding: utf-8

# In[3]:

import pandas as pd


# In[20]:

from bs4 import BeautifulSoup
import requests
from lxml import html
import json
import numpy as np

import pulp
import regex
import pickle
import itertools


# # Get Players

# In[9]:

def get_players():
    dump = requests.get('https://fantasy.premierleague.com/drf/bootstrap')
    load = dump.text
    json_dump = json.loads(load)
    
    datapoints = ['id', 'web_name', 'first_name', 'total_points', 'event_points', 'now_cost','cost_change_start', 
              'selected_by_percent', 'form','ep_next', 
              'chance_of_playing_next_round','minutes', 'bonus', 'goals_scored', 'assists', 'clean_sheets', 
              'goals_conceded', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 'ea_index', 'news']

    player_list = []

    for player in range(0, len(json_dump['elements'])):
        stats = [json_dump['elements'][player][x] for x in datapoints]
        player_list.append(stats)
    
    player_df = pd.DataFrame(player_list)

    # Rename columns
    player_df.columns = datapoints
    return player_df



# # Get Positions

# In[13]:

def add_positions(player_list):
    players = requests.get('https://fantasy.premierleague.com/player-list/')
    totals = players.text
    total_soup = BeautifulSoup(totals)
    
    #Get all player names

    player_names = total_soup.find_all('td')[::4]

    players = []

    for player in player_names:
        name = player.get_text()
        players.append(name)

    player_name_df = pd.DataFrame({"Name": players})
    
    # Positions for first and last player in each field

    for i, e in enumerate(player_name_df['Name']):
        if e == 'De Gea':   
            gk=i
        if e == 'Azpilicueta':   
            defe=i
        if e == 'Salah':   
            mid=i
        if e == 'Kane':   
            att=i
            
    #Populate df with positions
    player_name_df['position']=''

    player_name_df.loc[gk:(defe),'position']='Goalkeeper'
    player_name_df.loc[defe:(mid),'position']='Defender'
    player_name_df.loc[mid:(att),'position']='Midfielder'
    player_name_df.loc[att:,'position']='Attacker'
    
    #Merge with df
    fpl_players =  pd.merge(player_name_df, player_list, left_on='Name', right_on='web_name')
    
    return fpl_players



# In[32]:

def remove_duplicates(player_list):
    # Deal with duplicates

    duplicats = player_list['Name'].value_counts()>1

    dup_names = player_list['Name'].isin(['Rico', 'McCarthy','Ward','Bennett','Davies','Gray','Long','Simpson','Reid','Sánchez','McCartyh','Stephens', 'Pereira', 'Murphy', 'Williams'])
    dup_ids = player_list['id'].isin([295, 359])


    player_list.drop(player_list[dup_names].index, inplace=True)
    player_list.drop(player_list[dup_ids].index, inplace=True)
    return player_list



# # Optimal Choice

# In[36]:

def change_data(df):
    
    #Change format of df
    df['influence_f'] = df['influence'].astype(float)
    df['influence_f'].fillna(0, inplace=True)

    df['bps_f'] = df['bps'].astype(float)
    df['bps_f'].fillna(0, inplace=True)

    df['now_cost_f'] = df['now_cost'].astype(float)
    df['now_cost'].fillna(0, inplace=True)

    df['ict_f'] = df['ict_index'].astype(float)
    df['ict_f'].fillna(0, inplace=True)
    
    return df


# #Player variables by position
# influence = fpl_players[['id',"influence_f"]]
# threat = fpl_players[['id',"threat"]]
# creativity = fpl_players[['id',"creativity"]]

# # Get weighted summary stats for each player
# 
# condlist = [fpl_players['position']=='Goalkeeper', fpl_players['position']=='Defender',fpl_players['position']=='Midfielder',fpl_players['position']=='Attacker']
# choicelist = [fpl_players['stats']=fpl_players['influence'],fpl_players['stats']=fpl_players['influence'],fpl_players['stats']=fpl_players['influence'],fpl_players['stats']=fpl_players['influence']]

# In[42]:

def get_tuples(df, max_number, value_sort):

    #Make variables for positions
    #sorting = 'influence_f'
    #top_players = 100


    gks = df[df['position']=='Goalkeeper'].sort_values(by=value_sort, ascending=False)[:max_number]
    defs = df[df['position']=='Defender'].sort_values(by=value_sort, ascending=False)[:max_number]
    mds = df[df['position']=='Midfielder'].sort_values(by=value_sort, ascending=False)[:max_number]
    ats = df[df['position']=='Attacker'].sort_values(by=value_sort, ascending=False)[:max_number]

    rgks=range(0, len(gks))
    rdefs=range(0, len(defs))
    rmds=range(0, len(mds))
    rats=range(0, len(ats))
    
    #Make tuples
    gk = [tuple(c) for c in itertools.combinations(gks['id'], 2)]
    df = [tuple(c) for c in itertools.combinations(defs['id'], 5)]
    md = [tuple(c) for c in itertools.combinations(mds['id'], 5)]
    at = [tuple(c) for c in itertools.combinations(ats['id'], 3)]
    
    return gk, df, md, at



# 






