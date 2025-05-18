from shapely.geometry import LineString, Point

def obtener_lado_correcto(calle_geom: LineString, perc: float) -> str:
    if calle_geom is None or not isinstance(calle_geom, LineString):
        return 'R'
    point_on_line = calle_geom.interpolate(perc * calle_geom.length)
    offset_left = calle_geom.parallel_offset(7, 'left', join_style=2)
    offset_right = calle_geom.parallel_offset(7, 'right', join_style=2)
    if offset_left.distance(point_on_line) < offset_right.distance(point_on_line):
        return 'L'
    else:
        return 'R'

def distancia_a_calle(poi_geom: Point, calle_geom: LineString) -> float:
    if poi_geom is None or calle_geom is None:
        return float('inf')
    return poi_geom.distance(calle_geom)

def es_multipledigit(calle_atributos: dict) -> bool:
    return calle_atributos.get('MULTIDIGIT', 'N') == 'Y'