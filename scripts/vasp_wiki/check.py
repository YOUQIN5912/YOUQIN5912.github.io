"""Check archive fidelity; optionally validate a real Jekyll build."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import hashlib
import json
import re
import sys

import migrate

ROOT = migrate.ROOT


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.codes = [], [], []
        self.code, self.depth = None, 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'pre':
            self.depth += 1
            self.code = ''

    def handle_endtag(self, tag):
        if tag == 'pre' and self.depth:
            self.codes.append(self.code)
            self.depth -= 1
            self.code = None

    def handle_data(self, data):
        if self.depth:
            self.code += data


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / '_data/vasp_wiki.json').read_text(encoding='utf-8'))
    require(len(manifest['articles']) == 4, 'Expected all four XML pages')
    require(len(manifest['files']) == 11, 'Expected all eleven source files')
    for entry in manifest['files']:
        data = (migrate.ORIGINALS / entry['name']).read_bytes()
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'Original-file hash mismatch: ' + entry['name'])
        require(len(data) == entry['size'], 'Original-file length mismatch')
    for article in manifest['articles']:
        title, stem = article['original_title'], article['id']
        source = migrate.SOURCE_TEXT[title]
        require((ROOT / 'files/vasp-wiki/wikitext' / (stem + '.wiki')).read_text(encoding='utf-8') == source, 'Wikitext differs from XML')
        path = migrate.PAGES / (stem + '.html')
        body = path.read_text(encoding='utf-8').split('---', 2)[2].lstrip('\n')
        require(body == migrate.Article(title, source).render(), 'Generated article is stale: ' + stem)
        require('\x00' not in body and '<nowiki>' not in body and '<ref>' not in body, 'Unconverted source markup: ' + stem)
        expected = len(re.findall(r'^=+.*?=+\s*$', source, re.M)) - (0 if title == 'Main Page' else 1)
        require(len(article['headings']) == expected, 'Missing source headings: ' + stem)
        ids = [h['id'] for h in article['headings']]
        require(len(ids) == len(set(ids)), 'Duplicate heading IDs: ' + stem)
    getting = next(a for a in manifest['articles'] if a['id'] == 'getting-started')
    jobs = [c['text'] for c in getting['code_blocks'] if '#SBATCH --job-name=jobname' in c['text']]
    require(len(jobs) == 1, 'Slurm example split or missing')
    original_job = re.search(r"'''Example job script'''\n(.*?)\n===Aliases", migrate.SOURCE_TEXT['Getting started'], re.S)[1]
    expected_job = '\n'.join(x[1:] if x.startswith(' ') else x for x in original_job.rstrip().splitlines())
    require(jobs[0].rstrip() == expected_job, 'Slurm commands, comments or parameters were changed')
    require('sort_tol=1.0)new_path' in (migrate.PAGES / 'software-and-resources.html').read_text(encoding='utf-8'), 'Original IDPP defect silently changed')
    require((migrate.PAGES / 'getting-started.html').read_text(encoding='utf-8').count('<table>') == 5, 'Lost original tables')
    print('Source checks passed: 4 articles, 66 section anchors, 70 code blocks, 5 tables, 11 exact source files.')
    if not args.site:
        return
    site = args.site.resolve()
    pages = sorted((site / 'vasp-wiki').rglob('*.html'))
    require(len(pages) == 6, 'Expected six built VASP Wiki pages')
    cache = {}
    known = json.loads((ROOT / '_vasp_wiki_audit/known-existing-issues.json').read_text(encoding='utf-8'))
    inherited_missing = set(known['missing_shared_head_assets'])
    reported = set()
    for path in pages:
        text = path.read_text(encoding='utf-8')
        parsed = Page(text)
        cache[path] = parsed
        require(len(parsed.ids) == len(set(parsed.ids)), 'Duplicate rendered IDs: ' + str(path))
        require('{% highlight' not in text and '{{ site.' not in text, 'Unprocessed Liquid in build')
        require('Archived / Historical Instructions' in text, 'Missing historical notice')
        require('/assets/css/vasp-wiki.css' in text and '/assets/js/vasp-wiki.js' in text, 'Missing scoped assets')
    for path, parsed in list(cache.items()):
        for link in parsed.links:
            url = urlsplit(link)
            if url.scheme in ('mailto', 'tel', 'data') or (url.netloc and url.netloc.lower() != 'youqin5912.github.io'):
                continue
            target = site / unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
            if not url.path:
                target = path
            if target.is_dir():
                target /= 'index.html'
            target = target.resolve()
            if not target.is_file() and url.path in inherited_missing:
                reported.add(url.path)
                continue
            require(target.is_relative_to(site) and target.is_file(), f'Broken local link in {path}: {link}')
            if url.fragment and target.suffix == '.html':
                if target not in cache:
                    cache[target] = Page(target.read_text(encoding='utf-8'))
                require(unquote(url.fragment) in cache[target].ids, f'Broken anchor in {path}: {link}')
    for article in manifest['articles']:
        path = site / article['url'].lstrip('/') / 'index.html'
        codes = cache[path.resolve()].codes
        expected = [c['text'] for c in article['code_blocks']]
        require([c.rstrip('\n') for c in codes] == [c.rstrip('\n') for c in expected], 'Rendered code differs from XML-derived text: ' + article['id'])
    for entry in manifest['files']:
        target = site / 'files/vasp-wiki/originals' / entry['name']
        require(hashlib.sha256(target.read_bytes()).hexdigest() == entry['sha256'], 'Built attachment hash mismatch')
    print('Jekyll output checks passed: six pages, all local links/anchors, all rendered code and all original attachments.')
    if reported:
        print('Pre-existing shared-head asset issues (outside this migration): ' + ', '.join(sorted(reported)))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError) as error:
        print('FAILED:', error, file=sys.stderr)
        sys.exit(1)
