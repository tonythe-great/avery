"""
Seed data for the Avery personality assessment.
Run this script to populate the database with questions and cyber roles.
"""
from app.database import SessionLocal, engine, Base
from app.models.assessment import Question
from app.models.cyber_role import CyberRole


# Big Five personality questions (2-3 per trait = 12 total)
QUESTIONS = [
    # Openness (creativity, curiosity, willingness to learn new things)
    {"text": "I enjoy learning about new technologies and tools, even outside my job requirements.", "trait": "openness", "order": 1},
    {"text": "I often think of creative solutions to problems that others might not consider.", "trait": "openness", "order": 2},
    {"text": "I am comfortable adapting to new situations and changing environments.", "trait": "openness", "order": 3},
    
    # Conscientiousness (organization, attention to detail, dependability)
    {"text": "I prefer to follow established procedures and checklists rather than improvise.", "trait": "conscientiousness", "order": 4},
    {"text": "I pay close attention to details and rarely overlook important information.", "trait": "conscientiousness", "order": 5},
    {"text": "I always complete my tasks on time and meet my commitments.", "trait": "conscientiousness", "order": 6},
    
    # Extraversion (sociability, assertiveness, leadership)
    {"text": "I enjoy collaborating with team members and leading group discussions.", "trait": "extraversion", "order": 7},
    {"text": "I feel comfortable presenting information to large groups or stakeholders.", "trait": "extraversion", "order": 8},
    
    # Agreeableness (cooperation, trust, working with others)
    {"text": "I find it easy to understand and empathize with others' perspectives.", "trait": "agreeableness", "order": 9},
    {"text": "I prefer to find common ground rather than engage in confrontation.", "trait": "agreeableness", "order": 10},
    
    # Stability (calm under pressure, emotional resilience - inverted neuroticism)
    {"text": "I remain calm and focused when facing high-pressure situations or tight deadlines.", "trait": "stability", "order": 11},
    {"text": "I can handle criticism and setbacks without becoming discouraged.", "trait": "stability", "order": 12},
]


