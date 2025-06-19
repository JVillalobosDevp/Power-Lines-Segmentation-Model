import laspy
import numpy as np
import json

# Load the aligned point cloud
las = laspy.read("data/normalized_cloud.las")
points = np.vstack((las.x, las.y, las.z)).T

# Load saved offset difference
with open("offset_diff.json") as f:
    cloud_data = json.load(f)
offset = np.array(cloud_data["offset"])
og_scale = np.array(cloud_data["scale"])
min = np.array(cloud_data["min"])

# Restore original coordinates
restore_offset = points + min

restored_points = restore_offset + offset

# Create a new LAS file and copy header and metadata
restored_las = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
restored_las.header = las.header  # reuse safely here since we're restoring

# Compute new offset and scale
min_xyz = restored_points.min(axis=0)
scale = og_scale  # 1 mm precision

restored_las.header.x_offset = offset[0]
restored_las.header.y_offset = offset[1]
restored_las.header.z_offset = offset[2]

restored_las.header.x_scale = scale[0]
restored_las.header.y_scale = scale[1]
restored_las.header.z_scale = scale[2]

# Assign restored coordinates
restored_las.x = restored_points[:, 0]
restored_las.y = restored_points[:, 1]
restored_las.z = restored_points[:, 2]

# Copy over attributes
restored_las.red = (las.red.astype(np.uint16) * 256)
restored_las.green = (las.green.astype(np.uint16) * 256)
restored_las.blue = (las.blue.astype(np.uint16) * 256)

if 'classification' in las.point_format.dimension_names:
    restored_las.classification = las.classification

# Write the restored cloud
restored_las.write("data/restored_test_cloud.las")

