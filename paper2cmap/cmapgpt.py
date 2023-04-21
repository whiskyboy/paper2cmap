from __future__ import annotations

import json
from typing import Dict, List

import pkg_resources
import yaml

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseMessage

from paper2cmap import logger


class CMapGPT():
    def __init__(self, chatbot: ChatOpenAI | AzureChatOpenAI) -> None:
        self.prompt_config = yaml.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/prompts.yaml'), "r"),
            Loader=yaml.FullLoader
            )
        self.system_prompt = self.prompt_config["system_prompt"]
        self.user_prompt = self.prompt_config["user_prompt"]

        self.examples = json.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/examples.json'), "r")
            )

        self.cmap_prompt = self.create_cmap_prompt()
        
        self.chatbot = chatbot

    def create_cmap_prompt(self) -> ChatPromptTemplate:
        """
        Create the concept map prompt.

        :return: The concept map prompt.
        """
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=self.system_prompt,
                input_variables=[],
                template_format="jinja2"
            )
        )

        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=self.user_prompt,
                input_variables=["text_input", "cmap_input", "max_num_concepts", "max_num_relationships"],
                template_format="jinja2"
            )
        )

        examples_message_prompts = []
        for example in self.examples:
            role_message_prompt_template = AIMessagePromptTemplate if example["role"] == "assistant" else HumanMessagePromptTemplate
            examples_message_prompts.append(
                role_message_prompt_template(
                    prompt=PromptTemplate(
                        template=example["content"],
                        input_variables=[],
                        template_format="jinja2"
                    )
                )
            )

        return ChatPromptTemplate.from_messages([system_message_prompt, *examples_message_prompts, human_message_prompt])

    def format_cmap_prompt(self, text_input: str, cmap_input: List[Dict], 
                           max_num_concepts: int = 10, max_num_relationships: int = 30) -> List[BaseMessage]:
        """
        Format the concept map prompt.

        :param text_input: str, the text input to the model.
        :param cmap_input: List[Dict], a json that represents the concept map input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[BaseMessage], the formatted concept map prompt.
        """
        return self.cmap_prompt.format_prompt(
            text_input=text_input,
            cmap_input=cmap_input,
            max_num_concepts=max_num_concepts,
            max_num_relationships=max_num_relationships
        ).to_messages()

    def chat(self, text_input: str, cmap_input: List[Dict] = [],
             max_num_concepts: int = 10, max_num_relationships: int = 30) -> List[Dict]:
        """
        Chat with the model to generate a concept map.

        :param text_input: str, the text input to the model.
        :param cmap_input: List[Dict], a json that represents the concept map input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the generated concept map output.
        """
        inputs = self.format_cmap_prompt(text_input, cmap_input, max_num_concepts, max_num_relationships)
        logger.debug(f"[CMapGPT] Prompt: {inputs}")
        response = self.chatbot(inputs).content
        logger.debug(f"[CMapGPT] Result: {response}")
        return json.loads(response)