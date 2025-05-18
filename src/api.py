from flask import Flask, request, jsonify
import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString
import os
from shapely.geometry import Point
from src.validator import clasificar_poi
from src.updater import aplicar_correccion

app = Flask(__name__)

# Cargar datos locales una sola vez
calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
nombres_calles = gpd.read_file("data/STREETS_NAMING_ADDRESSING/SREETS_NAMING_ADDRESSING_4815075.geojson")

# Estandarizar nombres de columnas a mayúsculas
calles.columns = [col.upper() for col in calles.columns]
nombres_calles.columns = [col.upper() for col in nombres_calles.columns]

@app.route("/validar-poi", methods=["POST"])
def validar_poi():
    data = request.get_json()

    required_fields = ["POI_ID", "LINK_ID", "PERCFRREF", "POI_ST_SD"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    poi = {
        "POI_ID": data["POI_ID"],
        "LINK_ID": data["LINK_ID"],
        "PERCFRREF": data["PERCFRREF"],
        "POI_ST_SD": data["POI_ST_SD"]
    }

    calle = calles[calles["LINK_ID"] == data["LINK_ID"]]
    nombres = nombres_calles[nombres_calles["LINK_ID"] == data["LINK_ID"]]

    if calle.empty:
        return jsonify({"error": "LINK_ID no encontrado en geometría"}), 404

    geom_calle = calle.iloc[0]["GEOMETRY"]
    perc = float(data["PERCFRREF"])
    lado = data["POI_ST_SD"]
    punto_base = geom_calle.interpolate(perc * geom_calle.length)
    try:
        offset_geom = geom_calle.parallel_offset(5, 'left' if lado == 'L' else 'right', join_style=2)
        poi_geom = offset_geom.interpolate(perc * offset_geom.length)
    except Exception:
        poi_geom = punto_base

    poi["geometry"] = poi_geom

    clasificacion = clasificar_poi(poi, calle, nombres)
    resultado = aplicar_correccion(poi, clasificacion)

    return jsonify(resultado)

@app.route("/validar-pois", methods=["POST"])
def validar_pois():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Se esperaba una lista de POIs"}), 400

    resultados = []

    for poi in data:
        if not all(k in poi for k in ["POI_ID", "LINK_ID", "PERCFRREF", "POI_ST_SD"]):
            resultados.append({
                "poi_id": poi.get("POI_ID", "unknown"),
                "accion": "error",
                "comentario": "POI incompleto"
            })
            continue

        calle = calles[calles["LINK_ID"] == poi["LINK_ID"]]
        nombres = nombres_calles[nombres_calles["LINK_ID"] == poi["LINK_ID"]]

        if calle.empty:
            resultados.append({
                "poi_id": poi["POI_ID"],
                "accion": "error",
                "comentario": "LINK_ID no encontrado"
            })
            continue

        geom_calle = calle.iloc[0]["GEOMETRY"]
        perc = float(poi["PERCFRREF"])
        lado = poi["POI_ST_SD"]
        punto_base = geom_calle.interpolate(perc * geom_calle.length)
        try:
            offset_geom = geom_calle.parallel_offset(5, 'left' if lado == 'L' else 'right', join_style=2)
            poi_geom = offset_geom.interpolate(perc * offset_geom.length)
        except Exception:
            poi_geom = punto_base

        poi["geometry"] = poi_geom

        clasificacion = clasificar_poi(poi, calle, nombres)
        resultado = aplicar_correccion(poi, clasificacion)
        resultados.append(resultado)

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)
