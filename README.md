# SkillFirst Labs — Shortlisting Tasks

This repository contains two Python projects developed for the
Skill First Labs shortlisting assignment.

## Milestone 1: CSS Parser

Reads a CSS file and extracts structured information, including
selectors, declarations, values, importance flags, and nested
at-rule contexts.

Folder: `milestone1-css-parser/`

## Milestone 2: CSS Question-Answering AI Agent

Uses Python tools and a Gemini model to answer questions about
the CSS file. The tools read the source, search its contents,
and inspect its structure.

Folder: `milestone2-ai-agent/`

## Requirements

- Python 3.11 or compatible
- Dependencies listed in each milestone's `requirements.txt`
- A valid Gemini API key to run the AI agent

## Testing

Run the tests from each project's folder:

Milestone 1:

    python -m unittest -v test_parser.py

Milestone 2:

    python -m unittest -v test_agent.py

## Security

API credentials must be stored locally in the Milestone 2 `.env`
file. Never commit API keys, `.env` files, or virtual environments.