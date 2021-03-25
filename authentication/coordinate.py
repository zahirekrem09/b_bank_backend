import requests
from decouple import config


def find_lat_long(zip_code):
    url = config("CORD_BASE_URL")
    r = requests.get(url.format(zip_code))
    content = r.json()
    return content["resourceSets"][0]["resources"][0]
