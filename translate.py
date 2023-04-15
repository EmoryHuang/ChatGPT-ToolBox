from common import *
import config


def trans_check_input(type, change_type):
    if type == change_type:
        for c in config.LANGUAGE:
            if type != c:
                return c
    return change_type


def trans_porcess(
    text,
    from_type,
    to_type,
    api_key,
    model_select,
    temperature,
    top_p,
    frequency,
    presence,
):
    if not text:
        return ''
    system_prompt = f"""I want you to act as a/an {to_type} translator. 
I will speak to you in {from_type} language and you will translate. 
The translation result should be beautiful and elegant, upper level 
words and sentences. I want you to only reply the translation results, 
do not write explanations. My first sentence is '{text}'"""

    message_list = [construct_system(system_prompt)]
    response = get_response(message_list, api_key, model_select, temperature, top_p,
                            frequency, presence)
    return response
