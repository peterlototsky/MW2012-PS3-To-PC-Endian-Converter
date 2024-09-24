def changeEndianness(file_data : bytes):
    number_offsets = int((file_data[2] << 8) | file_data[3])
    
    try:
        offsets = calculateAllOffsets(file_data, number_offsets)
        number_offsets = number_offsets + 1
    
        output_data = flipBytes(file_data, number_offsets, offsets)

        return output_data
    
    except Exception as e:
        return e



def calculateAllOffsets(file_data : bytes, number_offsets : int) -> list:
    offsets = []
    length_file = len(file_data)

    for i in range(number_offsets, -1, -1):
        word = (file_data[length_file - 6 - (16 * i)] << 8) | file_data[length_file - 5 - (16 * i)]
        # print(f'{word:04X}')
        offsets.append(word)

    string_offset = (file_data[offsets[1] - 2] << 8 | file_data[offsets[1] - 1])
    offsets.append(string_offset)
    return offsets


def flipBytes(file_data : bytes, number_offsets : int, offsets, word_size : int = 4) -> bytes:
    output_data = bytearray(file_data)
    length_file = len(file_data)

    '''
    1. Flip all chunks at offsets
    2. Flip linker chunk
    3. Flip number of offsets word
    4. Flip string offset
    '''

    # 1
    for i in range(0, number_offsets):
        current_offset = int(offsets[i])
        byte_length = int(offsets[i + 1]) - int(offsets[i]) - 4
        if i == 0:
            byte_length = byte_length - 4

        for j in range(0, byte_length, word_size):
            output_data[current_offset + j: current_offset + j + 4] = output_data[current_offset + j: current_offset + j + 4][::-1] 

        if i == 0:
            output_data[current_offset + byte_length + 4: current_offset + byte_length + 8] = output_data[current_offset + byte_length + 4: current_offset + byte_length + 8][::-1]
        else: 
            output_data[current_offset + byte_length: current_offset + byte_length + 2] = output_data[current_offset + byte_length: current_offset + byte_length + 2][::-1] 

    # 2
    for i in range(number_offsets - 1, -1, -1):
        output_data[length_file - 16 - (16 * i):length_file - 8 - (16 * i)] = output_data[length_file - 16 - (16 * i):length_file - 8 - (16 * i)][::-1]
        output_data[length_file - 8 - (16 * i):length_file - 4 - (16 * i)] = output_data[length_file - 8 - (16 * i):length_file - 4 - (16 * i)][::-1]

    # 3 
    output_data[2: 4] = output_data[2: 4][::-1] 

    # 4
    string_offset = offsets[len(offsets) - 1]
    output_data[string_offset:string_offset + word_size] = output_data[string_offset:string_offset + word_size][::-1]


    return bytes(output_data)