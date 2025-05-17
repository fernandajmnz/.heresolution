# main.py

import geopandas as gpd
from src.utils_geo import get_reference_node, calculate_poi_position, is_poi_on_correct_side
from src.validator import classify_violation
from src.updater import apply_correction
import os

# === Cargar datos ===
STREETS_PATH = "data/STREETS_NAV/sample_street.geojson"
POIS_PATH = "data/POIs/sample_poi.geojson"

print("[INFO] Cargando datos...")
streets = gpd.read_file(STREETS_PATH)
pois = gpd.read_file(POIS_PATH)

# === Analizar POIs ===
print("[INFO] Analizando POIs...")
results = []

for _, poi in pois.iterrows():
    link_id = poi['LINK_ID']
    street_segment = streets[streets['link_id'] == link_id]
    if street_segment.empty:
        continue

    ref_node = get_reference_node(street_segment)
    expected_pos = calculate_poi_position(street_segment, poi['PERCFFREF'])
    side_correct = is_poi_on_correct_side(street_segment, poi)

    violation_type = classify_violation(poi, street_segment, side_correct)
    corrected_poi = apply_correction(poi, violation_type)

    results.append(corrected_poi)

# === Guardar resultados (como ejemplo) ===
corrected = gpd.GeoDataFrame(results)
corrected.to_file("output/corrected_pois.geojson", driver='GeoJSON')
print("[INFO] Proceso completo. Archivo guardado en output/corrected_pois.geojson")
