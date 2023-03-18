from .base import BaseStrEnum

class ROLE(BaseStrEnum):
    """ Roles for chat completion """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
