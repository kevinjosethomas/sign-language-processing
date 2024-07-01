"use client";

import { useState } from "react";

import Camera from "./Camera";

export default function Receptive() {
  const [ASLTranscription, setASLTranscription] = useState("");

  return (
    <div className="flex h-full flex-1 flex-col justify-start">
      <Camera />
    </div>
  );
}
