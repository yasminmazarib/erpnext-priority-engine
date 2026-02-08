import type { ReactNode } from "react";
import "./globals.css";
import Navigation from "@/components/Navigation";

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <Navigation />
        {children}
      </body>
    </html>
  );
}
