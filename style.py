mishtee_css = """
/* Global Styles */
.gradio-container {
    background-color: #FAF9F6 !important;
    color: #333333 !important;
    font-family: 'Crimson Text', 'Georgia', serif !important;
}

/* Headings: Clean, spaced-out Serif */
h1, h2, h3, .section-header {
    font-family: 'Crimson Text', 'Georgia', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #333333 !important;
    margin-bottom: 2rem !important;
}

/* Text & Labels */
p, label, .secondary-text {
    font-family: 'Inter', 'Helvetica', sans-serif !important;
    font-weight: 300 !important;
    letter-spacing: 0.05em !important;
}

/* Buttons: Sober Terracotta, sharp edges */
button.primary {
    background: #C06C5C !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0px !important;
    padding: 12px 24px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    transition: background 0.3s ease !important;
}

button.primary:hover {
    background: #A65D4F !important;
}

/* Inputs and Boxes: Sharp lines, no shadows */
input, textarea, .gr-box, .gr-input {
    background-color: #FAF9F6 !important;
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
    box-shadow: none !important;
}

/* Data Tables: Lightweight Sans-Serif */
table, .gr-table {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-collapse: collapse !important;
}

th, td {
    border: 1px solid #E0E0E0 !important;
    padding: 12px !important;
    text-align: left !important;
}

/* Padding/Whitespace: Significant spacing between elements */
.gr-block, .gr-form, .gap {
    padding: 2.5rem !important;
    margin-bottom: 1.5rem !important;
    border: none !important;
}

/* Remove default Gradio focus rings */
*:focus {
    outline: 1px solid #C06C5C !important;
    outline-offset: 2px !important;
}
"""
