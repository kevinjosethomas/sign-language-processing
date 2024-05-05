import { useEffect } from "react";

export default function Transcription({ content }: { content: string }) {
  return (
    <div className="flex grow flex-col border gap-2 rounded p-4">
      <p className="text-4xl">{content}</p>
    </div>
  );
}
