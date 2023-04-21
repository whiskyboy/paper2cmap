import os
import gradio as gr

from paper2cmap import Paper2CMap


def set_key(openai_api_key):
    os.environ["OPENAI_API_TYPE"] = "openai"
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
    return openai_api_key


def generate_cmap(paper_path, temperature, max_num_concepts, max_num_links, max_num_sections):
    paper2camp = Paper2CMap(temperature=temperature)
    paper2camp.load(paper_path.name)
    cmap = paper2camp.generate_cmap(
        max_num_concepts=max_num_concepts,
        max_num_relationships=max_num_links,
        max_num_iterations=max_num_sections,
    )
    return cmap


css = ".json {height: 657px; overflow: scroll;} .json-holder {height: 657px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1><center><a href='https://github.com/whiskyboy/paper2cmap'>Paper2CMap</a></center></h1>")
    gr.Markdown("<p align='center' style='font-size: 20px;'>A library to generate concept map from a research paper. Powered by LLM.</p>")

    # Set Key
    with gr.Row():
        with gr.Column(scale=0.85):
            openai_api_key = gr.Textbox(
                show_label=False,
                placeholder="Set your OpenAI API key here and press Enter",
                lines=1,
                type="password"
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            set_key_btn = gr.Button("Submit")

    # Inputs
    with gr.Row():
        with gr.Column(scale=0.25):
            # Set Parameters
            temperature = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.2,
                step=0.1,
                label="Temperature",
                interactive=True,
            )
            max_num_concepts = gr.Number(
                value=10,
                label="Max Number of Concepts",
                interactive=True,
                precision=0,
            )
            max_num_links = gr.Number(
                value=30,
                label="Max Number of Links",
                interactive=True,
                precision=0,
            )
            max_num_sections = gr.Number(
                value=-1,
                label="Max Number of Sections",
                interactive=True,
                precision=0,
            )

            # Upload File
            paper_path = gr.File(
                file_types=[".pdf"],
                label="PDF",
            )

            # Generate Button
            generate_btn = gr.Button("Generate")

        # Outputs
        with gr.Column(scale=0.75):
            # Output Concept Map
            concept_map = gr.JSON(label="Concept Map", elem_classes="json")

    # Event Handlers
    openai_api_key.submit(set_key, [openai_api_key], [openai_api_key])
    set_key_btn.click(set_key, [openai_api_key], [openai_api_key])

    generate_btn.click(
        fn=generate_cmap,
        inputs=[paper_path, temperature, max_num_concepts, max_num_links, max_num_sections],
        outputs=[concept_map],
    )
        

demo.launch()