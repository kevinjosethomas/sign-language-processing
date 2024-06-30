import { Hands } from "@mediapipe/hands";
import * as cam from "@mediapipe/camera_utils";
import React, { useRef, useEffect } from "react";

const Camera = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const contextRef = useRef(null);

  useEffect(() => {
    contextRef.current = canvasRef.current.getContext("2d");

    const hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      },
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    hands.onResults(onResults);

    const camera = new cam.Camera(videoRef.current, {
      onFrame: async () => {
        await hands.send({ image: videoRef.current });
      },
    });
    camera.start();

    function onResults(results) {
      contextRef.current.clearRect(
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );
      contextRef.current.drawImage(
        results.image,
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawLandmarks(contextRef.current, landmarks);
        }
      }
    }

    function drawLandmarks(ctx, landmarks) {
      ctx.fillStyle = "#00FF00";
      ctx.strokeStyle = "#FF0000";
      ctx.lineWidth = 2;
      for (let i = 0; i < landmarks.length; i++) {
        const x = landmarks[i].x * canvasRef.current.width;
        const y = landmarks[i].y * canvasRef.current.height;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
      }
    }
  }, []);

  return (
    <div>
      <video ref={videoRef} style={{ display: "none" }}></video>
      <canvas ref={canvasRef} width="960" height="720"></canvas>
    </div>
  );
};

export default Camera;
