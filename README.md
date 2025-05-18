# AutoValida MX – Starter Kit para Hackathon CDMX

Este repositorio contiene la base para una solución escalable e innovadora al problema de validación automática de datos espaciales (POI295) usando los datasets y APIs de HERE Technologies.

---

## 🚀 ¿Qué hace este proyecto?

- Carga datos de calles y puntos de interés de la Ciudad de México (HERE GeoJSON).
- Aplica reglas espaciales para validar ubicación de POIs en calles multivía.
- Clasifica errores con un modelo ligero (ML o lógica).
- Corrige datos automáticamente.
- Visualiza en un mapa interactivo los errores y soluciones.

---

## 📁 Estructura del repositorio

/autovalida-mx/
│
├── README.md ← Instrucciones del proyecto y cómo correrlo
├── requirements.txt ← Dependencias del proyecto
│
├── data/ ← GeoJSON de HERE (STREETS_NAV, POIs...)
│
├── src/
│ ├── main.py ← Ejecuta el flujo completo
│ ├── utils_geo.py ← Funciones geoespaciales (Rama: reglas-geoespaciales)
│ ├── validator.py ← Clasificación de tipo de error (Rama: validador-ml)
│ └── updater.py ← Corrección automática (Rama: updater)
│
├── notebooks/
│ └── exploration.ipynb ← Visualización, pruebas y anotación de errores (Rama: visualizador)
│
└── output/
└── mapa_resultado.html ← Visualización con Folium


Link a los archivos:
https://drive.google.com/drive/folders/1NnV2LWUpB408KRTz0ushbRUTVCBGuI47?usp=sharing
