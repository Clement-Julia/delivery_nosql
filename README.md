Script de création de la DB dans MongoDB : "python .\scripts\create_db.py"
À noter que les valeurs NaN ne sont pas incluses dans les graphiques.

Partie "Livreurs" : 
 - Deux points numériques qui démontrent la note moyenne de tous les livreurs
 - Répartition des livreur par tranches d'age
 - Temps de livraison moyen en fonction des tranches d'age
 - Note moyenne des livreurs en fonction des tranches d'ages

Le premier graphique montre une répartition plutôt equivalente entre les tranches d'ages. Avec ces tranches nous avons deux autre graphiques qui démontre le temps de livraison moyen par tranches d'ages, afin de déterminé quel tranches d'age est plus susceptible d'avoir un temps de livraison plus long, de même pour les notes moyenne, cependant les notes dont plus ou moins équivalentes en fonction des tranches d'ages

Partie "Distance" :
La partie 

Partie 'Trajet' :
 - La majorité des livreurs utilise une moto (58%) pour assurer leurs livraisons, suivis par le scooter (33.5%), le scooter électrique (8.4%) puis le vélo (0.1%).
 - L'environnement le plus récurrent des livraisons clients est un environnement Métropolitain (76.8%), Urbain (22.8%) et enfin Semi Urbain (0.4%)
 - On remarque que le temps moyen de livraison sont principalement étalés entre 15 et 32 minutes avec une moyenne de 26 minutes
 - Le traffic à un impact logique sur le temps de livraison, l'embouteillage (jam) à un fort impact sur la vitesse avec une durée de plus de 30 min contre 27 et 26 minutes pour une densité Haute et Moyenne respectivement. Un traffic Léger résulte d'une vitesse moyenne de 21 minutes.
 - Le type de véhicule ne semble pas avoir de gros impact sur la vitesse de livraison, la moto englobe les commandes les plus longues (> 50 minutes) mais peut s'expliquer par une plus grosses part dans le dataset (58%). Le vélo est semble légèrement allonger la durée de livraison par rapport au scooter et scooter électrique.
 - La météo a également un impact logique sur le temps de livraison, une météo Ensoleillé à une moyenne de temps de livraison plus basse (22 min) contre Venteux (26 min), Nuageux (28 min) et Embrumé (28 min). Étonnament les conditions de Tempête et Tempête de sable ont moins d'impact (environ 25 min).

On peut donc conclure que le livreur le plus rapide est probablement en scooter, dans un milieu urbain avec un trafic routier léger par une belle journée ensoleillée.