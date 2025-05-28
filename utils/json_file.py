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
    rutas = generar_rutas(base, "TL", range(30))
    # Seleccionar 20% (30 datos) y el resto
    seleccionados = random.sample(rutas, 3)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar VG (131 files)
    base = bases["VG"]  # Base correspondiente
    rutas = generar_rutas(base, "VG", range(74))
    # Seleccionar 20% (30 datos) y el resto
    seleccionados = random.sample(rutas, 7)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar GND (371 files)
    base = bases["GND"]  # Base correspondiente
    rutas = generar_rutas(base, "GND", range(75))
    # Seleccionar 20% (100 datos) y el resto
    seleccionados = random.sample(rutas, 8)
    rutas_submuestreadas.extend(seleccionados)
    rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])

    # Generar BD (295 files)
    base = bases["BD"]  # Base correspondiente
    rutas = generar_rutas(base, "BD", range(19))
    # Seleccionar 20% (100 datos) y el resto
    seleccionados = random.sample(rutas, 2)
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
    archivo_original = "shuffled_train_file_listt.json"
    archivo_submuestreo = "shuffled_val_file_list.json"

    rutas_originales, rutas_submuestreadas = generar_datos_y_dividir()
    guardar_json(rutas_originales, archivo_original)
    guardar_json(rutas_submuestreadas, archivo_submuestreo)