import pandas as pd
import geopandas as gpd

def generar_coordenadas_crudas():
    pois = pd.read_csv("data/POIs/POI_4815075.csv")
    calles = gpd.read_file("data/STREETS_NAV/SREETS_NAV_4815075.geojson")
    calles = calles.explode(index_parts=False).reset_index(drop=True)
    calles.columns = [col.upper() for col in calles.columns]

    # Validar que PERCFRREF esté entre 0 y 1
    pois = pois[(pois["PERCFRREF"] >= 0) & (pois["PERCFRREF"] <= 1)]
    pois = pois[pois["LINK_ID"].isin(calles["LINK_ID"])]

    pois_geom = []
    for _, poi in pois.iterrows():
        link_id = poi["LINK_ID"]
        perc = float(poi["PERCFRREF"])
        calle = calles[calles["LINK_ID"] == link_id]
        if calle.empty:
            continue
        geom_calle = calle.iloc[0]["GEOMETRY"]
        punto = geom_calle.interpolate(perc, normalized=True)
        poi_data = poi.to_dict()
        poi_data["geometry"] = punto
        pois_geom.append(poi_data)

    pois_geo = gpd.GeoDataFrame(pois_geom, geometry="geometry", crs="EPSG:4326")
    pois_geo["LAT"] = pois_geo.geometry.y
    pois_geo["LON"] = pois_geo.geometry.x
    pois_geo.to_csv("output/pois_con_coord.csv", index=False)
    print("🧪 Coordenadas crudas generadas.")
