from flask import Flask, render_template
import folium

#INSTALAR
import requests
from urllib.parse import urlencode
import json
import folium
import googlemaps
#====

lat=0
lng=0

app = Flask(__name__)
api_key = "AIzaSyBScKCVaK1TYx8ybLGJMHEmpXQW6k7c2eg"

@app.route('/')
def index():
    #getPosicion()
    #getMapR("pasta")
    return render_template('index.html')
    
def getPosicion():
    #OBTENER POSICION ACTUAL USER
    gmaps = googlemaps.Client(key=api_key)
    loc = gmaps.geolocate()
    if "location" in loc:
        global lat, lng
        lat=loc["location"]["lat"]
        lng=loc["location"]["lng"]
    else:
        print("ERRO EN LA API")
    #{'location': {'lat': 39.4755658, 'lng': -0.3466063}, 'accuracy': 930}

def getMapR(keyword):
    global lat, lng
    places_endpoint_2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params_2 = {
        "key": api_key,
        "location": f"{lat},{lng}",
        "radius": 500,
        "keyword": keyword,
        #"fields": "place_id,formatted_address,name,geometry,permanently_closed"
    }
    params_2_encoded = urlencode(params_2)
    places_url = f"{places_endpoint_2}?{params_2_encoded}"

    r2 = requests.get(places_url)
    data= r2.json()
    arrayData = []
    #PROCESA DATOS
    if data != None:
        try:
            #global arrayData
            #print(data['results'])
            for row in data['results']:
                #if "restaurant" and "food" in row['types']:
                if "restaurant" in row['types']:
                    lat=row["geometry"]["location"]["lat"]
                    lng=row["geometry"]["location"]["lng"]
                    user_ratings_total =0
                    rating=0
                    if row["rating"] != None:
                        rating=row["rating"]
                    if "user_ratings_total" in row:
                        user_ratings_total=row["user_ratings_total"]
                    open_now="CERRADO"
                    if "opening_hours" in row:
                        if row["opening_hours"]["open_now"]==True:
                            open_now ="ABIERTO"
                        else:
                            open_now ="CERRADO"
                    #print(row["name"])
                    #print(lat)
                    #print(lng)
                    #print(rating)
                    #print("##########################")
                    result = {'Place_id':row["place_id"],
                              'Name':row["name"] ,
                              'Rating':rating,
                              'User_ratings_total':user_ratings_total,
                              'Open_now':open_now,
                              'Location': [lat,lng]}
                    arrayData.append(result)
        except NameError:
            result=NameError
    if arrayData != None:
        m = folium.Map([lat, lng], tiles="cartodbpositron", zoom_start=17, world_copy_jump=True, no_wrap=False)
        for line in arrayData:
            if lat!=0 and lng !=0:
                folium.Marker(
                    location=[lat,lng],
                    popup="ESTOY AQUI",
                ).add_to(m)
            if line['Rating'] >=4:
                folium.Marker(
                    location=line['Location'],
                    popup=line['Name']+"\n"+line['Open_now']+"\nRanking: " + str(line['Rating']) +" - "+ str(line['User_ratings_total']) +" reseña(s) \n" ,
                    icon=folium.Icon(color="green", icon="ok-sign"),
                ).add_to(m)
            else:
                folium.Marker(
                    location=line['Location'],
                    popup=line['Name']+"\n"+line['Open_now']+"\nRanking: " + str(line['Rating']) +" - "+ str(line['User_ratings_total']) +" reseña(s) \n" ,
                    icon=folium.Icon(color="red", icon="remove-sign"),
                ).add_to(m)
        m.save('templates/map.html')

def btnK():
    print("SSSSSSSSS")

    
@app.route('/search')
def map():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)