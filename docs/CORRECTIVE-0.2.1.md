> Historical development record. Current release: [English patch 1.0.0](RELEASE-1.0.0.md).

# Corrective test patch 0.2.1-review

This revision responds to the completed playthrough report. It keeps full story descriptions and uses fixed bounds, smaller text and English word wrapping.

- 68 verified Unity layout objects: archive progress, item names and descriptions, Story Map labels, ending panel, choice text, instruction emblems and notification bounds.
- One formatter method now wraps whole English words. This is an intentional code change beyond the original 61 translated string literals.
- Care-home login artwork rebuilt with PhotoCraft. Both original input-box regions are pixel-identical, so live fields align with the artwork.
- Eleven subtitle cues translate chapter cards, the epilogue, Xu Yan's messages, two minigame cards and The End. Existing dialogue text and timing are preserved. The End uses a new GameOver.srt, removed by Restore Chinese.

The disappearing deduction text, blurred clue labels, accelerated video and persistent notification still need controlled runtime reproduction. This release does not claim to repair those faults. Playback and popup lifecycle code are unchanged.

Automated checks verify payload hashes, every modified layout tree, all 188 texture pixels and all untouched Unity object bytes. A disposable installation tests the packaged installer and restore. These checks do not replace in-game visual review of each affected screen.

Upgrade: close the game, Restore Chinese with the current patcher, then Install English with this complete package. Save files are untouched.
