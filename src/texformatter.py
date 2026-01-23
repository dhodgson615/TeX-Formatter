from __future__ import annotations

from argparse import ArgumentParser
from functools import reduce
from re import match
from shutil import copy2

# TODO: Make a final pass that cleans up multiple blank lines and trims trailing spaces


def indent_environments(
    lines: list[str], indent_str: str = "    "
) -> list[str]:
    """Indents LaTeX environments defined by \\begin{...} and
    \\end{...}
    """
    env_stack: list[str] = []
    new_lines = []
    in_verbatim = False

    for line in lines:
        stripped = line.strip()

        if in_verbatim:
            if stripped.startswith("\\end{verbatim}"):
                in_verbatim = False

            else:
                new_lines.append(line)
                continue

        if stripped.startswith("\\end{") and env_stack:
            env_stack.pop()

        new_lines.append(indent_str * len(env_stack) + stripped)
        m = match(r"\\begin\{([^}]+)}", stripped)

        if m:
            env = m.group(1)
            env_stack.append(env)

            if env == "verbatim":
                in_verbatim = True

    return new_lines


def indent_section_level(
    lines: list[str],
    command: str,
    exit_commands: list[str],
    indent_str: str = "    ",
) -> list[str]:
    """Generic indentation function for sections, subsections, etc."""
    in_section, in_verbatim = False, False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        in_verbatim = (
            True
            if stripped.startswith("\\begin{verbatim}")
            else (
                False
                if stripped.startswith("\\end{verbatim}")
                else in_verbatim
            )
        )

        if (
            in_verbatim
            and not stripped.startswith("\\begin{verbatim}")
            and not stripped.startswith("\\end{verbatim}")
        ):
            new_lines.append(line)
            continue

        current_line_lstripped = line.lstrip(" \t")
        current_indent_chars = len(line) - len(current_line_lstripped)

        current_indent_level = (
            current_indent_chars // len(indent_str)
            if len(indent_str) > 0
            else 0
        )

        new_indent_level, in_section = (
            (current_indent_level, True)
            if stripped.startswith(command)
            else (
                (
                    (current_indent_level, False)
                    if (
                        any(stripped.startswith(cmd) for cmd in exit_commands)
                        or stripped == "\\end{document}"
                    )
                    else (current_indent_level + 1, in_section)
                )
                if in_section
                else (current_indent_level, in_section)
            )
        )

        new_lines.append(indent_str * new_indent_level + stripped)

    return new_lines


def final_cleanup(lines: list[str]) -> list[str]:
    """Trim trailing spaces and collapse multiple blank lines into one.
    Also remove leading/trailing blank lines."""
    cleaned: list[str] = []
    blank_count = 0

    for line in lines:
        line = line.rstrip()

        if line == "":
            blank_count += 1

            if blank_count <= 1:
                cleaned.append("")

        else:
            blank_count = 0
            cleaned.append(line)

    while cleaned and cleaned[0] == "":
        cleaned.pop(0)

    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return cleaned


def indent_latex(code: str, indent_str: str = "    ") -> str:  # TODO: rewrite in such a way that doesn't shadow `lines`
    """Main Function: Indent LaTeX Code"""
    lines = reduce(
        lambda lines, level: indent_section_level(
            list(lines), level[0], level[1], indent_str
        ),
        [
            ("\\chapter", ["\\chapter", "\\section"]),
            ("\\section", ["\\chapter", "\\section"]),
            ("\\subsection", ["\\chapter", "\\section", "\\subsection"]),
            (
                "\\subsubsection",
                [
                    "\\chapter",
                    "\\section",
                    "\\subsection",
                    "\\subsubsection",
                ],
            ),
        ],
        indent_environments(code.split("\n"), indent_str),
    )

    cleaned = final_cleanup(list(lines))
    return "\n".join(cleaned)


def main() -> None:
    """Main function for the LaTeX formatter."""
    parser = ArgumentParser(
        description="Format LaTeX source code with proper indentation."
    )

    parser.add_argument("file", help="LaTeX file to format")

    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Edit the file in place (default: print to stdout)",
    )

    parser.add_argument(
        "-b",
        "--backup",
        action="store_true",
        help="Create a backup of the original file before editing in place",
    )

    parser.add_argument(
        "-s",
        "--spaces",
        type=int,
        default=4,
        help="Number of spaces per indent level (default: 4)",
    )

    parser.add_argument(
        "-t",
        "--tabs",
        action="store_true",
        help="Use tab character instead of spaces for indentation",
    )

    args = parser.parse_args()
    indent_str = "\t" if args.tabs else " " * args.spaces

    with open(args.file, "r", encoding="utf-8") as f:
        latex_code = f.read()

    formatted_code = indent_latex(latex_code, indent_str)

    if args.in_place:
        if args.backup:
            backup_file = args.file + ".bak"
            copy2(args.file, backup_file)
            print(f"Backup created: {backup_file}")

        with open(args.file, "w", encoding="utf-8") as f:
            f.write(formatted_code)

        print(f"File formatted in place: {args.file}")

    else:
        print("\n\n" + formatted_code + "\n\n")


if __name__ == "__main__":
    main()
