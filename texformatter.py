#!/usr/bin/env python3
"""
This script formats LaTeX source code using a series of indentation
passes. It handles environments, chapters, sections, subsections, and
subsubsections.

Usage: python indent_latex.py input.tex
"""


import re
import sys
from re import Match


def pass1(lines: list[str]) -> list[str]:
    """First Pass: Environment Indentation.  This function indents LaTeX
    environments defined by \\begin{...} and \\end{...}. Indentation
    increases for \\begin and decreases for \\end.
    """
    env_stack: list[str] = []
    new_lines: list[str] = []

    for line in lines:
        stripped: str = line.strip()
        if stripped.startswith("\\end{"):
            if env_stack:  # Only pop if the stack is not empty.
                env_stack.pop()

        current_indent: int = len(env_stack)

        indented_line: str = "    " * current_indent + stripped
        new_lines.append(indented_line)
        if stripped.startswith("\\begin{"):
            env_match: Match[str] | None = re.match(
                r"\\begin\{([^}]+)\}", stripped
            )
            if env_match:
                env_name: str = env_match.group(1)
                env_stack.append(env_name)

    return new_lines


def pass2(lines: list[str]) -> list[str]:
    """Second Pass: Chapter Indentation. Adjusts indentation for
    \\chapter commands and their content. Lines within a chapter are
    indented until a new chapter, section, or end of document.
    """
    in_chapter: bool = False
    new_lines: list[str] = []

    for line in lines:
        stripped: str = line.strip()
        current_indent: int = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\chapter"):
            new_indent: int = current_indent
            in_chapter = True
        elif in_chapter:
            if (
                any(
                    stripped.startswith(cmd)
                    for cmd in ("\\chapter", "\\section")
                )
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_chapter = False
            else:
                new_indent = current_indent + 4

        else:
            new_indent = current_indent

        new_line: str = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def pass3(lines: list[str]) -> list[str]:
    """Third Pass: Section Indentation. Adjusts indentation for
    \\section commands and their content. Lines within a section are
    indented until a new chapter/section or end of document.
    """
    in_section: bool = False
    new_lines: list[str] = []

    for line in lines:
        stripped: str = line.strip()
        current_indent: int = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\section"):
            new_indent: int = current_indent
            in_section = True

        elif in_section:
            if (
                any(
                    stripped.startswith(cmd)
                    for cmd in ("\\chapter", "\\section")
                )
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_section = False
            else:
                new_indent = current_indent + 4

        else:
            new_indent = current_indent

        new_line: str = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def pass4(lines: list[str]) -> list[str]:
    """Fourth Pass: Subsection Indentation. Adjusts indentation for
    \\subsection commands and their content. Lines within a subsection
    are indented until a new chapter/section/subsection or end of the
    document.
    """
    in_subsection: bool = False
    new_lines: list[str] = []

    for line in lines:
        stripped: str = line.strip()
        current_indent: int = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\subsection"):
            new_indent: int = current_indent
            in_subsection = True
        elif in_subsection:
            if (
                any(
                    stripped.startswith(cmd)
                    for cmd in ("\\chapter", "\\section", "\\subsection")
                )
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_subsection = False
            else:
                new_indent = current_indent + 4
        else:
            new_indent = current_indent

        new_line: str = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def pass5(lines: list[str]) -> list[str]:
    """Fifth Pass: Subsubsection Indentation. Adjusts indentation for
    \\subsubsection commands and their content. Lines within a
    subsubsection are indented until a new chapter, section, subsection,
    subsubsection or end of document.
    """
    in_subsubsection: bool = False
    new_lines: list[str] = []

    for line in lines:
        stripped: str = line.strip()
        current_indent: int = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\subsubsection"):
            new_indent: int = current_indent
            in_subsubsection = True
        elif in_subsubsection:
            if (
                any(
                    stripped.startswith(cmd)
                    for cmd in (
                        "\\chapter",
                        "\\section",
                        "\\subsection",
                        "\\subsubsection",
                    )
                )
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_subsubsection = False
            else:
                new_indent = current_indent + 4

        else:
            new_indent = current_indent

        new_line: str = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def indent_latex(code: str) -> str:
    """Main Function: Indent LaTeX Code. Applies all five indentation
    passes sequentially to the input LaTeX code string. Returns the
    fully formatted LaTeX code.
    """
    return "\n".join(pass5(pass4(pass3(pass2(pass1(code.split("\n")))))))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python indent_latex.py input.tex")
        sys.exit(1)

    file_path: str = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        latex_code: str = f.read()

    print("\n\n" + indent_latex(latex_code) + "\n\n")
