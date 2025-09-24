"""Simple web interface for TeX-Formatter. This Flask app provides a
minimalistic web interface for formatting LaTeX code.
"""

from __future__ import annotations

from typing import Any

import os
from flask import Flask, jsonify, render_template, request

try:
    from . import texformatter
except ImportError:
    # Fallback for when the module is imported directly
    import texformatter

# Configure Flask to look for templates and static files from the parent directory
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))


@app.route("/")
def index() -> str:
    """Render the main page with the TeX formatter interface."""
    return render_template("index.html")


@app.route("/format", methods=["POST"])
def format_latex() -> tuple[Any, int] | Any:  # TODO: fix type
    """Format LaTeX code and return the result."""
    data = request.get_json()

    if not data or "latex_code" not in data:
        return jsonify({"error": "No LaTeX code provided"}), 400

    latex_code = data["latex_code"]
    indent_str = data.get("indent_str", "    ")  # Default to 4 spaces

    try:
        formatted_code = texformatter.indent_latex(latex_code, indent_str)
        return jsonify({"formatted_code": formatted_code})

    except Exception as e:
        return jsonify({"error": f"Error formatting code: {str(e)}"}), 500


# Entry point moved to ../app.py
