from app import create_app

app = create_app()

if __name__ == "__main__":
    # Local development only. Use a production WSGI server when deploying.
    app.run(debug=True)
