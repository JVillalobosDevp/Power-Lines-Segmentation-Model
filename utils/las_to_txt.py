import laspy
import numpy as np

inputFile = "preprocessed_clss/class_1.las"
outFolder = "preprocessed_clss"
inFile = laspy.read(inputFile)
#print(list(inFile.point_format.dimension_names))
height = inFile.height
test = np.vstack((inFile.x, inFile.y, inFile.z, inFile.intensity, height, inFile.classification)).T

with open(f"{outFolder}/test.txt", mode='w') as f:
    for i in range(len(test)):
        f.write("%.6f "%float(test[i][0].item()))
        f.write("%.6f "%float(test[i][1].item()))
        f.write("%.6f "%float(test[i][2].item()))
        f.write("%.6f "%float(test[i][3].item()))
        f.write("%.6f "%float(test[i][4].item()))
        f.write("%.6f \n"%int(test[i][5].item()))