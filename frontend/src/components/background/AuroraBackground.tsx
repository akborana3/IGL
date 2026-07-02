/** Animated aurora background — pure CSS/SVG, lightweight, no Three.js dependency. */

"use client";

import { useEffect, useRef } from "react";

export function AuroraBackground() {
  const containerRef = useRef<HTMLDivElement>(null);

  // Subtle mouse parallax
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const x = (e.clientX / window.innerWidth - 0.5) * 20;
      const y = (e.clientY / window.innerHeight - 0.5) * 20;
      containerRef.current.style.setProperty("--parallax-x", `${x}px`);
      containerRef.current.style.setProperty("--parallax-y", `${y}px`);
    };
    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 -z-10 pointer-events-none overflow-hidden"
      style={{ "--parallax-x": "0px", "--parallax-y": "0px" } as React.CSSProperties}
    >
      {/* Base gradient */}
      <div className="absolute inset-0 aurora-bg opacity-60" />

      {/* Glowing orbs */}
      <div
        className="absolute -top-20 -left-20 w-[500px] h-[500px] rounded-full opacity-20 blur-[100px] animate-float"
        style={{
          background: "radial-gradient(circle, #a855f7 0%, transparent 70%)",
          transform: "translate(var(--parallax-x), var(--parallax-y))",
        }}
      />
      <div
        className="absolute top-1/3 -right-20 w-[400px] h-[400px] rounded-full opacity-15 blur-[100px] animate-float"
        style={{
          background: "radial-gradient(circle, #3b82f6 0%, transparent 70%)",
          animationDelay: "2s",
          transform: "translate(calc(var(--parallax-x) * -1), var(--parallax-y))",
        }}
      />
      <div
        className="absolute bottom-0 left-1/3 w-[450px] h-[450px] rounded-full opacity-10 blur-[120px] animate-float"
        style={{
          background: "radial-gradient(circle, #ec4899 0%, transparent 70%)",
          animationDelay: "4s",
        }}
      />

      {/* Floating particles via SVG */}
      <svg className="absolute inset-0 w-full h-full opacity-30" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="particleGrad">
            <stop offset="0%" stopColor="#a855f7" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#a855f7" stopOpacity="0" />
          </radialGradient>
        </defs>
        {Array.from({ length: 30 }).map((_, i) => {
          const cx = (i * 37) % 100;
          const cy = (i * 53) % 100;
          const r = 1 + (i % 3);
          const delay = (i % 6) * 0.8;
          return (
            <circle
              key={i}
              cx={`${cx}%`}
              cy={`${cy}%`}
              r={r}
              fill="url(#particleGrad)"
              style={{
                animation: `float ${6 + (i % 4)}s ease-in-out infinite`,
                animationDelay: `${delay}s`,
              }}
            />
          );
        })}
      </svg>

      {/* Animated gradient mesh overlay */}
      <div
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(236, 72, 153, 0.08) 0%, transparent 50%)
          `,
          backgroundSize: "200% 200%",
          animation: "aurora-shift 15s ease infinite",
        }}
      />

      {/* Vignette */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#0a0a0f]" />
    </div>
  );
}