"use client";

import React from "react";
import io from "socket.io-client";
import "regenerator-runtime/runtime";
import { useEffect, useRef, useState } from "react";

import { Slider } from "@/ui/components/Slider";
import Visualization from "../components/Visualization";

const socket = io("ws://localhost:1234");

export default function Home() {
  const wordAnimationsToPlay = useRef<any>([]);
  const [currentWord, setCurrentWord] = useState<string>("");
  const [signingSpeed, setSigningSpeed] = useState<number>(50);
  const [text, setText] = useState<string>("");
  const [duration, setDuration] = useState<string>("1");

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("E-ANIMATION", (animations) => {
      // if (duration != "0") {
      //   setSigningSpeed(
      //     Math.floor(animations[0][1].length / parseFloat(duration))
      //   );
      // }

      wordAnimationsToPlay.current = [
        ...wordAnimationsToPlay.current,
        ...animations,
      ];
    });
  }, []);

  function getNextWord(): string | null {
    if (!wordAnimationsToPlay.current.length) {
      return null;
    }

    let animation = wordAnimationsToPlay.current.shift();
    setCurrentWord(animation[0]);

    return animation[1];
  }

  return (
    <div className="w-screen h-screen flex flex-row gap-4">
      <div className="py-4 px-4 flex flex-col items-start gap-6 w-80 bg-white bg-opacity-10">
        <p className="text-4xl font-semibold text-white">Express</p>
        <div className="flex flex-col w-full gap-1">
          <p className="text-lg text-white">Signing Speed</p>
          <Slider
            defaultValue={[signingSpeed]}
            value={[signingSpeed]}
            onValueChange={(value) => setSigningSpeed(value[0])}
            min={20}
            max={100}
            step={1}
          />
        </div>
        <div className="flex flex-col gap-1 w-full items-start justify-start">
          <p className="text-lg text-white">Duration</p>
          <input
            value={duration}
            placeholder="Enter duration (in seconds)"
            onChange={(e) => setDuration(e.target.value)}
            className="w-full focus:outline-none placeholder-white placeholder-opacity-50 text-sm text-white p-2 border bg-transparent border-white border-opacity-10 rounded"
          />
        </div>
        <div className="flex flex-col gap-1 w-full h-full items-start justify-start">
          <p className="text-lg text-white">Content</p>
          <textarea
            value={text}
            placeholder="Enter text to sign"
            onChange={(e) => setText(e.target.value)}
            className="w-full focus:outline-none placeholder-white placeholder-opacity-50 text-sm text-white p-2 h-full border bg-transparent border-white border-opacity-10 rounded"
          />
        </div>
        <div
          className="bg-blue-600 hover:bg-blue-700 transition duration-300 flex items-center justify-center w-full py-2 rounded"
          onClick={() => socket.emit("E-REQUEST-ANIMATION", text)}
        >
          <p className="text-white select-none">Render</p>
        </div>
      </div>
      <Visualization
        full
        signingSpeed={signingSpeed}
        getNextWord={getNextWord}
        currentWord={currentWord}
      />
    </div>
  );
}
