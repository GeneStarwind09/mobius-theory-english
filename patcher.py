"""Mobius Theory English patcher. Builds replacements from the owner's game files."""
from __future__ import annotations
import pathlib,hashlib,json,os,sys,re,shutil,tempfile,subprocess,argparse,threading,queue
from artwork_support import payload_id,load_replacements,apply_replacements,verify_replacements

BASE=pathlib.Path(sys.executable).parent if getattr(sys,'frozen',False) else pathlib.Path(__file__).resolve().parent
CREATE_NO_WINDOW=0x08000000 if os.name=='nt' else 0

def digest(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def read_json(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))

def atomic_json(p,data):
    temp=p.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,p)

def targets(manifest):
    result={x['path']:x['original_sha256'] for x in (manifest['bundle'],manifest['managed'])}
    for name,info in manifest['subtitles'].items():result['轮回之理_Data/StreamingAssets/Videos/'+name]=info['original_sha256']
    return result

def safe_path(root,rel):
    p=(root/rel).resolve()
    if root.resolve() not in p.parents:raise RuntimeError('Unsafe target path: '+rel)
    return p

def game_running():
    p=subprocess.run([str(BASE/'TextPatch.exe'),'--running'],creationflags=CREATE_NO_WINDOW,capture_output=True)
    if p.returncode not in (0,3):raise RuntimeError('Could not check whether the game is running.')
    return p.returncode==3

def check(root,log=print):
    root=pathlib.Path(root).resolve();m=read_json(BASE/'manifest.json')
    if not (root/'轮回之理.exe').is_file():raise RuntimeError('Select the folder containing 轮回之理.exe.')
    state_path=root/'.mobius-english/state.json'
    if state_path.exists():
        state=read_json(state_path)
        if state.get('status')=='installed':
            for rel,info in state['files'].items():
                if digest(safe_path(root,rel))!=info['english']:raise RuntimeError('Installed file changed: '+rel+'\nRestore using Steam verification before reapplying if another mod/update changed it.')
            log('English patch is installed; all patched file hashes match.');return 'installed'
        if state.get('status')=='prepared':raise RuntimeError('An interrupted installation was detected. Use Restore Chinese first.')
    for rel,expected in targets(m).items():
        if digest(safe_path(root,rel))!=expected:raise RuntimeError('Unsupported or modified game file: '+rel+'\nThis patch supports the build listed in README. No files were changed.')
    log('Supported original game build verified.');return 'original'

def build_bundle(source,destination,mapping,manifest,log):
    import UnityPy
    artwork=load_replacements(BASE,manifest)
    log('Reading Unity bundle...')
    env=UnityPy.load(source.read_bytes());expected={};changed=set();text_count=0
    for path,obj in env.container.items():
        if obj.type.name!='TextAsset' or '/configs/' not in path or path.endswith('/contractus.json'):continue
        data=obj.read();s=data.m_Script
        def replace(match):
            nonlocal text_count
            try:value=json.loads(match.group())
            except ValueError:return match.group()
            if value not in mapping:return match.group()
            text_count+=1
            return json.dumps(mapping[value],ensure_ascii=False)
        new=re.sub(r'"(?:[^"\\]|\\.)*"',replace,s)
        if new!=s:
            data.m_Script=new;data.save();changed.add(obj.path_id);expected[obj.path_id]=('text',new)
    index={o.path_id:o for o in env.objects}
    for row in manifest['bundle']['ui_objects']:
        obj=index[row['id']];tree=obj.read_typetree();key=row['key']
        if tree.get(key)!=row['text']:raise RuntimeError('Unexpected UI text; bundle version mismatch.')
        tree[key]=mapping[row['text']]
        # Let longer English labels fit their existing UI rectangles.
        if 'm_FontData' in tree:
            font=tree['m_FontData'];font['m_BestFit']=True
            font['m_MinSize']=min(12,font.get('m_FontSize',24));font['m_MaxSize']=font.get('m_FontSize',24)
        obj.save_typetree(tree);changed.add(obj.path_id);expected[obj.path_id]=('ui',(key,tree[key]))
    if text_count<400:raise RuntimeError('Insufficient translated text matches in Unity bundle.')
    art_expected=apply_replacements(env,BASE,artwork,log)
    changed.update(art_expected)
    log('Writing translated Unity bundle...')
    destination.write_bytes(env.file.save(packer='lz4'))
    # Reload and verify every changed object and every untouched binary object.
    log('Verifying bundle text and unchanged assets...')
    verify=UnityPy.load(destination.read_bytes());out={o.path_id:o for o in verify.objects}
    if set(out)!=set(index):raise RuntimeError('Unity object inventory changed unexpectedly.')
    for ident,obj in index.items():
        other=out[ident]
        if ident not in changed:
            if obj.get_raw_data()!=other.get_raw_data():raise RuntimeError('An unrelated Unity object changed.')
        elif ident not in art_expected:
            kind,value=expected[ident]
            actual=other.read().m_Script if kind=='text' else other.read_typetree()[value[0]]
            if actual!=(value if kind=='text' else value[1]):raise RuntimeError('Translated Unity object failed verification.')
    verify_replacements(out,art_expected)
    log(f'Bundle verified: {text_count} text occurrences, {len(manifest["bundle"]["ui_objects"])} UI objects, {len(art_expected)} artwork replacements; other objects unchanged.')

