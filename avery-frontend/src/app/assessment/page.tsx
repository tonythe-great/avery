"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getQuestions, submitAssessment, Question, Answer } from "@/lib/api";
import { AveryOrb } from "@/components/AveryOrb";
import { GlowButton } from "@/components/ui/GlowButton";

// Avery-style answer options (no emojis - premium feel)
const ANSWER_OPTIONS = [
  { value: 1, label: "Strongly Disagree", intensity: 0.2 },
  { value: 2, label: "Disagree", intensity: 0.4 },
  { value: 3, label: "Neutral", intensity: 0.6 },
  { value: 4, label: "Agree", intensity: 0.8 },
  { value: 5, label: "Strongly Agree", intensity: 1.0 },
];

// Trait display names
const TRAIT_LABELS: Record<string, string> = {
  openness: "Openness",
  conscientiousness: "Conscientiousness",
  extraversion: "Extraversion",
  agreeableness: "Agreeableness",
  stability: "Emotional Stability",
  neuroticism: "Stress Response",
};

export default function AssessmentPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<number, number>>(new Map());
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [veteranId, setVeteranId] = useState<number | null>(null);
  const [veteranName, setVeteranName] = useState("");
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const storedId = localStorage.getItem("veteranId");
    const storedName = localStorage.getItem("veteranName");

    if (!storedId) {
      router.push("/start");
      return;
    }

    setVeteranId(parseInt(storedId));
    setVeteranName(storedName || "");
    loadQuestions();
  }, [router]);

  const loadQuestions = async () => {
    try {
      const data = await getQuestions();
      setQuestions(data);
    } catch (err) {
      setError("Failed to load questions. Please check your connection.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswer = useCallback((value: number) => {
    const question = questions[currentIndex];
    setAnswers((prev) => new Map(prev).set(question.id, value));

    // Auto-advance with transition
    setTimeout(() => {
      if (currentIndex < questions.length - 1) {
        setIsTransitioning(true);
        setTimeout(() => {
          setCurrentIndex(currentIndex + 1);
          setIsTransitioning(false);
        }, 200);
      }
    }, 400);
  }, [currentIndex, questions]);

  const handlePrevious = useCallback(() => {
    if (currentIndex > 0) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentIndex(currentIndex - 1);
        setIsTransitioning(false);
      }, 200);
    }
  }, [currentIndex]);

  const handleNext = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentIndex(currentIndex + 1);
        setIsTransitioning(false);
      }, 200);
    }
  }, [currentIndex, questions.length]);

  const handleSubmit = async () => {
    if (!veteranId) return;

    setIsSubmitting(true);
    setError("");

    try {
      const answerArray: Answer[] = Array.from(answers.entries()).map(
        ([question_id, answer_value]) => ({ question_id, answer_value })
      );

      await submitAssessment(veteranId, answerArray);
      router.push("/results");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit assessment");
      setIsSubmitting(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progress = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;
  const answeredCount = answers.size;
  const allAnswered = questions.length > 0 && answeredCount === questions.length;

  // Loading state with Avery orb
  if (isLoading) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center relative">
        <BackgroundGradient />
        <div className="relative z-10 text-center">
          <AveryOrb state="processing" size="medium" />
          <p className="text-avery-text-secondary mt-6">Loading assessment...</p>
        </div>
      </main>
    );
  }

  // Error state
  if (error && questions.length === 0) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center px-6 relative">
        <BackgroundGradient />
        <div className="relative z-10 text-center max-w-sm">
          <AveryOrb state="dormant" size="medium" />
          <h2 className="text-xl font-bold text-avery-text-primary mt-6 mb-2">Connection Error</h2>
          <p className="text-avery-text-secondary mb-6">{error}</p>
          <GlowButton variant="secondary" onClick={() => window.location.reload()}>
            Try Again
          </GlowButton>
        </div>
      </main>
    );
  }

  // Submitting state
  if (isSubmitting) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center relative">
        <BackgroundGradient />
        <div className="relative z-10 text-center">
          <AveryOrb state="processing" size="large" />
          <p className="text-avery-text-secondary mt-8 text-lg">
            Analyzing your responses...
          </p>
          <p className="text-avery-cyan mt-2">
            Generating career intelligence
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-avery-bg text-white relative">
      <BackgroundGradient />

      <div className="relative z-10 min-h-screen flex flex-col px-6 py-6 safe-area-inset">
        {/* Header with Orb */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-avery-text-muted text-sm">
              {veteranName ? `${veteranName.split(" ")[0]}'s Assessment` : "Assessment"}
            </p>
            <div className="flex items-baseline gap-3 mt-1">
              <h1 className="text-lg font-semibold text-avery-text-primary">
                Question {currentIndex + 1}
                <span className="text-avery-text-muted font-normal"> / {questions.length}</span>
              </h1>
            </div>
          </div>
          <AveryOrb state="attentive" size="small" />
        </div>

        {/* Progress bar */}
        <div className="mb-6">
          <div className="h-1 bg-avery-bg-elevated rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-avery-cyan via-avery-purple to-avery-teal transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="flex justify-between mt-2 text-xs text-avery-text-muted">
            <span>{answeredCount} answered</span>
            <span>{Math.round(progress)}% complete</span>
          </div>
        </div>

        {/* Question Card */}
        {currentQuestion && (
          <div className="flex-1 flex flex-col max-w-lg mx-auto w-full">
            <div
              className={`
                bg-avery-bg-elevated/60 backdrop-blur-sm rounded-2xl p-6 mb-6
                border border-avery-bg-hover
                transition-all duration-200
                ${isTransitioning ? "opacity-0 translate-x-4" : "opacity-100 translate-x-0"}
              `}
            >
              {/* Trait Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-avery-purple/20 rounded-full mb-4">
                <div className="w-2 h-2 rounded-full bg-avery-purple" />
                <span className="text-xs text-avery-purple font-medium uppercase tracking-wider">
                  {TRAIT_LABELS[currentQuestion.trait] || currentQuestion.trait}
                </span>
              </div>

              {/* Question Text */}
              <p className="text-xl text-avery-text-primary leading-relaxed">
                {currentQuestion.text}
              </p>
            </div>

            {/* Answer Options */}
            <div className="space-y-3 mb-6">
              {ANSWER_OPTIONS.map((option) => {
                const isSelected = answers.get(currentQuestion.id) === option.value;
                return (
                  <button
                    key={option.value}
                    onClick={() => handleAnswer(option.value)}
                    className={`
                      w-full flex items-center justify-between p-4 rounded-xl
                      transition-all duration-300 active:scale-[0.98]
                      ${isSelected
                        ? "bg-avery-cyan/20 border-2 border-avery-cyan shadow-glow-cyan"
                        : "bg-avery-bg-elevated border-2 border-transparent hover:border-avery-bg-hover"
                      }
                    `}
                  >
                    <div className="flex items-center gap-4">
                      {/* Intensity indicator */}
                      <div className="flex gap-1">
                        {[1, 2, 3, 4, 5].map((bar) => (
                          <div
                            key={bar}
                            className={`w-1 h-4 rounded-full transition-colors ${
                              bar <= option.value
                                ? isSelected
                                  ? "bg-avery-cyan"
                                  : "bg-avery-text-muted"
                                : "bg-avery-bg-hover"
                            }`}
                          />
                        ))}
                      </div>
                      <span
                        className={`font-medium ${
                          isSelected ? "text-avery-cyan" : "text-avery-text-secondary"
                        }`}
                      >
                        {option.label}
                      </span>
                    </div>

                    {/* Selection indicator */}
                    <div
                      className={`
                        w-6 h-6 rounded-full border-2 flex items-center justify-center
                        transition-all duration-300
                        ${isSelected
                          ? "border-avery-cyan bg-avery-cyan"
                          : "border-avery-bg-hover"
                        }
                      `}
                    >
                      {isSelected && (
                        <svg className="w-4 h-4 text-black" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Navigation */}
            <div className="flex gap-3 mt-auto">
              {currentIndex > 0 && (
                <GlowButton variant="ghost" onClick={handlePrevious} className="flex-1">
                  Previous
                </GlowButton>
              )}

              {currentIndex < questions.length - 1 ? (
                <GlowButton
                  variant="secondary"
                  onClick={handleNext}
                  disabled={!answers.has(currentQuestion.id)}
                  className="flex-1"
                >
                  Next
                </GlowButton>
              ) : allAnswered ? (
                <GlowButton variant="primary" onClick={handleSubmit} className="flex-1">
                  Generate Results
                </GlowButton>
              ) : (
                <GlowButton variant="secondary" disabled className="flex-1">
                  {questions.length - answeredCount} remaining
                </GlowButton>
              )}
            </div>

            {/* Error message */}
            {error && (
              <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm">
                {error}
              </div>
            )}

            {/* Question dots navigation */}
            <div className="flex justify-center gap-1 mt-6 flex-wrap">
              {questions.map((q, i) => (
                <button
                  key={q.id}
                  onClick={() => {
                    setIsTransitioning(true);
                    setTimeout(() => {
                      setCurrentIndex(i);
                      setIsTransitioning(false);
                    }, 200);
                  }}
                  className="p-2 -m-1"
                  aria-label={`Go to question ${i + 1}`}
                >
                  <div
                    className={`
                      h-2 rounded-full transition-all duration-300
                      ${i === currentIndex
                        ? "w-6 bg-avery-cyan shadow-glow-cyan"
                        : answers.has(q.id)
                          ? "w-2 bg-avery-cyan/50"
                          : "w-2 bg-avery-bg-hover"
                      }
                    `}
                  />
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

// Background gradient component
function BackgroundGradient() {
  return (
    <div
      className="fixed inset-0 pointer-events-none"
      style={{
        background: `
          radial-gradient(ellipse at 50% 0%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
          radial-gradient(ellipse at 80% 80%, rgba(124, 58, 237, 0.06) 0%, transparent 40%),
          radial-gradient(ellipse at 20% 90%, rgba(6, 182, 212, 0.05) 0%, transparent 40%)
        `,
      }}
    />
  );
}
