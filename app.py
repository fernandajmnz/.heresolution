from flask import Flask, request, render_template, jsonify
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

from src.validator import clasificar_poi
from src.updater import aplicar_correccion
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit

app = Flask(__name__)

# Cargar los datos de referencia una vez
calles = gpd.read_file("data/STREETS_NAV/STREETS_NAV_4815075.geojson")
nombres_calles = gpd.read_file("data/STREETS_NAMING_ADDRESSING/STREETS_NAMING_ADDRESSING_4815075.geojson")
calles.columns = [col.upper() for col in calles.columns]
nombres_calles.columns = [col.upper() for col in nombres_calles.columns]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validar", methods=["POST"])
def validar():
    archivo = request.files.get("archivo")
    if not archivo:
        return "No se subio ningun archivo", 400

    df = pd.read_csv(archivo)
    resultados = []

    for _, poi in df.iterrows():
        link_id = poi.get("LINK_ID")
        calle = calles[calles["LINK_ID"] == link_id]
        nombres = nombres_calles[nombres_calles["LINK_ID"] == link_id]

        if calle.empty:
            resultados.append({"poi_id": poi.get("POI_ID"), "accion": "error", "comentario": "LINK_ID no encontrado"})
            continue

        perc = float(poi.get("PERCFRREF", 0))
        lado = poi.get("POI_ST_SD", "R")
        geom_calle = calle.iloc[0]["GEOMETRY"]
        punto_base = geom_calle.interpolate(perc * geom_calle.length)

        try:
            offset_geom = geom_calle.parallel_offset(5, 'left' if lado == 'L' else 'right', join_style=2)
            poi_geom = offset_geom.interpolate(perc * offset_geom.length)
        except Exception:
            poi_geom = punto_base

        poi_dict = poi.to_dict()
        poi_dict["geometry"] = poi_geom

        clasificacion = clasificar_poi(poi_dict, calle, nombres)
        correccion = aplicar_correccion(poi_dict, clasificacion)
        resultados.append(correccion)

    df_out = pd.DataFrame(resultados)
    output_path = os.path.join("output", "resultado_web.csv")
    os.makedirs("output", exist_ok=True)
    df_out.to_csv(output_path, index=False)

    return render_template("resultado.html", tabla=resultados)

if __name__ == "__main__":
    app.run(debug=True)
