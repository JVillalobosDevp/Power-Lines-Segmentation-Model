import laspy
import numpy as np
import json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default=None)
parser.add_argument('--output_file', default=None)
args, opts = parser.parse_known_args()
##### Make structure as as fucntion to call it from process_las.py

las = laspy.read(f"{args.input_file}")
points = np.vstack((las.x, las.y, las.z)).T
og_offset = np.array([las.header.x_offset, las.header.y_offset, las.header.z_offset])
new_las = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
new_las.header = las.header
new_las.header.scale = las.header.scale

nomalized_points = points - og_offset

# Estimate new offset and scale
x_min, y_min, z_min = nomalized_points.min(axis=0)
offset = np.array([x_min, y_min, z_min])
if las.header.z_offset == 0:
    new_las.header.x_offset = offset[0]
    new_las.header.y_offset = offset[1]
    new_las.header.z_offset = las.header.z_offset
else:
    new_las.header.x_offset = offset[0]
    new_las.header.y_offset = offset[1]
    new_las.header.z_offset = nomalized_points[:, 2]

new_las.x = nomalized_points[:, 0] - x_min
new_las.y = nomalized_points[:, 1] - y_min
new_las.z = nomalized_points[:, 2] - z_min

if (las.red).max(axis=0) > 255:
    new_las.red   = (las.red / 256).astype(np.uint8)
    new_las.green = (las.green / 256).astype(np.uint8)
    new_las.blue  = (las.blue / 256).astype(np.uint8)
else:
    new_las.red   = las.red
    new_las.green = las.green
    new_las.blue  = las.blue

if 'classification' in las.point_format.dimension_names:
    new_las.classification = las.classification

new_las.write(f"{args.output_file}")

cloud_data = {
    "offset": og_offset.tolist(),
    "scale": new_las.header.scale.tolist(),
    "min": [x_min, y_min, z_min],
}

with open("offset_diff.json", "w") as f:
    json.dump(cloud_data, f, indent=2)