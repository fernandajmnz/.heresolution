from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit

def clasificar_poi(poi, calle_df, nombres_df):
    try:
        calle = calle_df.iloc[0]
        geom_calle = calle["GEOMETRY"]
        perc = float(poi["PERCFRREF"])
        lado_real = poi["POI_ST_SD"]
        poi_geom = poi["geometry"]
        dist = distancia_a_calle(poi_geom, geom_calle)
        lado_esperado = obtener_lado_correcto(geom_calle, perc)

        if dist > 5:
            return {'caso': 1, 'comentario': 'POI demasiado lejos de la calle'}
        elif lado_real != lado_esperado:
            return {'caso': 2, 'comentario': f'Lado incorrecto (real: {lado_real}, esperado: {lado_esperado})'}
        elif not es_multipledigit(dict(calle)):
            return {'caso': 3, 'comentario': 'Calle marcada incorrectamente como MULTIDIGIT'}
        else:
            return {'caso': 4, 'comentario': 'Excepción válida'}
    except Exception as e:
        return {'caso': 4, 'comentario': f'Error en validación: {str(e)}'}