#  GeoMétéo — Casablanca-Settat

Application web géospatiale interactive développée avec Python et Streamlit
pour visualiser les prévisions météorologiques de la région Casablanca-Settat.

##  Lien de l'application déployée
https://geometo-casablanca.streamlit.app/

##  Fonctionnalités de l'application

###  Module 1 — Navigation administrative
- Menu déroulant pour sélectionner une région parmi les 12 régions du Maroc
- Affichage automatique des provinces de la région sélectionnée
- Affichage automatique des communes de la province sélectionnée

###  Module 2 — Carte interactive
- Affichage du contour de la zone sélectionnée (rouge, sans remplissage)
- Modèle Numérique de Terrain (MNT) chargé depuis OpenTopoMap (WMS)
- Fond de carte OpenStreetMap
- Titre, légende et échelle graphique

###  Module 3 — Données climatiques
- Récupération automatique des prévisions météo sur 15 jours
- Température de l'air à 2 mètres (°C)
- Précipitations cumulées (mm)

###  Module 4 — Graphiques temporels
- Courbe interactive pour la température
- Histogramme pour les précipitations
- Dates au format JJ/MM/AAAA
- Tooltip interactif au survol

##  Sources de données
- **Shapefiles administratifs** : HCP Maroc — Découpage administratif WGS 84
- **MNT (Relief)** : OpenTopoMap WMS — https://tile.opentopomap.org
- **Prévisions météo** : Open-Meteo API — https://open-meteo.com (gratuite, sans clé)

##  Technologies utilisées
- **Streamlit** : Interface web interactive
- **GeoPandas** : Lecture et filtrage des shapefiles
- **Folium** : Cartographie interactive
- **Plotly Express** : Graphiques interactifs
- **Requests / Pandas** : Récupération et traitement des données météo

##  Installation locale
```bash
git clone https://github.com/elhajjymaryam123-png/Geometo-Casablanca/tree/main
cd Geometeo-Casablanca
pip install -r requirements.txt
streamlit run app.py
```

## 👥 Binôme
- Étudiant 1 : EL HAJJY MARYAM
- Étudiant 2 : BENSEAID ZAKARIA

**GIS Programming 2025-2026 — EHTP**
