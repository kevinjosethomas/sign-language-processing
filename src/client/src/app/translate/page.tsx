import React from "react";

import Receptive from "./components/Receptive";
import Expressive from "./components/Expressive";

export default function Translate() {
  return (
    <div className="flex h-screen w-screen items-center bg-neutral-950 p-16">
      <div className="grid h-full w-full grid-cols-2 gap-1 overflow-hidden rounded-xl bg-sky-500">
        <Receptive />
        <Expressive />
      </div>
    </div>
  );
}
