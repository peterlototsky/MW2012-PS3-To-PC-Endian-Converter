import Scripts.genesisObject as genesisObject
import Scripts.genesisType as genesisType

from Types.GenesisEnum import GenEnum
import Tools.fileManager as fileManager

def convert(file_path) -> tuple:

    file_data = fileManager.openFile(file_path)
    if isinstance(file_data, bytes):
        
        genType = determineType(file_data)
        
        if genType == GenEnum.UnknownType:
            return (True, f'Unknown Type for {file_path} : ({file_data[0:2].hex()}, {file_data[8:12].hex()})')
        elif genType == GenEnum.GenesisType:
            file_reversed = genesisType.changeEndianness(file_data)
        elif genType == GenEnum.GenesisObject:
            file_reversed = genesisObject.changeEndianness(file_data, genType)
        else:
            file_reversed = None
        
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
    

def determineType(file_data : bytes) -> GenEnum:
    genTypeBytes = int.from_bytes(file_data[0:2], byteorder='big') 
    genObjBytes = int.from_bytes(file_data[8:12], byteorder='big')

    if genTypeBytes in GenEnum.GenesisType.value:
        return GenEnum.GenesisType
    elif genObjBytes in GenEnum.GenesisObject.value:
        return GenEnum.GenesisObject
    else:
        return GenEnum.UnknownType