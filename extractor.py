from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
import os

if __name__ == '__main__':
    fe = FeatureExtractor()

    # 定义源目录和目标目录
    source_dir = './static/images'
    target_dir = './static/feature'

    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 遍历源目录中的所有文件夹和文件
    for subdir, dirs, files in os.walk(source_dir):
        for file in files:
            # 构建完整的文件路径
            file_path = os.path.join(subdir, file)

            # 检查是否为图片文件（这里假设图片文件以.jpg, .jpeg, .png, .gif等结尾）
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # 构建目标文件夹路径，它应该镜像源文件夹的结构
                destination_folder = os.path.join(target_dir, os.path.relpath(subdir, source_dir))
                os.makedirs(destination_folder, exist_ok=True)  # 确保目标文件夹存在
                feature = fe.extract(image=Image.open(file_path))
                relative_path = os.path.relpath(subdir, source_dir)
                feature_path = Path("./static/feature") /relative_path/(
                            file[:-4] + ".npy")  # e.g., ./static/feature/xxx.npy
                print(feature_path)
                np.save(feature_path, feature)
