from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit

def clasificar_poi(poi, calle_df, nombres_df):
    try:
        calle = calle_df.iloc[0]
        geom_calle = calle.geometry
        perc = float(poi["PERCFFREF"])  # de 0 a 1
        lado_real = poi["POI_ST_SD"]    # 'L' o 'R'

        # Crear punto del POI
        poi_geom = Point(poi["LONGITUDE"], poi["LATITUDE"])

        # Verificar distancia
        dist = distancia_a_calle(poi_geom, geom_calle)

        # Verificar lado correcto
        lado_esperado = obtener_lado_correcto(geom_calle, perc)

        if dist > 20:
            return {
                'caso': 1,
                'comentario': 'POI demasiado lejos de la calle'
            }
        elif lado_real != lado_esperado:
            return {
                'caso': 2,
                'comentario': f'Lado incorrecto (real: {lado_real}, esperado: {lado_esperado})'
            }
        elif es_multipledigit(dict(calle)) == False:
            return {
                'caso': 3,
                'comentario': 'Calle marcada incorrectamente como MULTIDIGIT'
            }
        else:
            return {
                'caso': 4,
                'comentario': 'Excepción válida'
            }

    except Exception as e:
        return {
            'caso': 4,
            'comentario': f'Error en validación: {str(e)}'
        }
