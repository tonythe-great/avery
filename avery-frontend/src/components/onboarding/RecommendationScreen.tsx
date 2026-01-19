'use client';

import React, { useState, useEffect } from 'react';
import { AveryOrb } from '@/components/AveryOrb';
import { GlowButton } from '@/components/ui/GlowButton';
import { ProgressDots } from '@/components/ui/ProgressDots';
import { TypewriterText } from '@/components/ui/TypewriterText';
import { LLMResultsResponse, LLMRecommendation } from '@/lib/api';

interface RecommendationScreenProps {
  veteranName: string;
  llmResults: LLMResultsResponse | null;
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
  const strokeWidth = 6;
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
        <span className="text-lg font-bold text-avery-text-primary">
          {Math.round(animatedPercentage)}%
        </span>
      </div>
    </div>
  );
};

const RecommendationCard: React.FC<{
  recommendation: LLMRecommendation;
  rank: number;
  isExpanded: boolean;
  onToggle: () => void;
}> = ({ recommendation, rank, isExpanded, onToggle }) => {
  const salaryRange = SALARY_RANGES[recommendation.role_name] || { min: 70000, max: 120000 };

  return (
    <div
      className={`
        bg-avery-bg-elevated/80 backdrop-blur-sm rounded-2xl p-4
        border transition-all duration-300 cursor-pointer
        ${rank === 1 ? 'border-avery-cyan/40' : 'border-avery-bg-hover'}
      `}
      onClick={onToggle}
    >
      {/* Header Row */}
      <div className="flex items-center gap-3 mb-3">
        {/* Rank Badge */}
        <span
          className={`
            px-2 py-0.5 text-xs font-bold rounded-full uppercase tracking-wider
            ${rank === 1 ? 'bg-avery-cyan/20 text-avery-cyan' : 'bg-avery-bg-hover text-avery-text-muted'}
          `}
        >
          #{rank}
        </span>

        {/* Role Name */}
        <h3 className="text-lg font-semibold text-avery-text-primary flex-1 truncate">
          {recommendation.role_name}
        </h3>

        {/* Match Score Ring */}
        <ConfidenceRing percentage={recommendation.match_score} size={50} />
      </div>

      {/* Primary Reason */}
      <p className="text-sm text-avery-text-secondary mb-3">
        {recommendation.primary_reason}
      </p>

      {/* Expandable Content */}
      <div
        className={`
          overflow-hidden transition-all duration-300
          ${isExpanded ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}
        `}
      >
        {/* Salary Range */}
        <div className="mb-3">
          <p className="text-sm text-avery-text-muted mb-1">Salary Range</p>
          <p className="text-base font-semibold text-avery-text-primary">
            {formatSalary(salaryRange.min)} — {formatSalary(salaryRange.max)}
          </p>
        </div>

        {/* Fit Factors */}
        {recommendation.fit_factors.length > 0 && (
          <div className="mb-3">
            <p className="text-xs font-semibold text-avery-text-muted uppercase tracking-wider mb-2">
              Why You Fit
            </p>
            <ul className="space-y-1">
              {recommendation.fit_factors.map((factor, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-avery-text-secondary">
                  <span className="text-avery-cyan mt-0.5 flex-shrink-0">&#10003;</span>
                  <span>{factor}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Concerns */}
        {recommendation.concerns.length > 0 && (
          <div className="mb-3">
            <p className="text-xs font-semibold text-avery-text-muted uppercase tracking-wider mb-2">
              Considerations
            </p>
            <ul className="space-y-1">
              {recommendation.concerns.map((concern, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-avery-text-secondary">
                  <span className="text-amber-500 mt-0.5 flex-shrink-0">!</span>
                  <span>{concern}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Avery Quote */}
        {recommendation.avery_quote && (
          <div className="pt-3 border-t border-avery-bg-hover">
            <p className="text-sm italic text-avery-text-muted">
              &ldquo;{recommendation.avery_quote}&rdquo;
            </p>
          </div>
        )}
      </div>

      {/* Expand/Collapse Indicator */}
      <div className="flex justify-center mt-2">
        <span
          className={`
            text-avery-text-muted text-xs transition-transform duration-300
            ${isExpanded ? 'rotate-180' : ''}
          `}
        >
          &#9660;
        </span>
      </div>
    </div>
  );
};

export const RecommendationScreen: React.FC<RecommendationScreenProps> = ({
  veteranName,
  llmResults,
  onSeeAllRoles,
  onStartAssessment,
}) => {
  const [showCards, setShowCards] = useState(false);
  const [expandedIndex, setExpandedIndex] = useState<number>(0);

  useEffect(() => {
    // Show cards after intro text
    const cardTimer = setTimeout(() => {
      setShowCards(true);
    }, 2000);

    return () => clearTimeout(cardTimer);
  }, []);

  if (!llmResults) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen min-h-[100dvh] px-4 py-6 safe-area-inset">
        <AveryOrb state="attentive" size="small" />
        <p className="text-avery-text-secondary mt-6">Loading recommendations...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen min-h-[100dvh] px-4 py-6 safe-area-inset">
      {/* Orb - small, top corner */}
      <div className="flex justify-start mb-3">
        <AveryOrb state="presenting" size="small" />
      </div>

      {/* Avery's Intro */}
      <div className="mb-4">
        <p className="text-base sm:text-lg text-avery-text-secondary">
          <TypewriterText
            text={llmResults.avery_intro}
            speed={30}
            cursor={false}
          />
        </p>
      </div>

      {/* Recommendation Cards */}
      <div
        className={`
          flex-1 space-y-3 overflow-y-auto transition-all duration-700 ease-out
          ${showCards ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}
        `}
      >
        {llmResults.recommendations.map((rec, index) => (
          <RecommendationCard
            key={rec.role_id}
            recommendation={rec}
            rank={index + 1}
            isExpanded={expandedIndex === index}
            onToggle={() => setExpandedIndex(expandedIndex === index ? -1 : index)}
          />
        ))}
      </div>

      {/* Action Buttons */}
      <div
        className={`
          space-y-2 mt-4 flex-shrink-0 transition-all duration-500 delay-500
          ${showCards ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}
        `}
      >
        <GlowButton
          variant="primary"
          size="lg"
          onClick={onStartAssessment}
          className="w-full"
        >
          Explore Top Match
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
      <ProgressDots total={4} current={4} className="mt-4 pb-2" />
    </div>
  );
};

export default RecommendationScreen;
