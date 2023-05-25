from wakuwaku import create_app

app = create_app()

if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)