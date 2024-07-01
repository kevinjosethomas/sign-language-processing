"use client";

import "regenerator-runtime/runtime";
import { useRef, useState } from "react";
import { useSpeechRecognition } from "react-speech-recognition";

import Checkbox from "@/ui/components/checkbox";
import { Slider } from "@/ui/components/Slider";
import Transcription from "@/app/components/Transcription";

export default function Expressive() {
  const wordAnimationsToPlay = useRef<any>([]);
  const [currentWord, setCurrentWord] = useState<string>("");
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [signingSpeed, setSigningSpeed] = useState<number>(50);

  return (
    <div className="flex flex-col items-center overflow-hidden bg-neutral-900">
      <div className="flex h-16 w-full items-center justify-between bg-neutral-900 px-6">
        <div className="flex items-center gap-2">
          <i className="fad fa-sign-language text-xl text-white" />
          <h1 className="text-xl text-white">English</h1>
        </div>
        <i className="fas fa-cog text-xl text-white" />
      </div>
      <div className="flex h-full w-full flex-col">
        {/* <Visualization
          signingSpeed={signingSpeed}
          getNextWord={getNextWord}
          currentWord={currentWord}
        /> */}
        <Transcription content={transcript} />
        <div className="flex flex-col items-start gap-2 bg-white bg-opacity-10 px-4 py-4">
          <div className="flex w-full items-center justify-between">
            <p className="text-lg text-white">Signing Speed</p>
            <div className="flex items-center gap-4">
              <div className="cursor-pointer rounded border border-white border-opacity-20 px-4 py-1 transition duration-300 hover:bg-white hover:bg-opacity-10">
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
  );
}
