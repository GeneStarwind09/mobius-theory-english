# Mind Palace primary font correction — 0.2.4-review

The owner compared the original Chinese and English versions: the original clue
words return after the opening shrink animation; the English words did not.
The issue must therefore be treated as a translation regression.

The original primary TMP font contains 5,914 characters but no printable ASCII.
All ten English clue labels consequently require fallback glyphs and a separate
submesh. The puzzle's TextMeshProFill component updates the primary renderer's
material; it does not update fallback renderers. The original showClues animation
scales the SelectText parent and returns its scale to one.

This correction removes that fallback dependency. During installation it reuses
the existing Liberation Sans SDF font tables and Alpha8 atlas from the owner's
resources.assets and resources.assets.resS, with verified source hashes. Those
files are read only. The destination keeps its font, texture and material object
IDs, and its original TextMeshPro/SpritesFill shader and reveal properties.
Atlas dimensions, padding and weight metrics match the copied glyph data. Every
character in all ten translated labels is checked against the primary font.
No original font or atlas is distributed in the patch package.

The correction changes three bundle objects: the font asset, its atlas and its
material metrics. Original animation, click/hold logic, clue answers and colliders
are retained. All 189 artwork replacements, 109 layout/geometry objects and 471
subtitle cues from 0.2.3 are retained. The managed assembly patch is unchanged.

The installer is now labelled English Patch. Version 0.2.4-review remains a local
QA version pending native confirmation; it is not a published v1.0 release.
Structural and installation checks cannot prove the in-game animation is fixed.

## Remaining in-game check

Enter Mind Palace, let the opening animation complete, and confirm all ten
English labels reappear. Hold a correct clue and verify the reveal effect, then
open and close its detail popup. Finish the three correct selections. Repeat
after reopening the section to check a second initialization.

Installation into the Steam folder is deferred while the owner is away; no
administrator prompt will be opened until they return.

## Final verification — 30 October 2026

Installed successfully with all hashes and independent asset checks passing.
The owner then confirmed the Mind Palace and Close-button tests both passed.
The same game-file replacements are promoted to release 1.0.0.
