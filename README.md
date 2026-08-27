# Get-it — Projeto 1A

Bloco de notas web desenvolvido em Python puro (apenas com a biblioteca padrão),
a partir dos handouts de Tecnologias Web.

Daniel Gozzi Fernandes

## Funcionalidades

- Listagem e criação de anotações (handout 01)
- Estilo da página com o CSS do Desafio CSS
- Persistência em banco de dados SQLite (handout 03)
- Editar anotações
- Apagar anotações, com página de confirmação
- Favoritar anotações (as favoritas aparecem primeiro na listagem)
- Validação do formulário e página de erro 404

## Como executar

O servidor precisa ser executado a partir da pasta do projeto, porque os
templates e os dados são carregados por caminhos relativos:

```
cd tecweb-2026-2-projeto1A
python servidor.py
```

Depois acesse <http://localhost:8080> no navegador.

Na primeira execução o arquivo `getit.db` é criado automaticamente e recebe as
anotações de exemplo do arquivo `data/notes.json`.

## Testes

```
python test_utils.py
```

## Rotas

| Rota                | Método | Descrição                                       |
| ------------------- | ------ | ----------------------------------------------- |
| `/`                 | GET    | Lista as anotações                              |
| `/`                 | POST   | Cria uma anotação                               |
| `/edit/<id>`        | GET    | Formulário de edição preenchido                 |
| `/edit/<id>`        | POST   | Salva a edição e volta para a página principal  |
| `/delete/<id>`      | GET    | Página de confirmação da exclusão               |
| `/delete/<id>`      | POST   | Apaga a anotação e volta para a página principal |
| `/favorite/<id>`    | GET    | Marca/desmarca a anotação como favorita         |

Qualquer outra rota responde com a página `templates/404.html` e o código HTTP 404.
