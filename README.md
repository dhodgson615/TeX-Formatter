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

## Installation

### Command Line Interface

The command line interface requires only Python 3.7+ and uses only standard library modules. No additional installation is needed:

```bash
python3 texformatter.py file.tex
```

### Web Interface

For the web interface, you need to install Flask and its dependencies:

```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.1.2
- Required dependencies (Werkzeug, Jinja2, etc.)

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

TeX-Formatter includes a modern web interface for easy online formatting.

**Quick Start:**
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `python3 app.py`
3. Open your browser to `http://localhost:8080`

**Features:**
- Clean, minimalistic design with a warm coffee shop theme
- Two large text areas for easy paste-and-format workflow
- Multiple indentation options (4 spaces, 2 spaces, or tabs)
- Copy to clipboard functionality
- Responsive design for desktop and mobile
- Keyboard shortcuts:
  - Ctrl+Enter (Cmd+Enter on Mac): Format the code
  - Ctrl+Shift+C (Cmd+Shift+C on Mac): Copy formatted code

**API Endpoint:**

The web interface exposes a REST API endpoint:

**POST /format**
- Content-Type: application/json
- Body: `{"latex_code": "your code here", "indent_str": "    "}`
- Response: `{"formatted_code": "formatted result"}` or `{"error": "error message"}`

Example using curl:
```bash
curl -X POST http://localhost:8080/format \
  -H "Content-Type: application/json" \
  -d '{"latex_code": "\\begin{document}\nHello\n\\end{document}", "indent_str": "    "}'
```

**Technical Details:**

The web interface is built using:
- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla HTML, CSS, and JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Typography**: System fonts with monospace for code areas

**Troubleshooting:**

*Server won't start:*
- Check that Python 3.7+ is installed: `python3 --version`
- Ensure Flask is installed: `pip list | grep Flask`
- Check if port 8080 is already in use

*Formatting errors:*
- Verify your LaTeX code syntax
- Check browser console for JavaScript errors
- Look at the Flask server logs for detailed error messages

*Browser compatibility:*
- Modern browsers (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- JavaScript must be enabled
- Cookies are not required

**Development:**

File Structure:
```
├── app.py           # Flask application entry point
├── texformatter.py  # CLI entry point
├── src/
│   ├── app.py       # Flask application logic
│   └── texformatter.py  # Core formatting logic
├── test/
│   └── test_texformatter.py  # Unit tests
├── examples/
│   ├── simple_document.tex   # Sample LaTeX document
│   ├── test_document.tex     # Test document with various features
│   └── environments_test.tex # Environment testing document
├── templates/
│   └── index.html   # Main page template
├── static/
│   ├── style.css    # Stylesheet
│   └── script.js    # JavaScript functionality
└── requirements.txt # Python dependencies
```

You can customize the web interface by:
- Modifying `static/style.css` for appearance
- Updating `static/script.js` for functionality
- Editing `templates/index.html` for layout
- Adjusting `src/app.py` for server behavior

The core formatting logic is in `src/texformatter.py` and is shared between the CLI and web interface.
