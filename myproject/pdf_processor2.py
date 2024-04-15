import fitz
import re
from rich.console import Console
from rich.table import Table


def extract_text_from_pdf2(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def extract_values2(text):
    values = {}

    number_pattern = r"(\d+(?:\.\d+)?)"

    lines = text.split("\n")
    for line in lines:

        numbers = re.findall(number_pattern, line)
        if len(numbers) >= 2:

            parameter = line.split(numbers[0])[0].strip()
            result = float(numbers[0])
            reference_value = list(map(float, numbers[1:]))
            values[parameter] = {"result": result, "reference_value": reference_value}
            if parameter == "Platelet Count":
                break
    return values


def analyze_results2(blood_test_results):
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


def main():

    pdf_file = "blood_test.pdf"

    pdf_text = extract_text_from_pdf2(pdf_file)

    blood_test_results = extract_values2(pdf_text)

    analysis = analyze_results2(blood_test_results)

    console = Console()
    table = Table(title="نتیجه تجزیه و تحلیل")
    table.add_column("پارامتر", justify="center", style="cyan")
    table.add_column("نتیجه", justify="center", style="magenta")
    table.add_column("مقدار مرجع", justify="center", style="yellow")
    table.add_column("وضعیت", justify="center", style="cyan")

    for parameter, data in blood_test_results.items():
        result = data["result"]
        reference_value = data["reference_value"]
        status = analysis[parameter]

        table.add_row(parameter, str(result), str(reference_value), status)

    console.print(table)

    all_within_reference = all(status == "نرمال" for status in analysis.values())

    if all_within_reference:
        print(
            "\nتمامی نتایج آزمایشات در محدوده مرجع قرار دارند. این نشان دهنده این است که سطح هموگلوبین، هماتوکریت، تعداد سلول‌های قرمز، میانگین هموگلوبین میانی، غلظت میانی هموگلوبین، و پهنای توزیع سلول‌های قرمز همگی در محدوده مورد انتظار و سالم برای این بیمار است."
        )
    else:
        print("\nبرخی از نتایج آزمایشات خارج از محدوده مرجع قرار دارند. توصیه‌ها:")
        for parameter, result in analysis.items():
            if result != "نرمال":
                print(f"{parameter}: {result}")
                if result == "کم":
                    print(
                        """
با توجه به نتایج کم، مهم است با یک پزشک متخصص مشورت کنید تا تشخیص و درمان صحیح را دریافت کنید. مقادیر کم ممکن است به مشکلات سلامت زیرین اشاره داشته باشد که باید مورد توجه قرار گیرد. پزشک شما می‌تواند راهنمایی درباره آزمایشات و درمان‌های بیشتر ارائه دهد."""
                    )


if __name__ == "__main__":
    main()
