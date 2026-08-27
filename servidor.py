import socket
from pathlib import Path
from utils import (build_response, content_type, extract_route,
                   missing_body_length, read_file)
from views import delete, edit, favorite, index, not_found

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(8192).decode()

    # O navegador às vezes abre uma conexão sem enviar nenhuma requisição
    if not request:
        client_connection.close()
        continue

    # O navegador pode enviar o corpo do formulário separado do cabeçalho,
    # então continuamos lendo até receber a requisição inteira.
    while missing_body_length(request) > 0:
        pedaco = client_connection.recv(8192).decode()
        if not pedaco:
            break
        request += pedaco

    print('*'*100)
    print(request)

    route = extract_route(request)

    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response(read_file(filepath),
                                  headers=content_type(filepath))
    elif route == '':
        response = index(request)
    elif route.startswith('edit/'):
        response = edit(request, route[len('edit/'):])
    elif route.startswith('delete/'):
        response = delete(request, route[len('delete/'):])
    elif route.startswith('favorite/'):
        response = favorite(request, route[len('favorite/'):])
    else:
        response = not_found()

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()
