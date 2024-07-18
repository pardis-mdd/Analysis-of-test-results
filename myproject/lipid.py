import fitz
import easyocr
import re

# Interpretation functions
def interpret_total_cholesterol(total_cholesterol):
    if total_cholesterol < 120:
        return "ایده‌آل: سطح کلسترول کل در محدوده ایده‌آل است (120 – 199 میلی‌گرم بر دسی‌لیتر)"
    elif 120 <= total_cholesterol <= 199:
        return "ایده‌آل: سطح کلسترول کل در محدوده ایده‌آل است (120 – 199 میلی‌گرم بر دسی‌لیتر)"
    elif 200 <= total_cholesterol <= 239:
        return "مرزی بین بالا: سطح کلسترول کل در محدوده مرزی بین بالا است (200 – 239 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "بالا: سطح کلسترول کل بالا است (≥ 240 میلی‌گرم بر دسی‌لیتر)"

def interpret_triglycerides(triglycerides):
    if triglycerides < 150:
        return "ایده‌آل: سطح تری‌گلیسرید در محدوده ایده‌آل است (< 150 میلی‌گرم بر دسی‌لیتر)"
    elif 150 <= triglycerides < 200:
        return "مرزی بین بالا: سطح تری‌گلیسرید در محدوده مرزی بین بالا است (150 – 199 میلی‌گرم بر دسی‌لیتر)"
    elif 200 <= triglycerides < 500:
        return "بالا: سطح تری‌گلیسرید در محدوده بالا است (200 – 499 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "خیلی بالا: سطح تری‌گلیسرید بسیار بالا است (≥ 500 میلی‌گرم بر دسی‌لیتر)"

def interpret_ldl_cholesterol(ldl_cholesterol):
    if ldl_cholesterol < 100:
        return "ایده‌آل: سطح کلسترول LDL در محدوده ایده‌آل است (< 100 میلی‌گرم بر دسی‌لیتر)"
    elif 100 <= ldl_cholesterol < 130:
        return "بالاتر از ایده‌آل: سطح کلسترول LDL بالاتر از ایده‌آل اما هنوز قابل قبول است (100 – 129 میلی‌گرم بر دسی‌لیتر)"
    elif 130 <= ldl_cholesterol < 160:
        return "مرزی بین بالا: سطح کلسترول LDL در محدوده مرزی بین بالا است (130 – 159 میلی‌گرم بر دسی‌لیتر)"
    elif 160 <= ldl_cholesterol < 190:
        return "بالا: سطح کلسترول LDL در محدوده بالا است (160 – 189 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "خیلی بالا: سطح کلسترول LDL بسیار بالا است (≥ 190 میلی‌گرم بر دسی‌لیتر)"

def interpret_hdl_cholesterol(hdl_cholesterol, gender):
        
        if hdl_cholesterol >= 40:
            return "ایده‌آل: سطح کلسترول HDL در محدوده ایده‌آل است (≥ 40 میلی‌گرم بر دسی‌لیتر )"
        else:
            return "پایین: سطح کلسترول HDL پایین است (< 40 میلی‌گرم بر دسی‌لیتر )"
    

def interpret_non_hdl_cholesterol(non_hdl_cholesterol):
    if non_hdl_cholesterol < 130:
        return "ایده‌آل: سطح کلسترول Non-HDL در محدوده ایده‌آل است (< 130 میلی‌گرم بر دسی‌لیتر)"
    elif 130 <= non_hdl_cholesterol < 160:
        return "ناسازگار: سطح کلسترول Non-HDL در محدوده ناسازگار است (130 – 159 میلی‌گرم بر دسی‌لیتر)"
    elif 160 <= non_hdl_cholesterol < 190:
        return "مرزی بین بالا: سطح کلسترول Non-HDL در محدوده مرزی بین بالا است (160 – 189 میلی‌گرم بر دسی‌لیتر)"
    elif 190 <= non_hdl_cholesterol < 220:
        return "بالا: سطح کلسترول Non-HDL در محدوده بالا است (190 – 219 میلی‌گرم بر دسی‌لیتر)"
    else:
        return "خیلی بالا: سطح کلسترول Non-HDL بسیار بالا است (≥ 220 میلی‌گرم بر دسی‌لیتر)"

# Helper functions
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
    keywords = ["total", "triglycerides", "ldl", "vldl", "hdl", "non-hdl"]  

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
