import os
import cv2
import json
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
pose_tools = mp.solutions.pose
pose_model = pose_tools.Pose()
hand_tools = mp.solutions.hands
hand_model = hand_tools.Hands()

videos = os.listdir("../data/signs/videos/")

points = {}
for i, file in enumerate(videos):
    video = os.path.join("../data/signs/videos/", file)
    word = file.split(".")[0]

    data = []
    frame_number = 0
    capture = cv2.VideoCapture(video)
    while capture.isOpened():
        success, frame = capture.read()

        if not success:
            break

        frame = cv2.resize(frame, (640, 480))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        poses = pose_model.process(frame_rgb)
        hands = hand_model.process(frame_rgb)

        point = {"frame": frame_number, "pose": [], "hand": {"left": [], "right": []}}

        if poses.pose_landmarks:
            for landmarks in poses.pose_landmarks.landmark:
                point["pose"].append(
                    {"x": landmarks.x, "y": landmarks.y, "z": landmarks.z}
                )

        if hands.multi_hand_landmarks:
            for landmarks in hands.multi_hand_landmarks:
                hand = landmarks.landmark

                if (
                    hand[hand_tools.HandLandmark.WRIST].x
                    < hand[hand_tools.HandLandmark.THUMB_CMC].x
                ):
                    handedness = "left"
                else:
                    handedness = "right"

                for joint, landmark in enumerate(hand):
                    point["hand"][handedness].append(
                        {
                            "joint": joint,
                            "x": landmark.x,
                            "y": landmark.y,
                            "z": landmark.z,
                        }
                    )

        data.append(point)
        frame_number += 1

    capture.release()
    points[word] = data

with open("../data/signs/points/raw_points.json", "w") as f:
    json.dump(points, f)
