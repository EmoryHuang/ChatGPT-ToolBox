from common import *


def chat_send_input(history, text):
    history = history + [(text, None)]
    return history, ""


def chat_clear(history):
    return history[:-1]


def chat_update_output(
    history,
    chat_type,
    api_key,
    model_select,
    temperature,
    top_p,
    frequency,
    presence,
):
    message_list = []
    if chat_type == 'Contextual' and len(history) > 1:
        for user, assistant in reversed(history[:20]):
            if assistant:
                message_list.append(construct_user(user))
                message_list.append(construct_assistant(assistant))
    message_list.append(construct_user(history[-1][0]))
    response = get_response(message_list, api_key, model_select, temperature, top_p,
                            frequency, presence)
    history[-1][1] = response
    return history