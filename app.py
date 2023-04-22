import os
import gradio as gr

from paper2cmap import Paper2CMap


def set_key(openai_api_key):
    os.environ["OPENAI_API_TYPE"] = "openai"
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
    return openai_api_key

    
def load_text(state, paper_path, temperature, max_num_sections):
    paper2cmap = Paper2CMap(temperature=temperature)
    paper2cmap.load(paper_path.name)
    if max_num_sections == -1:
        text = paper2cmap.paper_reader.full_text
    else:
        text = "\n\n".join(paper2cmap.paper_reader.sections[:max_num_sections])

    state["paper2cmap"] = paper2cmap
    return state, text


def generate_cmap(state, max_num_concepts, max_num_links, max_num_sections):
    paper2cmap = state["paper2cmap"]
    cmap = paper2cmap.generate_cmap(
        max_num_concepts=max_num_concepts,
        max_num_relationships=max_num_links,
        max_num_iterations=max_num_sections,
    )

    del state["paper2cmap"]
    return state, cmap


css = ".json {height: 657px; overflow: scroll;} .json-holder {height: 657px; overflow: scroll;}"
with gr.Blocks(css=css) as demo:
    state = gr.State(value={})
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
            paper_path = gr.File(file_types=[".pdf"], label="PDF")

            # Generate Button
            generate_btn = gr.Button("Generate")

        # Outputs
        with gr.Column(scale=0.75):
            # Output Text
            text = gr.Textbox(lines=10, max_lines=10, label="Text", interactive=False)
            # Output Concept Map
            concept_map = gr.JSON(label="Concept Map")

    # Event Handlers
    openai_api_key.submit(set_key, [openai_api_key], [openai_api_key])
    set_key_btn.click(set_key, [openai_api_key], [openai_api_key])

    generate_btn.click(
        fn=load_text,
        inputs=[state, paper_path, temperature, max_num_sections],
        outputs=[state, text],
    ).then(
        fn=generate_cmap,
        inputs=[state, max_num_concepts, max_num_links, max_num_sections],
        outputs=[state, concept_map],
    )

    # Examples
    gr.Examples(
        examples=[
            ["tests/examples/bert.pdf"],
            ["tests/examples/attentionisallyouneed.pdf"],
            ["tests/examples/ashortsurvey.pdf"],
        ],
        inputs=[paper_path],
    )
        

demo.launch()