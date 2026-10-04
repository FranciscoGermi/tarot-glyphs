# DECISIONS — what is settled, and why

**Edited in place to current truth.** A superseded decision is removed, not annotated.

---

## 1. What the project is

**A study first, with tests; a reading app later** (Francisco, 2026-10-04): draw spreads, see the cards
printed in glyphs, read what they mean. **Web with a phone layout is the leaning, not the decision.**
*"I think something web with mobile option is better. Also we have three.js if c++ does not reach
there."*

**The runtime waits** (his: *"I would like to have animated cards with the glyphs effects we have, but
we might not need everything. I think this needs to wait a bit to be decided."*). The candidates are a
browser shader (WebGL or WebGPU), three.js, and after-what-i-did's C++/Vulkan engine. Until it is
chosen, the glyph work is Python and offline (`tools/glyph.py`), so the findings carry to any of them.
§4 is an input to the choice that he has not weighed yet.

---

## 2. The card sources

**The Rider-Waite-Smith deck (1909, Pamela Colman Smith for A. E. Waite) is the primary deck**, and the
**Tarot de Marseille in Yoav Ben-Dov's restoration (CBD, 2010, after Nicolas Conver's 1760 deck)** the
second, both as scanned on steve-p.org's `RWSa` and `MaBD` pages (his pick: *"Its a tricky page to crawl
and get the good resolution pictures but is worth"*). **Everything those two pages link is taken**: the
cards at full size, the other images, the PDFs and the page text (his: *"I want everthing from
those"*). `tools/crawl_steve_p.py` owns how; the pages' own deck-by-deck notes are study material.

**The full-size card is behind a per-card key, not a session.** The page's script asks
`cscalc.php?fs=<stem>` for a short number and loads `pixe/<stem>_<number>.png`; the number is the same
on every call for a stem (checked twice, 2026-10-04), so the crawl is two plain requests a card. The
images are 1086 × 1810 PNGs of about 3 MB.

**What each source allows is in `THIRD_PARTY_LICENSES.md`** and decides what may ship. The difference
already visible: the 1909 art is in the public domain in the US, and the Ben-Dov deck is reported free
for **non-commercial** use only, which does not reach a product sold or ad-funded.

---

## 3. The glyph print, as after-what-i-did found it

Taken from after-what-i-did's `DECISIONS.md` §13 (*Chameleon glyphs*), where each was measured or judged
at the window. They are inherited, so each is re-checked on cards before a design leans on it.

- **A cell takes the glyph whose ink covers as much of it as the picture's light covers that patch,
  tinted with the patch's own colour.** It read, judged at the window, and it is the direction.
- **The ramp is measured off the font, not hand-picked**: all 256 glyphs counted, one per ink count,
  **the evenest of a tie**, since a box rule and a shade glyph can cover alike and the rule reads as an
  edge. `py tools/glyph.py` reproduces it: **57 steps** for the 8×16 font and **37** for the 8×8, as
  recorded there (checked 2026-10-04).
- **Each font has a 0.1875 hole**: the 8×16 between 0.5625 (▄) and 0.75 (▓), so it bands in the bright
  half; the 8×8 between 0.8125 and 1.0, at the top. Seen there as stripes across bright skies.
- **Density tracks linear light, and a patch is averaged in linear light**: averaging sRGB bytes
  darkens every patch with contrast in it. **A `gamma` of 2.2 reads better on continuous tone**; on a
  drawing the difference is small.
- **Square cells, not tall, for a picture**: a tall cell buys half the rows for the same count across.
- **48 to 64 cells across the subject** is where a photograph resolved; 16 to 24 was noise. **Below
  about 4 screen pixels a cell, the glyph is mush.**
- **The picture degrades to a picture**: past where glyphs resolve it still reads as a low-resolution
  image, not as noise.
- **Drawings carry far better than photographs**: flat colour with hard outlines survives the cell.
  That favours exactly these decks, which are line art with flat colour.
- **A base of about 0.5** under the ink: at 0 a dark picture sinks out of sight; at 1 the code page
  character is gone.

Not carried, because they are that renderer's: push-constant layout, the driver's `%` bug, the body
projections, bloom's internals. `PORT.md` points at them.

---

## 4. The fonts' licence constrains the runtime

**The Px437 fonts are CC BY-SA 4.0, and the credit to VileR is owed** in anything that ships them
(`assets/Px437.LICENSE.txt`). after-what-i-did kept ShareAlike away by rasterising the atlas in memory
from the unmodified fonts and never writing it out. **That reading does not transfer by itself**: a web
runtime that ships a pre-baked atlas PNG distributes an adaptation, and an offline pipeline that writes
glyph-printed card images is a greyer case. **Open**: rasterise in the browser from the shipped font, or
accept ShareAlike on the atlas, or choose another font. Decided with the runtime.

---

## 5. Left open deliberately

- The runtime (§1, §4).
- Which other decks to take, if any. steve-p.org has some thirty deck pages; only two are taken.
- Whether the product may be commercial, which decides whether the Marseille deck can be in it.
