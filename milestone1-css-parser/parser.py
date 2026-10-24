import json
from pathlib import Path
import tinycss2


def parse_declarations(content):
    """Extract CSS declarations into structured dictionaries."""
    nodes = tinycss2.parse_declaration_list(
        content,
        skip_comments=True,
        skip_whitespace=True,
    )

    declarations = []

    for node in nodes:
        if node.type != "declaration":
            continue

        declarations.append({
            "property": node.name,
            "value": tinycss2.serialize(node.value).strip(),
            "important": node.important,
        })

    return declarations
def parse_rules(nodes, at_rule_context=None):
    """Extract style rules, including rules nested inside at-rules."""
    if at_rule_context is None:
        at_rule_context = []

    structured_rules = []

    for node in nodes:
        if node.type == "qualified-rule":
            structured_rules.append({
                "selector": tinycss2.serialize(
                    node.prelude
                ).strip(),
                "at_rule_context": at_rule_context.copy(),
                "declarations": parse_declarations(node.content),
            })

        elif node.type == "at-rule" and node.content is not None:
            at_rule_name = f"@{node.at_keyword}"
            prelude = tinycss2.serialize(node.prelude).strip()

            if prelude:
                at_rule_name += f" {prelude}"

            nested_nodes = tinycss2.parse_rule_list(
                node.content,
                skip_comments=True,
                skip_whitespace=True,
            )

            structured_rules.extend(
                parse_rules(
                    nested_nodes,
                    at_rule_context + [at_rule_name],
                )
            )

    return structured_rules

def main():
    css_path = Path(__file__).with_name("sample.css")
    css_text = css_path.read_text(encoding="utf-8")

    rules = tinycss2.parse_stylesheet(
        css_text,
        skip_comments=True,
        skip_whitespace=True,
    )

    structured_rules = parse_rules(rules)

    result = {
        "source_file": css_path.name,
        "rules": structured_rules,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()