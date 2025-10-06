from __future__ import annotations

from argparse import ArgumentParser
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

        # Check if we're ending a verbatim environment
        if stripped.startswith("\\end{verbatim}"):
            in_verbatim = False

        if in_verbatim and not stripped.startswith("\\end{verbatim}"):
            new_lines.append(line)
            continue

        # Handle ending environments
        if stripped.startswith("\\end{") and env_stack:
            env_stack.pop()

        # Apply indentation
        indented_line = indent_str * len(env_stack) + stripped
        new_lines.append(indented_line)

        # Handle beginning environments
        if stripped.startswith("\\begin{"):
            env_match = match(r"\\begin\{([^}]+)}", stripped)

            if env_match:
                env_name = env_match.group(1)
                env_stack.append(env_name)

                if env_name == "verbatim":
                    in_verbatim = True

    return new_lines


def indent_section_level(
    lines: list[str],
    command: str,
    exit_commands: list[str],
    indent_str: str = "    ",
) -> list[str]:
    """Generic indentation function for sections, subsections, etc."""
    in_section = False
    in_verbatim = False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        # Track verbatim environment state
        if stripped.startswith("\\begin{verbatim}"):
            in_verbatim = True

        elif stripped.startswith("\\end{verbatim}"):
            in_verbatim = False

        # If we're inside verbatim, preserve the line exactly
        if (
            in_verbatim
            and not stripped.startswith("\\begin{verbatim}")
            and not stripped.startswith("\\end{verbatim}")
        ):
            new_lines.append(line)
            continue

        # Count current indentation in terms of indent_str units
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


def indent_latex(code: str, indent_str: str = "    ") -> str:
    """Main Function: Indent LaTeX Code"""
    lines = code.split("\n")

    # First pass: environment indentation
    lines = indent_environments(lines, indent_str)

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
        lines = indent_section_level(lines, command, exit_commands, indent_str)

    return "\n".join(lines)


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

    # Determine the indentation string
    if args.tabs:
        indent_str = "\t"

    else:
        indent_str = " " * args.spaces

    # Read the input file
    with open(args.file, "r", encoding="utf-8") as f:
        latex_code = f.read()

    # Format the code
    formatted_code = indent_latex(latex_code, indent_str)

    if args.in_place:
        # Create backup if requested
        if args.backup:
            backup_file = args.file + ".bak"
            copy2(args.file, backup_file)
            print(f"Backup created: {backup_file}")

        # Write formatted code back to the file
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(formatted_code)

        print(f"File formatted in place: {args.file}")

    else:
        print("\n\n" + formatted_code + "\n\n")


if __name__ == "__main__":
    main()
