"""
    Adrián Riaño Martínez
    Hoja de problemas 2
    Ejercicio 9
    python outlier_removal.py --ipc=PLYPointCloud --points=16 --radius=0.05 --opc=resulting_cloud.pcd
"""
import open3d as o3d
import numpy as np
import argparse


def radius_outlier_removal(point_cloud, min_number_points, radius):
    points = np.asarray(point_cloud.points)  # Convert Open3D point cloud to numpy array
    kdtree = o3d.geometry.KDTreeFlann(point_cloud) # Build KDTree

    inlier_indices = [] # List to store indices of inliers
    for i in range(len(points)): # Iterate through each point in the cloud
        k, idx, _ = kdtree.search_radius_vector_3d(points[i], radius)  #Query neighbors within the specified radius
        if k >= min_number_points:  #Check neighbors > minimum required
            inlier_indices.append(i)
    return point_cloud.select_by_index(inlier_indices)


def main(args):
    ipc = args['ipc']
    points = args['points']
    radius = args['radius']
    opc = args['opc']

    if ipc == 'PLYPointCloud':
        dataset = o3d.data.PLYPointCloud()
    elif ipc == 'EaglePointCloud':
        dataset = o3d.data.EaglePointCloud()
    else:
        raise Exception("not valid ipc argument :(")

    pcd = o3d.io.read_point_cloud(dataset.path)
    filtered_point_cloud = radius_outlier_removal(pcd, points, radius)
    o3d.io.write_point_cloud(opc, filtered_point_cloud)
    o3d.visualization.draw(filtered_point_cloud)


if __name__ == "__main__":
    desc = 'open3d script'
    parser = argparse.ArgumentParser(description=desc)

    args_values = {'nargs': 1, 'required': True}
    parser.add_argument('--ipc', type=str, help='source inference', **args_values)
    parser.add_argument('--points', type=int, help='number of points', **args_values)
    parser.add_argument('--radius', type=float, help='set radius', **args_values)
    parser.add_argument('--opc', type=str, help='output', **args_values)

    args = {i: j[0] for i, j in vars(parser.parse_args()).items() if j is not None}

    main(args)
