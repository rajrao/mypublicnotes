
def _getFiles(lsPath, files):
  dirPaths = dbutils.fs.ls(lsPath)
  subFolders = []
  for dirPath in dirPaths:
    if (dirPath.isDir() and dirPath != lsPath):
      subFolders.append(dirPath.path)
    else:
      splitPath = dirPath.path.split("/")
      files.append({"path": dirPath.path, "name": dirPath.name, "yyyy": splitPath[6], "mm": splitPath[7], "dd": splitPath[8]})
  for subFolder in subFolders:
    _getFiles(subFolder, files)

def getFiles(lsPath):    
  files = []
  _getFiles(filepath, files)
  return files
  
filepath = "abfss://raw@[REDACTED].dfs.core.windows.net/aaa/bbb/"

files = getFiles(filepath)
display(files)
