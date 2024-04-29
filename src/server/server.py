import asyncio
import socketio
from aiohttp import web
import os
import cv2
import threading
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from av import VideoFrame

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
from aiortc import (
    MediaStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    RTCConfiguration,
    RTCIceServer,
)
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)
relay = MediaRelay()
peer_connections = {}


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        success, image, points, first_landmark = landmarker.process(img)
        if success:
            new_frame = VideoFrame.from_ndarray(image, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        else:
            return frame


@sio.event
async def offer(sid, data):
    offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
    peer = RTCPeerConnection(
        configuration=RTCConfiguration(
            iceServers=[RTCIceServer(urls="stun:localhost:19302")]
        )
    )
    peer_connections[sid] = peer

    print("Created Peer Connection")

    @peer.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is ", peer.connectionState)
        if peer.connectionState == "failed":
            await peer.close()
            del peer_connections[sid]

    @peer.on("signal")
    async def on_signal(signal):
        print("\nReceived signal\n")
        await sio.emit("signal", signal, to=sid)

    @peer.on("track")
    def on_track(track):

        if track.kind == "video":
            peer.addTrack(VideoTransformTrack(relay.subscribe(track)))

        @track.on("ended")
        async def on_ended():
            print("Track %s ended", track.kind)

    # @peer.on("candidate")
    # async def on_candidate(candidate):
    #     print("\nReceived candidate\n")
    #     await sio.emit("candidate", candidate, to=sid)

    await peer.setRemoteDescription(offer)
    answer = await peer.createAnswer()
    await peer.setLocalDescription(answer)

    await sio.emit(
        "answer",
        {
            "sdp": peer.localDescription.sdp,
            "type": peer.localDescription.type,
        },
        to=sid,
    )


if __name__ == "__main__":
    web.run_app(app, port=1234)
