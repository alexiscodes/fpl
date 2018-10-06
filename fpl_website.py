#!/usr/bin/env python3
# coding: utf-8 

#takes Jinja template as input and produces pure HTML as output

from flask import Flask, render_template, url_for

#https://dev.to/paultopia/the-easiest-possible-way-to-throw-a-webapp-online-flask--heroku--postgres-185o
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import requests
import json
import pandas as pd
from flask_heroku import Heroku
import os

#Get formulas
from database.fpl_methods import get_all_data

app = Flask(__name__)

#Conncet db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Homepage - show table with all players from db
@app.route("/")
def get_news():
    players = get_all_data()  
    return render_template('tables.html',tables=[players.to_html()], titles = ['players'], classes='players')



if __name__ == '__main__':
  app.run(port=5000, debug=True)