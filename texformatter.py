#!/usr/bin/env python3
"""
This script formats LaTeX source code by applying a series of indentation
passes. Each pass handles a specific LaTeX construct (e.g., environments,
chapters, sections, subsections, subsubsections) by adjusting the indentation
level based on the hierarchy.

The process is broken into five passes:
    1. Environment Indentation: Handles LaTeX environments (\begin{} and
       \end{}).
    2. Chapter Indentation: Handles chapters and indents content within
       chapters.
    3. Section Indentation: Handles sections and indents content within
       sections.
    4. Subsection Indentation: Handles subsections and indents content within
       them.
    5. Subsubsection Indentation: Handles subsubsections similarly.

Usage:
    Run the script with the LaTeX file as an argument:
        python indent_latex.py input.tex

The formatted LaTeX code is printed to the standard output.
"""

# Import regular expressions module for pattern matching and system module for
# command-line arguments.

import re
import sys


def pass1_env_indent(lines) -> list[str]:
    """
    First Pass: Environment Indentation

    This function processes the LaTeX code to indent environments properly.
    LaTeX environments are defined with \begin{...} and \end{...} commands.
    Each time a \begin is encountered, the indentation level increases,
    and when an \end is encountered, the level decreases.

    Args:
        lines (list of str): A list of strings, where each string is a line of
                             the LaTeX code.

    Returns:
        list of str: A new list of strings with proper indentation for
                     environments.

    Detailed Process:
        1. Initialize an empty stack (env_stack) to keep track of nested
           environments.
        2. Iterate over each line:
            a. Strip leading/trailing whitespace for consistency.
            b. If the line starts with "\end{", pop an element from the stack
               (if available) before processing the line, reducing the current
               indentation.
            c. Calculate the current indentation level based on the size of the
               stack.
            d. Prepend the line with spaces ("    " * current indent level).
            e. After processing the line, if it starts with "\begin{", extract
               the environment name and push it onto the stack, increasing
               indentation for subsequent lines.
        3. Return the new list of indented lines.
    """
    # Stack to hold current environments.
    env_stack = []
    # List to accumulate the new indented lines.
    new_lines = []

    # Process each line in the LaTeX code.
    for line in lines:
        # Remove any leading and trailing whitespace.
        stripped = line.strip()

        # If the line is an environment closing command, adjust the environment
        # stack first.
        if stripped.startswith("\\end{"):
            if env_stack:  # Only pop if the stack is not empty.
                env_stack.pop()

        # Current indentation is based on how many environments are open.
        current_indent = len(env_stack)

        # Create a new line by adding indentation spaces (4 spaces per
        # indentation level).
        indented_line = "    " * current_indent + stripped
        new_lines.append(indented_line)

        # If the line is an environment opening command, process after adding
        # the line.
        if stripped.startswith("\\begin{"):
            # Extract the name of the environment using a regular expression.
            env_match = re.match(r"\\begin\{([^}]+)\}", stripped)
            if env_match:
                env_name = env_match.group(1)
                # Add the environment name to the stack to increase indentation
                # level.
                env_stack.append(env_name)

    # Return the list of new, indented lines.
    return new_lines


def pass2_chapter_indent(lines) -> list[str]:
    """
    Second Pass: Chapter Indentation

    This function further processes the indented LaTeX code to adjust the
    indentation for chapters and their content. When a chapter command is
    encountered, it sets a flag indicating that subsequent lines are part of
    the chapter, and indents those lines until a new chapter, section, or the
    end of the document is reached.

    Args:
        lines (list of str): A list of strings representing the lines of LaTeX
                             code from the previous pass.

    Returns:
        list of str: A new list of strings with adjusted indentation for
                     chapters and their content.

    Detailed Process:
        1. Iterate over each line and remove extra spaces.
        2. Check if the line is a chapter command:
            - If it is, do not add extra indentation for that line and set the
              chapter context flag.
        3. If inside a chapter context:
            - Indent subsequent lines by adding 4 spaces, until another
              chapter, section, or end document command is found.
        4. If the context ends, continue processing without extra indentation.
    """
    # Flag to indicate whether we are inside a chapter content block.
    in_chapter = False
    # List to store the new lines after processing.
    new_lines = []

    # Process each line.
    for line in lines:
        # Remove extra whitespace from both ends.
        stripped = line.strip()
        # Calculate the current indentation by measuring leading spaces.
        current_indent = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\chapter"):
            # For a chapter line, maintain the current indentation.
            new_indent = current_indent
            # Activate the chapter content context.
            in_chapter = True
        elif in_chapter:
            # Check if the current line signals a context change (new chapter,
            # section, or document end).
            if (
                any(stripped.startswith(cmd) for cmd in ("\\chapter", "\\section"))
                or stripped == "\\end{document}"
            ):
                # Exit the chapter context.
                new_indent = current_indent
                in_chapter = False
            else:
                # For content inside the chapter, add an extra indentation
                # level.
                new_indent = current_indent + 4
        else:
            # For lines outside the chapter context, keep the original
            # indentation.
            new_indent = current_indent

        # Reconstruct the line with the new indentation.
        new_line = " " * new_indent + stripped
        new_lines.append(new_line)

    # Return the updated list of lines.
    return new_lines