def restore(root,log=print):
    root=pathlib.Path(root).resolve()
    if game_running():raise RuntimeError('Close Mobius Theory before restoring.')
    backup=root/'.mobius-english';statepath=backup/'state.json'
    if not statepath.is_file():raise RuntimeError('No patch backup was found in this game folder.')
    state=read_json(statepath)
    # Validate the complete restore before writing anything.
    for rel,info in state['files'].items():
        saved=safe_path(backup/'original',rel);target=safe_path(root,rel)
        if not saved.is_file() or digest(saved)!=info['original']:raise RuntimeError('Missing or damaged backup: '+rel)
        if digest(target) not in (info['original'],info['english']):raise RuntimeError('File changed after patching: '+rel+'\nRestore refused to overwrite an update or another mod.')
    for rel in state['files']:
        target=safe_path(root,rel);temp=target.with_name(target.name+'.mobius-restore.tmp')
        shutil.copy2(safe_path(backup/'original',rel),temp);os.replace(temp,target)
        log('Restored '+rel)
    state['status']='restored';atomic_json(statepath,state)
    log('Original Chinese files restored. Backups retained. Save files were not touched.')

def install(root,log=print):
    root=pathlib.Path(root).resolve()
    if game_running():raise RuntimeError('Close Mobius Theory before installing.')
    if check(root,log)=='installed':
        state=read_json(root/'.mobius-english/state.json')
        if state.get('payload_id')!=payload_id(BASE):raise RuntimeError('Another patch revision is installed. Restore Chinese, then install this revision.')
        return
    if shutil.disk_usage(root).free<1500*1024*1024:raise RuntimeError('At least 1.5 GB free space is needed to stage and back up the patch.')
    manifest=read_json(BASE/'manifest.json')
    if digest(BASE/'translations.json')!=manifest['translations_sha256']:raise RuntimeError('Translation data hash mismatch.')
    mapping=read_json(BASE/'translations.json');backup=root/'.mobius-english'
    backup.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stage-',dir=backup) as stage_dir:
        stage=pathlib.Path(stage_dir);prepared={}
        for rel,original in targets(manifest).items():
            dest=safe_path(stage,rel);dest.parent.mkdir(parents=True,exist_ok=True)
            source=safe_path(root,rel)
            if rel==manifest['bundle']['path']:build_bundle(source,dest,mapping,manifest,log)
            elif rel==manifest['managed']['path']:
                log('Translating dynamic menu text...')
                result=subprocess.run([str(BASE/'TextPatch.exe'),str(source),str(dest),str(BASE/'translations.json')],capture_output=True,creationflags=CREATE_NO_WINDOW)
                if result.returncode:raise RuntimeError('Text helper failed: '+result.stderr.decode('utf-8',errors='replace'))
                log(result.stdout.decode('utf-8',errors='replace').strip())
            else:
                name=pathlib.Path(rel).name;payload=BASE/'subtitles'/name
                if digest(payload)!=manifest['subtitles'][name]['english_sha256']:raise RuntimeError('Subtitle data hash mismatch: '+name)
                shutil.copyfile(payload,dest)
            prepared[rel]={'original':original,'english':digest(dest)}
        log('All replacements built. Backing up originals...')
        for rel,info in prepared.items():
            source=safe_path(root,rel)
            if digest(source)!=info['original']:raise RuntimeError('Source changed during patch preparation: '+rel)
            saved=safe_path(backup/'original',rel);saved.parent.mkdir(parents=True,exist_ok=True)
            if saved.exists():
                if digest(saved)!=info['original']:raise RuntimeError('Existing backup does not match the original build.')
            else:shutil.copy2(source,saved)
            if digest(saved)!=info['original']:raise RuntimeError('Backup verification failed.')
        state={'version':manifest['version'],'status':'prepared','payload_id':payload_id(BASE),'files':prepared};atomic_json(backup/'state.json',state)
        try:
            for rel,info in prepared.items():
                os.replace(safe_path(stage,rel),safe_path(root,rel))
                if digest(safe_path(root,rel))!=info['english']:raise RuntimeError('Installed file verification failed: '+rel)
            state['status']='installed';atomic_json(backup/'state.json',state)
        except Exception:
            log('Installation failed. Restoring original files...');restore(root,log);raise
    log('English installed. Launch the game normally through Steam. Enable subtitles in Settings if needed.')

