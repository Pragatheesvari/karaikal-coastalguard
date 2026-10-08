import pandas as pd
import re
from pathlib import Path

URL = "https://karaikal.gov.in/namneer/list-of-water-bodies/"

# Read the Government webpage table
tables = pd.read_html(URL)

print("Tables found:", len(tables))

# Find the table containing the water-body data
df = None

for table in tables:
    text = " ".join(str(c) for c in table.columns)
    if "Municipality" in text or "Water Body" in text:
        df = table
        break

if df is None:
    raise Exception("Water-body table was not found.")

# Flatten multi-level column names if necessary
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [
        "_".join(str(x) for x in col if str(x) != "nan").strip()
        for col in df.columns
    ]
else:
    df.columns = [str(c).strip() for c in df.columns]

print("\nOriginal columns:")
print(df.columns.tolist())


# Convert DMS coordinates to decimal
def dms_to_decimal(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # Find degree, minute and second values
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*°\s*"
        r"(\d+(?:\.\d+)?)?\s*[’']?\s*"
        r"(\d+(?:\.\d+)?)?\s*[″\"]?",
        value
    )

    if not match:
        return None

    degrees = float(match.group(1))
    minutes = float(match.group(2) or 0)
    seconds = float(match.group(3) or 0)

    decimal = degrees + minutes / 60 + seconds / 3600

    if "S" in value.upper() or "W" in value.upper():
        decimal = -decimal

    return round(decimal, 6)


# Rename columns according to the Government table
new_columns = {}

for col in df.columns:
    c = col.lower()

    if "sl" in c or "no" in c:
        new_columns[col] = "id"

    elif "municipality" in c or "commune" in c:
        new_columns[col] = "commune"

    elif "village" in c:
        new_columns[col] = "village"

    elif "water" in c:
        new_columns[col] = "water_body"

    elif "latitude" in c or "lattitude" in c:
        new_columns[col] = "latitude_dms"

    elif "longitude" in c:
        new_columns[col] = "longitude_dms"

df = df.rename(columns=new_columns)


# Keep only useful columns
required = [
    "id",
    "commune",
    "village",
    "water_body",
    "latitude_dms",
    "longitude_dms"
]

missing = [c for c in required if c not in df.columns]

if missing:
    print("\nMissing columns:", missing)
    print("Available columns:", df.columns.tolist())
    raise Exception("Column names need adjustment.")

df = df[required].copy()


# Convert coordinates
df["latitude"] = df["latitude_dms"].apply(dms_to_decimal)
df["longitude"] = df["longitude_dms"].apply(dms_to_decimal)


# Remove unnecessary DMS columns
df = df[
    [
        "id",
        "commune",
        "village",
        "water_body",
        "latitude",
        "longitude"
    ]
]


# Clean text
for col in ["commune", "village", "water_body"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


# Save CSV
output_folder = Path("data")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "karaikal_locations.csv"

df.to_csv(output_file, index=False, encoding="utf-8-sig")


print("\n====================================")
print("DATASET 1 CREATED SUCCESSFULLY")
print("====================================")
print("Rows:", len(df))
print("File:", output_file)
print("\nFirst 5 records:")
print(df.head())