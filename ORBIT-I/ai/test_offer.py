from offer_generator import generate_offer

candidate = {
    "candidate_name": "Ali Khan",
    "domain": "Software Engineer",
    "salary": "120,000 PKR",
    "start_date": "1 August 2026"
}

result = generate_offer(candidate)
print(result)