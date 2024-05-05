"use client";

import React from "react";
import io from "socket.io-client";
import "regenerator-runtime/runtime";
import { useEffect, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import Camera from "./components/Camera";
import Transcription from "./components/Transcription";
import Visualization from "./components/Visualization";

const socket = io("http://localhost:1234");

export default function Home() {
  const { transcript, listening, resetTranscript } = useSpeechRecognition();
  const [ASLTranscription, setASLTranscription] = useState("");
  const [EnglishTranscription, setEnglishTranscription] = useState("");
  const [points, setPoints] = useState([]);

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
  }, []);

  useEffect(() => {
    setEnglishTranscription(transcript);
  }, [transcript]);

  return (
    <div className="w-screen h-screen flex flex-row gap-4 p-4">
      <div className="flex flex-col gap-4">
        <Camera />
        <Transcription content={ASLTranscription} />
      </div>
      <div className="flex flex-col gap-4 grow">
        <Visualization points={points} />
        <Transcription content={transcript} />
      </div>
    </div>
  );
}
