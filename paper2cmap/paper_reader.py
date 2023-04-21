from __future__ import annotations

import json
import re
from typing import List

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from PyPDF2 import PdfReader

from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)

from paper2cmap import logger


class PaperReader():
    def __init__(self, chatbot: ChatOpenAI | AzureChatOpenAI) -> None:
        self.chatbot = chatbot

        self.title_max_len = 50
        self.title_min_len = 5

        # Acknowledge to https://github.com/talkingwallace/ChatGPT-Paper-Reader for sharing the prompt
        self.system_prompt_for_catelogue = """
You are a researcher helper bot. Now I will give several texts and you help me to find out which of them are the section titles of a research paper.
You must return me in this json format:
{
    "titles": ["section title text", "section title text", ...]
}
If the title has a number, the number MUST be retained!!!!
        """

    def _extract_candidate_catelogue(self, paper_path: str) -> List[str]:
        cand_cate = []
        for page_layout in extract_pages(paper_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    title = element.get_text()
                    if len(title) <= self.title_max_len and len(title) > self.title_min_len:
                        cand_cate.append(title)

        logger.debug(f"[PaperReader] Extracted candidate catelogue: {cand_cate}")
        return cand_cate

    def _extract_catelogue_with_LLM(self, cand_cate: List[str]) -> List[str]:
        messages = [
            SystemMessage(content=self.system_prompt_for_catelogue),
            HumanMessage(content=f"These are the texts: {cand_cate}")
        ]
        response = self.chatbot(messages).content
        logger.debug(f"[PaperReader] Raw response from LLM: {response}")

        return json.loads(response)["titles"]

    def _extract_catelogue(self, paper_path: str) -> List[str]:
        cand_cate = self._extract_candidate_catelogue(paper_path)
        return self._extract_catelogue_with_LLM(cand_cate)

    def _split_text_by_catelogue(self, full_text: str, catelogue: List[str]) -> List[str]:

        def _find_all(text: str, token: str) -> List[int]:
            pattern = re.compile(re.escape(token))
            positions = [m.start() for m in re.finditer(pattern, text)]
            return positions

        split_pos_list = []
        for title in catelogue:
            split_pos_list.extend(_find_all(full_text, title))
        split_pos_list = sorted(split_pos_list)
        logger.debug(f"[PaperReader] Text split positions: {split_pos_list}")
        
        sections = []
        for i in range(len(split_pos_list) - 1):
            sections.append(full_text[split_pos_list[i]:split_pos_list[i+1]].strip())
        sections.append(full_text[split_pos_list[-1]:].strip())

        return sections

    def load(self, paper_path: str) -> None:
        """
        Load the paper and extract the catelogue and sections
        """
        self.paper = PdfReader(paper_path)
        self.full_text = ""
        for page in self.paper.pages:
            self.full_text += page.extract_text()
        logger.info(f"[PaperReader] Full Text Size: {len(self.full_text)}")

        self.catelogue = self._extract_catelogue(paper_path)
        logger.info(f"[PaperReader] Catelogue: {self.catelogue}")

        self.sections = self._split_text_by_catelogue(self.full_text, self.catelogue)
        logger.info(f"[PaperReader] Sections Count: {len(self.sections)}")