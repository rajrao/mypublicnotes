
def _getFilesRecursive(lsPath, files):
  dirPaths = dbutils.fs.ls(lsPath)
  for dirPath in dirPaths:
    if (dirPath.isDir() and dirPath != lsPath):
      _getFilesRecursive(dirPath.path, files)
    else:
      splitPath = dirPath.path.split("/")
      files.append({"path": dirPath.path, "name": dirPath.name, "yyyy": splitPath[6], "mm": splitPath[7], "dd": splitPath[8]})
    

def getFilesRecursive(environment, system, entityname):    
  filepath = "abfss://raw@" + BIStorageAccountName + ".dfs.core.windows.net/" + environment + "/" + system + "/" + entityname + "/"
  files = []
  _getFilesRecursive(filepath, files)
  return files
  
filepath = "abfss://raw@[REDACTED].dfs.core.windows.net/aaa/bbb/"

files = getFiles(filepath)
display(files)
