# Lab 7: Fuzzing for Input Validation Bugs

**Course:** Software Engineering Lab  
**Student:** Piyush Nadgir  
**SRN:** PES1UG24AM190  
**Topic:** Property-Based Fuzz Testing with Hypothesis (Bookstore Trade-In System)  
**Date:** November 15, 2026  

---

## 📌 Overview

This lab explores **Fuzz Testing** as a dynamic security and quality assurance technique. Using Python's **Hypothesis** library, the `processor.py` application is subjected to thousands of randomized, malformed, boundary, and unexpected inputs to identify input validation flaws. The functions are subsequently hardened using defensive programming practices and verified with 100% green test passes.

---

## 📂 Repository Contents

| File / Directory | Description |
|---|---|
| `processor.py` | Hardened application code implementing input validation and defensive programming |
| `test_processor.py` | Property-based fuzz testing suite using Hypothesis strategies |
| `Lab7_FuzzTesting_Report.pdf` | Comprehensive 4-page lab report with terminal screenshots and bug analysis |
| `screenshots/` | High-resolution terminal captures documenting each lab step |
| `README.md` | Lab documentation and execution instructions |

---

## 🧪 Tested Functions & Hardening Summary

### 1. `verify_isbn10_format(isbn_str)`
- **Fuzzing Issues Found:** `AttributeError` on `None`, `IndexError` on short or empty strings, `ValueError` when non-digits encountered.
- **Hardening:** Added `isinstance(..., str)` type guard, verified exact 10-character length, confirmed numeric digits for group code and start digit, and validated checksum (`0-9` or `'X'`).

### 2. `calculate_depreciation_factor(book_age_str)`
- **Fuzzing Issues Found:** `AttributeError` on `None`, `ValueError` on missing delimiter or non-numeric strings, `ZeroDivisionError` on `0/0` or lifespan of zero.
- **Hardening:** Verified single `/` delimiter, guarded against `life <= 0`, negative age, and `NaN`/`Inf` floats, returning `None` gracefully on invalid inputs.

### 3. `lookup_condition_multiplier(condition_code)`
- **Fuzzing Issues Found:** `AttributeError` on `None`, `KeyError` on unmapped condition codes or empty strings.
- **Hardening:** Validated string type, case-normalized strings, and utilized `.get(grade, None)` for safe dictionary retrieval.

---

## 🚀 Execution & Verification

### 1. Install Dependencies
```bash
pip install hypothesis pytest
```

### 2. Run the Application
```bash
python processor.py
```

### 3. Run Property-Based Fuzz Tests
```bash
pytest test_processor.py
```
*Result: 3 passed with 0 crashes across hundreds of fuzzing iterations.*
