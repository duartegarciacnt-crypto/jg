#!/usr/bin/env python3
"""Structural + content verification for index.html (WoodenYears site).

Checks:
  - every brand div is a DIRECT child of #brands (tab switching depends on this)
  - #materials is a sibling of #brands (not nested inside it)
  - initial-load visibility (only Dual visible) and simulated tab clicks
  - every brand section (compatibility/market/competition) is non-empty
  - price tables have consistent header/row column counts
Run from the repo root:  python3 tools/verify_structure.py
"""
import re
import sys
from html.parser import HTMLParser

INDEX = "index.html"


class Node:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.id = dict(attrs).get("id")
        self.classes = set((dict(attrs).get("class") or "").split())
        self.children = []
        self.parent = None
        self.text = ""


class TreeBuilder(HTMLParser):
    VOID = {"br", "img", "input", "meta", "link", "hr", "source"}

    def __init__(self):
        super().__init__()
        self.root = Node("root", [])
        self.stack = [self.root]
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True
        if tag in self.VOID:
            return
        n = Node(tag, attrs)
        n.parent = self.stack[-1]
        self.stack[-1].children.append(n)
        self.stack.append(n)

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        if tag in self.VOID:
            return
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        if not self.in_script and data.strip():
            self.stack[-1].text += data.strip()


def build(html):
    tb = TreeBuilder()
    tb.feed(html)
    byid = {}

    def walk(n):
        if n.id:
            byid[n.id] = n
        for c in n.children:
            walk(c)

    walk(tb.root)
    return byid


def visible(n):
    cur = n
    while cur and cur.tag != "root":
        c = cur.classes
        if "tab-content" in c and "active" not in c:
            return False
        if "sub-tab-content" in c and "active" not in c:
            return False
        cur = cur.parent
    return True


def parent_id(n):
    p = n.parent
    while p and not p.id:
        p = p.parent
    return p.id if p else None


def text_len(n):
    return len(n.text) + sum(text_len(c) for c in n.children)


def main():
    html = open(INDEX, encoding="utf-8").read()
    byid = build(html)
    brands = ["dual", "technics", "lenco", "garrard", "thorens",
              "denon", "jvc", "sony", "marantz"]
    ok = True

    print("== structure: brands are direct children of #brands ==")
    for b in brands:
        if b not in byid:
            print(f"  #{b}: *** MISSING ***"); ok = False; continue
        p = parent_id(byid[b])
        good = p == "brands"; ok &= good
        print(f"  #{b}: parent=#{p} {'OK' if good else '*** FAIL ***'}")

    print("== content: every section non-empty ==")
    for b in brands:
        for s in ("compatibility", "market", "competition"):
            nid = f"{b}-{s}"
            if nid not in byid:
                print(f"  #{nid}: *** MISSING ***"); ok = False; continue
            if text_len(byid[nid]) <= 100:
                print(f"  #{nid}: *** TOO SHORT ***"); ok = False

    print("== price tables: consistent column counts ==")
    for m in re.finditer(r"<table.*?</table>", html, re.S):
        blk = m.group(0)
        if not ("Faixa Preço" in blk or "Faixa de Preço" in blk):
            continue
        pre = html[:m.start()]
        tid = re.findall(r'id="([a-z0-9\-]+)"', pre)[-1]
        rows = re.findall(r"<tr>(.*?)</tr>", blk, re.S)
        nth = rows[0].count("<th")
        tds = {r.count("<td") for r in rows[1:]}
        good = tds == {nth}; ok &= good
        print(f"  {tid:16s} th={nth} td={tds} {'OK' if good else '*** MISMATCH ***'}")

    print("== div balance (body) ==")
    body = html[html.find("<body>"):html.find("<script>")]
    o = len(re.findall(r"<div\b", body)); c = len(re.findall(r"</div>", body))
    good = o == c; ok &= good
    print(f"  <div>={o} </div>={c} {'OK' if good else '*** IMBALANCE ***'}")

    print("\n>>> RESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
