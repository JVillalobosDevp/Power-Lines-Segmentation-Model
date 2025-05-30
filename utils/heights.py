import time, logging
import numpy as np
import open3d as o3d
from scipy.spatial import KDTree
import laspy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def no_ground_features_extraction(
    input_file,
    k_neighbors=30,
    no_ground_voxel_size=0.5,
    ground_voxel_size=0
):
    """
    Computes surface normals, curvature, and relative height for non-ground points,
    with optional voxel downsampling for both ground and non-ground points.

    Args:
        no_ground_points (np.ndarray): Non-ground points of shape (N, 3).
        ground_points (np.ndarray): Ground points of shape (N, 3).
        k_neighbors (int): Number of neighbors for estimating normals and curvature.
        no_ground_voxel_size (float): Voxel size for downsampling non-ground points.
        ground_voxel_size (float): Voxel size for downsampling ground points.

    Returns:
        tuple:
            - normals (np.ndarray): Estimated surface normals of shape (N, 3).
            - curvatures (np.ndarray): Surface curvature values (N,).
            - relative_heights (np.ndarray): Height of non-ground points relative to ground (N,).
            - downsampled_no_ground_points (np.ndarray): Final downsampled non-ground points (N, 3).
    """
    start_time = time.time()
    logger.info("Starting feature extraction: normals, curvature, and relative height")


    las = laspy.read(input_file)
    points = las.points[las.classification != 1]
    no_ground_points = np.vstack((points.x, points.y, points.z)).T
    logger.debug(f"Loaded {no_ground_points.shape[0]} points from file: {input_file}")

    points = las.points[las.classification == 1]
    ground_points = np.vstack((points.x, points.y, points.z)).T
    logger.debug(f"Loaded {ground_points.shape[0]} points from file: {input_file}")

    no_ground_points = np.asarray(no_ground_points, dtype=np.float64)
    ground_points = np.asarray(ground_points, dtype=np.float64)

    # Create point clouds
    pcd_noground = o3d.geometry.PointCloud()
    pcd_noground.points = o3d.utility.Vector3dVector(no_ground_points)

    pcd_ground = o3d.geometry.PointCloud()
    pcd_ground.points = o3d.utility.Vector3dVector(ground_points)

    # Downsample non-ground points
    if no_ground_voxel_size > 0:
        pcd_noground = pcd_noground.voxel_down_sample(voxel_size=no_ground_voxel_size)
        logger.debug(f"Downsampled no-ground points with voxel size {no_ground_voxel_size}")
    downsampled_no_ground_points = np.asarray(pcd_noground.points)

    # Downsample ground points
    if ground_voxel_size > 0:
        pcd_ground = pcd_ground.voxel_down_sample(voxel_size=ground_voxel_size)
        logger.debug(f"🔽 Downsampled ground points with voxel size {ground_voxel_size}")
    downsampled_ground_points = np.asarray(pcd_ground.points)

    """     # Estimate normals
    pcd_noground.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamKNN(knn=k_neighbors)
    )
    normals = np.asarray(pcd_noground.normals)
    logger.debug(f"Estimated normals using {k_neighbors}-NN")

    # Compute curvature for each point
    curvatures = []
    kdtree = o3d.geometry.KDTreeFlann(pcd_noground) """

    """ for i, point in enumerate(downsampled_no_ground_points):
        _, idx, _ = kdtree.search_knn_vector_3d(point, k_neighbors)
        neighbors = downsampled_no_ground_points[idx]
        centroid = neighbors.mean(axis=0)
        centered = neighbors - centroid
        cov = np.dot(centered.T, centered) / len(neighbors)
        eigenvalues, _ = np.linalg.eigh(cov)
        curvature = eigenvalues[0] / np.sum(eigenvalues)
        curvatures.append(curvature)

    logger.debug("Computed curvature for each downsampled point") """

    # Compute relative heights: non-ground Z - nearest ground Z (XY-based nearest neighbor)
    ground_tree = KDTree(downsampled_ground_points[:, :2])  
    _, nearest_indices = ground_tree.query(downsampled_no_ground_points[:, :2])
    ground_heights = downsampled_ground_points[nearest_indices, 2]
    relative_heights = downsampled_no_ground_points[:, 2] - ground_heights

    if "relative_height" not in las.point_format.dimension_names:
        extra_dim = laspy.ExtraBytesParams(name="relative_height", type=np.float32)
        las.add_extra_dim(extra_dim)
    
    las.points = las.points[las.classification != 1].copy()

    relative_height_array = np.full(len(las.points[las.classification != 1]), np.nan, dtype=np.float32)

    points = las.points
    relative_height_array[points] = relative_heights
    las['relative_height'] = relative_height_array

    las.write(output_file)

    logger.debug("📏 Computed relative heights to nearest ground")

    elapsed = time.time() - start_time
    logger.info(f"Feature extraction completed in {elapsed:.2f} seconds")

    return relative_heights, downsampled_no_ground_points

input_file = "VUELO_8_EDM.las"
output_file = "InH_Fly.las"
 
no_ground_features_extraction(
    input_file,
    k_neighbors=30,
    no_ground_voxel_size=0.5,
    ground_voxel_size=0
)