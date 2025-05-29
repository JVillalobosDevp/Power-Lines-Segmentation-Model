import laspy

format = {
    "3": 8,  
}

def filter(input_las):
    las = laspy.read(input_las)

    umbral_altura = 2154.2

    new_file = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
    new_file.points = las.points[(las.z > umbral_altura) & (las.classification == 3)]
    new_file.header.offsets = las.header.offsets  
    new_file.header.scales = las.header.scales
    new_file.write('segmented_file/cables.las')

    for num in format:
        remap = laspy.read('segmented_file/cables.las')
        remap.header.offsets = new_file.header.offsets  
        remap.header.scales = new_file.header.scales
        remap.classification[:] = format[num] 
        remap.write('segmented_file/cables.las')

    print("Remap done")



    print(f"El archivo ha sido filtrado exitosamente")

input_las = "restored_test_cloud.las"

filter(input_las)