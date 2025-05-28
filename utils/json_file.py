import json
import random
def generar_rutas(base_path, prefijo, rango):
    return [f"{base_path}/{prefijo}_{i:06d}" for i in rango]

# Asociar categorías con bases específicas
bases = {
    "GND": "shape_data/Ground", 
    "VG": "shape_data/Vegetation",  
    "BD": "shape_data/Buildings",   
    "TL": "shape_data/TL", 
}

# Generar los datos y dividir entre los dos archivos
def generar_datos_y_dividir():
    rutas_originales = []
    rutas_submuestreadas = []

    # Generar TL (186 files)
    base = bases["TL"]  # Base correspondiente
    rutas = generar_rutas(base, "TL", range(186))
    # Seleccionar 20% (30 datos) y el resto
    seleccionados = random.sample(rutas, 36)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar VG (131 files)
    base = bases["VG"]  # Base correspondiente
    rutas = generar_rutas(base, "VG", range(132))
    # Seleccionar 20% (30 datos) y el resto
    seleccionados = random.sample(rutas, 26)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar GND (371 files)
    base = bases["GND"]  # Base correspondiente
    rutas = generar_rutas(base, "GND", range(372))
    # Seleccionar 20% (100 datos) y el resto
    seleccionados = random.sample(rutas, 74)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar BD (295 files)
    base = bases["BD"]  # Base correspondiente
    rutas = generar_rutas(base, "BD", range(296))
    # Seleccionar 20% (100 datos) y el resto
    seleccionados = random.sample(rutas, 59)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Mezclar aleatoriamente las rutas
    random.shuffle(rutas_originales)
    random.shuffle(rutas_submuestreadas)

    return rutas_originales, rutas_submuestreadas

# Guardar JSON
def guardar_json(rutas, archivo_salida):
    with open(archivo_salida, 'w') as file:
        json.dump(rutas, file, separators=(',', ':'))

# Ejecutar el script
if __name__ == "__main__":
    archivo_original = "rutas_originales.json"
    archivo_submuestreo = "rutas_submuestreadas.json"

    rutas_originales, rutas_submuestreadas = generar_datos_y_dividir()
    guardar_json(rutas_originales, archivo_original)
    guardar_json(rutas_submuestreadas, archivo_submuestreo)