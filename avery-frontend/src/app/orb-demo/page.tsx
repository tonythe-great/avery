'use client';

import React, { useState } from 'react';
import { AveryOrb, OrbState, OrbSize } from '@/components/AveryOrb';

const states: OrbState[] = ['dormant', 'awakening', 'attentive', 'processing', 'presenting'];
const sizes: OrbSize[] = ['small', 'medium', 'large'];

export default function OrbDemoPage() {
  const [activeState, setActiveState] = useState<OrbState>('attentive');
  const [activeSize, setActiveSize] = useState<OrbSize>('large');

  return (
    <div className="min-h-screen bg-avery-bg flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-avery-text-primary mb-2">
          Avery Orb Component
        </h1>
        <p className="text-avery-text-secondary">
          Interactive demo of all orb states and sizes
        </p>
      </div>

      {/* Main Orb Display */}
      <div className="flex items-center justify-center mb-12 min-h-[350px]">
        <AveryOrb
          state={activeState}
          size={activeSize}
          onAwakeningComplete={() => console.log('Awakening complete!')}
        />
      </div>

      {/* Controls */}
      <div className="w-full max-w-2xl space-y-8">
        {/* State Controls */}
        <div className="bg-avery-bg-elevated rounded-xl p-6 border border-avery-bg-hover">
          <h2 className="text-lg font-semibold text-avery-text-primary mb-4">
            Orb State
          </h2>
          <div className="flex flex-wrap gap-3">
            {states.map((state) => (
              <button
                key={state}
                onClick={() => setActiveState(state)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                  activeState === state
                    ? 'bg-avery-cyan text-black shadow-glow-cyan'
                    : 'bg-avery-bg-hover text-avery-text-secondary hover:text-avery-text-primary hover:bg-avery-bg-hover/80'
                }`}
              >
                {state.charAt(0).toUpperCase() + state.slice(1)}
              </button>
            ))}
          </div>

          {/* State Description */}
          <div className="mt-4 p-4 bg-avery-bg-subtle rounded-lg">
            <p className="text-avery-text-secondary text-sm">
              {activeState === 'dormant' && (
                <>
                  <span className="text-avery-cyan font-semibold">Dormant:</span> Orb is dim, rings are still, no particles.
                  Used before user interaction begins.
                </>
              )}
              {activeState === 'awakening' && (
                <>
                  <span className="text-avery-cyan font-semibold">Awakening:</span> Orb fades from 30% to 100% opacity
                  over 1.5s. Rings begin to rotate. Used on welcome screen initialization.
                </>
              )}
              {activeState === 'attentive' && (
                <>
                  <span className="text-avery-cyan font-semibold">Attentive:</span> Orb is bright with gentle pulse.
                  Rings rotate slowly, particles drift. Used when awaiting user input.
                </>
              )}
              {activeState === 'processing' && (
                <>
                  <span className="text-avery-cyan font-semibold">Processing:</span> Rings spin 3x faster,
                  colors cycle cyan→purple→teal. Burst particles emit. Used during analysis.
                </>
              )}
              {activeState === 'presenting' && (
                <>
                  <span className="text-avery-cyan font-semibold">Presenting:</span> Steady, confident glow with
                  slow rotation. Used when showing results and recommendations.
                </>
              )}
            </p>
          </div>
        </div>

        {/* Size Controls */}
        <div className="bg-avery-bg-elevated rounded-xl p-6 border border-avery-bg-hover">
          <h2 className="text-lg font-semibold text-avery-text-primary mb-4">
            Orb Size
          </h2>
          <div className="flex flex-wrap gap-3">
            {sizes.map((size) => (
              <button
                key={size}
                onClick={() => setActiveSize(size)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                  activeSize === size
                    ? 'bg-avery-purple text-white shadow-glow-purple'
                    : 'bg-avery-bg-hover text-avery-text-secondary hover:text-avery-text-primary hover:bg-avery-bg-hover/80'
                }`}
              >
                {size.charAt(0).toUpperCase() + size.slice(1)}
                <span className="text-xs ml-2 opacity-60">
                  ({size === 'small' ? '80px' : size === 'medium' ? '200px' : '320px'})
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* All States Preview */}
        <div className="bg-avery-bg-elevated rounded-xl p-6 border border-avery-bg-hover">
          <h2 className="text-lg font-semibold text-avery-text-primary mb-4">
            All States (Small)
          </h2>
          <div className="flex flex-wrap justify-center gap-8">
            {states.map((state) => (
              <div key={state} className="flex flex-col items-center gap-2">
                <AveryOrb state={state} size="small" />
                <span className="text-xs text-avery-text-muted capitalize">{state}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Usage Code */}
      <div className="w-full max-w-2xl mt-8 bg-avery-bg-elevated rounded-xl p-6 border border-avery-bg-hover">
        <h2 className="text-lg font-semibold text-avery-text-primary mb-4">
          Usage
        </h2>
        <pre className="bg-avery-bg-subtle p-4 rounded-lg text-sm text-avery-text-secondary overflow-x-auto">
{`import { AveryOrb } from '@/components/AveryOrb';

// Basic usage
<AveryOrb state="attentive" size="large" />

// With callback
<AveryOrb
  state="awakening"
  size="medium"
  onAwakeningComplete={() => {
    // Triggered when awakening animation completes
    setCurrentState('attentive');
  }}
/>

// Available states:
// 'dormant' | 'awakening' | 'attentive' | 'processing' | 'presenting'

// Available sizes:
// 'small' (80px) | 'medium' (200px) | 'large' (320px)`}
        </pre>
      </div>
    </div>
  );
}
