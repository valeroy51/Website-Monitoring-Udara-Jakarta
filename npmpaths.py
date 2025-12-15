import os
import shutil 

def getPathNPM():
    path = shutil.which("npm")

    if path and os.path.isfile(path):
        return path
    
    raise RuntimeError("tidak ketemu")

# print(getPathNPM())