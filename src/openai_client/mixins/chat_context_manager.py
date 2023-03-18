from ..enums import ROLE
from typing import List, Dict, Union

class Chat_Context_Manager_Mixin():
    """ Manages OpenAI Chat Context
    
    More specifically, this acts as a cache of dialogue for a Python client 
    interacting with the AI
    """

    # Maximum "memory" of requests to the AI and responses
    # 0 means store nothing, -1 means store everything
    _max_stored_statements = -1

    # Permanent context the AI should always be reminded of, like "You are a helpful assistant"
    _directives:List[Dict] = []

    # "Ephemeral" statmenets the AI should be reminded of. The AI is reminded of all statments
    # Things like "{"role": "user", "content": "Who won the world series in 2020?"}"
    # if _max_stored_statements is -1 and none if it is 0
    _statements:List[Dict] = []

    def __init__(self, max_stored_statements:int=-1, directives:List[str]=None, statements:List[Dict]=None):
        self._max_stored_statements = max_stored_statements

        # Store permanent system context
        self._format_directives(directives)

        # Store initial user and assistant statments if passed
        self._statements = statements or []


    def _format_directives(self, directives:List[str]):
        """ Take a list of directives and format them in dict form """

        if directives:
            [self.add_directive(directive) for directive in directives]


    def _check_role(self, role:ROLE) -> bool:
        """ Check if a passed role is valid """

        if not role in ROLE:
            raise ValueError(f"Role [{role}] does not exist for {self.__class__}. Valid roles are: {ROLE.get_all_values()}")
        

    def add_directive(self, content:str):
        """ Add a directive to the directive list """

        self._directives.append({"role": ROLE.SYSTEM.value, "content": content})


    def add_statement(self, role:ROLE, content:str):
        """ Add a statment to the statement list. Evict oldest statement if the list if full """

        # If there are more than 0 context entries to store
        if self._max_stored_statements:
            # Ensure the prompt is valid
            self._check_role(role)

            # If the context is full, remove oldest context
            if len(self._statements) == self._max_stored_statements:
                del self._statements[0]

            # Store latest context
            self._statements.append({"role": role.value, "content": content})
        

    def get_statmenets(self, idx:int=None):
        """ Get all statements or an statement from context by index """

        return self._statements if not idx else self._statements[idx]
    
    def get_directives(self, idx:int=None):
        """ Get all directives or an item from directives by index """

        return self._directives if not idx else self._directives[idx]
    
    def get_context(self, idx:int=None):
        """ Get a combination of directives and statements to feed to the AI """

        context = self.get_directives() + self.get_statmenets()

        if not idx:
            return context
        
        return context[idx]
    
    def __getitem__(self, to_get:Union[int, slice]):
        if isinstance(to_get, slice):
            return self.get_context()[to_get.start:to_get.stop:to_get.step]
        else:
            return self.get_context()[to_get]
