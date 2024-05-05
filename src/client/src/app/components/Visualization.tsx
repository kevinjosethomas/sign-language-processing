import * as THREE from "three";
import { useEffect, useRef } from "react";
import { MeshLine, MeshLineMaterial } from "three.meshline";
import { Canvas, useThree, useFrame } from "@react-three/fiber";

const SCALE = 0.015;

function drawPoint(x: number, y: number, z: number) {
  const geometry = new THREE.SphereGeometry(0.1, 32, 16);
  const material = new THREE.MeshBasicMaterial({ color: 0x84ffff });
  const sphere = new THREE.Mesh(geometry, material);
  sphere.position.set(x, -y, z);
}

function drawLine(
  x1: number,
  y1: number,
  z1: number,
  x2: number,
  y2: number,
  z2: number,
  color: number[],
  scene: THREE.Scene
) {
  const p = [];
  p.push(new THREE.Vector3(x1, -y1, z1));
  p.push(new THREE.Vector3(x2, -y2, z2));
  const geometry = new THREE.BufferGeometry().setFromPoints(p);
  const material = new MeshLineMaterial({
    color: new THREE.Color(color[0]),
    opacity: color[1],
    lineWidth: 0.05,
    transparent: true,
    depthTest: false,
  });
  const line = new MeshLine();
  line.setGeometry(geometry);

  const mesh = new THREE.Mesh(line, material);
  scene.add(mesh);
}

function connectPose(index: number, animation: any, scene: THREE.Scene) {
  const edges = [
    [11, 12],
    [12, 14],
    [14, 16],
    [11, 13],
    [13, 15],
    [11, 23],
    [12, 24],
  ];

  const pose = animation[index][1];

  edges.map((edge) => {
    const u = edge[0];
    const v = edge[1];
    if (pose[u] && pose[v]) {
      const p1 = pose[u];
      const p2 = pose[v];
      drawLine(
        p1[1] * SCALE,
        p1[2] * SCALE,
        p1[3] * SCALE,
        p2[1] * SCALE,
        p2[2] * SCALE,
        p2[3] * SCALE,
        [0xffffff, 0.2],
        scene
      );
    }
  });
}

function connectHands(index: number, animation: any, scene: THREE.Scene) {
  const edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
    [0, 5],
    [5, 6],
    [6, 7],
    [7, 8],
    [5, 9],
    [9, 10],
    [10, 11],
    [11, 12],
    [9, 13],
    [13, 14],
    [14, 15],
    [15, 16],
    [13, 17],
    [17, 18],
    [18, 19],
    [19, 20],
    [0, 17],
  ];

  const left = animation[index][2][0];
  const right = animation[index][2][1];

  edges.map((edge) => {
    const u = edge[0];
    const v = edge[1];
    if (left[u] && left[v]) {
      const l1 = left[u];
      const l2 = left[v];
      drawLine(
        l1[1] * SCALE,
        l1[2] * SCALE,
        l1[3] * SCALE,
        l2[1] * SCALE,
        l2[2] * SCALE,
        l2[3] * SCALE,
        [0x00ff00, 1],
        scene
      );
    }
    if (right[u] && right[v]) {
      const r1 = right[u];
      const r2 = right[v];
      drawLine(
        r1[1] * SCALE,
        r1[2] * SCALE,
        r1[3] * SCALE,
        r2[1] * SCALE,
        r2[2] * SCALE,
        r2[3] * SCALE,
        [0x00ff00, 1],
        scene
      );
    }
  });
}

export default function Visualization({
  points,
  getNextWord,
  currentWord,
}: {
  points: number[][];
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

      pose.map((point) =>
        drawPoint(point[1] * SCALE, point[2] * SCALE, point[3] * SCALE)
      );

      left.map((point) =>
        drawPoint(point[1] * SCALE, point[2] * SCALE, point[3] * SCALE)
      );

      right.map((point) =>
        drawPoint(point[1] * SCALE, point[2] * SCALE, point[3] * SCALE)
      );

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
