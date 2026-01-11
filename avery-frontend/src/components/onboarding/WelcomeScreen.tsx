'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { TypewriterText } from '@/components/ui/TypewriterText';
import { GlowButton } from '@/components/ui/GlowButton';
import { ProgressDots } from '@/components/ui/ProgressDots';

interface WelcomeScreenProps {
  onInitialize: () => void;
}

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onInitialize }) => {
  const [orbState, setOrbState] = useState<'dormant' | 'awakening' | 'attentive'>('dormant');
  const [showTitle, setShowTitle] = useState(false);
  const [showSubtitle, setShowSubtitle] = useState(false);
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    // Start awakening sequence after a brief pause
    const awakeningTimer = setTimeout(() => {
      setOrbState('awakening');
    }, 500);

    return () => clearTimeout(awakeningTimer);
  }, []);

  const handleAwakeningComplete = useCallback(() => {
    setOrbState('attentive');
    setShowTitle(true);
  }, []);

  const handleTitleComplete = useCallback(() => {
    setShowSubtitle(true);
  }, []);

  const handleSubtitleComplete = useCallback(() => {
    setShowButton(true);
  }, []);

  return (
    <div className="flex flex-col items-center min-h-screen min-h-[100dvh] px-6 py-8 safe-area-inset">
      {/* Avery Orb - responsive size */}
      <div className="flex-shrink-0 mt-auto mb-6">
        <AveryOrb
          state={orbState}
          size="medium"
          onAwakeningComplete={handleAwakeningComplete}
        />
      </div>

      {/* Text Content */}
      <div className="text-center mb-6 min-h-[100px] flex flex-col items-center justify-center">
        {showTitle && (
          <h1 className="text-3xl sm:text-4xl font-bold text-avery-text-primary mb-3">
            <TypewriterText
              text="I am Avery."
              speed={80}
              onComplete={handleTitleComplete}
              cursor={!showSubtitle}
            />
          </h1>
        )}

        {showSubtitle && (
          <p className="text-lg sm:text-xl text-avery-text-secondary">
            <TypewriterText
              text="Your career intelligence system."
              speed={40}
              onComplete={handleSubtitleComplete}
              cursor={!showButton}
            />
          </p>
        )}
      </div>

      {/* Initialize Button - always visible area */}
      <div className={`w-full max-w-xs mb-4 transition-all duration-500 ${showButton ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <GlowButton
          variant="primary"
          size="lg"
          onClick={onInitialize}
          disabled={!showButton}
          className="w-full"
        >
          Initialize
        </GlowButton>
      </div>

      {/* Progress Dots */}
      <ProgressDots total={4} current={1} className="mb-auto pb-4" />
    </div>
  );
};

export default WelcomeScreen;
