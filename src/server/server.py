import os
import cv2
import logging
import psycopg2
from dotenv import load_dotenv
from flask import Flask, Response
from flask_socketio import SocketIO, emit
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

from utils.store import Store
from utils.recognition import Recognition

load_dotenv()
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
camera = cv2.VideoCapture(2)
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


@socketio.on("disconnect")
def on_disconnect():
    print("Disconnected from client")
    Store.reset()


@socketio.on("words")
def on_word(words):

    animations = []
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

    emit("words", animations)

    cursor.close()


if __name__ == "__main__":
    socketio.run(app, debug=False, port=1234)
