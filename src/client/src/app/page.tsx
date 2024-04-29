"use client";

import React from "react";
import { useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:1234");

export default function Home() {
  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("transcription", (data) => {
      console.log(data);
    });
  });
  return (
    <div>
      <iframe src="http://localhost:1234" className="w-screen h-screen" />
    </div>
  );
}
