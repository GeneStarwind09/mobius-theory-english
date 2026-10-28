# Contributing

For translation changes, include the original wording, proposed English,
chapter/scene and reason. Check repeated dialogue and names against the glossary.
Preserve formatting placeholders, colour tags, pipe-delimited event arguments,
IDs, dates and puzzle values. The text corpus contains full-story spoilers.

For artwork, follow docs/ARTWORK.md. Keep the source canvas size and sprite
positions. Do not upload original game bundles, assemblies, movies or whole
extracted art packs. Image contributions should identify the Unity texture and
the exact source hash; keep any proposed public batch separate for review.

For code, run `python -m unittest discover -s tests -v` and
`python tools/validate.py`. Keep the patcher offline at runtime, retain its
backups and fail before writing when files do not match. Test game-dependent
changes on a separate copy; include install, restore and relevant in-game checks.
Public CI does not have the commercial game and cannot perform those checks.

Please be explicit about AI-assisted work and its review status. Automated
checks establish data integrity and some invariants; they do not establish
linguistic quality or full gameplay compatibility.
