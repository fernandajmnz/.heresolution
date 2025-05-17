from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit

def clasificar_poi(poi, calle_df, nombres_df):
    try:
        calle = calle_df.iloc[0]
        geom_calle = calle.geometry
        perc = float(poi["PERCFRREF"])  # entre 0 y 1

        # Obtener punto interpolado del POI
        poi_geom = geom_calle.interpolate(perc * geom_calle.length)

        # Evaluar distancia
        distancia = distancia_a_calle(poi_geom, geom_calle)
        if distancia > 20:
            return {
                'caso': 1,
                'comentario': f'Distancia muy grande ({distancia:.2f}m)'
            }

        # Evaluar lado
        lado_esperado = obtener_lado_correcto(geom_calle, perc)
        lado_real = poi["POI_ST_SD"]
        if lado_esperado != lado_real:
            return {
                'caso': 2,
                'comentario': f'Lado incorrecto: real {lado_real}, esperado {lado_esperado}'
            }

        # Evaluar etiqueta MULTIDIGIT
        if not es_multipledigit(calle):
            return {
                'caso': 3,
                'comentario': 'MULTIDIGIT debería ser N'
            }

        # Todo correcto
        return {
            'caso': 4,
            'comentario': 'Excepción válida o sin errores relevantes'
        }

    except Exception as e:
        return {
            'caso': 4,
            'comentario': f'Error en validación: {str(e)}'
        }
