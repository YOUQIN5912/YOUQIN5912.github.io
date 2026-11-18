---
layout: vasp-wiki
title: "Contributing & Future Tutorials"
permalink: /vasp-wiki/contributing/
wiki_id: contributing
author_profile: false
wiki_toc:
  - {id: keep-the-archive-distinct, title: Keep the archive distinct, level: 2}
  - {id: planned-tutorials, title: Planned tutorials, level: 2}
  - {id: olivia-and-nris, title: Olivia and NRIS, level: 3}
  - {id: vasp-6, title: VASP 6, level: 3}
  - {id: dft, title: DFT foundations, level: 3}
  - {id: neb, title: Nudged Elastic Band, level: 3}
  - {id: aimd, title: Ab Initio Molecular Dynamics, level: 3}
  - {id: add-a-tutorial, title: Add a tutorial, level: 2}
  - {id: rebuild-recovered-pages, title: Rebuild recovered pages, level: 2}
---

## Keep the archive distinct

The four recovered chapters describe the original group's material. New tutorials should be separate pages with a named author, a date, tested software and hardware versions, and references. Do not silently replace historical commands or scientific settings. Use a pull request for corrections and explain the difference between the original text and the proposed update.

## Planned tutorials

These are reserved topics, not recovered or validated tutorials.

### Olivia and NRIS
{: #olivia-and-nris }

Reserved for current access procedures, environment modules, Slurm examples, storage and job accounting. Verify each instruction against the relevant NRIS system and document the verification date.

### VASP 6
{: #vasp-6 }

Reserved for version-specific setup and input guidance. The archive already contains a historical VASP 6.4.1 module example; that does not establish a current supported environment.

### DFT foundations
{: #dft }

Reserved for exchange-correlation functionals, convergence, defects and interpretation, with explicit evidence and assumptions.

### Nudged Elastic Band
{: #neb }

Reserved for newly tested workflows. The [recovered NEB section](/vasp-wiki/computational-methods/#nudged-elastic-band-neb) remains in the archive.

### Ab Initio Molecular Dynamics
{: #aimd }

Reserved for AIMD workflows, equilibration, timestep and ensemble choices, reproducibility and trajectory analysis. No AIMD guide was present in the supplied backup.

## Add a tutorial

Create a Markdown page under `_pages/vasp-wiki/` with the shared layout:

```yaml
---
layout: vasp-wiki
title: "A descriptive tutorial title"
permalink: /vasp-wiki/tutorial-slug/
wiki_id: tutorial-slug
author_profile: false
---
```

Use English headings and text. Use fenced code blocks labelled `bash`, `python`, `ini` or `text`, and keep long commands on their original lines. The existing site provides MathJax for mathematical notation. Code blocks are excluded from mathematical rendering.

Add the tutorial's link to the chapter navigation in `_layouts/vasp-wiki.html`. Identify its validation status and authors explicitly. A new tutorial may describe a current workflow while the recovered chapters remain labelled as historical.

## Rebuild recovered pages

The originals live in `files/vasp-wiki/originals/`. The standard-library migration script rebuilds the four articles, extracted wikitext and provenance manifest:

```bash
python scripts/vasp_wiki/migrate.py
python scripts/vasp_wiki/check.py
```

Do not edit the archived XML or binary files to correct a display issue. Fix the converter, document the recovery decision, regenerate and inspect the change. Generated articles carry stable chapter URLs and heading anchors. The PR workflow builds with GitHub's Pages-compatible Jekyll action, checks local links, original-file hashes and rendered code, and stores a preview artifact without deploying it.
