import laspy
import numpy as np
import json


##### Make structure as as fucntion to call it from process_las.py

las = laspy.read("nether_int.las")
points = np.vstack((las.x, las.y, las.z)).T
og_offset = np.vstack((las.header.x_offset, las.header.y_offset, las.header.z_offset)).T
new_las = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
new_las.header = las.header
new_las.header.scale = las.header.scale
new_las.intensity = las.intensity

nomalized_points = points - og_offset

# Estimate new offset and scale
x_min, y_min, z_min = nomalized_points.min(axis=0)

offset = np.array([x_min, y_min, z_min])  # You can also use mean
if las.header.z_offset == 0:
    new_las.header.x_offset = offset[0]
    new_las.header.y_offset = offset[1]
    new_las.header.z_offset = las.header.z_offset
    new_las.z = las.z
else:
    new_las.header.x_offset = offset[0]
    new_las.header.y_offset = offset[1]
    new_las.header.y_offset = offset[2]
    new_las.z = nomalized_points[:, 2]

new_las.x = nomalized_points[:, 0]
new_las.y = nomalized_points[:, 1]

#Copy attributes and normalize it to 8 bits
""" new_las.red   = (las_test.red / 256).astype(np.uint8)
new_las.green = (las_test.green / 256).astype(np.uint8)
new_las.blue  = (las_test.blue / 256).astype(np.uint8) """

if 'classification' in las.point_format.dimension_names:
    new_las.classification = las.classification

new_las.write("./normalized_cloud.las")

### change later in order to recover the original offset in inference tests
cloud_data = og_offset.tolist() + new_las.header.scale.tolist()
with open("offset_diff.json", "w") as f:
    json.dump(cloud_data, f, indent=2)