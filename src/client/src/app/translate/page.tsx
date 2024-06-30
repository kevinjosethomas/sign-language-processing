"use client";

import React from "react";
import io from "socket.io-client";
import "regenerator-runtime/runtime";
import { useEffect, useRef, useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

import Camera from "../components/Camera";
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
    <div className="w-screen h-screen p-16 flex items-center bg-neutral-950">
      <div className="grid grid-cols-2 gap-1 bg-sky-500 rounded-xl w-full h-full overflow-hidden">
        <div className="flex flex-col items-center bg-neutral-900 overflow-hidden">
          <div className="h-16 w-full flex items-center justify-start gap-2 px-4 bg-neutral-900">
            <i className="fad fa-american-sign-language-interpreting text-xl text-white" />
            <h1 className="text-xl text-white">ASL Fingerspell</h1>
          </div>
          <div className="w-full h-full flex-col flex rounded">
            <Camera />
            <Transcription content={ASLTranscription} />
            <div className="py-4 px-4 flex items-center justify-end gap-4 bg-white bg-opacity-10">
              <Checkbox label="Autocorrect" />
              <div
                onClick={clear}
                className="px-4 py-1 border-white border-opacity-20 border rounded hover:bg-white hover:bg-opacity-10 transition duration-300 cursor-pointer"
              >
                <p className="text-white text-lg select-none">Clear</p>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-center bg-neutral-900 overflow-hidden">
          <div className="h-16 w-full flex items-center justify-between px-6 bg-neutral-900">
            <div className="flex items-center gap-2">
              <i className="fad fa-sign-language text-xl text-white" />
              <h1 className="text-xl text-white">English</h1>
            </div>
            <i className="fas fa-cog text-white text-xl" />
          </div>
          <div className="w-full h-full flex-col flex">
            <Visualization
              signingSpeed={signingSpeed}
              getNextWord={getNextWord}
              currentWord={currentWord}
            />
            <Transcription content={transcript} />
            <div className="py-4 px-4 flex flex-col items-start gap-2 bg-white bg-opacity-10">
              <div className="flex items-center justify-between w-full">
                <p className="text-lg text-white">Signing Speed</p>
                <div className="flex items-center gap-4">
                  <div
                    onClick={() =>
                      SpeechRecognition.startListening({ continuous: true })
                    }
                    className="px-4 py-1 border-white border-opacity-20 border rounded hover:bg-white hover:bg-opacity-10 transition duration-300 cursor-pointer"
                  >
                    <p className="text-white select-none">Start</p>
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
