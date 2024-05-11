import { useEffect } from "react";

export default function Transcription({ content }: { content: string }) {
  return (
    <div className="flex grow w-full flex-col bg-white bg-opacity-10 gap-2 p-4">
      <p className="text-4xl text-white">{content}</p>
    </div>
  );
}
