#!/usr/bin/env python3
"""Télécharge une feuille Google Fonts (sous-ensembles latin) et l'héberge localement.
Usage : fonts.py <dossier_demo> "<url css2 Google Fonts>"  → crée fonts/ et fonts/fonts.css"""
import sys, re, os, urllib.request
dest, url = sys.argv[1], sys.argv[2]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read()
css = get(url).decode()
blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]*})", css)
os.makedirs(f"{dest}/fonts", exist_ok=True)
out = []
seen = {}
for subset, block in blocks:
    if subset not in ("latin", "latin-ext"):
        continue
    fam = re.search(r"font-family: '([^']+)'", block).group(1)
    sty = re.search(r"font-style: (\w+)", block).group(1)
    wgt = re.search(r"font-weight: ([\d ]+)", block).group(1).replace(" ", "-")
    src = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    name = seen.get(src) or f"{fam.lower().replace(' ', '-')}-{sty}-{wgt}-{subset}.woff2"
    seen[src] = name
    path = f"{dest}/fonts/{name}"
    if not os.path.exists(path):
        open(path, "wb").write(get(src))
    out.append(block.replace(src, name))
open(f"{dest}/fonts/fonts.css", "w").write("\n".join(out) + "\n")
print(len(out), "faces ->", dest + "/fonts")
