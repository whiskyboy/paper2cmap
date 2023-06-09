import os
import sys
sys.path.insert(0, './')

from paper2cmap import Paper2CMap, logger

logger.setLevel("DEBUG")

if __name__ == "__main__":
    paper2camp = Paper2CMap()

    demo_pdf = "./tests/examples/attentionisallyouneed.pdf"
    paper2camp.load(demo_pdf)

    print(paper2camp.generate_cmap(
        max_num_concepts=15,
        max_num_relationships=30,
        max_num_iterations=3,
    ))