'use client';

import React, { useState, useEffect, useRef } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { GlowButton } from '@/components/ui/GlowButton';
import { ProgressDots } from '@/components/ui/ProgressDots';
import { VeteranInput } from '@/lib/api';

const NAVY_RANKS = [
  'E-1 Seaman Recruit',
  'E-2 Seaman Apprentice',
  'E-3 Seaman',
  'E-4 Petty Officer Third Class',
  'E-5 Petty Officer Second Class',
  'E-6 Petty Officer First Class',
  'E-7 Chief Petty Officer',
  'E-8 Senior Chief Petty Officer',
  'E-9 Master Chief Petty Officer',
  'O-1 Ensign',
  'O-2 Lieutenant Junior Grade',
  'O-3 Lieutenant',
  'O-4 Lieutenant Commander',
  'O-5 Commander',
  'O-6 Captain',
];

const NAVY_RATES = [
  'IT - Information Systems Technician',
  'CTN - Cryptologic Technician Networks',
  'CTR - Cryptologic Technician Collection',
  'CTI - Cryptologic Technician Interpretive',
  'IS - Intelligence Specialist',
  'ET - Electronics Technician',
  'FC - Fire Controlman',
  'OS - Operations Specialist',
  'Other',
];

const SECURITY_CLEARANCES = [
  { value: 'none', label: 'No Active Clearance' },
  { value: 'secret', label: 'Secret' },
  { value: 'top_secret', label: 'Top Secret' },
  { value: 'ts_sci', label: 'TS/SCI' },
];

interface IdentityInputScreenProps {
  onComplete: (data: VeteranInput) => void;
  onBack: () => void;
}

type InputStep = 'name' | 'email' | 'rank' | 'rate' | 'clearance' | 'years';

const stepConfig = {
  name: {
    question: 'What should I call you?',
    placeholder: 'Enter your name',
    type: 'text' as const,
  },
  email: {
    question: 'Your professional email?',
    placeholder: 'you@example.com',
    type: 'email' as const,
  },
  rank: {
    question: 'Your highest rank achieved?',
    placeholder: '',
    type: 'select' as const,
  },
  rate: {
    question: 'What was your rate?',
    placeholder: '',
    type: 'rate_select' as const,
  },
  clearance: {
    question: 'Current security clearance?',
    placeholder: '',
    type: 'clearance_select' as const,
  },
  years: {
    question: 'Years of service?',
    placeholder: '',
    type: 'range' as const,
  },
};

