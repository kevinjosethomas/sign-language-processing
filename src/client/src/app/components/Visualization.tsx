import { useEffect, useRef } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";

import { drawPoint, connectHands, connectPose } from "./lib";

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
      className="relative border rounded overflow-hidden h-[540px] bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <p className="text-4xl upper text-white absolute z-10 bottom-10 justify-center flex w-full">
        {currentWord}
      </p>
      <Canvas>
        <Sign getNextWord={getNextWord} />
        <ambientLight intensity={1} />
      </Canvas>
    </div>
  );
}

function Sign({ getNextWord }: { getNextWord: () => string | null }) {
  const { camera } = useThree();
  const previous_frame = useRef(0);
  const start_time = useRef(0);
  const word = useRef<any>(null);

  useFrame(({ clock, scene }) => {
    const elapsed = clock.getElapsedTime() - start_time.current;
    const frame_index = Math.floor(elapsed * 45);

    if (frame_index !== previous_frame.current) {
      previous_frame.current = frame_index;

      if (!word.current) {
        word.current = getNextWord();
        start_time.current = clock.getElapsedTime();
        previous_frame.current = 0;
        return;
      }

      if (frame_index >= word.current.length) {
        word.current = null;
        return;
      }

      scene.remove(...scene.children);

      const left = word.current[0][2][0];
      const right = word.current[0][2][1];
      const pose = word.current[0][1];

      pose.map((point) => drawPoint(point[1], point[2], point[3]));

      left.map((point) => drawPoint(point[1], point[2], point[3]));

      right.map((point) => drawPoint(point[1], point[2], point[3]));

      connectHands(frame_index, word.current, scene);
      connectPose(frame_index, word.current, scene);
    }
  });

  useEffect(() => {
    camera.position.set(5, -5, 5);
    camera.rotation.set(0, 0, 0);
  }, [camera]);

  return null;
}
