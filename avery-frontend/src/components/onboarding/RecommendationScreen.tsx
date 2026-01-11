'use client';

import React, { useState, useEffect } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { GlowButton } from '@/components/ui/GlowButton';
import { ProgressDots } from '@/components/ui/ProgressDots';
import { TypewriterText } from '@/components/ui/TypewriterText';
import { RoleMatch } from '@/lib/api';

interface RecommendationScreenProps {
  veteranName: string;
  recommendation: RoleMatch | null;
  onSeeAllRoles: () => void;
  onStartAssessment: () => void;
}

// Salary estimates by role (simplified mapping)
const SALARY_RANGES: Record<string, { min: number; max: number }> = {
  'SOC Analyst': { min: 65000, max: 95000 },
  'Penetration Tester': { min: 85000, max: 140000 },
  'Incident Response Specialist': { min: 80000, max: 130000 },
  'Security Engineer': { min: 95000, max: 155000 },
  'Cybersecurity Consultant': { min: 90000, max: 160000 },
  'Threat Intelligence Analyst': { min: 85000, max: 135000 },
  'Security Awareness Training Specialist': { min: 70000, max: 110000 },
  'Chief Information Security Officer': { min: 180000, max: 350000 },
  'Digital Forensics Investigator': { min: 75000, max: 125000 },
  'Cloud Security Architect': { min: 140000, max: 220000 },
};

const formatSalary = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(amount);
};

const ConfidenceRing: React.FC<{ percentage: number; size?: number }> = ({
  percentage,
  size = 100,
}) => {
  const [animatedPercentage, setAnimatedPercentage] = useState(0);
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedPercentage / 100) * circumference;

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedPercentage(percentage);
    }, 300);
    return () => clearTimeout(timer);
  }, [percentage]);

  const getColor = () => {
    if (percentage >= 80) return '#10b981'; // green
    if (percentage >= 60) return '#f59e0b'; // yellow
    return '#f97316'; // orange
  };

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={getColor()}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{
            transition: 'stroke-dashoffset 1s ease-out',
            filter: `drop-shadow(0 0 6px ${getColor()})`,
          }}
        />
      </svg>
      {/* Percentage text */}
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-avery-text-primary">
          {Math.round(animatedPercentage)}%
        </span>
      </div>
    </div>
  );
};

export const RecommendationScreen: React.FC<RecommendationScreenProps> = ({
  veteranName,
  recommendation,
  onSeeAllRoles,
  onStartAssessment,
}) => {
  const [showCard, setShowCard] = useState(false);
  const [showIntro, setShowIntro] = useState(true);

  useEffect(() => {
    // Show intro text, then reveal card
    const cardTimer = setTimeout(() => {
      setShowCard(true);
    }, 2000);

    return () => clearTimeout(cardTimer);
  }, []);

  if (!recommendation) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
        <AveryOrb state="attentive" size="medium" />
        <p className="text-avery-text-secondary mt-8">Loading recommendation...</p>
      </div>
    );
  }

  const roleName = recommendation.role.name;
  const salaryRange = SALARY_RANGES[roleName] || { min: 70000, max: 120000 };

  return (
    <div className="flex flex-col min-h-screen px-6 py-8">
      {/* Orb - small, top corner */}
      <div className="flex justify-start mb-4">
        <AveryOrb state="presenting" size="small" />
      </div>

      {/* Intro Text */}
      {showIntro && (
        <div className="mb-6">
          <p className="text-lg text-avery-text-secondary">
            <TypewriterText
              text={`${veteranName}, based on your profile, I've identified your optimal career path.`}
              speed={30}
              cursor={false}
            />
          </p>
        </div>
      )}

      {/* Result Card */}
      <div
        className={`
          flex-1 transition-all duration-700 ease-out
          ${showCard ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}
        `}
      >
        <div
          className="bg-avery-bg-elevated/80 backdrop-blur-sm rounded-2xl p-6
                     border border-avery-cyan/20 shadow-lg relative overflow-hidden"
        >
          {/* Gradient border effect */}
          <div
            className="absolute inset-0 rounded-2xl opacity-30"
            style={{
              background: 'linear-gradient(135deg, rgba(0,212,255,0.2) 0%, rgba(124,58,237,0.2) 50%, rgba(6,182,212,0.2) 100%)',
              padding: '1px',
            }}
          />

          {/* Rank Badge */}
          <div className="flex items-center gap-2 mb-4">
            <span className="px-3 py-1 bg-avery-cyan/20 text-avery-cyan text-xs font-bold rounded-full uppercase tracking-wider">
              #1 Match
            </span>
          </div>

          {/* Role Title */}
          <h2 className="text-3xl font-bold text-avery-text-primary mb-6">
            {roleName}
          </h2>

          {/* Confidence & Salary Row */}
          <div className="flex items-center gap-6 mb-6">
            {/* Confidence Ring */}
            <div className="flex flex-col items-center">
              <ConfidenceRing percentage={recommendation.match_percentage} />
              <span className="text-xs text-avery-text-muted mt-2 uppercase tracking-wider">
                Confidence
              </span>
            </div>

            {/* Salary Range */}
            <div className="flex-1">
              <p className="text-2xl font-semibold text-avery-text-primary">
                {formatSalary(salaryRange.min)} — {formatSalary(salaryRange.max)}
              </p>
              <p className="text-sm text-avery-text-muted">median salary range</p>
            </div>
          </div>

          {/* Match Reasons */}
          <div className="border-t border-avery-bg-hover pt-4">
            <h3 className="text-sm font-semibold text-avery-text-muted uppercase tracking-wider mb-3">
              Why This Fits
            </h3>
            <ul className="space-y-2">
              {recommendation.match_reasons.slice(0, 3).map((reason, index) => (
                <li key={index} className="flex items-start gap-2 text-avery-text-secondary">
                  <span className="text-avery-cyan mt-0.5">&#10003;</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Role Description */}
        <div className="mt-4 p-4 bg-avery-bg-subtle rounded-xl">
          <p className="text-sm text-avery-text-muted leading-relaxed">
            {recommendation.role.description}
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div
        className={`
          space-y-3 mt-6 transition-all duration-500 delay-500
          ${showCard ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}
        `}
      >
        <GlowButton
          variant="primary"
          size="lg"
          onClick={onStartAssessment}
          className="w-full"
        >
          Take Full Assessment
        </GlowButton>

        <GlowButton
          variant="secondary"
          size="md"
          onClick={onSeeAllRoles}
          className="w-full"
        >
          See All Matching Roles
        </GlowButton>
      </div>

      {/* Progress Dots */}
      <ProgressDots total={4} current={4} className="mt-6 mb-4" />
    </div>
  );
};

export default RecommendationScreen;
