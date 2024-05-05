import * as THREE from "three";
import { MeshLine, MeshLineMaterial } from "three.meshline";

const SCALE = 0.015;
const BODY_COLOR = [0x686868, 1];

function drawPoint(x: number, y: number, z: number) {
  const geometry = new THREE.SphereGeometry(0.1, 32, 16);
  const material = new THREE.MeshBasicMaterial({ color: 0x84ffff });
  const sphere = new THREE.Mesh(geometry, material);
  sphere.position.set(x * SCALE, -y * SCALE, z * SCALE);
}

function drawLine(
  x1: number,
  y1: number,
  z1: number,
  x2: number,
  y2: number,
  z2: number,
  color: number[],
  scene: THREE.Scene,
  width?: number
) {
  const p = [];
  p.push(new THREE.Vector3(x1, -y1, z1));
  p.push(new THREE.Vector3(x2, -y2, z2));
  const geometry = new THREE.BufferGeometry().setFromPoints(p);
  const material = new MeshLineMaterial({
    color: color[0],
    opacity: color[1],
    lineWidth: width ? width : 0.08,
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
    [12, 14],
    [14, 16],
    [11, 13],
    [13, 15],
    // [11, 12],
    // [11, 23],
    // [12, 24],
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
        [BODY_COLOR[0], 1],
        scene,
        0.2
      );
    }
  });

  if (pose[7] && pose[8]) {
    const point1 = pose[7];
    const point2 = pose[8];
    const p1 = new THREE.Vector3(
      point1[1] * SCALE,
      -point1[2] * SCALE,
      point1[3] * SCALE
    );
    const p2 = new THREE.Vector3(
      point2[1] * SCALE,
      -point2[2] * SCALE,
      point2[3] * SCALE
    );

    let midPoint = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
    let distance = p1.distanceTo(p2);

    let majorRadius = distance / 2;
    let minorRadius = majorRadius * 1.25;

    const path = new THREE.Shape();
    path.absellipse(
      midPoint.x,
      midPoint.y,
      majorRadius,
      minorRadius,
      0,
      Math.PI * 2,
      false,
      0
    );
    const geometry = new THREE.ShapeGeometry(path, 20);
    const material = new THREE.MeshBasicMaterial({
      color: BODY_COLOR[0],
      opacity: BODY_COLOR[1],
      transparent: true,
      depthTest: false,
      side: THREE.DoubleSide,
    });
    const ellipse = new THREE.Mesh(geometry, material);
    ellipse.position.set(0, -0.8, 0);
    scene.add(ellipse);
  }

  if (pose[11] && pose[12] && pose[23] && pose[24]) {
    const p1 = pose[11];
    const p2 = pose[12];
    const p3 = pose[24];
    const p4 = pose[23];
    const points = [
      new THREE.Vector2(p1[1] * SCALE, -p1[2] * SCALE),
      new THREE.Vector2(p2[1] * SCALE, -p2[2] * SCALE),
      new THREE.Vector2(p3[1] * SCALE, -p3[2] * SCALE),
      new THREE.Vector2(p4[1] * SCALE, -p4[2] * SCALE),
    ];
    const path = new THREE.Shape(points);
    const geometry = new THREE.ShapeGeometry(path);
    const material = new THREE.MeshBasicMaterial({
      color: BODY_COLOR[0],
      opacity: 0.2,
      transparent: true,
      depthTest: false,
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
  }
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

export { drawPoint, drawLine, connectPose, connectHands };
