from flask import render_template, request, redirect, url_for, session
from models.global_model import *

class GlobalController:
    def __init__(self):
        test = ""

    def toggle_graph(self):
        graph_type = session.get('graph_type', 'Heures Vues')
        if graph_type == 'Heures Vues':
            session['graph_type'] = 'Moyenne des Viewers'
        else:
            session['graph_type'] = 'Heures Vues'
        return redirect(url_for('global_vue'))
    
    def distance(self):
        chart_histo = plot_reception_histogram()
        chart_livraison = plot_livraison_histogram()
        chart_avg_recep = get_average_reception_by_picked_date()
        chart_avg_livr = get_average_livraison_by_picked_date()
        chart_distance = calculate_distance()
        chart_livraison_diff = calculate_distance_by_traffic()

        return render_template('distance.html',
                               chart_histo=chart_histo,
                               chart_livraison=chart_livraison,
                               chart_livraison_density=chart_livraison_diff,
                               chart_avg_recep=chart_avg_recep,
                               chart_avg_livr=chart_avg_livr,
                               chart_distance=chart_distance
                            )