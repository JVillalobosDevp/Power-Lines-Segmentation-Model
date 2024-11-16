# Power Lines Segmentation Model Based in PVCNN


## Prerequisites

The following libraries were used in this project
- 3.7 ≤ Python < 3.10 (3.8.18 used)	
- [PyTorch](https://github.com/pytorch/pytorch) ≥ 1.3 
- [numba](https://github.com/numba/numba)
- [numpy](https://github.com/numpy/numpy)
- [scipy](https://github.com/scipy/scipy)
- [six](https://github.com/benjaminp/six)
- [tensorboardX](https://github.com/lanpa/tensorboardX) ≥ 1.2
- [tqdm](https://github.com/tqdm/tqdm)
- [plyfile](https://github.com/dranjan/python-plyfile)
- [h5py](https://github.com/h5py/h5py)
- [ninja](https://github.com/ninja-build/ninja.git)
- [setuptools](https://github.com/pypa/setuptools.git) == 59.5.0 (For Windows)
- CUDA ≥ 11.8


## Data Preparation


### ShapeNet

We adapt the data from point clouds in order to be readable for the model using shapenet configurations.

One can run [utils/process_las](utils/process_las.py) to read read data from las files and split it into parts to improve speed and reduce the load on the gpu when uploading the data to be classified

These data must then be added to the folder where the data is read [04460130](data/shapenet/shapenetcore_partanno_segmentation_benchmark_v0_normal/04460130).


## Code

The core code of PVCNN model is [modules/pvconv.py](modules/pvconv.py). Its key idea costs only a few lines of code:

```python
    voxel_features, voxel_coords = voxelize(features, coords)
    voxel_features = voxel_layers(voxel_features)
    voxel_features = trilinear_devoxelize(voxel_features, voxel_coords, resolution)
    fused_features = voxel_features + point_layers(features)
```

## Model

Here are some stats after the model training compared to other classes from shapenet



|           Class           |                        mIoU                       | 
| :-----------------------: | :-----------------------------------------------: |  
|  Bag                      |     83.1      | |     82.62     | |     86.32     |
|  Cap                      |     82.55     | |     84.16     | |     80.15     |
|  Car                      |     79.02     | |     80.15     | |     80.1      |
|  Tower                    |     84.17     | |     86.53     | |   **89.64**   |
                                                                            

## Testing Models

This code is focused only in the classification, for futher training to the model you can refer to the original repo ([PVCNN](https://github.com/mit-han-lab/pvcnn.git))

For instance, to evaluate and segment a cloud one can run:

```
python evaluate.py 
```
Always have in mind that the default configs are stablished to use CUDA device 0, and the [c0p5](configs/shapenet/pvcnn/c0p5.py) configuration from shapenet. However, can be changed as required in [evaluate.py](evaluate.py) file


Finally, after running the code you will get numerous files with the model predictions, as well as a text file with the union and subsequent coloring of these according to classification.

If you desire a las file again, you can run [utils/txt_to_las.py](utils/txt_to_las.py)


## License

This repository is released under the MIT license. See [LICENSE](LICENSE) for additional details.


## Acknowledgement

- The main model used in this repository can be found here: [PVCNN: Point-Voxel CNN for Efficient 3D Deep Learning](https://github.com/mit-han-lab/pvcnn.git)

- The data configuration for training was done thanks to the [CloudCompare](https://www.danielgm.net/cc/) software.
