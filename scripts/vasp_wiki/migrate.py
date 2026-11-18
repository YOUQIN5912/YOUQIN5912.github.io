"""Rebuild the four archived articles from the unmodified MediaWiki export."""
from pathlib import Path
from html import escape, unescape
from urllib.parse import quote, unquote, urlsplit
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ORIGINALS = ROOT / "files/vasp-wiki/originals"
PAGES = ROOT / "_pages/vasp-wiki"
ROUTES = {
    "Main Page": ("index", "Overview", "/vasp-wiki/"),
    "Getting started": ("getting-started", "Getting Started", "/vasp-wiki/getting-started/"),
    "Methods": ("computational-methods", "Computational Methods", "/vasp-wiki/computational-methods/"),
    "Software and resources": ("software-and-resources", "Software & Resources", "/vasp-wiki/software-and-resources/"),
}
XML = "mn.kjemi.vaspwiki-20250627110347.xml"
NS = {"m": "http://www.mediawiki.org/xml/export-0.10/"}
STUBS = {
    "Methods": {"Convergence tests", "Benchmark", "General calculations and relaxation", "Error messages"},
    "Software and resources": {"Binding energies of molecules"},
}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", unescape(re.sub(r"<[^>]+>", "", text)).lower()).strip("-")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_pages():
    tree = ET.parse(ORIGINALS / XML)
    pages = [(p.findtext("m:title", namespaces=NS), p.find("m:revision", NS))
             for p in tree.findall("m:page", NS)]
    return sorted(pages, key=lambda p: list(ROUTES).index(p[0]))


