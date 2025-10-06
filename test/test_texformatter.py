import sys
from os import path, remove, rmdir
from subprocess import run
from sys import executable
from tempfile import mkdtemp
from unittest import TestCase, main, mock

from src import texformatter


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

    def test_verbatim_environment_preserves_content(self) -> None:
        """Test that content inside verbatim environments is preserved exactly."""
        input_lines = [
            "\\begin{document}",
            "Some text",
            "\\begin{verbatim}",
            "Code block",
            '    print("Hello World")',
            "if True:",
            "    pass",
            "\\end{verbatim}",
            "More text",
            "\\end{document}",
        ]

        expected = [
            "\\begin{document}",
            "    Some text",
            "    \\begin{verbatim}",
            "Code block",
            '    print("Hello World")',
            "if True:",
            "    pass",
            "    \\end{verbatim}",
            "    More text",
            "\\end{document}",
        ]

        result = texformatter.indent_environments(input_lines)
        self.assertEqual(result, expected)

    def test_verbatim_environment_with_sections(self) -> None:
        """Test that verbatim content is preserved when mixed with sections."""
        input_code = """\\begin{document}
\\section{Code Examples}
Here is some code:
\\begin{verbatim}
def hello():
    print("Hello")
    if True:
        print("World")
\\end{verbatim}
That was the code.
\\end{document}"""

        expected = """\\begin{document}
    \\section{Code Examples}
        Here is some code:
        \\begin{verbatim}
def hello():
    print("Hello")
    if True:
        print("World")
        \\end{verbatim}
        That was the code.
\\end{document}"""

        result = texformatter.indent_latex(input_code)
        self.assertEqual(result, expected)

    def test_nested_verbatim_in_itemize(self) -> None:
        """Test verbatim environment inside other environments."""
        input_lines = [
            "\\begin{document}",
            "\\begin{itemize}",
            "\\item Here is code:",
            "\\begin{verbatim}",
            "x = 1",
            "  y = 2",
            "\\end{verbatim}",
            "\\item More text",
            "\\end{itemize}",
            "\\end{document}",
        ]

        expected = [
            "\\begin{document}",
            "    \\begin{itemize}",
            "        \\item Here is code:",
            "        \\begin{verbatim}",
            "x = 1",
            "  y = 2",
            "        \\end{verbatim}",
            "        \\item More text",
            "    \\end{itemize}",
            "\\end{document}",
        ]

        result = texformatter.indent_environments(input_lines)
        self.assertEqual(result, expected)


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.tex")

        # Create a test LaTeX file
        with open(self.test_file, "w") as f:
            f.write("\\begin{document}\nHello\n\\end{document}\n")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if path.exists(self.test_file):
            remove(self.test_file)

        backup_file = self.test_file + ".bak"

        if path.exists(backup_file):
            remove(backup_file)

        rmdir(self.temp_dir)

    def test_backup_creation(self) -> None:
        """Test that backup files are created when requested."""

        # Mock command line arguments
        argv_args = [
            "texformatter.py",
            self.test_file,
            "--in-place",
            "--backup",
        ]

        with mock.patch.object(sys, "argv", argv_args):
            texformatter.main()

        # Check that backup file was created
        backup_file = self.test_file + ".bak"
        self.assertTrue(path.exists(str(backup_file)))

    def test_cli_entry_point(self) -> None:
        """Test running texformatter.py as a script."""
        result = subprocess.run(
            [executable, "texformatter.py", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertIn("usage", result.stdout)

    def test_main_invalid_file(self) -> None:
        """Test main() with a missing file argument."""
        argv_args = ["texformatter.py", "nonexistent.tex"]
        with mock.patch.object(sys, "argv", argv_args):
            with self.assertRaises(FileNotFoundError):
                texformatter.main()


if __name__ == "__main__":
    unittest.main()
