from urllib.parse import unquote_plus
from utils import build_response, load_data, load_template, save_data


def index(request):
    if request.startswith('POST'):
        body = request.replace('\r\n', '\n').split('\n\n', 1)[1]

        nova_nota = {}
        for par in body.split('&'):
            chave, valor = par.split('=', 1)
            nova_nota[unquote_plus(chave)] = unquote_plus(valor)

        notas = load_data('notes.json')
        notas.append(nova_nota)
        save_data('notes.json', notas)

        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    return build_response(body)
