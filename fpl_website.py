#!/usr/bin/env python3
# coding: utf-8 

from flask import Flask, render_template

#Get formulas
from database.api_scrape import get_data

app = Flask(__name__)

#Homepage - show table with all players from db
@app.route("/table")
def player_data():
    #Call from mongo
    players = get_data()
    # return players.to_html()
    return render_template('tables.html', tables=[players.to_html()], titles=['players'], classes='players')
    # players

@app.route("/job")
def fetch_data():
    # fetch
    # save
    return "Everything is good, I've fetched the data. "
    # players = get_data()
    # return players.to_html()
    # return render_template('tables.html', tables=[players.to_html()], titles=['players'], classes='players')

if __name__ == '__main__':
  app.run(port=5000, debug=True)