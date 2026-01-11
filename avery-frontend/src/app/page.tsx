"use client";

import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
        {/* Logo/Icon */}
        <div className="mb-8 animate-fade-in">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center shadow-2xl">
            <svg
              className="w-14 h-14 text-navy-900"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-4xl font-bold text-center mb-4 animate-slide-up">
          Welcome to <span className="text-gold-400">Avery</span>
        </h1>

        {/* Subtitle */}
        <p className="text-navy-300 text-center text-lg mb-8 max-w-sm animate-slide-up">
          Your guide to transitioning from Navy service to a rewarding cybersecurity career.
        </p>

        {/* Features */}
        <div className="space-y-4 mb-12 w-full max-w-sm animate-slide-up">
          <div className="flex items-center gap-4 bg-navy-800/50 rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0">
              <span className="text-gold-400 font-bold">1</span>
            </div>
            <p className="text-navy-200 text-sm">Tell us about your Navy experience</p>
          </div>
          
          <div className="flex items-center gap-4 bg-navy-800/50 rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0">
              <span className="text-gold-400 font-bold">2</span>
            </div>
            <p className="text-navy-200 text-sm">Take a quick personality assessment</p>
          </div>
          
          <div className="flex items-center gap-4 bg-navy-800/50 rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0">
              <span className="text-gold-400 font-bold">3</span>
            </div>
            <p className="text-navy-200 text-sm">Discover your top 3 cybersecurity roles</p>
          </div>
        </div>

        {/* CTA Button */}
        <Link
          href="/onboarding"
          className="w-full max-w-sm bg-gradient-to-r from-gold-400 to-gold-500 text-navy-900 font-semibold py-4 px-8 rounded-2xl text-center text-lg shadow-lg active:scale-[0.98] transition-transform"
        >
          Get Started
        </Link>

        {/* Footer text */}
        <p className="text-navy-500 text-xs mt-8 text-center">
          Built for sailors, by those who understand service.
        </p>
      </div>
    </main>
  );
}
