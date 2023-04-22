Module paper2cmap.cmapgpt
=========================

Classes
-------

`CMapGPT(chatbot: ChatOpenAI | AzureChatOpenAI)`
:   

    ### Methods

    `chat(self, text_input: str, cmap_input: List[Dict] = [], max_num_concepts: int = 10, max_num_relationships: int = 30) ‑> List[Dict]`
    :   Chat with the model to generate a concept map.
        
        :param text_input: str, the text input to the model.
        :param cmap_input: List[Dict], a json that represents the concept map input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the generated concept map output.

    `create_cmap_prompt(self) ‑> langchain.prompts.chat.ChatPromptTemplate`
    :   Create the concept map prompt.
        
        :return: The concept map prompt.

    `format_cmap_prompt(self, text_input: str, cmap_input: List[Dict], max_num_concepts: int = 10, max_num_relationships: int = 30) ‑> List[langchain.schema.BaseMessage]`
    :   Format the concept map prompt.
        
        :param text_input: str, the text input to the model.
        :param cmap_input: List[Dict], a json that represents the concept map input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[BaseMessage], the formatted concept map prompt.