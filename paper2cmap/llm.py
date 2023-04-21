import os

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI

from paper2cmap import logger


class LLMManager():
    def __init__(self,
                 model_name: str = "",
                 deployment_name: str = "",
                 deployment_version: str = "",
                 **kwargs
                 ) -> None:
        # Required Env Vars
        OPENAI_API_TYPE = os.environ["OPENAI_API_TYPE"]
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

        # Required for Azure
        if OPENAI_API_TYPE == "azure":
            OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]

        if OPENAI_API_TYPE == "azure":
            logger.info(f"Using Azure deployment {deployment_name} (version {deployment_version})")
            self._LLM = AzureChatOpenAI(
                openai_api_type=OPENAI_API_TYPE,
                openai_api_base=OPENAI_API_BASE,
                openai_api_key=OPENAI_API_KEY,
                deployment_name=deployment_name,
                openai_api_version=deployment_version,
                **kwargs
            )
        elif OPENAI_API_TYPE == "openai":
            logger.info(f"Using OpenAI model {model_name}")
            self._LLM = ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                model_name=model_name,
                **kwargs
            )
        else:
            raise ValueError(f"OPENAI_API_TYPE must be either 'azure' or 'openai', but got {OPENAI_API_TYPE}")

    @property
    def LLM(self) -> ChatOpenAI:
        return self._LLM