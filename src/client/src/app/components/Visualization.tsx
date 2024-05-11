import { Canvas } from "@react-three/fiber";

import Avatar from "./Avatar";

export default function Visualization({
  getNextWord,
  currentWord,
}: {
  getNextWord: () => string | null;
  currentWord: string;
}) {
  return (
    <div
      id="canvas-container"
      className="relative w-full border-b border-white border-opacity-20 overflow-hidden h-[540px] bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <p className="text-4xl upper text-white absolute z-10 bottom-10 justify-center flex w-full">
        {currentWord}
      </p>
      <Canvas>
        <Avatar getNextWord={getNextWord} />
      </Canvas>
    </div>
  );
}
