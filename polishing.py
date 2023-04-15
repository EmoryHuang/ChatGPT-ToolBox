from common import *


def poli_porcess(
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
    system_prompt = f"""I want you to act as an {language} translator, 
spelling corrector and improver. I will speak to you in any 
language and you will detect the language, translate it and 
answer in the corrected and improved version of my text, in {language}. 
I want you to replace my simplified A0-level words and sentences 
with more beautiful and elegant, upper level {language} words and 
sentences. Keep the meaning same, but make them more literary. 
I want you to only reply the correction, the improvements and 
nothing else, do not write explanations. My first sentence is '{text}'"""

    message_list = [construct_system(system_prompt)]
    response = get_response(message_list, api_key, model_select, temperature, top_p,
                            frequency, presence)
    return response