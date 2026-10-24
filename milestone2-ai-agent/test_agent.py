import unittest
from unittest.mock import patch
from agent import ask_css_question, _cached_answer
from css_tools import (
    read_css_file,
    search_css,
    inspect_css_structure,
)


class TestCSSTools(unittest.TestCase):

    def test_read_actual_css_file(self):
        result = read_css_file()

        self.assertEqual(result["source_file"], "sample.css")
        self.assertGreater(result["line_count"], 0)
        self.assertIn(":root", result["content"])
        self.assertIn("@media", result["content"])

    def test_search_finds_spacing_variable(self):
        result = search_css("--spacing")

        self.assertEqual(result["match_count"], 2)
        self.assertEqual(
            [item["line"] for item in result["matches"]],
            [4, 19],
        )

    def test_search_is_case_insensitive(self):
        result = search_css("--BRAND-COLOR")

        self.assertGreater(result["match_count"], 0)

    def test_search_handles_missing_content(self):
        result = search_css("animation-name-that-does-not-exist")

        self.assertEqual(result["match_count"], 0)
        self.assertEqual(result["matches"], [])

    def test_search_rejects_empty_query(self):
        result = search_css("   ")

        self.assertIn("error", result)
        self.assertEqual(result["matches"], [])

    def test_structure_includes_nested_media_rule(self):
        result = inspect_css_structure()

        self.assertEqual(result["style_rule_count"], 3)
        self.assertEqual(len(result["at_rules"]), 1)
        self.assertEqual(result["parse_errors"], [])

        media_rule = next(
            rule
            for rule in result["rules"]
            if rule.get("selector") == ".card"
        )

        self.assertEqual(
            media_rule["at_rule_context"],
            ["@media (min-width: 768px)"],
        )

    def test_important_flag_is_preserved(self):
        result = inspect_css_structure()

        declarations = [
            declaration
            for rule in result["rules"]
            for declaration in rule["declarations"]
        ]

        border = next(
            item for item in declarations
            if item["property"] == "border"
        )

        self.assertTrue(border["important"])

    def test_repeated_inspection_is_deterministic(self):
        first = inspect_css_structure()
        second = inspect_css_structure()

        self.assertEqual(first, second)

    def test_repeated_search_is_deterministic(self):
        first = search_css("--spacing")
        second = search_css("--spacing")

        self.assertEqual(first, second)

class TestAgentReliability(unittest.TestCase):

    def setUp(self):
        _cached_answer.cache_clear()

    def tearDown(self):
        _cached_answer.cache_clear()

    def test_empty_question_does_not_call_model(self):
        with patch("agent._cached_answer") as cached:
            answer = ask_css_question("   ")

        self.assertIn("Please enter a question", answer)
        cached.assert_not_called()

    def test_identical_question_uses_cache(self):
        question = "What is the brand color?"
        css_digest = "test-css-hash"
        model_name = "test-model"

        with patch(
            "agent._call_model",
            return_value="The brand color is #1565c0.",
        ) as model:
            first = _cached_answer(
                question, css_digest, model_name
            )
            second = _cached_answer(
                question, css_digest, model_name
            )

        self.assertEqual(first, second)
        self.assertEqual(model.call_count, 1)

    def test_changed_css_content_gets_fresh_answer(self):
        question = "What is the brand color?"

        with patch(
            "agent._call_model",
            side_effect=["Old answer", "New answer"],
        ) as model:
            old_answer = _cached_answer(
                question, "old-css-hash", "test-model"
            )
            new_answer = _cached_answer(
                question, "new-css-hash", "test-model"
            )

        self.assertNotEqual(old_answer, new_answer)
        self.assertEqual(model.call_count, 2)
if __name__ == "__main__":
    unittest.main(verbosity=2)