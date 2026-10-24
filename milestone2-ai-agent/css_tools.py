from pathlib import Path

import tinycss2


# Locate sample.css in the Milestone 1 folder.
CSS_PATH = (
    Path(__file__).resolve().parent.parent
    / "milestone1-css-parser"
    / "sample.css"
)


def _read_text():
    """Read the CSS file or report a useful error."""
    try:
        return CSS_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"CSS file not found: {CSS_PATH.name}. "
            "Check that milestone1-css-parser/sample.css exists."
        ) from None
    except UnicodeDecodeError:
        raise ValueError(
            "The CSS file could not be decoded as UTF-8."
        ) from None


def read_css_file():
    """Return the complete CSS source and basic file information."""
    content = _read_text()

    return {
        "source_file": CSS_PATH.name,
        "line_count": len(content.splitlines()),
        "content": content,
    }


def search_css(query):
    """Search the CSS source, including comments, by line."""
    if not isinstance(query, str) or not query.strip():
        return {
            "error": "Please provide a non-empty search query.",
            "matches": [],
        }

    lines = _read_text().splitlines()
    matching_lines = [
        {"line": number, "text": line.strip()}
        for number, line in enumerate(lines, start=1)
        if query.casefold() in line.casefold()
    ]

    return {
        "query": query,
        "match_count": len(matching_lines),
        "matches": matching_lines[:50],
        "truncated": len(matching_lines) > 50,
    }


def _serialize(tokens):
    """Convert CSS tokens back into readable CSS text."""
    return tinycss2.serialize(tokens).strip()


def _get_declarations(content, errors):
    """Extract declarations while recording CSS parsing errors."""
    nodes = tinycss2.parse_declaration_list(
        content,
        skip_comments=True,
        skip_whitespace=True,
    )

    declarations = []

    for node in nodes:
        if node.type == "error":
            errors.append({
                "message": node.message,
                "line": node.source_line,
                "column": node.source_column,
            })
            continue

        if node.type != "declaration":
            continue

        declarations.append({
            "property": node.name,
            "value": _serialize(node.value),
            "important": node.important,
        })

    return declarations


def _collect_rules(
    nodes,
    context,
    rules,
    at_rules,
    errors,
):
    """Collect style rules recursively, preserving at-rule context."""
    for node in nodes:
        if node.type == "error":
            errors.append({
                "message": node.message,
                "line": node.source_line,
                "column": node.source_column,
            })
            continue

        if node.type == "qualified-rule":
            rules.append({
                "kind": "style_rule",
                "selector": _serialize(node.prelude),
                "at_rule_context": list(context),
                "line": node.source_line,
                "declarations": _get_declarations(
                    node.content, errors
                ),
            })

        elif node.type == "at-rule":
            prelude = _serialize(node.prelude)
            label = f"@{node.at_keyword}"

            if prelude:
                label += f" {prelude}"

            at_rules.append({
                "name": label,
                "context": list(context),
                "line": node.source_line,
                "has_block": node.content is not None,
            })

            if node.content is None:
                continue

            nested_nodes = tinycss2.parse_rule_list(
                node.content,
                skip_comments=True,
                skip_whitespace=True,
            )

            has_nested_rules = any(
                child.type in ("qualified-rule", "at-rule")
                for child in nested_nodes
            )

            if has_nested_rules:
                _collect_rules(
                    nested_nodes,
                    context + [label],
                    rules,
                    at_rules,
                    errors,
                )
            else:
                declarations = _get_declarations(
                    node.content, errors
                )

                if declarations:
                    rules.append({
                        "kind": "at_rule_declarations",
                        "at_rule": label,
                        "at_rule_context": list(context),
                        "line": node.source_line,
                        "declarations": declarations,
                    })

                for child in nested_nodes:
                    if child.type == "error":
                        errors.append({
                            "message": child.message,
                            "line": child.source_line,
                            "column": child.source_column,
                        })


def inspect_css_structure():
    """Return selectors, declarations, at-rules and parse errors."""
    content = _read_text()

    nodes = tinycss2.parse_stylesheet(
        content,
        skip_comments=True,
        skip_whitespace=True,
    )

    rules = []
    at_rules = []
    errors = []

    _collect_rules(
        nodes,
        [],
        rules,
        at_rules,
        errors,
    )

    return {
        "source_file": CSS_PATH.name,
        "style_rule_count": sum(
            rule["kind"] == "style_rule" for rule in rules
        ),
        "rules": rules,
        "at_rules": at_rules,
        "parse_errors": errors,
    }