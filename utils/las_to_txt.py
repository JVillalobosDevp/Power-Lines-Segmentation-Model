import os
import laspy
import numpy as np

input_dir = "data/shapenet/Test"
output_dir = "data/shapenet/TL"
contador = 0
for file in os.listdir(input_dir):
    filename = os.fsdecode(file)
    if filename.endswith(".las") or filename.endswith(".laz"):
        # Procesar cada archivo LAS
        input_path = os.path.join(input_dir, file)
        inFile = laspy.read(input_path)
        test = np.vstack((inFile.x, inFile.y, inFile.z, inFile.red, inFile.blue, inFile.green, inFile.classification)).T

        with open(f"{output_dir}/test_{contador:06d}.txt", mode='w') as f:
            for i in range(len(test)):
                f.write("%.6f "%float(test[i][0].item()))
                f.write("%.6f "%float(test[i][1].item()))
                f.write("%.6f "%float(test[i][2].item()))
                f.write("%d "%int(test[i][3].item()))
                f.write("%d "%int(test[i][4].item()))
                f.write("%d "%int(test[i][5].item()))                
                f.write("%.6f \n"%int(test[i][6].item()))
        contador += 1  # Incrementar el contador para el siguiente archivo