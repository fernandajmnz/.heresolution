import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit
from src.updater import aplicar_correccion
from src.classifier import clasificar_poi


def validar_errores():
    df = pd.read_csv("output/resultados_validacion_mejorado.csv")
    calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
    nombres_calles = gpd.read_file("data/STREETS_NAMING_ADDRESSING/SREETS_NAMING_ADDRESSING_4815075.geojson")

    calles.columns = [col.upper() for col in calles.columns]
    nombres_calles.columns = [col.upper() for col in nombres_calles.columns]

    df["geometry"] = df.apply(
        lambda r: Point(r["HERE_LON"], r["HERE_LAT"]) if pd.notna(r["HERE_LAT"]) else Point(r["LON"], r["LAT"]),
        axis=1
    )
    pois_geo = gpd.GeoDataFrame(df, geometry="geometry")

    resultados = []
    for _, poi in pois_geo.iterrows():
        link_id = poi["LINK_ID"]
        calle = calles[calles["LINK_ID"] == link_id]
        nombres = nombres_calles[nombres_calles["LINK_ID"] == link_id]
        if calle.empty:
            continue
        clasificacion = clasificar_poi(poi, calle, nombres)
        correccion = aplicar_correccion(poi, clasificacion)
        resultados.append(correccion)

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv("output/resultados_validacion_final.csv", index=False)
    print("✅ Validación final lista en output/resultados_validacion_final.csv")