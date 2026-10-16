# Lab 5: Static Code Analysis — Issue Report

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---|---|---|
| Mutable default argument | Code quality / Bug | 9 | A list used as a default argument could be shared between function calls. | Changed the default to `None` and initialized the list inside the function. |
| Bare exception handler | Security / Reliability | 21 | Catching every exception can hide unexpected errors. | Changed it to catch `ValueError` specifically. |
| Weak MD5 hash | Security | 25 | MD5 is not appropriate for security-sensitive hash generation. | Replaced it with random ticket-reference generation using `secrets`. |
| Permissive file permissions | Security | 55 | Mode `0o777` grants excessive permissions to the reservation file. | Removed the permission change. |
| Missing docstrings | Code quality | Multiple | Functions and the module lacked documentation. | Added module and function docstrings. |
| File handling | Code quality | 28, 33 | Files were opened without explicit encoding or context managers. | Used `with open(...)` and UTF-8 encoding. |
| Formatting violations | Style | Multiple | Long lines, missing blank lines and inconsistent formatting were reported. | Reformatted the code to follow Flake8 conventions. |

## Result

The corrected program achieved a Pylint score of 10.00/10 and Bandit reported no issues. The final Flake8 result must be verified from the saved after-report.
