import os

def onefile(carpeta_origen, archivo_salida):
    #Ensure output folder exist
    os.makedirs('./segmented_file', exist_ok=True)
    # Crear o vaciar el archivo de salida
    with open(archivo_salida, 'w') as f_salida:
       # pass  # Simplemente se abre en modo 'w' para vaciar el contenido si existe

        # Procesar cada archivo en la carpeta de origen
        for archivo in os.listdir(carpeta_origen):
            if archivo.endswith(".txt"):
                ruta_archivo = os.path.join(carpeta_origen, archivo)
            
                with open(ruta_archivo, 'r') as f_entrada:
                    for linea in f_entrada:
                        columnas = linea.split()

                        confidence = float(columnas[4])

                        cuarto_valor = float(columnas[3])

                        #if confidence > 0:
                            # Formatear la cuarta columna a seis decimales
                        cuarto_valor = float(columnas[3])
                        cuarto_formateado = f"{cuarto_valor:.6f}"
                        
                        if cuarto_valor == 0:
                            rgb = "139 69 19"
                        elif cuarto_valor == 1:
                            rgb = "34 139 34"
                        elif cuarto_valor == 2:
                            rgb = "255 0 0"
                        elif cuarto_valor == 3:
                            rgb = "255 255 0"
                        elif cuarto_valor == 4:
                            rgb = "255 255 0"
                        else: 
                            rgb = "128 128 128"
                        
                            # Crear la línea de salida y escribirla en el archivo
                        linea_salida = f"{columnas[0]} {columnas[1]} {columnas[2]} {rgb} {cuarto_formateado} {confidence:.6f}\n"
                        f_salida.write(linea_salida)

    print(f"Todos los archivos se han procesado y combinado en {archivo_salida}")

carpeta_origen = "data/shapenet/TL"

archivo_salida = "./segmented_file/segmented_file.txt"

onefile(carpeta_origen, archivo_salida)