---
layout: vasp-wiki
title: "Sources & Recovery"
permalink: /vasp-wiki/sources-and-recovery/
wiki_id: sources
author_profile: false
wiki_toc:
  - {id: about-this-archive, title: About this archive, level: 2}
  - {id: attribution-and-reuse, title: Attribution and reuse, level: 2}
  - {id: recovery-decisions, title: Recovery decisions, level: 2}
  - {id: known-gaps-and-source-limitations, title: Known gaps, level: 2}
  - {id: original-files, title: Original files, level: 2}
---

## About this archive

This section preserves the University of Oslo Electrochemistry group's VASP Wiki, formerly hosted at [wiki.uio.no/mn/kjemi/vaspwiki/](https://wiki.uio.no/mn/kjemi/vaspwiki/). The supplied backup is the source of this recovery. This personal website is an archival mirror, not an official UiO or VASP service.

The MediaWiki export is the primary source. It contains four pages and one revision per page. The four DOCX and four PDF exports were checked as secondary sources; they are retained as supplied. Original spelling, technical values, unfinished notes and scientific uncertainty have been preserved. Editorial notes are identified separately.

## Attribution and reuse

The original welcome page identifies the Electrochemistry group at the Centre for Materials Science and Nanotechnology, University of Oslo, and names Jonathan Polfus as the contact. The export records the following **latest editors**, not the complete authorship history:

| Original page | Revision | Date | Latest editor recorded |
| --- | --- | --- | --- |
{% for article in site.data.vasp_wiki.articles %}| {{ article.original_title }} | {{ article.revision }} | {{ article.updated | date: "%Y-%m-%d" }} | {{ article.editor }} |
{% endfor %}

The site maintainer has identified himself as a member of the original research group and confirmed permission to use the material. The backup does not state a public redistribution license. No Creative Commons or other open license is inferred from MediaWiki, UiO hosting, group membership, or the website theme's license. Original authors and third-party rights holders retain their rights. Confirm the applicable terms before further redistribution.

No VASP executable, licensed source code, pseudopotential dataset or POTCAR content is included. The original instructions for creating a POTCAR are retained; access to the underlying data remains subject to its license.

## Recovery decisions

- **Primary source:** `mn.kjemi.vaspwiki-20250627110347.xml`, exported with MediaWiki 1.27.4. Export timestamps in the file range from 2022 to 2025; the export filename is not an article revision date.
- **Original page content:** headings, five tables, ordered and unordered lists, references, commands, scripts and the supplied CatMAP image were recovered. The Main Page's three transclusions now link to the three recovered chapters.
- **Code boundaries:** one MediaWiki formatting space is removed from preformatted lines. Four unindented module lines inside the example Slurm script are grouped back into that script. No command, module name, parameter, scientific value or original code comment is changed.
- **Secondary-export artifacts:** the PDFs sometimes render a shell comment as a heading or interpret `$SCRATCH` as mathematics. Those artifacts do not override the XML. DOCX comment parts contain no actual comments or tracked changes.
- **Links:** MediaWiki page links and old Main Page fragment links are mapped to the new chapter anchors. Protocol-relative web links use HTTPS. Two visibly malformed URL destinations are repaired: `https://doi-org/…` becomes `https://doi.org/…`, and the trailing `|` is removed from the OVITO URL. Original visible text and raw wikitext remain available.
- **Historical material:** Saga project names, accounts, login hosts, storage paths, job scripts, modules and installation commands are marked as historical. External links are retained as historical references; their availability does not establish that the original instructions remain valid.
- **Metadata review:** the source contains institutional editor identifiers, named project managers and group allocation numbers. The screenshot includes an original account name and cluster path. These are preserved as provenance; no password, API token, private key or real job log was found. The spreadsheet is a template with example values and formulas. This review cannot prove the absence of all sensitive information.

## Known gaps and source limitations

- The XML contains only four page revisions. Earlier revisions, complete contributor lists, talk pages and any other pages not exported cannot be reconstructed from this backup.
- No standalone `vasptest` directory, full INCAR, full KPOINTS, complete example POSCAR/CONTCAR, jobfile attachment or VTST script collection was supplied. Commands that refer to those cluster files are preserved, not made into invented downloads.
- The POSCAR/CONTCAR output excerpts already end with `...` in the source. No missing coordinates have been fabricated.
- The CatMAP image is the only supplied image. Its rightmost columns and lower rows are outside the captured area. The original `energies.txt` data file is absent.
- Several Methods sections were unfinished: convergence examples, benchmarks, general relaxation settings and error messages. The molecular binding-energy table is a source TODO. These remain visibly incomplete.
- Incomplete sections are labelled **Content not recovered / Reserved for future additions**. They are intentionally left for the maintainer to complete; original short notes remain visible below the label.
- The original Pymatgen IDPP example contains a joined statement and other examples may depend on old APIs. These issues are flagged without silently changing code.
- Original external pages, old download targets, software documentation and bibliography records have not been exhaustively verified or updated. A restored hyperlink is not a technical endorsement.
- There is no new Olivia, NRIS, DFT or AIMD tutorial in the backup. Planned material is listed separately from recovered instructions.

## Original files
{: #original-files }

All files below are byte-for-byte copies of the non-metadata files in the supplied ZIP. The `__MACOSX` resource-fork records are omitted. The original ZIP itself is retained by the maintainer outside this website.

<div class="wiki-table" tabindex="0" role="region" aria-label="Original archive files">
<table><thead><tr><th scope="col">File</th><th scope="col">Bytes</th><th scope="col">SHA-256</th></tr></thead><tbody>
{% for file in site.data.vasp_wiki.files %}<tr><td><a href="{{ '/files/vasp-wiki/originals/' | append: file.name | relative_url }}" download>{{ file.name }}</a></td><td>{{ file.size }}</td><td><code>{{ file.sha256 }}</code></td></tr>
{% endfor %}</tbody></table></div>

The extracted [Overview wikitext](/files/vasp-wiki/wikitext/index.wiki), [Getting Started wikitext](/files/vasp-wiki/wikitext/getting-started.wiki), [Methods wikitext](/files/vasp-wiki/wikitext/computational-methods.wiki) and [Software & Resources wikitext](/files/vasp-wiki/wikitext/software-and-resources.wiki) preserve the page text directly from XML.
