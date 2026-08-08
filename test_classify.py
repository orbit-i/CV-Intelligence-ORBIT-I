import sys
sys.path.insert(0, 'ORBIT-I')
from classifier.domain_classifier import classify_resume

tests = {
    "Data Science": """
        Ahmed Ali - Data Scientist
        Skills: Python, R Programming, Machine Learning, Deep Learning, TensorFlow, PyTorch,
        Pandas, NumPy, Matplotlib, Seaborn, Scikit Learn, Statistical Analysis,
        Data Analysis, Data Visualization, Jupyter Notebook, Natural Language Processing,
        Neural Networks, Feature Engineering, Model Training, Regression, Classification,
        Clustering, Time Series, Data Wrangling, A B Testing, Tableau, Power BI,
        Predictive Modeling, Hypothesis Testing, EDA, Random Forest, XGBoost
        Experience: Developed and deployed ML models for customer churn prediction.
        Built data pipelines for real-time analytics. Conducted EDA on large datasets.
    """,

    "Software Engineering": """
        Sara Khan - Software Engineer
        Skills: Java, C++, C#, Spring Boot, REST API, Microservices,
        Object Oriented Programming, Design Patterns, Git, GitHub, Docker, Kubernetes,
        CI CD, Agile, Scrum, Unit Testing, Software Development Life Cycle,
        System Design, Algorithms, Data Structures, Linux, Jenkins, JIRA,
        Software Architecture, API Development, NET Framework, Backend Development,
        Code Review, Debugging, Refactoring, Version Control
        Experience: Designed and built scalable microservices. Led backend development
        for enterprise applications. Performed code reviews and system design sessions.
    """,

    "Cybersecurity": """
        Omar Farooq - Cybersecurity Analyst
        Skills: Ethical Hacking, Penetration Testing, Vulnerability Assessment,
        Network Security, Firewall, Intrusion Detection, SIEM, Malware Analysis,
        Incident Response, Threat Intelligence, Cryptography, Encryption, SSL TLS,
        VPN, Kali Linux, OWASP, Metasploit, Nmap, Burp Suite, Wireshark,
        Security Audit, Risk Assessment, Digital Forensics, CEH, CISSP,
        SOC Analyst, Reverse Engineering, Social Engineering
        Experience: Conducted penetration tests on enterprise networks.
        Led incident response for critical security breaches.
    """,

    "Web Development": """
        Zara Ahmed - Web Developer
        Skills: HTML, CSS, JavaScript, React, Angular, TypeScript,
        Bootstrap, Tailwind CSS, REST API, GraphQL, NodeJS,
        PHP, Laravel, WordPress, Webpack, Responsive Design,
        UI Development, Frontend, Backend, Full Stack,
        AJAX, JSON, DOM Manipulation, Web Performance,
        Progressive Web App, Sass, Next JS, SEO
        Experience: Built responsive SPAs using React. Developed full-stack
        web applications with Node.js and Laravel backends.
    """,

    "DevOps": """
        Bilal Hassan - DevOps Engineer
        Skills: Docker, Kubernetes, CI CD, Jenkins, GitLab CI,
        Ansible, Terraform, Infrastructure As Code, AWS, Azure,
        Google Cloud Platform, Cloud Computing, Monitoring, Prometheus,
        Grafana, ELK Stack, Load Balancing, Auto Scaling, Microservices,
        Container Orchestration, Site Reliability Engineering,
        Bash Scripting, Linux Administration, Nginx, Deployment Pipeline,
        Helm Charts, Service Mesh, Secrets Management
        Experience: Designed CI/CD pipelines. Managed Kubernetes clusters on AWS.
        Automated infrastructure provisioning using Terraform.
    """,

    "UI/UX Design": """
        Hina Malik - UI/UX Designer
        Skills: Figma, Adobe XD, Sketch, InVision, Prototyping,
        Wireframing, User Research, Usability Testing,
        Information Architecture, Interaction Design,
        Visual Design, Typography, Color Theory,
        Design Thinking, User Centered Design,
        Responsive Design, Accessibility, WCAG,
        Design Systems, Component Library,
        User Journey Mapping, Persona Creation, Zeplin, Adobe Illustrator,
        Motion Design, Micro Interactions, UX Writing
        Experience: Designed end-to-end UX for mobile and web apps.
        Conducted user research and usability testing sessions.
    """,
}

print("=" * 60)
print("  ORBIT-I CLASSIFICATION TEST RESULTS")
print("=" * 60)

passed = 0
failed = 0

for expected_domain, cv_text in tests.items():
    result = classify_resume(cv_text)
    predicted = result["predicted_domain"]
    confidence = result["confidence"]
    matched = result["matched_keywords"]
    status = result["status"]

    correct = predicted.lower().strip() == expected_domain.lower().strip()
    icon = "PASS" if correct else "FAIL"
    if correct:
        passed += 1
    else:
        failed += 1

    print(f"\n[{icon}] Expected : {expected_domain}")
    print(f"      Predicted: {predicted}")
    print(f"      Confidence: {confidence}%  |  Status: {status}")
    print(f"      Matched keywords ({len(matched)}): {', '.join(matched[:8])}{'...' if len(matched) > 8 else ''}")

print()
print("=" * 60)
print(f"  RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
print("=" * 60)
