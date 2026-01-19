'use client';

import React, { useState, useEffect } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { ProgressDots } from '@/components/ui/ProgressDots';
import { SCCTQuestion, SCCTAnswer, getSCCTQuestions, submitSCCTAssessment } from '@/lib/api';

interface SCCTQuestionScreenProps {
  veteranId: number;
  onComplete: () => void;
  onBack: () => void;
}

export const SCCTQuestionScreen: React.FC<SCCTQuestionScreenProps> = ({
  veteranId,
  onComplete,
  onBack,
}) => {
  const [questions, setQuestions] = useState<SCCTQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<number, number>>(new Map());
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await getSCCTQuestions();
      setQuestions(data);
      setIsLoading(false);
    } catch (err) {
      setError('Failed to load questions. Please try again.');
      setIsLoading(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const totalQuestions = questions.length;
  const selectedOptionId = currentQuestion ? answers.get(currentQuestion.id) : undefined;

  const handleOptionSelect = (optionId: number) => {
    if (!currentQuestion || isTransitioning) return;

    // Update answers
    setAnswers((prev) => new Map(prev).set(currentQuestion.id, optionId));

    // Auto-advance after selection with delay for visual feedback
    setTimeout(() => {
      if (currentIndex < totalQuestions - 1) {
        setIsTransitioning(true);
        setTimeout(() => {
          setCurrentIndex((prev) => prev + 1);
          setIsTransitioning(false);
        }, 300);
      } else {
        // Last question - submit
        handleSubmit(new Map(answers).set(currentQuestion.id, optionId));
      }
    }, 400);
  };

  const handleSubmit = async (finalAnswers: Map<number, number>) => {
    setIsSubmitting(true);
    try {
      const scctAnswers: SCCTAnswer[] = Array.from(finalAnswers.entries()).map(
        ([questionId, optionId]) => ({
          question_id: questionId,
          option_id: optionId,
        })
      );
      await submitSCCTAssessment(veteranId, scctAnswers);
      onComplete();
    } catch (err) {
      setError('Failed to submit assessment. Please try again.');
      setIsSubmitting(false);
    }
  };

  const handleBack = () => {
    if (currentIndex > 0) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentIndex((prev) => prev - 1);
        setIsTransitioning(false);
      }, 300);
    } else {
      onBack();
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen min-h-[100dvh] px-4">
        <AveryOrb state="processing" size="medium" />
        <p className="text-avery-text-secondary mt-6">Loading assessment...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen min-h-[100dvh] px-4">
        <AveryOrb state="dormant" size="medium" />
        <p className="text-red-400 mt-6">{error}</p>
        <button
          onClick={loadQuestions}
          className="mt-4 px-6 py-2 bg-avery-cyan/20 border border-avery-cyan rounded-xl text-avery-cyan"
        >
          Retry
        </button>
      </div>
    );
  }

  if (isSubmitting) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen min-h-[100dvh] px-4">
        <AveryOrb state="processing" size="medium" />
        <p className="text-avery-text-secondary mt-6">Analyzing your profile...</p>
      </div>
    );
  }

  if (!currentQuestion) {
    return null;
  }

  return (
    <div className="flex flex-col min-h-screen min-h-[100dvh] px-4 py-6 safe-area-inset">
      {/* Orb */}
      <div className="flex justify-center mb-4">
        <AveryOrb state="attentive" size="small" />
      </div>

      {/* SCCT Construct Badge */}
      <div className="flex justify-center mb-4">
        <span className="px-3 py-1 text-xs font-medium text-avery-purple bg-avery-purple/10 border border-avery-purple/30 rounded-full uppercase tracking-wider">
          {currentQuestion.scct_construct.replace('_', ' ')}
        </span>
      </div>

      {/* Question Card */}
      <div className="flex-1 flex flex-col max-w-md mx-auto w-full">
        <div
          className={`
            transition-all duration-300
            ${isTransitioning ? 'opacity-0 translate-x-4' : 'opacity-100 translate-x-0'}
          `}
        >
          {/* Question Text */}
          <h2 className="text-xl sm:text-2xl font-semibold text-avery-text-primary mb-6 text-center leading-relaxed">
            {currentQuestion.question_text}
          </h2>

          {/* Options */}
          <div className="space-y-3">
            {currentQuestion.options.map((option) => {
              const isSelected = selectedOptionId === option.id;
              return (
                <button
                  key={option.id}
                  onClick={() => handleOptionSelect(option.id)}
                  disabled={isTransitioning}
                  className={`
                    w-full text-left px-4 py-4 rounded-xl transition-all duration-300
                    border
                    ${
                      isSelected
                        ? 'bg-avery-cyan/20 border-avery-cyan text-avery-text-primary shadow-glow-cyan'
                        : 'bg-avery-bg-elevated border-avery-bg-hover text-avery-text-secondary hover:bg-avery-bg-hover hover:text-avery-text-primary hover:border-avery-bg-elevated'
                    }
                    ${isTransitioning ? 'pointer-events-none' : ''}
                  `}
                >
                  <div className="flex items-start gap-3">
                    <span
                      className={`
                        flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-sm font-semibold
                        ${
                          isSelected
                            ? 'bg-avery-cyan text-avery-bg'
                            : 'bg-avery-bg-hover text-avery-text-muted'
                        }
                      `}
                    >
                      {option.option_key.toUpperCase()}
                    </span>
                    <span className="pt-0.5">{option.option_text}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Back Button */}
        <button
          onClick={handleBack}
          className="mt-6 py-3 text-avery-text-muted hover:text-avery-text-secondary transition-colors"
        >
          Back
        </button>
      </div>

      {/* Progress indicators */}
      <div className="mt-auto pt-4">
        <ProgressDots total={4} current={3} className="mb-3" />

        {/* Question progress */}
        <div className="flex justify-center gap-1.5 pb-2">
          {questions.map((_, i) => (
            <div
              key={i}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                i < currentIndex
                  ? 'bg-avery-cyan'
                  : i === currentIndex
                  ? 'bg-avery-purple'
                  : 'bg-avery-bg-hover'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SCCTQuestionScreen;
