from database import Database, Note

db = Database('banco')

db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')

primeira = notes[0]
primeira.content = 'Abra o pão e coloque o seu achocolatado favorito.'
db.update(primeira)

db.delete(notes[-1].id)

print('Depois da atualização e da exclusão:')
for note in db.get_all():
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')
