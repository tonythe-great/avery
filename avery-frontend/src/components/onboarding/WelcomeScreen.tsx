'use client';

import React, { useState, useEffect } from 'react';
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

  const handleAwakeningComplete = () => {
    setOrbState('attentive');
    setShowTitle(true);
  };

  const handleTitleComplete = () => {
    setShowSubtitle(true);
  };

  const handleSubtitleComplete = () => {
    setShowButton(true);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
      {/* Avery Orb */}
      <div className="flex-1 flex items-center justify-center">
        <AveryOrb
          state={orbState}
          size="large"
          onAwakeningComplete={handleAwakeningComplete}
        />
      </div>

      {/* Text Content */}
      <div className="text-center mb-8 min-h-[120px] flex flex-col items-center justify-center">
        {showTitle && (
          <h1 className="text-4xl font-bold text-avery-text-primary mb-4">
            <TypewriterText
              text="I am Avery."
              speed={80}
              onComplete={handleTitleComplete}
              cursor={!showSubtitle}
            />
          </h1>
        )}

        {showSubtitle && (
          <p className="text-xl text-avery-text-secondary">
            <TypewriterText
              text="Your career intelligence system."
              speed={40}
              onComplete={handleSubtitleComplete}
              cursor={!showButton}
            />
          </p>
        )}
      </div>

      {/* Initialize Button */}
      <div className={`mb-8 transition-all duration-500 ${showButton ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <GlowButton
          variant="primary"
          size="lg"
          onClick={onInitialize}
          disabled={!showButton}
        >
          Initialize
        </GlowButton>
      </div>

      {/* Progress Dots */}
      <ProgressDots total={4} current={1} className="mb-8" />
    </div>
  );
};

export default WelcomeScreen;
