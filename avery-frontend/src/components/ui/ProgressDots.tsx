'use client';

import React from 'react';

interface ProgressDotsProps {
  total: number;
  current: number;
  className?: string;
}

export const ProgressDots: React.FC<ProgressDotsProps> = ({
  total,
  current,
  className = '',
}) => {
  return (
    <div className={`flex items-center justify-center gap-3 ${className}`}>
      {Array.from({ length: total }, (_, i) => {
        const isActive = i + 1 === current;
        const isCompleted = i + 1 < current;

        return (
          <div
            key={i}
            className={`
              transition-all duration-300 rounded-full
              ${isActive
                ? 'w-8 h-2 bg-avery-cyan shadow-glow-cyan'
                : isCompleted
                  ? 'w-2 h-2 bg-avery-cyan/60'
                  : 'w-2 h-2 bg-avery-bg-hover'
              }
            `}
          />
        );
      })}
    </div>
  );
};

export default ProgressDots;