def pass3_section_indent(lines) -> list[str]:
    """
    Third Pass: Section Indentation

    This function adjusts the indentation for sections and their content. Much
    like the chapter indentation, when a section command is encountered,
    subsequent lines (considered part of that section) are indented further
    until another chapter/section command or end of document is encountered.

    Args:
        lines (list of str): List of strings from the previous pass with
                             chapters processed.

    Returns:
        list of str: New list of strings with proper indentation for sections.
    """
    # Flag indicating whether we are inside a section block.
    in_section = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Calculate current indentation by subtracting the leading spaces
        # count.
        current_indent = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\section"):
            # A section command resets the indentation and activates section
            # context.
            new_indent = current_indent
            in_section = True
        elif in_section:
            # If the line starts with chapter or section commands or is the end
            # of document, exit section context.
            if (
                any(stripped.startswith(cmd) for cmd in ("\\chapter", "\\section"))
                or stripped == "\\end{document}"
            ):
                new_indent = current_indent
                in_section = False
            else:
                # Otherwise, indent the content within the section.
                new_indent = current_indent + 4
        else:
            new_indent = current_indent

        new_line = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def pass4_subsection_indent(lines) -> list[str]:
    """
    Fourth Pass: Subsection Indentation

    This function processes the LaTeX code for subsection commands. It works
    similarly to previous passes by indenting content within subsections by
    increasing the indentation level for lines following a subsection command,
    until another higher-level command or document end is encountered.

    Args:
        lines (list of str): List of strings from the previous pass with
                             section indentation applied.

    Returns:
        list of str: New list of strings with proper indentation for
                     subsections.
    """
    # Flag indicating whether we are currently within a subsection.
    in_subsection = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Determine current indentation by counting leading spaces.
        current_indent = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\subsection"):
            # When a subsection starts, use the current indentation and
            # activate the context.
            new_indent = current_indent
            in_subsection = True
        elif in_subsection:
            # Check if the current line signals a new chapter, section, or
            # subsection command, or document end.
            if (
                any(
                    stripped.startswith(cmd)
                    for cmd in ("\\chapter", "\\section", "\\subsection")
                )
                or stripped == "\\end{document}"
            ):
                # End the subsection context.
                new_indent = current_indent
                in_subsection = False
            else:
                # For content inside the subsection, increase the indentation
                # level.
                new_indent = current_indent + 4
        else:
            new_indent = current_indent

        new_line = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def pass5_subsubsection_indent(lines) -> list[str]:
    """
    Fifth Pass: Subsubsection Indentation

    This final pass adjusts the indentation for subsubsections. It follows the
    same logic as the previous passes: when a subsubsection command is
    encountered, the content following it is indented until a new command
    (chapter, section, subsection, or subsubsection) or the end of the document
    is reached.

    Args:
        lines (list of str): List of strings from the previous pass with
                             subsection indentation.

    Returns:
        list of str: A new list of strings with proper indentation for
                     subsubsections.
    """
    # Flag to indicate if we are inside a subsubsection.
    in_subsubsection = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        # Compute the current number of leading spaces.
        current_indent = len(line) - len(line.lstrip(" "))

        if stripped.startswith("\\subsubsection"):
            # For the subsubsection command itself, use the current
            # indentation.
            new_indent = current_indent
            in_subsubsection = True
        elif in_subsubsection:
            # Check for commands that indicate the end of the subsubsection
            # context.
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
                # Indent content within the subsubsection by adding extra
                # spaces.
                new_indent = current_indent + 4
        else:
            new_indent = current_indent

        new_line = " " * new_indent + stripped
        new_lines.append(new_line)

    return new_lines


def indent_latex(code: str) -> str:
    """
    Main Function: Indent LaTeX Code

    This function takes a single string containing LaTeX code and applies all
    five indentation passes sequentially. It splits the input code into lines,
    applies the passes, and then joins the lines back together to form the
    final formatted LaTeX code.

    Args:
        code (str): A string containing the LaTeX source code to be formatted.

    Returns:
        str: The formatted LaTeX code with appropriate indentation.
    """
    # Split the entire LaTeX code into individual lines.
    lines = code.split("\n")

    # Apply each pass in order:
    p1 = pass1_env_indent(lines)         # First pass:  environments
    p2 = pass2_chapter_indent(p1)        # Second pass: chapters
    p3 = pass3_section_indent(p2)        # Third pass:  sections
    p4 = pass4_subsection_indent(p3)     # Fourth pass: subsections
    p5 = pass5_subsubsection_indent(p4)  # Fifth pass:  subsubsections

    # Combine the processed lines into a single string with newline separators.
    return "\n".join(p5)


# If this script is run as the main program (not imported as a module), execute
# the following code.
if __name__ == "__main__":
    # Check that the script has been provided with an input filename.
    if len(sys.argv) < 2:
        # If no filename is provided, print the usage information and exit.
        print("Usage: python indent_latex.py input.tex")
        sys.exit(1)

    # Open and read the contents of the provided LaTeX file.
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        latex_code = f.read()

    # Call the main function to process the LaTeX code.
    formatted = indent_latex(latex_code)

    # Print two newlines for separation, then print the formatted code followed
    # by two newlines for clarity.
    print("\n\n" + formatted + "\n\n")
