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

from paper2cmap import logger


class CMapGPT():
    def __init__(self, chatbot: ChatOpenAI | AzureChatOpenAI) -> None:
        self._prompt_config = yaml.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/prompts.yaml'), "r"),
            Loader=yaml.FullLoader
            )
        self._preprocess_system_prompt = self._prompt_config["preprocess"]["system"]
        self._preprocess_user_prompt = self._prompt_config["preprocess"]["user"]
        self._generate_system_prompt = self._prompt_config["generate"]["system"]
        self._generate_user_prompt = self._prompt_config["generate"]["user"]
        self._merge_and_prune_system_prompt = self._prompt_config["merge_and_prune"]["system"]
        self._merge_and_prune_user_prompt = self._prompt_config["merge_and_prune"]["user"]

        self._preprocess_examples = json.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/preprocess_examples.json'), "r")
            )
        self._generate_examples = json.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/generate_examples.json'), "r")
            )
        self._merge_and_prune_examples = json.load(
            open(pkg_resources.resource_filename('paper2cmap', 'metas/merge_and_prune_examples.json'), "r")
            )

        self.preprocess_prompt = self._create_prompt(
            system_prompt=self._preprocess_system_prompt,
            user_prompt=self._preprocess_user_prompt,
            user_prompt_vars=["text"],
            examples=self._preprocess_examples
        )
        self.generate_prompt = self._create_prompt(
            system_prompt=self._generate_system_prompt,
            user_prompt=self._generate_user_prompt,
            user_prompt_vars=["text", "max_num_concepts", "max_num_relationships"],
            examples=self._generate_examples
        )
        self.merge_and_prune_prompt = self._create_prompt(
            system_prompt=self._merge_and_prune_system_prompt,
            user_prompt=self._merge_and_prune_user_prompt,
            user_prompt_vars=["cmap", "max_num_concepts", "max_num_relationships"],
            examples=self._merge_and_prune_examples
        )
        
        self.chatbot = chatbot

    def _create_prompt(self, 
                       system_prompt: str = "", system_prompt_vars: List[str] = [],
                       user_prompt: str = "", user_prompt_vars: List[str] = [], 
                       examples: List[Dict] = []) -> ChatPromptTemplate:
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=system_prompt,
                input_variables=system_prompt_vars,
                template_format="jinja2"
            )
        )

        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=user_prompt,
                input_variables=user_prompt_vars,
                template_format="jinja2"
            )
        )

        examples_message_prompts = []
        for example in examples:
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

    def preprocess(self, text: str) -> str:
        """
        Preprocess the given text to be ready for concept map generation.
        Currently we summarize the text into few simple sentences as preprocessing.

        :param text: str, the text input to the model.
        :return: str, the preprocessed text.
        """
        inputs = self.preprocess_prompt.format_prompt(text=text)
        logger.debug(f"[CMapGPT] Preprocess Prompt: {inputs.to_string()}")
        response = self.chatbot(inputs.to_messages()).content
        logger.debug(f"[CMapGPT] Preprocess Result: {response}")
        return response

    def generate(self, text: str, max_num_concepts: int = 10, max_num_relationships: int = 30) -> List[Dict]:
        """
        Generate a concept map from the given text.

        :param text: str, the text input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the generated concept map.
        """
        inputs = self.generate_prompt.format_prompt(
            text=text,
            max_num_concepts=max_num_concepts,
            max_num_relationships=max_num_relationships
        )
        logger.debug(f"[CMapGPT] Generate Prompt: {inputs.to_string()}")
        response = self.chatbot(inputs.to_messages()).content
        logger.debug(f"[CMapGPT] Generate Result: {response}")
        return json.loads(response)

    def merge_and_prune(self, cmap: List[Dict], max_num_concepts: int = 10, max_num_relationships: int = 30) -> List[Dict]:
        """
        Merge and prune the given concept map.

        :param cmap: List[Dict], the concept map to merge and prune.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the merged and pruned concept map.
        """
        inputs = self.merge_and_prune_prompt.format_prompt(
            cmap=json.dumps(cmap),
            max_num_concepts=max_num_concepts,
            max_num_relationships=max_num_relationships
        )
        logger.debug(f"[CMapGPT] Merge&Prune Prompt: {inputs.to_string()}")
        response = self.chatbot(inputs.to_messages()).content
        logger.debug(f"[CMapGPT] Merge&Prune Result: {response}")
        return json.loads(response)