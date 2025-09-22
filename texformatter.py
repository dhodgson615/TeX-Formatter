"""This script formats LaTeX source code using a series of indentation
passes. It handles environments, chapters, sections, subsections, and
subsubsections. Usage: python3 texformatter.py input.tex [-i]"""

from __future__ import annotations

import argparse
import re


def indent_environments(lines: list[str]) -> list[str]:  # TODO: unit tests
    """Indents LaTeX environments defined by \\begin{...} and
    \\end{...}
    """
    env_stack: list[str] = []
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("\\end{") and env_stack:
            env_stack.pop()

        indented_line = "    " * len(env_stack) + stripped
        new_lines.append(indented_line)

        if stripped.startswith("\\begin{"):
            env_match = re.match(r"\\begin\{([^}]+)}", stripped)

            if env_match:
                env_stack.append(env_match.group(1))

    return new_lines


def indent_section_level(
    lines: list[str], command: str, exit_commands: list[str]
) -> list[str]:  # TODO: unit tests
    """Generic indentation function for sections, subsections, etc."""
    in_section = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        current_indent = len(line) - len(line.lstrip(" "))

        if stripped.startswith(command):
            new_indent = current_indent
            in_section = True

        elif in_section:
            if (
                any(stripped.startswith(cmd) for cmd in exit_commands)
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_section = False

            else:
                new_indent = current_indent + 4

        else:
            new_indent = current_indent

        new_lines.append(" " * new_indent + stripped)

    return new_lines


def indent_latex(code: str) -> str:  # TODO: unit tests
    """Main Function: Indent LaTeX Code"""
    lines = code.split("\n")

    # First pass: environment indentation
    lines = indent_environments(lines)

    # Define section levels and their exit conditions
    section_levels = [
        ("\\chapter", ["\\chapter", "\\section"]),
        ("\\section", ["\\chapter", "\\section"]),
        ("\\subsection", ["\\chapter", "\\section", "\\subsection"]),
        (
            "\\subsubsection",
            ["\\chapter", "\\section", "\\subsection", "\\subsubsection"],
        ),
    ]

    # Apply each section level indentation in sequence
    for command, exit_commands in section_levels:
        lines = indent_section_level(lines, command, exit_commands)

    return "\n".join(lines)


# TODO: make actual main() function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Format LaTeX source code with proper indentation."
    )

    parser.add_argument("file", help="LaTeX file to format")

    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Edit the file in place (default: print to stdout)",
    )

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        latex_code = f.read()

    formatted_code = indent_latex(latex_code)

    if args.in_place:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(formatted_code)

    else:
        print("\n\n" + formatted_code + "\n\n")

# TODO: add command line option to back up original file
# TODO: add command line option to specify number of spaces per indent level
# TODO: add command line option to specify tab character instead of spaces
# TODO: add realistic dummy LaTeX files for testing
# TODO: add unit tests for all functions
