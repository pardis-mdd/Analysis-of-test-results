import re
import fitz


def extract_text_from_pdf(file):

    pdf_document = fitz.open(stream=file.read(), filetype="pdf")

    text = ""
    for page in pdf_document:
        text += page.get_text()

    return text


def extract_values(text):
    values = {}

    number_pattern = r"(\d+(?:\.\d+)?)"

    lines = text.split("\n")
    for line in lines:

        numbers = re.findall(number_pattern, line)
        if "GLUCOSE, FASTING" in line:
            parameter = "GLUCOSE, FASTING"
            result = float(numbers[0])
            reference_value = list(map(float, numbers[1:]))
            values[parameter] = {"result": result, "reference_value": reference_value}
            break
    return values


def analyze_results(blood_test_results):
    analysis = {}
    for parameter, data in blood_test_results.items():
        result = data["result"]
        reference_value = data["reference_value"]
        if result < reference_value[0]:
            analysis[parameter] = "کم"
        elif result > reference_value[1]:
            analysis[parameter] = "بالا"
        else:
            analysis[parameter] = "نرمال"
    return analysis
