from shapely.geometry import Point
import requests

API_KEY = "9BVyCDjeFIgpIM0Qostfay1sijVDJ1AhSMr7JfJV8AQ"

def buscar_lugar(nombre):
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={nombre}&apiKey={API_KEY}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    if not data.get("items"):
        return None
    pos = data["items"][0]["position"]
    return Point(pos["lng"], pos["lat"])
