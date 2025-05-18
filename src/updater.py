def aplicar_correccion(poi, clasificacion):
    caso = clasificacion.get('caso', 4)

    if caso == 0:
        accion = 'valido'
    elif caso == 1:
        accion = 'eliminar'
    elif caso == 2:
        accion = 'corregir lado (POI_ST_SD)'
    elif caso == 3:
        accion = 'cambiar MULTIDIGIT a N'
    elif caso == 4:
        accion = 'marcar como excepción'
    elif caso == -1:
        accion = 'error en procesamiento'
    else:
        accion = 'acción desconocida'

    return {
        'poi_id': poi.get('POI_ID', 'unknown'),
        'accion': accion,
        'comentario': clasificacion.get('comentario', 'Sin comentario')
    }