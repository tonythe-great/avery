const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface Veteran {
  id: number;
  name: string;
  email: string;
  branch: string;
  rank: string;
  rating?: string;
  years_of_service: number;
}

export interface VeteranInput {
  name: string;
  email: string;
  branch: string;
  rank: string;
  rating?: string;
  years_of_service: number;
}

export interface Question {
  id: number;
  text: string;
  trait: string;
  order: number;
}

export interface Answer {
  question_id: number;
  answer_value: number;
}

export interface RoleMatch {
  role: {
    id: number;
    name: string;
    description: string;
  };
  match_percentage: number;
  match_reasons: string[];
}

// Create veteran profile
export async function createVeteran(data: VeteranInput): Promise<Veteran> {
  const response = await fetch(`${API_BASE}/onboarding/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to create profile");
  }
  
  return response.json();
}

// Get assessment questions
export async function getQuestions(): Promise<Question[]> {
  const response = await fetch(`${API_BASE}/assessment/questions`);
  
  if (!response.ok) {
    throw new Error("Failed to load questions");
  }
  
  return response.json();
}

// Submit assessment answers
export async function submitAssessment(
  veteranId: number,
  answers: Answer[]
): Promise<{ message: string; veteran_id: number; answers_recorded: number }> {
  const response = await fetch(`${API_BASE}/assessment/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ veteran_id: veteranId, answers }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to submit assessment");
  }
  
  return response.json();
}

// Get results
export async function getResults(veteranId: number): Promise<RoleMatch[]> {
  const response = await fetch(`${API_BASE}/results/${veteranId}`);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get results");
  }
  
  return response.json();
}
