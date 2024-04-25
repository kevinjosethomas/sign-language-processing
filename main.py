import os
import cv2
import time
import threading
from langchain_community.llms import Ollama

from asl.landmarker import Landmarker
from asl.classifier import Classifier

landmarker = Landmarker()
classifier = Classifier()

llm = Ollama(model="llama3")
transcription = ""


def fix_transcription():
    global transcription

    previous = transcription
    response = llm.invoke(
        f"You are an LLM that corrects typos in words. I will keep sending you phrases, return the corrected sentence or word. Make sure your output is the corrected phrase WITH NO OTHER CONTENT. It should be exactly like the input but corrected. Do not precede or end it with any additional text. Here is the phrase: '{transcription}'"
    )
    print(response.strip())
    transcription = response.strip().upper() + " "


def main():
    global transcription
    camera = cv2.VideoCapture(0)

    start = time.time()
    # os.system("clear")

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

                # os.system("clear")

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

                new_thread = threading.Thread(target=fix_transcription)
                new_thread.start()

        size = cv2.getTextSize(transcription, cv2.FONT_HERSHEY_PLAIN, 1, 2)[0]
        textX = int((img.shape[1] - size[0]) / 2)
        cv2.putText(
            img=image,
            text=transcription,
            org=(textX, img.shape[0] - 100),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=5,
            color=(0, 0, 255),
            thickness=8,
            lineType=cv2.LINE_4,
        )

        cv2.imshow("Sign Language Recognition", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break


if __name__ == "__main__":
    main()
