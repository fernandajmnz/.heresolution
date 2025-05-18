# src/generar_mapa.py
import os
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import LineString

def generar_mapa(path_resultado, path_pois, path_calles, salida_mapa):
    df_result = pd.read_csv(path_resultado)
    df_pois = pd.read_csv(path_pois)
    gdf_calles = gpd.read_file(path_calles)

    # Normalizar columnas
    df_result.columns = [col.strip().upper() for col in df_result.columns]
    df_pois.columns = [col.strip().upper() for col in df_pois.columns]
    df_result = df_result.loc[:, ~df_result.columns.duplicated()]
    df_pois = df_pois.loc[:, ~df_pois.columns.duplicated()]
    gdf_calles.columns = [col.lower() for col in gdf_calles.columns]

    df = pd.merge(df_result, df_pois, on="POI_ID", how="left")

    color_dict = {
        "eliminar": "red",
        "corregir lado (POI_ST_SD)": "orange",
        "cambiar MULTIDIGIT a N": "blue",
        "marcar como excepción": "green"
    }

    points = []
    for _, row in df.iterrows():
        try:
            link_id = row["LINK_ID"]
            perc = float(row["PERCFRREF"])
            match = gdf_calles[gdf_calles["link_id"] == link_id]
            if match.empty:
                continue
            geom = match.iloc[0].geometry
            if not isinstance(geom, LineString):
                continue
            point = geom.interpolate(perc * geom.length)
            points.append({
                "LAT": point.y,
                "LON": point.x,
                "ACCION": row.get("ACCION", ""),
                "COMENTARIO": row.get("COMENTARIO", "")
            })
        except Exception:
            continue

    df_coords = pd.DataFrame(points)
    mapa = folium.Map(location=[df_coords["LAT"].mean(), df_coords["LON"].mean()], zoom_start=15)
    mapa.fit_bounds([[df_coords["LAT"].min(), df_coords["LON"].min()],
                     [df_coords["LAT"].max(), df_coords["LON"].max()]])

    for _, row in df_coords.iterrows():
        color = color_dict.get(row["ACCION"], "gray")
        folium.CircleMarker(
            location=[row["LAT"], row["LON"]],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.75,
            popup=folium.Popup(f"<b>{row['ACCION']}</b><br>{row['COMENTARIO']}", max_width=300)
        ).add_to(mapa)

    legend_html = """
    <div style='position: fixed; bottom: 50px; left: 50px; width: 230px; height: 120px;
         border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
         padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);'>
    <b>🗺️ Leyenda:</b><br>
    🔴 Eliminar<br>
    🟠 Corregir lado<br>
    🔵 Cambiar MULTIDIGIT<br>
    🟢 Excepción válida</div>
    """
    mapa.get_root().html.add_child(folium.Element(legend_html))
    mapa.save(salida_mapa)
