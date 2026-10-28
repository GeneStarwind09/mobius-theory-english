# Mobius Theory — English fan translation

Open-source tools and English translation data for **轮回之理 — MOBIUS THEORY**,
[Steam app 1925830](https://store.steampowered.com/app/1925830/MOBIUS_THEORY/).

**Status: test release.** All six shipped subtitle files are translated. Story
choices, evidence, endings, inner monologues and many text-based menus are also
translated. Chinese text baked into artwork remains; an artwork editing and
verified reimport workflow is included. A full branch-by-branch audiovisual
playtest has not been completed.

## Transparency

- The Python patcher, C# text helper, translation data and build tools are here.
- The patcher makes replacements from each player's own installation.
- Original game movies, bundles, assemblies and extracted art are not included.
- No account or network connection is required by the installed patcher.
- Every modified file is backed up and checked with SHA-256 hashes.
- The Unity rebuild verifies all unrelated objects remain byte-identical.
- Automated Windows builds use the source checkout and pinned Python packages.

The initial translation and tools were developed with AI assistance. Human
wording review, visual checking of edited artwork and full gameplay testing
remain valuable contributions. The project does not claim an independent
professional review has already occurred.

## Install a built package

1. Extract the complete Windows patch ZIP, including `_internal/`.
2. Close the game and run `Mobius-English-Patcher.exe`.
3. Select the folder containing `轮回之理.exe`.
4. Click **Check Installation**, then **Install English** and wait for completion.
5. Launch normally through Steam. Enable subtitles in Settings if needed (`字幕`).

The supported game is **Steam build 9328697 / in-game version 1.0.20**. Actual
file hashes must match; a matching displayed version alone is not sufficient.
Allow about 1.5 GB free space, more for large future artwork batches.

To uninstall, close the game and click **Restore Chinese**. Backups are retained
inside `.mobius-english/original` in the game folder. The patcher does not edit
save files. Steam verification can also restore official files and remove the
patch. Updates or other mods may cause the checks to reject an installation.

The previously tested text patch is version 0.1.0. The source adds an artwork
workflow for the next revision; no translated artwork batch is included yet.

## Run or build from source

On 64-bit Windows with Python 3.10:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m unittest discover -s tests -v
powershell -NoProfile -File tools/build.ps1
```

The build script downloads **Mono.Cecil 0.11.6** from NuGet, verifies its pinned
SHA-256, and compiles `TextPatch.cs` with the Windows .NET Framework C# compiler.
It packages the Python program using PyInstaller. Windows .NET Framework 4.x
is used by the small text helper. No game data is required to build the tools.

Output: `dist/Mobius-Theory-English/` and `dist/Mobius-Theory-English.zip`, with
a SHA-256 checksum file. The `Windows build` Actions workflow runs the same
script and uploads its build artifact. Inspect the workflow run's commit before
downloading its artifact. This is a documented build process, not a claim of
bit-for-bit reproducible executables or a code-signing certificate.

For a non-frozen source run, copy the generated `TextPatch.exe` and
`Mono.Cecil.dll` from `.build/` beside `patcher.py`, then run:

```powershell
.venv\Scripts\python patcher.py
```

CLI usage: `python patcher.py --action check|install|restore --game "path"`.

## Artwork editing

[Export and reimport instructions](docs/ARTWORK.md) explain how to create a
searchable local pack, edit PNGs without moving their sprite positions, and
prepare a batch with validated image dimensions, identities and hashes.

## Translation and testing

`Translation-Review.csv` accounts for all 459 source cues as 458 English cues.
One duplicate source line lasting 20 ms is merged. Subtitle start times remain
fixed; short lines extend into available silence by at most 500 ms. Lines wrap
to at most two lines of 42 characters; the initial maximum calculated reading
rate is 24.75 characters per second.

`translations.json` contains 546 dictionary entries, used for 496 configuration
text occurrences, 144 UI text objects and 61 dynamic assembly literals. Values
are editable, with translation integrity hashes refreshed using
`python tools/validate.py --refresh-hashes` before building a revised release.

- [Context and glossary — full spoilers](docs/Context-and-Translation-Notes.md)
- [Initial text-patch validation report](docs/Validation-Report.md)
- [Contribution guide](CONTRIBUTING.md)

Please report wording, timing, layout and gameplay issues with the chapter,
scene, relevant timestamp and game build. Mark story spoilers clearly.

## Licence and affiliation

Original project contributions are under the [MIT licence](LICENSE). Original
game assets, original Chinese text and third-party software are outside that
grant. Dependency notices are retained in `licenses/` and
`THIRD-PARTY-NOTICES.txt`. This is an unofficial fan project, unaffiliated with
the developer and Valve. A purchased, installed copy of the game is required.
