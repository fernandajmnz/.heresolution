def aplicar_correccion(poi, clasificacion):
    return {
        'poi_id': poi.get('ID', 'unknown'),
        'accion': 'corregir lado',
        'comentario': clasificacion.get('comentario', 'Sin comentario')
    }
