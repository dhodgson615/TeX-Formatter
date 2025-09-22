# TeX-Formatter
Python script that automatically formats .tex files based on my somewhat
opinionated formatting style. It formats LaTeX source code by applying a series
of indentation passes. Each pass handles a specific LaTeX construct (e.g.,
environments, chapters, sections, subsections, subsubsections) by adjusting the
indentation level based on the hierarchy so that the content is nested and
visually easier to find.

## Functionality

The script performs the indentation in five distinct passes:

1.  **Environment Indentation:** Handles LaTeX environments defined by
    `\begin{...}` and `\end{...}`. It increases the indentation level when a
    `\begin` command is encountered and decreases it upon seeing an `\end`.

2.  **Chapter Indentation:** Indents the content within `\chapter` commands. It
    increases the indentation level for lines following a `\chapter` until
    another chapter, section, or the end of the document is found.

3.  **Section Indentation:** Similarly, indents the content within `\section`
    commands. Indentation increases until another chapter, section, or the end
    of the document is encountered.

4.  **Subsection Indentation:** Handles indentation for content within
    `\subsection` commands. The indentation continues until a chapter, section,
    subsection, or the end of the document is found.

5.  **Subsubsection Indentation:** Applies indentation to content within
    `\subsubsection` commands, stopping when a chapter, section, subsection,
    subsubsection, or the end of the document is reached.

## Usage

### Command Line Interface

To use the script, run it from the command line with the LaTeX file you want to
format as an argument:

```bash
python3 texformatter.py file.tex
```

By default, the script prints the formatted output to stdout. To modify the file
in place, use the `-i` or `--in-place` flag:

```bash
python3 texformatter.py -i file.tex
python3 texformatter.py --in-place file.tex
```

### Web Interface

TeX-Formatter now includes a modern web interface for easy online formatting:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the web server:
   ```bash
   python3 app.py
   ```

3. Open your browser to `http://localhost:8080`

The web interface features:
- Clean, minimalistic design with a warm coffee shop theme
- Two large text areas for easy paste-and-format workflow
- Multiple indentation options (4 spaces, 2 spaces, or tabs)
- Copy to clipboard functionality
- Responsive design for desktop and mobile
- Comprehensive technical documentation

See `WEB_README.md` for detailed web interface documentation.
