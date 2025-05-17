from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit
from src.validator import clasificar_poi
from src.updater import aplicar_correccion
import geopandas as gpd
import pandas as pd

# Cargar datos
pois = pd.read_csv("data/POIs/POI_4815075.csv")
calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
nombres_calles = gpd.read_file("data/STREETS_NAMING/SREETS_NAMING_ADDRESSING_4815075.geojson")

resultados = []

for idx, poi in pois.iterrows():
    link_id = poi["LINK_ID"]
    calle = calles[calles["LINK_ID"] == link_id]
    nombres = nombres_calles[nombres_calles["LINK_ID"] == link_id]

    if calle.empty:
        continue

    clasificacion = clasificar_poi(poi, calle, nombres)
    correccion = aplicar_correccion(poi, clasificacion)
    resultados.append(correccion)

# Guardar resultados
pd.DataFrame(resultados).to_csv("output/resultados_validacion.csv", index=False)
print("✅ Validación terminada.")

#.venv\Scripts\activate  