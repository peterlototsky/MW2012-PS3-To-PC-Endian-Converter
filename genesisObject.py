from GenesisEnum import GenEnum


def changeEndianness(file_data : bytes, Gentype : GenEnum):
    genObjBytes = int.from_bytes(file_data[8:12], byteorder='big')

    try:
        if genObjBytes == 0xBEC01CB6:
            output_data = flipBytes_BEC01CB6(file_data)
        elif genObjBytes == 0xD66B170C:
            output_data = flipBytes_D66B170C(file_data)
        else:
            return "Not Implemented"
        return output_data
    except Exception as e:
        return e


# 0xBEC01CB6
def flipBytes_BEC01CB6(file_data : bytes, word_size : int = 4):
    number_offsets = int((file_data[28] << 8) | file_data[29])
    offsets = []
    length_file = len(file_data)

    '''
    1. Calculate Offsets
    2. Flip linker chunk
    3. Flip all chunks at offsets
    4. Flip first 20 Bytes
    5. Flip number of offsets word
    '''

    #1
    for i in range(number_offsets, -1, -1):
        word = (file_data[length_file - 6 - (16 * i)] << 8) | file_data[length_file - 5 - (16 * i)]
        #print(f'{word:04X}')
        offsets.append(word)

    output_data = bytearray(file_data)

    #2
    for i in range(number_offsets, -1, -1):
        output_data[length_file - 16 - (16 * i):length_file - 8 - (16 * i)] = output_data[length_file - 16 - (16 * i):length_file - 8 - (16 * i)][::-1]
        output_data[length_file - 8 - (16 * i):length_file - 4 - (16 * i)] = output_data[length_file - 8 - (16 * i):length_file - 4 - (16 * i)][::-1]
    
    #3
    offsets.append(length_file - ((number_offsets + 1) * word_size * word_size))
    for i in range(1, len(offsets) - 1):
        current_offset = int(offsets[i])
        byte_length = int(offsets[i + 1]) - int(offsets[i])

        for j in range(0, byte_length, word_size):
            output_data[current_offset + j: current_offset + j + word_size] = output_data[current_offset + j: current_offset + j + word_size][::-1] 

    #4
    for i in range(0, offsets[1] - word_size, word_size):
        output_data[i: i + word_size] = output_data[i: i + word_size][::-1]

    #5
    output_data[offsets[1] - word_size: offsets[1] - int(word_size / 2)] = output_data[offsets[1] - word_size: offsets[1] - int(word_size / 2)][::-1]

    return bytes(output_data)


# 0xD66B170C
def flipBytes_D66B170C(file_data : bytes, word_size : int = 4):
    files_offset = int((file_data[12] << 24) | (file_data[13] << 16) | (file_data[14] << 8) | (file_data[15]))
    number_files = int((file_data[20] << 8) | file_data[21])
    length_file = len(file_data)

    '''
    1. Flip Endianness of File Names
    2. Flip First 18 bytes
    3. Flip Number of Files
    4. Flip Arrays at EOF
    '''

    output_data = bytearray(file_data)

    # 1
    for i in range(files_offset, files_offset + (number_files * word_size), word_size):
        output_data[i: i + word_size] = output_data[i: i + word_size][::-1]

    # 2
    for i in range(0, files_offset - word_size, word_size):
        output_data[i: i + word_size] = output_data[i: i + word_size][::-1]

    # 3
    output_data[files_offset - word_size: files_offset - int(word_size / 2)] = output_data[files_offset - word_size: files_offset - int(word_size / 2)][::-1]

    # 4
    output_data[length_file - 16:length_file - 8] = output_data[length_file - 16:length_file - 8][::-1]
    output_data[length_file - 8:length_file - 4] = output_data[length_file - 8:length_file - 4][::-1]

    return bytes(output_data)