class Article:
    def __init__(self, title, source):
        self.title, self.source = title, source
        self.references, self.headings, self.codes = [], [], []

    def destination(self, target):
        page, _, anchor = target.partition("#")
        page = page.replace("_", " ") or self.title
        if page == "Main Page" and anchor:
            decoded = re.sub(r"\.([0-9A-Fa-f]{2})", lambda m: chr(int(m[1], 16)), anchor)
            for name, text in SOURCE_TEXT.items():
                if any(slug(h) == slug(decoded) for h in re.findall(r"^=+\s*(.*?)\s*=+\s*$", text, re.M)):
                    page, anchor = name, decoded
                    break
        if page in ROUTES:
            return ROUTES[page][2] + ("#" + slug(anchor) if anchor else "")
        if page.startswith("Media:"):
            return "/files/vasp-wiki/originals/" + quote(page[6:])
        raise ValueError("Unresolved internal link: " + target)

    def url(self, url):
        if url.startswith("//"):
            return "https:" + url
        parsed = urlsplit(url)
        if parsed.netloc == "wiki.uio.no" and "/vaspwiki/index.php/" in parsed.path:
            target = unquote(parsed.path.split("index.php/", 1)[1])
            return self.destination(target + ("#" + parsed.fragment if parsed.fragment else ""))
        # Repair URL punctuation only; the source and bibliography text stay available unchanged.
        if url == "https://www.ovito.org/about/|":
            return url[:-1]
        if url.startswith("https://doi-org/"):
            return url.replace("https://doi-org/", "https://doi.org/", 1)
        return url

    def inline(self, text):
        saved = []

        def keep(value):
            saved.append(value)
            return "\x00" + str(len(saved) - 1) + "\x00"

        def reference(match):
            self.references.append(match[1])
            n = len(self.references)
            return keep(f'<sup id="cite-{n}"><a href="#reference-{n}" aria-label="Reference {n}">[{n}]</a></sup>')

        text = re.sub(r"<ref>(.*?)</ref>", reference, text, flags=re.S)
        text = re.sub(r"<code>(.*?)</code>", lambda m: keep("<code>" + escape(unescape(re.sub(r"</?nowiki>", "", m[1]))) + "</code>"), text, flags=re.S)
        text = re.sub(r"<nowiki>(.*?)</nowiki>", lambda m: keep(escape(m[1])), text, flags=re.S)
        text = re.sub(r"<(sub|sup)>(.*?)</\1>", lambda m: keep(f'<{m[1]}>{escape(m[2])}</{m[1]}>'), text)

        def wiki_link(match):
            target, _, label = match[1].partition("|")
            if target.startswith("File:"):
                return keep('<figure class="wiki-figure"><a href="/files/vasp-wiki/originals/Image.png"><img src="/files/vasp-wiki/originals/Image.png" alt="Archived CatMAP input-file screenshot" width="940" height="450" loading="lazy"></a><figcaption>Original CatMAP input-file screenshot. The rightmost columns are cropped in the supplied image.</figcaption></figure>')
            return keep('<a href="' + escape(self.destination(target), quote=True) + '">' + escape(label or target.replace("Media:", "")) + '</a>')

        text = re.sub(r"\[\[(.*?)\]\]", wiki_link, text)
        text = re.sub(r"\[((?:https?://|//|mailto:)[^\s\]]+)(?:\s+([^\]]+))?\]", lambda m: keep('<a href="' + escape(self.url(m[1]), quote=True) + '">' + escape(m[2] or m[1]) + '</a>'), text)
        text = re.sub(r"(?<![\w\"'=])(https?://[^\s<>\x00]+)", lambda m: keep('<a href="' + escape(self.url(m[1]), quote=True) + '">' + escape(m[1]) + '</a>'), text)
        text = escape(text)
        text = re.sub(r"&#x27;&#x27;&#x27;(.*?)&#x27;&#x27;&#x27;", r"<strong>\1</strong>", text)
        text = re.sub(r"&#x27;&#x27;(.*?)&#x27;&#x27;", r"<em>\1</em>", text)
        return re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m[1])], text)

    def code(self, lines):
        text = "\n".join(line[1:] if line.startswith(" ") else line for line in lines)
        text = unescape(re.sub(r"</?(?:code|nowiki)>", "", text))
        language = "python" if re.search(r"from (?:ase|pymatgen|icet)\b|rxn_expressions", text) else "bash"
        if re.match(r"\s*(?:IMAGES|SPRING|LCLIMB|LPARD|IBAND|PREC|LAECHG)\s*=", text):
            language = "ini"
        if "Sr1 Ti1 O3" in text or "4.2200000000000000" in text or "4.2353879522908331" in text or "curvature:" in text:
            language = "text"
        self.codes.append({"language": language, "text": text})
        return "{% highlight " + language + " %}\n" + text + "\n{% endhighlight %}"

    def render(self):
        lines, out, i = self.source.splitlines(), [], 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            heading = re.match(r"^(=+)\s*(.*?)\s*\1\s*$", line)
            if heading:
                level, title = len(heading[1]), heading[2]
                if level == 1 and title.lower() in ("getting started", "methods", "software and resources"):
                    i += 1
                    continue
                level = max(2, level)
                self.headings.append({"id": slug(title), "title": unescape(re.sub(r"<[^>]+>", "", title)), "level": level})
                out.append(f'<h{level} id="{slug(title)}">{self.inline(title)}<a class="wiki-anchor" href="#{slug(title)}" aria-label="Link to {escape(title, quote=True)}">#</a></h{level}>')
                if title in STUBS.get(self.title, set()):
                    out.append('<aside class="wiki-editor-note"><strong>Content not recovered / Reserved for future additions</strong><p>This section was empty or only an outline in the backup. Any original notes are preserved below. No additional tutorial content has been supplied.</p></aside>')
            elif line.startswith("{|"):
                rows, cells, caption = [], [], ""
                i += 1
                while lines[i] != "|}":
                    entry = lines[i]
                    if entry.startswith("|+"):
                        caption = '<caption>' + self.inline(entry[2:].strip()) + '</caption>'
                    elif entry == "|-":
                        if cells:
                            rows.append('<tr>' + ''.join(cells) + '</tr>')
                            cells = []
                    elif entry.startswith(("!", "|")):
                        tag = "th" if entry[0] == "!" else "td"
                        cells.append(f'<{tag}' + (' scope="col"' if tag == 'th' else '') + '>' + self.inline(entry[1:].strip()) + f'</{tag}>')
                    else:
                        raise ValueError("Unsupported table syntax: " + entry)
                    i += 1
                if cells:
                    rows.append('<tr>' + ''.join(cells) + '</tr>')
                out.append('<div class="wiki-table" tabindex="0" role="region" aria-label="Scrollable archive table"><table>' + caption + ''.join(rows) + '</table></div>')
            elif line.lstrip().startswith("{{:"):
                target = line.strip()[3:-2]
                out.append('<p class="wiki-transclusion"><a href="' + self.destination(target) + '">' + escape(ROUTES[target][1]) + ' <span aria-hidden="true">&rarr;</span></a></p>')
            elif line.startswith('[[File:'):
                out.append(self.inline(line))
            elif line.strip() == '<references />':
                items = ['<li id="reference-' + str(n) + '">' + self.inline(ref) + ' <a href="#cite-' + str(n) + '" aria-label="Back to citation ' + str(n) + '">&uarr;</a></li>' for n, ref in enumerate(self.references, 1)]
                out.append('<ol class="wiki-references">' + ''.join(items) + '</ol>')
            elif re.match(r"^[*#] ", line):
                marker = line[0]
                items = []
                while i < len(lines) and lines[i].startswith(marker + " "):
                    items.append('<li>' + self.inline(lines[i][2:]) + '</li>')
                    i += 1
                tag = 'ul' if marker == '*' else 'ol'
                out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
                continue
            elif line.startswith(" ") or re.match(r"^(LPARD|IBAND|PREC|LAECHG)\s*=", line) or re.fullmatch(r"<code>.*</code>", line.strip()):
                chunk = []
                # The original job script has four unindented module lines. Recover its code boundary without changing the commands.
                job = line.startswith(" #!/bin/bash") and i > 0 and 'Example job script' in lines[i-1]
                while i < len(lines):
                    current = lines[i]
                    is_code = current.startswith(" ") or re.match(r"^(LPARD|IBAND|PREC|LAECHG)\s*=", current) or re.fullmatch(r"<code>.*</code>", current.strip())
                    if job and current.startswith("===Aliases"):
                        break
                    if not job and not is_code:
                        if not current.strip() and i+1 < len(lines) and lines[i+1].startswith(" "):
                            chunk.append(current)
                            i += 1
                            continue
                        break
                    chunk.append(current)
                    i += 1
                while chunk and not chunk[-1].strip():
                    chunk.pop()
                out.append(self.code(chunk))
                continue
            else:
                paragraph = [line]
                while i+1 < len(lines) and lines[i+1].strip() and not re.match(r"^(?:=| |\{\||[*#] |<references|\[\[File:)", lines[i+1]):
                    i += 1
                    paragraph.append(lines[i])
                out.append('<p>' + self.inline('\n'.join(paragraph)) + '</p>')
            i += 1
        return '\n\n'.join(out) + '\n'


