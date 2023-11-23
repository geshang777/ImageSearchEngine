import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
import os
from scipy.spatial import cKDTree
import pickle

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()


#  Build the k-d tree
with open('kd_tree.pkl', 'rb') as f:
    kd_tree, img_paths = pickle.load(f)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        distances, indices = kd_tree.query(query, k=10)  # k=10 for the 10 closest neighbors
        scores = [(distances[i], img_paths[index]) for i, index in enumerate(indices)]

        # dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        # ids = np.argsort(dists)[:20]  # Top 30 results
        # scores = [(dists[id], img_paths[id]) for id in ids]
        if scores[0][0]>50:
            scores.clear()
        return render_template('search.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('search.html')


if __name__=="__main__":
    app.run("0.0.0.0")
