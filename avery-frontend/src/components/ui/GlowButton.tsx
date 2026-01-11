'use client';

import React from 'react';

interface GlowButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  loading?: boolean;
}

export const GlowButton: React.FC<GlowButtonProps> = ({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'md',
  className = '',
  loading = false,
}) => {
  const baseStyles = `
    relative font-medium rounded-xl transition-all duration-300
    active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50
    focus:outline-none focus:ring-2 focus:ring-avery-cyan/50
  `;

  const sizeStyles = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  const variantStyles = {
    primary: `
      bg-gradient-to-r from-avery-cyan to-avery-teal text-black font-semibold
      shadow-glow-cyan hover:shadow-[0_0_30px_rgba(0,212,255,0.5)]
      disabled:shadow-none
    `,
    secondary: `
      bg-avery-bg-elevated border border-avery-cyan/30 text-avery-text-primary
      hover:border-avery-cyan/60 hover:shadow-glow-cyan
      disabled:border-avery-bg-hover disabled:shadow-none
    `,
    ghost: `
      bg-transparent border border-avery-bg-hover text-avery-text-secondary
      hover:text-avery-text-primary hover:border-avery-text-muted
    `,
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
    >
      {loading ? (
        <span className="flex items-center justify-center gap-2">
          <svg
            className="animate-spin h-5 w-5"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Processing...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};

export default GlowButton;
