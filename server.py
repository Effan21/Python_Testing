import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        todaysDate = datetime.now()
        todaysDate = todaysDate.strftime("%Y-%m-%d %H:%M:%S")
        return render_template('welcome.html',club=club,competitions=competitions,todaysDate=todaysDate)
    except IndexError:
        erreur = 1
        return render_template('index.html',erreur=erreur)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    dateCompetition=[c["date"] for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
            print(dateCompetition)
            return render_template('booking.html',club=foundClub,competition=foundCompetition)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    placesRequired = request.form['places']
    if placesRequired is None:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        error = 1
        return render_template('booking.html',club=club,competition=competition,error=error)
    
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        todaysDate = datetime.now()
        todaysDate = todaysDate.strftime("%Y-%m-%d %H:%M:%S")
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions,todaysDate=todaysDate)

    except ValueError: 
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        error = 1
        return render_template('booking.html',club=club,competition=competition,error=error)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))