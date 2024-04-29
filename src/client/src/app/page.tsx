"use client";

import React from "react";
import io from "socket.io-client";
import { useEffect, useState } from "react";

const socket = io("http://localhost:1234");

export default function Home() {
  const [transcription, setTranscription] = useState("");

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("transcription", (data) => {
      setTranscription(data);
    });
  });
  return (
    <div className="w-screen h-screen">
      <iframe src="http://localhost:1234" className="w-full h-screen" />
    </div>
  );
}
