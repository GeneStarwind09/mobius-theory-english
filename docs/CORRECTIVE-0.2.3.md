> Historical development record. Current release: [English patch 1.0.0](RELEASE-1.0.0.md).

# Close-label geometry correction — 0.2.3-review

The preceding font correction improved live headings but did not repair the visible Close label. That label is also a translated texture rendered through Sprite 602000. Its original tight mesh consists of disconnected regions around two Chinese characters, leaving a gap across the center of the English word. Reproducing that geometry against the approved English texture produces precisely the reported C / e fragments; only 33.09% of the English alpha lies within the old mesh.

A follow-up audit found 35 translated SpriteRenderer labels whose English texture pixels exceeded their original tight meshes. This revision replaces each affected sprite mesh with a four-vertex, two-triangle rectangle covering its native canvas (158 x 48 pixels for Close) and clears its Tight mesh flag. It preserves the sprite ID, texture ID, pixels, pivot, pixels-per-unit and all button collider/interaction objects. Existing physics outlines are retained; the button uses its separate original BoxCollider.

The payload retains 189 artwork replacements and 471 subtitle cues. There are now 109 layout/geometry objects. All unrelated object bytes are checked during rebuilding. Each repaired sprite extraction is checked against every pixel of its existing English texture during the disposable installation test. Native in-game confirmation remains pending.

No ending-music path changes are included. The user confirmed silent ending screens, consistent with original missing-path errors. The earlier ending-track list describes inferred intended assignments, not verified audible placements. No composer attribution has been established.
