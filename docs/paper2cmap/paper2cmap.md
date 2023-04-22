Module paper2cmap.paper2cmap
============================

Classes
-------

`Paper2CMap(model_name: str = '', deployment_name: str = '', deployment_version: str = '', temperature: float = 0.7, request_timeout: int = 60, max_retries: int = 6, max_tokens: int | None = None, verbose: bool = False)`
:   Initialize the Paper2CMap class.
    
    :param model_name: The OpenAI model name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
    :param deployment_name: The Azure deployment name. If not provided, it will be read from the environment variable OPENAI_MODEL_NAME.
    :param deployment_version: The Azure deployment version. If not provided, it will be read from the environment variable OPENAI_MODEL_VERSION.
    :param temperature: The temperature of the model. Default: 0.7.
    :param request_timeout: The request timeout. Default: 60.
    :param max_retries: The maximum number of retries. Default: 6.
    :param max_tokens: The maximum number of tokens. Default: None.
    :param verbose: Whether to print debug logs. Default: False.

    ### Methods

    `generate_cmap(self, max_num_concepts: int = 10, max_num_relationships: int = 30, max_num_iterations: int = -1, section_scale: float = 0.5) ‑> List[Dict]`
    :   Generate a concept map for the entire paper or {max_num_iterations} sections.
        
        :param max_num_concepts: The maximum number of concepts. Default: 10.
        :param max_num_relationships: The maximum number of relationships. Default: 30.
        :param max_num_iterations: The maximum number of iterations. If set to -1, it will iterate over all sections. Default: -1.
        :param section_scale: The scale of the maximum number of concepts and relationships for each section. Default: 0.5.
        :return: A concept map.

    `load(self, pdf_path: str) ‑> None`
    :   Load a PDF file.
        
        :param pdf_path: The path to the PDF file.