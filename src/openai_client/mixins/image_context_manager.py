from typing import List, Union

class Image_Context_Manager_Mixin():
    """ Manages OpenAI Image Context
    
        More specifically, this stores high level instructions to be passed to image
        generation endpoints
    """

    # Permanent context the AI should always be instructed with before a
    # passed prompt, like "draw the following character in anime style"
    _pre_prompt_context:List[str] = []

    # Permanent context the AI should always be instructed with after a
    # passed prompt, like "Ensure the style is dark and moody"
    _post_prompt_context:List[str] = []

    def __init__(self, pre_prompt_context:List[str] = None, post_prompt_context:List[str] = None):
        if pre_prompt_context:
            self._pre_prompt_context = pre_prompt_context
        
        if post_prompt_context:
            self._post_prompt_context = post_prompt_context


    def add_pre_prompt_context(self, context:str):
        """ Add pre-prompt context to the pre-prompt context list """

        self._pre_prompt_context.append(context)


    def add_post_prompt_context(self, context:str):
        """ Add post-prompt context to the post-prompt context list """

        self._post_prompt_context.append(context)
  

    def get_pre_prompt_context(self, idx:int=None) -> Union[List[str], str]:
        """ Get all pre-prompt context or pre-prompt context by index """

        return self._pre_prompt_context if not idx else self._pre_prompt_context[idx]
    

    def get_post_prompt_context(self, idx:int=None) -> Union[List[str], str]:
        """ Get all post-prompt context or post-prompt context by index """

        return self._post_prompt_context if not idx else self._post_prompt_context[idx]
    

    def get_prompt_with_context(self, prompt:str) -> List[str]:
        """ Get a combination of directives and statements to feed to the AI """

        context = self._pre_prompt_context + [prompt] + self._post_prompt_context

        return " ".join(context)