def find_game():
    candidates=[BASE,BASE.parent]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam') as key:steam=pathlib.Path(winreg.QueryValueEx(key,'SteamPath')[0])
        libraries=[steam];vdf=steam/'steamapps/libraryfolders.vdf'
        if vdf.exists():libraries += [pathlib.Path(x.replace('\\\\','\\')) for x in re.findall(r'"path"\s+"([^"]+)"',vdf.read_text(encoding='utf-8'))]
        for lib in libraries:
            app=lib/'steamapps/appmanifest_1925830.acf'
            if app.exists():
                match=re.search(r'"installdir"\s+"([^"]+)"',app.read_text(encoding='utf-8'))
                if match:candidates.append(lib/'steamapps/common'/match[1])
    except (OSError,ImportError):pass
    return str(next((p for p in candidates if (p/'轮回之理.exe').exists()),''))

def gui():
    import tkinter as tk
    from tkinter import ttk,filedialog,messagebox
    version=read_json(BASE/'manifest.json')['version']
    win=tk.Tk();win.title(f'Mobius Theory — English Test Patch {version}');win.geometry('780x520');win.minsize(680,440)
    frame=ttk.Frame(win,padding=18);frame.pack(fill='both',expand=True)
    ttk.Label(frame,text='MOBIUS THEORY — English Test Patch',font=('Segoe UI',17,'bold')).pack(anchor='w')
    ttk.Label(frame,text='English subtitles, choices, story text and text-based menus.\nChinese artwork and some puzzle images remain. Close the game first.',wraplength=720).pack(anchor='w',pady=(8,16))
    ttk.Label(frame,text='Steam game installation folder:').pack(anchor='w')
    row=ttk.Frame(frame);row.pack(fill='x',pady=5);path=tk.StringVar(value=find_game())
    ttk.Entry(row,textvariable=path).pack(side='left',fill='x',expand=True)
    ttk.Button(row,text='Browse...',command=lambda:path.set(filedialog.askdirectory() or path.get())).pack(side='left',padx=(8,0))
    buttons=ttk.Frame(frame);buttons.pack(fill='x',pady=12);messages=queue.Queue();busy=[False]
    console=tk.Text(frame,height=15,wrap='word',font=('Consolas',10),state='disabled');console.pack(fill='both',expand=True)
    def log(s):messages.put(str(s))
    def run(action):
        if busy[0]:return
        selected=path.get().strip()
        if not selected:messagebox.showerror('Select game folder','Select the Steam game installation folder.');return
        busy[0]=True
        for b in controls:b.state(['disabled'])
        def worker():
            try:action(selected,log)
            except Exception as e:log('ERROR: '+str(e))
            finally:messages.put(None)
        threading.Thread(target=worker,daemon=True).start()
    controls=[]
    for label,action in [('Check Installation',check),('Install English',install),('Restore Chinese',restore)]:
        b=ttk.Button(buttons,text=label,command=lambda a=action:run(a));b.pack(side='left',padx=(0,10));controls.append(b)
    def poll():
        try:
            while True:
                item=messages.get_nowait()
                if item is None:
                    busy[0]=False
                    for b in controls:b.state(['!disabled'])
                else:
                    console.configure(state='normal');console.insert('end',item+'\n');console.see('end');console.configure(state='disabled')
        except queue.Empty:pass
        win.after(150,poll)
    def close():
        if busy[0]:messagebox.showinfo('Patch in progress','Please wait for the current operation to finish.');return
        win.destroy()
    win.protocol('WM_DELETE_WINDOW',close);poll();win.mainloop()

if __name__=='__main__':
    # Windows console code pages may not support the Chinese installation path.
    for stream in (sys.stdout,sys.stderr):
        if stream is not None and hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8',errors='replace')
    parser=argparse.ArgumentParser();parser.add_argument('--game');parser.add_argument('--action',choices=['check','install','restore'])
    args=parser.parse_args()
    if args.action:
        try:globals()[args.action](args.game or find_game())
        except Exception as e:print('ERROR:',e);sys.exit(1)
    else:gui()
