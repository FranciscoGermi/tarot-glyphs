# STATE — what exists, what is next, what is open

Rewritten in place at each handoff (`CLAUDE.md`). Near 250 lines at most.

---

## What exists

- **The scaffold**, taken from after-what-i-did (`PORT.md` has what and from where): the Px437 fonts and
  their licence, the glyph pattern library, the working agreement, `tools/sec.py`,
  `tools/comment_cap.py` and its pre-commit hook (`core.hooksPath` is set in this clone).
- **`tools/glyph.py`**: code page 437 bitmaps off the fonts' outlines and the coverage ramp. `py
  tools/glyph.py` checks it against after-what-i-did's recorded numbers: 57 and 37 steps, both pass.
- **`tools/crawl_steve_p.py`** and its take in `research/sources/steve-p/` (gitignored): everything the
  `RWSa` and `MaBD` pages link. Resumable; `manifest.json` records URL, size, SHA-256 and date.
  Taken 2026-10-04, 183 files, 610 MB, no retries: **RWS** 78 cards and 2 backs at 1086 × 1810;
  **Marseille** 78 cards and 10 extras (backs, a blank, title cards, box faces) at 1300 × 2562; the two
  author portraits; seven PDFs (both LWBs, Waite's *Pictorial Key*, Jensen's *Early Waite-Smith Tarot
  Editions*, Mathers' *The Tarot*, two divinatory-meanings tables); both pages' HTML and text. A contact
  sheet of each deck was looked at: no bad or truncated scan.
- **The documents**: `DECISIONS.md` (the project, the sources, the inherited glyph findings, the fonts'
  licence against the runtime), `PLAN.md`, `PORT.md`, `THIRD_PARTY_LICENSES.md`.

Nothing is committed: the repository is initialised with no commits.

## What is next

`PLAN.md` step 2, the licences at their sources.

## What is open

- **The runtime**: web shader, three.js or the C++ engine (`DECISIONS.md` §1, §4).
- **Whether the product may be commercial**, which decides whether the Marseille deck is in it.
- **Rule 19 in `CLAUDE.md` (crawl politely, licence first) is proposed, not agreed.**
- **The critic skill is held** until there is a capture worth judging.

## Not verified

- Every finding in `DECISIONS.md` §3 except the ramp's step counts is inherited from a 3D surface and
  not yet re-checked on a card.
- Which printing of the RWS deck the "Rider" scans are.
