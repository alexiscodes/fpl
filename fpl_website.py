from flask import Flask

#takes Jinja template as input and produces pure HTML as output
from flask import render_template

#Get formulas
from database.fpl_methods import get_players

app = Flask(__name__)

@app.route("/")
def get_news():
  players = get_players()  
  return players.head().to_html()

if __name__ == '__main__':
  app.run(port=5000, debug=True)