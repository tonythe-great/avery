"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getResults, RoleMatch } from "@/lib/api";
import { AveryOrb } from "@/components/AveryOrb";
import { GlowButton } from "@/components/ui/GlowButton";

// Rank styling for top 3 matches
const RANK_CONFIG = [
  {
    label: "Primary Match",
    badge: "#1",
    color: "text-avery-cyan",
    bgColor: "bg-avery-cyan/20",
    borderColor: "border-avery-cyan/40",
    glowColor: "shadow-glow-cyan",
    ringColor: "#00d4ff",
  },
  {
    label: "Secondary Match",
    badge: "#2",
    color: "text-avery-purple",
    bgColor: "bg-avery-purple/20",
    borderColor: "border-avery-purple/40",
    glowColor: "shadow-glow-purple",
    ringColor: "#7c3aed",
  },
  {
    label: "Tertiary Match",
    badge: "#3",
    color: "text-avery-teal",
    bgColor: "bg-avery-teal/20",
    borderColor: "border-avery-teal/40",
    glowColor: "shadow-glow-teal",
    ringColor: "#06b6d4",
  },
];

// Salary estimates by role
const SALARY_RANGES: Record<string, { min: number; max: number }> = {
  "SOC Analyst": { min: 65000, max: 95000 },
  "Penetration Tester": { min: 85000, max: 140000 },
  "Incident Response Specialist": { min: 80000, max: 130000 },
  "Security Engineer": { min: 95000, max: 155000 },
  "Cybersecurity Consultant": { min: 90000, max: 160000 },
  "Threat Intelligence Analyst": { min: 85000, max: 135000 },
  "Security Awareness Training Specialist": { min: 70000, max: 110000 },
  "Chief Information Security Officer": { min: 180000, max: 350000 },
  "Digital Forensics Investigator": { min: 75000, max: 125000 },
  "Cloud Security Architect": { min: 140000, max: 220000 },
};

const formatSalary = (amount: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(amount);
};

