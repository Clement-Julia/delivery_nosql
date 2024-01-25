from flask import render_template, request, redirect, url_for, session
from models.trajet_model import get_typevehi_graph, get_typecity_graph, get_avgtemps_graph, get_density_graph, get_vehi_graph, get_weather_graph, get_vehitime_moy, get_citytime_moy
from pymongo import MongoClient

class TrajetController:
    def __init__(self):
        self.graph_type = None
        
    def index(self):
        client = MongoClient('localhost', 27017)
        db = client['food_delivery']
        collection = db['edf']

        graphs_dict = {
            'graph_circ_vehi': get_typevehi_graph(collection),
            'graph_circ_city': get_typecity_graph(collection),
            'graph_avgtemps': get_avgtemps_graph(collection),
            'graph_density': get_density_graph(collection),
            'graph_vehi': get_vehi_graph(collection),
            'graph_weather': get_weather_graph(collection),
        }
        avg_dict = {
            'avg_vehitime': get_vehitime_moy(collection),
            'avg_citytime': get_citytime_moy(collection)
        }

        return render_template('trajet.html', graphs_dict = graphs_dict, avg_dict = avg_dict)