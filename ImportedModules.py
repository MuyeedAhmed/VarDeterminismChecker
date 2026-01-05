import ast
import re
from itertools import islice
import linecache
import os
import fnmatch


class ImportedModules:
    def __init__(self, FilePath):
        self.FilePath = FilePath
        self.Script = ""
        self.tree = ""
        self.ImportedModules_3rd = set()
        self.ImportedMethods_pkg = []
        self.LocalMethods = set()
    
    def ReadScript(self):
        with open(self.FilePath, "r") as file:
            self.Script = file.read()
    def CreateAST(self):
        self.tree = ast.parse(self.Script)
        
    def getImportedMethods(self):
        self.ReadScript()
        self.CreateAST()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    self.ImportedModules_3rd.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                lineNumber = node.lineno
                line = linecache.getline(self.FilePath, lineNumber).strip()            
                for name in node.names:
                    if node.module:
                        module_path = self.findImportPath(line, name.name)
                        if module_path == None:
                            continue
                        row = {"LineNo": lineNumber, "Line": line, "LineNo": lineNumber, 
                               "ModuleName": node.module, "MethodName": name.name, "Path": module_path}                    
                        self.ImportedMethods_pkg.append(row)
                    else:
                        self.ImportedModules_3rd.add(name.name)
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.LocalMethods.add(node.name)
        return self.ImportedMethods_pkg
        
    def remove_comments(self, output_file):
        pattern = r'#.*?$|\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"'
        content_without_comments = re.sub(pattern, '', self.Script, flags=re.MULTILINE | re.DOTALL)

        with open(output_file, 'w') as f:
            f.write(content_without_comments)
            
    def findImportPath(self, line, imported_classOrMethod_name):
        moduleStr = line.split('import')[0].split('from')[1].replace(" ", "")
        items = moduleStr.split('.')
        dots = items.count('')
        if dots == 0:
            return ""
        mods = len(items)-dots 
        mod_path = self.FilePath.split("/")
        mod_path = mod_path[:-1*dots] + items
            
        mod_path = "/"+os.path.join(*filter(None, mod_path))+".py"
    
        if os.path.exists(mod_path):
            return mod_path
        else:
            mod_folder = mod_path[:-3]
            for root, dirs, files in os.walk(mod_folder):
                for file in fnmatch.filter(files, '*.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if imported_classOrMethod_name in content:
                        t = ast.parse(content)
                        for node in ast.walk(t):
                            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                if node.name == imported_classOrMethod_name:
                                    mod_path = mod_folder+"/"+file
                                    return mod_path
            else:
                # print(imported_classOrMethod_name, "not found")
                return None
        

                
        