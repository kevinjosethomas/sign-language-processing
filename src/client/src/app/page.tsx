"use client";

import React from "react";
import io from "socket.io-client";
import "regenerator-runtime/runtime";
import { useEffect, useRef, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import Camera from "./components/Camera";
import { Slider } from "@/ui/components/Slider";
import Transcription from "./components/Transcription";
import Visualization from "./components/Visualization";

const socket = io("http://localhost:1234");

export default function Home() {
  const currentWords = useRef<string[]>([]);
  const wordAnimationsToPlay = useRef<any>([]);
  const [currentWord, setCurrentWord] = useState<string>("");
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [signingSpeed, setSigningSpeed] = useState<number>(50);

  const [ASLTranscription, setASLTranscription] = useState("");

  useEffect(() => {
    SpeechRecognition.startListening({ continuous: true });

    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("transcription", (data) => {
      setASLTranscription(data);
    });

    socket.on("words", (animations) => {
      wordAnimationsToPlay.current = [
        ...wordAnimationsToPlay.current,
        ...animations,
      ];
    });
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => {
      currentWords.current = [...transcript.toLowerCase().split(" ")];
      resetTranscript();
      socket.emit("words", currentWords.current);
    }, 500);

    return () => {
      clearTimeout(timeout);
    };
  }, [transcript]);

  function getNextWord(): string | null {
    if (!wordAnimationsToPlay.current.length) {
      return null;
    }

    let animation = wordAnimationsToPlay.current.shift();
    setCurrentWord(animation[0]);

    return animation[1];
  }

  return (
    <div className="w-screen h-screen flex flex-row gap-4 p-4">
      <div className="flex flex-col gap-4 items-center grow">
        <h1 className="text-2xl text-white">ASL Fingerspell → English</h1>
        <div className="border w-full h-full flex-col flex rounded">
          <Camera />
          <Transcription content={ASLTranscription} />
        </div>
      </div>
      <div className="flex flex-col gap-4 items-center grow">
        <h1 className="text-2xl text-white">English → ASL</h1>
        <div className="border w-full h-full flex-col flex rounded">
          <Visualization
            signingSpeed={signingSpeed}
            getNextWord={getNextWord}
            currentWord={currentWord}
          />
          <Transcription content={transcript} />
          <div className="py-4 px-4 flex flex-col items-start gap-2 bg-white bg-opacity-10">
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
        </div>
      </div>
    </div>
  );
}
