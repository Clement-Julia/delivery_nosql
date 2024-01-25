import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl
import pandas as pd
from flask_mysqldb import MySQL
from pymongo import MongoClient
from pymongo import MongoClient
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import math
import pandas as pd
import seaborn as sns

def get_average_reception_by_picked_date():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Time_Order_picked': 1, 'Time_Orderd': 1})

    avg = 0
    i = 0
    FMT = '%H:%M:%S'
    for entry in data:
        picked_date_str = entry['Time_Order_picked']
        order_date_str = entry['Time_Orderd']
        
        if 'NaN' not in picked_date_str and 'NaN' not in order_date_str:
            time1 = datetime.strptime(order_date_str, FMT)
            time2 = datetime.strptime(picked_date_str, FMT)

            time_diff = (time2 - time1).total_seconds() / 60
            if time_diff > 0:
                avg += time_diff
                i += 1

    avg_diff = round(avg/i, 2)

    return avg_diff

def get_average_livraison_by_picked_date():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Time_Order_picked': 1, 'Time_Orderd': 1, 'Time_taken(min)': 1})

    total_time = 0
    i = 0
    FMT = '%H:%M:%S'
    for entry in data:
        picked_date_str = entry['Time_Order_picked']
        order_date_str = entry['Time_Orderd']

        time = entry['Time_taken(min)']
        time = time.split()[1]
        
        if 'NaN' not in picked_date_str and 'NaN' not in order_date_str :
            time1 = datetime.strptime(order_date_str, FMT)
            time2 = datetime.strptime(picked_date_str, FMT)

            time_diff = (time2 - time1).total_seconds() / 60
            if time_diff > 0:
                total_time += float(time) - time_diff
                i += 1

    avg_diff = round(total_time/i, 2)

    return avg_diff


def plot_reception_histogram():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Time_Order_picked': 1, 'Time_Orderd': 1})

    distances = []
    FMT = '%H:%M:%S'
    for entry in data:
        picked_date_str = entry['Time_Order_picked']
        order_date_str = entry['Time_Orderd']
        
        if 'NaN' not in picked_date_str and 'NaN' not in order_date_str:
            time1 = datetime.strptime(order_date_str, FMT)
            time2 = datetime.strptime(picked_date_str, FMT)

            time_diff = (time2 - time1).total_seconds() / 60
            if time_diff > 0:
                distances.append(time_diff)

    plt.hist(distances, bins=50, color='skyblue', edgecolor='black')
    plt.xlabel('Temps de réception de la commande (min)', fontsize=14)
    plt.ylabel('Nombre de commande', fontsize=14)
    plt.title('Temps de récupération', fontsize=16)
    plt.xticks(range(0, int(max(distances))+1, 5))
    plt.grid(True)

    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    chart_image_annee = base64.b64encode(image_buffer.read()).decode('utf-8')

    plt.clf()

    return chart_image_annee

def plot_livraison_histogram():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Time_taken(min)': 1})

    times = []
    for entry in data:
        time = entry['Time_taken(min)'].split()[1]
        times.append(time)

    plt.hist(times, bins=50, color='skyblue', edgecolor='black')
    plt.xlabel('Temps de livraison de la commande (min)', fontsize=14)
    plt.ylabel('Nombre de commande', fontsize=14)
    plt.title('Temps de livraison', fontsize=16)
    plt.xticks(range(0, int(max(times))+1, 5))
    plt.grid(True)

    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    chart_image_annee = base64.b64encode(image_buffer.read()).decode('utf-8')

    plt.clf()

    return chart_image_annee

def calculate_distance():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Restaurant_latitude': 1, 'Restaurant_longitude': 1, 'Delivery_location_latitude': 1, 'Delivery_location_longitude': 1, 'Time_taken(min)': 1})

    distances = []
    times = []
    rating = []
    deltas = []
    for entry in data:
        lat1 = entry['Restaurant_latitude']
        lon1 = entry['Restaurant_longitude']
        lat2 = entry['Delivery_location_latitude']
        lon2 = entry['Delivery_location_longitude']
        time = entry['Time_taken(min)']

        R = 6371

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        time = time.split()[1]

        temps_de_livraison_heures = float(time) / 60
        vitesse = distance / temps_de_livraison_heures

        seuil_tres_rapide = 80
        seuil_rapide = 30
        seuil_long = 10

        rating = ""
        
        if vitesse > seuil_tres_rapide:
            rating = "Très rapide"
        elif vitesse > seuil_rapide:
            rating = "Rapide"
        elif vitesse > seuil_long:
            rating = "Long"
        else:
            rating = "Trop long"

        if distance < 100:
            deltas.append(rating.strip())
            times.append(time)
            distances.append(distance)

    df = pd.DataFrame({'Temps (min)': times, 'Distance (km)': distances, 'Vitesse': deltas})
    df = df.sort_values(by=['Temps (min)'], ascending=True)

    sns.set_theme(style="ticks")

    f, ax = plt.subplots(figsize=(7, 5))
    sns.despine(f)
    ordre_categories = ["Trop long", "Long", "Rapide", "Très rapide"]

    colors = {"Très rapide": "green", "Rapide": "blue", "Long": "yellow", "Trop long": "red"}

    sns.histplot(
        df,
        x="Distance (km)", hue="Vitesse", y="Temps (min)", hue_order=ordre_categories,
        palette=colors
    )
    ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
    ax.set_yticks([0, 10, 20, 30, 40, 50])

    ax.invert_yaxis()
    ax.set_xticklabels(ax.get_xticks()[::-1])
    ax.invert_xaxis()
    ax.set_title("Vitesse de livraison")

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    my_base64_data = base64.b64encode(my_stringIObytes.read()).decode()

    plt.clf()

    return my_base64_data

def calculate_distance_by_traffic():
    client = MongoClient()
    db = client['food_delivery']
    collection = db['edf']

    data = collection.find({}, {'Road_traffic_density': 1, 'Time_taken(min)': 1})

    densities = []
    times = []
    for entry in data:
        density = entry['Road_traffic_density']
        time = entry['Time_taken(min)']
        time = time.split()[1]
        
        if 'NaN' not in density :
            densities.append(density.strip())
            times.append(time)

    df = pd.DataFrame({'Temps (min)': times, 'Densité': densities})
    df = df.sort_values(by=['Temps (min)'], ascending=True)
    df['Temps (min)'] = pd.to_numeric(df['Temps (min)'])

    # Spécification de l'ordre des catégories
    order = ['Low', 'Medium', 'High', 'Jam']
    df['Densité'] = pd.Categorical(df['Densité'], categories=order, ordered=True)

    # Calcul de la moyenne du temps pour chaque densité
    mean_times = df.groupby('Densité')['Temps (min)'].mean()

    # Création du bar plot
    plt.figure(figsize=(10, 6))
    colors = {'Low': '#27cc53', 'Medium': '#246cc9', 'High': '#ccc925', 'Jam': '#cc451d'}
    mean_times.sort_index().plot(kind='bar', color=[colors[d] for d in mean_times.index], edgecolor='black', rot=45)

    # Ajout des labels et du titre
    plt.xlabel('Densité')
    plt.ylabel('Temps moyen (min)')
    plt.title('Densité du trafic par rapport au temps de livraison')

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='png')
    my_stringIObytes.seek(0)
    my_base64_data = base64.b64encode(my_stringIObytes.read()).decode()

    plt.clf()

    return my_base64_data