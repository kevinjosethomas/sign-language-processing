import os
import glob
import json
import numpy as np
from tqdm import tqdm
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


base_options = python.BaseOptions(model_asset_path="../mediapipe.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)


def vectorize_image(image_path: str, index: int):
    original_path_split = image_path.split("/")

    alphabet = original_path_split[-2]

    if alphabet == "J" or alphabet == "Z":
        return

    category = original_path_split[-3]

    image = mp.Image.create_from_file(image_path)
    results = detector.detect(image)
    if not results.handedness:
        return

    handedness = results.handedness[0][0].category_name.lower()

    new_path = f"../data/dataset/{handedness}/{category}/{alphabet}/{index}"

    points = []

    if not results.hand_landmarks:
        return image_path

    for landmark in results.hand_landmarks[0]:
        points.append([landmark.x, landmark.y, landmark.z])

    points = np.array(points)

    min_x = np.min(points[:, 0])
    max_x = np.max(points[:, 0])
    min_y = np.min(points[:, 1])
    max_y = np.max(points[:, 1])
    for i in range(len(points)):
        points[i][0] = (points[i][0] - min_x) / (max_x - min_x)
        points[i][1] = (points[i][1] - min_y) / (max_y - min_y)

    np.save(new_path, points)


def start():
    files = []
    for file in glob.glob("../data/raw1/**/*.png", recursive=True):
        if "Blank" in file:
            continue
        files.append(file)

    progress_bar = tqdm(total=len(files))
    progress_bar.set_description("Vectorizing Dataset")

    for i, file in enumerate(files):
        vectorize_image(file, i + 1)
        progress_bar.update(1)


if __name__ == "__main__":
    start()
