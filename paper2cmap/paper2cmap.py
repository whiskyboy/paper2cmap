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

        :param model_name: The OpenAI model name.
        :param deployment_name: The Azure deployment name.
        :param deployment_version: The Azure deployment version.
        :param temperature: The temperature of the model.
        :param request_timeout: The request timeout.
        :param max_retries: The maximum number of retries.
        :param max_tokens: The maximum number of tokens.
        :param verbose: Whether to print debug logs.
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

        if verbose:
            logger.setLevel(colorlog.DEBUG)

    def load(self, pdf_path: str) -> None:
        """
        Load a PDF file.

        :param pdf_path: The path to the PDF file.
        """
        logger.info(f"[Paper2CMap] Loading PDF file: {pdf_path}")
        self.paper_reader.load(pdf_path)

    def yield_cmap_by_section(self, max_num_concepts: int = 10, max_num_relationships: int = 30, 
                   max_num_iterations: int = -1) -> List[Dict]:
        """
        Yield concept map iteratively by section.

        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections.
        """
        cmap = []
        for i, section in enumerate(self.paper_reader.sections):
            if max_num_iterations != -1 and i >= max_num_iterations:
                break

            logger.info(f"[Paper2CMap] Generating concept map for section {i}")
            cmap = self.cmap_gpt.chat(
                text_input=section,
                cmap_input=cmap,
                max_num_concepts=max_num_concepts,
                max_num_relationships=max_num_relationships
                )
            logger.info(f"[Paper2CMap] Concept map for section {i}: {cmap}")
            
            yield cmap

    def generate_cmap(self, max_num_concepts: int = 10, max_num_relationships: int = 30, 
                   max_num_iterations: int = -1) -> List[Dict]:
        """
        Generate concept map for the entire paper or {max_num_iterations} sections.

        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections.
        """
        return list(self.yield_cmap_by_section(max_num_concepts, max_num_relationships, max_num_iterations))[-1]
                