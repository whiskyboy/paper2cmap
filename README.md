# Paper2CMap

A package that automatically generates a concept map for a PDF document using LLM.

## TODO
- [ ] Optimize concept map generating prompt
- [ ] Add few shots for concept map generating
- [ ] Support LNKG/CXL/SVG format output
- [ ] Support QA based on generated concept map

## Overview

### What is Concept Map?

*(Answerd by ChatGPT)*
> A concept map is a visual tool that is used to organize and represent knowledge, ideas, and information in a hierarchical or non-linear way. It is a graphical representation of a network of interconnected concepts, ideas, or themes, and the relationships between them. Concept maps are commonly used in education, particularly in fields such as science, social studies, and language arts, to help students organize and understand complex information.
> 
> Concept maps typically consist of nodes or boxes, which represent concepts or ideas, and lines or arrows, which show the relationships between the concepts. The nodes can be labeled with keywords or short phrases, and the lines or arrows can be labeled with connecting words, such as "leads to," "is a type of," or "causes."
> 
> Concept maps can be created by individuals or groups, and can be used to facilitate learning, problem-solving, decision-making, and communication. They are a flexible and powerful tool that can be adapted to many different contexts and purposes.

### What is Paper2CMap?

Paper2CMap is a package that automatically generates a concept map for a PDF document using LLM. It will first extract the text from the PDF document, then cut the text into sections, and finally generate concept map based on the sections. Currently the generated concept map is in JSON format:
```JSON
[{"source": "source concept", "target": "target concept", "relationship": "relationship between source and target"}]
```
In future, we will support more formats export, such as LNKG/CXL/SVG.

## Quick Start

### Prerequisites

- Python 3.8+
- An OpenAI API key or Azure OpenAI Service deployment
- Set environment variables:
    ```bash
    # If you are using OpenAI Official Service
    export OPENAI_API_TYPE="openai"
    export OPENAI_API_KEY="<OpenAI API Key>"

    # If you are using Azure OpenAI Service
    export OPENAI_API_TYPE="azure"
    export OPENAI_API_BASE="<Azure OpenAI Service Endpoint>"
    export OPENAI_API_KEY="<Azure OpenAI Service Key>"
    ```

### Installation

You can now install Paper2CMap with pip:
```bash
pip install paper2cmap
```

### Usage

Now you can easily generate a concept map from a PDF document within 3 lines of code:
```python
from paper2cmap import Paper2CMap

paper2cmap = Paper2CMap(model_name="gpt-3.5-turb")
paper2cmap.load("path/to/paper.pdf")
paper2cmap.generate_cmap()
```

For more details of the API, please refer to [API Reference](docs/paper2cmap/paper2cmap.md).

### Gradio App

We also host a [Gradio App](https://huggingface.co/spaces/whiskyboy/paper2cmap) at HuggingFace Space for you to try out Paper2CMap without installing it locally. You can also deploy it to your own server:
```bash
pip install gradio
gradio app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contributing

As an open source project, we welcome contributions and suggestions. Please follow the [fork and pull request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) workflow to contribute to this project. Please do not try to push directly to this repo unless you are maintainer.

## Contact

If you have any questions, please feel free to contact us via <weitian.bnu@gmail.com>

