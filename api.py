import flask
from flask import Flask, request,Response
from coordinates import Coordinates
import json
from utils import restaurant_lists

restaurant_list = json.load(open('restaurants.json'))['restaurants'] #Load restaurant objects
app=Flask(__name__)
@app.route('/discovery',methods=['GET'])

def restaurants():
    lat,long = request.args.get('lat'),request.args.get('lon')
    
    coords = Coordinates(float(long),float(lat))
    newest,nearest,popular = restaurant_lists(coords,restaurant_list)
    sections = []
    
    for title,lst in zip(['Popular', 'New', 'Nearby'],[popular,newest,nearest]):
        ranked_obj={'title':f'{title} Restaurants','restaurants':lst}
        sections.append(ranked_obj)
    return {'sections': sections}
app.run(host='0.0.0.0',port=5000)


