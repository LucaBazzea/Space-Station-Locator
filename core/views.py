from django.shortcuts import render
import requests
from geopy.geocoders import Nominatim
import folium
import time
from pprint import pprint

# instantiate a new Nominatim client
app = Nominatim(user_agent="space-station-locator")

def iss_coords():

    iss = requests.get("http://api.open-notify.org/iss-now.json")

    iss_json = iss.json()

    latitude = iss_json["iss_position"]["latitude"]
    longitude = iss_json["iss_position"]["longitude"]

    return latitude, longitude

latitude, longitude = iss_coords()

def get_address_by_coords(latitude, longitude):

    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude},{longitude}"

    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates)
    except:
        return get_address_by_coords(latitude, longitude)

address = get_address_by_coords(latitude, longitude)

print(f"\nCoordinates: {latitude}, {longitude}")
print(f"address :: {address}")

def get_index(request):

    map = folium.Map(location=[latitude, longitude], zoom_start=4, width=1000, height=550)
    
    if address == None:
        marker_popup = f"{latitude},<br>{longitude}"
    else:
        marker_popup = address

    icon_iss = folium.features.CustomIcon("core/static/images/space-station.png", icon_size=(64,64))

    folium.Marker(
        [latitude, longitude],
        popup=marker_popup,
        icon=icon_iss
        ).add_to(map)

    map = map._repr_html_() # Convert python notebook map into HTML

    context = {
        "map": map
    }

    return render(request, "index.html", context)