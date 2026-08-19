# -*- coding: utf-8 -*-
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

CSS_TAG = '<link rel="stylesheet" id="enhance-css" href="/assets/css/enhance.css">\n'
JS_TAG = '<script id="enhance-js" src="/assets/js/enhance.js" defer></script>\n'

count = 0
for dirpath, dirnames, filenames in os.walk(SITE):
    if "assets" in dirpath.split(os.sep):
        continue
    if "index.html" not in filenames:
        continue
    path = os.path.join(dirpath, "index.html")
    html = open(path, encoding="utf-8").read()
    changed = False
    if "enhance-css" not in html and "</head>" in html:
        html = html.replace("</head>", CSS_TAG + "</head>", 1)
        changed = True
    if "enhance-js" not in html and "</body>" in html:
        html = html.replace("</body>", JS_TAG + "</body>", 1)
        changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print("injected:", os.path.relpath(path, SITE))

print("total pages updated:", count)
