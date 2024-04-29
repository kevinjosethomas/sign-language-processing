import { useEffect } from "react";

export default function Transcription({
  ASLTranscription,
  EnglishTranscription,
}: {
  ASLTranscription: string;
  EnglishTranscription: string;
}) {
  return (
    <div className="flex flex-col w-full h-full border gap-2 rounded p-4">
      <p className="text-4xl text-blue-500">{ASLTranscription}</p>
      <p className="text-4xl text-green-500">{EnglishTranscription}</p>
    </div>
  );
}
