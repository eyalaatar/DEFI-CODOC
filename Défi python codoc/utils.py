from geopy.geocoders import Nominatim
from datetime import datetime

import logging
logging.basicConfig( format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def get_coordinates(address):
    app = Nominatim(user_agent="myGeocoder")
    localisation =  app.geocode(address)
    if localisation:
        localisation = localisation.raw
        return localisation['lat'], localisation['lon']
    else:
        return None


def change_date_format(date):
    """
    YYYY-MM-DD
    """
    return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")