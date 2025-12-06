# 🛒 Lista de Compras

▶️ **[Assista ao sistema em ação]**
![listacompras](https://github.com/user-attachments/assets/026b500c-f04d-4087-8f69-4e1e6b3b15a1)

Aplicação web para gerenciar **carrinhos de compras**, construída com **Flask** para frontend, **FastAPI** para backend, **SQLAlchemy**, **PostgreSQL** para uso local, **Docker** para uso local e remoto em instancia na nuvem (aws) e **HTML/CSS/JavaScript**.  
Permite criar, visualizar, editar e deletar carrinhos, além de adicionar itens individualmente ou em lote e deletar o item selecionado no carrinho desejado

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
## 📦 Docker — Instalação e Configuração

Para rodar o sistema utilizando containers, é necessário instalar o Docker Desktop.
O Docker será usado para gerenciar o ambiente da aplicação e do banco de dados.

1. Instalação do Docker Desktop (Windows)

Baixar o Docker Desktop:
https://www.docker.com/products/docker-desktop

Executar o instalador .exe.

Marcar a opção:

Use WSL2 instead of Hyper-V

Finalizar a instalação e reiniciar o computador se solicitado.

2. Pré-requisitos

Windows 10/11 64 bits

Virtualização habilitada na BIOS

WSL2 instalado (apenas para Windows Home)
Para instalar o WSL2 (Após a instalação, reinicie o computador):
wsl --install

3. Verificando se o Docker funciona
docker --version
docker run hello-world
Se aparecer a mensagem “Hello from Docker!”, a instalação está correta.

## ▶️ Como rodar com Docker
Abra o terminal na raiz do projeto (onde está o docker-compose.yml).
Crie os arquivos de variáveis de ambiente:
.env (na raiz do projeto):
POSTGRES_DB=listacompras
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
SECRET_KEY=sua_secret_qualquer

backend/.env (dentro da pasta backend):
DATABASE_URL=postgresql://postgres:123@db:5432/listacompras
SECRET_KEY=sua_secret_qualquer ( a msm da outra)

Suba os containers:
docker compose up --build

✅ O comando:

Cria e inicia o PostgreSQL, FastAPI (backend) e Flask (frontend)
Cria automaticamente as tabelas no banco

Expõe:

Frontend: http://localhost:5000
Documentação da API: http://localhost:8000/docs

🛑 Como parar e limpar tudo
Parar os containers (mantém dados):
docker compose down

Parar e apagar tudo (incluindo o banco de dados):
docker compose down -v

####💡 Dicas de Desenvolvimento com Docker
As pastas ./frontend e ./backend são montadas nos containers via volumes, então alterações no código são refletidas imediatamente (sem precisar reconstruir).
O backend usa --reload (Uvicorn), então reinicia automaticamente ao salvar arquivos Python.

Para ver logs em tempo real:
docker compose logs -f

---
## 🌐 AWS 

Este projeto foi implantado na AWS usando:
- **EC2** (Ubuntu 22.04, t3.micro)
- **RDS** (PostgreSQL 15, db.t3.micro)
- **Docker Compose** para orquestração
- Tudo rodando dentro do **Free Tier de 12 meses**

✅ **Zero custo** — e totalmente reproduzível.

---
## ☁️ Deploy na AWS (EC2 + RDS)

Este projeto foi desenvolvido para rodar **gratuitamente** no **AWS Free Tier** (12 meses), aproveitando apenas recursos elegíveis para a camada gratuita:

- **EC2**: instância `t2.micro` (750h/mês gratuitas)  
- **RDS**: banco PostgreSQL `db.t3.micro` (750h/mês + 20 GB de armazenamento gratuito)

### Passos para deploy

1. **Crie uma instância EC2 (Ubuntu 22.04 LTS)**
   - Tipo de instância: `t2.micro`
   - Chave SSH: salve em local seguro
   - **Security Group** (regras de entrada):
     - Tipo: **SSH**, Porta: `22`, Origem: `Seu IP` ou `0.0.0.0/0` (temporário)
     - Tipo: **Custom TCP**, Porta: `5000`, Origem: `0.0.0.0/0`
     - Tipo: **Custom TCP**, Porta: `8000`, Origem: `0.0.0.0/0`

2. **(Opcional, mas recomendado) Crie um banco de dados RDS PostgreSQL**
   - Engine: **PostgreSQL 15**
   - Tipo de instância: `db.t3.micro`
   - Configuração:
     - **Publicly accessible**: `No` (mais seguro)
     - **VPC**: mesma da EC2
     - **Security Group do RDS**: permita tráfego de entrada na porta `5432` **apenas da EC2**
   - Após criado, atualize seu `.env` com o endpoint do RDS:
     ```env
     POSTGRES_HOST=listacompras-db.c32gauo20gy1.us-east-2.rds.amazonaws.com
     POSTGRES_PORT=5432
     POSTGRES_USER=seu_usuario
     POSTGRES_PASSWORD=sua_senha_forte
     POSTGRES_DB=listacompras
     ```

3. **Na instância EC2, execute os comandos abaixo:**
**    Atualize o sistema
**   sudo apt update && sudo apt upgrade -y

**    Instale Docker e Docker Compose
**   sudo apt install -y docker.io docker-compose

**    Adicione seu usuário ao grupo docker (para rodar sem sudo)
**   sudo usermod -aG docker $USER
   newgrp docker  # ou reinicie a sessão SSH

**    Clone o projeto
**   git clone https://github.com/seu-usuario/lista-compras.git
   cd lista-compras

**    Crie e edite o arquivo .env
**   cp .env.example .env
   nano .env  # preencha com suas credenciais

**    Suba a aplicação
**   docker-compose up --build -d


> Nota: os serviços estão atualmente **parados** para evitar consumo desnecessário, mas podem ser reiniciados em minutos com 2 comandos (docker-compose down
docker-compose up -d --build, no terminal EC2 da AWS); Rota publica: http://18.222.232.176:5000







