from shapely.geometry import Point
from src.utils_geo import obtener_lado_correcto, distancia_a_calle, es_multipledigit

def clasificar_poi(poi, calle_df, nombres_df):
    try:
        calle = calle_df.iloc[0]
        geom_calle = calle["GEOMETRY"]
        perc = float(poi["PERCFRREF"])
        lado_real = poi.get("POI_ST_SD", "").strip().upper()
        poi_geom = poi["geometry"]
        dist = distancia_a_calle(poi_geom, geom_calle)
        lado_esperado = obtener_lado_correcto(geom_calle, perc)

        # --- CASO 1: Muy lejos ---
        if dist > 20:
            return {'caso': 1, 'comentario': f'POI demasiado lejos de la calle ({dist:.1f}m)'}

        # --- CASO 2: Lado incorrecto 
        if lado_real in ["L", "R"]:
            if lado_real != lado_esperado and dist <= 15:
                return {'caso': 2, 'comentario': f'Lado incorrecto (real: {lado_real}, esperado: {lado_esperado})'}

        # --- CASO 3: Multiply Digitised conflictivo ---
        is_multipledigit = es_multipledigit(calle)
        if not is_multipledigit:
            return {'caso': 3, 'comentario': 'Calle no debe tener atributo Multiply Digitised'}

        # --- CASO 0: Todo correcto ---
        return {'caso': 0, 'comentario': 'Ubicacion valida'}

    except Exception as e:
        return {'caso': -1, 'comentario': f'Error: {e}'}
