import os


def openFolder(folder_location : str) -> list:
    dat_files = []
    for root, dirs, files in os.walk(folder_location):
           for file_name in files:
               if file_name.endswith('.dat'):
                   dat_files.append(os.path.join(root, file_name))
    return dat_files


def openFile(file_location : str) -> bytes:
    file_bytes = False

    try:
        with open(file_location, 'rb') as file_data:
            file_bytes = file_data.read()

    except Exception as e:
        print(f'{e}')
        return e
    
    return file_bytes


def saveFile(file_location : str, file_data : bytes):
    dir = os.path.join(os.getcwd(),'Output') 
    if not os.path.exists(dir):
        os.makedirs(dir)

    file_name = '_'.join(''.join(os.path.basename(file_location).split('.')[:-1]).split('_')[::-1]) + ".dat"
    file_name = os.path.join(dir, file_name)
    
    try:
        with open(file_name, 'wb') as reversed_file:
            reversed_file.write(file_data)
            print(f'Wrote file {file_name}')

    except Exception as e:
        print(f'{e}')
        return e

    return file_name


'''
if __name__ == "__main__":
    option_selected = 0
    file_location = ''
    while(1):
        option_selected = int(input("Select Option\n1. genesisType\n2. genesisObject\n9. Exit\n"))

        if option_selected == 1:
            file_location = input("Enter file path for genesisType: ")
            file_data = openFile(file_location)
            if file_data:
                file_reversed = genesisType.changeEndianness(file_data)
                saveFile(file_location, file_reversed)

        elif option_selected == 2:
            file_location = input("Enter file path for genesisObject: ")
            file_data = openFile(file_location)
            if file_data:
                file_reversed = genesisObject.changeEndianness(file_data)
                saveFile(file_location, file_data)

        elif option_selected == 9:
            print("Exiting...")
            break
'''