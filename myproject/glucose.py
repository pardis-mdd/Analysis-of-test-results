import fitz
import easyocr
import re

# Function to interpret glucose levels
def interpret_glucose(glucose):
    glucose = float(glucose)
    if glucose < 100:
        return "ایده‌آل: قند خون شما در محدوده ایده‌آل است (70 – 100 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "بالا: سطح قند خون شما بالا است (> 100 میلی‌گرم بر دسی‌لیتر)"
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_text(text):
    cleaned_text = text.replace('is', '')
    match = re.search(r'\d+', cleaned_text)
    if match:
        return match.group(0)
    return ''

def extract_keyword_values(file_path):
    if file_path.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
        extracted_lines = extracted_text.splitlines()
    else:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(file_path)
        extracted_text = '\n'.join([entry[1] for entry in result])
        extracted_lines = extracted_text.splitlines()

    extracted_lines = [line.lower() for line in extracted_lines]

    keyword_values = {}
    keywords = ["glucose"]  

    l = list(enumerate(extracted_lines))

    for keyword in keywords:
        for i, (line_num, line) in enumerate(l):
            if keyword in line:
                if i + 1 < len(l):
                    next_line_num, next_line = l[i + 1]
                    if any(char.isdigit() for char in next_line):
                        keyword_values[keyword] = next_line
                        break
                if i + 2 < len(l):
                    next_line_num, next_line = l[i + 2]
                    if any(char.isdigit() for char in next_line):
                        keyword_values[keyword] = next_line
                        break

    cleaned_keyword_values = {k: clean_text(v) for k, v in keyword_values.items()}
    return cleaned_keyword_values