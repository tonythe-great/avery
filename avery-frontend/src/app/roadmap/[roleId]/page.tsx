"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams, useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { getRoadmap, getPersonalizedRoadmap, CareerRoadmap } from "@/lib/api";
import { AveryOrb } from "@/components/AveryOrb";
import { GlowButton } from "@/components/ui/GlowButton";

export default function RoadmapPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const roleId = parseInt(params.roleId as string);
  const matchPercentage = searchParams.get("match");

  const [roadmap, setRoadmap] = useState<CareerRoadmap | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState<string>("skills");

  const loadRoadmap = useCallback(async () => {
    try {
      const veteranId = localStorage.getItem("veteranId");
      let data: CareerRoadmap;

      if (veteranId) {
        // Try personalized roadmap first
        try {
          data = await getPersonalizedRoadmap(parseInt(veteranId), roleId);
        } catch {
          // Fall back to generic roadmap
          data = await getRoadmap(roleId);
        }
      } else {
        data = await getRoadmap(roleId);
      }

      setRoadmap(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load roadmap");
    } finally {
      setIsLoading(false);
    }
  }, [roleId]);

  useEffect(() => {
    loadRoadmap();
  }, [loadRoadmap]);

  if (isLoading) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center">
        <BackgroundGradient />
        <div className="relative z-10 text-center">
          <AveryOrb state="processing" size="medium" />
          <p className="text-avery-text-primary text-lg mt-6">
            Building Your Career Roadmap
          </p>
        </div>
      </main>
    );
  }

  if (error || !roadmap) {
    return (
      <main className="min-h-screen bg-avery-bg flex flex-col items-center justify-center px-6">
        <BackgroundGradient />
        <div className="relative z-10 text-center max-w-sm">
          <AveryOrb state="dormant" size="medium" />
          <h2 className="text-xl font-bold text-avery-text-primary mt-6 mb-2">
            Roadmap Not Found
          </h2>
          <p className="text-avery-text-secondary mb-6">
            {error || "This career roadmap is not available."}
          </p>
          <GlowButton variant="primary" onClick={() => router.push("/results")}>
            Back to Results
          </GlowButton>
        </div>
      </main>
    );
  }

  const sections = [
    { id: "skills", label: "Skills" },
    { id: "certs", label: "Certifications" },
    { id: "timeline", label: "Timeline" },
  ];

  return (
    <main className="min-h-screen bg-avery-bg text-white">
      <BackgroundGradient />

      <div className="relative z-10 safe-area-inset">
        {/* Header */}
        <div className="px-6 pt-6 pb-4">
          <Link
            href="/results"
            className="inline-flex items-center gap-2 text-avery-text-muted text-sm hover:text-avery-text-secondary transition-colors mb-4"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Results
          </Link>

          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-avery-cyan text-sm font-medium">
                {matchPercentage ? `${matchPercentage}% Match` : "Career Roadmap"}
              </p>
              <h1 className="text-2xl font-bold text-avery-text-primary mt-1 leading-tight">
                {roadmap.role_name}
              </h1>
              <p className="text-avery-text-secondary text-sm mt-2">
                {roadmap.quick_summary}
              </p>
            </div>
            <AveryOrb state="presenting" size="small" />
          </div>
        </div>

        {/* Salary Banner */}
        <div className="mx-6 mb-4 bg-gradient-to-r from-avery-cyan/20 to-avery-teal/20 rounded-xl p-4 border border-avery-cyan/30">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-xs text-avery-text-muted uppercase tracking-wider">Entry Level</p>
              <p className="text-lg font-bold text-avery-text-primary">{roadmap.salary_entry}</p>
            </div>
            <div className="h-8 w-px bg-avery-cyan/30" />
            <div className="text-right">
              <p className="text-xs text-avery-text-muted uppercase tracking-wider">Experienced</p>
              <p className="text-lg font-bold text-avery-cyan">{roadmap.salary_experienced}</p>
            </div>
          </div>
          <p className="text-xs text-avery-text-muted mt-3">{roadmap.job_outlook}</p>
        </div>

        {/* Section Tabs */}
        <div className="px-6 mb-4">
          <div className="flex gap-2 bg-avery-bg-elevated rounded-xl p-1">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`
                  flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all
                  ${activeSection === section.id
                    ? "bg-avery-cyan text-avery-bg"
                    : "text-avery-text-secondary hover:text-avery-text-primary"
                  }
                `}
              >
                {section.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content Sections */}
        <div className="px-6 pb-24">
          {/* Skills Translation Section */}
          {activeSection === "skills" && (
            <div className="space-y-4 animate-fade-in">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-semibold text-avery-text-primary">
                  Your Military Experience Translates
                </h2>
              </div>
              {roadmap.skill_translations.map((skill, index) => (
                <SkillTranslationCard key={index} skill={skill} index={index} />
              ))}
            </div>
          )}

          {/* Certifications Section */}
          {activeSection === "certs" && (
            <div className="space-y-4 animate-fade-in">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-semibold text-avery-text-primary">
                  Certification Path
                </h2>
              </div>
              {roadmap.certifications.map((cert, index) => (
                <CertificationCard key={index} cert={cert} index={index} />
              ))}
            </div>
          )}

          {/* Timeline Section */}
          {activeSection === "timeline" && (
            <div className="space-y-4 animate-fade-in">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-semibold text-avery-text-primary">
                  Your Action Plan
                </h2>
              </div>
              {roadmap.action_steps.map((step, index) => (
                <ActionPhaseCard key={index} step={step} index={index} total={roadmap.action_steps.length} />
              ))}
            </div>
          )}
        </div>

        {/* Fixed Bottom Actions */}
        <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-avery-bg via-avery-bg to-transparent pt-8 pb-6 px-6" style={{ paddingBottom: 'max(1.5rem, env(safe-area-inset-bottom))' }}>
          <div className="flex gap-3 max-w-lg mx-auto">
            <GlowButton
              variant="secondary"
              className="flex-1"
              onClick={() => {
                // Future: Save roadmap functionality
                alert("Save feature coming soon!");
              }}
            >
              Save Roadmap
            </GlowButton>
            <GlowButton
              variant="primary"
              className="flex-1"
              onClick={() => {
                // Future: Share functionality
                if (navigator.share) {
                  navigator.share({
                    title: `Career Roadmap: ${roadmap.role_name}`,
                    text: `Check out my career transition roadmap to become a ${roadmap.role_name}`,
                    url: window.location.href,
                  });
                } else {
                  navigator.clipboard.writeText(window.location.href);
                  alert("Link copied to clipboard!");
                }
              }}
            >
              Share
            </GlowButton>
          </div>
        </div>
      </div>
    </main>
  );
}

