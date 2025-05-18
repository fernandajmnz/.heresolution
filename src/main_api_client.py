import pandas as pd
import requests
import os

# Asegurar carpeta de salida
os.makedirs("output", exist_ok=True)

# Cargar POIs
pois = pd.read_csv("data/POIs/POI_4815075.csv").head(800)  # limitar a 800 para prueba

# Convertir a lista de dicts para enviar a la API en lote
poi_list = []
for _, poi in pois.iterrows():
    poi_list.append({
        "POI_ID": poi["POI_ID"],
        "LINK_ID": poi["LINK_ID"],
        "PERCFRREF": poi["PERCFRREF"],
        "POI_ST_SD": poi["POI_ST_SD"]
    })

# Enviar todo en un solo POST
try:
    response = requests.post("http://localhost:5000/validar-pois", json=poi_list)
    if response.status_code == 200:
        resultados = response.json()
    else:
        print("❌ Error en la API:", response.status_code)
        resultados = []
except Exception as e:
    print("❌ Error al conectar con la API:", e)
    resultados = []

# Guardar resultados
df = pd.DataFrame(resultados)
df.to_csv("output/resultados_validacion_api.csv", index=False)
print("✅ Validación usando API completada.")
