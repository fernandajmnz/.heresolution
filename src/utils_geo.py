from shapely.geometry import LineString, Point

def obtener_lado_correcto(calle_geom: LineString, perc: float) -> str:
    """
    Dado un LineString de la calle y un valor entre 0–1 de PERCFFREF,
    interpola el punto a esa proporción y calcula un desplazamiento hacia la izquierda o derecha.
    Devuelve: 'L' (izquierda) o 'R' (derecha)
    """
    if calle_geom is None or not isinstance(calle_geom, LineString):
        return 'R'  # fallback

    # Punto en la línea según PERCFFREF
    point_on_line = calle_geom.interpolate(perc * calle_geom.length)

    # Crear offsets hacia ambos lados
    offset_left = calle_geom.parallel_offset(5, 'left', join_style=2)
    offset_right = calle_geom.parallel_offset(5, 'right', join_style=2)

    # Simular comparación: devolver lado más cercano
    if offset_left.distance(point_on_line) < offset_right.distance(point_on_line):
        return 'L'
    else:
        return 'R'

def distancia_a_calle(poi_geom: Point, calle_geom: LineString) -> float:
    """
    Calcula la distancia euclidiana entre el POI y la calle.
    """
    if poi_geom is None or calle_geom is None:
        return float('inf')
    return poi_geom.distance(calle_geom)

def es_multipledigit(calle_atributos: dict) -> bool:
    """
    Revisa si MULTIDIGIT == 'Y' en los atributos de la calle.
    """
    return calle_atributos.get('MULTIDIGIT', 'N') == 'Y'