# Cybersecurity roles with trait profiles
CYBER_ROLES = [
    {
        "name": "Security Operations Center (SOC) Analyst",
        "description": "Monitor security alerts, analyze threats, and respond to incidents in real-time. Perfect for those who thrive under pressure and have strong attention to detail.",
        "openness_weight": 0.4, "openness_ideal": 3.5,
        "conscientiousness_weight": 0.9, "conscientiousness_ideal": 4.5,
        "extraversion_weight": 0.3, "extraversion_ideal": 3.0,
        "agreeableness_weight": 0.5, "agreeableness_ideal": 3.5,
        "stability_weight": 0.9, "stability_ideal": 4.5,
        "min_years_preferred": 2, "leadership_bonus": 0.0,
    },
    {
        "name": "Penetration Tester / Ethical Hacker",
        "description": "Simulate cyber attacks to identify vulnerabilities before malicious actors do. Ideal for creative problem-solvers who think outside the box.",
        "openness_weight": 0.9, "openness_ideal": 4.5,
        "conscientiousness_weight": 0.6, "conscientiousness_ideal": 4.0,
        "extraversion_weight": 0.4, "extraversion_ideal": 3.0,
        "agreeableness_weight": 0.3, "agreeableness_ideal": 3.0,
        "stability_weight": 0.6, "stability_ideal": 4.0,
        "min_years_preferred": 0, "leadership_bonus": 0.0,
    },
    {
        "name": "Incident Response Specialist",
        "description": "Lead the response to security breaches, coordinate remediation efforts, and conduct forensic analysis. Great for calm leaders who excel in crisis situations.",
        "openness_weight": 0.5, "openness_ideal": 3.5,
        "conscientiousness_weight": 0.8, "conscientiousness_ideal": 4.5,
        "extraversion_weight": 0.7, "extraversion_ideal": 4.0,
        "agreeableness_weight": 0.6, "agreeableness_ideal": 3.5,
        "stability_weight": 1.0, "stability_ideal": 5.0,
        "min_years_preferred": 4, "leadership_bonus": 0.15,
    },
    {
        "name": "Security Engineer",
        "description": "Design and implement security solutions, automate security processes, and build defensive infrastructure. Perfect for methodical builders who love technical challenges.",
        "openness_weight": 0.7, "openness_ideal": 4.0,
        "conscientiousness_weight": 0.9, "conscientiousness_ideal": 4.5,
        "extraversion_weight": 0.3, "extraversion_ideal": 2.5,
        "agreeableness_weight": 0.4, "agreeableness_ideal": 3.0,
        "stability_weight": 0.6, "stability_ideal": 4.0,
        "min_years_preferred": 2, "leadership_bonus": 0.0,
    },
    {
        "name": "Cybersecurity Consultant",
        "description": "Advise organizations on security strategy, compliance, and risk management. Ideal for communicators who can translate technical concepts for business leaders.",
        "openness_weight": 0.6, "openness_ideal": 4.0,
        "conscientiousness_weight": 0.7, "conscientiousness_ideal": 4.0,
        "extraversion_weight": 0.9, "extraversion_ideal": 4.5,
        "agreeableness_weight": 0.8, "agreeableness_ideal": 4.0,
        "stability_weight": 0.7, "stability_ideal": 4.0,
        "min_years_preferred": 4, "leadership_bonus": 0.1,
    },
    {
        "name": "Threat Intelligence Analyst",
        "description": "Research and analyze cyber threat actors, tactics, and trends to provide actionable intelligence. Great for analytical minds who enjoy deep research.",
        "openness_weight": 0.8, "openness_ideal": 4.5,
        "conscientiousness_weight": 0.8, "conscientiousness_ideal": 4.0,
        "extraversion_weight": 0.3, "extraversion_ideal": 2.5,
        "agreeableness_weight": 0.4, "agreeableness_ideal": 3.0,
        "stability_weight": 0.5, "stability_ideal": 3.5,
        "min_years_preferred": 2, "leadership_bonus": 0.0,
    },
    {
        "name": "Security Awareness Training Specialist",
        "description": "Develop and deliver security training programs to educate employees. Perfect for patient communicators who enjoy teaching and helping others learn.",
        "openness_weight": 0.6, "openness_ideal": 4.0,
        "conscientiousness_weight": 0.6, "conscientiousness_ideal": 3.5,
        "extraversion_weight": 0.9, "extraversion_ideal": 4.5,
        "agreeableness_weight": 0.9, "agreeableness_ideal": 4.5,
        "stability_weight": 0.5, "stability_ideal": 3.5,
        "min_years_preferred": 0, "leadership_bonus": 0.05,
    },
    {
        "name": "Chief Information Security Officer (CISO)",
        "description": "Lead an organization's entire security program, manage teams, and interface with executives. Ideal for experienced leaders with strong strategic vision.",
        "openness_weight": 0.6, "openness_ideal": 4.0,
        "conscientiousness_weight": 0.8, "conscientiousness_ideal": 4.5,
        "extraversion_weight": 0.9, "extraversion_ideal": 4.5,
        "agreeableness_weight": 0.7, "agreeableness_ideal": 4.0,
        "stability_weight": 0.9, "stability_ideal": 4.5,
        "min_years_preferred": 10, "leadership_bonus": 0.25,
    },
    {
        "name": "Digital Forensics Investigator",
        "description": "Collect and analyze digital evidence from compromised systems and devices. Great for detail-oriented investigators who enjoy solving puzzles.",
        "openness_weight": 0.6, "openness_ideal": 3.5,
        "conscientiousness_weight": 1.0, "conscientiousness_ideal": 5.0,
        "extraversion_weight": 0.3, "extraversion_ideal": 2.5,
        "agreeableness_weight": 0.4, "agreeableness_ideal": 3.0,
        "stability_weight": 0.7, "stability_ideal": 4.0,
        "min_years_preferred": 2, "leadership_bonus": 0.0,
    },
    {
        "name": "Cloud Security Architect",
        "description": "Design secure cloud infrastructure and ensure compliance across cloud environments. Perfect for forward-thinking architects who embrace new technologies.",
        "openness_weight": 0.9, "openness_ideal": 4.5,
        "conscientiousness_weight": 0.8, "conscientiousness_ideal": 4.5,
        "extraversion_weight": 0.5, "extraversion_ideal": 3.5,
        "agreeableness_weight": 0.5, "agreeableness_ideal": 3.5,
        "stability_weight": 0.6, "stability_ideal": 4.0,
        "min_years_preferred": 4, "leadership_bonus": 0.1,
    },
]


def seed_database():
    """Seed the database with questions and cyber roles."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_questions = db.query(Question).count()
        existing_roles = db.query(CyberRole).count()
        
        if existing_questions == 0:
            print("Seeding questions...")
            for q in QUESTIONS:
                question = Question(**q)
                db.add(question)
            db.commit()
            print(f"Added {len(QUESTIONS)} questions.")
        else:
            print(f"Questions already exist ({existing_questions} found). Skipping.")
        
        if existing_roles == 0:
            print("Seeding cyber roles...")
            for role_data in CYBER_ROLES:
                role = CyberRole(**role_data)
                db.add(role)
            db.commit()
            print(f"Added {len(CYBER_ROLES)} cyber roles.")
        else:
            print(f"Cyber roles already exist ({existing_roles} found). Skipping.")
        
        print("Database seeding complete!")
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
