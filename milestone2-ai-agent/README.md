# CSS Question-Answering AI Agent

## 1. Overview

This project implements an AI agent that answers questions about a CSS
file by using Python tools to retrieve actual source content, search for
text, and inspect CSS structure.

The agent uses Google's Gemini API for natural-language understanding
and tool selection. The Python tools read the source file and return
evidence that the model can use to construct its answer.

The source CSS file is:
`../milestone1-css-parser/sample.css`

## 2. Features

- Reads the complete CSS source, including comments.
- Searches the file and returns matching lines with line numbers.
- Extracts selectors, declarations, values, and !important flags.
- Preserves nested at-rule contexts, such as media queries.
- Reports information that cannot be found instead of deliberately
  inventing missing CSS declarations.
- Caches answers for identical questions when the source CSS and model
  are unchanged.
- Includes automated tests for tool behavior and cache reliability.

## 3. Python Tools

### read_css_file()
Reads the complete CSS source and returns its filename, line count,
and content.

### search_css(query)
Searches the CSS source case-insensitively and returns matching lines.

### inspect_css_structure()
Extracts style rules, declarations, at-rules, nested contexts,
and recognized parsing errors.

## 4. Design Decisions and Reliability

The agent uses Python functions to obtain information from the actual
CSS file rather than relying only on the language model's memory.
Its instructions require it to distinguish source-backed facts from
general CSS explanations and to state when the file lacks evidence.

The cache key includes the question, a hash of the current CSS content,
and the selected model. This allows identical requests against unchanged
content to return the same cached answer.

Automated tests verify missing search results, repeated tool outputs,
cache behavior, and cache invalidation when the source changes. These
measures reduce unsupported answers and improve consistency, although
they cannot guarantee that a language model will never make a mistake.

## 5. Requirements

- Python 3.11 or compatible
- Dependencies listed in requirements.txt
- A valid Gemini API key and access to the configured model

## 6. Setup

From the repository root, create a virtual environment if one does
not already exist:

    python -m venv .venv

In PowerShell, install the dependencies for Milestone 2:

    & ".\.venv\Scripts\python.exe" -m pip install -r ".\milestone2-ai-agent\requirements.txt"

Create a local `.env` file in this directory containing:

    GEMINI_API_KEY=your_actual_api_key
    GEMINI_MODEL=your_configured_model_id

Replace the example values with your own credentials and model ID.
Never commit `.env` to GitHub.

## 7. Run the Agent

From the repository root:

    cd milestone2-ai-agent
    & "..\.venv\Scripts\python.exe" agent.py

Example questions:

- What is the brand color defined in the CSS file?
- What styles apply to .card at widths of 768px or more?
- Does this file define an animation-name property?
- What does the comment about card styling say?

Type `exit` or `quit` to stop the agent.

## 8. Run Automated Tests

From the `milestone2-ai-agent` directory:

    & "..\.venv\Scripts\python.exe" -m unittest -v test_agent.py

The test suite covers CSS reading, search behavior, nested rules,
missing information, repeatability, and cache invalidation.

## 9. Limitations

This project is intended as a CSS question-answering demonstration.
The CSS parser identifies syntax structures but does not guarantee
full CSS semantic validation or browser rendering correctness.
The language model may still make unsupported claims, so its answers
should be evaluated against the source and automated tests.

The agent needs network access and a valid Gemini API key for
model-generated answers.