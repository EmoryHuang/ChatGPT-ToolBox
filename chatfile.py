import os
from pathlib import Path
from common import *
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader


def chatfile_file_analysis(file, api_key):
    file_name = Path(file.name).stem
    index_path = f'./temp/{file_name}.json'
    if not api_key:
        return [(None, 'Please input your API-KEY.')]

    os.environ["OPENAI_API_KEY"] = api_key
    if not Path(index_path).exists():
        llama_reader(file)
    return [(None, 'Upload success! We can talk about this file.')]


def llama_reader(file):
    file_name = Path(file.name).stem
    index_path = f'./temp/{file_name}.json'
    if not Path(index_path).parent.exists():
        Path(index_path).parent.mkdir()
    documents = SimpleDirectoryReader(input_files=[file.name]).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents)
    index.save_to_disk(index_path)


def chatfile_send_input(history, text):
    history = history + [(text, None)]
    return history, ""


def chatfile_clear(history):
    return history[:-1]


def chatfile_update_output(
    history,
    file,
    api_key,
    model_select,
    temperature,
    top_p,
    frequency,
    presence,
):
    if not api_key:
        return [(None, 'Please input your API-KEY.')]
    os.environ["OPENAI_API_KEY"] = api_key
    file_name = Path(file.name).stem
    index_path = f'./temp/{file_name}.json'
    if not Path(index_path).exists():
        llama_reader(file)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    response = index.query(history[-1][0])
    history[-1][1] = str(response.response)
    return history