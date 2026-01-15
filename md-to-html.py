import re
import sys

from datetime import datetime

import markdown


def get_input() -> list[str]:
    if len(sys.argv) < 2:
        user_input = [input("Markdown file(s) to convert? ")]
    else:
        user_input = sys.argv[1:]

    user_input = [arg.strip(";|; |,|, | ") for arg in user_input]

    return user_input


def check_args(filenames: list[str]) -> list[str]:
    # early return if user passed all .md files
    if all(file.endswith(".md") is True for file in filenames):
        return filenames

    # allow passing extensionless filenames
    for index, file in enumerate(filenames):
        if file.find(".") == -1:
            filenames[index] = file + ".md"
        elif file[:-1].endswith(".md") is False:
            sys.exit(f"[{file}] doesn't end in .md, try again")

    return filenames


def load_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def main(filename: str) -> None:
    with open(filename) as f:
        md = f.read()
    content = markdown.markdown(md, extensions=["markdown.extensions.tables"])

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line[:4] == "<h1>" and line[-5:] == "</h1>":
            lines[i] = f"<header>\n{line}\n</header>"

    content = "\n".join(map(str, lines))

    style = "default.css" if filename != "cv.md" else "cv.css"
    navbar = load_template('templates/navbar.html') if filename != "cv.md" else ""
    javascript = f'<script src="static/js/nav.js"></script>' if filename != "cv.md" else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename.strip(".md").upper()}</title>
    <link rel="stylesheet" href="styles/{style}">
  </head>
  <body>
    {navbar}
    <div class="container">
      {content}
    </div>
    <footer>
      <p>&copy; {datetime.now().year} Luke Wass | Whatever you do, work at it with all your heart, as working for the Lord, not for men.</p>
    </footer>
  </body>
  {javascript}
</html>
    """

    print(f"{filename = } has been converted to")
    filename = filename.replace(".md", ".html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{html = }\nand saved as {filename = }\n\n")


if __name__ == "__main__":
    user_args = get_input()
    filenames = check_args(user_args)

    for filename in filenames:
        main(filename)
