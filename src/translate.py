import cv2
import numpy as np
from keras import ops
import mediapipe as mp
import tensorflow as tf

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

model = tf.keras.models.load_model("../model.keras")


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

            # image = cv2.flip(image, 1)

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
                handedness = results.multi_handedness[0].classification[0].label.lower()

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

                points = np.expand_dims(points, axis=0)
                predictions = model.predict(points, verbose=0)
                prediction = ops.argmax(predictions, -1)
                letters = "ABCDEFGHIKLMNOPQRSTUVWXY"
                letter = letters[prediction[0]]
                probability = predictions[0][prediction[0]]

                if probability > 0.6:
                    height, width, _ = image.shape
                    text_x = int(hand.landmark[0].x * width) - 100
                    text_y = int(hand.landmark[0].y * height) + 50
                    cv2.putText(
                        img=image,
                        text=f"{letter} {round(probability * 100 * 100) / 100}%",
                        org=(text_x, text_y),
                        fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=5,
                        color=(0, 255, 0),
                        thickness=4,
                        lineType=cv2.LINE_4,
                    )

            cv2.imshow("Translation", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break


if __name__ == "__main__":
    main()
