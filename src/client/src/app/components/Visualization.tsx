import * as THREE from "three";
import { useEffect, useRef } from "react";
import { useLoader, Canvas, useThree } from "@react-three/fiber";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

const PARENT_POINTS = [
  -1, // Palm (Root)
  0, // Thumb 1
  1, // Thumb 2
  2, // Thumb 3
  3, // Thumb 4
  0, // Index 1
  5, // Index 2
  6, // Index 3
  7, // Index 4
  0, // Middle 1
  9, // Middle 2
  10, // Middle 3
  11, // Middle 4
  0, // Ring 1
  13, // Ring 2
  14, // Ring 3
  15, // Ring 4
  0, // Pinky 1
  17, // Pinky 2
  18, // Pinky 3
  19, // Pinky 4
];

const BONE_TO_STARTING_POINT = [
  0, // Palm -> Thumb
  1, // Thumb 1 -> Thumb 2
  2, // Thumb 2 -> Thumb 3
  3, // Thumb 3 -> Thumb 4
  0, // Palm -> Index 1
  5, // Index 1 -> Index 2
  6, // Index 2 -> Index 3
  7, // Index 3 -> Index 4
  0, // Palm -> Middle 1
  9, // Middle 1 -> Middle 2
  10, // Middle 2 -> Middle 3
  11, // Middle 3 -> Middle 4
  0, // Palm -> Ring 1
  13, // Ring 1 -> Ring 2
  14, // Ring 2 -> Ring 3
  15, // Ring 3 -> Ring 4
  0, // Palm -> Pinky 1
  17, // Pinky 1 -> Pinky 2
  18, // Pinky 2 -> Pinky 3
  19, // Pinky 3 -> Pinky 4
];

export default function Visualization({ points }: { points: number[][] }) {
  return (
    <div
      id="canvas-container"
      className="border rounded w-full bg-gradient-to-br from-neutral-800 to-neutral-950"
    >
      <Canvas>
        <Model points={points} />
        <ambientLight intensity={1} />
      </Canvas>
    </div>
  );
}

function Model({ points }: { points: number[][] }) {
  const gltf = useLoader(GLTFLoader, "/2.glb");
  const { scene } = useThree();
  const skeleton = useRef();

  useEffect(() => {
    scene.add(gltf.scene);

    skeleton.current = new THREE.SkeletonHelper(gltf.scene);
    skeleton.current.visible = true;

    return () => {
      scene.remove(gltf.scene);
      scene.remove(skeleton.current);
    };
  }, [gltf, scene]);

  useEffect(() => {
    if (!points.length) {
      return;
    }

    const rotation = [null];

    for (let i = 1; i < points.length; i++) {
      let point = new THREE.Vector3(...points[i]);
      let parent = new THREE.Vector3(...points[PARENT_POINTS[i]]);
      let direction = new THREE.Vector3().subVectors(parent, point).normalize();

      const parentDirection = new THREE.Vector3(0, 1, 0); // Assuming the default bone direction is up the y-axis
      let quaternion = new THREE.Quaternion();
      quaternion.setFromUnitVectors(parentDirection, direction);

      if ([2, 3, 6, 7, 10, 11, 14, 15, 18, 19].includes(i)) {
        let euler = new THREE.Euler().setFromQuaternion(quaternion, "XYZ");

        euler.y = 0;
        euler.z = 0;
        euler.x = -1 * Math.abs(euler.x);

        quaternion.setFromEuler(euler);
      }

      rotation.push(quaternion);
    }

    for (let i = 1; i < skeleton.current.bones.length; i++) {
      let bone = skeleton.current.bones[i];
      let r = rotation[i + 1];

      bone.rotation.setFromQuaternion(r);
    }
  }, [points]);

  return (
    <>
      <primitive
        object={gltf.scene}
        position={[0, -4, 0]}
        scale={[0.4, 0.4, 0.4]}
      />
      {skeleton.current && (
        <primitive
          object={skeleton.current}
          position={[0, -4, 0]}
          scale={[0.4, 0.4, 0.4]}
        />
      )}
    </>
  );
}
