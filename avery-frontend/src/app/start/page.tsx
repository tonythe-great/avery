'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  WelcomeScreen,
  IdentityInputScreen,
  AnalysisScreen,
  RecommendationScreen,
} from '@/components/onboarding';
import { createVeteran, getResults, VeteranInput, RoleMatch } from '@/lib/api';

type OnboardingStep = 'welcome' | 'identity' | 'analysis' | 'recommendation';

export default function StartPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<OnboardingStep>('welcome');
  const [veteranData, setVeteranData] = useState<VeteranInput | null>(null);
  const [veteranId, setVeteranId] = useState<number | null>(null);
  const [veteranName, setVeteranName] = useState<string>('');
  const [recommendation, setRecommendation] = useState<RoleMatch | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  // Handle welcome screen initialization
  const handleInitialize = useCallback(() => {
    setCurrentStep('identity');
  }, []);

  // Handle identity completion - create profile and fetch initial recommendation
  const handleIdentityComplete = useCallback(async (data: VeteranInput) => {
    setVeteranData(data);
    setVeteranName(data.name);
    setCurrentStep('analysis');
    setIsLoading(true);
    setProgress(0);
    setError(null);

    try {
      // Simulate progress while API calls happen
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 85) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + Math.random() * 15;
        });
      }, 500);

      // Create veteran profile
      const veteran = await createVeteran(data);
      setVeteranId(veteran.id);

      // Store in localStorage for assessment flow
      localStorage.setItem('veteranId', veteran.id.toString());
      localStorage.setItem('veteranName', veteran.name);

      // Fetch initial results (based on profile alone, before full assessment)
      const results = await getResults(veteran.id);

      clearInterval(progressInterval);
      setProgress(100);

      // Set the top recommendation
      if (results && results.length > 0) {
        setRecommendation(results[0]);
      }

      setIsLoading(false);
    } catch (err) {
      console.error('Error during analysis:', err);
      setError(err instanceof Error ? err.message : 'Something went wrong');
      setIsLoading(false);
      // Stay on analysis screen but show error
    }
  }, []);

  // Handle analysis complete - move to recommendation
  const handleAnalysisComplete = useCallback(() => {
    if (recommendation) {
      setCurrentStep('recommendation');
    } else if (error) {
      // If there was an error, go back to identity
      setCurrentStep('identity');
    }
  }, [recommendation, error]);

  // Handle going back from identity
  const handleBackFromIdentity = useCallback(() => {
    setCurrentStep('welcome');
  }, []);

  // Handle navigation to full assessment
  const handleStartAssessment = useCallback(() => {
    router.push('/assessment');
  }, [router]);

  // Handle viewing all roles
  const handleSeeAllRoles = useCallback(() => {
    router.push('/results');
  }, [router]);

  return (
    <main className="min-h-screen bg-avery-bg">
      {/* Background gradient overlay */}
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

      {/* Content */}
      <div className="relative z-10">
        {currentStep === 'welcome' && (
          <WelcomeScreen onInitialize={handleInitialize} />
        )}

        {currentStep === 'identity' && (
          <IdentityInputScreen
            onComplete={handleIdentityComplete}
            onBack={handleBackFromIdentity}
          />
        )}

        {currentStep === 'analysis' && (
          <AnalysisScreen
            veteranName={veteranName}
            onAnalysisComplete={handleAnalysisComplete}
            isLoading={isLoading}
            progress={progress}
          />
        )}

        {currentStep === 'recommendation' && (
          <RecommendationScreen
            veteranName={veteranName}
            recommendation={recommendation}
            onSeeAllRoles={handleSeeAllRoles}
            onStartAssessment={handleStartAssessment}
          />
        )}
      </div>

      {/* Error Toast */}
      {error && currentStep === 'analysis' && (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50">
          <div className="bg-red-500/20 border border-red-500/50 text-red-300 px-6 py-3 rounded-xl backdrop-blur-sm">
            <p className="text-sm">{error}</p>
            <button
              onClick={() => setCurrentStep('identity')}
              className="text-xs text-red-400 underline mt-1"
            >
              Try again
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
