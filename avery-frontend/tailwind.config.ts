import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Legacy navy palette (kept for compatibility)
        navy: {
          50: "#f0f4f8",
          100: "#d9e2ec",
          200: "#bcccdc",
          300: "#9fb3c8",
          400: "#829ab1",
          500: "#627d98",
          600: "#486581",
          700: "#334e68",
          800: "#243b53",
          900: "#102a43",
          950: "#0a1929",
        },
        gold: {
          400: "#f6c744",
          500: "#e5b233",
          600: "#c9991c",
        },
        // Avery AI color palette
        avery: {
          // Backgrounds (dark to light)
          bg: {
            DEFAULT: "#000000",
            subtle: "#0a0a14",
            elevated: "#12121e",
            hover: "#1a1a2e",
          },
          // Primary cyan glow
          cyan: {
            DEFAULT: "#00d4ff",
            dim: "#00a8cc",
            bright: "#4de8ff",
            glow: "rgba(0, 212, 255, 0.5)",
          },
          // Secondary purple
          purple: {
            DEFAULT: "#7c3aed",
            dim: "#6025d1",
            bright: "#9f67ff",
            glow: "rgba(124, 58, 237, 0.5)",
          },
          // Accent teal
          teal: {
            DEFAULT: "#06b6d4",
            dim: "#0891a8",
            bright: "#22d3ee",
            glow: "rgba(6, 182, 212, 0.5)",
          },
          // Text colors
          text: {
            primary: "rgba(255, 255, 255, 0.9)",
            secondary: "#94a3b8",
            muted: "#64748b",
          },
          // Status colors
          success: "#10b981",
          warning: "#f59e0b",
          error: "#ef4444",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(0, 212, 255, 0.3), 0 0 40px rgba(0, 212, 255, 0.2)',
        'glow-purple': '0 0 20px rgba(124, 58, 237, 0.3), 0 0 40px rgba(124, 58, 237, 0.2)',
        'glow-teal': '0 0 20px rgba(6, 182, 212, 0.3), 0 0 40px rgba(6, 182, 212, 0.2)',
      },
      animation: {
        'orb-rotate': 'orbRotate 20s linear infinite',
        'orb-rotate-reverse': 'orbRotateReverse 20s linear infinite',
        'orb-pulse': 'orbPulse 3s ease-in-out infinite',
        'particle-float': 'particleFloat 4s ease-in-out infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
        'shimmer': 'shimmer 2s ease-in-out infinite',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'avery-gradient': 'linear-gradient(135deg, #00d4ff 0%, #7c3aed 50%, #06b6d4 100%)',
        'avery-gradient-subtle': 'linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(124, 58, 237, 0.1) 50%, rgba(6, 182, 212, 0.1) 100%)',
      },
    },
  },
  plugins: [],
};
export default config;
