"use client";

import { useState } from "react";

import Camera from "./Camera";
import Checkbox from "@/ui/components/checkbox";
import Transcription from "@/app/components/Transcription";

export default function Receptive() {
  const [ASLTranscription, setASLTranscription] = useState("");

  return (
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
          <div className="cursor-pointer rounded border border-white border-opacity-20 px-4 py-1 transition duration-300 hover:bg-white hover:bg-opacity-10">
            <p className="select-none text-lg text-white">Clear</p>
          </div>
        </div>
      </div>
    </div>
  );
}
