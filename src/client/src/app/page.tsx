"use client";

import React from "react";
import io from "socket.io-client";
import "regenerator-runtime/runtime";
import { useEffect, useRef, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import Camera from "./components/Camera";
import Transcription from "./components/Transcription";
import Visualization from "./components/Visualization";

const socket = io("http://localhost:1234");

export default function Home() {
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [ASLTranscription, setASLTranscription] = useState("");
  const [points, setPoints] = useState([]);
  const currentWords = useRef<string[]>([]);
  const [currentWord, setCurrentWord] = useState<string>("");
  const wordAnimationsToPlay = useRef<any>([]);

  useEffect(() => {
    SpeechRecognition.startListening({ continuous: true });
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("transcription", (data) => {
      setASLTranscription(data);
    });

    socket.on("points", (data) => {
      setPoints(data);
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
    }, 2000);

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
      <div className="flex flex-col gap-4">
        <Camera />
        <Transcription content={ASLTranscription} />
      </div>
      <div className="flex flex-col gap-4 grow">
        <Visualization
          points={points}
          getNextWord={getNextWord}
          currentWord={currentWord}
        />
        <Transcription content={transcript} />
      </div>
    </div>
  );
}
