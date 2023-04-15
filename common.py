import gradio as gr
import requests

import config


def get_response(
    history,
    openai_api_key,
    model_select,
    temperature,
    top_p,
    frequency,
    presence,
):
    if not openai_api_key:
        return 'Please input your API-KEY.'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    payload = {
        "model": model_select,
        "messages": history,
        "temperature": temperature,
        "top_p": top_p,
        "n": 1,
        "stream": False,
        "presence_penalty": frequency,
        "frequency_penalty": presence,
    }

    try:
        response = requests.post(
            config.COMPLETION_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=200,
        )
    except Exception as e:
        return str(e)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"API request failed with status code {response.status_code}: {response.text}"


def construct_text(role, text):
    return {"role": role, "content": text}


def construct_user(text):
    return construct_text("user", text)


def construct_system(text):
    return construct_text("system", text)


def construct_assistant(text):
    return construct_text("assistant", text)


if __name__ == '__main__':
    pass