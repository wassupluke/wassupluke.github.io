import markdown

filename = input("Markdown file to convert? ")
with open(filename) as f:
    md = f.read()
content = markdown.markdown(md)

lines = content.split("\n")
for i, line in enumerate(lines):
    if line[:4] == "<h1>" and line[-5:] == "</h1>":
        lines[i] = f"<header>\n{line}\n</header>"

content = "".join(map(str, lines))

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename.strip(".md").title()}</title>
    <link rel="stylesheet" href="stylesheet.css">
</head>
<body>
    {content}
    <footer>
        <p>&copy; 2025 Luke Wass | Whatever you do, work at it with all your heart, as working for the Lord, not for men.</p>
    </footer>
</body>
</html>
"""

filename = filename.replace(".md", ".html")
with open(filename, "w") as f:
    f.write(html)

print(html)
