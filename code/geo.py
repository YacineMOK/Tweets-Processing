from geopy.geocoders import Nominatim
import time
from pprint import pprint

# instantiate a new Nominatim client
app = Nominatim(user_agent="tutorial")

def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    try:
        return app.geocode(address).raw['lat'], app.geocode(address).raw['lon']
    except:
        return None