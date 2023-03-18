from enum import Enum, EnumMeta

class MetaStrEnum(EnumMeta):
    def __contains__(cls, item):
        if isinstance(item, str):
            return item in cls._value2member_map_
        else:
            cls.__members__
            return item in cls.__members__.values()

class BaseStrEnum(Enum, metaclass=MetaStrEnum):

    @classmethod
    def get_all_values(cls):
        return list(cls.__members__.values())
