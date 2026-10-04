# PORT — what comes across from after-what-i-did

**Translation status, not reasoning.** Sources are under `D:/projects/after-what-i-did/`, and that
project is not modified by this one. **This file is deleted when the port is done.**

**The rule:** reuse anything that serves the glyph look; the new project wins every inconsistency.
Nothing renderer-bound is ported until the runtime is chosen (`DECISIONS.md` §1).

---

## Done

- **The fonts**, unmodified: `assets/Px437_IBM_VGA_8x16.ttf`, `assets/Px437_IBM_BIOS.ttf`, and
  `assets/Px437.LICENSE.txt` with the credit their author asks for.
- **The pattern library**, `assets/glyph-patterns.txt`, verbatim. Its parser
  (`engine/glyph/patterns.hpp`) is not ported yet.
- **The ramp and the bitmaps**, from `tools/canary.py` (`cp437_codepoints`, `glyph_bitmaps`,
  `glyph_ramp`, the sRGB pair) into `tools/glyph.py`, with no capture or engine dependency. Its check
  reproduces the source's 57 and 37 steps.
- **The working agreement**, adapted, into `CLAUDE.md`; `tools/sec.py` unchanged; `tools/comment_cap.py`
  with web source types added; `.githooks/pre-commit`.

## Port when the runtime is chosen

| source | what it is | port as |
|---|---|---|
| `engine/glyph/chameleon.hpp` | the ramp in C++, and a picture into a sheet of glyph bytes and colours | the runtime's print, checked against `tools/glyph.py` |
| `engine/glyph/atlas.cpp`, `atlas.hpp` | the atlas rasterised from the fonts in memory, and the halo atlas | the runtime's atlas, if §4 keeps it in memory |
| `engine/glyph/patterns.hpp` | the pattern file's parser | a parser for the card frames' patterns |
| `engine/glyph/look.hpp`, `look_view.hpp` | per-slot glyph colour, base and animation, as a strict text file | the card's look, if cards get slots |
| `engine/glyph/raised.hpp`, `breath.hpp` | the relief and breathing effects | reference for animated cards |
| `shaders/glyph.slang` | the glyph surface: per-fragment glyph pick, effects, relief, the picture print | reference for a WebGL/WebGPU shader; three.js takes a GLSL port |
| `shaders/post.slang`, `engine/renderer/vulkan/bloom.cpp` | the composite and the bloom chain | reference, if the cards glow |
| `tools/canary.py`, `tools/mutate.py` | predict every pixel of a capture, and check a test can fail | the runtime's instruments |
| `.claude/skills/awid-critic` | the blind critic loop | with the first capture worth judging, trimmed of the game's shot tools |

## Not needed

The body, the dungeon, the world, the level mesh, Blender and Mixamo tooling, the HUD senses, the
playground binary, SDL and Vulkan setup (unless the C++ engine wins), `game/paintings.hpp` (its
picture averaging is three lines of numpy here).
