# 🛒 Lista de Compras

Aplicação web simples para gerenciar **carrinhos de compras**, construída com **Flask**, **SQLAlchemy** e **HTML/CSS/JavaScript**.  
Permite criar, visualizar, editar e deletar carrinhos, além de adicionar itens individualmente ou em lote.

---

## 🚀 Funcionalidades

- Criar novos carrinhos
- Visualizar lista de carrinhos existentes
- Selecionar múltiplos carrinhos ao mesmo tempo
- Gerenciar carrinhos em quadrinhos flutuantes (adicionar itens, adicionar em lote, finalizar)
- Popups de aviso quando nenhuma seleção foi feita
- Confirmação antes de deletar carrinho, com opção de "não mostrar novamente"
- Banco de dados persistente (SQLite)

---

## 🛠️ Tecnologias

- **Backend:** Flask + SQLAlchemy
- **Banco de Dados:** SQLite (persistente em arquivo `meubanco.db`)
- **Frontend:** HTML, CSS (estilo Mercado Livre), JavaScript
- **Templates:** Jinja2

---

📖 Rotas principais
/ → Página inicial com lista de carrinhos

/create_cart → Criar novo carrinho (POST)

/delete/<id> → Deletar carrinho (POST)

/cart/<id> → Visualizar carrinho

/edit/<id> → Editar carrinho

Acesse em: http://localhost:5000

## Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

## Instalar dependências
pip install flask flask_sqlalchemy

## Rodar aplicação
python app.py

