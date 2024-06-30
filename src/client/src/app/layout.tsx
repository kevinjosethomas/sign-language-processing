import type { Metadata } from "next";
import { Inter } from "next/font/google";

import "@/ui/tailwind.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ASL Sign Language Recognition",
  description: "ASL Sign Language Recognition",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://pro.fontawesome.com/releases/v5.15.1/css/all.css"
        />
      </head>
      <body className={`${inter.className} bg-black`}>{children}</body>
    </html>
  );
}
