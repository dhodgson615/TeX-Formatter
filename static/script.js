document.addEventListener('DOMContentLoaded', () => {
    // Cache DOM elements
    const elements = {
        input: document.getElementById('latex-input'),
        output: document.getElementById('latex-output'),
        formatBtn: document.getElementById('format-btn'),
        copyBtn: document.getElementById('copy-btn'),
        customSpaces: document.getElementById('custom-spaces'),
        customRadio: document.querySelector('input[name="indent"][value="custom"]'),
        formatterSection: document.querySelector('.formatter-section'),
        controls: document.querySelector('.controls'),
        inputSection: document.querySelector('.input-section'),
        themeToggle: document.getElementById('theme-toggle'),
        themeIcon: document.querySelector('.theme-icon')
    };

    // Theme management
    const themes = {
        light: { icon: '🌙', label: 'Switch to dark mode' },
        dark: { icon: '☀️', label: 'Switch to light mode' }
    };

    // Initialize theme
    initializeTheme();

    // Event listeners
    elements.formatBtn.addEventListener('click', formatLatex);
    elements.copyBtn.addEventListener('click', copyToClipboard);
    elements.input.addEventListener('input', updateButtonStates);
    elements.themeToggle.addEventListener('click', toggleTheme);

    // Custom spaces input handling
    ['focus', 'input'].forEach(event => {
        elements.customSpaces.addEventListener(event, () => elements.customRadio.checked = true);
    });

    // Initialize UI state
    updateButtonStates();

    // Add sample button
    const addSampleBtn = document.createElement('button');
    addSampleBtn.textContent = 'Load Sample';
    addSampleBtn.className = 'copy-button';
    addSampleBtn.style.cssText = 'margin-top: 1rem; align-self: flex-start;';
    addSampleBtn.addEventListener('click', loadSample);
    elements.inputSection.appendChild(addSampleBtn);

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);

    function formatLatex() {
        const latexCode = elements.input.value.trim();
        if (!latexCode) {
            showError('Please paste some LaTeX code to format.');
            return;
        }

        // Get selected indent option
        const selectedIndent = document.querySelector('input[name="indent"]:checked').value;
        let indentStr;

        if (selectedIndent === '\\t') {
            indentStr = '\t';
        } else if (selectedIndent === 'custom') {
            const customSpaces = parseInt(elements.customSpaces.value) || 3;
            indentStr = ' '.repeat(Math.max(1, Math.min(20, customSpaces)));
        } else {
            indentStr = selectedIndent;
        }

        setLoadingState(true);
        hideError();

        fetch('/format', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({latex_code: latexCode, indent_str: indentStr})
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                } else {
                    elements.output.value = data.formatted_code;
                    elements.copyBtn.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while formatting the LaTeX code. Please try again.');
            })
            .finally(() => setLoadingState(false));
    }

    function copyToClipboard() {
        if (!elements.output.value) return;

        elements.output.select();
        elements.output.setSelectionRange(0, 99999);

        navigator.clipboard.writeText(elements.output.value)
            .then(() => {
                const originalText = elements.copyBtn.textContent;
                elements.copyBtn.textContent = 'Copied!';
                elements.copyBtn.style.background = '#6c7b7f';

                setTimeout(() => {
                    elements.copyBtn.textContent = originalText;
                    elements.copyBtn.style.background = '';
                }, 2000);
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
                showError('Could not copy to clipboard. Please select and copy manually.');
            });
    }

    function updateButtonStates() {
        const hasInput = elements.input.value.trim().length > 0;
        elements.formatBtn.disabled = !hasInput;

        if (!hasInput) {
            elements.output.value = '';
            elements.copyBtn.disabled = true;
        }
    }

    function setLoadingState(loading) {
        if (loading) {
            elements.formatBtn.disabled = true;
            elements.formatBtn.textContent = 'Formatting...';
            elements.formatterSection.classList.add('loading');
        } else {
            elements.formatBtn.textContent = 'Format LaTeX';
            elements.formatterSection.classList.remove('loading');
            updateButtonStates();
        }
    }

    function showError(message) {
        let errorDiv = document.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            elements.controls.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    function hideError() {
        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) errorDiv.style.display = 'none';
    }

    function loadSample() {
        elements.input.value = `\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
\\section{Introduction}
This is a sample document.
\\subsection{Background}
Some background information.
\\begin{itemize}
\\item First item
\\item Second item
\\end{itemize}
\\begin{equation}
E = mc^2
\\end{equation}
\\end{document}`;
        updateButtonStates();
        elements.output.value = '';
        elements.copyBtn.disabled = true;
    }

    function handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to format
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!elements.formatBtn.disabled) formatLatex();
        }

        // Ctrl/Cmd + C when output is focused to copy
        if ((e.ctrlKey || e.metaKey) && e.key === 'c' && document.activeElement === elements.output) {
            if (elements.output.value) copyToClipboard();
        }
    }

    function initializeTheme() {
        // Check for saved theme preference or default to system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        let currentTheme;
        if (savedTheme) {
            currentTheme = savedTheme;
        } else {
            currentTheme = systemPrefersDark ? 'dark' : 'light';
        }
        
        setTheme(currentTheme);
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem('theme')) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (elements.themeIcon) {
            elements.themeIcon.textContent = themes[theme].icon;
        }
        if (elements.themeToggle) {
            elements.themeToggle.setAttribute('aria-label', themes[theme].label);
        }
    }
});
