# Linux installer — SteamOS / Linux x86-64

This package contains native **x86-64 Linux** executables and the complete
v1.0.0 English translation. It patches the Windows game installed by Steam;
launch the game normally through Proton afterward. There is no native Linux
port of the game itself.

## Install in Desktop Mode

1. Close Mobius Theory completely.
2. Extract the entire `.tar.gz` archive. Keep `_internal/`, `artwork/` and the
   other files beside the executable.
3. Run **Mobius-English-Patcher** or **Launch-Patcher.sh**. If the file manager
   asks, choose to execute it. The archive preserves executable permissions.
4. Check the detected Steam game folder, or select it with Browse. Steam's
   Manage > Browse local files can help locate it.
5. Choose **Check Installation**, then **Install English**, and wait for completion.
6. Return to Steam and launch the game through Proton. **Proton Experimental is
   recommended** (see the testing notes below). Enable subtitles.

No sudo, system package installation, Python, .NET, Mono or Wine is needed by
the installer. Desktop Mode and a graphical display are needed for its window.
The owner tested this installer on a Steam Machine running SteamOS: installation
worked, the Steam game directory was detected automatically, and patched gameplay
appeared correct. Steam Deck and a complete Linux playthrough are not yet confirmed.

## Proton and playback notes

The tester encountered an audio/video sync issue with standard Proton. After
switching to Proton Experimental, no further sync or other issues appeared during
about ten minutes of play. Proton Experimental is therefore the tester's
recommendation, not a verified fix: the improvement could be coincidental.
Intermittent playback problems were also reported during Windows QA; their cause
has not been established. Restart the game if playback loses sync.

Download **Mobius-Theory-English-Linux-x86_64-v1.0.0.tar.gz** from the
[v1.0.0 release](https://github.com/GeneStarwind09/mobius-theory-english/releases/tag/v1.0.0).
The release provides `LINUX-SHA256SUMS.txt` and `linux-build-info.json`; the latter
identifies the exact source revision used for the executable. The tested archive
is published unchanged. Its bundled instructions and build-time report predate
the SteamOS test; this page and `Linux-Release-Notes.md` record the updated results.

To uninstall, close the game and choose **Restore Chinese**. Saves are not
changed. If another patch revision is installed, restore it before upgrading.
Backups are kept in `.mobius-english/original` under the game folder.

For a terminal launch:

```sh
./Launch-Patcher.sh
./Mobius-English-Patcher --action check --game "/path/to/轮回之理"
```

The package targets glibc-based x86-64 Linux and is built on Ubuntu 22.04 for
compatibility with SteamOS. It is not an ARM or Alpine/musl package. If an
external drive is mounted with execution disabled, extract the patcher under
your home directory; the game can remain on its Steam library drive.

## Validation and transparency

The portable assembly delta reproduces the exact approved v1.0.0 Windows
Assembly-CSharp.dll, checked with SHA-256 before and after patching. The original
assembly is required and is not distributed. The tool that generates the delta
is `tools/make_managed_patch.py`; maintainers generate it from the original game
and the approved output of the public C# patcher. Recreate it after changing the
managed translations or word-wrap helper.

The Unity bundle is rebuilt and verified using the same artwork, text, font and
layout code as Windows. The installer never rewrites video playback or controls.
Linux build tests verify native dependencies, running-game detection and safe
failure on unsupported files. The owner has now confirmed installation and a
short patched gameplay test on SteamOS. See the scope and playback notes above.

Build from source on x86-64 Linux with Python 3.10:

```sh
python -m pip install -r requirements.txt
python tools/fetch_release_artwork.py
python tools/validate.py
python -m unittest discover -s tests -v
python tools/package_linux.py
```

Building requires compiler/build tools and Tk development/runtime dependencies;
the extracted user package bundles Python and its application dependencies.
The Linux build workflow documents the runner setup and checks.
