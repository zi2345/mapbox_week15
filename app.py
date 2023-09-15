from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)
import certifi
from pymongo import MongoClient

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

MONGODB_URl = os.environ.get("MONGODB_URl")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URl)
db = client[DB_NAME]
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/restaurants', methods=["GET"])
def get_restaurants():
    restaurants = list(db.restaurants.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'restaurants': restaurants})


@app.route('/restaurant/create', methods=["POST"])
def create_restaurant():
    name = request.form.get('name')
    categories = request.form.get('categories')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    doc = {
        'name': name,
        'categories': categories,
        'location': location,
        'center': [longitude, latitude],
    }

    db.restaurants.insert_one(doc)

    return jsonify({
        'result': 'success',
        'msg': 'succesfully created a restaurant'
    })


@app.route('/restaurant/delete', methods=["POST"])
def delete_restaurant():
    name = request.form.get('name')
    db.restaurants.delete_one({'name': name})
    return jsonify({
        'result': 'success',
        'msg': 'succesfully delete a restaurant'
    })



@app.route('/map')
def map_example():
    return render_template('prac_map.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)