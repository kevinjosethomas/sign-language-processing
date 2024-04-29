"use client";

import React, { useEffect, useRef } from "react";
import io from "socket.io-client";
import Peer from "simple-peer";

const socket = io("http://localhost:1234");

const VideoComponent = () => {
  const localRef = useRef();
  const remoteRef = useRef();
  const peerRef: any = useRef(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
          width: { ideal: 4096 },
        },
      })
      .then((stream) => {
        if (localRef.current) {
          localRef.current.srcObject = stream;
        }

        const peer = new Peer({
          initiator: true,
          trickle: false,
          stream: stream,
          config: {
            iceServers: [],
          },
        });

        peerRef.current = peer;

        peer.on("signal", (data) => {
          socket.emit("offer", data);
        });

        socket.on("answer", (data) => {
          peer.signal(data);
        });

        peer.on("stream", (s) => {
          if (remoteRef.current) {
            remoteRef.current.srcObject = s;
          }
        });
      });
  }, []);

  return (
    <div>
      <div className="w-screen">
        <video
          ref={localRef}
          className="z-10 w-full hidden"
          autoPlay
          muted
        ></video>
        <video
          ref={remoteRef}
          className="z-20 w-full"
          autoPlay
          playsInline
        ></video>
        <iframe
          src="http://localhost:5001/video"
          className="w-screen h-screen"
        />
      </div>
    </div>
  );
};

export default VideoComponent;
