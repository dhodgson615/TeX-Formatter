// TeX-Formatter Web Interface JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const inputTextarea = document.getElementById('latex-input');
    const outputTextarea = document.getElementById('latex-output');
    const formatBtn = document.getElementById('format-btn');
    const copyBtn = document.getElementById('copy-btn');
    const indentRadios = document.querySelectorAll('input[name="indent"]');
    
    // Format button click handler
    formatBtn.addEventListener('click', formatLatex);
    
    // Copy button click handler
    copyBtn.addEventListener('click', copyToClipboard);
    
    // Input change handler to enable/disable buttons
    inputTextarea.addEventListener('input', updateButtonStates);
    
    // Initial button state
    updateButtonStates();
    
    function formatLatex() {
        const latexCode = inputTextarea.value.trim();
        
        if (!latexCode) {
            showError('Please paste some LaTeX code to format.');
            return;
        }
        
        // Get selected indent option
        const selectedIndent = document.querySelector('input[name="indent"]:checked').value;
        const indentStr = selectedIndent === '\\t' ? '\t' : selectedIndent;
        
        // Show loading state
        setLoadingState(true);
        hideError();
        
        // Make API call
        fetch('/format', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                latex_code: latexCode,
                indent_str: indentStr
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
            } else {
                outputTextarea.value = data.formatted_code;
                copyBtn.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('An error occurred while formatting the LaTeX code. Please try again.');
        })
        .finally(() => {
            setLoadingState(false);
        });
    }
    
    function copyToClipboard() {
        if (outputTextarea.value) {
            outputTextarea.select();
            outputTextarea.setSelectionRange(0, 99999); // For mobile devices
            
            navigator.clipboard.writeText(outputTextarea.value).then(() => {
                // Visual feedback for successful copy
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                copyBtn.style.background = '#6c7b7f';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
            }).catch(err => {
                console.error('Could not copy text: ', err);
                showError('Could not copy to clipboard. Please select and copy manually.');
            });
        }
    }
    
    function updateButtonStates() {
        const hasInput = inputTextarea.value.trim().length > 0;
        formatBtn.disabled = !hasInput;
        
        if (!hasInput) {
            outputTextarea.value = '';
            copyBtn.disabled = true;
        }
    }
    
    function setLoadingState(loading) {
        if (loading) {
            formatBtn.disabled = true;
            formatBtn.textContent = 'Formatting...';
            document.querySelector('.formatter-section').classList.add('loading');
        } else {
            formatBtn.textContent = 'Format LaTeX';
            document.querySelector('.formatter-section').classList.remove('loading');
            updateButtonStates();
        }
    }
    
    function showError(message) {
        let errorDiv = document.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            document.querySelector('.controls').appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
    
    function hideError() {
        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }
    
    // Sample LaTeX code for demonstration
    const sampleLatex = `\\documentclass{article}
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
    
    // Add sample button functionality
    const addSampleBtn = document.createElement('button');
    addSampleBtn.textContent = 'Load Sample';
    addSampleBtn.className = 'copy-button';
    addSampleBtn.style.marginTop = '1rem';
    addSampleBtn.style.alignSelf = 'flex-start';
    
    addSampleBtn.addEventListener('click', () => {
        inputTextarea.value = sampleLatex;
        updateButtonStates();
        outputTextarea.value = '';
        copyBtn.disabled = true;
    });
    
    document.querySelector('.input-section').appendChild(addSampleBtn);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to format
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!formatBtn.disabled) {
                formatLatex();
            }
        }
        
        // Ctrl/Cmd + C when output is focused to copy
        if ((e.ctrlKey || e.metaKey) && e.key === 'c' && document.activeElement === outputTextarea) {
            if (outputTextarea.value) {
                copyToClipboard();
            }
        }
    });
});