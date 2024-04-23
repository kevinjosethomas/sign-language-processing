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
            result_callback=update_result,
            model_complexity=0,
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

        if not hand:
            return image

        handedness = detection_result.handedness[0][0].category_name.lower()
        print(handedness)

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
        predictions = model.predict(points, verbose=0)
        prediction = ops.argmax(predictions, -1)
        letters = "ABCDEFGHIKLMNOPQRSTUVWXY"
        letter = letters[prediction[0]]
        probability = predictions[0][prediction[0]]

        annotated_image = np.copy(image)
        height, width, _ = annotated_image.shape
        text_x = int(hand[0].x * width) - 100
        text_y = int(hand[0].y * height) + 50
        cv2.putText(
            img=annotated_image,
            text=f"{letter} {round(probability * 100 * 100) / 100}%",
            org=(text_x, text_y),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=5,
            color=(0, 255, 0),
            thickness=4,
            lineType=cv2.LINE_4,
        )
        return annotated_image
    except Exception as e:
        return image


# def main():
#     model = tf.keras.models.load_model("../model.keras")
#     hand_landmarker = Landmarker()
#     cap = cv2.VideoCapture(1)

#     while True:
#         _, frame = cap.read()
#         frame = cv2.flip(frame, 1)

#         hand_landmarker.detect_async(frame)
#         frame = draw_landmarks_on_image(frame, hand_landmarker.result)
#         # frame = recognize_asl_signs(frame, model, hand_landmarker.result)

#         cv2.imshow("frame", frame)

#         if cv2.waitKey(1) == ord("q"):
#             break

#     cap.release()
#     hand_landmarker.close()
#     cv2.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def main():

    cap = cv2.VideoCapture(1)
    with mp_hands.Hands(
        model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style(),
                    )

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break


if __name__ == "__main__":
    main()
