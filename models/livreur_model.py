import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
from pymongo import MongoClient

class LivreurModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['food_delivery']
        self.collection = self.db['edf']

    def get_data(self):
        data = self.collection.find()
        return data

    def graphe_age_tempslivraison(data):
        data_list = list(data)
        
        if not data_list:
            # Gérer le cas où data_list est vide
            return None

        df = pd.DataFrame(data_list)

        df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)', '').str.strip()
        df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')

        df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')

        df.dropna(subset=['Delivery_person_Age', 'Time_taken(min)'], inplace=True)

        bins = [0, 25, 30, 36, df['Delivery_person_Age'].max()]
        labels = ['- de 25 ans', '26-30 ans', '31-36 ans', '+ de 36 ans']
        df['Age_Group'] = pd.cut(df['Delivery_person_Age'], bins=bins, labels=labels)

        age_groups = labels
        time_means = [df[df['Age_Group'] == age_group]['Time_taken(min)'].mean() for age_group in age_groups]

        plt.figure(figsize=(10, 6))
        plt.bar(age_groups, time_means)
        plt.xlabel("Tranches d'âge des livreurs")
        plt.ylabel("Temps de livraison moyen (minutes)")
        plt.title("Temps de livraison moyen en fonction des tranches d'âge des livreurs")
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.clf()

        return image_base64

    def graphe_nombreslivreur_age(data):
        data_list = list(data)

        if not data_list:
            # Gérer le cas où data_list est vide
            return None

        df = pd.DataFrame(data_list)

        if 'Delivery_person_Age' not in df.columns or 'Time_taken(min)' not in df.columns:
            # Gérer le cas où les colonnes nécessaires sont absentes
            return None

        df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')

        df.dropna(subset=['Delivery_person_Age'], inplace=True)

        bins = [0, 25, 30, 36, df['Delivery_person_Age'].max()]
        labels = ['- de 25 ans', '26-30 ans', '31-36 ans', '+ de 36 ans']
        df['Age_Group'] = pd.cut(df['Delivery_person_Age'], bins=bins, labels=labels, right=False)

        age_order = ['- de 25 ans', '26-30 ans', '31-36 ans', '+ de 36 ans']

        age_group_counts = df['Age_Group'].value_counts().reindex(age_order)

        plt.figure(figsize=(8, 8))
        plt.pie(age_group_counts.values, labels=age_group_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Assurez-vous que le diagramme est un cercle
        plt.title("Répartition des livreurs par tranche d'âge")

        plt.show()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.clf()

        return image_base64

    def graphe_notemoy_livreur(data):
        data_list = list(data)
        
        if not data_list:
            # Gérer le cas où data_list est vide
            return None

        df = pd.DataFrame(data_list)

        df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')

        df.dropna(subset=['Delivery_person_Age', 'Delivery_person_Ratings'], inplace=True)

        bins = [0, 25, 30, 36, df['Delivery_person_Age'].max()]
        labels = ['Moins de 25 ans', '26-30 ans', '31-36 ans', 'Plus de 36 ans']
        df['Age_Group'] = pd.cut(df['Delivery_person_Age'], bins=bins, labels=labels)

        age_groups = labels
        ratings_means = [df[df['Age_Group'] == age_group]['Delivery_person_Ratings'].mean() for age_group in age_groups]
        age_group_counts = [len(df[df['Age_Group'] == age_group]) for age_group in age_groups]  # Nombre total de livreurs par tranche d'âge

        plt.figure(figsize=(10, 6))
        bars = plt.bar(age_groups, ratings_means)
        plt.xlabel("Tranches d'âge des livreurs")
        plt.ylabel("Note moyenne de livraison")
        plt.title("Note moyenne de livraison en fonction des tranches d'âge des livreurs")
        # plt.grid(True)

        # Définir les limites de l'axe des ordonnées (y-axis) de 0 à 5
        plt.ylim(0, 6)

        for bar, mean, count in zip(bars, ratings_means, age_group_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'Moyenne: {mean:.2f}\nTotal: {count}', ha='center', va='bottom')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.clf()

        return image_base64
    
    def heurecommande_tempslivraison(data):
        data_list = list(data)
        
        if not data_list:
            # Gérer le cas où data_list est vide
            return None

        df = pd.DataFrame(data_list)
                # Remplacer les valeurs non valides ou corrompues dans la colonne 'Time_Orderd' par NaN
        df['Time_Orderd'] = df['Time_Orderd'].apply(lambda x: pd.to_datetime(x, errors='coerce'))

        # Supprimer les lignes contenant des valeurs NaN dans la colonne 'Time_Orderd'
        df.dropna(subset=['Time_Orderd'], inplace=True)

        # Conversion des colonnes en formats appropriés
        df['Time_taken(min)'] = df['Time_taken(min)'].str.extract('(\d+)').astype(int)

        # Création de tranches horaires pour l'heure de la commande (par exemple, matin, après-midi, soir)
        bins = [0, 6, 12, 18, 24]
        labels = ['Nuit', 'Matin', 'Après-midi', 'Soir']
        df['Time_Ordered_Category'] = pd.cut(df['Time_Orderd'].dt.hour, bins=bins, labels=labels)

        # Calcul de la moyenne du temps de livraison en minutes pour chaque tranche horaire
        average_delivery_time_minutes = df.groupby('Time_Ordered_Category')['Time_taken(min)'].mean()

        # Tracer le graphique
        plt.figure(figsize=(10, 6))
        plt.bar(average_delivery_time_minutes.index, average_delivery_time_minutes.values)
        plt.xlabel("Tranche horaire de la commande")
        plt.ylabel("Temps de livraison moyen (minutes)")
        plt.title("Impact de l'heure de la commande sur le temps de livraison moyen")
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.clf()

        return image_base64
    
    def alldata(data):
        data_list = list(data)
        if not data_list:
            return None

        df = pd.DataFrame(data_list)
        print(df)
        return df

    def nb_total_livreur(data):
        data_list = list(data)
        
        if not data_list:
            return None

        df = pd.DataFrame(data_list)

        nb_livreurs_distincts = df['ID'].nunique()

        return nb_livreurs_distincts

    def moy_total_livreur(data):
        data_list = list(data)
        
        if not data_list:
            # Gérer le cas où data_list est vide
            return None

        df = pd.DataFrame(data_list)

        # Convertir le champ 'Delivery_person_Ratings' en entiers et gérer les valeurs NaN
        df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].apply(pd.to_numeric, errors='coerce')
        df.dropna(subset=['Delivery_person_Ratings'], inplace=True)

        # Utilisez la méthode mean() pour calculer la moyenne globale du champ 'Delivery_person_Ratings'
        moyenne_globale = df['Delivery_person_Ratings'].mean()
        moyenne_globale = round(moyenne_globale,2)

        return moyenne_globale

