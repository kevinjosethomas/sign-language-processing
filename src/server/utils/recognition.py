import cv2
import threading
import numpy as np

from utils.llm import LLM
from utils.store import Store
from utils.landmarker import Landmarker
from utils.classifier import Classifier


class Recognition:

    def __init__(self, min_confidence: float = 0.80):
        self.min_confidence = min_confidence
        self.landmarker = Landmarker()
        self.classifier = Classifier()

    def process(self, image: np.ndarray):

        success, image, points, first_landmark, hand = self.landmarker.draw_landmarks(
            image
        )

        # If a hand is detected in the frame
        if success:

            added_letter = False
            letter, probability = self.classifier.classify(points)
            letter = self.fix_misrecognition(letter, points, hand)
            Store.raw_letters.append(letter)

            # Ensure the alphabet classification probability is larger than the minimum confidence
            if probability > self.min_confidence:

                # Ensure the last X letters are the same before repeating a letter
                last_x_letters = set(Store.raw_letters[-20:])
                if len(last_x_letters) == 1 and (
                    len(Store.raw_word) < 2 or Store.raw_word[-2:] != letter * 2
                ):
                    Store.raw_word += letter
                    added_letter = True
                else:

                    # Ensure that the last Y letters are the same before adding a letter
                    last_y_letters = set(Store.raw_letters[-4:])
                    if len(last_y_letters) == 1 and (
                        not Store.raw_word or Store.raw_word[-1] != letter
                    ):
                        Store.raw_word += letter
                        added_letter = True

                height, width, _ = image.shape
                text_x = int(first_landmark[0] * width) - 100
                text_y = int(first_landmark[1] * height) + 50
                cv2.putText(
                    img=image,
                    text=f"{letter} {round(probability * 100 * 100) / 100}%",
                    org=(text_x, text_y),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=5,
                    color=(0, 0, 255) if added_letter else (0, 255, 0),
                    thickness=4,
                    lineType=cv2.LINE_4,
                )
        else:  # If no hand is detected, add a space
            if Store.raw_word:
                Store.raw_transcription.append(Store.raw_word)
                thread = threading.Thread(target=LLM.fix)
                thread.start()

        output = (" ".join(Store.raw_transcription) + " " + Store.raw_word).strip()

        different = output != Store.parsed
        if different:
            Store.parse(output)

        return (image, different, points if success else None)

    def fix_misrecognition(self, letter: str, points: np.ndarray, hand: str):

        if letter in ["A", "T"]:
            thumb_tip = points[0][4]
            thumb_middle = points[0][3]
            index_tip = points[0][8]
            if hand == "left":
                if thumb_tip[0] > index_tip[0] and thumb_middle[0] > index_tip[0]:
                    letter = "A"
                else:
                    letter = "T"
            else:
                if thumb_tip[0] < index_tip[0] and thumb_middle[0] < index_tip[0]:
                    letter = "A"
                else:
                    letter = "T"

        # if letter == "K":
        #     index_tip = points[0][8]
        #     index_middle = points[0][7]
        #     middle_tip = points[0][12]
        #     middle_middle = points[0][11]

        #     if index_tip[1] < index_middle[1] or middle_tip[1] < middle_middle[1]:
        #         print(index_tip[1], index_middle[1], middle_tip[1], middle_middle[1])
        #         letter = "I"

        if letter in ["D", "I"]:
            index_tip = points[0][8]
            pinky_tip = points[0][20]

            if index_tip[1] > pinky_tip[1]:
                letter = "I"
            else:
                letter = "D"

        if letter in ["F", "W"]:
            index_tip = points[0][8]
            pinky_tip = points[0][20]

            if index_tip[1] > pinky_tip[1]:
                letter = "F"
            else:
                letter = "W"

        return letter
