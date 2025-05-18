from flask import Flask, request, jsonify
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
import os
from src.validator import clasificar_poi
from src.updater import aplicar_correccion

app = Flask(__name__)

# Cargar datos locales una sola vez (puedes cambiar esto a datos de CDMX reales)
calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
nombres_calles = gpd.read_file("data/STREETS_NAMING_ADDRESSING/SREETS_NAMING_ADDRESSING_4815075.geojson")

# Estandarizar nombres de columnas
calles.columns = [col.lower() for col in calles.columns]
nombres_calles.columns = [col.lower() for col in nombres_calles.columns]

# (Opcional) HERE API Key si decides usarla luego
HERE_API_KEY = os.getenv("HERE_API_KEY")  # exporta esto en tu terminal si quieres usarla luego

@app.route("/validar-poi", methods=["POST"])
def validar_poi():
    data = request.get_json()

    required_fields = ["POI_ID", "LINK_ID", "PERCFRREF", "POI_ST_SD", "MULTIDIGIT"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Crear POI simulado como dict
    poi = {
        "POI_ID": data["POI_ID"],
        "LINK_ID": data["LINK_ID"],
        "PERCFRREF": data["PERCFRREF"],
        "POI_ST_SD": data["POI_ST_SD"]
    }

    # Buscar geometría de la calle correspondiente
    calle = calles[calles["link_id"] == data["LINK_ID"]]
    nombres = nombres_calles[nombres_calles["link_id"] == data["LINK_ID"]]

    if calle.empty:
        return jsonify({"error": "LINK_ID no encontrado en geometría"}), 404

    # Inyectar MULTIDIGIT temporalmente en atributos
    calle = calle.copy()  # Asegura que trabajas con una copia real
    calle.at[calle.index[0], "MULTIDIGIT"] = data["MULTIDIGIT"]


    # Procesar POI usando tu lógica existente
    clasificacion = clasificar_poi(poi, calle, nombres)
    resultado = aplicar_correccion(poi, clasificacion)

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
