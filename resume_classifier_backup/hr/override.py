from flask import render_template
from hr.models import candidate

def review_candidate():
    return render_template(
        "hr_review.html",
        candidate=candidate
    )
    
