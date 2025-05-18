import pandas as pd
import requests
import time

API_KEY = "."  # 🔐 Cambia esto por tu HERE API Key real
INPUT_FILE = "output/pois_con_coord.csv"
OUTPUT_FILE = "output/resultados_validacion_mejorado.csv"

df = pd.read_csv(INPUT_FILE).head(100)

coords_corregidas = []

for idx, row in df.iterrows():
    lat, lon = row["LAT"], row["LON"]
    url = "https://browse.search.hereapi.com/v1/browse"
    params = {
        "at": f"{lat},{lon}",
        "limit": 1,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        if items:
            new_lat = items[0]["position"]["lat"]
            new_lon = items[0]["position"]["lng"]
        else:
            new_lat, new_lon = None, None
    except Exception as e:
        print(f"Error en índice {idx}: {e}")
        new_lat, new_lon = None, None

    coords_corregidas.append((new_lat, new_lon))
    time.sleep(0.2)

df["HERE_LAT"] = [coord[0] for coord in coords_corregidas]
df["HERE_LON"] = [coord[1] for coord in coords_corregidas]

df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Coordenadas corregidas guardadas en: {OUTPUT_FILE}")
