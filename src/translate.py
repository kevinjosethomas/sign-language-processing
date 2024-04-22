import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def main():
    cap = cv2.VideoCapture(1)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1,
    ) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Empty camera frame")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(
                            color=(0, 0, 255), thickness=8, circle_radius=8
                        ),
                        mp_drawing.DrawingSpec(
                            color=(0, 255, 0), thickness=6, circle_radius=2
                        ),
                    )

                hand = results.multi_hand_landmarks[0]

                points = []
                for landmark in hand.landmark:
                    points.append([landmark.x, landmark.y, landmark.z])

                points = np.array(points)

                min_x = np.min(points[:, 0])
                max_x = np.max(points[:, 0])
                min_y = np.min(points[:, 1])
                max_y = np.max(points[:, 1])
                for i in range(len(points)):
                    points[i][0] = (points[i][0] - min_x) / (max_x - min_x)
                    points[i][1] = (points[i][1] - min_y) / (max_y - min_y)

            cv2.imshow("Translation", cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break


if __name__ == "__main__":
    main()
