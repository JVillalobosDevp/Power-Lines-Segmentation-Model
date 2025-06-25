import laspy 
import os, argparse, logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default=None)
parser.add_argument('--output_dir', default=None)
args, opts = parser.parse_known_args()

def div_n_remap(input_file, outdir):
    # Abrir archivo .las
    las = laspy.read(input_file)

    # Crear un nuevo archivo .las con los puntos filtrados
    header = las.header  # Obtener el encabezado original

    os.makedirs(outdir, exist_ok=True)

    #Classes of interest in pointcloud:
    classes = {
        "Ground": 2,
        "Vegetation": 6, 
        "Wire+Tower": 18,   
    }

    for cls in classes:
        new_file = laspy.create(point_format=header.point_format, file_version=header.version)
        new_file.points = las.points[las.classification == classes[cls]]
        new_file.header.offsets = header.offsets  
        new_file.header.scales = header.scales
        new_file.write(f'{outdir}/class_{classes[cls]}.las')
        logger.info(f"Extracted class: {cls}")



    #Remap classes in model values
    format = {
        "2": 0,  
        "4": 1,   
        "18": 3, 
    }

    for num in format:
        remap = laspy.read(f'{outdir}/class_{num}.las')
        remap.classification[:] = format[num] 
        remap.write(f'{outdir}/class_{format[num]}.las')

    logger.info("Classes remaped")    
    
    for cls in classes:
        os.remove(f'{outdir}/class_{classes[cls]}.las')
        os.remove(f'{outdir}/class_{classes[cls]}.las')
        os.remove(f'{outdir}/class_{classes[cls]}.las')    
        #os.remove(f'{outdir}/class_0.las')
   

def dividir_nube_las(input_file, output_dir, num_partes):
    # Abrir el archivo LAS para obtener la cantidad de puntos y el header original
    archivo_las = laspy.read(input_file)
    total_puntos = archivo_las.header.point_count
    header_original = archivo_las.header  # Guardar el header original
    
    #Crea carpeta de salida
    os.makedirs(output_dir, exist_ok=True)
    print("Readed Folder: ", output_dir)
    # Calcular cuántos puntos por parte
    puntos_por_parte = total_puntos // num_partes

    # Leer todos los puntos
    puntos = archivo_las.points

    # Dividir y guardar las partes
    for i in range(num_partes):
        inicio = i * puntos_por_parte
        fin = inicio + puntos_por_parte if i < num_partes - 1 else total_puntos
        puntos_divididos = puntos[inicio:fin]
        
        # Crear nuevo header para la parte dividida, copiando el original
        header_nuevo = laspy.LasHeader(point_format=archivo_las.header.point_format, version=archivo_las.header.version)
        header_nuevo.offsets = header_original.offsets
        header_nuevo.scales = header_original.scales
        
        # Crear nuevo archivo LAS
        archivo_las_dividido = laspy.LasData(header_nuevo)
        archivo_las_dividido.points = puntos_divididos
        
        # Guardar el archivo dividido
        output_file = os.path.join(output_dir, f"parte_{i + 1}.las")
        archivo_las_dividido.write(output_file)
        logger.debug(f"Parte {i + 1} guardada en {output_file}")

def las_a_txt(input_dir, output_dir, data):

    contador = 0
    print(f"Reading files from {input_dir}") 

    for file in os.listdir(input_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".las") or filename.endswith(".laz"):
            # Procesar cada archivo LAS
            input_path = os.path.join(input_dir, file)
            # Leer el archivo LAS
            inFile = laspy.read(input_path)
            test = np.vstack((inFile.x, inFile.y, inFile.z, inFile.red, inFile.blue, inFile.green, inFile.classification)).T

            with open(f"{output_dir}/{data}_{contador:06d}.txt", mode='w') as f:
                for i in range(len(test)):
                    f.write("%.6f "%float(test[i][0].item()))
                    f.write("%.6f "%float(test[i][1].item()))
                    f.write("%.6f "%float(test[i][2].item()))
                    f.write("%d "%int(test[i][3].item()))
                    f.write("%d "%int(test[i][4].item()))
                    f.write("%d "%int(test[i][5].item()))                
                    f.write("%.6f \n"%int(test[i][6].item()))
        
            logger.debug(f"Guardado archivo: {output_dir}/{data}_{contador:06d}.txt")
            contador += 1  # Incrementar el contador para el siguiente archivo
        continue
    # Inicializar contador para los nombres de los archivos





#### Class div and remap  ####

# Cargar el archivo .las

input_file = args.input_file
outdir = args.output_dir

div_n_remap(input_file, outdir)

#### Divisiones de archivo las  ####

partsdir = "data/preprocessed_clss"
    
for file in os.listdir(partsdir):
    filename = os.fsdecode(file)
    if filename.endswith(".las") or filename.endswith(".laz"): 
        input_file = os.path.join(partsdir, file)
        print("Procesing file: ", file)
        class_name = os.path.splitext(file)[0]
        output_dir = os.path.join("data/outdir", class_name)
        num_partes = 500
        dividir_nube_las(input_file, output_dir, num_partes)
        continue


#### Las to txt ####
names = {
    #"Ground": 0,
    "Vegetation": 1,
    "TL": 3,
}

data = [
    #"GD",
    "VG", 
    "TL",  
]
i=0
for n in names:
    input_dir = f'data/outdir/class_{names[n]}'
    output_dir = f'data/shapenet/{n}'  
    las_a_txt(input_dir, output_dir, data[i])
    i=i+1
