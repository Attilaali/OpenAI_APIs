import openai, os
from . import OpenAI_Client

# Typing
from typing import Union, List
from ..enums import IMAGE_SIZE, IMAGE_RESPONSE_FORMAT

class OpenAI_Image_Client(OpenAI_Client):
    """ Base client for interacting with OpenAI Image generation API """

    _api = openai.Image
    _size = IMAGE_SIZE.SIZE_1024x1024.value
    _response_format = IMAGE_RESPONSE_FORMAT.URL.value
    _number_of_images = 1

    def __init__(self, api_key: str = None, max_retries=3, ms_between_retries=500, default_size:IMAGE_SIZE = None, 
                 default_number_of_images:int=1, default_response_format:str=None) -> None:
        
        super().__init__(api_key, self._model, self._temperature, max_retries, ms_between_retries)

        # Read passed default image size
        self._size = self.check_size(default_size or os.environ.get('OPENAI_DEFAULT_IMAGE_SIZE', self._size))

        # Read passed default number of images to generate
        self._number_of_images = default_number_of_images or os.environ.get('OPENAI_DEFAULT_NUMBER_OF_IMAGES', self._number_of_images)

        # Read passed default image response format
        self._response_format = default_response_format or os.environ.get('OPENAI_DEFAULT_IMAGE_RESPONSE_FORMAT', self._response_format)

    
    def check_size(self, size:IMAGE_SIZE) -> IMAGE_SIZE:
        """ Check if a passed image size is valid. Raise a ValueError if not """

        if not size in IMAGE_SIZE:
            raise ValueError(f"Image size [{size}] does not exist for {self.__class__}. Valid roles are: {IMAGE_SIZE.get_all_values()}")
        
        return size
        

    def process_response(self, num_images:int, response:dict) -> Union[List[str], str]:
        """ Process the response received from the API. Basically, if there
            was more than one image generated return a list of URLs or b64 JSON for each
            image. 
        """

        if num_images == 1:
            return response['data'][0][self._response_format]
        
        else:
            return [result[self._response_format] for result in response['data']]


    def run_prompt(self, prompt:str, number_of_images:int=None, size:IMAGE_SIZE=None):
        """ Sends a prompt to OpenAPI to be generated by DALLE. You can specify the 
            number of images to generate and the dimensions of the image.
             
            If more than one image should be generated, this method will return a list of URLs 
            or b64 JSON for each image. 
        """

        # Allow the number_of_images to generate and image size to be specified per call, 
        # but fall back on defaults
        number_of_images = number_of_images or self._number_of_images
        size = self.check_size(size or self._size)

        result = self._api.create(prompt=prompt, n=number_of_images, size=size, response_format=self._response_format)

        return self.process_response(number_of_images, result)