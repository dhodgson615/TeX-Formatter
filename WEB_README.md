# TeX-Formatter Web Interface

This document provides detailed information about the web interface for TeX-Formatter.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installing Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Required Flask dependencies (Werkzeug, Jinja2, etc.)

## Running the Web Interface

1. Navigate to the TeX-Formatter directory
2. Start the web server:
   ```bash
   python3 app.py
   ```
3. Open your web browser and go to `http://localhost:8080`

The server will start in debug mode by default, which means:
- The server will reload automatically when you make changes to the code
- Detailed error messages will be shown if something goes wrong
- The server runs on all network interfaces (0.0.0.0) on port 8080

## Using the Web Interface

### Basic Workflow

1. **Paste LaTeX Code**: Copy your LaTeX source code and paste it into the left text area
2. **Choose Indentation**: Select your preferred indentation style:
   - 4 Spaces (default)
   - 2 Spaces
   - Tabs
3. **Format**: Click the "Format LaTeX" button
4. **Copy Result**: Use the "Copy to Clipboard" button to copy the formatted code

### Features

- **Clean Interface**: Minimalistic design with a warm, professional theme
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Formatting**: Fast server-side processing
- **Multiple Indentation Options**: Choose between spaces or tabs
- **Copy to Clipboard**: One-click copying of formatted results
- **Sample Code**: Load sample LaTeX code to try the formatter
- **Keyboard Shortcuts**: 
  - Ctrl+Enter (Cmd+Enter on Mac): Format the code
  - Ctrl+Shift+C (Cmd+Shift+C on Mac): Copy formatted code

### Technical Details

The web interface is built using:
- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla HTML, CSS, and JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Typography**: System fonts with monospace for code areas

### API Endpoint

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

## Troubleshooting

### Common Issues

**Server won't start**
- Check that Python 3.7+ is installed: `python3 --version`
- Ensure Flask is installed: `pip list | grep Flask`
- Check if port 8080 is already in use

**Formatting errors**
- Verify your LaTeX code syntax
- Check browser console for JavaScript errors
- Look at the Flask server logs for detailed error messages

**Browser compatibility**
- Modern browsers (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- JavaScript must be enabled
- Cookies are not required

### Performance

- The formatter handles large documents efficiently
- Processing time depends on document complexity and length
- No document size limits imposed by the web interface
- All processing happens server-side for consistent results

## Development

### File Structure

```
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main page template
├── static/
│   ├── style.css       # Stylesheet
│   └── script.js       # JavaScript functionality
└── texformatter.py    # Core formatting logic
```

### Customization

You can customize the web interface by:
- Modifying `static/style.css` for appearance
- Updating `static/script.js` for functionality
- Editing `templates/index.html` for layout
- Adjusting `app.py` for server behavior

The core formatting logic is in `texformatter.py` and is shared between the CLI and web interface.