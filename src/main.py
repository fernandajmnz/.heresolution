from src.generator import generar_coordenadas_crudas
from src.validator import validar_errores

print("🚀 Iniciando proceso completo...")

# 1. Generar coordenadas crudas
generar_coordenadas_crudas()

# 2. Ejecutar corrección (debes correrlo tú manualmente por ahora)
print("🛑 Corre ahora: python tools/update_cords.py")

# 3. Luego ejecuta la validación
respuesta = input("¿Ya ejecutaste update_cords.py? (s/n): ")
if respuesta.lower() == "s":
    validar_errores()


#.venv\Scripts\activate