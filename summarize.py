from common import *


def summ_porcess(
    text,
    language,
    api_key,
    model_select,
    temperature,
    top_p,
    frequency,
    presence,
):
    if not text:
        return ''
    system_prompt = f"""I want you to act as an {language} summarizer.
I will speak to you in any language and you will detect the language, 
summarize it and briefly describe the core content of my text, in {language}. 
I want you to only reply the summarization results, 
do not write explanations. My first sentence is '{text}'"""

    message_list = [construct_system(system_prompt)]
    response = get_response(message_list, api_key, model_select, temperature, top_p,
                            frequency, presence)
    return response