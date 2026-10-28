using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using Mono.Cecil;
using Mono.Cecil.Cil;

class TextPatch {
    static IEnumerable<TypeDefinition> AllTypes(IEnumerable<TypeDefinition> types) {
        foreach(var t in types) { yield return t; foreach(var n in AllTypes(t.NestedTypes)) yield return n; }
    }
    static int Main(string[] args) {
        try {
            if(args.Length==1 && args[0]=="--running")
                return System.Diagnostics.Process.GetProcessesByName("轮回之理").Length>0 ? 3 : 0;
            if(args.Length!=3) throw new Exception("Usage: TextPatch input.dll output.dll translations.json");
            var serializer=new JavaScriptSerializer(); serializer.MaxJsonLength=10000000;
            var map=serializer.Deserialize<Dictionary<string,string>>(File.ReadAllText(args[2],Encoding.UTF8));
            var resolver=new DefaultAssemblyResolver(); resolver.AddSearchDirectory(Path.GetDirectoryName(Path.GetFullPath(args[0])));
            using(var asm=AssemblyDefinition.ReadAssembly(args[0],new ReaderParameters { AssemblyResolver=resolver, ReadSymbols=false })) {
                int count=0;
                foreach(var t in AllTypes(asm.MainModule.Types)) foreach(var m in t.Methods) {
                    if(!m.HasBody) continue;
                    foreach(var i in m.Body.Instructions) if(i.OpCode==OpCodes.Ldstr) {
                        string replacement;
                        if(map.TryGetValue((string)i.Operand,out replacement)) {i.Operand=replacement; count++;}
                    }
                }
                if(count<30) throw new Exception("Too few matching text literals; unsupported game build.");
                asm.Write(args[1]);
                Console.WriteLine("Translated "+count+" text literals.");
            }
            return 0;
        } catch(Exception e) {Console.Error.WriteLine(e.ToString());return 1;}
    }
}
