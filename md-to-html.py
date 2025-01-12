import re
import sys

import markdown


def main(filename: str) -> None:
    with open(filename) as f:
        md = f.read()
    content = markdown.markdown(md, extensions=["markdown.extensions.tables"])

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line[:4] == "<h1>" and line[-5:] == "</h1>":
            lines[i] = f"<header>\n{line}\n</header>"

    content = "".join(map(str, lines))

    navbar = """<nav>
      <button class="hamburger" aria-label="Toggle navigation">
      ☰
      </button>
      <div class="nav-links">
        <a href="index.html" class="active">Home</a>
        <a href="nursing.html">Nursing</a>
        <a href="https://instagram.com/lukewassphotography">Gallery</a>
        <a href="athlete.html">Athletics</a>
        <a href="https://github.com/wassupluke/">GitHub</a>
        <a href="cv.html">CV</a>
      </div>
    </nav>
    """
    
    javascript = """<script>
        // Toggle the visibility of the menu
        document.querySelector('.hamburger').addEventListener('click', () => {
            const navLinks = document.querySelector('.nav-links');
            navLinks.classList.toggle('active');
        });
    </script>
    """

    if filename == "cv.md":
        navbar = ""
        javascript = ""

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename.strip(".md").upper()}</title>
    <link rel="stylesheet" href="styles/default.css">
  </head>
  <body>
    {navbar}
    <div class="container">
      {content}
    </div>
    <footer>
      <p>&copy; 2025 Luke Wass | Whatever you do, work at it with all your heart, as working for the Lord, not for men.</p>
    </footer>
  </body>
  {javascript}
</html>
    """

    if filename == "cv.md":
        html = html.replace("default.css", "cv.css")

    print(f"{filename = } has been converted to")
    filename = filename.replace(".md", ".html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{html = }\nand saved as {filename = }\n\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        filenames = [input("Markdown file(s) to convert? ")]
        filenames = re.split(";|; |,|, | ", str(filenames)[2:-2])
        if not all(arg.endswith(".md") is True for arg in filenames):
            sys.exit("You gave a file that didn't end in .md, try again")
    elif len(sys.argv) >= 2 and all(
        arg.endswith(".md") is True for arg in sys.argv[1:]
    ):
        filenames = sys.argv[1:]
    else:
        sys.exit("That probably wasn't a Markdown file, try again")

    for filename in filenames:
        main(filename)
