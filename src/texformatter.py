from __future__ import annotations

from argparse import ArgumentParser
from functools import reduce
from re import match
from shutil import copy2


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

        if stripped.startswith("\\begin{verbatim}"):
            in_verbatim = True
            new_lines.append(line)
            continue

        if in_verbatim:
            if stripped.startswith("\\end{verbatim}"):
                in_verbatim = False
                new_lines.append(line)
                continue

            new_lines.append(line)
            continue

        current_line_lstripped = line.lstrip(" \t")
        current_indent_chars = len(line) - len(current_line_lstripped)

        current_indent_level = (
            current_indent_chars // len(indent_str)
            if len(indent_str) > 0
            else 0
        )

        if stripped.startswith(command):
            new_indent_level = current_indent_level
            in_section = True

        elif in_section:
            if (
                any(stripped.startswith(cmd) for cmd in exit_commands)
                or stripped == "\\end{document}"
            ):
                new_indent_level = current_indent_level
                in_section = False

            else:
                new_indent_level = current_indent_level + 1

        else:
            new_indent_level = current_indent_level

        new_lines.append(indent_str * new_indent_level + stripped)

    return new_lines


def collapse_and_trim_lines(lines: list[str]) -> list[str]:
    """Trim trailing spaces from each line and collapse multiple
    consecutive blank lines into one."""
    result: list[str] = []
    blank_count = 0

    for line in lines:
        line = line.rstrip()

        if line == "":
            blank_count += 1

            if blank_count <= 1:
                result.append("")

        else:
            blank_count = 0
            result.append(line)

    return result


def trim_edge_blank_lines(lines: list[str]) -> list[str]:
    """Remove leading and trailing blank lines from the list."""
    cleaned = lines[:]

    while cleaned and cleaned[0] == "":
        cleaned.pop(0)

    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return cleaned


def final_cleanup(
    lines: list[str],
) -> list[str]:
    """Trim trailing spaces, collapse multiple blank lines into one,
    and remove leading/trailing blank lines by delegating to focused helpers.
    """
    collapsed = collapse_and_trim_lines(lines)
    trimmed = trim_edge_blank_lines(collapsed)
    return trimmed


def split_into_lines(code: str) -> list[str]:
    """Split code into lines without adding an extra trailing empty line."""
    return code.splitlines()


def get_section_levels() -> list[tuple[str, list[str]]]:
    """Return the ordered section levels and their exit commands."""
    return [
        ("\\chapter", ["\\chapter", "\\section"]),
        ("\\section", ["\\chapter", "\\section"]),
        ("\\subsection", ["\\chapter", "\\section", "\\subsection"]),
        (
            "\\subsubsection",
            ["\\chapter", "\\section", "\\subsection", "\\subsubsection"],
        ),
    ]


def apply_environment_indentation(
    lines: list[str], indent_str: str
) -> list[str]:
    """Apply environment-based indentation first (begin/end, verbatim
    handling)."""
    return indent_environments(lines, indent_str)


def apply_section_indents(lines: list[str], indent_str: str) -> list[str]:
    """Apply section/subsection indentation levels in order using a
    single reduce.
    """
    return reduce(
        lambda acc, pair: indent_section_level(
            acc, pair[0], pair[1], indent_str
        ),
        get_section_levels(),
        lines,
    )


def indent_latex(code: str, indent_str: str = "    ") -> str:
    """Main Function: Indent LaTeX Code"""
    src_lines = split_into_lines(code)
    env_indented = apply_environment_indentation(src_lines, indent_str)
    section_indented = apply_section_indents(env_indented, indent_str)
    cleaned = final_cleanup(section_indented)
    return "\n".join(cleaned)


def main() -> None:
    """Main function for the LaTeX formatter"""
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
