from flask import Flask, request, render_template
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
from src.mapa import generar_mapa
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit
from src.validator import clasificar_poi
from src.updater import aplicar_correccion

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validar", methods=["POST"])
def validar():
    archivo = request.files.get("archivo")
    nav_file = request.files.get("streets_nav")
    naming_file = request.files.get("naming")

    if not archivo or not nav_file or not naming_file:
        return "Faltan uno o más archivos requeridos", 400

    # Cargar archivos
    pois = pd.read_csv(archivo)
    calles = gpd.read_file(nav_file)
    nombres_calles = gpd.read_file(naming_file)

    # Normalizar columnas
    calles.columns = [col.upper() for col in calles.columns]
    nombres_calles.columns = [col.upper() for col in nombres_calles.columns]

    # Generar geometría interpolada (punto base)
    pois_geom_lado = []
    for idx, poi in pois.iterrows():
        link_id = poi["LINK_ID"]
        perc = float(poi["PERCFRREF"])
        calle = calles[calles["LINK_ID"] == link_id]
        if calle.empty:
            continue
        geom_calle = calle.iloc[0]["GEOMETRY"]
        punto_base = geom_calle.interpolate(perc * geom_calle.length)
        poi_data = poi.to_dict()
        poi_data["geometry"] = punto_base
        pois_geom_lado.append(poi_data)

    # Crear GeoDataFrame con geometría base
    pois_geo = gpd.GeoDataFrame(pois_geom_lado, geometry="geometry")

    # Extraer coordenadas
    pois_geo["LAT"] = pois_geo.geometry.y
    pois_geo["LON"] = pois_geo.geometry.x

    # Crear carpeta de salida
    os.makedirs("output", exist_ok=True)

    # Guardar coordenadas
    pois_geo.to_csv("output/pois_con_coord.csv", index=False)

    # Validación y corrección
    resultados = []
    for idx, poi in pois_geo.iterrows():
        link_id = poi["LINK_ID"]
        calle = calles[calles["LINK_ID"] == link_id]
        nombres = nombres_calles[nombres_calles["LINK_ID"] == link_id]
        if calle.empty:
            continue
        clasificacion = clasificar_poi(poi, calle, nombres)
        correccion = aplicar_correccion(poi, clasificacion)
        correccion["LAT"] = poi["LAT"]
        correccion["LON"] = poi["LON"]
        correccion["POI_ID"] = poi.get("POI_ID")
        correccion["POI_NAME"] = poi.get("POI_NAME", "Sin nombre")
        resultados.append(correccion)

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv("output/resultados_validacion.csv", index=False)

    # ✅ Generar mapa visual con clasificación
    map_path = "static/mapa_resultado.html"
    generar_mapa(
        path_resultado="output/resultados_validacion.csv",
        path_pois="output/pois_con_coord.csv",
        path_calles=nav_file,  # usamos el archivo subido directamente
        salida_mapa=map_path
    )

    # Renderizar tabla + mapa
    return render_template("resultado.html", tabla=resultados)

if __name__ == "__main__":
    app.run(debug=True)
