import React from "react";

import Receptive from "./components/Receptive";
import Expressive from "./components/Expressive";

export default function Translate() {
  return (
    <div className="flex h-screen w-screen items-center bg-white">
      <div className="grid h-full w-full grid-cols-2 items-center justify-center rounded-xl">
        <Receptive />
        <Expressive />
      </div>
    </div>
  );
}
