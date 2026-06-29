from parser.pdf_parser import parse_pdf
from parser.docx_parser import parse_docx


def extract_resume(file_path, extension):
    if extension == 'pdf':
        return parse_pdf(file_path)
    if extension == 'docx':
        return parse_docx(file_path)
    raise ValueError('Unsupported file format')
