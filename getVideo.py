import cv2
import os
from nuscenes.nuscenes import NuScenes
nusc = NuScenes(version='v1.0-trainval', dataroot='./DataSets/nuScenes', verbose=True)

fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('output-6.mp4', fourcc, 5.0, (1600, 900))

# 遍历场景中的每个帧
for my_sample in nusc.sample:
    # 获取相机图片的路径
    cam_token = my_sample['data']['CAM_FRONT']
    cam_data = nusc.get('sample_data', cam_token)
    img_path = f"{nusc.dataroot}/{cam_data['filename']}"
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        # 如果图像不是空的，则写入视频
        if img is not None:
            out.write(img)
        else:
            print(f"Image is empty: {img_path}")
    else:
        print(f"File does not exist: {img_path}")

# 释放资源
out.release()