// Skill Translation Card Component
function SkillTranslationCard({
  skill,
  index,
}: {
  skill: { military_skill: string; military_context: string; cyber_skill: string; transferability: number };
  index: number;
}) {
  return (
    <div
      className="bg-avery-bg-elevated/80 backdrop-blur-sm rounded-xl p-4 border border-avery-bg-hover"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="flex items-start gap-4">
        {/* Transferability indicator */}
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-full bg-avery-cyan/20 flex items-center justify-center">
            <span className="text-avery-cyan font-bold text-sm">{skill.transferability}%</span>
          </div>
        </div>

        <div className="flex-1 min-w-0">
          {/* Military Skill */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs text-avery-text-muted uppercase tracking-wider">Navy</span>
            <div className="flex-1 h-px bg-avery-bg-hover" />
          </div>
          <p className="text-avery-text-primary font-medium">{skill.military_skill}</p>
          <p className="text-avery-text-muted text-sm mt-1 leading-relaxed">
            {skill.military_context}
          </p>

          {/* Arrow */}
          <div className="flex items-center gap-2 my-3">
            <div className="flex-1 h-px bg-avery-cyan/30" />
            <svg className="w-5 h-5 text-avery-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
            <div className="flex-1 h-px bg-avery-cyan/30" />
          </div>

          {/* Cyber Skill */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs text-avery-cyan uppercase tracking-wider">Cybersecurity</span>
            <div className="flex-1 h-px bg-avery-bg-hover" />
          </div>
          <p className="text-avery-cyan font-medium">{skill.cyber_skill}</p>
        </div>
      </div>
    </div>
  );
}

// Certification Card Component
function CertificationCard({
  cert,
  index,
}: {
  cert: {
    name: string;
    provider: string;
    level: string;
    estimated_weeks: number;
    cost_usd: number;
    url: string;
    description: string;
  };
  index: number;
}) {
  const levelColors = {
    foundation: { bg: "bg-green-500/20", text: "text-green-400", border: "border-green-500/30" },
    intermediate: { bg: "bg-yellow-500/20", text: "text-yellow-400", border: "border-yellow-500/30" },
    advanced: { bg: "bg-red-500/20", text: "text-red-400", border: "border-red-500/30" },
  };

  const colors = levelColors[cert.level as keyof typeof levelColors] || levelColors.foundation;

  return (
    <div
      className="bg-avery-bg-elevated/80 backdrop-blur-sm rounded-xl p-4 border border-avery-bg-hover"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-avery-purple/20 flex items-center justify-center text-avery-purple font-bold">
            {index + 1}
          </div>
          <div>
            <h3 className="font-semibold text-avery-text-primary">{cert.name}</h3>
            <p className="text-xs text-avery-text-muted">{cert.provider}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text} ${colors.border} border`}>
          {cert.level}
        </span>
      </div>

      {/* Description */}
      <p className="text-avery-text-secondary text-sm mb-4 leading-relaxed">
        {cert.description}
      </p>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm">
        <div className="flex items-center gap-1 text-avery-text-muted">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{cert.estimated_weeks} weeks</span>
        </div>
        <div className="flex items-center gap-1 text-avery-text-muted">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>${cert.cost_usd}</span>
        </div>
      </div>

      {/* Learn More Link */}
      <a
        href={cert.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-avery-cyan text-sm mt-4 hover:underline"
      >
        Learn More
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>
    </div>
  );
}

// Action Phase Card Component
function ActionPhaseCard({
  step,
  index,
  total,
}: {
  step: { phase: string; title: string; description: string; tasks: string[] };
  index: number;
  total: number;
}) {
  const [isExpanded, setIsExpanded] = useState(index === 0);

  return (
    <div
      className="relative"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Timeline connector */}
      {index < total - 1 && (
        <div className="absolute left-5 top-14 bottom-0 w-0.5 bg-avery-bg-hover" />
      )}

      <div
        className={`
          bg-avery-bg-elevated/80 backdrop-blur-sm rounded-xl border transition-all
          ${isExpanded ? "border-avery-teal/40" : "border-avery-bg-hover"}
        `}
      >
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full p-4 text-left"
        >
          <div className="flex items-start gap-4">
            {/* Phase indicator */}
            <div className={`
              w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center
              ${isExpanded ? "bg-avery-teal text-avery-bg" : "bg-avery-teal/20 text-avery-teal"}
            `}>
              {index + 1}
            </div>

            <div className="flex-1 min-w-0">
              <p className="text-xs text-avery-teal font-medium uppercase tracking-wider">
                {step.phase}
              </p>
              <h3 className="font-semibold text-avery-text-primary mt-1">
                {step.title}
              </h3>
              {!isExpanded && (
                <p className="text-avery-text-muted text-sm mt-1 line-clamp-1">
                  {step.description}
                </p>
              )}
            </div>

            <svg
              className={`w-5 h-5 text-avery-text-muted transition-transform ${isExpanded ? "rotate-180" : ""}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>

        {/* Expanded content */}
        {isExpanded && (
          <div className="px-4 pb-4 animate-fade-in">
            <p className="text-avery-text-secondary text-sm mb-4 ml-14">
              {step.description}
            </p>

            <div className="ml-14 space-y-2">
              {step.tasks.map((task, taskIndex) => (
                <div key={taskIndex} className="flex items-start gap-3">
                  <div className="w-5 h-5 rounded border border-avery-bg-hover flex-shrink-0 mt-0.5" />
                  <span className="text-avery-text-secondary text-sm">{task}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
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
