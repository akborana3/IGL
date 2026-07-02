import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          purple: "#a855f7",
          blue: "#3b82f6",
          pink: "#ec4899",
        },
        glass: {
          light: "rgba(255, 255, 255, 0.08)",
          DEFAULT: "rgba(255, 255, 255, 0.05)",
          dark: "rgba(0, 0, 0, 0.25)",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "aurora-gradient": "linear-gradient(135deg, #1a0b2e 0%, #0f172a 50%, #1e1b4b 100%)",
        "glass-gradient": "linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.02) 100%)",
        "neon-glow": "radial-gradient(circle, rgba(168,85,247,0.3) 0%, transparent 70%)",
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        "neon-purple": "0 0 20px rgba(168, 85, 247, 0.5)",
        "neon-blue": "0 0 20px rgba(59, 130, 246, 0.5)",
        "premium": "0 10px 40px -10px rgba(0, 0, 0, 0.5)",
      },
      animation: {
        "aurora-shift": "aurora-shift 15s ease infinite",
        "float": "float 6s ease-in-out infinite",
        "shimmer": "shimmer 2s linear infinite",
        "fade-in": "fade-in 0.5s ease forwards",
        "slide-up": "slide-up 0.5s ease forwards",
        "glow-pulse": "glow-pulse 3s ease-in-out infinite",
      },
      keyframes: {
        "aurora-shift": {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-20px)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-1000px 0" },
          "100%": { backgroundPosition: "1000px 0" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(20px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "glow-pulse": {
          "0%, 100%": { boxShadow: "0 0 20px rgba(168, 85, 247, 0.3)" },
          "50%": { boxShadow: "0 0 40px rgba(168, 85, 247, 0.6)" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};

export default config;