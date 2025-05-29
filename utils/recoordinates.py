import laspy
import numpy as np
import json
 
las_train = laspy.read("/home/binahlab/AI-Labs/clever-data/electrical-elements/data/nederland/geotiles-2025_05_08/raw/pointclouds/37AZ1_20.LAZ")
train_points = np.vstack((las_train.x, las_train.y, las_train.z)).T
train_offset = np.mean(train_points, axis=0)

las_test = laspy.read("class_013.las")
test_points = np.vstack((las_test.x, las_test.y, las_test.z)).T
test_offset = np.mean(test_points, axis=0)

new_las = laspy.create(point_format=las_test.header.point_format, file_version=las_test.header.version)
new_las.header = las_test.header

offset_diff = train_offset - test_offset

aligned_test_points = test_points + offset_diff

# Estimate new offset and scale
x_min, y_min, z_min = aligned_test_points.min(axis=0)
x_max, y_max, z_max = aligned_test_points.max(axis=0)

offset = np.array([x_min, y_min, z_min])  # You can also use mean

new_las.header.x_offset = offset[0]
new_las.header.y_offset = offset[1]
new_las.header.z_offset = offset[2]

new_las.x = aligned_test_points[:, 0]
new_las.y = aligned_test_points[:, 1]
new_las.z = aligned_test_points[:, 2]

#Copy attributes and normalize it to 8 bits
new_las.red   = (las_test.red / 256).astype(np.uint8)
new_las.green = (las_test.green / 256).astype(np.uint8)
new_las.blue  = (las_test.blue / 256).astype(np.uint8)

if 'classification' in las_test.point_format.dimension_names:
    new_las.classification = las_test.classification

new_las.write("./aligned_test_cloud.las")

offset_diff = train_offset - test_offset
with open("offset_diff.json", "w") as f:
    json.dump(offset_diff.tolist(), f)
