# English patch 1.0.0 — 30 October 2026

First public complete release for Mobius Theory, Steam build 9328697 / game 1.0.20.

Includes 471 subtitle cues, 546 dictionary entries covering 496 configuration
occurrences, 144 UI text objects, 61 managed text literals and 189 artwork
replacements. Thirteen subtitle cues translate important video overlays.
No original movie, audio, game bundle, assembly or font data is distributed.

English layout corrections preserve full descriptions, wrap at word boundaries,
fit evidence and popup panels, align the care-home login fields and accommodate
Story Map titles. Thirty-five translated sprite labels use full-canvas geometry
so their English letters are not clipped by Chinese-character-shaped meshes.
Mind Palace uses the game's own English font atlas on its primary renderer,
retaining its original animation, hold-to-reveal shader and puzzle logic.

The owner completed a full English playthrough and additional QA passes. On
30 October they confirmed both the final Mind Palace interaction and Close
button checks passed. Twenty automated tests and a disposable Windows
install/check/reinstall/restore cycle support the release. This does not claim
exhaustive branch or hardware coverage.

## Installation and upgrade

Download Mobius-Theory-English-v1.0.0.zip and extract everything. Run the included
patcher with the game closed. Check Installation, then Install English. Launch
through Steam with subtitles enabled. Restore Chinese uninstalls it; saves stay
intact. Restore an earlier English patch before installing a different version.
The approved 0.2.4 QA revision already has identical game-file replacements.

## SteamOS / Linux package added

A native x86-64 Linux installer is available alongside the Windows ZIP. It applies
the same v1.0.0 game-file replacements. The owner confirmed installation, automatic
Steam-library detection and a short patched gameplay test on a Steam Machine.
Use [the Linux instructions](LINUX.md) in Desktop Mode, then launch the game via
Proton. Proton Experimental is recommended based on the tester's experience, but
is not a proven fix for intermittent audio/video sync issues. A full SteamOS
playthrough and Steam Deck testing are not claimed.

## Known limitations and reported technical issues

- A few long Story Map names can remain crowded, especially narrow ending cards.
- Logos are bilingual. Incidental scenery, branding and nonessential video text
  may remain Chinese; important identified video overlays have English captions.
- Numeric and symbol puzzle clues retain their original design. The abstract
  chapter-two keypad puzzle is unchanged by the translation.
- During QA, late-game video sometimes accelerated while audio stayed normal.
  Restarting the game and continuing restored normal playback, occasionally
  requiring a second restart. Its cause has not been established.
- A late-game success notification sometimes remained on screen until restart.
  Its cause has not been established either.

The patch does not rewrite video playback or notification timing. That alone
does not prove the translation cannot influence these issues. Please include
recordings and original-versus-English comparisons when reporting them.

The personal soundtrack extraction and provisional music-location notes are not
part of this release; they do not establish composer credits or audible ending
music assignments.
