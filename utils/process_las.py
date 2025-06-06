import laspy
import os, logging, shutil 
import numpy as np
from heights import no_ground_features_extraction
import math

logging.basicConfig(
    level=logging.INFO,  # or DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def div_n_remap(input_file, outdir):
    las = laspy.read(input_file)

    header = las.header  # Obtener el encabezado original

    os.makedirs(outdir, exist_ok=True)

    #Classes of interest in pointcloud:
    classes = {
        "Ground": 1,
        "Vegetation": 2, 
        #"Tower": 2, 
        "TL": 14,   
    }

    for cls in classes:
        new_file = laspy.create(point_format=header.point_format, file_version=header.version)
        new_file.points = las.points[las.classification == classes[cls]]
        new_file.header.offsets = header.offsets  
        new_file.header.scales = header.scales
        new_file.write(f'preprocessed_clss/class_{classes[cls]}.las')
        print("extraída la clase:", cls)



    ### Remap classes in model values
    format = {
        "2": 0,  
        "1": 1,   
        "14": 3, 
    }

    for num in format:
        remap = laspy.read(f'{outdir}/class_{num}.las')
        remap.classification[:] = format[num] 
        remap.write(f'{outdir}/class_{format[num]}.las')
    
    #os.remove(f'{outdir}/class_6.laz')
    os.remove(f'{outdir}/class_2.las')
    #os.remove(f'{outdir}/class_1.las')    
    os.remove(f'{outdir}/class_14.las')


def dividir_nube_las(input_file, output_dir, threshold, sampling=False):
    
    archivo_las = laspy.read(input_file)
    total_puntos = archivo_las.header.point_count
    header_original = archivo_las.header
    
    os.makedirs(output_dir, exist_ok=True)
    print("Se leyó el folder: ", output_dir)
    # Calcular cuántos puntos por parte
    min_divisions_needed = math.ceil(total_puntos / threshold)
    puntos_por_parte = total_puntos // min_divisions_needed
    if min_divisions_needed > 1000:
        min_divisions_needed = 500
        sampling = True
    print(f"Total de puntos: {total_puntos}, Puntos por parte: {puntos_por_parte}")

    # Leer todos los puntos
    puntos = archivo_las.points

    # Dividir y guardar las partes
    for i in range(min_divisions_needed):
        inicio = i * puntos_por_parte
        fin = inicio + puntos_por_parte if i < min_divisions_needed - 1 else total_puntos
        
        if sampling:
            np.random.seed(1024+i)
            indices = np.random.choice(total_puntos, size=16384, replace=False)
            indices.sort()
            puntos_divididos = puntos[indices]
        else:
            puntos_divididos = puntos[inicio:fin]
        # Crear nuevo header para la parte dividida, copiando el original
        header_nuevo = laspy.LasHeader(point_format=archivo_las.header.point_format, version=archivo_las.header.version)
        header_nuevo.offsets = header_original.offsets  # Mantener el offset original
        header_nuevo.scales = header_original.scales    # Mantener el scale factor original
        
        # Crear nuevo archivo LAS
        archivo_las_dividido = laspy.LasData(header_nuevo)
        archivo_las_dividido.points = puntos_divididos
        
        # Guardar el archivo dividido
        output_file = os.path.join(output_dir, f"parte_{i + 1}.las")
        archivo_las_dividido.write(output_file)
        print(f"Parte {i + 1} guardada en {output_file}")

def las_a_txt(input_dir, output_dir, data):

    contador = 0

    for file in os.listdir(input_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".las") or filename.endswith(".laz"): 
            
            input_path = os.path.join(input_dir, file)
            
            inFile = laspy.read(input_path)
            test = np.vstack((inFile.x, inFile.y, inFile.z, inFile.intensity, inFile.height, inFile.classification)).T

            with open(f"{output_dir}/{data}t_{contador:06d}.txt", mode='w') as f:
                for i in range(len(test)):
                    f.write("%.6f "%float(test[i][0].item()))
                    f.write("%.6f "%float(test[i][1].item()))
                    f.write("%.6f "%float(test[i][2].item()))
                    f.write("%.6f "%float(test[i][3].item()))
                    f.write("%.6f "%float(test[i][4].item()))
                    f.write("%.6f \n"%int(test[i][5].item()))
        
            print(f"Guardado archivo: {output_dir}/{data}t_{contador:06d}.txt")
            contador += 1 
        continue
    


#### Class div and remap  ####

### Cargar el archivo .las

input_file = "normalized_cloud.las" 
outdir = "preprocessed_clss/"

div_n_remap(input_file, outdir)

#### Heights extraction ####

input_file = "preprocessed_clss/class_0.las"

data = [
    1,
    #2,
    3,
]

for num in data:
    no_ground_file = f'preprocessed_clss/class_{num}.las'
    
    no_ground_features_extraction(
        input_file,
        no_ground_file,
        k_neighbors=30,
        no_ground_voxel_size=0,
        ground_voxel_size=0
    )

os.remove('preprocessed_clss/class_0.las')

#### Divisiones de archivo las  ####

partsdir = "./preprocessed_clss"
    
for file in os.listdir(partsdir):
    filename = os.fsdecode(file)
    if filename.endswith(".las") or filename.endswith(".laz"): 
        input_file = os.path.join(partsdir, file)
        print("Procesing file: ", file)
        class_name = os.path.splitext(file)[0]
        output_dir = os.path.join("./outdir", class_name)
        threshold = 16384
        dividir_nube_las(input_file, output_dir, threshold, sampling=False)
        continue


""" #### Individual division   #### 

input_file = "preprocessed_clss/class_0.las"
output_dir = "outdir/class_0"
num_partes = 1000

#dividir_nube_las(input_file, output_dir, num_partes)  """


#### Las to txt ####
names = {
    "Ground": 1,
    "Buildings": 3,
    #"Ground": 3,
}

data = [
    "VG",
    #"BD", 
    "TL",  
]
i=0
for n in names:
    input_dir = f'outdir/class_{names[n]}' 
    #output_dir = f'Absolute_path_to_your_output_directory/{n}' 
    las_a_txt(input_dir, output_dir, data[i])
    i=i+1


os.remove('preprocessed_clss/class_1.las')
#os.remove('preprocessed_clss/class_2.las')
os.remove('preprocessed_clss/class_3.las')
shutil.rmtree('outdir/class_1')
#shutil.rmtree('outdir/class_2')
shutil.rmtree('outdir/class_3')