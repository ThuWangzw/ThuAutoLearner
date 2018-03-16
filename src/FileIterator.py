import os
def fileinpath(path,filename):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(path+"/"+file):
            nfiles = os.listdir(path+'/'+file)
            for i,nfile in enumerate(nfiles):
                nfiles[i] = file + "/" + nfile
            files.extend(nfiles)
        else:
            if(filename in file):
                return True
    return False
