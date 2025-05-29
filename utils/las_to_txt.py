import laspy
import numpy as np

inputFile = "aligned_test_cloud.las"
outFolder = "preprocessed_clss"
inFile = laspy.read(inputFile)
test = np.vstack((inFile.x, inFile.y, inFile.z, inFile.red, inFile.blue, inFile.green, inFile.classification)).T

with open(f"{outFolder}/test.txt", mode='w') as f:
    for i in range(len(test)):
        f.write("%.6f "%float(test[i][0].item()))
        f.write("%.6f "%float(test[i][1].item()))
        f.write("%.6f "%float(test[i][2].item()))
        f.write("%d "%int(test[i][3].item()))
        f.write("%d "%int(test[i][4].item()))
        f.write("%d "%int(test[i][5].item()))                
        f.write("%.6f \n"%int(test[i][6].item()))