import sys
import os
import pandas as pd


from ImportedModules import ImportedModules
from ModifyLibraryFile import ModifyLibraryFile



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
    
    
def Reset(libFile):
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
    os.rename("TraceOutput/Trace.csv",  "TraceOutput/Trace_"+libFile.split("/")[-1].split(".")[0]+".csv")

if __name__ == "__main__":
    libFile = ""
    args = sys.argv
    if os.path.exists(args[1]):
        libFile = args[1]
    else:
        if args[1] == "AP":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/cluster/_affinity_propagation.py"
        elif args[1] == "SC":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/cluster/_spectral.py"
        elif args[1] == "KM":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/cluster/_kmeans.py"
        elif args[1] == "GM":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/mixture/_base.py"
        elif args[1] == "LogReg":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/linear_model/_logistic.py"
        elif args[1] == "DT":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/tree/_classes.py"
        elif args[1] == "IF":
            libFile = "/Users/muyeedahmed/Desktop/Gitcode/ForkedLibrary/scikit-learn/sklearn/ensemble/_iforest.py"
    if libFile == "":
        print("Invalid source code directory")
        sys.exit()
        
    if args[2] == "R1":
        EditBeforeRun1(libFile)
    elif args[2] == "R2":
        EditBeforeRun2(libFile)
    elif args[2] == "Reset":
        Reset(libFile)
    
        
    
    
    




