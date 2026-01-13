const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://avery-sg3k.onrender.com/api/v1";

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

// SCCT Types
export interface SCCTOption {
  id: number;
  option_key: string;
  option_text: string;
}

export interface SCCTQuestion {
  id: number;
  question_key: string;
  scct_construct: string;
  question_text: string;
  order: number;
  options: SCCTOption[];
}

export interface SCCTAnswer {
  question_id: number;
  option_id: number;
}

// Get SCCT questions
export async function getSCCTQuestions(): Promise<SCCTQuestion[]> {
  const response = await fetch(`${API_BASE}/scct/questions`);

  if (!response.ok) {
    throw new Error("Failed to load SCCT questions");
  }

  return response.json();
}

// Submit SCCT assessment
export async function submitSCCTAssessment(
  veteranId: number,
  answers: SCCTAnswer[]
): Promise<{ message: string; veteran_id: number; answers_recorded: number }> {
  const response = await fetch(`${API_BASE}/scct/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ veteran_id: veteranId, answers }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to submit SCCT assessment");
  }

  return response.json();
}

// Get SCCT status
export async function getSCCTStatus(veteranId: number): Promise<{
  veteran_id: number;
  questions_answered: number;
  total_questions: number;
  completed: boolean;
  vector_computed: boolean;
}> {
  const response = await fetch(`${API_BASE}/scct/status/${veteranId}`);

  if (!response.ok) {
    throw new Error("Failed to get SCCT status");
  }

  return response.json();
}

// Career Roadmap Types
export interface Certification {
  name: string;
  provider: string;
  level: "foundation" | "intermediate" | "advanced";
  estimated_weeks: number;
  cost_usd: number;
  url: string;
  description: string;
}

export interface SkillTranslation {
  military_skill: string;
  military_context: string;
  cyber_skill: string;
  transferability: number;
}

export interface ActionStep {
  phase: string;
  title: string;
  description: string;
  tasks: string[];
}

export interface CareerRoadmap {
  role_id: number;
  role_name: string;
  quick_summary: string;
  estimated_months_to_entry: number;
  certifications: Certification[];
  skill_translations: SkillTranslation[];
  action_steps: ActionStep[];
  salary_entry: string;
  salary_experienced: string;
  job_outlook: string;
}

export interface RoadmapPreview {
  role_id: number;
  quick_summary: string;
  top_certification: string;
  estimated_months: number;
  salary_entry: string;
}

// Get career roadmap for a role
export async function getRoadmap(roleId: number): Promise<CareerRoadmap> {
  const response = await fetch(`${API_BASE}/roadmap/${roleId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get roadmap");
  }

  return response.json();
}

// Get personalized roadmap for a veteran
export async function getPersonalizedRoadmap(
  veteranId: number,
  roleId: number
): Promise<CareerRoadmap> {
  const response = await fetch(
    `${API_BASE}/roadmap/veteran/${veteranId}/role/${roleId}`
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get personalized roadmap");
  }

  return response.json();
}

// Get roadmap preview for results cards
export async function getRoadmapPreview(roleId: number): Promise<RoadmapPreview> {
  const response = await fetch(`${API_BASE}/roadmap/${roleId}/preview`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to get roadmap preview");
  }

  return response.json();
}
