import * as THREE from "three";
import { useEffect, useRef } from "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import {
  useLoader,
  Canvas,
  useThree,
  ThreeElements,
  useFrame,
} from "@react-three/fiber";

export default function Visualization() {
  return (
    <div
      id="canvas-container"
      className="border rounded w-full bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <Canvas>
        <Model />
        <ambientLight intensity={1} />
      </Canvas>
    </div>
  );
}

function Model() {
  const gltf = useLoader(GLTFLoader, "/scene.gltf");
  const { scene } = useThree();

  useEffect(() => {
    scene.add(gltf.scene);
    return () => {
      scene.remove(gltf.scene);
    };
  }, [gltf, scene]);

  return (
    <primitive object={gltf.scene} position={[0, -7.5, 0]} scale={[5, 5, 5]} />
  );
}
