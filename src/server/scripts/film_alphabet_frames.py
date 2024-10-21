import os
import cv2
import json
import dotenv
import mediapipe as mp

dotenv.load_dotenv()

mp_drawing = mp.solutions.drawing_utils
pose_tools = mp.solutions.pose
pose_model = pose_tools.Pose()
hand_tools = mp.solutions.hands
hand_model = hand_tools.Hands()

data = []
frame_number = 0
capture = cv2.VideoCapture(1)

while capture.isOpened():
    success, frame = capture.read()

    if not success:
        break

    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)

    frame_number += 1
    point = [
        frame_number,
        [],
        [[], []],
    ]  # [frame_number, pose_landmarks, [left_hand_landmarks, right_hand_landmarks]]

    if frame_number == 50:
        print("Started Recording")
    elif frame_number == 70:
        print("Stopped Recording")
        break
    else:
        print(frame_number)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    poses = pose_model.process(frame_rgb)
    hands = hand_model.process(frame_rgb)

    if poses.pose_landmarks:
        for i, landmark in enumerate(poses.pose_landmarks.landmark):
            point[1].append([i, landmark.x * 640, landmark.y * 480, landmark.z])

    if hands.multi_hand_landmarks:
        for landmarks in hands.multi_hand_landmarks:
            hand = landmarks.landmark

            if (
                hand[hand_tools.HandLandmark.WRIST].x
                < hand[hand_tools.HandLandmark.THUMB_CMC].x
            ):
                handedness = 0
            else:
                handedness = 1

            for i, landmark in enumerate(hand):
                point[2][handedness].append(
                    [i, landmark.x * 640, landmark.y * 480, landmark.z]
                )

    if frame_number >= 50 and frame_number <= 70:
        data.append(point)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

capture.release()

letter = input("Enter the letter: ")
path = os.path.join("../src/server/alphabets", f"{letter}.json")
with open(path, "w") as file:
    json.dump(data, file)
    print(f"Data saved to {path}")
