using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using Mono.Cecil;
using Mono.Cecil.Cil;

class TextPatch {
    static void PatchEnglishWrap(ModuleDefinition module) {
        string helper=Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"EnglishWrap.dll");
        if(!File.Exists(helper)) throw new Exception("Missing EnglishWrap.dll patching helper.");
        var type=AllTypes(module.Types).Single(t=>t.Name=="GameThinkingHallUtility");
        var target=type.Methods.Single(m=>m.Name=="SetString" && m.Parameters.Count==2);
        using(var source=AssemblyDefinition.ReadAssembly(helper)) {
            var method=source.MainModule.Types.Single(t=>t.Name=="EnglishWrap").Methods.Single(m=>m.Name=="SetString");
            if(method.Body.ExceptionHandlers.Count!=0) throw new Exception("Unexpected formatter exception handlers.");
            var body=new MethodBody(target);body.InitLocals=method.Body.InitLocals;body.MaxStackSize=method.Body.MaxStackSize;
            var variables=new Dictionary<VariableDefinition,VariableDefinition>();
            foreach(var v in method.Body.Variables) {var copy=new VariableDefinition(module.ImportReference(v.VariableType));variables[v]=copy;body.Variables.Add(copy);}
            var instructions=new Dictionary<Instruction,Instruction>();
            foreach(var i in method.Body.Instructions) {var copy=Instruction.Create(OpCodes.Nop);copy.OpCode=i.OpCode;instructions[i]=copy;body.Instructions.Add(copy);}
            foreach(var i in method.Body.Instructions) {
                object value=i.Operand;
                if(value is Instruction)value=instructions[(Instruction)value];
                else if(value is Instruction[])value=((Instruction[])value).Select(x=>instructions[x]).ToArray();
                else if(value is VariableDefinition)value=variables[(VariableDefinition)value];
                else if(value is ParameterDefinition)value=target.Parameters[((ParameterDefinition)value).Index];
                else if(value is MethodReference)value=module.ImportReference((MethodReference)value);
                else if(value is TypeReference)value=module.ImportReference((TypeReference)value);
                else if(value is FieldReference)value=module.ImportReference((FieldReference)value);
                instructions[i].Operand=value;
            }
            target.Body=body;
            if(module.AssemblyReferences.Any(r=>r.Name=="EnglishWrap"))
                throw new Exception("Formatter unexpectedly depends on the patching helper at runtime.");
        }
    }
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
                PatchEnglishWrap(asm.MainModule);
                asm.Write(args[1]);
                Console.WriteLine("Translated "+count+" text literals.");
                Console.WriteLine("Patched English word wrapping in GameThinkingHallUtility.SetString.");
            }
            return 0;
        } catch(Exception e) {Console.Error.WriteLine(e.ToString());return 1;}
    }
}