// Confidence Ring Component
const ConfidenceRing: React.FC<{
  percentage: number;
  color: string;
  size?: number;
}> = ({ percentage, color, size = 72 }) => {
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

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.1)"
          strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{
            transition: "stroke-dashoffset 1s ease-out",
            filter: `drop-shadow(0 0 6px ${color})`,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-lg font-bold text-avery-text-primary">
          {Math.round(animatedPercentage)}%
        </span>
      </div>
    </div>
  );
};

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<RoleMatch[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [veteranName, setVeteranName] = useState("");
  const [expandedCard, setExpandedCard] = useState<number | null>(0);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    const storedId = localStorage.getItem("veteranId");
    const storedName = localStorage.getItem("veteranName");

    if (!storedId) {
      router.push("/start");
      return;
    }

    setVeteranName(storedName || "");
    loadResults(parseInt(storedId));
  }, [router]);

  const loadResults = async (veteranId: number) => {
    try {
      const data = await getResults(veteranId);
      setResults(data);
      // Delay showing results for dramatic effect
      setTimeout(() => setShowResults(true), 500);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load results");
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartOver = () => {
    localStorage.removeItem("veteranId");
    localStorage.removeItem("veteranName");
    router.push("/");
  };

  const handleRetakeAssessment = () => {
    router.push("/assessment");
  };

  // Loading state
  if (isLoading) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center relative">
        <BackgroundGradient />
        <div className="relative z-10 text-center">
          <AveryOrb state="processing" size="large" />
          <p className="text-avery-text-primary text-xl mt-8 font-medium">
            Generating Career Intelligence
          </p>
          <p className="text-avery-text-secondary mt-2">
            Analyzing {veteranName ? `${veteranName.split(" ")[0]}'s` : "your"} profile...
          </p>
        </div>
      </main>
    );
  }

  // Error state
  if (error) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center px-6 relative">
        <BackgroundGradient />
        <div className="relative z-10 text-center max-w-sm">
          <AveryOrb state="dormant" size="medium" />
          <h2 className="text-xl font-bold text-avery-text-primary mt-6 mb-2">
            Analysis Interrupted
          </h2>
          <p className="text-avery-text-secondary mb-6">{error}</p>
          <div className="space-y-3">
            <GlowButton variant="primary" onClick={handleRetakeAssessment} className="w-full">
              Retake Assessment
            </GlowButton>
            <GlowButton variant="ghost" onClick={handleStartOver} className="w-full">
              Start Over
            </GlowButton>
          </div>
        </div>
      </main>
    );
  }

  const firstName = veteranName ? veteranName.split(" ")[0] : "Your";

  return (
    <main className="min-h-screen bg-avery-bg text-white relative">
      <BackgroundGradient />

      <div className="relative z-10 px-6 py-8">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <p className="text-avery-text-muted text-sm">Career Intelligence Report</p>
            <h1 className="text-2xl font-bold text-avery-text-primary mt-1">
              {firstName}&apos;s Top Matches
            </h1>
          </div>
          <AveryOrb state="presenting" size="small" />
        </div>

        {/* Summary Stats */}
        <div
          className={`
            bg-avery-bg-elevated/60 backdrop-blur-sm rounded-2xl p-4 mb-6
            border border-avery-bg-hover
            transition-all duration-500
            ${showResults ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
          `}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-avery-text-muted text-xs uppercase tracking-wider">
                Roles Analyzed
              </p>
              <p className="text-2xl font-bold text-avery-text-primary">847</p>
            </div>
            <div className="h-10 w-px bg-avery-bg-hover" />
            <div>
              <p className="text-avery-text-muted text-xs uppercase tracking-wider">
                Top Match
              </p>
              <p className="text-2xl font-bold text-avery-cyan">
                {results[0] ? Math.round(results[0].match_percentage) : 0}%
              </p>
            </div>
            <div className="h-10 w-px bg-avery-bg-hover" />
            <div>
              <p className="text-avery-text-muted text-xs uppercase tracking-wider">
                Matches Found
              </p>
              <p className="text-2xl font-bold text-avery-text-primary">{results.length}</p>
            </div>
          </div>
        </div>

        {/* Results Cards */}
        <div className="space-y-4 max-w-lg mx-auto">
          {results.map((match, index) => {
            const config = RANK_CONFIG[index] || RANK_CONFIG[2];
            const salary = SALARY_RANGES[match.role.name] || { min: 70000, max: 120000 };
            const isExpanded = expandedCard === index;

            return (
              <div
                key={match.role.id}
                className={`
                  transition-all duration-500
                  ${showResults ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}
                `}
                style={{ transitionDelay: `${(index + 1) * 150}ms` }}
              >
                <button
                  onClick={() => setExpandedCard(isExpanded ? null : index)}
                  className="w-full text-left"
                >
                  <div
                    className={`
                      relative bg-avery-bg-elevated/80 backdrop-blur-sm rounded-2xl
                      border-2 transition-all duration-300
                      ${isExpanded ? `${config.borderColor} ${config.glowColor}` : "border-avery-bg-hover"}
                    `}
                  >
                    {/* Rank Badge */}
                    <div
                      className={`
                        absolute -top-3 left-4 px-3 py-1 rounded-full
                        ${config.bgColor} ${config.color}
                        text-xs font-bold uppercase tracking-wider
                        border ${config.borderColor}
                      `}
                    >
                      {config.badge} {config.label}
                    </div>

                    <div className="p-5 pt-6">
                      <div className="flex items-start gap-4">
                        {/* Confidence Ring */}
                        <ConfidenceRing
                          percentage={match.match_percentage}
                          color={config.ringColor}
                        />

                        {/* Role Info */}
                        <div className="flex-1 min-w-0">
                          <h3 className="font-bold text-lg text-avery-text-primary leading-tight">
                            {match.role.name}
                          </h3>

                          {/* Salary Range */}
                          <p className="text-avery-text-secondary text-sm mt-1">
                            {formatSalary(salary.min)} — {formatSalary(salary.max)}
                          </p>

                          {/* Expand indicator */}
                          <div className="flex items-center gap-1 mt-2 text-avery-text-muted text-xs">
                            <span>{isExpanded ? "Hide details" : "View details"}</span>
                            <svg
                              className={`w-4 h-4 transition-transform duration-300 ${
                                isExpanded ? "rotate-180" : ""
                              }`}
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M19 9l-7 7-7-7"
                              />
                            </svg>
                          </div>
                        </div>
                      </div>

                      {/* Expanded Content */}
                      {isExpanded && (
                        <div className="mt-4 pt-4 border-t border-avery-bg-hover animate-fade-in">
                          {/* Description */}
                          <p className="text-avery-text-secondary text-sm leading-relaxed mb-4">
                            {match.role.description}
                          </p>

                          {/* Match Reasons */}
                          {match.match_reasons.length > 0 && (
                            <div>
                              <p className="text-xs text-avery-text-muted uppercase tracking-wider mb-3">
                                Why You Match
                              </p>
                              <div className="space-y-2">
                                {match.match_reasons.map((reason, i) => (
                                  <div
                                    key={i}
                                    className="flex items-start gap-2 text-sm"
                                  >
                                    <span className={config.color}>&#10003;</span>
                                    <span className="text-avery-text-secondary">{reason}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Quick Stats */}
                          <div className="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-avery-bg-hover">
                            <div className="bg-avery-bg-subtle rounded-lg p-3">
                              <p className="text-xs text-avery-text-muted">Median Salary</p>
                              <p className="text-lg font-semibold text-avery-text-primary">
                                {formatSalary((salary.min + salary.max) / 2)}
                              </p>
                            </div>
                            <div className="bg-avery-bg-subtle rounded-lg p-3">
                              <p className="text-xs text-avery-text-muted">Match Confidence</p>
                              <p className={`text-lg font-semibold ${config.color}`}>
                                {match.match_percentage >= 80
                                  ? "High"
                                  : match.match_percentage >= 60
                                  ? "Medium"
                                  : "Moderate"}
                              </p>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </button>
              </div>
            );
          })}
        </div>

        {/* Action Buttons */}
        <div
          className={`
            max-w-lg mx-auto mt-8 space-y-3
            transition-all duration-500 delay-700
            ${showResults ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}
          `}
        >
          <GlowButton variant="secondary" onClick={handleRetakeAssessment} className="w-full">
            Retake Assessment
          </GlowButton>
          <GlowButton variant="ghost" onClick={handleStartOver} className="w-full">
            Start New Session
          </GlowButton>
        </div>

        {/* Footer */}
        <p
          className={`
            text-center text-avery-text-muted text-xs mt-8 max-w-sm mx-auto
            transition-all duration-500 delay-1000
            ${showResults ? "opacity-100" : "opacity-0"}
          `}
        >
          Career matches generated by Avery AI based on personality analysis and military experience.
          Salary data reflects industry averages for 2024-2025.
        </p>
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
