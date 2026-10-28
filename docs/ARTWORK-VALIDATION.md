# Artwork workflow validation — 28 October 2026

The initial local editing pack contains **648 static textures**, including
403 high-priority candidates, with 27 contact sheets and a searchable gallery.
The priority filter is a category-based aid, not verified Chinese text detection.
381 animation/effect textures, technical textures and font atlases are excluded
from that pack. Original video frames are outside its scope.

Ten automated tests passed for translation payload integrity and artwork
preparation: stable texture identity and replacement hashes, resized files,
flattened transparency, unknown names, changed originals, unchanged copies,
path traversal, duplicate IDs and payload revision tracking.

A separate integration check used two real exported textures: a transparent
language label and an opaque 1920×1080 tutorial image. Artificial test edits
were prepared, inserted with the English text into a complete rebuilt Unity
bundle, decoded again, and compared with the intended RGBA pixels. Both matched
exactly, and every unrelated Unity object remained byte-identical.

The artificial test edits are not in the source repository or a user release.
No actual English artwork batch has been reviewed or installed. Once edited
art is supplied, its wording, alpha edges, mipmaps, sprite placement and in-game
appearance still need review. The earlier text patch's live visual checks are
recorded in Validation-Report.md; this report does not extend those checks to
new translated artwork.
