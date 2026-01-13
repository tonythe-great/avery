"""
Career roadmap data for all 10 cybersecurity roles.
Contains certifications, skill translations, and action steps for Navy veterans.
"""

ROADMAPS = {
    # Role ID 1: SOC Analyst
    1: {
        "role_name": "Security Operations Center (SOC) Analyst",
        "quick_summary": "Entry-ready in 3-6 months with Security+",
        "estimated_months_to_entry": 4,
        "salary_entry": "$55,000 - $75,000",
        "salary_experienced": "$85,000 - $110,000",
        "job_outlook": "High demand with 35% growth projected. SOC roles are the most common entry point into cybersecurity.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Industry-standard baseline certification. Required by DoD for IAT Level II positions. Covers network security, threats, and risk management."
            },
            {
                "name": "Splunk Core Certified User",
                "provider": "Splunk",
                "level": "foundation",
                "estimated_weeks": 3,
                "cost_usd": 130,
                "url": "https://www.splunk.com/en_us/training/certification-track/splunk-core-certified-user.html",
                "description": "Learn the most widely-used SIEM platform. Essential for log analysis and alert investigation in SOC environments."
            },
            {
                "name": "CompTIA CySA+",
                "provider": "CompTIA",
                "level": "intermediate",
                "estimated_weeks": 10,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/cybersecurity-analyst",
                "description": "Cybersecurity Analyst certification focused on threat detection, analysis, and response. Natural progression after Security+."
            },
            {
                "name": "GIAC Security Essentials (GSEC)",
                "provider": "SANS/GIAC",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 2499,
                "url": "https://www.giac.org/certifications/security-essentials-gsec/",
                "description": "Highly respected hands-on certification. Demonstrates practical security skills valued by top employers."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Watch Standing",
                "military_context": "Your experience standing watch and monitoring systems during 24/7 operations directly applies to SOC work.",
                "cyber_skill": "24/7 Alert Monitoring & Triage",
                "transferability": 95
            },
            {
                "military_skill": "Incident Reporting",
                "military_context": "Writing SITREPs, casualty reports, and maintaining logs translates perfectly to security documentation.",
                "cyber_skill": "Security Incident Documentation",
                "transferability": 90
            },
            {
                "military_skill": "Operational Security",
                "military_context": "OPSEC awareness and protecting sensitive information is foundational to cybersecurity.",
                "cyber_skill": "Security Awareness & Threat Recognition",
                "transferability": 85
            },
            {
                "military_skill": "Communications Systems",
                "military_context": "Operating and troubleshooting military comm systems gives you network fundamentals.",
                "cyber_skill": "Network Traffic Analysis",
                "transferability": 75
            },
            {
                "military_skill": "Shift Work & Handoffs",
                "military_context": "Experience with watch rotations and proper turnover procedures is exactly how SOCs operate.",
                "cyber_skill": "Shift Transitions & Continuity",
                "transferability": 95
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-2",
                "title": "Foundation Building",
                "description": "Establish your baseline knowledge and start Security+ preparation.",
                "tasks": [
                    "Enroll in Security+ course (Professor Messer free videos or paid bootcamp)",
                    "Set up a home lab with VirtualBox and practice VMs",
                    "Join veteran cybersecurity communities (VetSec, Hiring Our Heroes)",
                    "Update LinkedIn with military-to-cyber career transition",
                    "Study 1-2 hours daily using flashcards and practice exams"
                ]
            },
            {
                "phase": "Month 3-4",
                "title": "Certification & Hands-On",
                "description": "Pass Security+ and gain practical SIEM experience.",
                "tasks": [
                    "Take and pass CompTIA Security+ exam",
                    "Complete Splunk free training and certification",
                    "Practice with TryHackMe SOC Level 1 path (free tier available)",
                    "Build 2-3 lab scenarios documenting your analysis process",
                    "Start applying to entry-level SOC positions"
                ]
            },
            {
                "phase": "Month 5-6",
                "title": "Job Search & Interview Prep",
                "description": "Actively pursue positions while continuing skill development.",
                "tasks": [
                    "Apply to 5-10 SOC Analyst positions weekly",
                    "Practice common SOC interview scenarios and technical questions",
                    "Leverage veteran hiring programs (Amazon, Microsoft, Cisco)",
                    "Attend virtual cybersecurity job fairs",
                    "Consider CySA+ if extending timeline for stronger positioning"
                ]
            },
            {
                "phase": "Month 7-12",
                "title": "Career Advancement",
                "description": "Once employed, focus on growth and specialization.",
                "tasks": [
                    "Master your organization's specific tools and processes",
                    "Pursue CySA+ or GSEC for advancement",
                    "Document interesting cases for your portfolio",
                    "Identify specialization interests (threat intel, incident response)",
                    "Mentor other transitioning veterans"
                ]
            }
        ]
    },

    # Role ID 2: Penetration Tester / Ethical Hacker
    2: {
        "role_name": "Penetration Tester / Ethical Hacker",
        "quick_summary": "Entry-ready in 6-12 months with hands-on practice",
        "estimated_months_to_entry": 9,
        "salary_entry": "$70,000 - $95,000",
        "salary_experienced": "$120,000 - $160,000",
        "job_outlook": "Growing demand with premium pay. Requires more preparation but offers higher ceiling and variety.",
        "certifications": [
            {
                "name": "CompTIA PenTest+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 10,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/pentest",
                "description": "Entry-level penetration testing certification. Good starting point before more advanced certs."
            },
            {
                "name": "eLearnSecurity Junior Penetration Tester (eJPT)",
                "provider": "INE Security",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 249,
                "url": "https://security.ine.com/certifications/ejpt-certification/",
                "description": "Practical, hands-on certification. Great for building real skills and demonstrating ability."
            },
            {
                "name": "Certified Ethical Hacker (CEH)",
                "provider": "EC-Council",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 1199,
                "url": "https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/",
                "description": "Well-known industry certification. Often required in job postings, especially government contracts."
            },
            {
                "name": "Offensive Security Certified Professional (OSCP)",
                "provider": "Offensive Security",
                "level": "advanced",
                "estimated_weeks": 16,
                "cost_usd": 1599,
                "url": "https://www.offsec.com/courses/pen-200/",
                "description": "Gold standard for penetration testers. 24-hour practical exam. Highly respected by employers."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Tactical Problem Solving",
                "military_context": "Finding creative solutions under pressure and adapting to changing situations is core to pen testing.",
                "cyber_skill": "Vulnerability Discovery & Exploitation",
                "transferability": 85
            },
            {
                "military_skill": "Mission Planning",
                "military_context": "Planning operations with clear objectives, phases, and contingencies mirrors pen test methodology.",
                "cyber_skill": "Engagement Planning & Scoping",
                "transferability": 90
            },
            {
                "military_skill": "Intelligence Analysis",
                "military_context": "Gathering and analyzing information to identify weaknesses is exactly what reconnaissance is.",
                "cyber_skill": "Reconnaissance & OSINT",
                "transferability": 85
            },
            {
                "military_skill": "Report Writing",
                "military_context": "Clear, actionable reporting is critical. Your military writing skills transfer directly.",
                "cyber_skill": "Penetration Test Reporting",
                "transferability": 80
            },
            {
                "military_skill": "Rules of Engagement",
                "military_context": "Understanding boundaries and operating within defined parameters is essential in authorized testing.",
                "cyber_skill": "Scope Compliance & Ethics",
                "transferability": 95
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-3",
                "title": "Foundation & Networking Basics",
                "description": "Build strong fundamentals before diving into offensive security.",
                "tasks": [
                    "Complete CompTIA Network+ or equivalent knowledge",
                    "Learn Linux command line thoroughly (OverTheWire Bandit)",
                    "Set up Kali Linux in a home lab environment",
                    "Complete TryHackMe Pre-Security and Introduction to Cyber paths",
                    "Study basic scripting (Python and Bash)"
                ]
            },
            {
                "phase": "Month 4-6",
                "title": "Hands-On Hacking Practice",
                "description": "Develop practical skills through deliberate practice.",
                "tasks": [
                    "Complete TryHackMe Jr Penetration Tester path",
                    "Practice on HackTheBox easy machines (20+ boxes)",
                    "Study for and pass eJPT or PenTest+",
                    "Document all practice in a portfolio/blog",
                    "Learn web application testing basics (OWASP Top 10)"
                ]
            },
            {
                "phase": "Month 7-9",
                "title": "Advanced Skills & Certification",
                "description": "Pursue recognized certification and deepen expertise.",
                "tasks": [
                    "Enroll in OSCP or CEH based on career goals",
                    "Complete 50+ HackTheBox/Proving Grounds machines",
                    "Participate in CTF competitions",
                    "Build a professional portfolio website",
                    "Network at security conferences (virtual or in-person)"
                ]
            },
            {
                "phase": "Month 10-12",
                "title": "Job Search & Specialization",
                "description": "Enter the job market and identify your niche.",
                "tasks": [
                    "Apply to junior pen tester and security consultant roles",
                    "Leverage bug bounty platforms for real-world experience",
                    "Consider specialization (web apps, network, mobile, cloud)",
                    "Prepare for technical interviews with practice scenarios",
                    "Target companies with veteran hiring programs"
                ]
            }
        ]
    },

    # Role ID 3: Incident Response Specialist
    3: {
        "role_name": "Incident Response Specialist",
        "quick_summary": "Entry-ready in 4-8 months, leadership experience valued",
        "estimated_months_to_entry": 6,
        "salary_entry": "$65,000 - $90,000",
        "salary_experienced": "$100,000 - $140,000",
        "job_outlook": "Critical role with consistent demand. Your military crisis management experience is highly valued.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Essential baseline certification. Foundation for all incident response work."
            },
            {
                "name": "CompTIA CySA+",
                "provider": "CompTIA",
                "level": "intermediate",
                "estimated_weeks": 10,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/cybersecurity-analyst",
                "description": "Focuses on threat detection and response. Directly applicable to IR work."
            },
            {
                "name": "GIAC Certified Incident Handler (GCIH)",
                "provider": "SANS/GIAC",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 2499,
                "url": "https://www.giac.org/certifications/certified-incident-handler-gcih/",
                "description": "Premier incident handling certification. Covers attack techniques and response procedures."
            },
            {
                "name": "EC-Council Certified Incident Handler (ECIH)",
                "provider": "EC-Council",
                "level": "intermediate",
                "estimated_weeks": 8,
                "cost_usd": 999,
                "url": "https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/",
                "description": "More affordable alternative to GCIH. Covers IR lifecycle and procedures."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Crisis Management",
                "military_context": "Leading responses to emergencies, casualties, or security incidents is directly applicable.",
                "cyber_skill": "Incident Command & Coordination",
                "transferability": 95
            },
            {
                "military_skill": "Damage Control",
                "military_context": "Containing and mitigating damage while maintaining operations mirrors cyber IR.",
                "cyber_skill": "Containment & Eradication",
                "transferability": 90
            },
            {
                "military_skill": "After Action Reports",
                "military_context": "Conducting post-incident analysis and documenting lessons learned is identical.",
                "cyber_skill": "Post-Incident Analysis & Reporting",
                "transferability": 95
            },
            {
                "military_skill": "Chain of Command Communication",
                "military_context": "Escalating issues and briefing leadership under pressure is essential in IR.",
                "cyber_skill": "Stakeholder Communication",
                "transferability": 90
            },
            {
                "military_skill": "Evidence Handling",
                "military_context": "Maintaining chain of custody and preserving evidence applies directly to digital forensics.",
                "cyber_skill": "Digital Evidence Preservation",
                "transferability": 85
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-2",
                "title": "Foundation & Framework Study",
                "description": "Build baseline knowledge and understand IR frameworks.",
                "tasks": [
                    "Complete Security+ certification",
                    "Study NIST Incident Response framework (SP 800-61)",
                    "Learn common attack types and indicators of compromise",
                    "Set up a home lab for malware analysis basics",
                    "Join incident response communities and forums"
                ]
            },
            {
                "phase": "Month 3-4",
                "title": "Hands-On Response Skills",
                "description": "Develop practical incident handling capabilities.",
                "tasks": [
                    "Practice with SANS incident response scenarios",
                    "Learn log analysis with Splunk or ELK stack",
                    "Study memory forensics basics (Volatility)",
                    "Complete Blue Team Labs Online exercises",
                    "Document your IR processes and playbooks"
                ]
            },
            {
                "phase": "Month 5-6",
                "title": "Certification & Job Search",
                "description": "Get certified and enter the job market.",
                "tasks": [
                    "Pass CySA+ or begin GCIH preparation",
                    "Apply to IR and SOC positions (IR often hires from SOC)",
                    "Highlight leadership experience in applications",
                    "Practice incident response interview scenarios",
                    "Target MSSPs and large enterprises with IR teams"
                ]
            },
            {
                "phase": "Month 7-12",
                "title": "Advancement & Specialization",
                "description": "Grow into senior roles and develop expertise.",
                "tasks": [
                    "Pursue GCIH or equivalent advanced certification",
                    "Develop expertise in specific attack types",
                    "Build relationships with threat intel and forensics teams",
                    "Consider IR team lead or manager track",
                    "Contribute to IR playbook development"
                ]
            }
        ]
    },

    # Role ID 4: Security Engineer
    4: {
        "role_name": "Security Engineer",
        "quick_summary": "Entry-ready in 6-9 months with technical foundation",
        "estimated_months_to_entry": 7,
        "salary_entry": "$80,000 - $105,000",
        "salary_experienced": "$130,000 - $170,000",
        "job_outlook": "High demand for builders who can implement security solutions. Strong growth trajectory.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Baseline security certification. Starting point for security engineering path."
            },
            {
                "name": "AWS Certified Security - Specialty",
                "provider": "Amazon Web Services",
                "level": "intermediate",
                "estimated_weeks": 10,
                "cost_usd": 300,
                "url": "https://aws.amazon.com/certification/certified-security-specialty/",
                "description": "Cloud security focus. Highly valued as organizations migrate to AWS."
            },
            {
                "name": "Certified Information Systems Security Professional (CISSP)",
                "provider": "ISC2",
                "level": "advanced",
                "estimated_weeks": 16,
                "cost_usd": 749,
                "url": "https://www.isc2.org/certifications/cissp",
                "description": "Gold standard management certification. Requires 5 years experience (1 year waived with degree)."
            },
            {
                "name": "Certified Cloud Security Professional (CCSP)",
                "provider": "ISC2",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 599,
                "url": "https://www.isc2.org/certifications/ccsp",
                "description": "Cloud-focused security certification. Great complement to hands-on cloud skills."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Systems Administration",
                "military_context": "Managing and hardening military IT systems translates directly to security engineering.",
                "cyber_skill": "Security Architecture & Hardening",
                "transferability": 90
            },
            {
                "military_skill": "Equipment Maintenance",
                "military_context": "Maintaining complex systems with strict procedures applies to security tool management.",
                "cyber_skill": "Security Tool Administration",
                "transferability": 80
            },
            {
                "military_skill": "Technical Documentation",
                "military_context": "Creating and maintaining technical procedures and configurations is essential.",
                "cyber_skill": "Security Documentation & Procedures",
                "transferability": 85
            },
            {
                "military_skill": "Troubleshooting",
                "military_context": "Systematic problem-solving and root cause analysis are core engineering skills.",
                "cyber_skill": "Security Issue Diagnosis",
                "transferability": 85
            },
            {
                "military_skill": "Network Operations",
                "military_context": "Understanding network architecture and protocols is foundational.",
                "cyber_skill": "Network Security Design",
                "transferability": 80
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-3",
                "title": "Technical Foundation",
                "description": "Build strong systems and networking fundamentals.",
                "tasks": [
                    "Complete Security+ certification",
                    "Learn Linux system administration deeply",
                    "Study networking (consider CCNA or Network+)",
                    "Learn scripting (Python, Bash, PowerShell)",
                    "Set up home lab with firewalls, IDS/IPS"
                ]
            },
            {
                "phase": "Month 4-6",
                "title": "Security Tools & Cloud",
                "description": "Gain hands-on experience with security technologies.",
                "tasks": [
                    "Deploy and configure security tools (firewalls, SIEM, EDR)",
                    "Complete AWS Cloud Practitioner and start Security Specialty",
                    "Learn infrastructure as code (Terraform, Ansible)",
                    "Practice hardening systems (CIS Benchmarks)",
                    "Build security automation scripts"
                ]
            },
            {
                "phase": "Month 7-9",
                "title": "Specialization & Job Search",
                "description": "Focus expertise and enter the job market.",
                "tasks": [
                    "Complete cloud security certification",
                    "Build portfolio of security projects on GitHub",
                    "Apply to security engineer positions",
                    "Target cloud-focused companies and DoD contractors",
                    "Practice technical interviews and whiteboarding"
                ]
            },
            {
                "phase": "Month 10-12",
                "title": "Career Growth",
                "description": "Advance skills and work toward senior roles.",
                "tasks": [
                    "Master your organization's security stack",
                    "Begin CISSP preparation (if experience qualifies)",
                    "Contribute to open source security projects",
                    "Develop DevSecOps and automation expertise",
                    "Mentor junior team members"
                ]
            }
        ]
    },

    # Role ID 5: Cybersecurity Consultant
    5: {
        "role_name": "Cybersecurity Consultant",
        "quick_summary": "Entry-ready in 6-12 months, communication skills key",
        "estimated_months_to_entry": 8,
        "salary_entry": "$75,000 - $100,000",
        "salary_experienced": "$130,000 - $180,000",
        "job_outlook": "Strong demand for advisors who bridge technical and business. Travel often required.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Essential baseline. Required for many consulting engagements."
            },
            {
                "name": "Certified Information Security Manager (CISM)",
                "provider": "ISACA",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 760,
                "url": "https://www.isaca.org/credentialing/cism",
                "description": "Management-focused certification. Great for consulting and advisory roles."
            },
            {
                "name": "Certified Information Systems Auditor (CISA)",
                "provider": "ISACA",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 760,
                "url": "https://www.isaca.org/credentialing/cisa",
                "description": "Audit-focused certification. Valuable for compliance consulting."
            },
            {
                "name": "CISSP",
                "provider": "ISC2",
                "level": "advanced",
                "estimated_weeks": 16,
                "cost_usd": 749,
                "url": "https://www.isc2.org/certifications/cissp",
                "description": "Industry gold standard. Opens doors to senior consulting roles."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Briefing Leadership",
                "military_context": "Presenting complex information to commanders and stakeholders is core consulting.",
                "cyber_skill": "Executive Communication",
                "transferability": 95
            },
            {
                "military_skill": "Risk Assessment",
                "military_context": "Evaluating threats and recommending mitigations is exactly what consultants do.",
                "cyber_skill": "Security Risk Assessment",
                "transferability": 90
            },
            {
                "military_skill": "Policy Development",
                "military_context": "Creating and implementing policies and procedures translates directly.",
                "cyber_skill": "Security Policy Advisory",
                "transferability": 85
            },
            {
                "military_skill": "Cross-functional Coordination",
                "military_context": "Working across departments and commands mirrors client engagement.",
                "cyber_skill": "Stakeholder Management",
                "transferability": 90
            },
            {
                "military_skill": "Compliance & Inspections",
                "military_context": "Preparing for and conducting inspections applies to security audits.",
                "cyber_skill": "Compliance Assessment",
                "transferability": 85
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-3",
                "title": "Foundation & Frameworks",
                "description": "Build technical baseline and learn key frameworks.",
                "tasks": [
                    "Complete Security+ certification",
                    "Study major frameworks (NIST CSF, ISO 27001, CIS Controls)",
                    "Learn compliance requirements (HIPAA, PCI-DSS, SOC 2)",
                    "Develop presentation and communication skills",
                    "Start building professional network"
                ]
            },
            {
                "phase": "Month 4-6",
                "title": "Governance & Risk Management",
                "description": "Develop advisory and assessment skills.",
                "tasks": [
                    "Study for CISM or CISA certification",
                    "Learn risk assessment methodologies",
                    "Practice writing executive summaries and recommendations",
                    "Shadow consultants or watch consulting case studies",
                    "Develop expertise in 1-2 industry verticals"
                ]
            },
            {
                "phase": "Month 7-9",
                "title": "Certification & Job Search",
                "description": "Get certified and target consulting roles.",
                "tasks": [
                    "Pass CISM, CISA, or equivalent certification",
                    "Apply to consulting firms (Big 4, boutique security firms)",
                    "Prepare case study presentations for interviews",
                    "Leverage military network for referrals",
                    "Consider GRC analyst roles as stepping stone"
                ]
            },
            {
                "phase": "Month 10-12",
                "title": "Client Engagement & Growth",
                "description": "Build client experience and advance career.",
                "tasks": [
                    "Develop deep expertise in specific frameworks",
                    "Build client relationships and delivery skills",
                    "Work toward CISSP for senior roles",
                    "Consider industry specialization (healthcare, finance, government)",
                    "Develop thought leadership through writing or speaking"
                ]
            }
        ]
    },

    # Role ID 6: Threat Intelligence Analyst
    6: {
        "role_name": "Threat Intelligence Analyst",
        "quick_summary": "Entry-ready in 4-8 months, analytical mindset essential",
        "estimated_months_to_entry": 6,
        "salary_entry": "$65,000 - $90,000",
        "salary_experienced": "$100,000 - $140,000",
        "job_outlook": "Growing field as organizations prioritize proactive threat awareness. Intelligence background highly valued.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Baseline security knowledge required for threat intel work."
            },
            {
                "name": "GIAC Cyber Threat Intelligence (GCTI)",
                "provider": "SANS/GIAC",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 2499,
                "url": "https://www.giac.org/certifications/cyber-threat-intelligence-gcti/",
                "description": "Premier threat intelligence certification. Covers strategic, operational, and tactical intel."
            },
            {
                "name": "Certified Threat Intelligence Analyst (CTIA)",
                "provider": "EC-Council",
                "level": "intermediate",
                "estimated_weeks": 8,
                "cost_usd": 999,
                "url": "https://www.eccouncil.org/train-certify/certified-threat-intelligence-analyst-ctia/",
                "description": "Affordable alternative covering threat intel lifecycle and methodologies."
            },
            {
                "name": "MITRE ATT&CK Defender (MAD)",
                "provider": "MITRE",
                "level": "foundation",
                "estimated_weeks": 4,
                "cost_usd": 0,
                "url": "https://attack.mitre.org/resources/training/",
                "description": "Free training on the industry-standard ATT&CK framework. Essential knowledge."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Intelligence Analysis",
                "military_context": "Your military intel training directly applies to cyber threat analysis.",
                "cyber_skill": "Threat Actor Analysis",
                "transferability": 95
            },
            {
                "military_skill": "OSINT Collection",
                "military_context": "Open source intelligence gathering is identical in cyber threat intel.",
                "cyber_skill": "Cyber OSINT",
                "transferability": 95
            },
            {
                "military_skill": "Intelligence Briefings",
                "military_context": "Delivering actionable intel to decision-makers is the core deliverable.",
                "cyber_skill": "Threat Intelligence Reporting",
                "transferability": 90
            },
            {
                "military_skill": "Pattern Recognition",
                "military_context": "Identifying trends and connecting disparate information is essential.",
                "cyber_skill": "Threat Pattern Analysis",
                "transferability": 90
            },
            {
                "military_skill": "Classification Handling",
                "military_context": "Managing sensitive information and need-to-know applies to threat intel sharing.",
                "cyber_skill": "Intelligence Sharing & TLP",
                "transferability": 85
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-2",
                "title": "Foundation & Frameworks",
                "description": "Build security baseline and learn intel frameworks.",
                "tasks": [
                    "Complete Security+ certification",
                    "Study MITRE ATT&CK framework thoroughly",
                    "Learn threat intel platforms (MISP, OpenCTI)",
                    "Understand the Cyber Kill Chain and Diamond Model",
                    "Follow threat intel researchers and reports"
                ]
            },
            {
                "phase": "Month 3-4",
                "title": "Practical Analysis Skills",
                "description": "Develop hands-on threat analysis capabilities.",
                "tasks": [
                    "Practice malware analysis basics",
                    "Learn to pivot on IOCs using tools like VirusTotal, Shodan",
                    "Complete MITRE ATT&CK Defender training",
                    "Write practice threat reports on current campaigns",
                    "Build a personal intel collection workflow"
                ]
            },
            {
                "phase": "Month 5-6",
                "title": "Certification & Job Search",
                "description": "Get certified and enter the field.",
                "tasks": [
                    "Pursue CTIA or begin GCTI preparation",
                    "Apply to threat intel and SOC analyst positions",
                    "Highlight military intel experience prominently",
                    "Target government contractors and financial sector",
                    "Build portfolio of threat analysis samples"
                ]
            },
            {
                "phase": "Month 7-12",
                "title": "Specialization & Growth",
                "description": "Develop expertise and advance career.",
                "tasks": [
                    "Complete GCTI for career advancement",
                    "Develop expertise in specific threat actors or regions",
                    "Contribute to threat intel sharing communities",
                    "Consider specialization (APT tracking, dark web, geopolitical)",
                    "Build relationships with ISAC communities"
                ]
            }
        ]
    },

    # Role ID 7: Security Awareness Training Specialist
    7: {
        "role_name": "Security Awareness Training Specialist",
        "quick_summary": "Entry-ready in 3-6 months, instructor experience valued",
        "estimated_months_to_entry": 4,
        "salary_entry": "$55,000 - $75,000",
        "salary_experienced": "$80,000 - $110,000",
        "job_outlook": "Steady demand as human factor remains top security risk. Great for those who enjoy teaching.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Baseline security knowledge to credibly teach security topics."
            },
            {
                "name": "Certified Security Awareness Practitioner (CSAP)",
                "provider": "H Layer",
                "level": "foundation",
                "estimated_weeks": 4,
                "cost_usd": 495,
                "url": "https://www.yourlearningcredentials.com/csap",
                "description": "Focused certification for security awareness professionals."
            },
            {
                "name": "SANS Security Awareness Professional (SSAP)",
                "provider": "SANS",
                "level": "intermediate",
                "estimated_weeks": 6,
                "cost_usd": 2100,
                "url": "https://www.sans.org/security-awareness-training/career-development/credential/",
                "description": "Premium certification from SANS. Strong credential for the field."
            },
            {
                "name": "Certified Information Security Manager (CISM)",
                "provider": "ISACA",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 760,
                "url": "https://www.isaca.org/credentialing/cism",
                "description": "Broader security management certification. Good for program leadership."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Training & Instruction",
                "military_context": "Your experience as an instructor or training petty officer transfers perfectly.",
                "cyber_skill": "Security Training Delivery",
                "transferability": 95
            },
            {
                "military_skill": "Curriculum Development",
                "military_context": "Creating training materials and lesson plans is directly applicable.",
                "cyber_skill": "Awareness Program Development",
                "transferability": 90
            },
            {
                "military_skill": "Public Speaking",
                "military_context": "Briefing groups and presenting information engagingly is essential.",
                "cyber_skill": "Training Presentation",
                "transferability": 90
            },
            {
                "military_skill": "Evaluating Readiness",
                "military_context": "Assessing personnel readiness through drills and tests applies to phishing simulations.",
                "cyber_skill": "Security Awareness Assessment",
                "transferability": 85
            },
            {
                "military_skill": "Mentoring",
                "military_context": "Coaching and developing others is core to security awareness work.",
                "cyber_skill": "Security Culture Development",
                "transferability": 85
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-2",
                "title": "Security Foundation",
                "description": "Build credible security knowledge base.",
                "tasks": [
                    "Complete Security+ certification",
                    "Study common attack vectors (phishing, social engineering)",
                    "Learn about security awareness platforms (KnowBe4, Proofpoint)",
                    "Research adult learning principles",
                    "Review industry awareness program benchmarks"
                ]
            },
            {
                "phase": "Month 3-4",
                "title": "Content Development & Certification",
                "description": "Create training materials and get certified.",
                "tasks": [
                    "Pursue CSAP or equivalent certification",
                    "Develop sample training presentations",
                    "Create engaging content (videos, quizzes, scenarios)",
                    "Practice phishing simulation concepts",
                    "Build portfolio of training materials"
                ]
            },
            {
                "phase": "Month 5-6",
                "title": "Job Search & Program Experience",
                "description": "Enter the field and gain program experience.",
                "tasks": [
                    "Apply to security awareness and training positions",
                    "Target large enterprises with dedicated programs",
                    "Highlight instructor and training experience",
                    "Offer to help with awareness programs as volunteer",
                    "Network with security awareness community"
                ]
            },
            {
                "phase": "Month 7-12",
                "title": "Program Leadership",
                "description": "Advance to program ownership and leadership.",
                "tasks": [
                    "Develop metrics-driven program improvements",
                    "Pursue SSAP for advanced credential",
                    "Build executive presentation skills",
                    "Consider CISM for program management roles",
                    "Speak at security awareness conferences"
                ]
            }
        ]
    },

    # Role ID 8: CISO
    8: {
        "role_name": "Chief Information Security Officer (CISO)",
        "quick_summary": "Executive role requiring 8-15 years total journey",
        "estimated_months_to_entry": 120,
        "salary_entry": "$150,000 - $200,000",
        "salary_experienced": "$250,000 - $400,000",
        "job_outlook": "Top of the security career ladder. Requires extensive experience but rewards with significant compensation.",
        "certifications": [
            {
                "name": "Certified Information Systems Security Professional (CISSP)",
                "provider": "ISC2",
                "level": "advanced",
                "estimated_weeks": 16,
                "cost_usd": 749,
                "url": "https://www.isc2.org/certifications/cissp",
                "description": "Essential certification for security leadership. Requires 5 years experience."
            },
            {
                "name": "Certified Information Security Manager (CISM)",
                "provider": "ISACA",
                "level": "advanced",
                "estimated_weeks": 12,
                "cost_usd": 760,
                "url": "https://www.isaca.org/credentialing/cism",
                "description": "Management-focused certification. Demonstrates governance and leadership ability."
            },
            {
                "name": "Certified in Risk and Information Systems Control (CRISC)",
                "provider": "ISACA",
                "level": "advanced",
                "estimated_weeks": 12,
                "cost_usd": 760,
                "url": "https://www.isaca.org/credentialing/crisc",
                "description": "Risk management focus. Essential for board-level risk discussions."
            },
            {
                "name": "MBA or MS Cybersecurity",
                "provider": "Various Universities",
                "level": "advanced",
                "estimated_weeks": 104,
                "cost_usd": 50000,
                "url": "https://www.usnews.com/education/online-education/cybersecurity-masters-degree",
                "description": "Graduate degree demonstrates commitment and business acumen. Many programs offer veteran benefits."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Command Leadership",
                "military_context": "Leading organizations and being accountable for mission success is exactly what CISOs do.",
                "cyber_skill": "Security Program Leadership",
                "transferability": 95
            },
            {
                "military_skill": "Strategic Planning",
                "military_context": "Developing and executing long-term strategies aligns with security roadmap development.",
                "cyber_skill": "Security Strategy Development",
                "transferability": 90
            },
            {
                "military_skill": "Budget Management",
                "military_context": "Managing resources and justifying expenditures is a core CISO responsibility.",
                "cyber_skill": "Security Budget Management",
                "transferability": 85
            },
            {
                "military_skill": "Stakeholder Management",
                "military_context": "Working with senior leadership and external partners is daily CISO work.",
                "cyber_skill": "Executive & Board Communication",
                "transferability": 90
            },
            {
                "military_skill": "Risk-Based Decision Making",
                "military_context": "Making decisions under uncertainty with imperfect information is the CISO's constant challenge.",
                "cyber_skill": "Enterprise Risk Management",
                "transferability": 90
            }
        ],
        "action_steps": [
            {
                "phase": "Years 1-3",
                "title": "Technical Foundation",
                "description": "Build deep technical expertise as a security practitioner.",
                "tasks": [
                    "Start in SOC Analyst, Security Engineer, or similar role",
                    "Complete Security+, then CySA+ or equivalent",
                    "Gain hands-on experience with security operations",
                    "Develop breadth across multiple security domains",
                    "Begin building professional network"
                ]
            },
            {
                "phase": "Years 4-6",
                "title": "Leadership Development",
                "description": "Transition to team lead and management roles.",
                "tasks": [
                    "Move into senior individual contributor or team lead role",
                    "Complete CISSP certification",
                    "Begin CISM preparation",
                    "Develop people management skills",
                    "Consider MBA or MS Cybersecurity program"
                ]
            },
            {
                "phase": "Years 7-10",
                "title": "Security Management",
                "description": "Lead security teams and programs.",
                "tasks": [
                    "Achieve Security Manager or Director position",
                    "Complete CISM and CRISC certifications",
                    "Develop board and executive communication skills",
                    "Build vendor and partner relationships",
                    "Lead significant security initiatives"
                ]
            },
            {
                "phase": "Years 10+",
                "title": "Executive Leadership",
                "description": "Transition to CISO or equivalent role.",
                "tasks": [
                    "Target VP of Security or Deputy CISO roles",
                    "Develop business acumen and financial skills",
                    "Build external reputation through speaking and writing",
                    "Network with other CISOs and executives",
                    "Prepare for board-level presentations and accountability"
                ]
            }
        ]
    },

    # Role ID 9: Digital Forensics Investigator
    9: {
        "role_name": "Digital Forensics Investigator",
        "quick_summary": "Entry-ready in 6-9 months, detail orientation critical",
        "estimated_months_to_entry": 7,
        "salary_entry": "$60,000 - $85,000",
        "salary_experienced": "$95,000 - $130,000",
        "job_outlook": "Consistent demand in law enforcement, corporate, and consulting. Methodical investigators valued.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Baseline security certification. Foundation for forensics work."
            },
            {
                "name": "GIAC Certified Forensic Examiner (GCFE)",
                "provider": "SANS/GIAC",
                "level": "intermediate",
                "estimated_weeks": 12,
                "cost_usd": 2499,
                "url": "https://www.giac.org/certifications/certified-forensic-examiner-gcfe/",
                "description": "Premier Windows forensics certification. Highly respected in the field."
            },
            {
                "name": "EnCase Certified Examiner (EnCE)",
                "provider": "OpenText",
                "level": "intermediate",
                "estimated_weeks": 8,
                "cost_usd": 750,
                "url": "https://www.opentext.com/products/training-and-certification",
                "description": "Certification for the widely-used EnCase forensics tool."
            },
            {
                "name": "Certified Forensic Computer Examiner (CFCE)",
                "provider": "IACIS",
                "level": "advanced",
                "estimated_weeks": 16,
                "cost_usd": 1500,
                "url": "https://www.iacis.com/certification/",
                "description": "Rigorous law enforcement focused certification. Gold standard for legal proceedings."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Investigation Experience",
                "military_context": "Any investigation experience (NCIS support, command investigations) directly applies.",
                "cyber_skill": "Digital Evidence Investigation",
                "transferability": 90
            },
            {
                "military_skill": "Evidence Handling",
                "military_context": "Maintaining chain of custody and documenting evidence is identical.",
                "cyber_skill": "Digital Chain of Custody",
                "transferability": 95
            },
            {
                "military_skill": "Attention to Detail",
                "military_context": "Meticulous documentation and procedure following is critical in forensics.",
                "cyber_skill": "Forensic Documentation",
                "transferability": 90
            },
            {
                "military_skill": "Report Writing",
                "military_context": "Creating detailed, accurate reports that withstand scrutiny applies directly.",
                "cyber_skill": "Forensic Report Writing",
                "transferability": 85
            },
            {
                "military_skill": "Technical Troubleshooting",
                "military_context": "Systematic problem-solving helps in artifact analysis and data recovery.",
                "cyber_skill": "Forensic Analysis",
                "transferability": 80
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-3",
                "title": "Foundation & Tools",
                "description": "Build security baseline and learn forensic fundamentals.",
                "tasks": [
                    "Complete Security+ certification",
                    "Learn forensic concepts (imaging, hashing, chain of custody)",
                    "Set up forensics lab with Autopsy and FTK Imager (free tools)",
                    "Study file systems (NTFS, ext4, APFS)",
                    "Practice with forensic challenge images (DFIR training resources)"
                ]
            },
            {
                "phase": "Month 4-6",
                "title": "Hands-On Forensics",
                "description": "Develop practical forensic analysis skills.",
                "tasks": [
                    "Complete forensic CTF challenges",
                    "Learn Windows artifact analysis (registry, event logs, prefetch)",
                    "Study memory forensics with Volatility",
                    "Practice writing forensic reports",
                    "Learn about legal requirements and court testimony"
                ]
            },
            {
                "phase": "Month 7-9",
                "title": "Certification & Job Search",
                "description": "Get certified and enter the field.",
                "tasks": [
                    "Pursue GCFE, EnCE, or equivalent certification",
                    "Apply to corporate forensics, consulting, and government roles",
                    "Target law enforcement support positions if interested",
                    "Highlight investigation and evidence experience",
                    "Prepare for scenario-based interviews"
                ]
            },
            {
                "phase": "Month 10-12",
                "title": "Specialization & Advancement",
                "description": "Develop expertise and advance career.",
                "tasks": [
                    "Specialize (mobile forensics, malware analysis, incident response)",
                    "Pursue CFCE for law enforcement track",
                    "Develop expertise in specific platforms or artifacts",
                    "Consider expert witness preparation training",
                    "Network with forensics community (HTCIA, IACIS)"
                ]
            }
        ]
    },

    # Role ID 10: Cloud Security Architect
    10: {
        "role_name": "Cloud Security Architect",
        "quick_summary": "Entry-ready in 9-15 months, cloud experience required",
        "estimated_months_to_entry": 12,
        "salary_entry": "$100,000 - $130,000",
        "salary_experienced": "$160,000 - $220,000",
        "job_outlook": "High growth as cloud adoption accelerates. Premium compensation for cloud security expertise.",
        "certifications": [
            {
                "name": "CompTIA Security+",
                "provider": "CompTIA",
                "level": "foundation",
                "estimated_weeks": 8,
                "cost_usd": 392,
                "url": "https://www.comptia.org/certifications/security",
                "description": "Baseline security certification before cloud specialization."
            },
            {
                "name": "AWS Certified Security - Specialty",
                "provider": "Amazon Web Services",
                "level": "intermediate",
                "estimated_weeks": 10,
                "cost_usd": 300,
                "url": "https://aws.amazon.com/certification/certified-security-specialty/",
                "description": "Deep dive into AWS security services and architecture."
            },
            {
                "name": "Certified Cloud Security Professional (CCSP)",
                "provider": "ISC2",
                "level": "advanced",
                "estimated_weeks": 12,
                "cost_usd": 599,
                "url": "https://www.isc2.org/certifications/ccsp",
                "description": "Vendor-neutral cloud security certification. Covers all major platforms."
            },
            {
                "name": "Google Professional Cloud Security Engineer",
                "provider": "Google Cloud",
                "level": "intermediate",
                "estimated_weeks": 10,
                "cost_usd": 300,
                "url": "https://cloud.google.com/learn/certification/cloud-security-engineer",
                "description": "GCP-focused security certification. Valuable for multi-cloud environments."
            }
        ],
        "skill_translations": [
            {
                "military_skill": "Systems Architecture",
                "military_context": "Designing and maintaining complex systems applies to cloud architecture.",
                "cyber_skill": "Cloud Security Architecture",
                "transferability": 85
            },
            {
                "military_skill": "Network Security",
                "military_context": "Understanding network segmentation and access control applies to cloud VPCs.",
                "cyber_skill": "Cloud Network Security",
                "transferability": 80
            },
            {
                "military_skill": "Access Control",
                "military_context": "Managing clearances and need-to-know applies to IAM and least privilege.",
                "cyber_skill": "Cloud Identity & Access Management",
                "transferability": 85
            },
            {
                "military_skill": "Compliance",
                "military_context": "Understanding regulatory requirements applies to cloud compliance (FedRAMP, etc.).",
                "cyber_skill": "Cloud Compliance & Governance",
                "transferability": 85
            },
            {
                "military_skill": "Technical Documentation",
                "military_context": "Creating architecture documents and procedures is essential.",
                "cyber_skill": "Cloud Security Documentation",
                "transferability": 80
            }
        ],
        "action_steps": [
            {
                "phase": "Month 1-4",
                "title": "Cloud & Security Foundation",
                "description": "Build combined cloud and security fundamentals.",
                "tasks": [
                    "Complete Security+ certification",
                    "Complete AWS Cloud Practitioner or Azure Fundamentals",
                    "Learn cloud networking concepts (VPCs, subnets, security groups)",
                    "Understand shared responsibility model",
                    "Set up personal cloud lab environment"
                ]
            },
            {
                "phase": "Month 5-8",
                "title": "Cloud Security Deep Dive",
                "description": "Develop hands-on cloud security skills.",
                "tasks": [
                    "Complete AWS Solutions Architect Associate",
                    "Begin AWS Security Specialty preparation",
                    "Learn infrastructure as code (Terraform, CloudFormation)",
                    "Practice cloud security configurations and hardening",
                    "Study cloud security frameworks (CSA CCM, CIS Benchmarks)"
                ]
            },
            {
                "phase": "Month 9-12",
                "title": "Certification & Positioning",
                "description": "Get certified and prepare for architect roles.",
                "tasks": [
                    "Complete AWS Security Specialty certification",
                    "Begin CCSP preparation for vendor-neutral credential",
                    "Apply to cloud security engineer positions",
                    "Build portfolio of cloud security projects",
                    "Target cloud-native companies and DoD cloud migrations"
                ]
            },
            {
                "phase": "Month 13-18",
                "title": "Architecture & Leadership",
                "description": "Advance to architect level roles.",
                "tasks": [
                    "Complete CCSP certification",
                    "Develop multi-cloud expertise (AWS + Azure or GCP)",
                    "Lead cloud security design reviews",
                    "Build expertise in cloud-native security (containers, serverless)",
                    "Consider solutions architect or principal engineer track"
                ]
            }
        ]
    }
}


def get_roadmap(role_id: int) -> dict:
    """Get roadmap data for a specific role."""
    return ROADMAPS.get(role_id)


def get_all_roadmaps() -> dict:
    """Get all roadmap data."""
    return ROADMAPS
