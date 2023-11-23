import os
import numpy as np
from scipy.spatial import cKDTree
import pickle
from pathlib import Path

features = []
index_names = []
for subdir, dirs, files in os.walk('./static/feature/'):
    for filename in files:

        if filename.endswith('.npy'):
            file_path = os.path.join(subdir,filename)

            feature = np.load(file_path)
            features.append(feature)

            relative_path = os.path.relpath(subdir, './static/feature/')
            feature_path = Path("./static/images") / relative_path / (
                    filename[:-4] + ".jpg")
            index_names.append((feature_path))
            print(feature_path)

# Convert list of features to a numpy array
features = np.vstack(features)

kd_tree = cKDTree(features)
with open('kd_tree.pkl', 'wb') as f:
    pickle.dump((kd_tree, index_names), f)