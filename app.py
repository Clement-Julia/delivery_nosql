from controllers.global_controller import GlobalController
from controllers.livreur_controller import LivreurController
import pandas as pd
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import json
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
import datetime
import pandas as pd
from raceplotly.plots import barplot
import plotly.graph_objects as go
import plotly
from random import sample
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/livreur')
def Livreur():
    livreur_controller = LivreurController()
    return livreur_controller.index()


@app.route('/toggle_graph', methods=['POST'])
def toggle_graph():
    global_controller = GlobalController()
    return global_controller.toggle_graph()

@app.template_filter('format')
def format_number(value):
    return '{:,}'.format(value)

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port="5005")