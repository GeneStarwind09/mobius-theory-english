"""Platform-specific discovery and running-game checks; no Proton dependency."""
import os,pathlib,re

GAME_EXE='轮回之理.exe'


def linux_game_running(proc_root=pathlib.Path('/proc')):
    for process in pathlib.Path(proc_root).iterdir():
        if not process.name.isdigit() or int(process.name)==os.getpid():continue
        try:args=(process/'cmdline').read_bytes().split(b'\0')
        except (FileNotFoundError,PermissionError,ProcessLookupError):continue
        for arg in args:
            name=arg.decode('utf-8',errors='replace').strip('"').replace('\\','/').rsplit('/',1)[-1]
            if name.casefold()==GAME_EXE.casefold():return True
    return False


def linux_steam_roots(home=None,environ=None):
    home=pathlib.Path(home or pathlib.Path.home());environ=os.environ if environ is None else environ
    roots=[home/'.local/share/Steam',home/'.steam/steam',home/'.steam/root',
           home/'.var/app/com.valvesoftware.Steam/.local/share/Steam']
    client=environ.get('STEAM_COMPAT_CLIENT_INSTALL_PATH')
    if client:roots.insert(0,pathlib.Path(client))
    return roots


def steam_game_candidates(roots):
    libraries=[];seen=set()
    for root in roots:
        root=pathlib.Path(root);vdf=root/'steamapps/libraryfolders.vdf'
        libraries.append(root)
        if vdf.is_file():
            libraries.extend(pathlib.Path(p.replace('\\\\','\\')) for p in
                re.findall(r'"path"\s+"([^"]+)"',vdf.read_text(encoding='utf-8',errors='replace')))
    for lib in libraries:
        key=str(lib.resolve())
        if key in seen:continue
        seen.add(key);app=lib/'steamapps/appmanifest_1925830.acf'
        if not app.is_file():continue
        match=re.search(r'"installdir"\s+"([^"]+)"',app.read_text(encoding='utf-8',errors='replace'))
        if match:yield lib/'steamapps/common'/match[1]
