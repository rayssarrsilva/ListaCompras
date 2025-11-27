# 🛒 Lista de Compras

Aplicação web para gerenciar **carrinhos de compras**, construída com **Flask**, **SQLAlchemy**, **PostgreSQL** e **HTML/CSS/JavaScript**.  
Permite criar, visualizar, editar e deletar carrinhos, além de adicionar itens individualmente ou em lote.

---

## 🚀 Funcionalidades

- Criar novos carrinhos
- Visualizar lista de carrinhos existentes
- Selecionar um carrinho ativo
- Adicionar itens individualmente ou em lote (separados por vírgula)
- Deletar carrinhos e itens
- Login de usuário (com suporte a múltiplos usuários)
- Banco de dados persistente com **PostgreSQL**

---

## 🛠️ Tecnologias

- **Backend:** Flask + SQLAlchemy + Flask-Login + FastAPI
- **Banco de Dados:** PostgreSQL  
- **Frontend:** HTML, CSS, JavaScript  
- **Gerenciamento de dependências:** `requirements.txt`  
- **Variáveis de ambiente:** `.env` com `python-dotenv`

---

## 💻 Como rodar na sua máquina

Siga **todos os passos abaixo na ordem** para evitar erros comuns (como o `UnicodeDecodeError` causado por caminhos com espaços ou acentos).

---

### ✅ 1. Requisitos prévios

- **Python 3.8+** instalado ([baixe aqui](https://www.python.org/downloads/))
- **PostgreSQL** instalado e rodando ([baixe aqui](https://www.postgresql.org/download/))
- **Git** (para clonar o repositório)

> ⚠️ **IMPORTANTE:**  
> ❌ **NÃO use pastas com espaços, acentos ou caracteres especiais** no caminho (ex: `Área de Trabalho`, `Documentos pessoais`, `projetos oficiais`).  
> ✅ **Use um caminho simples**, como:  
> - Windows: `C:\dev\ListaCompras`  
> - Linux/Mac: `~/dev/ListaCompras`

---

### 📥 2. Clone o repositório

Abra o terminal (PowerShell, CMD ou Bash) e execute:

```bash
git clone https://github.com/seu-usuario/ListaCompras.git
cd ListaCompras
```
🐍 3. Crie e ative o ambiente virtual
```bash

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

📦 4. Instale as dependências
pip install -r requirements.txt

🗃️ 5. Configure seu banco de dados PostgreSQL
1 instale o postgresql
2 Abra o pgAdmin ou o terminal psql.
3 Crie um banco de dados com o nome que você quiser (ex: minha_lista).
```bash
CREATE DATABASE minha_lista;
```
4 Anote:
Usuário do banco (ex: postgres)
Senha do usuário (ex: minhasenha123)
Nome do banco (ex: minha_lista)
Porta (geralmente 5432)

🔐 6. Crie o arquivo .env
Na raiz do projeto (mesma pasta do app.py), crie um arquivo chamado .env com o seguinte conteúdo:

``` 
DATABASE_URL=postgresql://SEU_USUARIO:SUA_SENHA@localhost:5432/NOME_DO_SEU_BANCO
SECRET_KEY=sua_chave_secreta_aqui_com_pelo_menos_32_caracteres
```
🔁 Substitua pelos seus dados reais!
💡 Dica para gerar uma SECRET_KEY forte: 
```
python -c "import secrets; print(secrets.token_hex(32))"
```
🚫 Nunca envie o .env para o GitHub!
Verifique se há uma linha .env no seu .gitignore. 

7. Execute no terminal o arquivo ja existente create_db:
python create_db.py

8. Inicie a aplicação
```
python app.py
```
Acesse no navegador:
👉 http://localhost:5000

Aproveite e faça várias listas de compras :)

---
## 🧪 Como rodar os testes automatizados (Pytest + PostgreSQL)

1. Criar o banco de dados de teste no PostgreSQL
Você deve criar manualmente (no pgAdmin ou no terminal) um banco chamado: **listacompras_test**

Passo a Passo:
1- Pelo pgAdmin:

2- Clique com botão direito em Databases

3- Create > Database

4- Em Database name: listacompras_test
5- Save

📌 Por que esse banco existe?
Ele é usado exclusivamente pelos testes, para que seu banco real não seja afetado.

5. Configurar o arquivo .env

Crie um arquivo .env dentro da pasta backend e insira:
TEST_DATABASE_URL=postgresql://postgres:SENHA@localhost:5432/listacompras_test

6. Rodar os testes com Pytest

Dentro da pasta /backend, execute: python -m pytest

Se tudo estiver correto, o resultado esperado é algo como:
===================== 5 passed in 1.22s =====================

7. (Opcional) Ver o teste rodando com prints
python -m pytest -s
---