SOURCE_TEXT = {title: rev.findtext('m:text', namespaces=NS) or '' for title, rev in load_pages()}


def main():
    data = {"articles": [], "export": XML, "recovery_date": "2026-11-18", "files": []}
    for title, rev in load_pages():
        source = SOURCE_TEXT[title]
        article = Article(title, source)
        body = article.render()
        stem, display_title, url = ROUTES[title]
        front = '---\nlayout: vasp-wiki\ntitle: ' + json.dumps(display_title) + '\npermalink: ' + url + '\nwiki_id: ' + stem + '\nauthor_profile: false\n---\n\n'
        write(PAGES / (stem + '.html'), front + body)
        write(ROOT / 'files/vasp-wiki/wikitext' / (stem + '.wiki'), source)
        data['articles'].append({"id": stem, "title": display_title, "original_title": title, "url": url,
            "revision": rev.findtext('m:id', namespaces=NS), "updated": rev.findtext('m:timestamp', namespaces=NS),
            "editor": rev.findtext('m:contributor/m:username', namespaces=NS), "headings": article.headings,
            "code_blocks": article.codes, "source_sha256": hashlib.sha256(source.encode()).hexdigest()})
    for path in sorted(ORIGINALS.iterdir()):
        data['files'].append({"name": path.name, "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    write(ROOT / '_data/vasp_wiki.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('Recovered four articles; original attachments retained byte-for-byte.')


if __name__ == '__main__':
    main()
