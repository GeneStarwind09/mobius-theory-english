# Validation report — 28 October 2026

## Translation data

- Six SRT files; all 459 source cues accounted for in the bilingual review CSV.
- 458 output cues; the source's duplicate 20 ms bathroom cue is merged.
- No Chinese characters remain in the SRT translation text.
- Sequential cue numbering, positive durations and no overlapping cues.
- At most two lines per cue; longest line: 41 characters.
- Highest computed reading rate: 24.75 characters per second.
- 546 translation dictionary entries; no Chinese characters in translated values.
- 496 configuration text occurrences and 144 UI text objects verified after bundle reconstruction.
- Every other Unity object compared byte-for-byte against its source representation.

## Installation and restoration

- Installed-state hash verification passed.
- Repeated install is idempotent.
- Modified installed files rejected without overwriting any target.
- Restore is byte-for-byte identical for all eight original files.
- Unsupported source build rejected before patching.

- The standalone packaged Windows executable completed a full installation on a separate test copy, without relying on an external Python installation.
- The standalone executable's restore operation completed and all eight restored target hashes match their originals.
- The standalone GUI detected the Steam installation and verified the installed patch successfully.
- The live game installation was patched and all installed target hashes were checked.

## Managed assembly comparison

- 3,236 methods and 70,914 instructions compared.
- Method names, instruction opcodes, non-token operands and referenced member/type names match.
- All 61 changed string literals match the translation dictionary.

## Live visual checks

- Patched game opened through Steam.
- Main menu: English labels rendered with Latin glyphs.
- Opening video: English subtitles displayed over the original footage.
- First home investigation: translated tutorial heading and instruction displayed.
- Standalone patcher GUI: folder field, buttons and installed-hash result displayed.

## Remaining validation

A full audiovisual playthrough and every branch/ending have **not** been completed. Later subtitle timing, long evidence/ending text layout, all puzzle interactions and all story transitions have not been exhaustively checked in live gameplay. Texture-based Chinese interface labels and puzzle/document artwork remain. These limitations make this a test release, not a claim of a fully localised, publication-ready game.
