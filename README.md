# TeX-Formatter
Python script that automatically formats .tex files based on my somewhat opinionated formatting style. It formats LaTeX source code by applying a series of indentation passes. Each pass handles a specific LaTeX construct (e.g., environments, chapters, sections, subsections, subsubsections) by adjusting the indentation level based on the hierarchy.

## Functionality

The script performs the indentation in five distinct passes:

1.  **Environment Indentation:** Handles LaTeX environments defined by `\begin{...}` and `\end{...}`. It increases the indentation level when a `\begin` command is encountered and decreases it upon seeing an `\end`.

2.  **Chapter Indentation:** Indents the content within `\chapter` commands. It increases the indentation level for lines following a `\chapter` until another chapter, section, or the end of the document is found.

3.  **Section Indentation:** Similarly, indents the content within `\section` commands. Indentation increases until another chapter, section, or the end of the document is encountered.

4.  **Subsection Indentation:** Handles indentation for content within `\subsection` commands. The indentation continues until a chapter, section, subsection, or the end of the document is found.

5.  **Subsubsection Indentation:** Applies indentation to content within `\subsubsection` commands, stopping when a chapter, section, subsection, subsubsection, or the end of the document is reached.

## Usage

To use the script, run it from the command line with the LaTeX file you want to format as an argument:

```bash
python indent_latex.py input.tex
```
