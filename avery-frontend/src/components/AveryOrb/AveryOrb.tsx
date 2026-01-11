'use client';

import React, { useEffect, useState } from 'react';

export type OrbState = 'dormant' | 'awakening' | 'attentive' | 'processing' | 'presenting';
export type OrbSize = 'small' | 'medium' | 'large';

interface AveryOrbProps {
  state?: OrbState;
  size?: OrbSize;
  className?: string;
  onAwakeningComplete?: () => void;
}

const sizeConfig = {
  small: { container: 80, orb: 48, ring1: 60, ring2: 72, ring3: 84 },
  medium: { container: 200, orb: 120, ring1: 150, ring2: 175, ring3: 200 },
  large: { container: 320, orb: 200, ring1: 250, ring2: 290, ring3: 330 },
};

const stateConfig = {
  dormant: {
    orbOpacity: 0.3,
    glowIntensity: 0.3,
    ringSpeed: 0,
    particleSpeed: 0,
    colorShift: false,
  },
  awakening: {
    orbOpacity: 1,
    glowIntensity: 1,
    ringSpeed: 1,
    particleSpeed: 1,
    colorShift: false,
  },
  attentive: {
    orbOpacity: 1,
    glowIntensity: 0.8,
    ringSpeed: 1,
    particleSpeed: 1,
    colorShift: false,
  },
  processing: {
    orbOpacity: 1,
    glowIntensity: 1,
    ringSpeed: 3,
    particleSpeed: 3,
    colorShift: true,
  },
  presenting: {
    orbOpacity: 1,
    glowIntensity: 0.7,
    ringSpeed: 0.5,
    particleSpeed: 0.5,
    colorShift: false,
  },
};

// Generate random particles
const generateParticles = (count: number, containerSize: number) => {
  return Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * containerSize,
    y: Math.random() * containerSize,
    size: Math.random() * 3 + 1,
    delay: Math.random() * 5,
    duration: Math.random() * 3 + 2,
    angle: Math.random() * 360,
  }));
};

