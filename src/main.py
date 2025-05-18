import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit
from src.validator import clasificar_poi
from src.updater import aplicar_correccion

# Cargar archivos
pois = pd.read_csv("data/POIs/POI_4815075.csv")
calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
nombres_calles = gpd.read_file("data/STREETS_NAMING_ADDRESSING/SREETS_NAMING_ADDRESSING_4815075.geojson")

# Normalizar columnas
calles.columns = [col.upper() for col in calles.columns]
nombres_calles.columns = [col.upper() for col in nombres_calles.columns]

# Generar geometría desplazada por lado de calle
pois_geom_lado = []
for idx, poi in pois.iterrows():
    link_id = poi["LINK_ID"]
    perc = float(poi["PERCFRREF"])
    lado = poi["POI_ST_SD"]
    calle = calles[calles["LINK_ID"] == link_id]
    if calle.empty:
        continue
    geom_calle = calle.iloc[0]["GEOMETRY"]
    punto_base = geom_calle.interpolate(perc * geom_calle.length)
    try:
        offset_geom = geom_calle.parallel_offset(5, 'left' if lado == 'L' else 'right', join_style=2)
        poi_geom = offset_geom.interpolate(perc * offset_geom.length)
    except Exception:
        poi_geom = punto_base
    poi_data = poi.to_dict()
    poi_data["geometry"] = poi_geom
    pois_geom_lado.append(poi_data)

pois_geo = gpd.GeoDataFrame(pois_geom_lado, geometry="geometry")

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
    resultados.append(correccion)

# Guardar resultado
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv("output/resultados_validacion.csv", index=False)
print("✅ Validación completada.")

#.venv\Scripts\activate  