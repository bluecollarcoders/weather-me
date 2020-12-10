

import requests
from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from forms import RegisterForm, LoginForm
from models import db, connect_db, User, City


app = Flask(__name__)


app.config['Debug']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///weather_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "oh so secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Home landing page"""
    
    return render_template('landing.html')


def get_weather_data(city):
     url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=6b47a10251f21f0ed8e36fe46beb1242'
     r = requests.get(url).json()
     return r


@app.route('/weather')
def index_get():
    """Get Weather page"""

    if not session.get('user_id'):
        return redirect('/')

    user = User.query.get(session['user_id'])


    cities = City.query.all()

    
    weather_data = []

    for city in cities:
    
        r = get_weather_data(city.name)
        print(r)

        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data, user=user)


@app.route('/weather', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
           new_city_data = get_weather_data(new_city)

           if new_city_data['cod'] == 200:
              new_city_obj = City(name=new_city)

              db.session.add(new_city_obj)
              db.session.commit()
           else:
              err_msg = 'City does not exist in the World'
        else:
            err_msg = 'City already exists in the database!'

    if err_msg:
        flash(err_msg, 'error' )
    else:
        flash('City added succesfully!')   

    return redirect(url_for('index_get'))


@app.route('/delete/<name>/')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'City successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user: produce form & handle for submission"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.register(username, email, password)

        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        # on successful login, redirect to weather page
        return redirect(url_for('index_get'))

    else:
       return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login"""

    form = LoginForm() 

    if form.validate_on_submit():
        username = form.username.data
        auth_password = form.password.data

        # authenticate will return a user or false
        log_user = User.authenticate(username, auth_password)

        if log_user:
            session['user_id'] = log_user.id 
            return redirect(url_for('index_get'))

        else:
            flash('Could not find user')
            return redirect("/login")

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage"""

    session.pop('user_id')

    return redirect('/')