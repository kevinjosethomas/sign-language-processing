import glob
import uuid
import numpy as np
from tqdm import tqdm
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


base_options = python.BaseOptions(model_asset_path="../mediapipe.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)


def vectorize_image(image_path: str):
    original_path_split = image_path.split("/")

    alphabet = original_path_split[-2]

    letters = "ABCDEFGHIKLMNOPQRSTUVWXY"
    if alphabet not in letters:
        return

    image = mp.Image.create_from_file(image_path)
    results = detector.detect(image)

    # handedness = results.handedness[0][0].category_name.lower()

    if not results.hand_landmarks:
        return 1

    new_path = f"../data/merged/{alphabet}/{uuid.uuid4().hex[:8]}"

    points = []

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
    for file in glob.glob("../data/raw3/train/**/*.jpg", recursive=True):
        if "Blank" in file:
            continue
        files.append(file)

    progress_bar = tqdm(total=len(files))
    progress_bar.set_description("Vectorizing Dataset")

    failed_count = 0
    for file in files:
        failed = vectorize_image(file)
        if failed:
            failed_count += 1

        if failed_count % 1000 == 0 and failed_count > 1000:
            print(f"Failed Vectorization: {failed_count} Images")
        progress_bar.update(1)

    print("Failed Vectorization: ", failed_count)


if __name__ == "__main__":
    start()
