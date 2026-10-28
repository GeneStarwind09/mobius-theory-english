# Artwork translation workflow

## Export

With the pinned Python environment installed:

```powershell
python tools/artwork.py export --game "D:\SteamLibrary\steamapps\common\轮回之理" --out "editing-pack"
```

The exporter reads the patcher's original backup when present, otherwise the
installed bundle. It validates the source against the supported build hash.
It does not write to the game directory. PNGs are decoded from actual Texture2D
objects, not screenshots, with their original dimensions and alpha channel.

Open `editing-pack/index.html`. It has a high-priority view, category filtering,
ID/filename search and links to full-resolution originals. Contact sheets are
for browsing only. The inventory includes candidate artwork that may have no
text; it is not a claim that OCR has detected Chinese in every image.

Font atlases, empty placeholders, and animation/effect frames are excluded.
Pass `--include-effects` only if you need to inspect the latter. Original movie
frames and text embedded in the videos are not part of this exporter.

## Edit and return

- Work from `originals/`, never thumbnails or contact sheets.
- Save only changed PNGs to `replacements/`, keeping category folders and filenames.
- Keep canvas dimensions, transparency, layout and sprite positions unchanged.
- Preserve dates, digits, diagrams, highlighted symbols and puzzle solutions.
- Return the replacements and `assets.json`. Partial batches are supported.
- Check spelling and wording produced by image AI against the story glossary.

Example editor instruction:

> Replace only the Chinese writing with the supplied English translation.
> Match the original typography, lighting, perspective and wear. Preserve the
> exact canvas size, transparent background, icons, numbers and puzzle symbols.
> Do not crop, upscale, move UI elements, or add a background behind transparent art.

## Prepare a batch

```powershell
python tools/artwork.py prepare --pack "editing-pack" --edited "editing-pack/replacements" --out "artwork"
```

Preparation rejects unknown filenames, non-PNG files, changed dimensions,
changed original exports and obviously flattened transparency. Unchanged
copies are skipped. Transparent backgrounds and corners are checked, but
visual review is still needed for partially transparent artwork.

Restore Chinese before installing a revision with a new artwork batch. The
patcher refuses to silently treat an earlier installed payload as the new one.
Only the selected textures are replaced; the original game's videos, sprite
rectangles, pivots and object references remain unchanged.

## Repository boundaries

The public source tree includes the tools and schema, not the extracted original
art pack. Local exports and replacement batches are ignored by Git. Review any
future public image contribution separately before intentionally tracking it.
