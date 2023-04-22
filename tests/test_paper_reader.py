import sys
sys.path.insert(0, './')

from paper2cmap import PaperReader, LLMManager, logger

logger.setLevel("DEBUG")

if __name__ == "__main__":
    chatbot = LLMManager().LLM

    paper_reader = PaperReader(chatbot=chatbot)
    
    demo_pdf = "./tests/examples/attentionisallyouneed.pdf"
    paper_reader.load(demo_pdf)

    print(f"Catelogue: {paper_reader.catelogue}")
    for i, section in enumerate(paper_reader.sections):
        print(f"\nSection {i}: {section}\n")