import * as THREE from "three";
import { useEffect, useRef } from "react";
import { useLoader, Canvas, useThree } from "@react-three/fiber";

import points from "../../../public/points.json";

export default function Visualization({ points }: { points: number[][] }) {
  return (
    <div
      id="canvas-container"
      className="border rounded w-full bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <Canvas>
        <Sign />
        <ambientLight intensity={1} />
      </Canvas>
    </div>
  );
}

function Sign() {
  const { scene } = useThree(); // Get the scene from the context
  useEffect(() => {
    for (const point of points.again[0].pose) {
      let geometry = new THREE.SphereGeometry(0.1, 32, 16);
      let material = new THREE.MeshBasicMaterial({ color: 0x84ffff });
      let sphere = new THREE.Mesh(geometry, material);

      scene.add(sphere); // Add the cube to the scene

      sphere.position.set(point.x, point.y, point.z);
    }
  }, []);

  return null;
}
