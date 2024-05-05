import * as THREE from "three";
import { useEffect, useRef } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";

import points from "../../../public/raw_points.json";

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
  color: number,
  scene: THREE.Scene
) {
  const p = [];
  p.push(new THREE.Vector3(x1, -y1, z1));
  p.push(new THREE.Vector3(x2, -y2, z2));
  const geometry = new THREE.BufferGeometry().setFromPoints(p);
  const material = new THREE.LineBasicMaterial({ color: color });
  const line = new THREE.Line(geometry, material);
  scene.add(line);
}

function connectPose(index: number, scene: THREE.Scene) {
  const edges = [
    [11, 12],
    [12, 14],
    [14, 16],
    [11, 13],
    [13, 15],
    [11, 23],
    [12, 24],
  ];

  const pose = points.name[index].pose;

  edges.map((edge) => {
    const u = edge[0];
    const v = edge[1];
    if (pose[u] && pose[v]) {
      const p1 = pose[u];
      const p2 = pose[v];
      drawLine(
        p1.x * SCALE,
        p1.y * SCALE,
        p1.z * SCALE,
        p2.x * SCALE,
        p2.y * SCALE,
        p2.z * SCALE,
        0x494949,
        scene
      );
    }
  });
}

function connectHands(index: number, scene: THREE.Scene) {
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

  const left = points.name[index].hand.left;
  const right = points.name[index].hand.right;

  edges.map((edge) => {
    const u = edge[0];
    const v = edge[1];
    if (left[u] && left[v]) {
      const l1 = left[u];
      const l2 = left[v];
      drawLine(
        l1.x * SCALE,
        l1.y * SCALE,
        l1.z * SCALE,
        l2.x * SCALE,
        l2.y * SCALE,
        l2.z * SCALE,
        0x00ff00,
        scene
      );
    }
    if (right[u] && right[v]) {
      const r1 = right[u];
      const r2 = right[v];
      drawLine(
        r1.x * SCALE,
        r1.y * SCALE,
        r1.z * SCALE,
        r2.x * SCALE,
        r2.y * SCALE,
        r2.z * SCALE,
        0x00ff00,
        scene
      );
    }
  });
}

export default function Visualization({ points }: { points: number[][] }) {
  return (
    <div
      id="canvas-container"
      className="border rounded overflow-hidden h-[540px] bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <Canvas>
        <Sign />
        <ambientLight intensity={1} />
      </Canvas>
    </div>
  );
}

function Sign() {
  const { scene, camera } = useThree();
  const previous_frame = useRef(0);

  useFrame(({ clock, scene }) => {
    const elapsed = clock.getElapsedTime();
    const frame_index = Math.floor(elapsed * 45);

    if (frame_index !== previous_frame.current) {
      previous_frame.current = frame_index;

      if (frame_index >= points.name.length) {
        return;
      }

      scene.remove(...scene.children);

      const left = points.name[0].hand.left;
      const right = points.name[0].hand.right;
      const pose = points.name[0].pose;

      pose.map((point) =>
        drawPoint(point.x * SCALE, point.y * SCALE, point.z * SCALE)
      );

      left.map((point) =>
        drawPoint(point.x * SCALE, point.y * SCALE, point.z * SCALE)
      );

      right.map((point) =>
        drawPoint(point.x * SCALE, point.y * SCALE, point.z * SCALE)
      );

      connectHands(frame_index, scene);
      connectPose(frame_index, scene);
    }
  });

  useEffect(() => {
    camera.position.set(5, -5, 4);
    camera.rotation.set(0, 0, 0);
  }, [camera]);

  return null;
}
