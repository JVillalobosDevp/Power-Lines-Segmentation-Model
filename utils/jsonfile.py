import json
import random

# Función para generar rutas con un patrón específico
def generar_rutas(base_path, prefijo, rango):
    return [f"{base_path}/{prefijo}_{i:06d}" for i in rango]



# Asociar categorías con bases específicas
bases = {
    "GND": "shape_data/Ground", 
    "VG": "shape_data/Vegetation",  
    "BD": "shape_data/Buildings",   
    "TL": "shape_data/TL", 
}

#for ruta in bases:
#    print("la ruta para ", ruta, "es: ", bases[ruta])

# Generar los datos y dividir entre los dos archivos
def generar_datos_y_dividir():
    rutas_originales = []
    #rutas_submuestreadas = []

    # Generar TL (186 files)
    base = bases["TL"]  # Base correspondiente
    rutas = generar_rutas(base, "TL", range(500))
    # Seleccionar 20% (30 datos) y el resto
    #seleccionados = random.sample(rutas, 1)
    #rutas_submuestreadas.extend(seleccionados)
    #rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])
    rutas_originales.extend(rutas)

    # Generar VG (131 files)
    base = bases["VG"]  # Base correspondiente
    rutas = generar_rutas(base, "VG", range(500))
    # Seleccionar 20% (30 datos) y el resto
    #seleccionados = random.sample(rutas, 1)
    #rutas_submuestreadas.extend(seleccionados)
    #rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])
    rutas_originales.extend(rutas)    

    # # Generar GND (371 files)
    # base = bases["GND"]  # Base correspondiente
    # rutas = generar_rutas(base, "GD", range(500))
    # # Seleccionar 20% (100 datos) y el resto
    # #seleccionados = random.sample(rutas, 1)
    # #rutas_submuestreadas.extend(seleccionados)
    # #rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])
    # rutas_originales.extend(rutas)

    # Generar BD (295 files)
 #    base = bases["BD"]  # Base correspondiente
 #   rutas = generar_rutas(base, "BDt3", range(23))
    # Seleccionar 20% (100 datos) y el resto
    #seleccionados = random.sample(rutas, 1)
    #rutas_submuestreadas.extend(seleccionados)
    #rutas_originales.extend([ruta for ruta in rutas if ruta not in seleccionados])
 #   rutas_originales.extend(rutas)

    # Mezclar aleatoriamente las rutas ""
    random.shuffle(rutas_originales)
    #random.shuffle(rutas_submuestreadas)

    #return rutas_originales, rutas_submuestreadas

    #Only Test
    return rutas_originales

# Guardar JSON
def guardar_json(rutas, archivo_salida):
    with open(archivo_salida, 'w') as file:
        json.dump(rutas, file, separators=(',', ':'))

# Ejecutar el script
if __name__ == "__main__":
    archivo_original = "shuffled_test_file_list.json"
    archivo_submuestreo = "rutas_submuestreadas.json"

    #rutas_originales, rutas_submuestreadas = generar_datos_y_dividir()

    #Only test
    rutas_originales = generar_datos_y_dividir()

    guardar_json(rutas_originales, archivo_original)
    #guardar_json(rutas_submuestreadas, archivo_submuestreo)

    print(f"Archivo JSON original generado con {len(rutas_originales)} rutas en '{archivo_original}'.")
    #print(f"Archivo JSON submuestreado generado con {len(rutas_submuestreadas)} rutas en '{archivo_submuestreo}'.")