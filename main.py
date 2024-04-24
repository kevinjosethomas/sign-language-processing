import os
import cv2
import time

from asl.landmarker import Landmarker
from asl.classifier import Classifier

landmarker = Landmarker()
classifier = Classifier()

if __name__ == "__main__":
    camera = cv2.VideoCapture(1)

    start = time.time()
    os.system("clear")
    transcription = ""
    transcription_log = []

    while camera.isOpened():

        success, img = camera.read()
        if not success:
            continue

        success, image, points, first_landmark = landmarker.process(img)

        if time.time() - start > 1 and success:
            letter, probability = classifier.classify(points)
            transcription_log.append(letter)

            if probability > 0.90:
                transcribed = False

                longer_recent = set(transcription_log[-20:])
                if len(longer_recent) == 1 and transcription[-2:] != letter * 2:
                    transcription += letter
                    transcribed = True
                else:
                    recent = set(transcription_log[-4:])
                    if len(recent) == 1 and (
                        not transcription or transcription[-1] != letter
                    ):
                        transcription += letter
                        transcribed = True

                os.system("clear")
                print(transcription)

                height, width, _ = image.shape
                text_x = int(first_landmark[0] * width) - 100
                text_y = int(first_landmark[1] * height) + 50
                cv2.putText(
                    img=image,
                    text=f"{letter} {round(probability * 100 * 100) / 100}%",
                    org=(text_x, text_y),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=5,
                    color=(0, 0, 255) if transcribed else (0, 255, 0),
                    thickness=4,
                    lineType=cv2.LINE_4,
                )
        else:
            if transcription and transcription[-1] != " ":
                transcription += " "

        cv2.imshow("Sign Language Recognition", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
