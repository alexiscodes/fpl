#!/usr/bin/env python
# coding: utf-8


# # Scrape FPL APIs
# https://www.reddit.com/r/FantasyPL/comments/c64rrx/fpl_api_url_has_been_changed/
# https://fantasy.premierleague.com/api/fixtures/
# https://fantasy.premierleague.com/api/element-summary/176/

def get_data():
    import pandas as pd
    import requests
    import json

    dump = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    load = dump.text
    json_dump = json.loads(load)

    player_list = []

    for team in range(0, len(json_dump['elements'])):
        stats = json_dump['elements'][team]
        player_list.append(stats)
        
    player_df = pd.DataFrame(player_list)

    # Rename columns
    player_df = player_df.apply(pd.to_numeric, errors='ignore')
    player_df.columns = ['pl_'+col for col in player_df.columns.values]
    return player_df
