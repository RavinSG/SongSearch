import os
from flask import Flask, render_template, request
from wtforms import SelectField, StringField
from flask_wtf import FlaskForm

from searchapp.data import all_songs
from searchapp.app.search import search

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class Form(FlaskForm):
    country = SelectField('country', choices=[])
    state = StringField("Song name")
    city = SelectField('city', choices=[])


@app.route('/home', methods=['GET', 'POST'])
def landing_page():
    form = Form()
    form.country.choices = ["asd", 'asdfaf', "qweq", "cqdas", 1, 23, 4, 534, 6342, 522, 364537, 57, 567456, 3, 234, 32,
                            562, 6, 246, 253]
    return render_template('frontPage.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    """
    Search for products across a variety of terms, and show 9 results for each.
    """
    search_terms = [
        'අම්මා',
        'තාත්තා',
        'ආදරේ',
        'දුක',
        'පාසල'
    ]

    num_results = 9
    products_by_category = [(t, search(t, num_results)) for t in search_terms]
    return render_template(
        'index.html',
        products_by_category=products_by_category,
    )


@app.route('/search', methods=['GET', 'POST'])
def search_single_product():
    """
    Execute a search for a specific search term.

    Return the top 50 results.
    """
    query = request.args.get('search')
    artist_name = request.args.get('artist_name')
    min_rating = request.args.get('min_rating')
    num_results = 50
    products_by_category = [(query, search(query, num_results, artist_name, min_rating))]
    return render_template(
        'index.html',
        products_by_category=products_by_category,
        search_term=query,
        artist_name=artist_name,
        min_rating=min_rating
    )


@app.route('/product/<int:product_id>')
def single_product(product_id):
    """
    Display information about a specific product
    """

    product = str(all_songs()[product_id - 1])

    return render_template(
        'product.html',
        product_json=product,
        search_term='',
    )
