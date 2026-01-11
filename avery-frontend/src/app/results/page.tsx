"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getResults, RoleMatch } from "@/lib/api";

const MEDAL_COLORS = [
  "from-yellow-300 to-yellow-500", // Gold
  "from-gray-300 to-gray-400",     // Silver
  "from-amber-600 to-amber-700",   // Bronze
];

const MEDAL_LABELS = ["Best Match", "Great Fit", "Strong Option"];

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<RoleMatch[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [veteranName, setVeteranName] = useState("");
  const [expandedCard, setExpandedCard] = useState<number | null>(0);

  useEffect(() => {
    const storedId = localStorage.getItem("veteranId");
    const storedName = localStorage.getItem("veteranName");
    
    if (!storedId) {
      router.push("/onboarding");
      return;
    }
    
    setVeteranName(storedName || "");
    loadResults(parseInt(storedId));
  }, [router]);

  const loadResults = async (veteranId: number) => {
    try {
      const data = await getResults(veteranId);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load results");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white flex items-center justify-center">
        <div className="text-center px-6">
          <div className="w-16 h-16 border-4 border-gold-400 border-t-transparent rounded-full animate-spin mx-auto mb-6" />
          <h2 className="text-xl font-bold mb-2">Analyzing Your Profile</h2>
          <p className="text-navy-400">Finding your perfect cybersecurity matches...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2">Couldn't Load Results</h2>
          <p className="text-navy-400 mb-6">{error}</p>
          <Link
            href="/assessment"
            className="inline-block px-6 py-3 bg-navy-700 rounded-xl text-white"
          >
            Retake Assessment
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white px-6 py-8">
      {/* Header */}
      <div className="max-w-sm mx-auto text-center mb-8 animate-fade-in">
        <div className="w-20 h-20 bg-gradient-to-br from-gold-400 to-gold-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
          <svg className="w-10 h-10 text-navy-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold mb-2">
          {veteranName ? `${veteranName.split(" ")[0]}'s` : "Your"} Top Matches
        </h1>
        <p className="text-navy-400">
          Based on your personality and Navy experience
        </p>
      </div>

      {/* Results Cards */}
      <div className="max-w-sm mx-auto space-y-4">
        {results.map((match, index) => (
          <div
            key={match.role.id}
            className="animate-slide-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <button
              onClick={() => setExpandedCard(expandedCard === index ? null : index)}
              className="w-full text-left"
            >
              <div className={`relative bg-navy-800/70 backdrop-blur rounded-2xl overflow-hidden transition-all ${
                expandedCard === index ? "ring-2 ring-gold-400" : ""
              }`}>
                {/* Rank badge */}
                <div className={`absolute top-0 right-0 px-3 py-1 rounded-bl-xl bg-gradient-to-r ${MEDAL_COLORS[index]} text-navy-900 text-xs font-bold`}>
                  #{index + 1} {MEDAL_LABELS[index]}
                </div>

                <div className="p-5 pt-8">
                  {/* Match percentage circle */}
                  <div className="flex items-start gap-4">
                    <div className="relative w-16 h-16 flex-shrink-0">
                      <svg className="w-16 h-16 transform -rotate-90">
                        <circle
                          cx="32"
                          cy="32"
                          r="28"
                          stroke="currentColor"
                          strokeWidth="6"
                          fill="none"
                          className="text-navy-700"
                        />
                        <circle
                          cx="32"
                          cy="32"
                          r="28"
                          stroke="currentColor"
                          strokeWidth="6"
                          fill="none"
                          strokeDasharray={`${match.match_percentage * 1.76} 176`}
                          className="text-gold-400"
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-sm font-bold">{Math.round(match.match_percentage)}%</span>
                      </div>
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-lg leading-tight mb-1">
                        {match.role.name}
                      </h3>
                      <div className="flex items-center gap-1 text-navy-400 text-sm">
                        <span>Tap to {expandedCard === index ? "collapse" : "expand"}</span>
                        <svg
                          className={`w-4 h-4 transition-transform ${expandedCard === index ? "rotate-180" : ""}`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>
                  </div>

                  {/* Expanded content */}
                  {expandedCard === index && (
                    <div className="mt-4 pt-4 border-t border-navy-700 animate-fade-in">
                      <p className="text-navy-300 text-sm mb-4">
                        {match.role.description}
                      </p>
                      
                      {match.match_reasons.length > 0 && (
                        <div>
                          <p className="text-xs text-navy-500 uppercase tracking-wide mb-2">Why you're a great fit:</p>
                          <div className="flex flex-wrap gap-2">
                            {match.match_reasons.map((reason, i) => (
                              <span
                                key={i}
                                className="px-3 py-1 bg-gold-500/20 text-gold-400 text-xs rounded-full"
                              >
                                {reason}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </button>
          </div>
        ))}
      </div>

      {/* Action buttons */}
      <div className="max-w-sm mx-auto mt-8 space-y-3">
        <button
          onClick={() => {
            localStorage.removeItem("veteranId");
            localStorage.removeItem("veteranName");
            router.push("/");
          }}
          className="w-full py-4 rounded-xl border border-navy-600 text-navy-300 font-medium active:scale-[0.98] transition-transform"
        >
          Start Over
        </button>
      </div>

      {/* Footer */}
      <p className="text-center text-navy-500 text-xs mt-8 max-w-xs mx-auto">
        These recommendations are based on personality traits and military experience. 
        Explore each role to learn more about required certifications and career paths.
      </p>
    </main>
  );
}
