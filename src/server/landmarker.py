import cv2
import numpy as np
import mediapipe as mp
from cv2.typing import MatLike

LETTERS = "ABCDEFGHIKLMNOPQRSTUVWXY"
drawing_utils = mp.solutions.drawing_utils
drawing_styles = mp.solutions.drawing_styles


class Landmarker:

    def __init__(
        self,
        model_complexity: int = 0,
        min_detection_confidence: float = 0.75,
        min_tracking_confidence: float = 0.75,
        max_num_hands: int = 1,
    ):
        self.model = mp.solutions.hands.Hands(
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands,
        )

    def draw_landmarks(self, image: MatLike):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.model.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not results.multi_hand_landmarks:
            return False, image, None, None

        for landmarks in results.multi_hand_landmarks:
            drawing_utils.draw_landmarks(
                image,
                landmarks,
                mp.solutions.hands.HAND_CONNECTIONS,
                drawing_utils.DrawingSpec(
                    color=(0, 0, 255), thickness=8, circle_radius=8
                ),
                drawing_utils.DrawingSpec(
                    color=(0, 255, 0), thickness=6, circle_radius=2
                ),
            )

        hand = results.multi_hand_landmarks[0]
        points = np.array(
            [(landmark.x, landmark.y, landmark.z) for landmark in hand.landmark]
        )
        points = self.normalize_points(points)

        return True, image, points, (hand.landmark[0].x, hand.landmark[0].y)

    def normalize_points(self, points):
        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])
        for i in range(len(points)):
            points[i][0] = (points[i][0] - min_x) / (max_x - min_x)
            points[i][1] = (points[i][1] - min_y) / (max_y - min_y)

        points = np.expand_dims(points, axis=0)

        return points
