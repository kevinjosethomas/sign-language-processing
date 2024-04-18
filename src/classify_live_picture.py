import cv2
import time
import numpy as np
from keras import ops
import mediapipe as mp
import tensorflow as tf
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2


class Landmarker:
    def __init__(self):
        self.result = mp.tasks.vision.HandLandmarkerResult
        self.landmarker = mp.tasks.vision.HandLandmarker
        self.initialize()

    def initialize(self):

        def update_result(
            result: mp.tasks.vision.HandLandmarkerResult,
            output_image: mp.Image,
            timestamp_ms: int,
        ):
            self.result = result

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path="../mediapipe.task"),
            running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            result_callback=update_result,
        )

        self.landmarker = self.landmarker.create_from_options(options)

    def detect_async(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.landmarker.detect_async(
            image=mp_image, timestamp_ms=int(time.time() * 1000)
        )

    def close(self):
        self.landmarker.close()


def draw_landmarks_on_image(
    image, detection_result: mp.tasks.vision.HandLandmarkerResult
):
    try:
        if not detection_result.hand_landmarks:
            return image

        annotated_image = np.copy(image)
        hand = detection_result.hand_landmarks[0]

        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(x=point.x, y=point.y, z=point.z)
                for point in hand
            ]
        )
        mp.solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style(),
        )

        return annotated_image
    except:
        return image


def recognize_asl_signs(
    image, model, detection_result: mp.tasks.vision.HandLandmarkerResult
):
    try:
        if not detection_result.hand_landmarks:
            return image

        hand = detection_result.hand_landmarks[0]

        points = []
        for point in hand:
            points.append([point.x, point.y, point.z])

        points = np.array(points)

        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])
        for i in range(len(points)):
            points[i][0] = (points[i][0] - min_x) / (max_x - min_x)
            points[i][1] = (points[i][1] - min_y) / (max_y - min_y)

        points = np.expand_dims(points, axis=0)
        prediction = model.predict(points)
        prediction = ops.argmax(prediction, -1)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter = letters[prediction[0]]

        annotated_image = np.copy(image)
        height, width, _ = annotated_image.shape
        text_x = int(hand[0].x * width) - 100
        text_y = int(hand[0].y * height) + 50
        cv2.putText(
            img=annotated_image,
            text=letter,
            org=(text_x, text_y),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=5,
            color=(0, 255, 0),
            thickness=4,
            lineType=cv2.LINE_4,
        )
        return annotated_image
    except Exception as e:
        print(e)
        return image


def main():
    model = tf.keras.models.load_model("../model.keras")
    # print(model.summary())
    hand_landmarker = Landmarker()
    cap = cv2.VideoCapture(1)

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        hand_landmarker.detect_async(frame)
        frame = draw_landmarks_on_image(frame, hand_landmarker.result)
        frame = recognize_asl_signs(frame, model, hand_landmarker.result)

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    hand_landmarker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
