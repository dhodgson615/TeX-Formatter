"""
Simple web interface for TeX-Formatter.

This Flask app provides a minimalistic web interface for formatting LaTeX code.
"""

from flask import Flask, render_template, request, jsonify
from texformatter import indent_latex

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page with the TeX formatter interface."""
    return render_template('index.html')


@app.route('/format', methods=['POST'])
def format_latex():
    """Format LaTeX code and return the result."""
    data = request.get_json()
    
    if not data or 'latex_code' not in data:
        return jsonify({'error': 'No LaTeX code provided'}), 400
    
    latex_code = data['latex_code']
    indent_str = data.get('indent_str', '    ')  # Default to 4 spaces
    
    try:
        formatted_code = indent_latex(latex_code, indent_str)
        return jsonify({'formatted_code': formatted_code})
    except Exception as e:
        return jsonify({'error': f'Error formatting code: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)