import unittest
import tinycss2

from parser import parse_declarations, parse_rules


class TestCSSParser(unittest.TestCase):

    def test_multiple_declarations(self):
        result = parse_declarations(
            "color: blue; margin: 10px;"
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["property"], "color")
        self.assertEqual(result[0]["value"], "blue")
        self.assertEqual(result[1]["property"], "margin")

    def test_semicolon_inside_quoted_value(self):
        result = parse_declarations(
            'content: "left; right";'
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], '"left; right"')

    def test_important_flag(self):
        result = parse_declarations(
            "border: 1px solid #ddd !important;"
        )

        self.assertEqual(result[0]["property"], "border")
        self.assertEqual(result[0]["value"], "1px solid #ddd")
        self.assertTrue(result[0]["important"])

    def test_custom_css_property(self):
        result = parse_declarations(
            "--brand-color: #1565c0;"
        )

        self.assertEqual(result[0]["property"], "--brand-color")
        self.assertEqual(result[0]["value"], "#1565c0")

    def test_nested_media_rule(self):
        css = """
        @media (min-width: 768px) {
            .card {
                display: grid;
                gap: var(--spacing);
            }
        }
        """

        nodes = tinycss2.parse_stylesheet(
            css,
            skip_comments=True,
            skip_whitespace=True,
        )

        result = parse_rules(nodes)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["selector"], ".card")
        self.assertEqual(
            result[0]["at_rule_context"],
            ["@media (min-width: 768px)"],
        )

        properties = [
            item["property"]
            for item in result[0]["declarations"]
        ]

        self.assertEqual(properties, ["display", "gap"])

    def test_top_level_rule(self):
        css = ".card { color: blue; }"

        nodes = tinycss2.parse_stylesheet(
            css,
            skip_comments=True,
            skip_whitespace=True,
        )

        result = parse_rules(nodes)

        self.assertEqual(result[0]["selector"], ".card")
        self.assertEqual(result[0]["at_rule_context"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)