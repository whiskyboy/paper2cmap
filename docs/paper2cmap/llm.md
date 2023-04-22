Module paper2cmap.llm
=====================

Classes
-------

`LLMManager(model_name: str = '', deployment_name: str = '', deployment_version: str = '', **kwargs)`
:   Manage the Large Language Model.
    
    :param model_name: The OpenAI model name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
    :param deployment_name: The Azure deployment name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
    :param deployment_version: The Azure deployment version. If not provided, it will be read from the environment variable OPENAI_MODEL_VERSION.

    ### Instance variables

    `LLM: langchain.chat_models.openai.ChatOpenAI`
    :