export const IdentityInputScreen: React.FC<IdentityInputScreenProps> = ({
  onComplete,
  onBack,
}) => {
  const [currentStep, setCurrentStep] = useState<InputStep>('name');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [formData, setFormData] = useState<VeteranInput>({
    name: '',
    email: '',
    branch: 'Navy',
    rank: '',
    rating: '',
    security_clearance: '',
    years_of_service: 4,
  });
  const inputRef = useRef<HTMLInputElement>(null);

  const steps: InputStep[] = ['name', 'email', 'rank', 'rate', 'clearance', 'years'];
  const stepIndex = steps.indexOf(currentStep);

  useEffect(() => {
    // Focus input on step change
    if (inputRef.current && !isTransitioning) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [currentStep, isTransitioning]);

  const canProceed = () => {
    switch (currentStep) {
      case 'name':
        return formData.name.trim().length >= 2;
      case 'email':
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email);
      case 'rank':
        return formData.rank.length > 0;
      case 'rate':
        return (formData.rating?.length ?? 0) > 0;
      case 'clearance':
        return (formData.security_clearance?.length ?? 0) > 0;
      case 'years':
        return formData.years_of_service > 0;
      default:
        return false;
    }
  };

  const handleNext = () => {
    if (!canProceed()) return;

    const nextStepIndex = stepIndex + 1;
    if (nextStepIndex < steps.length) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentStep(steps[nextStepIndex]);
        setIsTransitioning(false);
      }, 300);
    } else {
      onComplete(formData);
    }
  };

  const handlePrevious = () => {
    if (stepIndex > 0) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentStep(steps[stepIndex - 1]);
        setIsTransitioning(false);
      }, 300);
    } else {
      onBack();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && canProceed()) {
      handleNext();
    }
  };

  const renderInput = () => {
    const config = stepConfig[currentStep];

    switch (config.type) {
      case 'text':
      case 'email':
        return (
          <input
            ref={inputRef}
            type={config.type}
            value={currentStep === 'name' ? formData.name : formData.email}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                [currentStep]: e.target.value,
              }))
            }
            onKeyDown={handleKeyDown}
            placeholder={config.placeholder}
            className="w-full bg-transparent border-b-2 border-avery-bg-hover focus:border-avery-cyan
                       text-2xl text-avery-text-primary placeholder:text-avery-text-muted
                       py-3 px-1 outline-none transition-colors duration-300"
            autoComplete="off"
          />
        );

      case 'select':
        return (
          <div className="space-y-2 max-h-[40vh] overflow-y-auto pr-2 custom-scrollbar">
            {NAVY_RANKS.map((rank) => (
              <button
                key={rank}
                onClick={() => {
                  setFormData((prev) => ({ ...prev, rank }));
                }}
                className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-300 ${
                  formData.rank === rank
                    ? 'bg-avery-cyan/20 border border-avery-cyan text-avery-text-primary shadow-glow-cyan'
                    : 'bg-avery-bg-elevated border border-transparent text-avery-text-secondary hover:bg-avery-bg-hover hover:text-avery-text-primary'
                }`}
              >
                {rank}
              </button>
            ))}
          </div>
        );

      case 'rate_select':
        return (
          <div className="space-y-2 max-h-[40vh] overflow-y-auto pr-2 custom-scrollbar">
            {NAVY_RATES.map((rate) => (
              <button
                key={rate}
                onClick={() => {
                  setFormData((prev) => ({ ...prev, rating: rate }));
                }}
                className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-300 ${
                  formData.rating === rate
                    ? 'bg-avery-cyan/20 border border-avery-cyan text-avery-text-primary shadow-glow-cyan'
                    : 'bg-avery-bg-elevated border border-transparent text-avery-text-secondary hover:bg-avery-bg-hover hover:text-avery-text-primary'
                }`}
              >
                {rate}
              </button>
            ))}
          </div>
        );

      case 'clearance_select':
        return (
          <div className="space-y-2 max-h-[40vh] overflow-y-auto pr-2 custom-scrollbar">
            {SECURITY_CLEARANCES.map((clearance) => (
              <button
                key={clearance.value}
                onClick={() => {
                  setFormData((prev) => ({ ...prev, security_clearance: clearance.value }));
                }}
                className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-300 ${
                  formData.security_clearance === clearance.value
                    ? 'bg-avery-cyan/20 border border-avery-cyan text-avery-text-primary shadow-glow-cyan'
                    : 'bg-avery-bg-elevated border border-transparent text-avery-text-secondary hover:bg-avery-bg-hover hover:text-avery-text-primary'
                }`}
              >
                {clearance.label}
              </button>
            ))}
          </div>
        );

      case 'range':
        return (
          <div className="w-full">
            <div className="text-center mb-8">
              <span className="text-6xl font-bold text-avery-cyan">
                {formData.years_of_service}
              </span>
              <span className="text-2xl text-avery-text-muted ml-3">years</span>
            </div>

            <input
              type="range"
              min="1"
              max="40"
              value={formData.years_of_service}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  years_of_service: parseInt(e.target.value),
                }))
              }
              className="w-full h-2 bg-avery-bg-hover rounded-full appearance-none cursor-pointer
                         [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-6
                         [&::-webkit-slider-thumb]:h-6 [&::-webkit-slider-thumb]:rounded-full
                         [&::-webkit-slider-thumb]:bg-avery-cyan [&::-webkit-slider-thumb]:shadow-glow-cyan
                         [&::-webkit-slider-thumb]:cursor-pointer [&::-webkit-slider-thumb]:transition-transform
                         [&::-webkit-slider-thumb]:hover:scale-110"
            />

            <div className="flex justify-between text-sm text-avery-text-muted mt-3">
              <span>1 year</span>
              <span>40 years</span>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="flex flex-col min-h-screen min-h-[100dvh] px-4 py-6 safe-area-inset">
      {/* Orb - smaller on mobile */}
      <div className="flex justify-center mb-4">
        <AveryOrb state="attentive" size="small" />
      </div>

      {/* Question Card */}
      <div className="flex-1 flex flex-col max-w-md mx-auto w-full">
        <div
          className={`
            bg-avery-bg-elevated/50 backdrop-blur-sm rounded-2xl p-4 sm:p-6
            border border-avery-bg-hover shadow-lg
            transition-all duration-300
            ${isTransitioning ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'}
          `}
        >
          {/* Question */}
          <h2 className="text-xl sm:text-2xl font-semibold text-avery-text-primary mb-6 text-center">
            {stepConfig[currentStep].question}
          </h2>

          {/* Input Area */}
          <div className="min-h-[180px]">{renderInput()}</div>
        </div>

        {/* Navigation Buttons */}
        <div className="flex gap-3 mt-6">
          <GlowButton variant="ghost" size="md" onClick={handlePrevious} className="flex-1">
            Back
          </GlowButton>

          <GlowButton
            variant="primary"
            size="md"
            onClick={handleNext}
            disabled={!canProceed()}
            className="flex-1"
          >
            {stepIndex === steps.length - 1 ? 'Analyze' : 'Continue'}
          </GlowButton>
        </div>
      </div>

      {/* Progress indicators */}
      <div className="mt-auto pt-4">
        <ProgressDots total={4} current={2} className="mb-3" />

        {/* Sub-progress for identity steps */}
        <div className="flex justify-center gap-2 pb-2">
          {steps.map((step, i) => (
            <div
              key={step}
              className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                i <= stepIndex ? 'bg-avery-purple' : 'bg-avery-bg-hover'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default IdentityInputScreen;
