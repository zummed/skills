#!/usr/bin/env python3
# Inlines the font and logos into one offline file.
# usage: python3 build.py [src/deck.html] [deck.html]   (paths relative to this script)
import base64, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent
src = root / (sys.argv[1] if len(sys.argv) > 1 else "src/deck.html")
out = root / (sys.argv[2] if len(sys.argv) > 2 else "deck.html")
html = src.read_text()

font = base64.b64encode((root / "src" / "inter.woff2").read_bytes()).decode()
html = html.replace("%%FONT%%", font)

for svg in sorted((root / "icons").glob("*.svg")):  # no icons/ is fine
    text = re.sub(r"<!--.*?-->", "", svg.read_text(), flags=re.S)
    view_box = re.search(r'viewBox="([^"]+)"', text).group(1)
    inner = re.search(r"<svg\b[^>]*>(.*)</svg>", text, re.S).group(1).strip()
    html = html.replace(f"%%VB_{svg.stem}%%", view_box).replace(f"%%SVG_{svg.stem}%%", inner)

leftover = re.findall(r"%%[A-Za-z_]+%%", html)
if leftover:
    raise SystemExit(f"unfilled placeholders: {sorted(set(leftover))}")
out.write_text(html)
print(f"{out.name} {len(html) // 1024} KiB")
