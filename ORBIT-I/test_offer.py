import sys 
sys.path.insert(0, '.') 
from core.offer_generator import generate_offer 
result = generate_offer({'candidate_name': 'Test Candidate', 'domain': 'Software Engineering', 'position_title': 'Software Engineer', 'salary': 'PKR 100,000', 'company_name': 'iCompany Pakistan', 'hr_signatory': 'HR Department', 'probation_period': '3 months', 'location': 'Hybrid - Karachi, Pakistan'}) 
print(result) 
