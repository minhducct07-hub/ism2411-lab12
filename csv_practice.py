# Reflection 1: Python makes repeatable, automated ETL easier, especially when processing many files or applying the same rules regularly.
# Excel is more convenient for interactive inspection, formulas, and charts, while Python handles custom workflows and larger repeatable jobs well.
# Reflection 2: A business could append each daily payment batch's processing time and amount to a transaction run log for later auditing.
# Append mode is appropriate because it preserves earlier runs while adding a new record each time the process executes.

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
SALES_FILE = DATA_DIR / "sales.csv"
CLEANED_FILE = DATA_DIR / "cleaned.csv"
RUN_LOG_FILE = DATA_DIR / "run_log.txt"


# Exercise 1: Confirm the source file has the expected header and 12 data rows.
print("Exercise 1: Verify sales file")
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.reader(sales_file)
    source_header = next(reader)
    source_rows = list(reader)
assert source_header == ["product", "price", "quantity"]
assert len(source_rows) == 12
print(f"Header: {source_header}; data rows: {len(source_rows)}")


# Exercise 2: Read and print every raw row, including the header.
print("Exercise 2: Raw rows")
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.reader(sales_file)
    for row in reader:
        print(row)


# Exercise 3: Store and print the header separately.
print("\nExercise 3: Header and data rows")
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.reader(sales_file)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)


# Exercise 4: Compute each product total and overall revenue.
print("\nExercise 4: Line totals")
total_revenue = Decimal("0")
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.reader(sales_file)
    next(reader)
    for product, price_text, quantity_text in reader:
        price = Decimal(price_text)
        quantity = int(quantity_text)
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")


# Exercise 5: Keep only rows whose total is greater than $100.
print("\nExercise 5: Filtered rows")
original_count = 0
written_count = 0
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.reader(sales_file)
    next(reader)
    with CLEANED_FILE.open("w", newline="", encoding="utf-8") as cleaned_file:
        writer = csv.writer(cleaned_file)
        writer.writerow(["Product", "Price", "Qty", "Total"])
        for product, price_text, quantity_text in reader:
            original_count += 1
            price = Decimal(price_text)
            quantity = int(quantity_text)
            line_total = price * quantity
            if line_total > Decimal("100"):
                writer.writerow([product, price_text, quantity, f"{line_total:.2f}"])
                written_count += 1
print(f"Wrote {written_count} qualifying rows out of {original_count} original rows.")


# Exercise 6: Read the same fields by their header names.
# csv.reader is compact and works well when column order is fixed and known.
# DictReader is clearer when columns have meaningful names or their order may change.
print("\nExercise 6: DictReader totals")
dict_total_revenue = Decimal("0")
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.DictReader(sales_file)
    for row in reader:
        product = row["product"]
        price = Decimal(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"DictReader total revenue: ${dict_total_revenue:.2f}")


# Exercise 7: Accumulate revenue by product and print products alphabetically.
print("\nExercise 7: Revenue by product")
revenue_by_product = {}
with SALES_FILE.open(newline="", encoding="utf-8") as sales_file:
    reader = csv.DictReader(sales_file)
    for row in reader:
        product = row["product"]
        line_total = Decimal(row["price"]) * int(row["quantity"])
        revenue_by_product[product] = revenue_by_product.get(product, Decimal("0")) + line_total

for product in sorted(revenue_by_product):
    print(f"{product}: ${revenue_by_product[product]:.2f}")


# Exercise 8: Append one timestamped total for this run.
with RUN_LOG_FILE.open("a", encoding="utf-8") as log_file:
    timestamp = datetime.now().isoformat(timespec="seconds")
    log_file.write(f"{timestamp} - Total revenue: ${total_revenue:.2f}\n")
print(f"\nAppended this run to {RUN_LOG_FILE.name}.")