"""The glyph core, lifted from after-what-i-did's tools/canary.py: code page 437 bitmaps read off the
Px437 fonts' outlines, and the coverage ramp a picture is printed with. py tools/glyph.py checks both."""
import math
import pathlib
import sys

import numpy as np
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONTS = {"tall": ("Px437_IBM_VGA_8x16.ttf", 16), "square": ("Px437_IBM_BIOS.ttf", 8)}
CP437_SYMBOLS = "☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼"


def srgb_to_linear(c):
    c = np.asarray(c, dtype=float)
    return np.where(c <= 0.04045, c / 12.92, np.power((c + 0.055) / 1.055, 2.4))


def linear_to_srgb(linear):
    linear = np.clip(linear, 0, 1)
    return np.where(linear <= 0.0031308, linear * 12.92, 1.055 * np.power(linear, 1 / 2.4) - 0.055)


def cp437_codepoints():
    """Byte to Unicode, from the codec and the IBM graphic set; 0x00 is a blank and 0x7F the house."""
    out = [0x20] + [ord(c) for c in CP437_SYMBOLS]
    out += [ord(bytes([b]).decode("cp437")) for b in range(0x20, 0x7F)] + [0x2302]
    out += [ord(bytes([b]).decode("cp437")) for b in range(0x80, 0x100)]
    return out


def glyph_bitmaps(font_file, cell_h):
    """All 256 glyphs as 8 x cell_h booleans: a texel is ink if its centre is inside the outline.
    A codepoint the font has no glyph for comes back blank."""
    font = TTFont(ASSETS / font_file)
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    ascent, descent = font["hhea"].ascent, font["hhea"].descent
    unit = (ascent - descent) / cell_h
    out = np.zeros((256, cell_h, 8), dtype=bool)
    for b, code in enumerate(cp437_codepoints()):
        name = cmap.get(code)
        if name is None:
            continue
        for row in range(cell_h):
            for col in range(8):
                pen = PointInsidePen(glyphs, ((col + 0.5) * unit, ascent - (row + 0.5) * unit))
                glyphs[name].draw(pen)
                out[b, row, col] = bool(pen.getResult())
    return out


def glyph_ramp(bitmaps, gamma=1.0):
    """Luminance level 0-255 to glyph byte: one candidate per ink texel count, the evenest of a tie,
    because a rule and a shade glyph can cover alike and the rule reads as a false edge."""
    count, cell_h = bitmaps.shape[0], bitmaps.shape[1]
    fx = (np.arange(8) + 0.5) / 8.0
    fy = (np.arange(cell_h) + 0.5) / cell_h
    even = 1.0 / math.sqrt(12.0)
    best = {}
    for g in range(count):
        on = bitmaps[g]
        n = int(on.sum())
        if n == 0:
            uneven = 0.0
        else:
            xs = np.broadcast_to(fx, on.shape)[on]
            ys = np.broadcast_to(fy[:, None], on.shape)[on]
            sx, sy = float(xs.std()), float(ys.std())
            uneven = (abs(float(xs.mean()) - 0.5) + abs(float(ys.mean()) - 0.5)
                      + abs(sx - sy) + 0.5 * abs(0.5 * (sx + sy) - even))
        if n not in best or uneven < best[n][0]:
            best[n] = (uneven, g)
    steps = [(n / (8.0 * cell_h), best[n][1]) for n in sorted(best)]
    ramp = np.zeros(256, dtype=int)
    for level in range(256):
        target = (level / 255.0) ** (1.0 / gamma)
        pick, gap = 0, abs(steps[0][0] - target)
        for i in range(1, len(steps)):
            d = abs(steps[i][0] - target)
            if d < gap:
                gap, pick = d, i
        ramp[level] = steps[pick][1]
    return ramp, steps


def main():
    want = {"tall": 57, "square": 37}
    bad = 0
    for shape, (font_file, cell_h) in FONTS.items():
        _, steps = glyph_ramp(glyph_bitmaps(font_file, cell_h))
        gap = max(b[0] - a[0] for a, b in zip(steps, steps[1:]))
        ok = len(steps) == want[shape]
        bad += not ok
        print(f"{shape}: {len(steps)} coverage steps (want {want[shape]}), widest gap {gap:.4f}"
              f" {'OK' if ok else 'MISMATCH'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
