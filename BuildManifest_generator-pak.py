import os
import re

file_basepath = "D:/Unreal Projects/PatcherDemo/"
Pakfolder = "Windows/PatcherDemo/Content/Paks"
file_name = "BuildManifest.txt"

def Foo(inFilePath, inFileName):
    if not os.path.exists(inFilePath):
        print(f'Path does not exist: {inFilePath}')
        return
    
    if not os.path.exists(inFileName):
        print(f'Creating a new file...')
        # Creates a new file 
        open(file_name, 'w')

    # open file to read content
    f = open(inFileName, 'r')
    linelist = f.readlines()

    # open file to write
    f = open(inFileName, 'w')

    ### Write NUM_ENTRIES and BUILD_ID 
    count = 0

    for path in os.listdir(inFilePath):
        # check if current path is a file
        if os.path.isfile(os.path.join(inFilePath, path)):
            count += 1

    f.write(f"$NUM_ENTRIES = " + str(count) + "\n")
    f.write(f"$BUILD_ID = Patcher-Live\n")

    if len(linelist) > 0:
        linelist.pop(0)
        linelist.pop(0)
    #####

    ### Checking each files' properties
    for folder, subfolders, files in os.walk(inFilePath):
        
        # remove pakchunk0
        files.pop(0)

        count = 0
        for file in files:
    
            FullFilePath = os.path.join(folder, file)

            # get information from chunk generated 
            chunkID, size, version = GetInfo(file, count, FullFilePath)

            localLine = ""
            if len(linelist) > 0:

                localLine = linelist[count]

                # get information from chunk on previous BuildManifest file
                chunkIDSavedinFile, sizeSavedinFile, versionSavedinFile = GetInfoFromLine(localLine, count)

                # compare if a specific chunk has need to be updated
                if chunkID == chunkIDSavedinFile:
                    if size != sizeSavedinFile:
                        
                        # it needs to be updated
                        WriteNewLine(f, file, sizeSavedinFile, versionSavedinFile, chunkIDSavedinFile)

                        count +=1 
                        continue
            

            WriteNewLine(f, file, size, version, chunkID)
            count += 1
    #####

    f.close()

def WriteNewLine(f, file, size, version, chunkID):
    try:
        f.write(f'{file} {size} {version} {chunkID} {file}\n')
        print(f'{file} {size} {version} {chunkID} {file}')
    except Exception as e:
        print(f'Error while writing in the file: {e}')

def getVersion(localLine):
    
    localVersion = False
    a = localLine.split(' ')
    for item in a:
        if item.startswith("ver"):
            newVersion = int(re.search(r'\d+', item).group()) + 1
            newString = "{:03d}".format(newVersion)
            localVersion = "ver" + newString 

    if localVersion is False:
        localVersion = "ver001" 

    return localVersion

def getChunkId(localFile):
    return int(re.search(r'\d+', localFile).group())

def GetInfoFromLine(localLine, index):
    localChunkId = getChunkId(localLine)
    localFileSize = int(getFileSizeFromLine(localLine))
    localVersion = getVersion(localLine)

    return localChunkId, localFileSize, localVersion

def getFileSizeFromLine(localLine):
    a = localLine.split(' ')
    return a[1]

def GetInfo(file, index, fullFilePath):  
    localChunkId = getChunkId(file)
    localFileSize = int(getFileSize(fullFilePath))
    localVersion = getVersion(file)

    return localChunkId, localFileSize, localVersion

def getFileSize(fullFilePath):
    return os.path.getsize(fullFilePath)

# Call Function
Foo(file_basepath + Pakfolder, file_basepath + file_name)


print("Done!")
