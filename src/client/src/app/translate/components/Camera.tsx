import { Hands } from "@mediapipe/hands";
import * as cam from "@mediapipe/camera_utils";
import React, { useRef, useEffect } from "react";

const Camera = () => {
  const video = useRef(null);
  const canvas = useRef(null);
  const ctx = useRef(null);

  useEffect(() => {
    ctx.current = canvas.current.getContext("2d");

    const hands = new Hands({
      locateFile: (file) => {
        return `/landmarker/${file}`;
      },
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    hands.onResults(onResults);

    const camera = new cam.Camera(video.current, {
      onFrame: async () => {
        await hands.send({ image: video.current });
      },
    });
    camera.start();

    function onResults(results) {
      ctx.current.clearRect(0, 0, canvas.current.width, canvas.current.height);
      ctx.current.drawImage(
        results.image,
        0,
        0,
        canvas.current.width,
        canvas.current.height
      );
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawLandmarks(ctx.current, landmarks);
        }
      }
    }

    function drawLandmarks(ctx, landmarks) {
      ctx.fillStyle = "#00FF00";
      ctx.strokeStyle = "#FF0000";
      ctx.lineWidth = 2;
      for (let i = 0; i < landmarks.length; i++) {
        const x = landmarks[i].x * canvas.current.width;
        const y = landmarks[i].y * canvas.current.height;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  }, []);

  return (
    <div>
      <video ref={video} style={{ display: "none" }}></video>
      <canvas ref={canvas} width="960" height="720"></canvas>
    </div>
  );
};

export default Camera;
