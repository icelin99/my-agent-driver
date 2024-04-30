import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from nuscenes.utils.geometry_utils import view_points

nusc = NuScenes(version='v1.0-trainval', dataroot='./DataSets/nuScenes', verbose=True)

index_list = []  
with open('sample-index.txt', 'r') as file:
    for line in file:
        index = int(line.strip())  # 去除可能的空白字符，并转换为整数
        index_list.append(index)

output_directory = "./point-cloud-image"
os.makedirs(output_directory, exist_ok=True)  # 确保目录存在，如果不存在则创建

for i,index in enumerate(index_list):
    # 获取点云数据
    my_sample = nusc.sample[index]
    lidar_data = nusc.get('sample_data', my_sample['data']['LIDAR_TOP'])
    lidar_path = f"{nusc.dataroot}/{lidar_data['filename']}"
    pc = LidarPointCloud.from_file(lidar_path)
    points = pc.points[0:3, :]
    z_filter = points[2] < 1.0  # 过滤一些点以清晰显示
    points = points[:, z_filter]

    # 创建俯视图图像
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(points[0], points[1], s=1)
    ax.set_aspect('equal')
    ax.set_xlim([-50, 50])  # 可以调整以更好地控制显示范围
    ax.set_ylim([-50, 50])

    filename = f"point_cloud_top_{i}.png"
    filepath = os.path.join(output_directory, filename)
    # 保存图像
    plt.savefig(filepath)
    plt.close(fig)  # 关闭图形，释放内存

# my_sample = nusc.sample[10]

# # 获取激光雷达数据
# lidar_data = nusc.get('sample_data', my_sample['data']['LIDAR_TOP'])
# lidar_path = f"{nusc.dataroot}/{lidar_data['filename']}"

# if os.path.exists(lidar_path):
#     pc = LidarPointCloud.from_file(lidar_path)

#     # 投影到水平面以生成俯视图
#     points = pc.points[0:3, :]  # 取x, y, z
#     z_filter = points[2] < 1.0  # 可选的高度过滤
#     points = points[:, z_filter]

#     # 绘制俯视图
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.scatter(points[0], points[1], s=1)
#     ax.set_aspect('equal')
#     ax.set_title('Top-Down View of LiDAR Data')
#     plt.xlabel('X [m]')
#     plt.ylabel('Y [m]')
#     plt.show()
# else:
#     print("file not exist:",lidar_path)