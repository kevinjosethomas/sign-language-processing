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
import Checkbox from "@/ui/components/checkbox";
import Transcription from "../components/Transcription";
import Visualization from "../components/Visualization";

const socket = io("ws://localhost:1234");

export default function Home() {
  const wordAnimationsToPlay = useRef<any>([]);
  const [currentWord, setCurrentWord] = useState<string>("");
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [signingSpeed, setSigningSpeed] = useState<number>(50);

  const [ASLTranscription, setASLTranscription] = useState("");

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("R-TRANSCRIPTION", (data) => {
      setASLTranscription(data);
    });

    socket.on("E-ANIMATION", (animations) => {
      wordAnimationsToPlay.current = [
        ...wordAnimationsToPlay.current,
        ...animations,
      ];
    });
  }, []);

  useEffect(() => {
    const timeout = setTimeout(() => {
      socket.emit("E-REQUEST-ANIMATION", transcript.toLowerCase());
      resetTranscript();
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

  function clear() {
    socket.emit("R-CLEAR-TRANSCRIPTION");
  }

  return (
    <div className="flex h-screen w-screen items-center bg-neutral-950">
      <div className="grid h-full w-full grid-cols-2 gap-1 overflow-hidden rounded-xl bg-sky-500">
        <div className="flex flex-col items-center overflow-hidden bg-neutral-900">
          <div className="flex h-16 w-full items-center justify-start gap-2 bg-neutral-900 px-4">
            <i className="fad fa-american-sign-language-interpreting text-xl text-white" />
            <h1 className="text-xl text-white">ASL Fingerspell</h1>
          </div>
          <Camera />
          <div className="flex h-full w-full flex-col rounded">
            <Transcription content={ASLTranscription} />
            <div className="flex items-center justify-end gap-4 bg-white bg-opacity-10 px-4 py-4">
              <Checkbox label="Autocorrect" />
              <div
                onClick={clear}
                className="cursor-pointer rounded border border-white border-opacity-20 px-4 py-1 transition duration-300 hover:bg-white hover:bg-opacity-10"
              >
                <p className="select-none text-lg text-white">Clear</p>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-center overflow-hidden bg-neutral-900">
          <div className="flex h-16 w-full items-center justify-between bg-neutral-900 px-6">
            <div className="flex items-center gap-2">
              <i className="fad fa-sign-language text-xl text-white" />
              <h1 className="text-xl text-white">English</h1>
            </div>
            <i className="fas fa-cog text-xl text-white" />
          </div>
          <div className="flex h-full w-full flex-col">
            <Visualization
              signingSpeed={signingSpeed}
              getNextWord={getNextWord}
              currentWord={currentWord}
            />
            <Transcription content={transcript} />
            <div className="flex flex-col items-start gap-2 bg-white bg-opacity-10 px-4 py-4">
              <div className="flex w-full items-center justify-between">
                <p className="text-lg text-white">Signing Speed</p>
                <div className="flex items-center gap-4">
                  <div
                    onClick={() =>
                      SpeechRecognition.startListening({ continuous: true })
                    }
                    className="cursor-pointer rounded border border-white border-opacity-20 px-4 py-1 transition duration-300 hover:bg-white hover:bg-opacity-10"
                  >
                    <p className="select-none text-white">Start</p>
                  </div>
                  <Checkbox label="ASL Gloss" />
                </div>
              </div>
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
    </div>
  );
}
