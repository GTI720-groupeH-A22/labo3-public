import numpy as np
import skmob
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import folium


def spacial_dist(lat_1, lng_1, lat_2, lng_2):
    """
    Calcul la distance entre deux points. Les points doivent être exprimés 
    en coordoonées GPS (float). La distance est exprimée en mètre.
    """
    if (lat_1 == lat_2 and lng_1 == lng_2): 
        return 0.0
    
    er = 6366707
    latFrom = np.radians(lat_1)
    latTo = np.radians(lat_2)
    lngFrom = np.radians(lng_1)
    lngTo = np.radians(lng_2)
    
    return np.arccos(
        np.sin(latFrom) * np.sin(latTo)+\
        np.cos(latFrom) * np.cos(latTo) * np.cos(lngTo - lngFrom)
        )* er

def time_diff(time_1, time_2):
    """
    Calcul de la différence entre deux valeurs de datetime. La différence 
    est exprimée en seconde.
    """
    
    return np.timedelta64(time_2 - time_1, 's').astype("int") if time_2 > time_1 else np.timedelta64(time_1 - time_2, "s").astype("int")

def calcul_vitesse_point(lat_1, lng_1, time_1, lat_2, lng_2, time_2):
    """
    Calcul la vitesse entre deux points.
    
    lat_1, lng_1, time_1 : latitude, longitude et temps du premier point
    lat_2, lng_2, time_2 : latitude, longitude et temps du second point 
    
    return: vit, la vitesse entre ces deux points en mètre/seconde.

    """
    return spacial_dist(lat_1, lng_1, lat_2, lng_2) / time_diff(time_1, time_2) if time_diff(time_1, time_2) > 0 else 0

# vectorisation de la focntion calcul_vitesse_point
f = np.vectorize(calcul_vitesse_point)


def plot_points(lat_array, lng_array, zoom=6):
    """ Affiche les points représenter par lat_array et lng_array sur une carte Folium.
    :lat_array: tableau des latitudes.
    :lng_array: tableau des longitudes.
    
    :return: une carte Folium des points.
    """
    
    lat_array = np.array(lat_array)
    lng_array = np.array(lng_array)
        
    assert lat_array.shape[0] == lng_array.shape[0], "Les tableaux de latitudes et longitudes ne sont pas de la meme taille !"
    
    size_a = lat_array.shape[0]
    center = [np.sum(lat_array)/size_a, np.sum(lng_array)/size_a]
    mymap = folium.Map(location=center, zoom_start=zoom, tiles='Stamen Toner')
    
    for i in range(0, size_a):
        folium.CircleMarker(location=[lat_array[i], lng_array[i]], radius=5, color='blue').add_to(mymap)
        
    return mymap


def compute_centroid(arr_lat, arr_lng):
    """
    arr_lat: tableau des latitudes
    arr_lng: tableau des longitudes
    """
    
    xx = np.cos(np.radians(arr_lat)) * np.cos(np.radians(arr_lng))
    yy = np.cos(np.radians(arr_lat)) * np.sin(np.radians(arr_lng))
    zz = np.sin(np.radians(arr_lat))

    xxx = xx.sum() / xx.shape[0]
    yyy = yy.sum() / xx.shape[0]
    zzz = zz.sum() / xx.shape[0]

    assert (xx.shape[0] == yy.shape[0] and xx.shape[0] == zz.shape[0])

    central_longitude = np.arctan2(yyy, xxx)
    central_square_root = np.sqrt(xxx * xxx + yyy * yyy)
    central_latitude = np.arctan2(zzz, central_square_root)

    return np.array([np.degrees(central_latitude), np.degrees(central_longitude)])