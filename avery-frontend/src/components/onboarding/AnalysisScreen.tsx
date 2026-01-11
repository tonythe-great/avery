'use client';

import React, { useState, useEffect } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { ProgressDots } from '@/components/ui/ProgressDots';

const STATUS_MESSAGES = [
  'Analyzing your experience...',
  'Cross-referencing 847 cybersecurity roles',
  'Mapping skill transferability...',
  'Calculating salary potential...',
  'Identifying optimal career paths...',
  'Generating recommendations...',
];

interface AnalysisScreenProps {
  veteranName: string;
  onAnalysisComplete: () => void;
  isLoading: boolean;
  progress: number;
}

export const AnalysisScreen: React.FC<AnalysisScreenProps> = ({
  veteranName,
  onAnalysisComplete,
  isLoading,
  progress,
}) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [displayProgress, setDisplayProgress] = useState(0);

  // Rotate status messages
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMessageIndex((prev) => (prev + 1) % STATUS_MESSAGES.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Smooth progress animation
  useEffect(() => {
    const targetProgress = isLoading ? Math.min(progress, 90) : 100;

    if (displayProgress < targetProgress) {
      const timer = setTimeout(() => {
        setDisplayProgress((prev) => Math.min(prev + 1, targetProgress));
      }, 30);
      return () => clearTimeout(timer);
    }

    // When progress hits 100 and loading is done, trigger completion
    if (displayProgress >= 100 && !isLoading) {
      const completeTimer = setTimeout(() => {
        onAnalysisComplete();
      }, 500);
      return () => clearTimeout(completeTimer);
    }
  }, [displayProgress, progress, isLoading, onAnalysisComplete]);

  return (
    <div className="flex flex-col items-center min-h-screen min-h-[100dvh] px-4 py-6 safe-area-inset">
      {/* Avery Orb - Processing State */}
      <div className="flex-shrink-0 mt-auto mb-6">
        <AveryOrb state="processing" size="medium" />
      </div>

      {/* Status Text */}
      <div className="text-center mb-6 min-h-[80px]">
        <p className="text-base sm:text-lg text-avery-text-secondary mb-2">
          {veteranName ? `Analyzing ${veteranName}'s profile...` : 'Initializing analysis...'}
        </p>

        <p
          className="text-avery-cyan font-medium transition-opacity duration-300 text-sm sm:text-base"
          key={currentMessageIndex}
        >
          {STATUS_MESSAGES[currentMessageIndex]}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="w-full max-w-sm mb-6">
        <div className="flex justify-between text-sm text-avery-text-muted mb-2">
          <span>Processing</span>
          <span>{Math.round(displayProgress)}%</span>
        </div>

        <div className="h-2 bg-avery-bg-elevated rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-avery-cyan via-avery-purple to-avery-teal
                       transition-all duration-100 ease-out rounded-full
                       shadow-[0_0_10px_rgba(0,212,255,0.5)]"
            style={{ width: `${displayProgress}%` }}
          />
        </div>
      </div>

      {/* Progress Dots */}
      <ProgressDots total={4} current={3} className="mb-auto pb-4" />
    </div>
  );
};

export default AnalysisScreen;
