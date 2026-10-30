> Historical development record. Current release: [English patch 1.0.0](RELEASE-1.0.0.md).

# Corrective test patch 0.2.2-review

The second playthrough review confirmed most layout fixes. This revision addresses the remaining reported details:

- Thinking Hall Close, heading and feedback text use the readable Source Han Sans font and its matching material instead of UniDreamLED, whose letterforms were unsuitable for English words. The Close label is vertically centered.
- The right-edge continuation prompt reads "Click to continue." inside a narrower 250-pixel text region. Its existing click interaction is retained.
- Chapter 5 opening title and "Three years earlier..." have timed English captions. Existing subtitle text and timing are preserved.
- Both Chinese-only static logo textures (the small reusable logo and the ending background logo) use the game's existing bilingual title-screen artwork. Existing bilingual logo backgrounds are unchanged.
- Story Map layout is retained as accepted by the reviewer.

The payload now contains 189 artwork replacements, 74 layout objects and 471 English subtitle cues. Earlier unresolved runtime faults are not claimed fixed. In-game visual confirmation of the font/material change is still needed.

Original Chinese files and the previous English revision are backed up when applying the local upgrade. Save files are untouched. The music extraction is a separate personal output and is not part of this patch or public source repository.
