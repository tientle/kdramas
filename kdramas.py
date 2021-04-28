from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from sqlalchemy import desc
import csv

app = Flask(__name__)
application = app

app.config['SECRET_KEY'] = 'gV6Crpsy4D'

Bootstrap(app)

def convert_to_dict(filename):
    datafile = open(filename, newline='')
    my_reader = csv.DictReader(datafile)
    list_of_dicts = list(my_reader)
    datafile.close()

    return list_of_dicts

drama_dict_list = convert_to_dict('everything_kdrama_data.csv')

directory_pairs = []
for drama in drama_dict_list:
    directory_pairs.append( (drama['id'], drama['name']) )

# the name of the database; add path if necessary
db_name = 'kdrama_app_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Drama(db.Model):
    __tablename__ = 'everything_kdrama_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    image_name = db.Column(db.Text)
    genre = db.Column(db.Text)
    starring = db.Column(db.Text)
    num_episodes = db.Column(db.Integer)
    release_year = db.Column(db.Integer)
    plot = db.Column(db.Text)
    rating = db.Column(db.String)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404


@app.route('/title/<title>')
def searchTitle(title):
    titles = Drama.query.filter(Drama.name.like("%" + title + "%")).all()
    return render_template('title_list.html', titles=titles, title=title)

@app.route('/genre/<genre>/')
def searchGenre(genre):
    genres = Drama.query.filter(Drama.genre.like("%" + genre + "%")).all()
    return render_template('genre_list.html', genres=genres, genre=genre)

@app.route('/actor/<actor>/')
def searchActor(actor):
    actors = Drama.query.filter(Drama.starring.like("%" + actor + "%")).all()
    return render_template('actor_list.html', actors=actors, actor=actor)

@app.route('/year/<year>')
def searchYear(year):
    years = Drama.query.filter(Drama.release_year.like("%" + year + "%")).all()
    return render_template('year_list.html', years=years, year=year)

@app.route('/rating/<rating>')
def searchRating(rating):
    ratings = Drama.query.filter(Drama.rating.like("%" + rating + "." + "%")).all()
    return render_template('rating_list.html', ratings=ratings, rating=rating)


#routes

@app.route('/drama/<id>')
def drama(id):
    drama = drama_dict_list[int(id)]
    return render_template('drama.html', drama=drama)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/directory/')
def directory():
    return render_template('directory.html', drama_dict_list=drama_dict_list)

if __name__ == '__main__':
    app.run(debug=True)
