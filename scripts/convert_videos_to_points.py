import os
import cv2
import json
import dotenv
import psycopg2
from tqdm import tqdm
import mediapipe as mp

dotenv.load_dotenv()

conn = psycopg2.connect(
    database="signs",
    host="localhost",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432,
)
cur = conn.cursor()

mp_drawing = mp.solutions.drawing_utils
pose_tools = mp.solutions.pose
pose_model = pose_tools.Pose()
hand_tools = mp.solutions.hands
hand_model = hand_tools.Hands()


videos = os.listdir("../data/signs/videos/")


bar = tqdm(total=len(videos))

try:
    for i, file in enumerate(videos):
        bar.update(1)
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

            frame_number += 1
            point = [
                frame_number,
                [],
                [[], []],
            ]  # [frame_number, pose_landmarks, [left_hand_landmarks, right_hand_landmarks]]

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
            else:
                continue

            data.append(point)

        capture.release()
        try:
            cur.execute(
                "INSERT INTO signs (word, points) VALUES (%s, %s)",
                (word, json.dumps(data)),
            )
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
            continue
except Exception as e:
    print(e)
