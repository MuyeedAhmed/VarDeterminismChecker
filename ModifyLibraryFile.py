import os
import ast
import shutil
import pandas as pd
import csv

class ModifyLibraryFile:
    def __init__(self, FilePath):
        self.FilePath = FilePath
        self.OriginalCodeTemporaryPath = self.FilePath[:-3]+"_Original.py"
        self.OutputFilePath = self.FilePath[:-3]+"_Output.py"
        
        self.VariableDF = pd.DataFrame()
        
        if not os.path.exists("VariableValues/"):
            os.makedirs("VariableValues")
        if not os.path.exists("TraceOutput/"):
            os.makedirs("TraceOutput")
            
    def reset(self):
        os.remove(self.FilePath)
        os.rename(self.OriginalCodeTemporaryPath, self.FilePath)
        os.system('rm -rf VariableValues/*')
        
    def init_decorator(self):
        '''
        First run: Add decorator to save variables
        '''
        self.NewFile.write("import pickle\n")
        self.NewFile.write("import os\n")
        self.NewFile.write("import numpy\n")
        
        self.NewFile.write("def record_variable():\n")
        self.NewFile.write("    def inner(f):\n")
        self.NewFile.write("        def init(*args, **kwargs):\n")
        self.NewFile.write("            if type(args[0]).__module__== '_thread' or type(args[0]).__module__ == 'threadpoolctl':\n")
        self.NewFile.write("                return\n")
        self.NewFile.write("            saveFileName = 'VariableValues/'+args[2]+'_'+args[1]+'_'+str(args[3])+'.pkl'\n")
        self.NewFile.write("            output = open(saveFileName, 'ab')\n")
        self.NewFile.write("            try:\n")
        self.NewFile.write("                pickle.dump(args[0], output)\n")
        self.NewFile.write("            except:\n")
        self.NewFile.write("                pass\n")
        self.NewFile.write("            output.close()\n")
        self.NewFile.write("        return init\n")
        self.NewFile.write("    return inner\n")
        self.NewFile.write("@record_variable()\n")
        self.NewFile.write("def _store_variable(v, vn, f, k):\n")
        self.NewFile.write("    pass\n")
             
        '''
        Second run: Compare variables with run1
        '''
        
        self.NewFile.write("def compare_to_previous(variable, variableName, functionName, lineCount):\n")
        self.NewFile.write("    if type(variable).__module__== '_thread' or type(variable).__module__ == 'threadpoolctl':\n")
        self.NewFile.write("        return\n")
        self.NewFile.write("    filePath = f'VariableValues/{functionName}_{variableName}_{lineCount}.pkl'\n")
        self.NewFile.write("    iterationFilePath = f'VariableValues/{functionName}_{variableName}_{lineCount}.txt'\n")
        self.NewFile.write("    sameValue = 1\n")
        self.NewFile.write("    if os.path.exists(filePath):\n")
        self.NewFile.write("        iteration = 1\n")
        self.NewFile.write("        if os.path.exists(iterationFilePath):\n")
        self.NewFile.write("            with open(iterationFilePath) as f:\n")
        self.NewFile.write("                line = f.readline().rstrip()\n")
        self.NewFile.write("                iteration = int(line)+1\n")
        self.NewFile.write("            iterationFile = open(iterationFilePath, 'w')\n")
        self.NewFile.write("            iterationFile.write(str(iteration))\n")
        self.NewFile.write("            iterationFile.close()\n")
        self.NewFile.write("        else:\n")
        self.NewFile.write("            iterationFile = open(iterationFilePath, 'w')\n")
        self.NewFile.write("            iterationFile.write('1')\n")
        self.NewFile.write("            iterationFile.close()\n")
        self.NewFile.write("        with open(filePath, 'rb') as f:\n")
        self.NewFile.write("            for i in range(iteration):\n")
        self.NewFile.write("                try:\n")
        self.NewFile.write("                    _old_variable = pickle.load(f)\n")
        self.NewFile.write("                except EOFError:\n")
        # self.NewFile.write("                    print(f'During Run 1, variable {variableName} in line {lineCount} changed {iteration-1} times. But in Run 2 it changed more than that')\n")    
        self.NewFile.write("                    break\n")
        self.NewFile.write("        if type(variable) is not numpy.ndarray:\n")
        self.NewFile.write("            if type(variable) is tuple:\n")
        self.NewFile.write("                try:\n")
        self.NewFile.write("                    for e1, e2 in zip(_old_variable, variable):\n")
        self.NewFile.write("                        if not e1 != e2:\n")
        self.NewFile.write("                            sameValue = 0\n")
        # self.NewFile.write("                            print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("                            break\n")
        self.NewFile.write("                except:\n")
        self.NewFile.write("                    pass\n")
        self.NewFile.write("            elif isinstance(variable, dict):\n")
        self.NewFile.write("                try:\n")
        self.NewFile.write("                    if _old_variable != variable:\n")
        self.NewFile.write("                        sameValue = 0\n")
        # self.NewFile.write("                        print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("                except:\n")
        self.NewFile.write("                    try:\n")
        self.NewFile.write("                        if recursive_dict_compare(_old_variable, variable) == False:\n")
        self.NewFile.write("                            sameValue = 0\n")
        # self.NewFile.write("                            print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("                    except:\n")
        self.NewFile.write("                        sameValue = 2\n")
        self.NewFile.write("                        print(f\"Failed to compare {variableName}, with type {type(variable)}\")\n")
        self.NewFile.write("                        print(\"I tried again and failed\")\n")
        self.NewFile.write("            else:\n")
        self.NewFile.write("                try:\n")
        self.NewFile.write("                    if _old_variable != variable:\n")
        self.NewFile.write("                        sameValue = 0\n")
        # self.NewFile.write("                        print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("                except:\n")
        self.NewFile.write("                    print(type(variable))\n")
        self.NewFile.write("        else:\n")
        self.NewFile.write("            try:\n")
        self.NewFile.write("                if (_old_variable == variable).all() == False:\n")
        self.NewFile.write("                    sameValue = 0\n")
        # self.NewFile.write("                    print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("            except:\n")
        self.NewFile.write("                if _old_variable == variable == False:\n")
        self.NewFile.write("                    sameValue = 0\n")
        # self.NewFile.write("                    print(f'Difference at line {lineCount} and variable {variableName}')\n")
        self.NewFile.write("        trace = open('TraceOutput/Trace.csv', 'a')\n")
        self.NewFile.write("        trace.write(f\"{str(variableName)},{str(os.path.basename(__file__))},{str(os.path.abspath(__file__))},{str(lineCount)},{str(iteration)},{str(sameValue)}\\n\")\n")
        self.NewFile.write("        trace.close()\n")
        
        self.NewFile.write("def recursive_dict_compare(dict1, dict2):\n")
        self.NewFile.write("    for key in dict1.keys():\n")
        self.NewFile.write("        if isinstance(dict1[key], dict):\n")
        self.NewFile.write("            if not recursive_dict_compare(dict1[key], dict2[key]):\n")
        self.NewFile.write("                return False\n")
        self.NewFile.write("        elif isinstance(dict1[key], numpy.ndarray) and isinstance(dict2[key], numpy.ndarray):\n")
        self.NewFile.write("            if not numpy.array_equal(dict1[key], dict2[key]):\n")
        self.NewFile.write("                return False\n")
        self.NewFile.write("        else:\n")
        self.NewFile.write("            if dict1[key] != dict2[key]:\n")
        self.NewFile.write("                return False\n")
        self.NewFile.write("    return True\n")
                
        
    def add_decorator(self, spaces, functionName, variableName, lineCount):
        self.NewFile.write(f"#<SecondRun>{spaces}compare_to_previous({variableName}, '{variableName}', '{functionName}', {lineCount})\n") 
        self.NewFile.write(f"{spaces}_store_variable({variableName}, '{variableName}', '{functionName}', {lineCount}) #<FirstRun>\n")


    def GetVariableNamesAndLineNumber(self):
        var_dict = {'LineNumber': [], 'VariableName': [], 'StartLineNumber': []}
        # function_name = None
        for node in ast.walk(self.tree):
            # if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            #     function_name = node.name
            #     print("FuntionName: ", function_name)
                
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_dict['LineNumber'].append(node.end_lineno)
                        var_dict['VariableName'].append(target.id)
                        var_dict['StartLineNumber'].append(node.lineno)
                    elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'self':
                            s = f'self.{target.attr}'
                        else:
                            s = f'{target.value.id}.{target.attr}'
                        var_dict['LineNumber'].append(node.end_lineno)
                        var_dict['VariableName'].append(s)
                        var_dict['StartLineNumber'].append(node.lineno)
                    elif isinstance(target, ast.Subscript):
                        # e[:, it % convergence_iter] = E
                        if isinstance(target.value, ast.Name):
                            var_dict['LineNumber'].append(node.end_lineno)
                            var_dict['VariableName'].append(target.value.id)
                            var_dict['StartLineNumber'].append(node.lineno)
                        # S.flat[:: (n_samples + 1)] = preference
                        elif isinstance(target.value.value, ast.Name):
                            var_dict['LineNumber'].append(node.end_lineno)
                            var_dict['VariableName'].append(target.value.value.id)
                            var_dict['StartLineNumber'].append(node.lineno)
                    # a, b = 5, 7
                    else:
                        try:
                            variable_names = [target.id for target in node.targets[0].elts if isinstance(target, ast.Name)]
                            for v in variable_names:
                                var_dict['LineNumber'].append(node.end_lineno)
                                var_dict['VariableName'].append(v)
                                var_dict['StartLineNumber'].append(node.lineno)
                        except Exception as e:
                            print("Error in ", node.lineno, self.FilePath, "\nError:", e)
                            pass
            elif isinstance(node, ast.AugAssign):
                if isinstance(node.target, ast.Name):
                    var_dict['LineNumber'].append(node.end_lineno)
                    var_dict['VariableName'].append(node.target.id)
                    var_dict['StartLineNumber'].append(node.lineno)
            
            
        self.VariableDF = pd.DataFrame(var_dict)
        
    def CreateNewFileWithDecorator(self):
        self.GetVariableNamesAndLineNumber()
        
        self.init_decorator()
        
        '''Read Source File'''
        OrginalFile = open(self.OriginalCodeTemporaryPath, 'r')
        OrginalFileLines = OrginalFile.readlines()
        OFLines = iter(OrginalFileLines)
        lineCount = 0
        spaces = ''
        for line in OFLines:
            self.NewFile.write(line)
            lineCount+=1
            if self.VariableDF[self.VariableDF["StartLineNumber"] == lineCount].shape[0] > 0:
                num_spaces = len(line) - len(line.lstrip(' '))
                spaces = ' ' * num_spaces
            filtered_df = self.VariableDF[self.VariableDF["LineNumber"] == lineCount]
            if filtered_df.shape[0] > 0:
                # num_spaces = len(line) - len(line.lstrip(' '))
                # spaces = ' ' * num_spaces
                for index, row in filtered_df.iterrows():
                    self.add_decorator(spaces, "Global", row["VariableName"], row["LineNumber"])
                spaces = ''

                
    
    def fit(self):
        ''' Save Original Source Code '''
        if os.path.exists(self.OriginalCodeTemporaryPath) == 0:
            shutil.copy(self.FilePath, self.OriginalCodeTemporaryPath)
            
        '''Read File And Create Tree'''
        with open(self.FilePath, 'r') as file:
            self.code = file.read()
        self.tree = ast.parse(self.code)
        
        self.NewFile = open(self.OutputFilePath, 'w')
        
        self.CreateNewFileWithDecorator()
        
        os.remove(self.FilePath)
        os.rename(self.OutputFilePath, self.FilePath)

        # # Store LOC
        # loc = sum(1 for line in self.code.splitlines() if line.strip())
        # with open("/Users/muyeedahmed/Desktop/Gitcode/Trace_ND_Source/TraceND/LOC/loc.csv", mode='a', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
            
        #     if csv_file.tell() == 0:
        #         writer.writerow(['FilePath', 'LOC'])
            
        #     writer.writerow([self.FilePath, loc])
        

        
        
        