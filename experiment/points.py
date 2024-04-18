import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

base_options = python.BaseOptions(model_asset_path="../mediapipe.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

image = mp.Image.create_from_file("image.png")
results = detector.detect(image)

points = []
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

# Plot the Hand
img = np.zeros([244, 244, 3], dtype=np.uint8)
img.fill(255)
for hc in mp.solutions.hands.HAND_CONNECTIONS:
    cv2.line(
        img,
        (int((points[hc[0]][0]) * 244), int((points[hc[0]][1]) * 244)),
        (int((points[hc[1]][0]) * 244), int((points[hc[1]][1]) * 244)),
        (0, 0, 255),
        4,
    )
cv2.imshow("", img)
cv2.waitKey(0)
