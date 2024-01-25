import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd
import seaborn as sns

import base64
from io import BytesIO

def get_df_clean(collection):
    df = pd.DataFrame(list(collection.find()))

    # Nettoyage de la colonne 'Time_taken(min)'
    df['Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min)', '').str.strip()
    df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'], errors='coerce')

    # Nettoyage de la colonne 'Weatherconditions'
    df['Weatherconditions'] = df['Weatherconditions'].apply(lambda x: x.replace('conditions', '').strip())

    # Nettoyage de la colonne 'City'
    df['City'] = df['City'].str.strip()

    return df

def get_typevehi_graph(collection):

    vehicles = collection.distinct("Type_of_vehicle")
    dict = {"Type_of_vehicle": [], "count": []}

    for vehicle in vehicles:
        count = collection.count_documents({"Type_of_vehicle": vehicle})
        dict["Type_of_vehicle"].append(vehicle)
        dict["count"].append(count)

    df = pd.DataFrame(dict)
    df['Type_of_vehicle'] = df['Type_of_vehicle'].replace({
        'bicycle ': 'Vélo',
        'electric_scooter ': 'Scooter électrique',
        'motorcycle ': 'Moto',
        'scooter ': 'Scooter'
    })
    
    plt.figure(figsize=(9, 6))
    plt.pie(df['count'], labels=df['Type_of_vehicle'], autopct='%1.1f%%', startangle=120)
    plt.title('Répartition des types de véhicules')

    # Convertir le graphique en données base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode('utf-8')
    
    return image_data

def get_typecity_graph(collection):

    df = get_df_clean(collection)
    df = df.dropna(subset=['City'])
    df['City'] = df['City'].replace({
        'Metropolitian': 'Metropolitain',
        'Semi-Urban': 'Semi Urbain',
        'Urban': 'Urbain',
    })

    allowed_values = ['Metropolitain', 'Semi Urbain', 'Urbain']
    filtered_df = df[df['City'].isin(allowed_values)]
    city_counts = filtered_df['City'].value_counts()
    
    plt.figure(figsize=(9, 6))
    plt.pie(city_counts, labels=city_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Répartition des types de villes')

    # Convertir le graphique en données base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode('utf-8')
    
    return image_data

def get_avgtemps_graph(collection):

    df = get_df_clean(collection)

    plt.figure(figsize=(12, 6))
    sns.histplot(df['Time_taken(min)'], bins=10, kde=True, color='#21c5fc')
    #plt.title('Durée moyenne de livraison')
    plt.xlabel('Temps moyen de trajet (min)')
    plt.ylabel("Nombre d'occurrences")

    time = df['Time_taken(min)'].mean()
    plt.axvline(time, color='black', linestyle='dashed', linewidth=2, label=f'Moyenne: {time:.2f} min')
    plt.legend()

    graph_filename = 'static/graphs/trajet_avgtemps_graph.png'
    plt.savefig(graph_filename)

    return graph_filename

def get_density_graph(collection):

    df = get_df_clean(collection)

    df_filtered = df.dropna(subset=['Road_traffic_density'])
    df_filtered['Road_traffic_density'] = df_filtered['Road_traffic_density'].str.strip()

    order = ["Low", "Medium", "High", "Jam"]

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Road_traffic_density', y='Time_taken(min)', data=df_filtered, order=order, color='#fc3721', errorbar=None)
    #plt.title('Relation entre le traffic et le temps de livraison')
    plt.xlabel('Densité du trafic')
    plt.ylabel('Temps de livraison (min)')

    graph_filename = 'static/graphs/trajet_density_graph.png'
    plt.savefig(graph_filename)

    return graph_filename

def get_weather_graph(collection):

    df = get_df_clean(collection)

    df_filtered = df.dropna(subset=['Weatherconditions'])
    order = ['Sunny', 'Windy', 'Cloudy', 'Fog', 'Stormy', 'Sandstorms']

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Weatherconditions', y='Time_taken(min)', data=df_filtered, order=order, color='#f5c842', errorbar=None)
    #plt.title('Relation entre la météo et le temps de livraison')
    plt.xlabel('Conditions météorologiques')
    plt.ylabel('Temps de livraison total (min)')

    graph_filename = 'static/graphs/trajet_weather_graph.png'
    plt.savefig(graph_filename)

    return graph_filename

def get_vehi_graph(collection):

    df = get_df_clean(collection)

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Time_taken(min)', y='Type_of_vehicle', data=df, color='#12ffb4')
    #plt.title('Relation entre le type de véhicule et le temps de livraison')
    plt.xlabel('Temps de livraison (min)')
    plt.ylabel('Type de véhicule')

    graph_filename = 'static/graphs/trajet_vehi_graph.png'
    plt.savefig(graph_filename)

    return graph_filename

def get_vehitime_moy(collection):

    df = get_df_clean(collection)
    df['Type_of_vehicle'] = df['Type_of_vehicle'].replace({
        'bicycle ': 'Vélo',
        'electric_scooter ': 'Scooter électrique',
        'motorcycle ': 'Moto',
        'scooter ': 'Scooter'
    })

    avg_delivery = df.groupby('Type_of_vehicle')['Time_taken(min)'].mean().reset_index()
    avg_delivery['Time_taken(min)'] = avg_delivery['Time_taken(min)'].round(1)

    return avg_delivery

def get_citytime_moy(collection):

    df = get_df_clean(collection)
    df_filtered = df.dropna(subset=['City'])

    df_filtered['City'] = df_filtered['City'].replace({
        'Metropolitian': 'Metropolitain',
        'Semi-Urban': 'Semi Urbain',
        'Urban': 'Urbain',
    })

    allowed_values = ["Metropolitain", "Semi Urbain", "Urbain"]
    df_filtered = df_filtered[df_filtered['City'].isin(allowed_values)]
    avg_delivery = df_filtered.groupby('City')['Time_taken(min)'].mean().reset_index()
    avg_delivery['Time_taken(min)'] = avg_delivery['Time_taken(min)'].round(1)

    return avg_delivery