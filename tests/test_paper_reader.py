import os
import sys
sys.path.insert(0, './')

from paper2cmap import PaperReader, LLMManager


if __name__ == "__main__":
    OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "")
    OPENAI_MODEL_VERSION = os.environ.get("OPENAI_MODEL_VERSION", "")
    
    chatbot = LLMManager(
        model_name=OPENAI_MODEL_NAME,
        deployment_name=OPENAI_MODEL_NAME,
        deployment_version=OPENAI_MODEL_VERSION,
        temperature=0.2,
        ).LLM

    paper_reader = PaperReader(chatbot=chatbot)
    demo_pdf = "./tests/examples/attentionisallyouneed.pdf"
    paper_reader.load(demo_pdf)

    print(f"Catelogue: {paper_reader.catelogue}")
    for i, section in enumerate(paper_reader.sections):
        print(f"\nSection {i}: {section}\n")