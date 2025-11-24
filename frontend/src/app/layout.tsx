import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "../components/Navbar";
import LiquidEther from "../components/LiquidEther";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Crypto Bank",
  description: "A decentralized token banking application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased text-foreground`}>
        <div className="relative min-h-screen overflow-hidden bg-slate-950">
          <LiquidEther
            className="pointer-events-none"
            colors={["#5227FF", "#FF9FFC", "#B19EEF"]}
            mouseForce={16}
            cursorSize={120}
            isViscous
            viscous={22}
            iterationsViscous={24}
            iterationsPoisson={24}
            resolution={0.28}
            autoIntensity={1.8}
            autoSpeed={0.35}
            autoRampDuration={0.7}
            autoResumeDelay={4000}
            minViewportWidth={900}
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              width: "100%",
              height: "100%",
              zIndex: 0,
            }}
          />
          <div className="fixed inset-0 bg-gradient-to-br from-indigo-950/80 via-purple-900/60 to-blue-900/80 -z-10" />
          <div className="relative z-10 flex min-h-screen flex-col backdrop-blur-[2px]">
            <Navbar />
            <main className="flex-grow container mx-auto px-4 py-8">
              {children}
            </main>
            <footer className="text-center py-4 text-sm text-white/70">
              <p>&copy; 2025 Crypto Bank. All rights reserved.</p>
            </footer>
          </div>
        </div>
      </body>
    </html>
  );
}