# PLAN — the order of the work ahead

Each step goes through plan mode (`CLAUDE.md` rule 1). Deleted when its last step is done.

---

## 2. The licences, read at their sources

Read and record in `THIRD_PARTY_LICENSES.md`, with the date: Ben-Dov's own terms at cbdtarot.com (the
non-commercial claim is steve-p's report of it), what steve-p.org says of its scans, and the 1909 art's
status outside the US (Pamela Colman Smith died in 1951, so life + 70 ended in 2021 where that rule
applies; check, do not assume). Also: which RWS printing steve-p's "Rider" scans are, from Jensen's
*Early Waite-Smith Tarot Editions*, already in the take.

## 3. First print of a card

`tools/glyph.py` grows a print: one card into glyph bytes and colours, written as a PNG and as HTML
text. Sweep cells across (32, 48, 64, 96), square against tall, gamma 1 against 2.2, base 0 to 1, on a
few cards chosen for range (a dark one, a bright sky, a busy one: The Moon, The Sun, Ten of Wands).
**Re-check §3's inherited findings on cards** and put the contact sheets to Francisco: *"does it read?"*

## 4. The study's first documents

From the take's PDFs and pages, with rule 2's citations: the deck's structure and naming across the two
traditions (Marseille's numbering and titles against Waite's swaps of Strength and Justice), and each
card's meanings as Waite's *Pictorial Key* gives them, upright and reversed, as structured data
(`research/data/`) so an app can read it. Each claim keeps its book and page.

## 5. The runtime decision

With step 3's look in hand: a small animated card in a browser shader and in three.js, measured on a
phone, against what the C++ engine already does. The fonts' licence (`DECISIONS.md` §4) is part of the
question. Then the reading app is planned.
