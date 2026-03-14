---
name: No pandas - write logic from scratch
description: Do not use pandas; write CSV processing logic from scratch using stdlib
type: feedback
---

Do not use pandas for data processing scripts. Write logic from scratch using Python's standard library (csv module, etc.) to avoid unnecessary dependencies.

**Why:** User explicitly prefers minimal dependencies and has been burned by this before.

**How to apply:** Any time writing a Python script that processes CSV or tabular data, use `import csv` and manual logic instead of reaching for pandas.
