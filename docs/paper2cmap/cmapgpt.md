Module paper2cmap.cmapgpt
=========================

Classes
-------

`CMapGPT(chatbot: ChatOpenAI | AzureChatOpenAI)`
:   

    ### Methods

    `generate(self, text: str, max_num_concepts: int = 10, max_num_relationships: int = 30) ‑> List[Dict]`
    :   Generate a concept map from the given text.
        
        :param text: str, the text input to the model.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the generated concept map.

    `merge_and_prune(self, cmap: List[Dict], max_num_concepts: int = 10, max_num_relationships: int = 30) ‑> List[Dict]`
    :   Merge and prune the given concept map.
        
        :param cmap: List[Dict], the concept map to merge and prune.
        :param max_num_concepts: int, the maximum number of concepts to generate.
        :param max_num_relationships: int, the maximum number of relationships to generate.
        :return: List[Dict], the merged and pruned concept map.