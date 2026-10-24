# CSS Parser

## Overview
This project reads a CSS file and extracts meaningful, structured information using Python and the `tinycss2` library. It produces JSON containing CSS selectors, declaration properties, values, importance flags, and applicable at-rule contexts.

## Design Choices
I extracted selectors because they identify the elements targeted by CSS rules. I stored each declaration as a property-value pair and retained the `!important` flag to preserve relevant styling information. I also included at-rule context so that nested rules, such as media queries, retain the conditions under which they apply.

## Edge Case
One edge case is a semicolon inside a quoted CSS value, such as `content: "left; right";`. A parser based on splitting text at every semicolon could incorrectly divide this declaration. Using `tinycss2` allows the declaration to be parsed according to CSS syntax, and an automated test verifies that the quoted value remains intact.

## Requirements
- Python 3.11 or compatible
- `tinycss2==1.5.1`

## Run the Project
Install the dependency:

```powershell
python -m pip install -r requirements.txt
```

Run the parser:

```powershell
python parser.py
```

Run the automated tests:

```powershell
python -m unittest -v test_parser.py
```

## Current Scope
The parser handles ordinary style rules and nested rule-based at-rules, including media queries. It does not currently implement every CSS at-rule or perform full CSS validation.
