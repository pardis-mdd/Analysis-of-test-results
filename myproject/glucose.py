import fitz
import easyocr
import re

# Function to interpret glucose levels
def interpret_glucose(glucose):
    glucose = float(glucose)
    if glucose < 100:
        return "ایده‌آل: قند خون شما در محدوده ایده‌آل است (70 – 100 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "بالا: سطح قند خون شما بالا است (< 100 میلی‌گرم بر دسی‌لیتر)"

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to clean extracted text and find glucose value
def clean_text(text):
    match = re.search(r'\d+', text)
    if match:
        return match.group(0)
    return ''

# Function to extract keyword values from PDF or image
def extract_keyword_values(file_path):
    if file_path.lower().endswith('.pdf'):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(file_path)
        extracted_text = '\n'.join([entry[1] for entry in result])
    
    extracted_lines = extracted_text.splitlines()
    extracted_lines = [line.lower() for line in extracted_lines]

    keyword_values = {}
    keywords = ["glucose"]

    for line in extracted_lines:
        for keyword in keywords:
            if keyword in line:
                # Find the number in the same line or the next lines
                match = re.search(r'glucose.*?(\d+)', line)
                if match:
                    keyword_values[keyword] = match.group(1)
                else:
                    # Check the next lines for a number
                    for next_line in extracted_lines[extracted_lines.index(line) + 1:]:
                        if any(char.isdigit() for char in next_line):
                            keyword_values[keyword] = clean_text(next_line)
                            break
                break

    return keyword_values