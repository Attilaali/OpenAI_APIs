# OpenAI API Python Client

A (very rough WIP) base Python 3.9+ client for OpenAI APIs and some concrete "stateful" clients for common operations like running a chatbot with context

## Overview

Right now this just provides a base client that allows a reusable way to do common things
(like loading the API key or backing-off/retrying on an APIError) plus some easy overrides (like which model to use) and some mixins for when state dependence is important.

Now this also includes some pre-built "recipe" clients:

- [ChatBot Client](https://github.com/Topazoo/OpenAI-Python-Client/blob/main/src/openai_client/clients/chatbot/client.py)
- [Image Generation Client ](https://github.com/Topazoo/OpenAI-Python-Client/blob/main/src/openai_client/clients/image_generation/clients/create_image.py)


## Example

All I've got in lieu of real docs for now :). Run a local chatbot to play Dungeons and Dragons from your command line:

1. Install this library as a PyPi package

```sh
pip install OpenAI-API-Python-Client
```

2. Export your OpenAI API key in your shell environment

```sh
export OPENAI_API_KEY=AKIAIOSFODNN7EXAMPLE
```

3. Use a recipe class to create apps!

### Chatbot Client

```python
# Import this library :)
from openai_client import Chat_Bot_Client

# Simple D&D chatbot app :)
if __name__ == "__main__":
    # API Key is read from OPENAI_API_KEY environmental variable
    client = Chat_Bot_Client()

    # Add a high level directives to guide the model
    client.add_directive("You are a Dungeons and Dragons Dungeon Master. Use the 5th edition of the Dungeons and Dragons Player Handbook, Dungeon Master Guide, and Monster Manual")
    client.add_directive("At the beginning of your chat with the user you will assist them in creating a character. This character will have a description and stats as outlined in the 5th edition of the Dungeons and Dragons Player Handbook.")
    client.add_directive("Let the user choose race and class before assigning a personality, stats, and starting inventory. Provide the user with a list of races and classes they can be. Tell the user they can ask for more details about a class or race")
    client.add_directive("Once you introduce the character, give the player the start of an adventure campaign and ask the player what they would like to do")
    client.add_directive("As outlined in the handbook, if a roll is necessary based on the situation, roll for the user")
    client.add_directive("Finish by asking the player what they'd like to do next")

    # Simple loop to run a chat session
    while True:
        # Send it to the chatbot and get the response
        response = client.run_prompt()
        # Print the response
        print("\n" + response + "\n")
        # Get question from the user
        client.get_user_input()
```

### Image Generation Client

```python
# Import this library :)
from openai_client import URL_Image_Client

# Simple animal mashup app :)
if __name__ == "__main__":
    # API Key is read from OPENAI_API_KEY
    client = URL_Image_Client()

    # Add a context to always include before the prompt that is sent to the API
    client.add_pre_prompt_context("Generate a hybrid animal using the following animals:")
    # Add a context to always include after the prompt that is sent to the API
    client.add_post_prompt_context("This rendering should be hyperrealistic. The background \
                                   should be a savannah during the daytime")

    # Prompt the user for input
    animals = input("Choose two animals to create a hybrid of:\n>>> ")

    # Send the request and get the image URL
    image_url = client.run_prompt(animals)

    # Get the image URL
    print(image_url)
```


4. Use Mixins and the base class to create new "stateful" clients on top of the base client. See the implementation of [Chat_Bot_Client](https://github.com/Topazoo/OpenAI-Python-Client/blob/main/src/openai_client/clients/chatbot/client.py) for an example

## Contributing

Contributions are welcome! Please not the following when contributing:

- Unittests must be added under the `tests/` directory for the PR to be approved. You can run unittests from the root project directory with the following command:

    ```sh
    python setup.py test
    ```

- PRs cannot be merged without all unittests passing (they will execute automatically)
- Merges to `main` will automatically create a new release on PyPi **[unless it is from a forked Repo](https://stackoverflow.com/questions/58737785/github-actions-empty-env-secrets)**
