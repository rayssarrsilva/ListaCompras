# 🛒 Lista de Compras – Full Stack (Flask + FastAPI + PostgreSQL)

## Um sistema elegante e funcional para gerenciar listas de compras com login, múltiplos carrinhos, adição em lote e interface com efeitos de pergaminho!

### Permite criar, visualizar, editar e deletar carrinhos, além de adicionar individualmente ou em lote e deletar itens.

---

## 🚀 Funcionalidades

✅ Registro e login de usuários
✅ Criação de múltiplos carrinhos por usuário
✅ Adição de itens únicos ou em lote (separados por vírgula)
✅ Visualização de itens em um "pergaminho" animado com som
✅ Deleção individual de itens sem recarregar a página
✅ Interface elegante, minimalista e sem alertas intrusivos
✅ Integração segura entre frontend (Flask) e backend (FastAPI)

📦 Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.10+
Git
PostgreSQL 12+
```💡 Dica para Windows: Use o PowerShell (não o CMD) para evitar problemas com permissões de script.```


---

## 🛠️ Tecnologias

- **Backend:** Flask + SQLAlchemy + Flask-Login + FastAPI
- **Banco de Dados:** PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript  
- **Gerenciamento de dependências:** `requirements.txt`  
- **Variáveis de ambiente:** `.env` com `python-dotenv`

---

🛠️ Passo a Passo para Rodar o Projeto
1. Clone o repositório
git clone https://github.com/seu-usuario/ListaCompras.git 
cd ListaCompras 

2. Crie e ative o ambiente virtual
Windows (PowerShell):
 python -m venv venv
.\venv\Scripts\Activate.ps1 
⚠️ Se aparecer erro de execução de scripts, abra o PowerShell como administrador e execute uma vez:
```  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser ```

3. Instale as dependências
```  pip install -r requirements.txt ```
✅ O arquivo requirements.txt já inclui todas as dependências necessárias, inclusive psycopg2-binary (driver do PostgreSQL) e python-multipart.

4. Configure o banco de dados PostgreSQL
Abra o pgAdmin ou use o terminal do PostgreSQL.
Crie um banco de dados chamado:

``` listacompras  ```
Certifique-se de que o usuário postgres tenha senha 123 (apenas para desenvolvimento!).
🔒 Em produção, nunca use senha fraca nem o usuário postgres!


Qwen3-Max
2:13 PM
Perfeito! Com essas informações, posso criar um README.md completo, seguro e extremamente claro — feito especialmente para evitar os erros que você enfrentou e garantir que qualquer pessoa consiga rodar seu projeto em minutos.

Aqui está o README.md pronto para seu GitHub:

🛒 Lista de Compras – Full Stack (Flask + FastAPI + PostgreSQL)
Um sistema elegante e funcional para gerenciar listas de compras com login, múltiplos carrinhos, adição em lote e interface com efeitos de pergaminho!


🚀 Funcionalidades
✅ Registro e login de usuários
✅ Criação de múltiplos carrinhos por usuário
✅ Adição de itens únicos ou em lote (separados por vírgula)
✅ Visualização de itens em um "pergaminho" animado com som
✅ Deleção individual de itens sem recarregar a página
✅ Interface elegante, minimalista e sem alertas intrusivos
✅ Integração segura entre frontend (Flask) e backend (FastAPI)
📦 Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.10+
Git
PostgreSQL 12+
💡 Dica para Windows: Use o PowerShell (não o CMD) para evitar problemas com permissões de script.

🛠️ Passo a Passo para Rodar o Projeto
1. Clone o repositório
bash
12
2. Crie e ative o ambiente virtual
Windows (PowerShell):
powershell
12
⚠️ Se aparecer erro de execução de scripts, abra o PowerShell como administrador e execute uma vez:

powershell
1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Linux / macOS:
bash
12
3. Instale as dependências
bash
1
✅ O arquivo requirements.txt já inclui todas as dependências necessárias, inclusive psycopg2-binary (driver do PostgreSQL) e python-multipart.

4. Configure o banco de dados PostgreSQL
Abra o pgAdmin ou use o terminal do PostgreSQL.
Crie um banco de dados chamado:
1
Certifique-se de que o usuário postgres tenha senha 123 (apenas para desenvolvimento!).
🔒 Em produção, nunca use senha fraca nem o usuário postgres!

5. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
``` DATABASE_URL=postgresql://postgres:123@localhost:5432/listacompras
SECRET_KEY=4b08d4a0795967a5345a82597f91f1f182ecac009681ca3058efecdcb0b6a459 ```
📌 Importante: O .env não deve ser commitado em repositórios públicos. Ele já está listado no .gitignore.

6. Inicie o Backend (FastAPI)
Abra um novo terminal (mantenha o ambiente virtual ativado) e execute:
``` # Você deve estar na RAIZ do projeto (pasta ListaCompras/)
uvicorn backend.main:app --reload --port 8000 ```
✅ Você verá: ``` INFO:     Uvicorn running on http://127.0.0.1:8000 ```
🔍 Teste no navegador: http://localhost:8000 → deve retornar {"message": "API ListaCompras está rodando 🚀"}


7. Inicie o Frontend (Flask)
Em outro terminal (com o ambiente virtual ativado):
```  # Na raiz do projeto
python -m frontend.app```

8. Acesse a aplicação
Abra o navegador e vá para:
👉 http://127.0.0.1:5000

Crie uma conta
Faça login
Crie carrinhos, adicione itens e use o pergaminho mágico! 


🗂️ Estrutura do Projeto
ListaCompras/
├── backend/               # API REST com FastAPI
│   ├── main.py            # Ponto de entrada (com CORS configurado)
│   ├── models.py          # Modelos SQLAlchemy (User, Cart, Item)
│   ├── database.py        # Conexão com PostgreSQL
│   └── routes/            # Rotas de autenticação e carrinhos
├── frontend/              # Interface com Flask + Jinja2
│   ├── app.py             # App Flask com Flask-Login
│   ├── templates/         # HTML com efeitos de pergaminho
│   └── static/            # CSS, JS e áudio (scroll-open.mp3)
├── .env                   # Variáveis de ambiente (ex: DATABASE_URL)
├── requirements.txt       # Todas as dependências
└── README.md              # Este arquivo!

📬 Dúvidas ou Problemas?
Se você seguiu todos os passos e ainda assim não funcionou, sinta-se à vontade para entrar em contato!

➡️ Acesse meu Portfólio (hospedado no GitHub Pages)
➡️ Na aba "Contato", você pode me enviar uma mensagem diretamente.

Estou aqui para ajudar! 💙

📜 Licença
Este projeto é de código aberto e gratuito para uso pessoal e educacional.

Feito com ❤️ para quem acredita que tecnologia deve ser acessível, elegante e funcional.

✅ Pronto para usar!
Basta seguir os passos acima — e em menos de 5 minutos, você terá seu próprio sistema de lista de compras rodando localmente.

Boa sorte, e divirta-se! 🛒✨



