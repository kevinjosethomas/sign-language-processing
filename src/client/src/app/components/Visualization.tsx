import * as THREE from "three";
import { useEffect, useRef } from "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { useLoader, Canvas, useThree } from "@react-three/fiber";

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

const BONE_TO_POINT = [
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

const BONE_SIZES = [];

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
  const gltf = useLoader(GLTFLoader, "/untitled.glb");
  const { scene } = useThree();
  const skeleton = useRef();

  useEffect(() => {
    scene.add(gltf.scene);

    skeleton.current = new THREE.SkeletonHelper(gltf.scene);
    skeleton.current.visible = true;

    console.log(skeleton.current.bones);
    for (let i = 0; i < skeleton.current.bones.length; i++) {
      let bone = skeleton.current.bones[i];
      let child = bone.children[0];

      if (!child) {
        BONE_SIZES.push(1);
      } else {
        BONE_SIZES.push(bone.position.distanceTo(child.position));
      }
    }

    return () => {
      scene.remove(gltf.scene);
      scene.remove(skeleton.current);
    };
  }, [gltf, scene]);

  // function createMatrixFromLandmark(landmark: number[]) {
  //   const matrices = [];
  //   for (const point of points) {
  //     let matrix = new THREE.Matrix4();
  //     matrix.setPosition(new THREE.Vector3(point[0], point[1], point[2]));
  //     matrices.push(matrix);
  //   }
  // }

  useEffect(() => {
    // skeleton.current.bones[1].position.set(0, 0, 0);

    if (!points.length) {
      return;
    }

    const relativePoints = [];

    for (let i = 0; i < points.length; i++) {
      let point = points[i];
      let parent_index = PARENT_POINTS[i];

      if (parent_index == -1) {
        relativePoints.push(point);
        continue;
      }

      let parent = points[parent_index];
      let new_point = [
        point[0] - parent[0],
        point[1] - parent[1],
        point[2] - parent[2],
      ];

      relativePoints.push(new_point);
    }

    for (let i = 1; i < skeleton.current.bones.length; i++) {
      let bone = skeleton.current.bones[i];
      let point_index = BONE_TO_POINT[i];
      let point = relativePoints[point_index];

      bone.position.set(point[1] * 10, -1 * point[1] * 50, point[2] * 50);
    }

    //
    // console.log(points);
    // console.log(skeleton.current.bones);
    // if (!skeleton.current || !points.length) {
    //   return;
    // }
    // for (let i = 0; i < 20; i++) {
    //   skeleton.current.bones[i].position.set(
    //     points[i][0],
    //     points[i][1],
    //     points[i][2]
    //   );
    // }
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
