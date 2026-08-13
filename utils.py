import json
from pathlib import Path


def extract_route(request):
    primeira_linha = request.split('\n')[0]

    partes = primeira_linha.split(' ')

    rota = partes[1]

    return rota[1:]


def read_file(filepath):
    with open(filepath, 'rb') as arquivo:
        return arquivo.read()


def load_data(filename):
    filepath = Path('data') / filename

    with open(
        filepath,
        encoding='utf-8'
    ) as arquivo:
        return json.load(arquivo)


def save_data(filename, data):
    filepath = Path('data') / filename

    with open(
        filepath,
        'w',
        encoding='utf-8'
    ) as arquivo:
        json.dump(data, arquivo, ensure_ascii=False, indent=2)


def load_template(filename):
    filepath = Path('templates') / filename

    with open(
        filepath,
        encoding='utf-8'
    ) as arquivo:
        return arquivo.read()


def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()

    response_line = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response_line += f'{headers}\n'
    response_line += '\n'

    return response_line.encode() + body
