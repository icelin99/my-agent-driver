import cv2
import os
import numpy as np
import importlib
import matplotlib.pyplot as plt
from nuscenes.nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud
from nuscenes.utils.geometry_utils import view_points
# importlib.reload(nuscenes.nuscenes)
import nuscenes.nuscenes as nuscenes_module
importlib.reload(nuscenes_module)

nusc = NuScenes(version='v1.0-trainval', dataroot='./DataSets/nuScenes', verbose=True)

index_list = []  
with open('./sample-index.txt', 'r') as file:
    for line in file:
        index = int(line.strip())  # 去除可能的空白字符，并转换为整数
        index_list.append(index)

scene_token_list = []
for index in index_list:
    sample = nusc.sample[index]
    for scene in nusc.scene:
        if sample['token'] == scene['first_sample_token']:
            scene_token_list.append(scene['token'])
            continue

list_tk = []
for index, token in enumerate(scene_token_list):
    list_tk.append(token)
    nusc.render_egoposes_on_map(log_location='boston-seaport',scene_tokens=list_tk,out_path=f"./vue-app/public/assets/map-image/map-{index}.png")