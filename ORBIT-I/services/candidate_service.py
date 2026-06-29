from ai.domain_classifier import classify_domain
from parser.extractor import extract_resume


def process_candidate(file_path, extension):
    resume_data = extract_resume(file_path, extension)
    return classify_domain(resume_data)
