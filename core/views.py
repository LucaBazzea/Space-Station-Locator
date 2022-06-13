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

if address == None:
    print("The ISS is not above any geographical landmarks at the moment")
else:
    pprint(address)

print(f"\nCoordinates: {latitude}, {longitude}")

def get_index(request):

    map = folium.Map(location=[latitude, longitude], zoom_start=5, width=800, height=400)
    map = map._repr_html_() # Convert python notebook map into HTML

    context = {
        "map": map
    }

    return render(request, "index.html", context)