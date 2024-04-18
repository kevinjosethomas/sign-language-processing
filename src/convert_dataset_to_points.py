import os
import glob
import json
import numpy as np
from tqdm import tqdm
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Initialize Model
base_options = python.BaseOptions(model_asset_path="../mediapipe.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)


def vectorize_image(image_path: str, index: int):
    original_path_split = image_path.split("/")
    new_path = (
        "/".join(original_path_split[:-1]).replace("signs", "points") + "/" + f"{index}"
    )

    image = mp.Image.create_from_file(image_path)
    results = detector.detect(image)

    points = []

    if not results.hand_landmarks:
        return image_path

    for landmark in results.hand_landmarks[0]:
        points.append([landmark.x, landmark.y, landmark.z])

    points = np.array(points)

    # Normaliza data into a standard range
    min_x = np.min(points[:, 0])  # Find lowest x-value
    max_x = np.max(points[:, 0])  # Find highest x-value
    min_y = np.min(points[:, 1])  # Find lowest y-value
    max_y = np.max(points[:, 1])  # Find highest y-value
    for i in range(len(points)):
        points[i][0] = (points[i][0] - min_x) / (max_x - min_x)
        points[i][1] = (points[i][1] - min_y) / (max_y - min_y)

    np.save(new_path, points)


def start():
    files = []
    for file in glob.glob("../data/signs/**/*.png", recursive=True):
        if "Blank" in file:
            continue
        files.append(file)

    progress_bar = tqdm(total=len(files))
    progress_bar.set_description("Vectorizing Dataset")
    failed_images = []

    for i, file in enumerate(files):
        failed = vectorize_image(file, i + 1)
        if failed:
            failed_images.append(failed)
        progress_bar.update(1)

    with open("failed_images.txt", "w") as f:
        json.dump(failed_images, f)


if __name__ == "__main__":
    start()
