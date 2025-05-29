import sys, os
import laspy
import numpy as np

sys.path.append('/home/binahlab/AI-Labs/360i-Experiments/src/math_classify')

from buid_vs_veg_methods import no_ground_features_extraction # type: ignore

inputFile = "/home/binahlab/AI-Labs/clever-data/electrical-elements/data/flynorth/HIDRALPOR/processed/classify/math-classify-v2/VUELO_8_EDM-hash-map0.laz"
inFile = laspy.read(inputFile)
no_ground = inFile.points[inFile.classification != 2]
no_ground_points = np.ndarray(no_ground.x, no_ground.y, no_ground.z)
ground = inFile.points[inFile.classification == 2]
ground_points = np.ndarray(ground.x, ground.y, ground.z)
no_ground_voxel_size=0

no_ground_features_extraction(no_ground_points, ground_points, no_ground_voxel_size)