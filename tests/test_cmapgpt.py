import sys
sys.path.insert(0, './')

from paper2cmap import CMapGPT, LLMManager


if __name__ == "__main__":
    chatbot = LLMManager(temperature=0.2).LLM
    
    cmap_gpt = CMapGPT(chatbot=chatbot)

    text_input = """
    A large language model (LLM) is a language model consisting of a neural network with many parameters (typically billions of weights or more), trained on large quantities of unlabelled text using self-supervised learning. 
    LLMs emerged around 2018 and perform well at a wide variety of tasks.
    This has shifted the focus of natural language processing research away from the previous paradigm of training specialized supervised models for specific tasks.
    Large language models have most commonly used the transformer architecture, which, since 2018, has become the standard deep learning technique for sequential data (previously, recurrent architectures such as the LSTM were most common).
    LLMs are trained in an unsupervised manner on unannotated text. A left-to-right transformer is trained to maximize the probability assigned to the next word in the training data, given the previous context.
    Alternatively, an LLM may use a bidirectional transformer (as in the example of BERT), which assigns a probability distribution over words given access to both preceding and following context.
    In addition to the task of predicting the next word or "filling in the blanks", LLMs may be trained on auxiliary tasks which test their understanding of the data distribution, such as Next Sentence Prediction (NSP), in which pairs of sentences are presented and the model must predict whether they appear side-by-side in the training corpus.
    """
    cmap_input = []

    print(cmap_gpt.chat(text_input, cmap_input,
                        max_num_concepts=5, max_num_relationships=10))