import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import plotly.express as px
import os

st.title("GeoMétéo — Casablanca-Settat")

# Chargement  des fichiers
# Chemin sur  PC
chemin_pc = "data/Decoupage_admin_WGS84/Decoupage_HCP_WGS84/"
# Chemin sur GitHub
chemin_github = "data/Decoupage_HCP_WGS84/"

# le bon chemin automatiquement
if os.path.exists(chemin_pc):
    chemin = chemin_pc
else:
    chemin = chemin_github

regions   = gpd.read_file(chemin + "Regions_WGS84.shp")
provinces = gpd.read_file(chemin + "Provinces_WGS84.shp")
communes  = gpd.read_file(chemin + "communes_WGS84.shp")

# Menu 1 des regions
liste_regions = sorted(regions["libelle_fr"].tolist())
region_choisie = st.selectbox("Choisir une région", liste_regions)

# Les provinces des regions
provinces_filtrees = provinces[provinces["region_fr"] == region_choisie]
liste_provinces = sorted(provinces_filtrees["libelle_fr"].tolist())

# Menu 2 des provinces
province_choisie = st.selectbox(" Choisir une province", liste_provinces)

# Les communes 
communes_filtrees = communes[communes["FIRST_prov"] == province_choisie]
liste_communes = sorted(communes_filtrees["FIRST_com_"].tolist())

# Menu 3 des communes 
commune_choisie = st.selectbox("Choisir une commune", liste_communes)

# Afficher ce qui est choisi
st.write("Région :", region_choisie)
st.write("Province :", province_choisie)
st.write("Commune :",commune_choisie)

# Zone active selon le niveau le plus fin choisi
if commune_choisie:
    zone = communes[communes["FIRST_com_"] == commune_choisie]
    zoom = 12
elif province_choisie:
    zone = provinces[provinces["libelle_fr"] == province_choisie]
    zoom = 10
else:
    zone = regions[regions["libelle_fr"] == region_choisie]
    zoom = 8


# Centroïde = centre de la zone pour centrer la carte
centre = zone.geometry.centroid.iloc[0]

# Créer la carte centrée sur la zone choisie
carte = folium.Map(
    location=[centre.y, centre.x],
    zoom_start=zoom,
    control_scale=True
)
# Ajouter le relief (MNT)
folium.TileLayer(
    tiles="https://tile.opentopomap.org/{z}/{x}/{y}.png",
    attr="OpenTopoMap",
    name="Relief (MNT)",
    overlay=False
).add_to(carte)

# Dessiner le contour de la zone
folium.GeoJson(
    zone,
    style_function=lambda x: {
        "color": "red",       # couleur du contour
        "weight": 3,          # épaisseur du contour
        "fillOpacity": 0      # pas de couleur à l'intérieur
    }
).add_to(carte)

# Nom de la zone active
nom_zone = commune_choisie or province_choisie or region_choisie

# Titre
st.subheader(f" Carte de : {nom_zone}")

# Légende 
st.markdown("**Légende :**")
st.markdown(" **Contour rouge** : Limite administrative de la zone sélectionnée")
st.markdown(" **Fond de carte** : Relief du terrain (MNT - OpenTopoMap)")
st.markdown(" **Échelle** : Voir l'outil de mesure en bas à gauche de la carte")

# Afficher la carte
st_folium(carte, width=800, height=500)

#affichage du meteo
# Coordonnées du centre de la zone
lat = centre.y
lon = centre.x

# Demander la météo à Open-Meteo
url = "https://api.open-meteo.com/v1/forecast"
parametres = {
    "latitude": lat,
    "longitude": lon,
    "daily": ["temperature_2m_max", "precipitation_sum"],
    "timezone": "Africa/Casablanca",
    "forecast_days": 15
}

reponse = requests.get(url, params=parametres)
donnees = reponse.json()

# Organiser les données dans un tableau
tableau = pd.DataFrame({
    "Date"         : donnees["daily"]["time"],
    "Température (°C)" : donnees["daily"]["temperature_2m_max"],
    "Précipitations (mm)" : donnees["daily"]["precipitation_sum"]
})
tableau["Date"] = pd.to_datetime(tableau["Date"]).dt.strftime("%d/%m/%Y") #chanfement de format des dates

# Afficher le tableau
st.write("###  Prévisions météo")
st.dataframe(tableau)

#affichage des graphiques
# Sélecteur entre température et précipitations
st.write("### Graphique Prévisions météo ")
choix = st.radio(
    "Choisir le paramètre",
    ["Température", "Précipitations"]
)

# Afficher le graphique selon le choix
if choix == "Température":
    fig = px.line(
        tableau,
        x="Date",
        y="Température (°C)",
        title=f"Température sur 15 jours — {nom_zone}",
        markers=True
    )
else:
    fig = px.bar(
        tableau,
        x="Date",
        y="Précipitations (mm)",
        title=f"Précipitations sur 15 jours — {nom_zone}"
    )


st.plotly_chart(fig)
