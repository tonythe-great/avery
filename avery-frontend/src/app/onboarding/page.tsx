"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createVeteran, VeteranInput } from "@/lib/api";

const NAVY_RANKS = [
  "E-1 Seaman Recruit",
  "E-2 Seaman Apprentice", 
  "E-3 Seaman",
  "E-4 Petty Officer Third Class",
  "E-5 Petty Officer Second Class",
  "E-6 Petty Officer First Class",
  "E-7 Chief Petty Officer",
  "E-8 Senior Chief Petty Officer",
  "E-9 Master Chief Petty Officer",
  "O-1 Ensign",
  "O-2 Lieutenant Junior Grade",
  "O-3 Lieutenant",
  "O-4 Lieutenant Commander",
  "O-5 Commander",
  "O-6 Captain",
];

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  
  const [formData, setFormData] = useState<VeteranInput>({
    name: "",
    email: "",
    branch: "Navy",
    rank: "",
    rating: "",
    years_of_service: 0,
  });

  const updateField = (field: keyof VeteranInput, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setError("");
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError("");
    
    try {
      const veteran = await createVeteran(formData);
      // Store veteran ID for assessment
      localStorage.setItem("veteranId", veteran.id.toString());
      localStorage.setItem("veteranName", veteran.name);
      router.push("/assessment");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  };

  const canProceed = () => {
    if (step === 1) return formData.name.length >= 2;
    if (step === 2) return formData.email.includes("@");
    if (step === 3) return formData.rank.length > 0;
    if (step === 4) return formData.years_of_service > 0;
    return false;
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-navy-900 via-navy-800 to-navy-950 text-white px-6 py-8">
      {/* Progress bar */}
      <div className="max-w-sm mx-auto mb-8">
        <div className="flex justify-between text-xs text-navy-400 mb-2">
          <span>Step {step} of 4</span>
          <span>{Math.round((step / 4) * 100)}%</span>
        </div>
        <div className="h-2 bg-navy-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-gold-400 to-gold-500 transition-all duration-300"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>
      </div>

      <div className="max-w-sm mx-auto">
        {/* Step 1: Name */}
        {step === 1 && (
          <div className="animate-slide-up">
            <h2 className="text-2xl font-bold mb-2">What's your name?</h2>
            <p className="text-navy-400 mb-8">Let's get to know you.</p>
            
            <input
              type="text"
              value={formData.name}
              onChange={(e) => updateField("name", e.target.value)}
              placeholder="Enter your full name"
              className="w-full bg-navy-800 border border-navy-600 rounded-xl px-4 py-4 text-lg placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
              autoFocus
            />
          </div>
        )}

        {/* Step 2: Email */}
        {step === 2 && (
          <div className="animate-slide-up">
            <h2 className="text-2xl font-bold mb-2">What's your email?</h2>
            <p className="text-navy-400 mb-8">We'll use this to save your results.</p>
            
            <input
              type="email"
              value={formData.email}
              onChange={(e) => updateField("email", e.target.value)}
              placeholder="you@example.com"
              className="w-full bg-navy-800 border border-navy-600 rounded-xl px-4 py-4 text-lg placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
              autoFocus
            />
          </div>
        )}

        {/* Step 3: Rank */}
        {step === 3 && (
          <div className="animate-slide-up">
            <h2 className="text-2xl font-bold mb-2">What was your rank?</h2>
            <p className="text-navy-400 mb-8">Select your highest rank achieved.</p>
            
            <div className="space-y-2 max-h-[50vh] overflow-y-auto pr-2">
              {NAVY_RANKS.map((rank) => (
                <button
                  key={rank}
                  onClick={() => updateField("rank", rank)}
                  className={`w-full text-left px-4 py-3 rounded-xl transition-all ${
                    formData.rank === rank
                      ? "bg-gold-500 text-navy-900 font-medium"
                      : "bg-navy-800 hover:bg-navy-700"
                  }`}
                >
                  {rank}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Years of Service */}
        {step === 4 && (
          <div className="animate-slide-up">
            <h2 className="text-2xl font-bold mb-2">Years of service?</h2>
            <p className="text-navy-400 mb-8">How long did you serve?</p>
            
            <div className="text-center mb-8">
              <span className="text-6xl font-bold text-gold-400">
                {formData.years_of_service}
              </span>
              <span className="text-2xl text-navy-400 ml-2">years</span>
            </div>
            
            <input
              type="range"
              min="1"
              max="40"
              value={formData.years_of_service}
              onChange={(e) => updateField("years_of_service", parseInt(e.target.value))}
              className="w-full h-3 bg-navy-700 rounded-full appearance-none cursor-pointer accent-gold-400"
            />
            
            <div className="flex justify-between text-sm text-navy-500 mt-2">
              <span>1 year</span>
              <span>40 years</span>
            </div>

            {/* Optional: Rating */}
            <div className="mt-8">
              <label className="block text-sm text-navy-400 mb-2">
                Rating/MOS (optional)
              </label>
              <input
                type="text"
                value={formData.rating || ""}
                onChange={(e) => updateField("rating", e.target.value)}
                placeholder="e.g., IT, CTN, ET"
                className="w-full bg-navy-800 border border-navy-600 rounded-xl px-4 py-3 placeholder:text-navy-500 focus:outline-none focus:border-gold-400 transition-colors"
              />
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-300 text-sm">
            {error}
          </div>
        )}

        {/* Navigation buttons */}
        <div className="flex gap-4 mt-8">
          {step > 1 && (
            <button
              onClick={() => setStep(step - 1)}
              className="flex-1 py-4 rounded-xl border border-navy-600 text-navy-300 font-medium active:scale-[0.98] transition-transform"
            >
              Back
            </button>
          )}
          
          {step < 4 ? (
            <button
              onClick={() => setStep(step + 1)}
              disabled={!canProceed()}
              className="flex-1 py-4 rounded-xl bg-gradient-to-r from-gold-400 to-gold-500 text-navy-900 font-semibold disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98] transition-transform"
            >
              Continue
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!canProceed() || isLoading}
              className="flex-1 py-4 rounded-xl bg-gradient-to-r from-gold-400 to-gold-500 text-navy-900 font-semibold disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98] transition-transform"
            >
              {isLoading ? "Creating Profile..." : "Start Assessment"}
            </button>
          )}
        </div>
      </div>
    </main>
  );
}
