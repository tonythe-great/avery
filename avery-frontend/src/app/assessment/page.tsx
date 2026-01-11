"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getQuestions, submitAssessment, Question, Answer } from "@/lib/api";

const ANSWER_OPTIONS = [
  { value: 1, label: "Strongly Disagree", emoji: "😕" },
  { value: 2, label: "Disagree", emoji: "🙁" },
  { value: 3, label: "Neutral", emoji: "😐" },
  { value: 4, label: "Agree", emoji: "🙂" },
  { value: 5, label: "Strongly Agree", emoji: "😄" },
];

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

  useEffect(() => {
    // Get veteran ID from localStorage
    const storedId = localStorage.getItem("veteranId");
    const storedName = localStorage.getItem("veteranName");
    
    if (!storedId) {
      router.push("/onboarding");
      return;
    }
    
    setVeteranId(parseInt(storedId));
    setVeteranName(storedName || "");
    
    // Load questions
    loadQuestions();
  }, [router]);

  const loadQuestions = async () => {
    try {
      const data = await getQuestions();
      setQuestions(data);
    } catch (err) {
      setError("Failed to load questions. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswer = (value: number) => {
    const question = questions[currentIndex];
    setAnswers((prev) => new Map(prev).set(question.id, value));
    
    // Auto-advance after a short delay
    setTimeout(() => {
      if (currentIndex < questions.length - 1) {
        setCurrentIndex(currentIndex + 1);
      }
    }, 300);
  };

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
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progress = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;
  const allAnswered = questions.length > 0 && answers.size === questions.length;

  if (isLoading) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-gold-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-navy-400">Loading assessment...</p>
        </div>
      </main>
    );
  }

  if (error && questions.length === 0) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2">Connection Error</h2>
          <p className="text-navy-400 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-navy-700 rounded-xl text-white"
          >
            Try Again
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white px-6 py-8">
      {/* Header */}
      <div className="max-w-sm mx-auto mb-6">
        <p className="text-navy-400 text-sm mb-1">
          {veteranName ? `Hey ${veteranName.split(" ")[0]}!` : "Personality Assessment"}
        </p>
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-bold">Question {currentIndex + 1} of {questions.length}</h1>
          <span className="text-gold-400 font-medium">{Math.round(progress)}%</span>
        </div>
        
        {/* Progress bar */}
        <div className="h-2 bg-navy-700 rounded-full overflow-hidden mt-3">
          <div
            className="h-full bg-gradient-to-r from-gold-400 to-gold-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      {currentQuestion && (
        <div className="max-w-sm mx-auto">
          <div
            key={currentQuestion.id}
            className="bg-navy-800/50 backdrop-blur rounded-2xl p-6 mb-8 animate-slide-up"
          >
            <div className="text-xs text-gold-400 uppercase tracking-wide mb-3">
              {currentQuestion.trait.replace("_", " ")}
            </div>
            <p className="text-lg leading-relaxed">
              {currentQuestion.text}
            </p>
          </div>

          {/* Answer Options */}
          <div className="space-y-3">
            {ANSWER_OPTIONS.map((option) => {
              const isSelected = answers.get(currentQuestion.id) === option.value;
              return (
                <button
                  key={option.value}
                  onClick={() => handleAnswer(option.value)}
                  className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all active:scale-[0.98] ${
                    isSelected
                      ? "bg-gold-500 text-navy-900"
                      : "bg-navy-800 hover:bg-navy-700"
                  }`}
                >
                  <span className="text-2xl">{option.emoji}</span>
                  <span className={`font-medium ${isSelected ? "text-navy-900" : "text-white"}`}>
                    {option.label}
                  </span>
                  {isSelected && (
                    <svg className="w-5 h-5 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              );
            })}
          </div>

          {/* Navigation */}
          <div className="flex gap-4 mt-8">
            {currentIndex > 0 && (
              <button
                onClick={() => setCurrentIndex(currentIndex - 1)}
                className="flex-1 py-4 rounded-xl border border-navy-600 text-navy-300 font-medium active:scale-[0.98] transition-transform"
              >
                Previous
              </button>
            )}
            
            {currentIndex < questions.length - 1 ? (
              <button
                onClick={() => setCurrentIndex(currentIndex + 1)}
                disabled={!answers.has(currentQuestion.id)}
                className="flex-1 py-4 rounded-xl bg-navy-700 text-white font-medium disabled:opacity-50 active:scale-[0.98] transition-transform"
              >
                Next
              </button>
            ) : allAnswered ? (
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="flex-1 py-4 rounded-xl bg-gradient-to-r from-gold-400 to-gold-500 text-navy-900 font-semibold disabled:opacity-50 active:scale-[0.98] transition-transform"
              >
                {isSubmitting ? "Submitting..." : "See My Results"}
              </button>
            ) : null}
          </div>

          {/* Error message */}
          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-300 text-sm">
              {error}
            </div>
          )}

          {/* Question dots */}
          <div className="flex justify-center gap-1.5 mt-8 flex-wrap">
            {questions.map((q, i) => (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(i)}
                className={`w-2.5 h-2.5 rounded-full transition-all ${
                  i === currentIndex
                    ? "bg-gold-400 scale-125"
                    : answers.has(q.id)
                    ? "bg-gold-400/50"
                    : "bg-navy-600"
                }`}
              />
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
