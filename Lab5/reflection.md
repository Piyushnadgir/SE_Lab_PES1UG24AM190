# Lab 5 -- Reflection

## 1. What is the purpose of static code analysis?

Static code analysis checks source code without running the program. It
helps identify potential bugs, insecure coding patterns, and formatting
or style problems early. In this lab, Pylint, Bandit, and Flake8 were
used to examine different aspects of `theater_system.py`.

## 2. What did you learn from using Pylint?

Pylint helped identify code-quality and maintainability problems. The
original code had missing docstrings, a mutable default argument,
old-style string formatting, a bare exception handler, file-handling
problems, and a function name that did not follow Python naming
conventions. Fixing these issues made the code easier to read and
maintain. The final Pylint score improved from **5.87/10 to 10.00/10**.

## 3. What did you learn from using Bandit?

Bandit focuses on common security weaknesses in Python code. It reported
the use of MD5, overly permissive file permissions, and a
`try/except/pass` pattern. I replaced MD5 with SHA-256, changed the file
permission mode from `0o777` to `0o600`, and handled the expected
`ValueError` explicitly. The final Bandit scan reported **no issues**.

## 4. What did you learn from using Flake8?

Flake8 checks Python code for style and formatting violations. It
identified problems such as missing blank lines, lines that were too
long, and a bare `except` clause. Correcting these made the source code
more consistent with Python style conventions. The final Flake8 report
contained **zero violations**.

## 5. What challenges did you face, and how did you resolve them?

One challenge was understanding that each tool checks a different aspect
of the same source file. Some findings overlapped: for example, the bare
`except` was reported by both Pylint and Flake8, while Bandit also
identified the exception-handling pattern as a security concern. I fixed
the underlying code rather than treating each report as an unrelated
problem. I then reran the tools and saved the before-and-after reports.

Another small challenge was making sure the reports were saved in the
correct `Lab5` directory and that generated files and the virtual
environment were not added to Git. I used `.gitignore` rules for local
and generated files.

## 6. Why is it important to run static analysis regularly?

Running static analysis regularly helps detect problems before code is
submitted or deployed. It can improve readability, maintainability, and
security, and it encourages consistent coding practices. It is
especially useful in team projects because it helps maintain a common
quality standard.

## 7. What is the overall outcome of this lab?

The lab demonstrated how static analysis tools can be used together to
improve a Python program. After fixing the reported issues, the program
achieved a **10.00/10 Pylint score**, **zero Bandit findings**, and
**zero Flake8 violations**. I learned that code should not only work; it
should also be readable, maintainable, consistently formatted, and
written with security in mind.
