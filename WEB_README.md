# TeX-Formatter Web Interface

A simple and elegant web interface for the TeX-Formatter LaTeX code formatting tool.

## Features

- **Clean, minimalistic design** with a warm coffee shop theme
- **Two large text areas** for input and output
- **Multiple indentation options** (4 spaces, 2 spaces, or tabs)
- **Copy to clipboard** functionality
- **Load sample** button for quick testing
- **Responsive design** that works on desktop and mobile
- **Comprehensive technical documentation** included on the page

## Running the Web Interface

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask application:
   ```bash
   python3 app.py
   ```

3. Open your browser and navigate to `http://localhost:8080`

## API Usage

The web interface also provides a REST API endpoint for programmatic access:

### POST /format

Format LaTeX code via JSON API.

**Request:**
```json
{
  "latex_code": "\\begin{document}\n\\section{Test}\nContent\n\\end{document}",
  "indent_str": "    "
}
```

**Response:**
```json
{
  "formatted_code": "\\begin{document}\n    \\section{Test}\n        Content\n\\end{document}"
}
```

## Design

The web interface features:
- **Taupe/coffee shop color scheme** for a professional, warm appearance
- **Modern typography** using serif fonts for elegance
- **Responsive grid layout** that adapts to different screen sizes
- **Intuitive user experience** with clear visual feedback
- **Accessibility features** including keyboard shortcuts

## Technical Details

The web interface is built with:
- **Flask** for the backend web framework
- **Vanilla JavaScript** for client-side interactivity
- **CSS Grid** for responsive layout
- **Modern CSS** with custom properties for consistent theming

The formatting engine uses the same core `indent_latex()` function from the command-line tool, ensuring consistent results across both interfaces.