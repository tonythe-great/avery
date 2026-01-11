"use client";

import Link from "next/link";
import { AveryOrb } from "@/components/AveryOrb";

export default function Home() {
  return (
    <main className="min-h-screen bg-avery-bg text-white relative overflow-hidden">
      {/* Background gradient overlay */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background: `
            radial-gradient(ellipse at 50% 30%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(124, 58, 237, 0.08) 0%, transparent 40%),
            radial-gradient(ellipse at 20% 90%, rgba(6, 182, 212, 0.06) 0%, transparent 40%)
          `,
        }}
      />

      {/* Hero Section */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-12">
        {/* Avery Orb */}
        <div className="mb-6 animate-fade-in">
          <AveryOrb state="attentive" size="medium" />
        </div>

        {/* Title */}
        <h1 className="text-4xl font-bold text-center mb-3 animate-slide-up">
          <span className="text-avery-text-primary">Meet </span>
          <span className="text-avery-cyan">Avery</span>
        </h1>

        {/* Subtitle */}
        <p className="text-avery-text-secondary text-center text-lg mb-10 max-w-sm animate-slide-up">
          Your AI career intelligence system for cybersecurity.
        </p>

        {/* Features */}
        <div className="space-y-3 mb-10 w-full max-w-sm animate-slide-up">
          <div className="flex items-center gap-4 bg-avery-bg-elevated/50 border border-avery-bg-hover rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-avery-cyan/10 flex items-center justify-center flex-shrink-0">
              <span className="text-avery-cyan font-semibold">01</span>
            </div>
            <p className="text-avery-text-secondary text-sm">Share your military experience</p>
          </div>

          <div className="flex items-center gap-4 bg-avery-bg-elevated/50 border border-avery-bg-hover rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-avery-purple/10 flex items-center justify-center flex-shrink-0">
              <span className="text-avery-purple font-semibold">02</span>
            </div>
            <p className="text-avery-text-secondary text-sm">Avery analyzes your profile</p>
          </div>

          <div className="flex items-center gap-4 bg-avery-bg-elevated/50 border border-avery-bg-hover rounded-xl p-4 backdrop-blur">
            <div className="w-10 h-10 rounded-full bg-avery-teal/10 flex items-center justify-center flex-shrink-0">
              <span className="text-avery-teal font-semibold">03</span>
            </div>
            <p className="text-avery-text-secondary text-sm">Get matched to high-paying roles</p>
          </div>
        </div>

        {/* CTA Button */}
        <Link
          href="/start"
          className="w-full max-w-sm bg-gradient-to-r from-avery-cyan to-avery-teal text-black font-semibold
                     py-4 px-8 rounded-2xl text-center text-lg shadow-glow-cyan
                     hover:shadow-[0_0_40px_rgba(0,212,255,0.5)] active:scale-[0.98] transition-all duration-300"
        >
          Begin Session
        </Link>

        {/* Secondary link to old onboarding (for comparison) */}
        <Link
          href="/onboarding"
          className="text-avery-text-muted text-xs mt-6 hover:text-avery-text-secondary transition-colors"
        >
          Use classic onboarding
        </Link>

        {/* Footer text */}
        <p className="text-avery-text-muted text-xs mt-8 text-center">
          Powered by career intelligence
        </p>
      </div>
    </main>
  );
}
