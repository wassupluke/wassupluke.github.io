import re
import sys

import markdown
from bs4 import BeautifulSoup as bs

# ---  CUSTOMIZE Prettify FUNCTION TO ALLOW INDENT WIDTH SPECIFICATION
# https://stackoverflow.com/a/15513483/22771801
og_prettify = bs.prettify
r = re.compile(r"^(\s*)", re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=2):
    return r.sub(r"\1" * indent_width, og_prettify(self, encoding, formatter))


bs.prettify = prettify
# ---


def main(filename):
    with open(filename) as f:
        md = f.read()
    content = markdown.markdown(md, extensions=["markdown.extensions.tables"])

    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line[:4] == "<h1>" and line[-5:] == "</h1>":
            lines[i] = f"<header>\n{line}\n</header>"

    content = "".join(map(str, lines))
    soup = bs(content, "html.parser")
    content = soup.prettify()
    content = content.replace("\n", "\n    ")

    html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename.strip(".md").title()}</title>
    <link rel="stylesheet" href="styles/default.css">
  </head>
  <body>
    {content}
    <footer>
      <p>&copy; 2025 Luke Wass | Whatever you do, work at it with all your heart, as working for the Lord, not for men.</p>
    </footer>
  </body>
</html>
    """

    if filename == "cv.md":
        html = html.replace("default.css", "cv.css")

    print(f"{filename = } has been converted to")
    filename = filename.replace(".md", ".html")
    with open(filename, "w") as f:
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
