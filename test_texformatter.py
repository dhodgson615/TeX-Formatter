"""Unit tests for texformatter.py functions."""

import os
import sys
import tempfile
import unittest
import unittest.mock

import texformatter


class TestTexFormatter(unittest.TestCase):
    """Test cases for the LaTeX formatter functions."""

    def test_indent_environments_simple(self) -> None:
        """Test basic environment indentation."""
        input_lines = [
            "\\documentclass{article}",
            "\\begin{document}",
            "Hello world",
            "\\end{document}",
        ]

        expected = [
            "\\documentclass{article}",
            "\\begin{document}",
            "    Hello world",
            "\\end{document}",
        ]

        result = texformatter.indent_environments(input_lines)
        self.assertEqual(result, expected)

    def test_indent_environments_nested(self) -> None:
        """Test nested environment indentation."""
        input_lines = [
            "\\begin{document}",
            "\\begin{itemize}",
            "\\item First item",
            "\\begin{enumerate}",
            "\\item Nested item",
            "\\end{enumerate}",
            "\\end{itemize}",
            "\\end{document}",
        ]

        expected = [
            "\\begin{document}",
            "    \\begin{itemize}",
            "        \\item First item",
            "        \\begin{enumerate}",
            "            \\item Nested item",
            "        \\end{enumerate}",
            "    \\end{itemize}",
            "\\end{document}",
        ]

        result = texformatter.indent_environments(input_lines)
        self.assertEqual(result, expected)

    def test_indent_environments_custom_indent(self) -> None:
        """Test environment indentation with custom indent string."""
        input_lines = ["\\begin{document}", "Hello world", "\\end{document}"]
        expected = ["\\begin{document}", "  Hello world", "\\end{document}"]
        result = texformatter.indent_environments(input_lines, "  ")
        self.assertEqual(result, expected)

    def test_indent_environments_tabs(self) -> None:
        """Test environment indentation with tabs."""
        input_lines = ["\\begin{document}", "Hello world", "\\end{document}"]
        expected = ["\\begin{document}", "\tHello world", "\\end{document}"]
        result = texformatter.indent_environments(input_lines, "\t")
        self.assertEqual(result, expected)

    def test_indent_section_level_chapter(self) -> None:
        """Test chapter level indentation."""
        input_lines = [
            "\\documentclass{book}",
            "\\chapter{First Chapter}",
            "Chapter content",
            "\\section{Section}",
            "Section content",
            "\\chapter{Second Chapter}",
            "More content",
        ]

        expected = [
            "\\documentclass{book}",
            "\\chapter{First Chapter}",
            "    Chapter content",
            "\\section{Section}",
            "Section content",
            "\\chapter{Second Chapter}",
            "    More content",
        ]

        result = texformatter.indent_section_level(
            input_lines, "\\chapter", ["\\chapter", "\\section"]
        )

        self.assertEqual(result, expected)

    def test_indent_section_level_section(self) -> None:
        """Test section level indentation."""
        input_lines = [
            "\\section{First Section}",
            "Section content",
            "\\subsection{Subsection}",
            "Subsection content",
            "\\section{Second Section}",
            "More content",
        ]

        expected = [
            "\\section{First Section}",
            "    Section content",
            "    \\subsection{Subsection}",
            "    Subsection content",
            "\\section{Second Section}",
            "    More content",
        ]

        result = texformatter.indent_section_level(
            input_lines, "\\section", ["\\chapter", "\\section"]
        )

        self.assertEqual(result, expected)

    def test_indent_section_level_custom_indent(self) -> None:
        """Test section level indentation with custom indent string."""
        input_lines = ["\\section{Test Section}", "Content here"]
        expected = ["\\section{Test Section}", "  Content here"]

        result = texformatter.indent_section_level(
            input_lines, "\\section", ["\\section"], "  "
        )

        self.assertEqual(result, expected)

    def test_indent_latex_complete(self) -> None:
        """Test complete LaTeX indentation."""
        input_lines = [
            "\\documentclass{article}",
            "\\begin{document}",
            "\\chapter{Chapter}",
            "Chapter content",
            "\\section{Section}",
            "Section content",
            "\\begin{itemize}",
            "\\item Item 1",
            "\\item Item 2",
            "\\end{itemize}",
            "\\subsection{Subsection}",
            "Subsection content",
            "\\end{document}",
        ]
        input_code = "\n".join(input_lines)

        expected_lines = [
            "\\documentclass{article}",
            "\\begin{document}",
            "    \\chapter{Chapter}",
            "        Chapter content",
            "    \\section{Section}",
            "        Section content",
            "        \\begin{itemize}",
            "            \\item Item 1",
            "            \\item Item 2",
            "        \\end{itemize}",
            "        \\subsection{Subsection}",
            "            Subsection content",
            "\\end{document}",
        ]

        expected = "\n".join(expected_lines)
        result = texformatter.indent_latex(input_code)
        self.assertEqual(result, expected)

    def test_indent_latex_with_tabs(self) -> None:
        """Test complete LaTeX indentation with tabs."""
        input_lines = [
            "\\begin{document}",
            "\\section{Section}",
            "Content",
            "\\end{document}",
        ]
        input_code = "\n".join(input_lines)

        result = texformatter.indent_latex(input_code, "\t")
        lines = result.split("\n")

        # Check that tabs are used instead of spaces
        self.assertTrue(lines[1].startswith("\t\\section"))
        self.assertTrue(lines[2].startswith("\t\tContent"))

    def test_indent_latex_with_custom_spaces(self) -> None:
        """Test complete LaTeX indentation with custom space count."""
        input_lines = [
            "\\begin{document}",
            "\\section{Section}",
            "Content",
            "\\end{document}",
        ]
        input_code = "\n".join(input_lines)

        result = texformatter.indent_latex(input_code, "  ")
        lines = result.split("\n")

        # Check that 2 spaces are used per level
        self.assertTrue(lines[1].startswith("  \\section"))
        self.assertTrue(lines[2].startswith("    Content"))


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.tex")

        # Create a test LaTeX file
        with open(self.test_file, "w") as f:
            f.write("\\begin{document}\nHello\n\\end{document}\n")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        backup_file = self.test_file + ".bak"

        if os.path.exists(backup_file):
            os.remove(backup_file)

        os.rmdir(self.temp_dir)

    def test_backup_creation(self) -> None:
        """Test that backup files are created when requested."""

        # Mock command line arguments
        test_args = [
            "texformatter.py",
            self.test_file,
            "--in-place",
            "--backup",
        ]

        with unittest.mock.patch.object(sys, "argv", test_args):
            texformatter.main()

        # Check that backup file was created
        backup_file = self.test_file + ".bak"
        self.assertTrue(os.path.exists(backup_file))


if __name__ == "__main__":
    unittest.main()
