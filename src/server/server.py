from flask import Flask, render_template, Response
import os
import cv2
import threading
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from landmarker import Landmarker
from classifier import Classifier

load_dotenv()
landmarker = Landmarker()
classifier = Classifier()
llm = ChatOpenAI(
    # model="gpt-4-turbo-preview",
    model="gpt-3.5-turbo-0125",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

PROMPT = ChatPromptTemplate.from_messages(  # The alphabets that the software often gets confused between are: A, S, T, N and M; G and H; D and I; F and W; P and Q; R and U.
    [
        (
            "system",
            "You are an LLM meant to fix typos in given phrases. I will send you a "
            "phrase, please correct it if there are any typos. These are the alphabets that are mistaken for each other the most often: A and S and T and N and M. G and H. D and I. F and W. P and Q. R and U. "
            "Please output nothing but the corrected phrase. No punctuation. Make sure everything is an English word"
            "or a proper noun. Make sure the phrase makes sense.",
        ),
        ("human", "{transcription}"),
    ]
)
chain = PROMPT | llm

transcription_current_word = ""
ai_transcription_words = []
transcription_words = []
transcription_alphabet_log = []

app = Flask(__name__)
camera = cv2.VideoCapture(2)


def fix_transcription():
    global transcription_words, transcription_current_word, transcription_alphabet_log, ai_transcription_words

    ai_transcription_words.append(transcription_current_word)
    transcription_current_word = ""
    transcription = " ".join(transcription_words)
    response = chain.invoke(
        {
            "transcription": transcription,
        }
    )

    print(" ".join(transcription_words))
    ai_transcription_words = response.content.strip().upper().split()


def generate_frames():
    global transcription_words, transcription_current_word, transcription_alphabet_log, ai_transcription_words
    while True:

        while camera.isOpened():

            success, img = camera.read()
            if not success:
                continue

            success, image, points, first_landmark = landmarker.process(img)

            if success:
                letter, probability = classifier.classify(points)
                transcription_alphabet_log.append(letter)

                if probability > 0.80:
                    transcribed = False

                    # 1. Ensure that the last 20 letters are the same
                    # 2. Ensure that it does not repeat the same character more than twice
                    longer_recent = set(transcription_alphabet_log[-20:])
                    if len(longer_recent) == 1 and (
                        len(transcription_current_word) < 2
                        or transcription_current_word[-2:] != letter * 2
                    ):
                        transcription_current_word += letter
                        transcribed = True
                    else:
                        # Ensure that the last 4 letters are the same
                        # Ensure that it does not repeat the same character more than once
                        recent = set(transcription_alphabet_log[-4:])
                        if len(recent) == 1 and (
                            not transcription_current_word
                            or transcription_current_word[-1] != letter
                        ):
                            transcription_current_word += letter
                            transcribed = True

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
                if transcription_current_word:
                    transcription_words.append(transcription_current_word)

                    new_thread = threading.Thread(target=fix_transcription)
                    new_thread.start()

            output = (
                " "
                + (
                    " ".join(ai_transcription_words) + " " + transcription_current_word
                ).strip()
                + " "
            )
            text_width = cv2.getTextSize(output, cv2.FONT_HERSHEY_DUPLEX, 2, 5)[0][0]
            pos = ((image.shape[1] - text_width) // 2, image.shape[0] - 30)
            cv2.rectangle(
                image,
                (0, image.shape[0] - 100),
                (image.shape[1], image.shape[0]),
                (255, 255, 255),
                -1,
            )
            cv2.putText(
                img=image,
                text=output,
                org=pos,
                fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=2,
                color=(0, 0, 0),
                thickness=5,
                lineType=cv2.LINE_4,
            )

            _, buffer = cv2.imencode(".jpg", image)
            frame = buffer.tobytes()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def video():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True, port=1234)
