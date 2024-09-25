import threading

import Scripts.genesisObject as genesisObject
import Scripts.genesisType as genesisType

from Types.GenesisEnum import GenEnum
from Types.Colors import Colors
from UI.signals import guiSignals
import Tools.fileManager as fileManager


thread_name = 'Converter'

class conversionRunner:
    
    def __init__(self, gui_signals : guiSignals):
        self.gui_signals = gui_signals
        self.file_list = []
        self.is_running = False
        self.converter_thread = None


    def startConversion(self, file_list : list):
        self.setFileList(file_list)
        if not self.is_running:
            self.converter_thread = threading.Thread(target=self.converter, name=thread_name)
            self.converter_thread.start()

        '''
        files_converted = 0
        if self.files:
            for file in self.files:
                item = self.ui.listWidget.item(files_converted)
                output = conversionRunner.convert(file)
                if output[0]:
                    self.ui.textEdit.append(f'{output[1]}\n')
                else:
                    self.ui.textEdit.append(f'Wrote File {output[1]}\n')
                files_converted = files_converted + 1
        '''


    def converter(self):
        self.is_running = True
        
        files_converted = 0
        if self.file_list:
            for file_path in self.file_list:
                file_data = fileManager.openFile(file_path)
                if isinstance(file_data, bytes):

                    genType = self.determineType(file_data)

                    if genType == GenEnum.UnknownType:
                        file_reversed = f'Unknown Type for {file_path} : ({file_data[0:2].hex()}, {file_data[8:12].hex()})'
                    elif genType == GenEnum.GenesisType:
                        file_reversed = genesisType.changeEndianness(file_data)
                    elif genType == GenEnum.GenesisObject:
                        file_reversed = genesisObject.changeEndianness(file_data, genType)


                    if isinstance(file_reversed, bytes):
                        result = fileManager.saveFile(file_path, file_reversed)
                        if isinstance(result, str):
                            self.gui_signals.output_to_console.emit(f'Wrote file {result}')
                            self.gui_signals.update_row_color.emit(files_converted, Colors.Green.value)
                        else:
                            self.gui_signals.output_to_console.emit(f'{result}')
                            self.gui_signals.update_row_color.emit(files_converted, Colors.Red.value)
                    else:
                        self.gui_signals.output_to_console.emit(f'{file_reversed}')
                        self.gui_signals.update_row_color.emit(files_converted, Colors.Red.value)
                else:
                    self.gui_signals.output_to_console.emit(f'{file_data}')
                    self.gui_signals.update_row_color.emit(files_converted, Colors.Red.value)
                
                files_converted = files_converted + 1
                self.gui_signals.increment_progress_bar.emit(files_converted)
        
        self.is_running = False


    def determineType(self, file_data : bytes) -> GenEnum:
        genTypeBytes = int.from_bytes(file_data[0:2], byteorder='big') 
        genObjBytes = int.from_bytes(file_data[8:12], byteorder='big')

        if genTypeBytes in GenEnum.GenesisType.value:
            return GenEnum.GenesisType
        elif genObjBytes in GenEnum.GenesisObject.value:
            return GenEnum.GenesisObject
        else:
            return GenEnum.UnknownType
        

    def setFileList(self, file_list : list):
        self.file_list = file_list

