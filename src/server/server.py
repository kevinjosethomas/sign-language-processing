import os
import cv2
import logging
import psycopg2
from dotenv import load_dotenv
from flask import Flask, Response
from flask_socketio import SocketIO, emit
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

from utils.llm import LLM
from utils.store import Store
from utils.recognition import Recognition
import json

load_dotenv()
llm = LLM()
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
camera = cv2.VideoCapture(1)
recognition = Recognition()

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = psycopg2.connect(
    database="signs",
    host="localhost",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432,
)
register_vector(conn)

alphabet_frames = {}

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    file_path = os.path.join("alphabets", f"{letter}.json")
    with open(file_path, "r") as file:
        alphabet_frames[letter] = json.load(file)


def recognize():

    while camera.isOpened():

        success, image = camera.read()
        if not success:
            continue

        # image = cv2.flip(image, 1)
        image, updated, points = recognition.process(image)

        image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))

        _, buffer = cv2.imencode(".jpg", image)
        frame = buffer.tobytes()

        if updated:
            socketio.emit("transcription", Store.parsed)

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def stream():
    return Response(recognize(), mimetype="multipart/x-mixed-replace; boundary=frame")


@socketio.on("connect")
def on_connect():
    print("Connected to client")
    emit("transcription", Store.parsed)

    cursor = conn.cursor()
    animations = []
    embedding = model.encode("hello")
    cursor.execute(
        "SELECT word, points, (embedding <=> %s) AS cosine_similarity FROM signs ORDER BY cosine_similarity ASC LIMIT 1",
        (embedding,),
    )
    result = cursor.fetchone()
    if result and 1 - result[2] > 0.70:
        animations.append(("hello", result[1]))

    emit("words", animations)

    cursor.close()


@socketio.on("clear")
def on_clear():
    print("Clearing the store")
    Store.reset()
    emit("transcription", Store.parsed)


@socketio.on("disconnect")
def on_disconnect():
    print("Disconnected from client")


@socketio.on("words")
def on_word(words):

    animations = []
    words = words.strip()

    if not words:
        return

    words = llm.gloss(words)
    cursor = conn.cursor()
    for word in words:

        word = word.strip()
        if not word:
            continue

        embedding = model.encode(word)
        cursor.execute(
            "SELECT word, points, (embedding <=> %s) AS cosine_similarity FROM signs ORDER BY cosine_similarity ASC LIMIT 1",
            (embedding,),
        )
        result = cursor.fetchone()
        if result and 1 - result[2] > 0.70:
            animations.append((word, result[1]))
        else:
            animation = []
            for letter in word:
                animation.extend(alphabet_frames.get(letter.upper(), []))

            for i in range(len(animation)):
                animation[i][0] = i
            animations.append((f"fs-{word.upper()}", animation))

    emit("words", animations)

    cursor.close()


if __name__ == "__main__":
    socketio.run(app, debug=False, port=1234)
