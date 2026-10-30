# Linux installer — SteamOS testing build

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
6. Return to Steam and launch with your usual Proton settings. Enable subtitles.

No sudo, system package installation, Python, .NET, Mono or Wine is needed by
the installer. Desktop Mode and a graphical display are needed for its window.
SteamOS game compatibility was reported by the owner on a Steam Machine;
Steam Deck and a complete Linux playthrough are not yet confirmed.

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
failure on unsupported files. Testing the full commercial game install and
gameplay on SteamOS remains the owner's next step.

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
