from __future__ import annotations

from typing import Dict, List
import colorlog

from paper2cmap import LLMManager, CMapGPT, PaperReader, logger


class Paper2CMap():
    def __init__(self,
                 model_name: str = "",
                 deployment_name: str = "",
                 deployment_version: str = "",
                 temperature: float = 0.7,
                 request_timeout: int = 60,
                 max_retries: int = 6,
                 max_tokens: int | None = None,
                 verbose: bool = False,
                 ) -> None:
        """
        Initialize the Paper2CMap class.

        :param model_name: The OpenAI model name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
        :param deployment_name: The Azure deployment name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
        :param deployment_version: The Azure deployment version. If not provided, it will be read from the environment variable OPENAI_MODEL_VERSION.
        :param temperature: The temperature of the model. Default: 0.7.
        :param request_timeout: The request timeout. Default: 60.
        :param max_retries: The maximum number of retries. Default: 6.
        :param max_tokens: The maximum number of tokens. Default: None.
        :param verbose: Whether to print debug logs. Default: False.
        """
        self.chatbot = LLMManager(
            model_name=model_name,
            deployment_name=deployment_name,
            deployment_version=deployment_version,
            temperature=temperature,
            request_timeout=request_timeout,
            max_retries=max_retries,
            max_tokens=max_tokens,
            verbose=verbose,
        ).LLM

        self.paper_reader = PaperReader(chatbot=self.chatbot)
        self.cmap_gpt = CMapGPT(chatbot=self.chatbot)

        self._loaded = False

        if verbose:
            logger.setLevel(colorlog.DEBUG)

    def load(self, pdf_path: str) -> None:
        """
        Load a PDF file.

        :param pdf_path: The path to the PDF file.
        """
        logger.info(f"[Paper2CMap] Loading PDF file: {pdf_path}")
        self.paper_reader.load(pdf_path)
        self._loaded = True

    def _generate_cmaps_by_section(self, max_num_concepts: int = 10, max_num_relationships: int = 30, 
                   max_num_iterations: int = -1) -> List[List[Dict]]:
        """
        Generate concept maps for each section separately.

        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections.
        :return: A list of concept maps.
        """
        cmap_list = []
        for i, section in enumerate(self.paper_reader.sections):
            if max_num_iterations != -1 and i >= max_num_iterations:
                break

            logger.info(f"[Paper2CMap] Generating concept map for section {i}")
            cmap = self.cmap_gpt.generate(
                text=section,
                max_num_concepts=max_num_concepts,
                max_num_relationships=max_num_relationships
                )
            logger.info(f"[Paper2CMap] Concept map for section {i}: {cmap}")
            
            cmap_list.append(cmap)

        return cmap_list
    
    def _merge_and_prune_cmaps(self, cmap_list: List[List[Dict]],
                               max_num_concepts: int = 10, max_num_relationships: int = 30) -> List[Dict]:
        """
        Merge and prune a list of concept maps.

        :param cmap_list: A list of concept maps.
        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :return: A merged and pruned concept map.
        """
        cmap = [_ele for _cmap in cmap_list for _ele in _cmap]
        return self.cmap_gpt.merge_and_prune(cmap, max_num_concepts, max_num_relationships)

    def generate_cmap(self, max_num_concepts: int = 10, max_num_relationships: int = 30, 
                   max_num_iterations: int = -1, section_scale: float = 0.5) -> List[Dict]:
        """
        Generate a concept map for the entire paper or {max_num_iterations} sections.

        :param max_num_concepts: The maximum number of concepts. Default: 10.
        :param max_num_relationships: The maximum number of relationships. Default: 30.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections. Default: -1.
        :param section_scale: The scale of the maximum number of concepts and relationships for each section. Default: 0.5.
        :return: A concept map.
        """
        if not self._loaded:
            logger.error(f"[Paper2CMap] Please load a PDF file first.")
            raise Exception("Please load a PDF file first.")
        
        logger.info(f"[Paper2CMap] Generating concept maps by section")
        cmap_list = self._generate_cmaps_by_section(int(max_num_concepts * section_scale), int(max_num_relationships * section_scale), max_num_iterations)

        logger.info(f"[Paper2CMap] Merging and pruning concept maps")
        cmap = self._merge_and_prune_cmaps(cmap_list, max_num_concepts, max_num_relationships)

        logger.info(f"[Paper2CMap] Fianl concept map: {cmap}")
        return cmap
                