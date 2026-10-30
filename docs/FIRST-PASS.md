> Historical development record. Current release: [English patch 1.0.0](RELEASE-1.0.0.md).

# First-pass test patch — 0.2.0-firstpass

The local playthrough package combines the English subtitle/text patch and 188
translated artwork textures: 100 in batch 1, 49 in batch 2, 38 in batch 3 and
one final computer screen in batch 4. The darts instructions now include the
previously missed footer: “Reach the highest stage for a hidden reward.”

The artwork audit covers all 648 static textures in the editing pack. Remaining
originals are retained intentionally: textless props, photographs, backgrounds,
visual effects, numeric/symbol clues, official title branding, decorative text,
or thumbnail microprint whose readable full-size evidence is translated.
An additional 381 animation textures and six technical textures were inspected;
no additional readable gameplay instructions were identified. Four empty
texture placeholders contain no image data. This is a visual first pass,
not an OCR-certified guarantee that every Chinese glyph has been replaced.

Chinese title logos, QQ/WeChat branding and incidental photographed scenery may
remain. Original numeric puzzle clues are retained. The old darts tutorial
describes mobile tilt/touch controls; whether the Steam version displays that
particular texture remains unconfirmed. Text photographed into movies is
outside the static-texture patch. No movie files are redistributed or changed.

The user approved batch 1 and the spoiler-free portions of batches 2 and 3.
Story-sensitive artwork remains pending their post-playthrough review. Batch 4
and the revised darts footer also await their review. Technical checks verify
native dimensions, PNG identities/hashes, rebuilt RGBA pixels, translated Unity
text and byte preservation of unrelated Unity objects. These checks do not
replace an in-game branch-by-branch playthrough.

## Install or upgrade

Close the game. If an earlier English patch is installed, first use **Restore
Chinese** in the patcher, then **Check Installation**, then **Install English**
in the new package. The patcher deliberately rejects overwriting a different
patch revision. Restoration retains backups and does not edit saves. Keep the
whole extracted package together, including `_internal` and `artwork`.

This is a local test build for the supported Steam build 9328697 / game 1.0.20.
It has not been published as a final GitHub release. The code is open source;
local extracted originals, generation attempts and original game binaries are
excluded from the source repository.
