import { Canvas } from "@react-three/fiber";

import Avatar from "./Avatar";

export default function Visualization({
  signingSpeed,
  getNextWord,
  currentWord,
  full,
}: {
  signingSpeed: number;
  getNextWord: () => string | null;
  full?: boolean;
  currentWord: string;
}) {
  return (
    <div
      id="canvas-container"
      className={`relative w-full  ${
        full
          ? "h-full bg-black"
          : "border-b border-white border-opacity-20 overflow-hidden h-[540px] bg-gradient-to-br from-neutral-800 to-neutral-950"
      }`}
    >
      <p
        className={`${
          full ? "text-7xl" : "text-4xl"
        } upper text-white absolute z-10 bottom-10 justify-center flex w-full`}
      >
        {currentWord}
      </p>
      <Canvas>
        <Avatar signingSpeed={signingSpeed} getNextWord={getNextWord} />
      </Canvas>
    </div>
  );
}
