"""
SCCT (Social Cognitive Career Theory) seed data for Avery.
10 Navy-authentic questions covering self-efficacy, outcome expectations, goals, and barriers.
"""
from app.database import SessionLocal, engine, Base
from app.models.scct import SCCTQuestion, SCCTOption, SalaryBand
from app.models.cyber_role import CyberRole


# The 10 SCCT Questions with calibrated option weights
SCCT_QUESTIONS = [
    # Q1: Watchstation Identity (Self-Efficacy - Technical)
    {
        "question_key": "watchstation_identity",
        "scct_construct": "self_efficacy",
        "question_text": "Think about your best watchstation or duty assignment. What made you good at it?",
        "order": 1,
        "options": [
            {
                "option_key": "a",
                "option_text": "I stayed calm when everything went sideways",
                "se_technical": 0.0, "se_stress": 0.8, "se_growth": 0.1, "se_social": 0.1,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "I caught details that others missed",
                "se_technical": 0.3, "se_stress": 0.2, "se_growth": 0.2, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "I figured out problems no one else could solve",
                "se_technical": 0.6, "se_stress": 0.2, "se_growth": 0.5, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.1,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I kept my team organized and on track",
                "se_technical": 0.1, "se_stress": 0.3, "se_growth": 0.2, "se_social": 0.5,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.3,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "e",
                "option_text": "I could explain complex situations clearly",
                "se_technical": 0.2, "se_stress": 0.1, "se_growth": 0.3, "se_social": 0.6,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.2,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
        ],
    },

    # Q2: Pressure Response (Self-Efficacy - Stress)
    {
        "question_key": "pressure_response",
        "scct_construct": "self_efficacy",
        "question_text": "When the CO is breathing down your neck and everything is on fire, what happens to your performance?",
        "order": 2,
        "options": [
            {
                "option_key": "a",
                "option_text": "I get sharper - pressure is my fuel",
                "se_technical": 0.0, "se_stress": 0.9, "se_growth": 0.2, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.1,
                "goals_timeline": 0.0, "goals_level": 0.2,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "I stay steady - same output regardless",
                "se_technical": 0.0, "se_stress": 0.7, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "I need a minute to regroup, then I'm good",
                "se_technical": 0.0, "se_stress": 0.4, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I prefer to avoid those situations when possible",
                "se_technical": 0.0, "se_stress": 0.1, "se_growth": 0.0, "se_social": 0.1,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.4, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
        ],
    },

    # Q3: Learning Velocity (Self-Efficacy - Growth)
    {
        "question_key": "learning_velocity",
        "scct_construct": "self_efficacy",
        "question_text": "When the Navy handed you a new system you'd never seen before, how did you handle it?",
        "order": 3,
        "options": [
            {
                "option_key": "a",
                "option_text": "I dove into the manuals and figured it out myself",
                "se_technical": 0.4, "se_stress": 0.1, "se_growth": 0.9, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.1,
                "barriers_financial": 0.0, "barriers_technical": -0.2, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "I found someone who knew it and asked questions",
                "se_technical": 0.2, "se_stress": 0.0, "se_growth": 0.5, "se_social": 0.4,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "I learned just enough to do my job",
                "se_technical": 0.1, "se_stress": 0.0, "se_growth": 0.2, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": -0.1,
                "barriers_financial": 0.0, "barriers_technical": 0.1, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I struggled until I got formal training",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.1, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.3, "barriers_direction": 0.1,
            },
        ],
    },

    # Q4: Outcome Priority (Outcome Expectations)
    {
        "question_key": "outcome_priority",
        "scct_construct": "outcome_expectations",
        "question_text": "Be honest with yourself. What matters most in your next career?",
        "order": 4,
        "options": [
            {
                "option_key": "a",
                "option_text": "Making serious money (6 figures+)",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.9, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.3,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "Stability and work-life balance",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.9, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "Doing work that actually matters",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.9,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "Keeping my brain engaged and learning",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.3, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.5,
                "goals_timeline": 0.0, "goals_level": 0.1,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "e",
                "option_text": "Building something I can be proud of",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.7,
                "goals_timeline": 0.0, "goals_level": 0.2,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
        ],
    },

    # Q5: Timeline Pressure (Goals - Urgency)
    {
        "question_key": "timeline_pressure",
        "scct_construct": "goals",
        "question_text": "When do you need to be earning civilian pay?",
        "order": 5,
        "options": [
            {
                "option_key": "a",
                "option_text": "Yesterday - I'm already separated and need income now",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": -0.3, "goals_level": 0.0,
                "barriers_financial": 0.5, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "0-6 months - I'm about to transition",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.2, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "6-12 months - I have time to prepare",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.3, "goals_level": 0.0,
                "barriers_financial": -0.1, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "1+ year - I'm planning ahead",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.6, "goals_level": 0.1,
                "barriers_financial": -0.2, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
        ],
    },

    # Q6: Risk Appetite (Barriers - Financial)
    {
        "question_key": "risk_appetite",
        "scct_construct": "barriers",
        "question_text": "Could you handle 3-6 months of intensive training with reduced or no income?",
        "order": 6,
        "options": [
            {
                "option_key": "a",
                "option_text": "Yes - I have savings and/or VA benefits to cover me",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.2, "goals_level": 0.1,
                "barriers_financial": -0.3, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "Maybe - if the payoff is worth it",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.2, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.1, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "No - I need steady income from day one",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.3, "oe_meaning_priority": 0.0,
                "goals_timeline": -0.1, "goals_level": 0.0,
                "barriers_financial": 0.5, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I'd need to see the numbers to decide",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.2, "barriers_technical": 0.0, "barriers_direction": 0.1,
            },
        ],
    },

    # Q7: Tech Comfort (Self-Efficacy - Technical)
    {
        "question_key": "tech_comfort",
        "scct_construct": "self_efficacy",
        "question_text": "How do you feel about the tech side of cybersecurity?",
        "order": 7,
        "options": [
            {
                "option_key": "a",
                "option_text": "I can already code or script",
                "se_technical": 0.9, "se_stress": 0.0, "se_growth": 0.3, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.1,
                "barriers_financial": 0.0, "barriers_technical": -0.3, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "I've done IT work and can pick up new tools fast",
                "se_technical": 0.6, "se_stress": 0.0, "se_growth": 0.4, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": -0.1, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "I'm tech-comfortable but not technical",
                "se_technical": 0.3, "se_stress": 0.0, "se_growth": 0.2, "se_social": 0.2,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.2, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I'll need to start from zero on the tech stuff",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.1, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.5, "barriers_direction": 0.2,
            },
        ],
    },

    # Q8: Social Preference (Self-Efficacy - Social)
    {
        "question_key": "social_preference",
        "scct_construct": "self_efficacy",
        "question_text": "In your ideal workday, how much are you interacting with people?",
        "order": 8,
        "options": [
            {
                "option_key": "a",
                "option_text": "Constantly - I'm presenting, meeting, coordinating",
                "se_technical": 0.0, "se_stress": 0.1, "se_growth": 0.1, "se_social": 0.9,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.2,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "Regularly - team huddles and collaboration",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.6,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "Occasionally - mostly heads-down with check-ins",
                "se_technical": 0.1, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.3,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "Rarely - I do my best work alone",
                "se_technical": 0.2, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
        ],
    },

    # Q9: Authority Preference (Goals - Career Level)
    {
        "question_key": "authority_preference",
        "scct_construct": "goals",
        "question_text": "Where do you want to be in 5 years?",
        "order": 9,
        "options": [
            {
                "option_key": "a",
                "option_text": "Running the show - managing teams and strategy",
                "se_technical": 0.0, "se_stress": 0.1, "se_growth": 0.1, "se_social": 0.3,
                "oe_salary_priority": 0.2, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.1,
                "goals_timeline": 0.0, "goals_level": 0.9,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "b",
                "option_text": "Senior individual contributor - expert, not manager",
                "se_technical": 0.2, "se_stress": 0.0, "se_growth": 0.2, "se_social": 0.0,
                "oe_salary_priority": 0.1, "oe_stability_priority": 0.1, "oe_meaning_priority": 0.1,
                "goals_timeline": 0.0, "goals_level": 0.5,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "c",
                "option_text": "Solid mid-career role - stable and respected",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.2, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.2,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.0,
            },
            {
                "option_key": "d",
                "option_text": "I just need to get started - 5 years feels far away",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": -0.1, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.2,
            },
        ],
    },

    # Q10: Barrier Awareness (Barriers - Self-Assessment)
    {
        "question_key": "barrier_awareness",
        "scct_construct": "barriers",
        "question_text": "What's the biggest thing standing between you and a cybersecurity career?",
        "order": 10,
        "options": [
            {
                "option_key": "a",
                "option_text": "I don't know where to start",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.1, "barriers_direction": 0.7,
            },
            {
                "option_key": "b",
                "option_text": "I don't have the certifications",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.1, "barriers_technical": 0.3, "barriers_direction": 0.3,
            },
            {
                "option_key": "c",
                "option_text": "I don't have the technical skills yet",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.6, "barriers_direction": 0.2,
            },
            {
                "option_key": "d",
                "option_text": "I don't have connections in the industry",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.0, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": 0.0, "barriers_technical": 0.0, "barriers_direction": 0.4,
            },
            {
                "option_key": "e",
                "option_text": "Nothing - I just need the roadmap",
                "se_technical": 0.0, "se_stress": 0.0, "se_growth": 0.1, "se_social": 0.0,
                "oe_salary_priority": 0.0, "oe_stability_priority": 0.0, "oe_meaning_priority": 0.0,
                "goals_timeline": 0.0, "goals_level": 0.0,
                "barriers_financial": -0.1, "barriers_technical": -0.1, "barriers_direction": 0.0,
            },
        ],
    },
]


# Salary bands by role and experience level (USD, annual, 2024-2025 data)
SALARY_BANDS = [
    # SOC Analyst
    {"role_name": "Security Operations Center (SOC) Analyst", "experience_level": "entry", "p10": 55000, "p25": 60000, "p50": 70000, "p75": 80000, "p90": 90000},
    {"role_name": "Security Operations Center (SOC) Analyst", "experience_level": "mid", "p10": 65000, "p25": 75000, "p50": 85000, "p75": 95000, "p90": 110000},
    {"role_name": "Security Operations Center (SOC) Analyst", "experience_level": "senior", "p10": 80000, "p25": 90000, "p50": 100000, "p75": 115000, "p90": 130000},

    # Penetration Tester
    {"role_name": "Penetration Tester / Ethical Hacker", "experience_level": "entry", "p10": 70000, "p25": 80000, "p50": 90000, "p75": 100000, "p90": 115000},
    {"role_name": "Penetration Tester / Ethical Hacker", "experience_level": "mid", "p10": 90000, "p25": 100000, "p50": 115000, "p75": 130000, "p90": 150000},
    {"role_name": "Penetration Tester / Ethical Hacker", "experience_level": "senior", "p10": 110000, "p25": 125000, "p50": 140000, "p75": 160000, "p90": 180000},

    # Incident Response
    {"role_name": "Incident Response Specialist", "experience_level": "entry", "p10": 65000, "p25": 75000, "p50": 85000, "p75": 95000, "p90": 110000},
    {"role_name": "Incident Response Specialist", "experience_level": "mid", "p10": 80000, "p25": 95000, "p50": 110000, "p75": 125000, "p90": 140000},
    {"role_name": "Incident Response Specialist", "experience_level": "senior", "p10": 100000, "p25": 115000, "p50": 130000, "p75": 150000, "p90": 170000},
    {"role_name": "Incident Response Specialist", "experience_level": "lead", "p10": 120000, "p25": 135000, "p50": 150000, "p75": 170000, "p90": 190000},

    # Security Engineer
    {"role_name": "Security Engineer", "experience_level": "entry", "p10": 80000, "p25": 90000, "p50": 100000, "p75": 115000, "p90": 130000},
    {"role_name": "Security Engineer", "experience_level": "mid", "p10": 100000, "p25": 115000, "p50": 130000, "p75": 150000, "p90": 170000},
    {"role_name": "Security Engineer", "experience_level": "senior", "p10": 130000, "p25": 145000, "p50": 160000, "p75": 180000, "p90": 200000},

    # Cybersecurity Consultant
    {"role_name": "Cybersecurity Consultant", "experience_level": "entry", "p10": 70000, "p25": 80000, "p50": 95000, "p75": 110000, "p90": 125000},
    {"role_name": "Cybersecurity Consultant", "experience_level": "mid", "p10": 90000, "p25": 105000, "p50": 125000, "p75": 145000, "p90": 165000},
    {"role_name": "Cybersecurity Consultant", "experience_level": "senior", "p10": 120000, "p25": 140000, "p50": 160000, "p75": 185000, "p90": 210000},
    {"role_name": "Cybersecurity Consultant", "experience_level": "lead", "p10": 150000, "p25": 170000, "p50": 195000, "p75": 220000, "p90": 250000},

    # Threat Intelligence Analyst
    {"role_name": "Threat Intelligence Analyst", "experience_level": "entry", "p10": 70000, "p25": 80000, "p50": 90000, "p75": 100000, "p90": 115000},
    {"role_name": "Threat Intelligence Analyst", "experience_level": "mid", "p10": 85000, "p25": 100000, "p50": 115000, "p75": 130000, "p90": 145000},
    {"role_name": "Threat Intelligence Analyst", "experience_level": "senior", "p10": 110000, "p25": 125000, "p50": 140000, "p75": 155000, "p90": 175000},

    # Security Awareness Trainer
    {"role_name": "Security Awareness Training Specialist", "experience_level": "entry", "p10": 55000, "p25": 65000, "p50": 75000, "p75": 85000, "p90": 100000},
    {"role_name": "Security Awareness Training Specialist", "experience_level": "mid", "p10": 70000, "p25": 80000, "p50": 95000, "p75": 110000, "p90": 125000},
    {"role_name": "Security Awareness Training Specialist", "experience_level": "senior", "p10": 90000, "p25": 105000, "p50": 120000, "p75": 140000, "p90": 160000},

    # CISO
    {"role_name": "Chief Information Security Officer (CISO)", "experience_level": "mid", "p10": 150000, "p25": 175000, "p50": 200000, "p75": 250000, "p90": 300000},
    {"role_name": "Chief Information Security Officer (CISO)", "experience_level": "senior", "p10": 200000, "p25": 250000, "p50": 300000, "p75": 350000, "p90": 400000},
    {"role_name": "Chief Information Security Officer (CISO)", "experience_level": "director", "p10": 250000, "p25": 300000, "p50": 375000, "p75": 450000, "p90": 550000},

    # Digital Forensics
    {"role_name": "Digital Forensics Investigator", "experience_level": "entry", "p10": 60000, "p25": 70000, "p50": 80000, "p75": 90000, "p90": 105000},
    {"role_name": "Digital Forensics Investigator", "experience_level": "mid", "p10": 75000, "p25": 90000, "p50": 105000, "p75": 120000, "p90": 140000},
    {"role_name": "Digital Forensics Investigator", "experience_level": "senior", "p10": 100000, "p25": 115000, "p50": 130000, "p75": 150000, "p90": 175000},

    # Cloud Security Architect
    {"role_name": "Cloud Security Architect", "experience_level": "entry", "p10": 100000, "p25": 115000, "p50": 130000, "p75": 150000, "p90": 170000},
    {"role_name": "Cloud Security Architect", "experience_level": "mid", "p10": 130000, "p25": 150000, "p50": 170000, "p75": 195000, "p90": 220000},
    {"role_name": "Cloud Security Architect", "experience_level": "senior", "p10": 160000, "p25": 185000, "p50": 210000, "p75": 240000, "p90": 280000},
    {"role_name": "Cloud Security Architect", "experience_level": "lead", "p10": 190000, "p25": 220000, "p50": 250000, "p75": 290000, "p90": 340000},
]


def seed_scct_data():
    """Seed the database with SCCT questions, options, and salary bands."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if SCCT data already exists
        existing_questions = db.query(SCCTQuestion).count()
        existing_salary_bands = db.query(SalaryBand).count()

        if existing_questions == 0:
            print("Seeding SCCT questions and options...")
            for q_data in SCCT_QUESTIONS:
                question = SCCTQuestion(
                    question_key=q_data["question_key"],
                    scct_construct=q_data["scct_construct"],
                    question_text=q_data["question_text"],
                    order=q_data["order"],
                )
                db.add(question)
                db.flush()  # Get the question ID

                for opt_data in q_data["options"]:
                    option = SCCTOption(
                        question_id=question.id,
                        **opt_data
                    )
                    db.add(option)

            db.commit()
            print(f"Added {len(SCCT_QUESTIONS)} SCCT questions with options.")
        else:
            print(f"SCCT questions already exist ({existing_questions} found). Skipping.")

        if existing_salary_bands == 0:
            print("Seeding salary bands...")
            for band_data in SALARY_BANDS:
                # Find the role by name
                role_name = band_data.pop("role_name")
                role = db.query(CyberRole).filter(CyberRole.name == role_name).first()
                if role:
                    salary_band = SalaryBand(role_id=role.id, **band_data)
                    db.add(salary_band)
                else:
                    print(f"Warning: Role '{role_name}' not found for salary band.")
                band_data["role_name"] = role_name  # Restore for potential retry

            db.commit()
            print(f"Added {len(SALARY_BANDS)} salary bands.")
        else:
            print(f"Salary bands already exist ({existing_salary_bands} found). Skipping.")

        print("SCCT data seeding complete!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_scct_data()
