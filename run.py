from app import create_app

app = create_app()

@app.route("/")
def index():
    return "<h1>API running</h1>"

if __name__ == "__main__":
    app.run(debug=True)