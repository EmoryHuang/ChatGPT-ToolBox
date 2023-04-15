import gradio as gr

import config
from chat import *
from common import *
from polishing import *
from summarize import *
from translate import *
from chatfile import *

with open("custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

with gr.Blocks(css=customCSS) as demo:
    gr.Markdown(config.TITLE)

    with gr.Row():
        with gr.Column(scale=5):
            with gr.Tab('Chat'):
                chat_chatbot = gr.Chatbot([]).style(height=500)
                with gr.Row():
                    with gr.Column(scale=0.7):
                        chat_input_txt = gr.Textbox(
                            show_label=False,
                            placeholder="Enter text and press enter",
                            label="message").style(container=False)
                    with gr.Column(scale=0.15, min_width=0):
                        chat_send_btn = gr.Button("Send")
                    with gr.Column(scale=0.15, min_width=0):
                        chat_clear_btn = gr.Button("Clear")
                chat_type_radio = gr.Radio(["Single", "Contextual"],
                                           value="Single",
                                           label="Choose chat type")
            with gr.Tab('Translate'):
                with gr.Row():
                    with gr.Column(scale=0.5, min_width=150):
                        trans_from_type_dropdown = gr.Dropdown(
                            choices=config.LANGUAGE,
                            value=config.LANGUAGE[0],
                            label="From",
                            multiselect=False,
                        )
                    with gr.Column(scale=0.5, min_width=150):
                        trans_to_type_dropdown = gr.Dropdown(
                            choices=config.LANGUAGE,
                            value=config.LANGUAGE[1],
                            label="To",
                            multiselect=False,
                        )
                with gr.Row():
                    with gr.Column(scale=0.5, min_width=150):
                        trans_input_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                            placeholder="Enter text and press enter",
                        ).style(show_copy_button=True, container=False)
                    with gr.Column(scale=0.5, min_width=150):
                        trans_output_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                        ).style(show_copy_button=True, container=False)
                trans_main_btn = gr.Button("Translate")
            with gr.Tab('Polishing'):
                poli_language_dropdown = gr.Dropdown(
                    choices=config.LANGUAGE,
                    value=config.LANGUAGE[0],
                    label="Language",
                    multiselect=False,
                )
                with gr.Row():
                    with gr.Column(scale=0.5, min_width=150):
                        poli_input_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                            placeholder="Enter text and press enter",
                        ).style(show_copy_button=True, container=False)
                    with gr.Column(scale=0.5, min_width=150):
                        poli_output_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                        ).style(show_copy_button=True, container=False)
                poli_main_btn = gr.Button("Polishing")
            with gr.Tab('Summarize'):
                summ_language_dropdown = gr.Dropdown(
                    choices=config.LANGUAGE,
                    value=config.LANGUAGE[0],
                    label="Language",
                    multiselect=False,
                )
                with gr.Row():
                    with gr.Column(scale=0.5, min_width=150):
                        summ_input_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                            placeholder="Enter text and press enter",
                        ).style(show_copy_button=True, container=False)
                    with gr.Column(scale=0.5, min_width=150):
                        summ_output_txt = gr.Textbox(
                            show_label=False,
                            lines=20,
                        ).style(show_copy_button=True, container=False)
                summ_main_btn = gr.Button("Summarize")
            with gr.Tab('FileChat'):
                chatfile_file = gr.File(file_types=['file'])
                chatfile_chatbot = gr.Chatbot([]).style(height=450)
                with gr.Row():
                    with gr.Column(scale=0.7):
                        chatfile_input_txt = gr.Textbox(
                            show_label=False,
                            placeholder="Enter text and press enter",
                            label="message").style(container=False)
                    with gr.Column(scale=0.15, min_width=0):
                        chatfile_send_btn = gr.Button("Send")
                    with gr.Column(scale=0.15, min_width=0):
                        chatfile_clear_btn = gr.Button("Clear")
                chatfile_type_radio = gr.Radio(["Single", "Contextual"],
                                               value="Single",
                                               label="Choose chat type")
            with gr.Tab('...'):
                pass

        with gr.Column(scale=1):
            with gr.Accordion('Base'):
                api_key_text = gr.Textbox(
                    show_label=True,
                    placeholder="OpenAI API-key...",
                    type="password",
                    label="API-Key",
                )
                model_select_dropdown = gr.Dropdown(
                    choices=config.MODELS,
                    value=config.MODELS[0],
                    label="Model",
                    multiselect=False,
                )
                # language_select_dropdown = gr.Dropdown(
                #     choices=config.LANGUAGE,
                #     value=config.LANGUAGE[0],
                #     label="Language",
                #     multiselect=False,
                # )
            with gr.Accordion('Advanced', open=False):
                temperature_slider = gr.Slider(0, 1, value=0.7, label="Temperature")
                top_p_slider = gr.Slider(0, 1, value=1, label="Top P")
                frequency_slider = gr.Slider(0, 2, value=0, label="Frequency penalty")
                presence_slider = gr.Slider(0, 2, value=0, label="Presence penalty")
    gr.HTML(config.DESC)

    global_args = [
        api_key_text,
        model_select_dropdown,
        temperature_slider,
        top_p_slider,
        frequency_slider,
        presence_slider,
    ]

    # Chat
    chat_input_args = dict(fn=chat_send_input,
                           inputs=[chat_chatbot, chat_input_txt],
                           outputs=[chat_chatbot, chat_input_txt])
    chat_output_args = dict(fn=chat_update_output,
                            inputs=[chat_chatbot, chat_type_radio] + global_args,
                            outputs=[chat_chatbot])
    chat_clear_args = dict(fn=chat_clear, inputs=[chat_chatbot], outputs=[chat_chatbot])

    chat_input_txt.submit(**chat_input_args).then(**chat_output_args)
    chat_send_btn.click(**chat_input_args).then(**chat_output_args)
    chat_clear_btn.click(**chat_clear_args)

    # Translate
    trans_from_args = dict(fn=trans_check_input,
                           inputs=[trans_from_type_dropdown, trans_to_type_dropdown],
                           outputs=[trans_to_type_dropdown])
    trans_to_args = dict(fn=trans_check_input,
                         inputs=[trans_to_type_dropdown, trans_from_type_dropdown],
                         outputs=[trans_from_type_dropdown])
    trans_output_args = dict(
        fn=trans_porcess,
        inputs=[trans_input_txt, trans_from_type_dropdown, trans_to_type_dropdown] +
        global_args,
        outputs=[trans_output_txt])
    trans_from_type_dropdown.change(**trans_from_args)
    trans_to_type_dropdown.change(**trans_to_args)
    trans_main_btn.click(**trans_output_args)

    # Polishing
    poli_output_args = dict(fn=poli_porcess,
                            inputs=[poli_input_txt, poli_language_dropdown] + global_args,
                            outputs=[poli_output_txt])
    poli_main_btn.click(**poli_output_args)

    # Summarize
    summ_output_args = dict(fn=summ_porcess,
                            inputs=[summ_input_txt, summ_language_dropdown] + global_args,
                            outputs=[summ_output_txt])
    summ_main_btn.click(**summ_output_args)

    # chatfile
    chatfile_file_args = dict(fn=chatfile_file_analysis,
                              inputs=[chatfile_file, api_key_text],
                              outputs=[chatfile_chatbot])
    chatfile_input_args = dict(fn=chatfile_send_input,
                               inputs=[chatfile_chatbot, chatfile_input_txt],
                               outputs=[chatfile_chatbot, chatfile_input_txt])
    chatfile_output_args = dict(fn=chatfile_update_output,
                                inputs=[chatfile_chatbot, chatfile_file] + global_args,
                                outputs=[chatfile_chatbot])
    chatfile_clear_args = dict(fn=chatfile_clear,
                               inputs=[chatfile_chatbot],
                               outputs=[chatfile_chatbot])

    chatfile_file.upload(**chatfile_file_args)
    chatfile_input_txt.submit(**chatfile_input_args).then(**chatfile_output_args)
    chatfile_send_btn.click(**chatfile_input_args).then(**chatfile_output_args)
    chatfile_clear_btn.click(**chatfile_clear_args)

if __name__ == "__main__":
    demo.launch()
    # demo.launch(auth=("username", "password"))
