# Optional translated artwork

No original game images or edited image batch is committed here.

Use `tools/artwork.py export` to create a local editing pack from your own game.
Use `tools/artwork.py prepare` to validate returned PNGs and place a batch here.
The patcher loads `artwork/manifest.json` only when it exists.

Files in a prepared batch have stable Unity IDs, expected source pixel hashes,
fixed dimensions and replacement SHA-256 hashes. The patcher verifies those,
encodes replacement textures losslessly as RGBA32, preserves sprite references,
and verifies the decoded pixel data after rebuilding the Unity bundle.

Regenerated mipmaps and uncompressed textures can increase bundle size. The
original shared texture resource remains intact; unrelated objects are checked
byte-for-byte. Always inspect the artwork in the actual game before release.

See [the artwork workflow](../docs/ARTWORK.md).