export const AveryOrb: React.FC<AveryOrbProps> = ({
  state = 'dormant',
  size = 'large',
  className = '',
  onAwakeningComplete,
}) => {
  const [currentOpacity, setCurrentOpacity] = useState(
    state === 'dormant' ? 0.3 : 1
  );
  const [isAwakening, setIsAwakening] = useState(false);

  const sizes = sizeConfig[size];
  const config = stateConfig[state];
  const particles = generateParticles(
    size === 'small' ? 8 : size === 'medium' ? 15 : 24,
    sizes.container
  );

  // Handle awakening animation
  useEffect(() => {
    if (state === 'awakening' && !isAwakening) {
      setIsAwakening(true);
      setCurrentOpacity(0.3);

      // Fade in over 1.5s
      const fadeTimeout = setTimeout(() => {
        setCurrentOpacity(1);
      }, 100);

      // Callback when awakening complete
      const completeTimeout = setTimeout(() => {
        setIsAwakening(false);
        onAwakeningComplete?.();
      }, 1500);

      return () => {
        clearTimeout(fadeTimeout);
        clearTimeout(completeTimeout);
      };
    } else if (state !== 'awakening') {
      setCurrentOpacity(config.orbOpacity);
    }
  }, [state, isAwakening, config.orbOpacity, onAwakeningComplete]);

  const ringAnimationDuration = config.ringSpeed > 0
    ? `${20 / config.ringSpeed}s`
    : '0s';

  const particleAnimationDuration = config.particleSpeed > 0
    ? `${4 / config.particleSpeed}s`
    : '0s';

  return (
    <div
      className={`avery-orb-container relative ${className}`}
      style={{
        width: sizes.container,
        height: sizes.container,
      }}
    >
      <svg
        viewBox={`0 0 ${sizes.container} ${sizes.container}`}
        className="w-full h-full"
        style={{ overflow: 'visible' }}
      >
        <defs>
          {/* Core orb gradient */}
          <radialGradient id={`orbGradient-${size}`} cx="30%" cy="30%" r="70%">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.9" />
            <stop offset="40%" stopColor="#7c3aed" stopOpacity="0.7" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.3" />
          </radialGradient>

          {/* Processing color shift gradient */}
          <radialGradient id={`processingGradient-${size}`} cx="30%" cy="30%" r="70%">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.9">
              {config.colorShift && (
                <animate
                  attributeName="stop-color"
                  values="#00d4ff;#7c3aed;#06b6d4;#00d4ff"
                  dur="2s"
                  repeatCount="indefinite"
                />
              )}
            </stop>
            <stop offset="50%" stopColor="#7c3aed" stopOpacity="0.7">
              {config.colorShift && (
                <animate
                  attributeName="stop-color"
                  values="#7c3aed;#06b6d4;#00d4ff;#7c3aed"
                  dur="2s"
                  repeatCount="indefinite"
                />
              )}
            </stop>
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.3" />
          </radialGradient>

          {/* Outer glow filter */}
          <filter id={`glow-${size}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={sizes.orb * 0.08} result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          {/* Inner glow */}
          <filter id={`innerGlow-${size}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation={sizes.orb * 0.15} result="blur" />
            <feFlood floodColor="#00d4ff" floodOpacity={config.glowIntensity * 0.5} />
            <feComposite in2="blur" operator="in" />
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Ring gradient */}
          <linearGradient id={`ringGradient-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.8" />
            <stop offset="50%" stopColor="#7c3aed" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.8" />
          </linearGradient>
        </defs>

        {/* Ambient glow background */}
        <circle
          cx={sizes.container / 2}
          cy={sizes.container / 2}
          r={sizes.orb * 0.8}
          fill="none"
          style={{
            filter: `drop-shadow(0 0 ${sizes.orb * 0.3}px rgba(0, 212, 255, ${config.glowIntensity * 0.4}))`,
          }}
        />

        {/* Orbital Ring 1 - outermost */}
        <g
          className="orb-ring"
          style={{
            transformOrigin: 'center',
            animation: config.ringSpeed > 0
              ? `orbRotate ${ringAnimationDuration} linear infinite`
              : 'none',
          }}
        >
          <ellipse
            cx={sizes.container / 2}
            cy={sizes.container / 2}
            rx={sizes.ring3 / 2}
            ry={sizes.ring3 / 4}
            fill="none"
            stroke={`url(#ringGradient-${size})`}
            strokeWidth={1}
            opacity={config.ringSpeed > 0 ? 0.6 : 0}
            style={{
              transform: 'rotateX(70deg) rotateZ(-20deg)',
              transformOrigin: 'center',
            }}
          />
        </g>

        {/* Orbital Ring 2 */}
        <g
          className="orb-ring"
          style={{
            transformOrigin: 'center',
            animation: config.ringSpeed > 0
              ? `orbRotateReverse ${ringAnimationDuration} linear infinite`
              : 'none',
            animationDelay: '-3s',
          }}
        >
          <ellipse
            cx={sizes.container / 2}
            cy={sizes.container / 2}
            rx={sizes.ring2 / 2}
            ry={sizes.ring2 / 3.5}
            fill="none"
            stroke={`url(#ringGradient-${size})`}
            strokeWidth={1.5}
            opacity={config.ringSpeed > 0 ? 0.8 : 0}
            style={{
              transform: 'rotateX(60deg) rotateZ(30deg)',
              transformOrigin: 'center',
            }}
          />
        </g>

        {/* Orbital Ring 3 - innermost, most visible */}
        <g
          className="orb-ring"
          style={{
            transformOrigin: 'center',
            animation: config.ringSpeed > 0
              ? `orbRotate ${parseFloat(ringAnimationDuration) * 0.8}s linear infinite`
              : 'none',
            animationDelay: '-7s',
          }}
        >
          <ellipse
            cx={sizes.container / 2}
            cy={sizes.container / 2}
            rx={sizes.ring1 / 2}
            ry={sizes.ring1 / 3}
            fill="none"
            stroke={`url(#ringGradient-${size})`}
            strokeWidth={2}
            opacity={config.ringSpeed > 0 ? 1 : 0.3}
            style={{
              transform: 'rotateX(65deg) rotateZ(-45deg)',
              transformOrigin: 'center',
            }}
          />
        </g>

        {/* Core orb - outer glow layer */}
        <circle
          cx={sizes.container / 2}
          cy={sizes.container / 2}
          r={sizes.orb / 2 + 5}
          fill={`url(#${config.colorShift ? `processingGradient-${size}` : `orbGradient-${size}`})`}
          opacity={currentOpacity * 0.3}
          filter={`url(#glow-${size})`}
          className="orb-glow"
          style={{
            animation: config.glowIntensity > 0.5
              ? `orbPulse ${config.colorShift ? '1s' : '3s'} ease-in-out infinite`
              : 'none',
            transition: 'opacity 1.5s ease-in-out',
          }}
        />

        {/* Core orb - main sphere */}
        <circle
          cx={sizes.container / 2}
          cy={sizes.container / 2}
          r={sizes.orb / 2}
          fill={`url(#${config.colorShift ? `processingGradient-${size}` : `orbGradient-${size}`})`}
          opacity={currentOpacity}
          filter={`url(#innerGlow-${size})`}
          className="orb-core"
          style={{
            transition: 'opacity 1.5s ease-in-out',
          }}
        />

        {/* Inner highlight */}
        <ellipse
          cx={sizes.container / 2 - sizes.orb * 0.15}
          cy={sizes.container / 2 - sizes.orb * 0.15}
          rx={sizes.orb * 0.2}
          ry={sizes.orb * 0.12}
          fill="white"
          opacity={currentOpacity * 0.3}
          style={{
            transition: 'opacity 1.5s ease-in-out',
          }}
        />

        {/* Particles */}
        {particles.map((particle) => (
          <circle
            key={particle.id}
            cx={particle.x}
            cy={particle.y}
            r={particle.size}
            fill="#00d4ff"
            opacity={config.particleSpeed > 0 ? 0.8 : 0}
            className="orb-particle"
            style={{
              animation: config.particleSpeed > 0
                ? `particleFloat ${particleAnimationDuration} ease-in-out infinite`
                : 'none',
              animationDelay: `${particle.delay}s`,
              transformOrigin: `${sizes.container / 2}px ${sizes.container / 2}px`,
            }}
          />
        ))}

        {/* Processing burst particles */}
        {config.colorShift && (
          <>
            {[0, 45, 90, 135, 180, 225, 270, 315].map((angle) => (
              <circle
                key={`burst-${angle}`}
                cx={sizes.container / 2}
                cy={sizes.container / 2}
                r={2}
                fill="#00d4ff"
                className="burst-particle"
                style={{
                  animation: `particleBurst 1.5s ease-out infinite`,
                  animationDelay: `${angle / 360}s`,
                  transformOrigin: 'center',
                  '--burst-angle': `${angle}deg`,
                } as React.CSSProperties}
              />
            ))}
          </>
        )}
      </svg>

      {/* Reflection/ground glow */}
      {size !== 'small' && (
        <div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 w-3/4 h-4 rounded-full blur-xl"
          style={{
            background: `radial-gradient(ellipse, rgba(0, 212, 255, ${config.glowIntensity * 0.3}) 0%, transparent 70%)`,
            transition: 'opacity 1.5s ease-in-out',
            opacity: currentOpacity,
          }}
        />
      )}
    </div>
  );
};

export default AveryOrb;
