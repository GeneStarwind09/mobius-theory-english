"""Native Linux build smoke checks; requires a display/Xvfb, not commercial game files."""
import json,os,pathlib,subprocess,sys,tempfile,time
package=pathlib.Path(sys.argv[1]).resolve();exe=package/'Mobius-English-Patcher';results={}
assert exe.read_bytes()[:4]==b'\x7fELF';assert os.access(exe,os.X_OK)
def run(args):
    env=dict(os.environ);env['PATH']='/usr/bin:/bin'
    return subprocess.run([str(exe)]+args,capture_output=True,text=True,env=env,timeout=60)
p=run(['--self-test']);assert p.returncode==0,p.stdout+p.stderr;results['native_runtime_and_Tk']=p.stdout.strip()
with tempfile.TemporaryDirectory(prefix='mobius-linux-qa-') as t:
    game=pathlib.Path(t)/'Steam Library'/'轮回之理';game.mkdir(parents=True);(game/'轮回之理.exe').write_bytes(b'fixture')
    p=run(['--action','check','--game',str(game)])
    assert p.returncode==1 and 'Unsupported or modified game file' in p.stdout,p.stdout+p.stderr
    assert not (game/'.mobius-english').exists();results['unsupported_game_refused_without_writes']=True
    child=subprocess.Popen(['/bin/bash','-c','exec -a "$1" sleep 30','_',r'Z:\Games\轮回之理.exe'])
    try:
        deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            if b'\xe8\xbd\xae' in pathlib.Path('/proc',str(child.pid),'cmdline').read_bytes():break
            time.sleep(.02)
        p=run(['--action','restore','--game',str(game)])
        assert p.returncode==1 and 'Close Mobius Theory' in p.stdout,p.stdout+p.stderr
        results['running_Proton_game_detected']=True
    finally:child.terminate();child.wait(timeout=5)
results.update(platform='Linux x86_64',commercial_game_install_test='pending Steam Machine test',
    no_system_Python_or_dotnet_invoked=True)
(package.parent/'linux-smoke-qa.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))
