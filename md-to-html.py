import markdown
from pathlib import Path

def markdown_to_html(input_file, output_file):
    # Read the markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # HTML Template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Site</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #0366d6;
            --secondary-color: #24292e;
            --background-color: #f8f9fa;
            --text-color: #333;
            --font-primary: 'Montserrat', sans-serif;
            --font-secondary: 'Open Sans', sans-serif;
        }}

        body {{
            margin: 0;
            font-family: var(--font-secondary);
            color: var(--text-color);
            background-color: var(--background-color);
        }}

        header {{
            background: var(--primary-color);
            color: white;
            text-align: center;
            padding: 2rem;
        }}

        header h1 {{
            font-family: var(--font-primary);
            margin: 0;
            font-size: 2.5rem;
        }}

        header p {{
            margin: 0.5rem 0 0;
            font-size: 1.25rem;
        }}

        nav {{
            display: flex;
            justify-content: center;
            background: var(--secondary-color);
            padding: 0.5rem 0;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 600;
        }}

        nav a:hover {{
            text-decoration: underline;
        }}

        .content {{
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .content h1, .content h2, .content h3 {{
            font-family: var(--font-primary);
            color: var(--primary-color);
        }}

        .content a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        .content a:hover {{
            text-decoration: underline;
        }}

        footer {{
            background: var(--secondary-color);
            color: white;
            text-align: center;
            padding: 1rem;
        }}

        footer p {{
            margin: 0;
        }}

        @media (max-width: 600px) {{
            header h1 {{
                font-size: 1.5rem;
            }}

            header p {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Generated Site</h1>
        <p>Automatically formatted from markdown</p>
    </header>
    <nav>
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Contact</a>
    </nav>
    <main class="content">
        {html_content}
    </main>
    <footer>
        <p>&copy; 2025 Generated Site</p>
    </footer>
</body>
</html>"""

    # Write the formatted HTML to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template.format(html_content=html_content))

# Example Usage
input_markdown_file = Path("input.md")
output_html_file = Path("output.html")
markdown_to_html(input_markdown_file, output_html_file)
print(f"Converted {input_markdown_file} to {output_html_file}")
