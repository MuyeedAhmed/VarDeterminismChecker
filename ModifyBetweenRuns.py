import sys
import os
import pandas as pd


from ImportedModules import ImportedModules
from ModifyLibraryFile import ModifyLibraryFile
from GetLibraryPath import ResolveSourcePath


def EditBeforeRun1(libFile):
    im = ImportedModules(FilePath=libFile)
    imported_modules = im.getImportedMethods()
    imported_modules = pd.DataFrame(imported_modules)
    imported_modules_path = list(set(imported_modules["Path"].to_numpy()))
    imported_modules_path.remove("")
    # print(imported_modules_path)
    mlf = ModifyLibraryFile(FilePath=libFile)
    mlf.fit()
    
    for p in imported_modules_path:
        # try:
        mlf = ModifyLibraryFile(FilePath=p)
        mlf.fit()
        # except:
        #     print("Error in", p)
            
def EditBeforeRun2(libFile):
    newFilePath = libFile[:-3]+'New.py'

    file1 = open(libFile, 'r')
    Lines = file1.readlines()
    
    newFile = open(newFilePath, 'w')

    for line in Lines:
        line = line.replace('#<SecondRun>', '')
        if '#<FirstRun>' not in line:
            newFile.write(line)
    os.remove(libFile)
    os.rename(newFilePath, libFile)
    
    im = ImportedModules(FilePath=libFile[:-3]+"_Original.py")
    imported_modules = im.getImportedMethods()
    imported_modules = pd.DataFrame(imported_modules)
    imported_modules_path = imported_modules["Path"].to_numpy().tolist()
    imported_modules_path = [s.replace("_Original","") for s in imported_modules_path]
    imported_modules_path = list(set(imported_modules_path))
    imported_modules_path.remove("")
    
    for p in imported_modules_path:
        newFilePath = p[:-3]+'New.py'

        file1 = open(p, 'r')
        Lines = file1.readlines()
        
        newFile = open(newFilePath, 'w')

        for line in Lines:
            line = line.replace('#<SecondRun>', '')
            if '#<FirstRun>' not in line:
                newFile.write(line)
        os.remove(p)
        os.rename(newFilePath, p)
    
    
def Reset(libFile, libFunc):
    mlf = ModifyLibraryFile(FilePath=libFile)
    mlf.reset()
    im = ImportedModules(FilePath=libFile)
    imported_modules = im.getImportedMethods()
    imported_modules = pd.DataFrame(imported_modules)
    imported_modules_path = imported_modules["Path"].to_numpy().tolist()
    imported_modules_path = [s.replace("_Original","") for s in imported_modules_path]
    imported_modules_path = list(set(imported_modules_path))
    imported_modules_path.remove("")
    
    for p in imported_modules_path:
        # try:
        mlf = ModifyLibraryFile(FilePath=p)
        mlf.reset()
        # except:
        #     print("Error in", p)
    traceFile = pd.read_csv("TraceOutput/Trace.csv", header=None)
    if traceFile.shape[0]>1:
        traceFile.columns = ["Variable","Filename","FilePath","LineNo","Iteration","Deterministic"]
        traceFile.to_csv(f"TraceOutput/Trace_{libFunc}.csv", index=False)
    os.remove("TraceOutput/Trace.csv")

if __name__ == "__main__":
    libFile = ""
    args = sys.argv
    libFunc = args[1]
    try:
        libFile = ResolveSourcePath(libFunc)
    except Exception as e:
        print("Error:", e)
        sys.exit()
    print("Modifying:", libFile)
    if args[2] == "R1":
        EditBeforeRun1(libFile)
    elif args[2] == "R2":
        EditBeforeRun2(libFile)
    elif args[2] == "Reset":
        Reset(libFile, libFunc)
    
        
    
    
    




