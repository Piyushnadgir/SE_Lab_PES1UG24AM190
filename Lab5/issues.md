# Lab 5 -- Static Code Analysis Issues

**Project:** Movie Seat Reservation System\
**File analyzed:** `theater_system.py`\
**Tools used:** Pylint, Bandit, and Flake8

## Issues identified in the original code

  -----------------------------------------------------------------------------------
  Tool              Issue / finding      Severity or       Resolution
                                         category          
  ----------------- -------------------- ----------------- --------------------------
  Pylint            Missing module       Convention        Added a module-level
                    docstring                              docstring.

  Pylint            Missing function     Convention        Added docstrings to the
                    docstrings                             functions.

  Pylint            Mutable default      Warning           Changed the default to
                    argument                               `None` and initialized a
                    (`system_logs=[]`)                     new list inside the
                                                           function.

  Pylint            Old-style `%` string Convention        Replaced it with
                    formatting                             f-strings.

  Pylint            Bare `except` clause Warning           Caught the specific
                                                           `ValueError` expected when
                                                           a seat is not present.

  Pylint            File opened without  Warning           Added `encoding="utf-8"`.
                    an explicit encoding                   

  Pylint            File handling        Refactor          Used `with open(...)` so
                    without a context                      files are closed
                    manager                                automatically.

  Pylint            Use of the `global`  Warning           Updated the existing
                    statement                              global dictionary in place
                                                           using `clear()` and
                                                           `update()`.

  Pylint            Function name did    Convention        Renamed
                    not follow                             `printSeatingSummary` to
                    snake_case                             `print_seating_summary`.

  Pylint            Unused loop variable Convention        Iterated over
                                                           `shows.values()` because
                                                           the key was not needed.

  Pylint            Line exceeded the    Convention        Split long statements
                    configured maximum                     across multiple lines.
                    length                                 

  Bandit            B110 --              Low               Replaced broad exception
                    `try/except/pass`                      handling with a specific
                    pattern                                `ValueError` handler and
                                                           an explicit return value.

  Bandit            B324 -- MD5 hash     High              Replaced MD5 with SHA-256.
                    function                               

  Bandit            B103 -- overly       High              Changed the file
                    permissive file                        permission mode to
                    permissions                            `0o600`.
                    (`0o777`)                              

  Flake8            E302 -- expected two Formatting        Added the required blank
                    blank lines between                    lines.
                    top-level                              
                    definitions                            

  Flake8            E501 -- line too     Formatting        Wrapped long lines.
                    long                                   

  Flake8            E722 -- bare         Code quality      Replaced it with a
                    `except`                               specific exception
                                                           handler.

  Flake8            E305 -- expected two Formatting        Corrected the spacing at
                    blank lines after a                    the end of the file.
                    function definition                    
  -----------------------------------------------------------------------------------

## Before-and-after results

  Tool     Before                           After
  -------- -------------------------------- ---------------------
  Pylint   Score: **5.87/10**               Score: **10.00/10**
  Bandit   **3 findings** (2 High, 1 Low)   **0 findings**
  Flake8   **11 violations**                **0 violations**

## Summary

The original program had code-quality, formatting, and security issues.
The fixes improved readability, consistency, file handling, exception
handling, and the security of the ticket hash and saved-file
permissions. The final reports show a Pylint score of 10.00/10, no
Bandit findings, and no Flake8 violations.
