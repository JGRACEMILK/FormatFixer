# FormatFixer
Fixes the format of a tsv that has been malformed by an embedded newline character. It requires a consistent pattern for the beginning of each row which must be defined by regex.

# TSV Row Repair Utility

This script repairs **broken TSV files** where fields (typically addresses) contain embedded newline characters, causing logical rows to be split across multiple physical lines.

It reconstructs rows using a **regex anchor pattern** that reliably identifies the start of each valid data row.

---

## 🚨 Problem Context

In many real-world TSV exports:

- Text fields (e.g. addresses) are **not quoted**
- Embedded newline characters split a single logical row across multiple lines
- Standard TSV/CSV parsers fail because row boundaries are corrupted

### Example broken file
1234 1234567890 John Smith 12 Main Street\n
Apartment 4B\n
Cityville\n
1235 1234567891 Jane Doe 8 High Road

### Fixed output
1234 1234567890 John Smith 12 Main Street Apartment 4B Cityville
1235 1234567891 Jane Doe 8 High Road

---

## ✅ How It Works

- A **regular expression** defines what a valid row start looks like
- Any line **matching the pattern** starts a new logical row
- Any line **not matching the pattern** is treated as a continuation of the previous row
- Optional header handling ensures column headers are preserved
- Orphan lines (continuations before the first valid row) are counted and reported

This approach is **deterministic, fast, and safe** for large files.

---

## 📦 Features

- Regex-anchored row reconstruction
- Works with **unquoted TSV files**
- Optional header support
- Configurable line-join behavior
- Clean exit codes for automation and pipelines
- Streaming processing (handles large files)

---

## 🛠 Requirements

- Python **3.7+**
- No external dependencies

---

## 🚀 Usage

### Basic command
python fix_tsv_rows.py \
  --input broken.tsv \
  --output fixed.tsv \
  --row-start-pattern '^\d{4}\t\d{10}\t'

### With header row
python fix_tsv_rows.py \
  --input broken.tsv \
  --output fixed.tsv \
  --row-start-pattern '^\d{4}\t\d{10}\t' \
  --has-header

### Fail pipeline if malformed data is found (the pattern isn't applying to a row)
python fix_tsv_rows.py \
  --input broken.tsv \
  --output fixed.tsv \
  --row-start-pattern '^\d{4}\t\d{10}\t' \
  --has-header \
  --fail-on-orphans

### --row-start-pattern
^\d{4}\t\d{10}\t

- This example says that each row of data should start with 4 digit value in the first column and 10 digits in the second column