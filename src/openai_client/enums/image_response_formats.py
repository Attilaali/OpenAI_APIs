from .base import BaseStrEnum

class IMAGE_RESPONSE_FORMAT(BaseStrEnum):
    """ Image response formats for DALLE """

    URL = "url"
    B64_JSON = "b64_json"
