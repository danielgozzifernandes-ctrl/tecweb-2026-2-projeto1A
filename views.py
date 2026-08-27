from html import escape
from urllib.parse import unquote_plus

from database import Database, Note
from utils import build_response, load_data, load_template

HTML_HEADERS = 'Content-Type: text/html; charset=utf-8'

db = Database('getit')


def load_initial_notes():
    # Na primeira execução o banco está vazio, então ele é preenchido com as
    # anotações de exemplo que antes ficavam no arquivo data/notes.json.
    if db.get_all():
        return

    for dados in load_data('notes.json'):
        db.add(Note(title=dados['titulo'], content=dados['detalhes']))


load_initial_notes()


def extract_params(request):
    # Cabeçalho e corpo estão sempre separados por duas quebras de linha
    partes = request.replace('\r', '').split('\n\n', 1)
    corpo = partes[1] if len(partes) > 1 else ''

    params = {}
    for chave_valor in corpo.split('&'):
        if '=' not in chave_valor:
            continue

        chave, valor = chave_valor.split('=', 1)
        params[unquote_plus(chave)] = unquote_plus(valor)

    return params


def find_note(note_id):
    if not note_id.isdigit():
        return None

    return db.get(int(note_id))


def validate(titulo, detalhes):
    if not titulo:
        return 'A anotação precisa de um título.'

    if not detalhes:
        return 'A anotação precisa de um conteúdo.'

    return ''


def render_error(mensagem):
    if not mensagem:
        return ''

    return load_template('components/error.html').format(message=escape(mensagem))


def render_notes():
    note_template = load_template('components/note.html')
    notes_html = [
        note_template.format(
            id=note.id,
            title=escape(note.title or ''),
            content=escape(note.content),
            favorite_icon='★' if note.favorite else '☆',
            favorite_title='Desfavoritar' if note.favorite else 'Favoritar',
        )
        for note in db.get_all()
    ]

    return '\n'.join(notes_html)


def redirect_to_index():
    return build_response(code=303, reason='See Other', headers='Location: /')


def index(request):
    titulo = ''
    detalhes = ''
    erro = ''

    if request.startswith('POST'):
        params = extract_params(request)
        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()
        erro = validate(titulo, detalhes)

        if not erro:
            db.add(Note(title=titulo, content=detalhes))
            return redirect_to_index()

    body = load_template('index.html').format(
        error=render_error(erro),
        titulo=escape(titulo),
        detalhes=escape(detalhes),
        notes=render_notes(),
    )

    return build_response(body, headers=HTML_HEADERS)


def edit(request, note_id):
    note = find_note(note_id)
    if note is None:
        return not_found()

    titulo = note.title or ''
    detalhes = note.content
    erro = ''

    if request.startswith('POST'):
        params = extract_params(request)
        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()
        erro = validate(titulo, detalhes)

        if not erro:
            note.title = titulo
            note.content = detalhes
            db.update(note)
            return redirect_to_index()

    body = load_template('edit.html').format(
        id=note.id,
        error=render_error(erro),
        titulo=escape(titulo),
        detalhes=escape(detalhes),
    )

    return build_response(body, headers=HTML_HEADERS)


def delete(request, note_id):
    note = find_note(note_id)
    if note is None:
        return not_found()

    # A exclusão só acontece depois que o usuário confirma na página de
    # confirmação, que é enviada em resposta à requisição GET.
    if request.startswith('POST'):
        db.delete(note.id)
        return redirect_to_index()

    body = load_template('delete.html').format(
        id=note.id,
        title=escape(note.title or ''),
        content=escape(note.content),
    )

    return build_response(body, headers=HTML_HEADERS)


def favorite(request, note_id):
    note = find_note(note_id)
    if note is None:
        return not_found()

    note.favorite = 0 if note.favorite else 1
    db.update(note)

    return redirect_to_index()


def not_found():
    return build_response(
        load_template('404.html'),
        code=404,
        reason='Not Found',
        headers=HTML_HEADERS,
    )
