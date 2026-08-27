import json
from pathlib import Path


CONTENT_TYPES = {
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.html': 'text/html; charset=utf-8',
    '.json': 'application/json',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
}


def extract_route(request):
    primeira_linha = request.split('\n')[0]

    partes = primeira_linha.split(' ')

    rota = partes[1]

    return rota[1:]


def missing_body_length(request):
    # O corpo tem o tamanho anunciado pelo cabeçalho Content-Length. Cabeçalho e
    # corpo estão separados por duas quebras de linha.
    cabecalho, _, corpo = request.replace('\r\n', '\n').partition('\n\n')

    tamanho = 0
    for linha in cabecalho.split('\n'):
        if linha.lower().startswith('content-length:'):
            tamanho = int(linha.split(':')[1])

    return tamanho - len(corpo)


def read_file(filepath):
    with open(filepath, 'rb') as arquivo:
        return arquivo.read()


def content_type(filepath):
    tipo = CONTENT_TYPES.get(filepath.suffix, 'application/octet-stream')

    return f'Content-Type: {tipo}'


def load_data(filename):
    filepath = Path('data') / filename

    with open(
        filepath,
        encoding='utf-8'
    ) as arquivo:
        return json.load(arquivo)


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
