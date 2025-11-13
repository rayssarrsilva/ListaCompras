#chama create_app() e roda a aplicação
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

