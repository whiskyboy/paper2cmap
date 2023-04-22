Module paper2cmap.paper2cmap
============================

Classes
-------

`Paper2CMap(model_name: str = '', deployment_name: str = '', deployment_version: str = '', temperature: float = 0.7, request_timeout: int = 60, max_retries: int = 6, max_tokens: int | None = None, verbose: bool = False)`
:   Initialize the Paper2CMap class.
    
    :param model_name: The OpenAI model name.
    :param deployment_name: The Azure deployment name.
    :param deployment_version: The Azure deployment version.
    :param temperature: The temperature of the model.
    :param request_timeout: The request timeout.
    :param max_retries: The maximum number of retries.
    :param max_tokens: The maximum number of tokens.
    :param verbose: Whether to print debug logs.

    ### Methods

    `generate_cmap(self, max_num_concepts: int = 10, max_num_relationships: int = 30, max_num_iterations: int = -1) ‑> List[Dict]`
    :   Generate concept map for the entire paper or {max_num_iterations} sections.
        
        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections.

    `load(self, pdf_path: str) ‑> None`
    :   Load a PDF file.
        
        :param pdf_path: The path to the PDF file.

    `yield_cmap_by_section(self, max_num_concepts: int = 10, max_num_relationships: int = 30, max_num_iterations: int = -1) ‑> List[Dict]`
    :   Yield concept map iteratively by section.
        
        :param max_num_concepts: The maximum number of concepts.
        :param max_num_relationships: The maximum number of relationships.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections.