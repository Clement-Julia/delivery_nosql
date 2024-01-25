from models.livreur_model import LivreurModel
from flask import render_template


class LivreurController:
    def __init__(self):
        self.model = LivreurModel()

    def index(self):
        data = self.model.get_data()
        graphe_age_tempslivraison = LivreurModel.graphe_age_tempslivraison(data) 
        data = self.model.get_data()
        graphe_nombreslivreur_age = LivreurModel.graphe_nombreslivreur_age(data)
        data = self.model.get_data()
        graphe_notemoy_livreur =LivreurModel.graphe_notemoy_livreur(data)
        data = self.model.get_data()
        test = LivreurModel.nb_total_livreur(data)
        data = self.model.get_data()
        test2 = LivreurModel.moy_total_livreur(data)
        data = self.model.get_data()
        table = LivreurModel.alldata(data)
        # test3 =LivreurModel.heurecommande_tempslivraison(data)
        

        return render_template('livreur.html', table= table, test2 = test2, test = test, graphe_age_tempslivraison=graphe_age_tempslivraison, graphe_nombreslivreur_age=graphe_nombreslivreur_age,graphe_notemoy_livreur = graphe_notemoy_livreur)
