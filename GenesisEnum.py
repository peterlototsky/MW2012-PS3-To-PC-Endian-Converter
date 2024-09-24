from enum import Enum, auto


class GenEnum(Enum):
    GenesisType = {0x0207}
    GenesisObject = {0xBEC01CB6, 0xD66B170C}
    UnknownType = 0x0
    