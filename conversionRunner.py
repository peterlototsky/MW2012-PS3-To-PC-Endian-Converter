import fileManager
import genesisObject as genesisObject
import genesisType as genesisType

def convert(file_path):

    file_data = fileManager.openFile(file_path)

    

    if isinstance(file_data, bytes):
        file_reversed = genesisType.changeEndianness(file_data)
        if isinstance(file_reversed, bytes):
            result = fileManager.saveFile(file_path, file_reversed)
            if isinstance(result, str):
                return (False, result)
            else:
                return (True, result)
        else:
            return (True, file_reversed)
    else:
        return (True, file_data)
    

def determineType():
    pass